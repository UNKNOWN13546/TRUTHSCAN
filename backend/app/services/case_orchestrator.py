"""
Trust Case Orchestrator:
Unifies all Six Pillars: Detect, Protect, Verify, Trace, Secure, Build Trust
Receives multi-modal inputs, dispatches to relevant analyzers, aggregates evidence,
and constructs the attack chain and transparent reliability explanation.
"""
import re
from typing import Dict, Any, List, Optional
from app.schemas import TrustCaseReport, PillarStatus, EvidenceItem
from app.services.forensics_service import ForensicsService
from app.services.c2pa_service import C2PAService
from app.services.identity_service import IdentityService
from app.services.simswap_service import SimSwapService
from app.services.document_service import DocumentService
from app.services.claim_service import ClaimService
from app.services.factcheck_service import FactCheckService
from app.services.provenance_service import ProvenanceService
from app.services.attack_chain import AttackChainService
from app.services.gemini_service import GeminiService
from app.services.deepfake_bench_service import DeepfakeBenchService

class CaseOrchestrator:
    @classmethod
    async def process_case(
        cls,
        text_content: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        pdf_bytes: Optional[bytes] = None,
        claimed_entity: Optional[str] = None,
        channel_sender: Optional[str] = None,
        sim_swap_answers: Optional[List[str]] = None,
        skip_gemini: bool = False
    ) -> TrustCaseReport:
        evidence_vault: List[EvidenceItem] = []
        pillars: Dict[str, PillarStatus] = {}
        gemini_res: Optional[Dict[str, Any]] = None

        if (text_content or image_bytes) and not skip_gemini:
            gemini_res = await GeminiService.analyze_multimodal_threat(text_content=text_content, image_bytes=image_bytes)

        # ----------------- 1. SECURE PILLAR -----------------
        # Inspect text for phishing URLs, urgency, and UPI fraud patterns
        sec_evidence_ids = []
        if text_content:
            text_low = text_content.lower()
            # Detect phishing URLs
            urls = re.findall(r'https?://[^\s]+', text_content)
            for u in urls:
                if any(bad in u.lower() for bad in ["bit.ly", "tinyurl", "ngrok", "apk", "login-sbi", "kyc-update", "free"]):
                    ev = EvidenceItem(
                        source="Rules",
                        category="phishing_url",
                        severity="CRITICAL",
                        title=f"High-Risk Phishing Link Pattern: {u[:40]}",
                        description=f"Link '{u}' uses deceptive domain obfuscation or unauthorized third-party redirection.",
                        exact_match=u,
                        confidence=0.97
                    )
                    evidence_vault.append(ev)
                    sec_evidence_ids.append(ev.id)

            # Detect UPI collect request scam
            if any(term in text_low for term in ["collect request", "approve request", "receive reward", "upi pin", "enter pin to get"]):
                ev = EvidenceItem(
                    source="Rules",
                    category="upi_fraud",
                    severity="CRITICAL",
                    title="UPI Collect Request Scam Detected",
                    description="Text instructs entering a UPI PIN to receive money. In Indian UPI architecture, entering your PIN only transfers money OUT of your bank.",
                    confidence=0.99
                )
                evidence_vault.append(ev)
                sec_evidence_ids.append(ev.id)

            # Detect loan app blackmail / harassment
            if any(term in text_low for term in ["contact all your relatives", "legal notice", "police coming", "defamation", "pay loan in 10 mins"]):
                ev = EvidenceItem(
                    source="Rules",
                    category="social_engineering",
                    severity="HIGH",
                    title="Predatory Loan App Harassment Language",
                    description="Coercive blackmail tactics threatening family reputation or imminent police detention.",
                    confidence=0.94
                )
                evidence_vault.append(ev)
                sec_evidence_ids.append(ev.id)

            if not image_bytes and gemini_res and gemini_res.get("evidence"):
                for ev in gemini_res["evidence"]:
                    evidence_vault.append(ev)
                    sec_evidence_ids.append(ev.id)

            pillars["secure"] = PillarStatus(
                status="RISK_DETECTED" if sec_evidence_ids else "OK",
                evidence_ids=sec_evidence_ids,
                summary=f"Analyzed message text. {len(sec_evidence_ids)} threat indicator(s) discovered.",
                limits="URL heuristic analysis checks structural keywords; live sandbox detonation requires external VirusTotal API integration."
            )
        else:
            pillars["secure"] = PillarStatus(status="NOT_RUN", summary="No message or URL input supplied.")

        # ----------------- 2. DETECT PILLAR (Media Manipulation) -----------------
        det_evidence_ids = []
        if image_bytes:
            # 1. Provenance / C2PA
            c2pa_info, c2pa_ev = C2PAService.inspect_credentials(image_bytes)
            for ev in c2pa_ev:
                evidence_vault.append(ev)
                det_evidence_ids.append(ev.id)

            # 2. EXIF Metadata
            exif_meta, exif_ev = ForensicsService.inspect_exif(image_bytes)
            for ev in exif_ev:
                evidence_vault.append(ev)
                det_evidence_ids.append(ev.id)

            # 3. ELA & Copy-Move
            ela_bytes, ela_ev, boxes = ForensicsService.generate_ela(image_bytes)
            for ev in ela_ev:
                evidence_vault.append(ev)
                det_evidence_ids.append(ev.id)

            cm_ev = ForensicsService.detect_copy_move(image_bytes)
            for ev in cm_ev:
                evidence_vault.append(ev)
                det_evidence_ids.append(ev.id)

            # 4. DeepfakeBench Spatial & Frequency Analysis
            df_res = DeepfakeBenchService.analyze_deepfake(image_bytes)
            for ev in df_res.get("evidence", []):
                evidence_vault.append(ev)
                det_evidence_ids.append(ev.id)

            # 5. Gemini Multimodal Vision Reasoning (Capped at MODERATE as opinion)
            if gemini_res and gemini_res.get("evidence"):
                for ev in gemini_res.get("evidence", []):
                    evidence_vault.append(ev)
                    det_evidence_ids.append(ev.id)

            has_manip = any(e.severity in ["MODERATE", "HIGH", "CRITICAL"] for e in (exif_ev + ela_ev + cm_ev + df_res.get("evidence", []) + gemini_res.get("evidence", [])))
            det_status = "POTENTIALLY_MANIPULATED" if has_manip else "NO_SIGNIFICANT_INDICATORS"
            pillars["detect"] = PillarStatus(
                status=det_status,
                evidence_ids=det_evidence_ids,
                summary=f"Ran image forensics (ELA, EXIF, Copy-Move, DeepfakeBench, Gemini Vision). Status: {det_status}.",
                limits="Forensics detects compression anomalies and digital stamping. DeepfakeBench checks spatial Face X-Ray boundaries & F3Net frequency rolls. Absence of indicators does NOT prove authenticity."
            )
        else:
            pillars["detect"] = PillarStatus(status="NOT_RUN", summary="No image/video media uploaded for forensic testing.")

        # ----------------- 3. PROTECT PILLAR (Identity & SIM-Swap) -----------------
        prot_evidence_ids = []
        if claimed_entity or channel_sender:
            id_res = IdentityService.check_impersonation(
                claimed_entity=claimed_entity or "Official Organization",
                channel_details={
                    "email": channel_sender if "@" in (channel_sender or "") else "",
                    "phone": channel_sender if "@" not in (channel_sender or "") else "",
                    "domain": channel_sender if "." in (channel_sender or "") else "",
                    "sms_header": channel_sender if len(channel_sender or "") <= 8 else "",
                    "message_text": text_content or ""
                }
            )
            for ev in id_res["evidence"]:
                evidence_vault.append(ev)
                prot_evidence_ids.append(ev.id)

        if sim_swap_answers:
            sim_res = SimSwapService.evaluate_self_check(sim_swap_answers)
            for ev in sim_res["evidence"]:
                evidence_vault.append(ev)
                prot_evidence_ids.append(ev.id)

        if prot_evidence_ids:
            pillars["protect"] = PillarStatus(
                status="RISK_DETECTED",
                evidence_ids=prot_evidence_ids,
                summary=f"Identity & SIM-Swap analysis flagged {len(prot_evidence_ids)} risk pattern(s).",
                limits="Self-check evaluates deterministic behavioral indicators without accessing private carrier subscriber logs."
            )
        elif claimed_entity or sim_swap_answers is not None:
            pillars["protect"] = PillarStatus(status="OK", summary="No known identity mismatch or SIM swap indicators reported.")
        else:
            pillars["protect"] = PillarStatus(status="NOT_RUN", summary="Identity credentials and SIM telemetry not submitted.")

        # ----------------- 4. VERIFY PILLAR (Documents & Seals) -----------------
        ver_evidence_ids = []
        if pdf_bytes:
            pdf_res = DocumentService.analyze_pdf(pdf_bytes)
            for ev in pdf_res["evidence"]:
                evidence_vault.append(ev)
                ver_evidence_ids.append(ev.id)
            pillars["verify"] = PillarStatus(
                status=pdf_res["verdict"],
                evidence_ids=ver_evidence_ids,
                summary=f"PDF document parsed. Verdict: {pdf_res['verdict']}.",
                limits="Inspects structural object trees and metadata; physical scanned paper should also be checked via ELA forensics."
            )
        else:
            pillars["verify"] = PillarStatus(status="NOT_RUN", summary="No PDF document or Exam Seal submitted for verification.")

        # ----------------- 5. TRACE PILLAR (Claims & Provenance) -----------------
        trace_evidence_ids = []
        if text_content:
            claim_res = ClaimService.extract_atomic_claims(text_content)
            for ev in claim_res["evidence"]:
                evidence_vault.append(ev)
                trace_evidence_ids.append(ev.id)
            # Query fact checks
            claims_to_check = [c["claim_text"] for c in claim_res["claims"] if c.get("is_checkable")]
            if claims_to_check:
                fc_res = await FactCheckService.query_fact_checks(claims_to_check[:3])
                for ev in fc_res["evidence"]:
                    evidence_vault.append(ev)
                    trace_evidence_ids.append(ev.id)

        if image_bytes:
            prov_res = ProvenanceService.check_image_provenance(image_bytes)
            for ev in prov_res["evidence"]:
                evidence_vault.append(ev)
                trace_evidence_ids.append(ev.id)

        if trace_evidence_ids:
            pillars["trace"] = PillarStatus(
                status="RISK_DETECTED",
                evidence_ids=trace_evidence_ids,
                summary=f"Trace engine identified {len(trace_evidence_ids)} claim or provenance anomaly(ies).",
                limits="Checks public fact-checks and reverse image crawl index; private WhatsApp group chains are not traceable."
            )
        elif text_content or image_bytes:
            pillars["trace"] = PillarStatus(status="OK", summary="No known false viral claims or recycled image matches identified.")
        else:
            pillars["trace"] = PillarStatus(status="NOT_RUN", summary="No claim text or image supplied for provenance tracing.")

        # ----------------- 6. BUILD TRUST (Transparent Decided-By) -----------------
        decided_by = {
            "rules_fired": [e.title for e in evidence_vault],
            "sources_used": list(set(e.source for e in evidence_vault)),
            "sources_unavailable": ["VirusTotal Live Sandbox (No API key)", "CAMARA Telecom Live Carrier Gateway (Demo Mock)"],
            "gemini_cognitive_report": gemini_res,
            "transparency_note": "Every finding in this Trust Report is grounded in a specific verifiable detector."
        }

        # Correlate Attack Chain
        attack_chain = AttackChainService.evaluate_chain(evidence_vault)

        # Overall verdict
        has_critical = any(e.severity == "CRITICAL" for e in evidence_vault)
        has_high = any(e.severity == "HIGH" for e in evidence_vault)
        if has_critical or has_high:
            overall = "ELEVATED_RISK"
        elif any(e.severity == "MODERATE" for e in evidence_vault):
            overall = "SUSPICIOUS"
        else:
            overall = "VERIFIED_CLEAN_INDICATORS"

        # Recommendations
        recommendations = []
        if any(e.category == "upi_fraud" for e in evidence_vault):
            recommendations.append({"action": "DO NOT enter UPI PIN", "reason": "PIN authorizes money deduction only, never credit."})
        if any(e.category == "identity_impersonation" for e in evidence_vault):
            recommendations.append({"action": "Verify out-of-band", "reason": "Contact the claimed entity via official published channels only."})
        if any(e.category == "sim_swap_indicator" for e in evidence_vault):
            recommendations.append({"action": "Dial 1930 & Call Carrier", "reason": "Initiate emergency freeze on mobile SIM and net banking."})
        if not recommendations:
            recommendations.append({"action": "Standard Caution", "reason": "Continue to practice zero-trust digital hygiene."})

        gemini_analysis = gemini_res.get("analysis") if gemini_res else None

        return TrustCaseReport(
            input_type="multi_modal",
            overall_verdict=overall,
            pillars=pillars,
            evidence_vault=evidence_vault,
            attack_chain=attack_chain,
            recommendations=recommendations,
            decided_by=decided_by,
            gemini_human_report=gemini_analysis
        )

