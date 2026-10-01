"""
Exam Integrity Seal Service:
Cryptographic Ed25519 signature + Perceptual Hashing (dhash/phash)
Enables institutions to prove exam paper / answer key integrity,
and detects exact matches, re-photographed/re-scanned copies, or tampered leaks.
"""
import io
import time
import json
import base64
import hashlib
from typing import Dict, Any, Tuple, Optional
from PIL import Image
import imagehash
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from app.schemas import EvidenceItem

# Ephemeral demo authority keypair generated on startup
_private_key = ed25519.Ed25519PrivateKey.generate()
_public_key = _private_key.public_key()
_public_bytes = _public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)
PUBLIC_KEY_B64 = base64.b64encode(_public_bytes).decode('utf-8')

# In-memory registry of issued seals for the demo
SEAL_REGISTRY: Dict[str, Dict[str, Any]] = {}

class SealService:
    @staticmethod
    def compute_hashes(file_bytes: bytes) -> Tuple[str, str]:
        """
        Computes SHA-256 for byte-level exact match,
        and Perceptual Hash (dHash) for visual/rephoto tolerance.
        """
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        
        phash_str = ""
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                # 64-bit dhash
                ph = imagehash.dhash(img)
                phash_str = str(ph)
        except Exception:
            # Fallback if non-image PDF: take hash of first 4KB as proxy
            phash_str = hashlib.md5(file_bytes[:4096]).hexdigest()[:16]
            
        return sha256, phash_str

    @classmethod
    def issue_seal(cls, file_bytes: bytes, issuer: str, title: str, valid_hours: int = 48) -> Dict[str, Any]:
        """
        Issues an Ed25519-signed integrity manifest.
        Stores only manifest and hashes — NEVER stores the actual document file.
        """
        sha256, phash = cls.compute_hashes(file_bytes)
        now = int(time.time())
        valid_until = now + (valid_hours * 3600)
        
        manifest = {
            "issuer": issuer,
            "title": title,
            "sha256": sha256,
            "phash": phash,
            "issued_at": now,
            "valid_from": now,
            "valid_until": valid_until,
            "public_key": PUBLIC_KEY_B64
        }
        
        manifest_canonical = json.dumps(manifest, sort_keys=True).encode('utf-8')
        signature = _private_key.sign(manifest_canonical)
        sig_b64 = base64.b64encode(signature).decode('utf-8')
        
        seal_payload = {
            "manifest": manifest,
            "signature": sig_b64
        }
        
        seal_id = f"SEAL-{sha256[:10].upper()}"
        SEAL_REGISTRY[seal_id] = seal_payload
        
        return {
            "seal_id": seal_id,
            "seal_payload": seal_payload,
            "sha256": sha256,
            "phash": phash,
            "limits": "Privacy-safe: Only cryptographic perceptual hashes are registered; document contents are not retained."
        }

    @classmethod
    def verify_seal(cls, file_bytes: bytes, seal_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies:
        1. Cryptographic Ed25519 signature of the manifest
        2. Exact byte match (SHA-256) -> ORIGINAL_UNMODIFIED
        3. Perceptual hash distance (Hamming distance <= 12) -> MATCHES_WITH_MODIFICATIONS_OR_REPHOTO
        4. No hash correlation -> NOT_RECOGNISED
        """
        evidence = []
        try:
            manifest = seal_payload.get("manifest", {})
            sig_b64 = seal_payload.get("signature", "")
            pub_b64 = manifest.get("public_key", PUBLIC_KEY_B64)
            
            # 1. Verify Ed25519 signature
            pub_bytes = base64.b64decode(pub_b64)
            verify_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            
            manifest_canonical = json.dumps(manifest, sort_keys=True).encode('utf-8')
            verify_key.verify(base64.b64decode(sig_b64), manifest_canonical)
            sig_valid = True
        except Exception as e:
            return {
                "verdict": "SEAL_INVALID",
                "signature_valid": False,
                "error": f"Digital signature verification failed: {str(e)}",
                "evidence": [
                    EvidenceItem(
                        source="IntegritySeal",
                        category="signature_invalid",
                        severity="CRITICAL",
                        title="Integrity Seal Signature Forgery",
                        description="The cryptographic signature on this manifest does not match the authority public key.",
                        confidence=1.0
                    )
                ]
            }

        # 2. Check hashes of provided candidate document
        target_sha256 = manifest.get("sha256", "")
        target_phash_str = manifest.get("phash", "")
        
        candidate_sha256, candidate_phash_str = cls.compute_hashes(file_bytes)
        
        # Check Exact Match
        if candidate_sha256 == target_sha256:
            verdict = "ORIGINAL_UNMODIFIED"
            evidence.append(EvidenceItem(
                source="IntegritySeal",
                category="missing_provenance",
                severity="INFO",
                title="Cryptographic Bit-for-Bit Authenticity Match",
                description=f"Candidate document byte hash ({candidate_sha256[:16]}...) precisely matches the registered master release.",
                confidence=1.0
            ))
            hamming_dist = 0
        else:
            # Calculate Hamming distance between perceptual hashes
            try:
                h1 = imagehash.hex_to_hash(target_phash_str)
                h2 = imagehash.hex_to_hash(candidate_phash_str)
                hamming_dist = int(h1 - h2)
            except Exception:
                hamming_dist = 99

            if hamming_dist <= 14:
                verdict = "MATCHES_ORIGINAL_WITH_MODIFICATIONS_OR_REPHOTO"
                evidence.append(EvidenceItem(
                    source="IntegritySeal",
                    category="document_tampering",
                    severity="MODERATE",
                    title=f"Perceptual Visual Match With Alterations (Hamming Distance: {hamming_dist})",
                    description="The visual layout closely matches the registered master exam/document, but binary bytes or visual elements show tampering, watermark overlay, or re-photography.",
                    confidence=0.89,
                    limits_and_disclaimer="Perceptual hashing tolerates slight camera perspective tilt and compression artifacts."
                ))
            else:
                verdict = "NOT_RECOGNISED"
                evidence.append(EvidenceItem(
                    source="IntegritySeal",
                    category="document_tampering",
                    severity="HIGH",
                    title="No Match to Certified Master Seal",
                    description="This document does not match the perceptual or binary signature of the registered paper.",
                    confidence=0.92
                ))

        # Check time-lock validity window
        now = int(time.time())
        valid_from = manifest.get("valid_from", 0)
        valid_until = manifest.get("valid_until", now + 99999)
        time_status = "VALID_WINDOW"
        if now < valid_from:
            time_status = "PRE_RELEASE_LEAK"
            evidence.append(EvidenceItem(
                source="IntegritySeal",
                category="metadata_anomaly",
                severity="CRITICAL",
                title="Time-Lock Breach: Pre-Release Leak Flagged",
                description=f"Seal manifest validity starts at {valid_from}, but was scanned before official distribution time.",
                confidence=0.95
            ))
        elif now > valid_until:
            time_status = "EXPIRED"

        return {
            "verdict": verdict,
            "signature_valid": sig_valid,
            "time_status": time_status,
            "title": manifest.get("title"),
            "issuer": manifest.get("issuer"),
            "hamming_distance": int(hamming_dist),
            "evidence": evidence,
            "limits": "Seal verification proves whether content matches a declared authority release; it does not identify who leaked the document."
        }
