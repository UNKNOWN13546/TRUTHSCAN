"""
SIM-Swap Service:
1. Self-Check Wizard (Deterministic, client-side capable)
2. Immediate-Action Playbook (Cybercrime 1930, Sanchar Saathi, Bank Freeze)
3. CAMARA API Mock/Sandbox Provider adapter (Honest simulation labelling)
"""
from typing import List, Dict, Any
from app.schemas import EvidenceItem

class SimSwapService:
    KNOWN_INDICATORS = {
        "signal_loss": {
            "weight": 35,
            "title": "Sudden Total Loss of Cellular Signal",
            "desc": "Phone abruptly shows 'No Service' or 'SOS only' despite being in a known coverage area with an active plan."
        },
        "unexpected_esim_sms": {
            "weight": 40,
            "title": "Unprompted SIM/eSIM Activation Notification",
            "desc": "Received an SMS from telecom provider confirming SIM replacement, eSIM transfer, or porting request that you never initiated."
        },
        "unprompted_otps": {
            "weight": 25,
            "title": "Flood of Unexpected One-Time Passwords (OTPs)",
            "desc": "Repeated verification codes arriving for banking, WhatsApp, or email logins without your action."
        },
        "password_reset_emails": {
            "weight": 20,
            "title": "Multiple Account Security Alert Emails",
            "desc": "Notifications from Google, Apple, or banks reporting password change attempts from new locations."
        },
        "social_logout": {
            "weight": 25,
            "title": "Abrupt Logout from WhatsApp or Messaging Apps",
            "desc": "WhatsApp displays 'Your phone number is no longer registered with WhatsApp on this phone'."
        },
        "call_requesting_otp": {
            "weight": 30,
            "title": "Caller Posing as Telecom Agent Asking to Confirm Code",
            "desc": "Impersonator claims network upgrade/5G verification and asks you to read back an SMS code."
        }
    }

    @classmethod
    def evaluate_self_check(cls, selected_indicator_keys: List[str]) -> Dict[str, Any]:
        evidence: List[EvidenceItem] = []
        total_score = 0
        
        for key in selected_indicator_keys:
            if key in cls.KNOWN_INDICATORS:
                meta = cls.KNOWN_INDICATORS[key]
                total_score += meta["weight"]
                evidence.append(EvidenceItem(
                    source="SIMSwapCheck",
                    category="sim_swap_indicator",
                    severity="HIGH" if meta["weight"] >= 35 else "MODERATE",
                    title=meta["title"],
                    description=meta["desc"],
                    confidence=0.9
                ))

        if total_score >= 50:
            risk_level = "CRITICAL"
        elif total_score >= 25:
            risk_level = "HIGH"
        elif total_score > 0:
            risk_level = "MODERATE"
        else:
            risk_level = "NO_INDICATORS"

        playbook = [
            {"step": 1, "urgency": "IMMEDIATE (0-5 min)", "action": "Call your mobile network operator immediately from another phone. Request an emergency freeze on your SIM and ask for the recent SIM/eSIM swap log."},
            {"step": 2, "urgency": "CRITICAL (5-15 min)", "action": "Contact your primary banks and freeze UPI services and net banking credentials to prevent unauthorized account drain."},
            {"step": 3, "urgency": "HIGH (15-30 min)", "action": "Log in to your primary email (from a secure Wi-Fi connection) and check active session devices; invalidate all unauthorized sessions."},
            {"step": 4, "urgency": "REPORTING", "action": "Call National Cybercrime Helpline 1930 and file a complaint at https://cybercrime.gov.in."},
            {"step": 5, "urgency": "VERIFY NUMBERS", "action": "Check India's Sanchar Saathi portal (TAFCOP: https://sancharsaathi.gov.in) to verify all mobile connections registered against your Aadhaar/ID."}
        ]

        return {
            "risk_level": risk_level,
            "score": total_score,
            "evidence": evidence,
            "playbook": playbook,
            "disclaimer": "This self-check is deterministic and privacy-preserving. No phone numbers or private telemetry leave your device."
        }

    @classmethod
    def camara_lookup_mock(cls, msisdn_hash: str) -> Dict[str, Any]:
        """
        Modelled on GSMA Open Gateway / CAMARA SIM Swap API:
        GET /sim-swap/v0/check
        """
        # Demonstrates telco API contract with honest SIMULATED disclaimer
        is_mock_swapped = msisdn_hash.endswith("7") or msisdn_hash.endswith("9")
        return {
            "provider_type": "SIMULATED_MOCK_PROVIDER",
            "standard": "CAMARA SIM Swap API (GSMA Open Gateway)",
            "swapped_in_last_hours": 4 if is_mock_swapped else 0,
            "status": "SWAP_DETECTED" if is_mock_swapped else "NO_RECENT_SWAP",
            "notice": "SIMULATED — live network operator access requires dedicated enterprise carrier contract (Airtel/Jio/Vodafone CAMARA sandbox). Not claiming live carrier telemetry."
        }
