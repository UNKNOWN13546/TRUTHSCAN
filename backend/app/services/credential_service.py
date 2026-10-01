"""
Credential Service:
W3C-style Verifiable Credential generation, verification, and revocation list checks.
Uses Ed25519 digital signatures with JSON canonicalization.
"""
import json
import time
import base64
from typing import Dict, Any, List
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from app.schemas import EvidenceItem

# Demo credential authority keypair
_cred_priv = ed25519.Ed25519PrivateKey.generate()
_cred_pub = _cred_priv.public_key()
_cred_pub_b64 = base64.b64encode(_cred_pub.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)).decode('utf-8')

# Demo Revocation List (stores revoked credential IDs)
REVOCATION_REGISTRY = set(["VC-REVOKED-9912"])

class CredentialService:
    @classmethod
    def issue_credential(cls, subject_name: str, degree_or_cert: str, institution: str) -> Dict[str, Any]:
        cred_id = f"VC-{int(time.time()*1000)%1000000:06d}"
        now = int(time.time())
        
        payload = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "id": cred_id,
            "type": ["VerifiableCredential", "EducationalCredential"],
            "issuer": {
                "name": institution,
                "publicKey": _cred_pub_b64
            },
            "issuanceDate": now,
            "expirationDate": now + (365 * 24 * 3600),
            "credentialSubject": {
                "id": f"did:example:{abs(hash(subject_name)) % 100000}",
                "name": subject_name,
                "certification": degree_or_cert
            }
        }
        
        canonical = json.dumps(payload, sort_keys=True).encode('utf-8')
        sig = _cred_priv.sign(canonical)
        
        vc = {
            "credential": payload,
            "proof": {
                "type": "Ed25519Signature2020",
                "created": now,
                "proofPurpose": "assertionMethod",
                "proofValue": base64.b64encode(sig).decode('utf-8')
            }
        }
        return vc

    @classmethod
    def verify_credential(cls, vc_document: Dict[str, Any]) -> Dict[str, Any]:
        evidence: List[EvidenceItem] = []
        try:
            payload = vc_document.get("credential", {})
            proof = vc_document.get("proof", {})
            cred_id = payload.get("id", "")
            
            # Check Revocation
            if cred_id in REVOCATION_REGISTRY:
                return {
                    "valid": False,
                    "status": "REVOKED",
                    "evidence": [
                        EvidenceItem(
                            source="IdentityCheck",
                            category="document_tampering",
                            severity="CRITICAL",
                            title=f"Credential Revoked by Issuer ({cred_id})",
                            description="This verifiable credential is listed on the authority's cryptographic Revocation List.",
                            confidence=1.0
                        )
                    ]
                }
            
            # Verify Signature
            pub_b64 = payload.get("issuer", {}).get("publicKey", _cred_pub_b64)
            pub_bytes = base64.b64decode(pub_b64)
            verify_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            
            canonical = json.dumps(payload, sort_keys=True).encode('utf-8')
            sig_bytes = base64.b64decode(proof.get("proofValue", ""))
            verify_key.verify(sig_bytes, canonical)
            
            evidence.append(EvidenceItem(
                source="IdentityCheck",
                category="missing_provenance",
                severity="INFO",
                title="Cryptographic W3C-VC Signature Valid",
                description=f"Credential successfully verified against issuer key ({payload.get('issuer', {}).get('name')}).",
                confidence=1.0
            ))
            
            return {
                "valid": True,
                "status": "VERIFIED_GENUINE",
                "subject": payload.get("credentialSubject", {}),
                "issuer": payload.get("issuer", {}).get("name"),
                "evidence": evidence
            }
        except Exception as e:
            return {
                "valid": False,
                "status": "INVALID_SIGNATURE",
                "error": str(e),
                "evidence": [
                    EvidenceItem(
                        source="IdentityCheck",
                        category="signature_invalid",
                        severity="CRITICAL",
                        title="Invalid Verifiable Credential Signature",
                        description=f"Signature verification failure: {str(e)}",
                        confidence=1.0
                    )
                ]
            }
