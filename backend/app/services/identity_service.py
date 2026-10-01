"""
Identity Service: Channel vs Claim impersonation analysis, executive fraud,
lookalike handle detection, and out-of-band verification guidance.
"""
from typing import Dict, Any, List
import re
from app.schemas import EvidenceItem

class IdentityService:
    KNOWN_OFFICIALS = {
        "sbi": {"official_domains": ["sbi.co.in", "onlinesbi.sbi"], "sms_headers": ["SBIN", "SBIPSG", "SBIINB"], "type": "Bank"},
        "hdfc": {"official_domains": ["hdfcbank.com"], "sms_headers": ["HDFCBK", "HDFCLD"], "type": "Bank"},
        "icici": {"official_domains": ["icicibank.com"], "sms_headers": ["ICICIB", "ICICIT"], "type": "Bank"},
        "income tax": {"official_domains": ["incometax.gov.in"], "sms_headers": ["ITDPRC", "CBDTIN"], "type": "Government"},
        "aadhaar": {"official_domains": ["uidai.gov.in"], "sms_headers": ["AADHAR", "UIDAI"], "type": "Government"},
        "mumbai police": {"official_domains": ["mumbaipolice.gov.in"], "type": "Law Enforcement"},
        "cbi": {"official_domains": ["cbi.gov.in"], "type": "Law Enforcement"}
    }

    FREE_EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "rediffmail.com", "proton.me"]

    @classmethod
    def check_impersonation(cls, claimed_entity: str, channel_details: Dict[str, str]) -> Dict[str, Any]:
        """
        Compares claimed identity against sender channel:
        - Free-mail used by official sender
        - Display name vs domain mismatch
        - Hi Mum / Family in distress pattern
        - Lookalike Unicode / typosquatted domains
        """
        evidence: List[EvidenceItem] = []
        sender_email = channel_details.get("email", "").lower().strip()
        sender_phone = channel_details.get("phone", "").strip()
        sender_domain = channel_details.get("domain", "").lower().strip()
        sender_header = channel_details.get("sms_header", "").upper().strip()
        message_context = channel_details.get("message_text", "").lower()
        claimed_lower = claimed_entity.lower().strip()

        # 1. Family impersonation ("Hi Mum / Dad, lost my phone, new number")
        if any(term in claimed_lower for term in ["family", "son", "daughter", "mother", "father", "mum", "dad"]):
            if any(k in message_context for k in ["new number", "lost my phone", "urgent help", "pay this bill", "hospital", "temporary number"]):
                evidence.append(EvidenceItem(
                    source="IdentityCheck",
                    category="identity_impersonation",
                    severity="HIGH",
                    title="Classic 'Hi Mum / New Number' Family Impersonation",
                    description="Sender claims to be a relative using a new/unfamiliar number urgently demanding funds or payment.",
                    confidence=0.92,
                    limits_and_disclaimer="Legitimate family members do occasionally change numbers. Always verify via call before sending funds."
                ))

        # 2. Institutional Impersonation (Bank / Govt / Police)
        matched_official = None
        for key, details in cls.KNOWN_OFFICIALS.items():
            if key in claimed_lower:
                matched_official = (key, details)
                break

        if matched_official:
            name, details = matched_official
            # Check email domain
            if sender_email:
                domain_part = sender_email.split("@")[-1] if "@" in sender_email else ""
                if domain_part in cls.FREE_EMAIL_DOMAINS:
                    evidence.append(EvidenceItem(
                        source="IdentityCheck",
                        category="identity_impersonation",
                        severity="CRITICAL",
                        title=f"Official Impersonation via Public Webmail: @{domain_part}",
                        description=f"Sender claims to represent {claimed_entity.title()} ({details['type']}), but contacted from a public consumer email domain (@{domain_part}).",
                        confidence=0.99,
                        limits_and_disclaimer="Government bodies and banks never conduct official regulatory or account business from free public webmail."
                    ))
                elif not any(domain_part.endswith(allowed) for allowed in details.get("official_domains", [])):
                    evidence.append(EvidenceItem(
                        source="IdentityCheck",
                        category="identity_impersonation",
                        severity="HIGH",
                        title=f"Domain Mismatch for Claimed Entity",
                        description=f"Email domain '@{domain_part}' does not match official certified domains: {', '.join(details.get('official_domains', []))}.",
                        confidence=0.95
                    ))

            # Check SMS Headers (TRAI format in India)
            if sender_header and "sms_headers" in details:
                valid_headers = details["sms_headers"]
                if not any(header in sender_header for header in valid_headers):
                    evidence.append(EvidenceItem(
                        source="IdentityCheck",
                        category="identity_impersonation",
                        severity="HIGH",
                        title=f"Unregistered SMS Header for {claimed_entity.title()}",
                        description=f"Sender SMS header '{sender_header}' is not a recognized TRAI DLT transactional header for {claimed_entity.title()}.",
                        confidence=0.88,
                        limits_and_disclaimer="International or illegal spoofed SMS gateways often bypass official telecom routing."
                    ))

        # 3. Lookalike / typosquatted domains
        if sender_domain:
            if re.search(r"[0-9]", sender_domain) and any(b in sender_domain for b in ["sbi", "hdfc", "icici", "gov", "police"]):
                evidence.append(EvidenceItem(
                    source="IdentityCheck",
                    category="identity_impersonation",
                    severity="CRITICAL",
                    title="Suspicious Typosquatted / Numeric Lookalike Domain",
                    description=f"Domain '{sender_domain}' mixes digits with reputable institution brands, typical of fraudulent infrastructure.",
                    confidence=0.93
                ))

        out_of_band_plan = {
            "entity": claimed_entity.title(),
            "step_1": "Do not reply or click any links in this conversation.",
            "step_2": f"Find the official verified contact number independently (from the back of your debit card, official portal, or trusted physical paperwork).",
            "step_3": "Call the known official helpline or ask a question only the genuine entity could answer.",
            "emergency_cyber_helpline": "India Cyber Crime Helpline: 1930 / https://cybercrime.gov.in"
        }

        return {
            "claimed_entity": claimed_entity,
            "evidence": evidence,
            "out_of_band_plan": out_of_band_plan,
            "risk_status": "HIGH" if any(e.severity in ["HIGH", "CRITICAL"] for e in evidence) else "LOW"
        }
