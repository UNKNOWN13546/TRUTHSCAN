"""
Attack Chain Service:
Correlates evidence across Detect, Protect, Verify, Trace, Secure
into a 6-stage structured fraud attack chain:
1 CONTACT -> 2 MANIPULATION -> 3 CREDENTIAL -> 4 TAKEOVER -> 5 CASH_OUT -> 6 COVER
Highlights the specific point where the user can still break the kill-chain.
"""
from typing import List, Dict, Any
from app.schemas import EvidenceItem, AttackChainStage

STAGE_DEFINITIONS = [
    {
        "stage_number": 1,
        "stage_name": "CONTACT",
        "pillar_source": "Secure/Protect",
        "description": "Initial reach out via fake bank SMS, spoofed caller, or unsolicited message with lookalike sender.",
        "categories": ["identity_impersonation", "phishing_url", "first_seen_mismatch"],
        "break_action": "Block the sender immediately and independently verify through official published customer care numbers."
    },
    {
        "stage_number": 2,
        "stage_name": "MANIPULATION",
        "pillar_source": "Secure/Detect/Trace",
        "description": "Psychological pressure: artificial urgency, fabricated emergency, cloned voice note, or deepfake video.",
        "categories": ["media_manipulation", "social_engineering", "known_false_claim"],
        "break_action": "Pause. Recognize artificial panic triggers. Demand independent visual/audio proof or call a known shared contact."
    },
    {
        "stage_number": 3,
        "stage_name": "CREDENTIAL",
        "pillar_source": "Secure/Protect",
        "description": "Attempt to extract passwords, OTPs, net banking credentials, or Aadhaar OTP.",
        "categories": ["phishing_url", "metadata_anomaly"],
        "break_action": "NEVER share an OTP or banking password with any caller or via an unverified link."
    },
    {
        "stage_number": 4,
        "stage_name": "TAKEOVER",
        "pillar_source": "Protect",
        "description": "Unauthorized access attempt: SIM swap, unauthorized login, or remote control app installation (AnyDesk/TeamViewer).",
        "categories": ["sim_swap_indicator", "signature_invalid"],
        "break_action": "If cellular signal abruptly vanishes, call telecom operator from another phone and freeze banking immediately."
    },
    {
        "stage_number": 5,
        "stage_name": "CASH_OUT",
        "pillar_source": "Secure",
        "description": "Fraudulent fund siphoning via UPI collect requests, credit card charges, or crypto mule wallets.",
        "categories": ["upi_fraud"],
        "break_action": "Remember: entering your UPI PIN always DEBITS money from your account; you never enter a PIN to receive funds."
    },
    {
        "stage_number": 6,
        "stage_name": "COVER",
        "pillar_source": "Secure",
        "description": "Scammer instructs victim to keep the transaction secret, delete SMS history, or promises a delayed refund.",
        "categories": ["social_engineering"],
        "break_action": "Do not delete records. Preserve screenshots and immediately dial Cyber Crime 1930."
    }
]

class AttackChainService:
    @classmethod
    def evaluate_chain(cls, evidence_items: List[EvidenceItem]) -> List[AttackChainStage]:
        stages: List[AttackChainStage] = []
        observed_categories = set(e.category for e in evidence_items)
        category_to_ids: Dict[str, List[str]] = {}
        for e in evidence_items:
            category_to_ids.setdefault(e.category, []).append(e.id)

        first_breakable_assigned = False

        for defn in STAGE_DEFINITIONS:
            # Check if any associated category matched
            matched_cats = [c for c in defn["categories"] if c in observed_categories]
            detected = len(matched_cats) > 0
            
            matched_evidence_ids = []
            for c in matched_cats:
                matched_evidence_ids.extend(category_to_ids.get(c, []))

            # Identify if this is the active frontline stage where the user can break the scam
            can_break = False
            if detected and not first_breakable_assigned:
                can_break = True
                first_breakable_assigned = True

            stages.append(AttackChainStage(
                stage_number=defn["stage_number"],
                stage_name=defn["stage_name"],
                pillar_source=defn["pillar_source"],
                description=defn["description"],
                detected=detected,
                evidence_ids=matched_evidence_ids,
                can_user_break_here=can_break,
                action_to_break=defn["break_action"] if detected else ""
            ))

        return stages
