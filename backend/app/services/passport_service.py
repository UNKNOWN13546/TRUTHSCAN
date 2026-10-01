"""
Trust Passport & SHA-256 Privacy Commitment Service:
Generates cryptographically random TS-XXXXX assessment passports,
canonical metadata JSON, and tamper-evident SHA-256 integrity commitments.
Never reveals or stores original sensitive text.
"""
import uuid
import json
import time
import hashlib
from typing import Dict, Any, Optional, List

# In-memory store for generated passports during session
PASSPORT_STORE: Dict[str, Dict[str, Any]] = {}

class PassportService:
    @staticmethod
    def generate_assessment_id() -> str:
        # Cryptographically secure random ID (e.g. TS-A7F29)
        return f"TS-{uuid.uuid4().hex[:5].upper()}"

    @classmethod
    def create_passport(
        cls,
        assessment_id: Optional[str],
        risk_level: str,
        evidence_count: int,
        sources: List[str]
    ) -> Dict[str, Any]:
        aid = assessment_id or cls.generate_assessment_id()
        now = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

        # Canonical metadata dictionary (strictly excludes private raw messages)
        canonical_meta = {
            "assessment_id": aid,
            "evidence_count": evidence_count,
            "risk_level": risk_level,
            "sources": sorted(sources),
            "timestamp": now
        }

        # SHA-256 Privacy Commitment
        canonical_bytes = json.dumps(canonical_meta, sort_keys=True).encode("utf-8")
        sha256_proof = hashlib.sha256(canonical_bytes).hexdigest()

        # Connect with ZKPrivacyService
        from app.services.zkp_privacy_service import ZKPrivacyService
        privacy_proof = ZKPrivacyService.create_privacy_proof(
            assessment_id=aid,
            risk_level=risk_level,
            evidence_count=evidence_count,
            statement=f"TrustScan Assessment {aid} classifies content as {risk_level}",
            proof_mode="commitment"
        )

        passport_data = {
            "assessment_id": aid,
            "risk_level": risk_level,
            "evidence_count": evidence_count,
            "sources": sources,
            "timestamp": now,
            "privacy_proof_sha256": sha256_proof,
            "privacy_commitment": sha256_proof,
            "verify_url": f"/verify/{aid}",
            "privacy_status": "PRIVATE_CONTENT_NOT_STORED",
            "proof_object": privacy_proof,
            "disclaimer": "This SHA-256 hash commits to the assessment metadata without storing or exposing original private content. It is an integrity commitment, not a full ZKP."
        }

        PASSPORT_STORE[aid] = passport_data
        return passport_data

    @classmethod
    def get_passport(cls, assessment_id: str) -> Optional[Dict[str, Any]]:
        if assessment_id in PASSPORT_STORE:
            return PASSPORT_STORE[assessment_id]
        from app.services.zkp_privacy_service import ZKPrivacyService
        pub = ZKPrivacyService.get_public_verification(assessment_id)
        if pub:
            return {
                "assessment_id": assessment_id,
                "risk_level": pub.get("risk_level", "HIGH"),
                "evidence_count": pub.get("evidence_count", 4),
                "sources": ["Gemini AI", "VirusTotal", "SynthID"],
                "timestamp": pub.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S UTC")),
                "privacy_proof_sha256": pub.get("privacy_commitment"),
                "privacy_commitment": pub.get("privacy_commitment"),
                "verify_url": f"/verify/{assessment_id}",
                "privacy_status": "PRIVATE_CONTENT_NOT_STORED",
                "disclaimer": "Public verification record retrieved. Original content was never stored."
            }
        return None
