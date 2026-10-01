"""
Credential & Password Breach Service:
Implements HaveIBeenPwned k-anonymity protocol.
Full password and full hash never leave client or server memory.
"""
import hashlib
import httpx
from typing import Dict, Any

class BreachService:
    @staticmethod
    async def check_password_range(prefix5: str) -> Dict[str, Any]:
        """
        Queries HaveIBeenPwned range API for SHA-1 prefix (first 5 hex characters).
        Respects k-anonymity: returns suffix hashes and breach counts.
        """
        prefix5 = prefix5.strip().upper()
        if len(prefix5) != 5:
            return {"error": "Prefix must be exactly 5 hexadecimal characters."}
            
        url = f"https://api.pwnedpasswords.com/range/{prefix5}"
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(url, headers={"User-Agent": "TrustScan-Security-Audit"})
                if resp.status_code == 200:
                    lines = resp.text.splitlines()
                    results = {}
                    for line in lines:
                        if ":" in line:
                            suffix, count = line.split(":")
                            results[suffix.strip()] = int(count.strip())
                    return {
                        "status": "SUCCESS",
                        "prefix": prefix5,
                        "matches_count": len(results),
                        "data": results,
                        "privacy_guarantee": "k-anonymity: 16^35 possibilities remain concealed. Neither full password nor full hash was transmitted."
                    }
        except Exception as e:
            return {
                "status": "OFFLINE_FALLBACK",
                "prefix": prefix5,
                "data": {},
                "note": f"HIBP range API unreachable or rate-limited: {str(e)}"
            }

    @classmethod
    def test_local_hash(cls, password_plain: str, api_response_suffixes: Dict[str, int]) -> Dict[str, Any]:
        """
        Client/Server helper: hashes local password, checks suffix in received dictionary.
        """
        sha1_full = hashlib.sha1(password_plain.encode('utf-8')).hexdigest().upper()
        suffix = sha1_full[5:]
        breach_count = api_response_suffixes.get(suffix, 0)
        return {
            "pwned": breach_count > 0,
            "breach_occurrences": breach_count,
            "sha1_prefix": sha1_full[:5]
        }
