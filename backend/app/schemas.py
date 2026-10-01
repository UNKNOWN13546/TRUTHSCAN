"""
Core schemas and contracts for TRUSTSCAN Six-Pillar Architecture.
Evidence-based, honest reporting with attack chain integration.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
import time

class EvidenceItem(BaseModel):
    id: str = Field(default_factory=lambda: f"EV-{uuid.uuid4().hex[:6].upper()}")
    source: str  # Forensics, C2PA, FactCheck, ReverseImage, IdentityCheck, SIMSwapCheck, DocumentCheck, IntegritySeal, Rules, GeminiVision
    category: str  # media_manipulation, missing_provenance, metadata_anomaly, document_tampering, signature_invalid, identity_impersonation, sim_swap_indicator, known_false_claim, first_seen_mismatch, social_engineering, phishing_url, upi_fraud
    severity: str  # INFO, LOW, MODERATE, HIGH, CRITICAL
    title: str
    description: str
    exact_match: Optional[str] = None
    bounding_box: Optional[List[float]] = None  # [ymin, xmin, ymax, xmax] normalized or [x, y, w, h]
    confidence: float = 0.8
    limits_and_disclaimer: Optional[str] = None

class PillarStatus(BaseModel):
    status: str  # OK, NOT_RUN, UNAVAILABLE, INCONCLUSIVE, POTENTIALLY_MANIPULATED, NO_SIGNIFICANT_INDICATORS, TAMPERING_INDICATORS, SIGNATURE_VALID, SIGNATURE_INVALID, RISK_DETECTED
    evidence_ids: List[str] = Field(default_factory=list)
    summary: str = ""
    limits: str = ""

class AttackChainStage(BaseModel):
    stage_number: int
    stage_name: str  # CONTACT, MANIPULATION, CREDENTIAL, TAKEOVER, CASH_OUT, COVER
    pillar_source: str
    description: str
    detected: bool = False
    evidence_ids: List[str] = Field(default_factory=list)
    can_user_break_here: bool = False
    action_to_break: str = ""

class TrustCaseReport(BaseModel):
    case_id: str = Field(default_factory=lambda: f"TS-{uuid.uuid4().hex[:6].upper()}")
    timestamp: float = Field(default_factory=time.time)
    input_type: str  # multi, text, image, document, qr, audio
    overall_verdict: str  # ELEVATED_RISK, SUSPICIOUS, VERIFIED_CLEAN_INDICATORS, INCONCLUSIVE
    honest_disclaimer: str = "Absence of detected indicators is NOT proof of authenticity. Detectors are probabilistic."
    pillars: Dict[str, PillarStatus]
    evidence_vault: List[EvidenceItem] = Field(default_factory=list)
    attack_chain: List[AttackChainStage] = Field(default_factory=list)
    recommendations: List[Dict[str, str]] = Field(default_factory=list)
    decided_by: Dict[str, Any] = Field(default_factory=dict)
    gemini_human_report: Optional[Dict[str, Any]] = None
