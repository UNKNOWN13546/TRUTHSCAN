"""
Claim Extraction Service:
Extracts atomic, checkable factual claims from incoming messages or OCR text.
Separates factual claims from opinion and emotional manipulation triggers.
"""
import re
from typing import List, Dict, Any
from app.schemas import EvidenceItem

class ClaimService:
    EMOTIONAL_TRIGGERS = [
        "forward to all", "share immediately", "breaking news", "shocking video",
        "secret leaked", "government doesn't want you to know", "cure discovered",
        "free recharges", "whatsapp will become paid", "arrest warrant issued",
        "modi announces", "urgent alert", "pass this to 10 friends"
    ]

    @classmethod
    def extract_atomic_claims(cls, text: str) -> Dict[str, Any]:
        """
        Parses text into checkable factual statements vs emotional persuasion.
        """
        claims = []
        emotional_flags = []
        text_lower = text.lower()

        # Check emotional urgency triggers
        for trigger in cls.EMOTIONAL_TRIGGERS:
            if trigger in text_lower:
                emotional_flags.append(trigger)

        # Break into sentences
        sentences = re.split(r'[.!?\n]+', text)
        for s in sentences:
            cleaned = s.strip()
            if len(cleaned) < 15:
                continue
            
            # Simple heuristic classifier for factual assertions:
            # Contains quantities, named entities, dates, or definitive verbs
            has_quant = bool(re.search(r'\b\d+\b|percent|crore|lakh|rupees|free', cleaned, re.IGNORECASE))
            has_event = bool(re.search(r'\bannounced|banned|died|approved|arrested|launched|closing|won\b', cleaned, re.IGNORECASE))
            
            claim_type = "FACTUAL_ASSERTION" if (has_quant or has_event) else "OPINION_OR_COMMENTARY"
            
            claims.append({
                "claim_text": cleaned,
                "type": claim_type,
                "is_checkable": claim_type == "FACTUAL_ASSERTION",
                "extracted_entities": re.findall(r'\b[A-Z][a-z]+\b', s)
            })

        evidence = []
        if emotional_flags:
            evidence.append(EvidenceItem(
                source="FactCheck",
                category="known_false_claim",
                severity="MODERATE",
                title="Emotional Urgency Virality Markers",
                description=f"Message employs viral manipulation patterns: '{', '.join(emotional_flags)}'. Designed to bypass rational skepticism.",
                confidence=0.85,
                limits_and_disclaimer="Emotional language alone does not disprove facts, but strongly correlates with viral disinformation."
            ))

        return {
            "total_extracted": len(claims),
            "claims": claims,
            "emotional_triggers": emotional_flags,
            "evidence": evidence
        }
