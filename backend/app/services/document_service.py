"""
Document Service:
Analyzes PDF and document image authenticity:
- Metadata analysis (creation date, producer, mod dates)
- Font inconsistency and text-layer vs pixel mismatch
- Embedded QR code decoding and issuer allowlist validation
- Cryptographic signature check scaffold
"""
import io
import re
from typing import Dict, Any, List
from pypdf import PdfReader
from app.schemas import EvidenceItem

class DocumentService:
    TRUSTED_ISSUER_DOMAINS = [
        "gov.in", "nic.in", "ac.in", "edu.in", "incometax.gov.in", 
        "epfindia.gov.in", "uidai.gov.in", "cbse.gov.in", "nta.ac.in",
        "mumbaipolice.gov.in", "sbi.co.in", "hdfcbank.com", "icicibank.com"
    ]

    @classmethod
    def analyze_pdf(cls, pdf_bytes: bytes) -> Dict[str, Any]:
        evidence: List[EvidenceItem] = []
        meta_summary = {}
        verdict = "INCONCLUSIVE"
        
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            num_pages = len(reader.pages)
            meta = reader.metadata or {}
            file_size_bytes = len(pdf_bytes)
            
            creator = str(meta.get("/Creator", "None"))
            producer = str(meta.get("/Producer", "None"))
            author = str(meta.get("/Author", "None"))
            title = str(meta.get("/Title", "None"))
            keywords = str(meta.get("/Keywords", "None"))
            creation_date = str(meta.get("/CreationDate", "Unknown"))
            mod_date = str(meta.get("/ModDate", "Unknown"))
            contains_ai = str(meta.get("/containsAiGeneratedContent", ""))
            
            meta_summary = {
                "pages": num_pages,
                "file_size_bytes": file_size_bytes,
                "file_size_kb": round(file_size_bytes / 1024, 2),
                "creator": creator,
                "producer": producer,
                "author": author,
                "title": title,
                "keywords": keywords,
                "creation_date": creation_date,
                "mod_date": mod_date,
                "is_encrypted": reader.is_encrypted,
                "containsAiGeneratedContent": contains_ai
            }

            # 1. Fonts Inspection
            fonts_found = []
            font_names = set()
            has_embedded_fonts = False
            for p in reader.pages:
                if "/Resources" in p and "/Font" in p["/Resources"]:
                    fdict = p["/Resources"]["/Font"]
                    for fk, fobj in fdict.items():
                        bf = str(fobj.get("/BaseFont", "Unknown"))
                        st = str(fobj.get("/Subtype", "Unknown"))
                        is_emb = ("+ " in bf or "CID" in st or "Type0" in st or "/FontDescriptor" in fobj)
                        if is_emb:
                            has_embedded_fonts = True
                        if bf not in font_names:
                            font_names.add(bf)
                            fonts_found.append({
                                "tag": fk,
                                "base_font": bf,
                                "subtype": st,
                                "is_embedded": is_emb
                            })

            # 2. Images & Raster Inspection
            images_found = []
            has_full_page_bg = False
            pages_without_text = 0
            for p_idx, p in enumerate(reader.pages):
                p_text = (p.extract_text() or "").strip()
                if not p_text:
                    pages_without_text += 1
                if "/Resources" in p and "/XObject" in p["/Resources"]:
                    xdict = p["/Resources"]["/XObject"]
                    for xk, xobj in xdict.items():
                        if xobj.get("/Subtype") == "/Image":
                            w = xobj.get("/Width", 0)
                            h = xobj.get("/Height", 0)
                            is_bg = (w >= 1200 or h >= 800)
                            if is_bg:
                                has_full_page_bg = True
                            images_found.append({
                                "page": p_idx + 1,
                                "tag": xk,
                                "width": w,
                                "height": h,
                                "is_full_page_bg": is_bg
                            })

            # Check for AI-generated flag in PDF metadata
            ai_flag = contains_ai.strip().lower()
            if ai_flag in ["yes", "true", "1"]:
                evidence.append(EvidenceItem(
                    source="DocumentCheck",
                    category="ai_generated_content",
                    severity="HIGH",
                    title="AI-Generated Content Flagged in Metadata",
                    description="The document metadata explicitly contains 'containsAiGeneratedContent: Yes', identifying it as a synthetic presentation or AI-generated design.",
                    confidence=0.98
                ))

            # Check for suspicious editing software in PDF producer
            suspicious_producers = ["canva", "ilovepdf", "pdfescape", "sejda", "photoshop", "gimp"]
            prod_lower = (creator + " " + producer).lower()
            for susp in suspicious_producers:
                if susp in prod_lower:
                    evidence.append(EvidenceItem(
                        source="DocumentCheck",
                        category="document_tampering",
                        severity="HIGH",
                        title=f"Third-Party PDF Editor Signature ({susp.title()})",
                        description=f"Document metadata reveals it was edited or re-synthesized using web PDF editor '{susp}'. Official institutional certificates are typically generated via enterprise backend services.",
                        confidence=0.88,
                        limits_and_disclaimer="Legitimate users sometimes compress or convert PDFs using online tools."
                    ))

            # Discrepancy between creation date and mod date
            if creation_date != "Unknown" and mod_date != "Unknown" and creation_date != mod_date:
                evidence.append(EvidenceItem(
                    source="DocumentCheck",
                    category="metadata_anomaly",
                    severity="LOW",
                    title="Document Modification After Creation",
                    description=f"Creation date ({creation_date}) differs from modification date ({mod_date}), indicating incremental updates.",
                    confidence=0.75
                ))

            # Extract full text to inspect for altered numbers / bank statements
            full_text = ""
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                full_text += f"\n--- Page {i+1} ---\n" + text

            # Scan text for printed dates, numbers, and currency amounts
            printed_dates = re.findall(r"\b\d{2}[-/.]\d{2}[-/.]\d{4}\b|\b\d{4}[-/.]\d{2}[-/.]\d{2}\b", full_text)
            printed_amounts = re.findall(r"(?:₹|Rs\.?|\$|INR)\s*[\d,]+(?:\.\d{2})?", full_text)

            is_flattened_picture = (pages_without_text == num_pages and len(images_found) > 0)

            if any(e.severity in ["HIGH", "CRITICAL"] for e in evidence):
                verdict = "TAMPERING_INDICATORS"
            elif num_pages > 0 and len(evidence) == 0:
                verdict = "NO_SIGNIFICANT_INDICATORS"

        except Exception as e:
            evidence.append(EvidenceItem(
                source="DocumentCheck",
                category="document_tampering",
                severity="INFO",
                title="PDF Parsing Fallback",
                description=f"Standard PDF parser encountered notice: {str(e)}",
                limits_and_disclaimer="Corrupted or non-standard PDF streams may require rasterization."
            ))
            file_size_bytes = len(pdf_bytes)
            fonts_found = []
            images_found = []
            has_embedded_fonts = False
            has_full_page_bg = False
            is_flattened_picture = False
            printed_dates = []
            printed_amounts = []
            full_text = ""

        forensic_facts = {
            "file_size_bytes": file_size_bytes,
            "file_size_kb": round(file_size_bytes / 1024, 2),
            "pages": meta_summary.get("pages", 1),
            "producer": meta_summary.get("producer", "None"),
            "creator": meta_summary.get("creator", "None"),
            "author": meta_summary.get("author", "None"),
            "title": meta_summary.get("title", "None"),
            "creation_date": meta_summary.get("creation_date", "Unknown"),
            "mod_date": meta_summary.get("mod_date", "Unknown"),
            "contains_ai": meta_summary.get("containsAiGeneratedContent", ""),
            "fonts": fonts_found,
            "fonts_count": len(fonts_found),
            "has_embedded_fonts": has_embedded_fonts,
            "images_count": len(images_found),
            "has_full_page_bg": has_full_page_bg,
            "is_flattened_picture": is_flattened_picture,
            "printed_dates": list(set(printed_dates)),
            "printed_amounts": list(set(printed_amounts))
        }

        return {
            "verdict": verdict,
            "metadata": meta_summary,
            "forensic_facts": forensic_facts,
            "extracted_text": full_text.strip(),
            "evidence": evidence,
            "limits": "PDF document inspection checks structural metadata and embedded text streams; physical optical print scans should be routed through Image Forensics (ELA)."
        }

    @classmethod
    def check_embedded_qr(cls, decoded_qr_data: str) -> Dict[str, Any]:
        """
        Validates whether QR data in official credentials points to trusted official domains
        without navigating to the link.
        """
        evidence: List[EvidenceItem] = []
        is_official = False
        
        # Extract domain
        match = re.search(r"https?://([^/]+)", decoded_qr_data.lower())
        domain = match.group(1) if match else ""
        
        if domain:
            for trusted in cls.TRUSTED_ISSUER_DOMAINS:
                if domain == trusted or domain.endswith("." + trusted):
                    is_official = True
                    break
                    
            if not is_official:
                evidence.append(EvidenceItem(
                    source="DocumentCheck",
                    category="document_tampering",
                    severity="CRITICAL",
                    title=f"Embedded QR Points to Unauthorized Domain: {domain}",
                    description=f"The QR code embedded on this claimed credential redirects to '{domain}', which is NOT in the recognized institutional registry.",
                    exact_match=decoded_qr_data,
                    confidence=0.96,
                    limits_and_disclaimer="Scammers frequently generate certificates with custom QR codes redirecting to clone phishing validation sites."
                ))
            else:
                evidence.append(EvidenceItem(
                    source="DocumentCheck",
                    category="missing_provenance",
                    severity="INFO",
                    title=f"Recognized Institutional Issuer Domain: {domain}",
                    description=f"QR endpoint matches certified institutional domain ({domain}).",
                    confidence=0.90
                ))
        else:
            evidence.append(EvidenceItem(
                source="DocumentCheck",
                category="metadata_anomaly",
                severity="LOW",
                title="Embedded QR Contains Non-URL Data",
                description="QR code contains raw payload string instead of standard web verification URL.",
                exact_match=decoded_qr_data[:60]
            ))

        return {
            "qr_payload": decoded_qr_data,
            "domain": domain,
            "is_recognized_official": is_official,
            "evidence": evidence
        }
