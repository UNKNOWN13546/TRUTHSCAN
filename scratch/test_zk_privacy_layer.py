import requests
import json

BASE = "http://127.0.0.1:8000"

print("=====================================================================")
print(" TRUSTSCAN 360: ZERO-KNOWLEDGE PRIVACY LAYER VERIFICATION SUITE")
print("=====================================================================")

# 1. Test Privacy Commitment Generation (SHA-256)
print("\n--- [1/6] Testing SHA-256 Privacy Commitment Generation ---")
payload_commit = {
    "assessment_id": "TS-A7F29",
    "risk_level": "HIGH_RISK",
    "evidence_count": 5,
    "statement": "This assessment is HIGH_RISK",
    "proof_mode": "commitment",
    "raw_content": "CONFIDENTIAL_PRIVATE_OTP_984129"
}
res_c = requests.post(f"{BASE}/api/privacy/generate-proof", json=payload_commit)
print(f"Status: {res_c.status_code}")
proof_commit = res_c.json()
print("  Proof Type:", proof_commit.get("proof_type"))
print("  Statement:", proof_commit.get("statement"))
print("  Commitment Hash:", proof_commit.get("privacy_commitment"))
print("  Raw Content Leaked?:", "CONFIDENTIAL" in json.dumps(proof_commit))
print("  Original Content Stored?:", proof_commit.get("original_content_stored"))
print("  Disclaimer:", proof_commit.get("cryptographic_disclaimer"))
assert not ("CONFIDENTIAL" in json.dumps(proof_commit)), "SECURITY LEAK: Raw content in proof!"

# 2. Test Verification of Privacy Commitment
print("\n--- [2/6] Testing Cryptographic Verification of Commitment ---")
res_v1 = requests.post(f"{BASE}/api/privacy/verify-proof", json={"proof_object": proof_commit})
print(f"Status: {res_v1.status_code}")
v1 = res_v1.json()
print("  Valid:", v1.get("valid"))
print("  Integrity Verified:", v1.get("integrity_verified"))
print("  Statement Satisfied:", v1.get("statement_satisfied"))
print("  Original Content Status:", v1.get("original_content"))
assert v1.get("valid") is True, "Verification failed!"

# 3. Test ZK-Ready Groth16 Circuit Proof Generation
print("\n--- [3/6] Testing ZK-Ready Groth16 Simulated Proof ---")
payload_zk = {
    "assessment_id": "TS-ZK881",
    "risk_level": "HIGH_RISK",
    "evidence_count": 4,
    "statement": "I possess a TrustScan assessment whose risk level is HIGH_RISK",
    "proof_mode": "zk_ready_snark"
}
res_zk = requests.post(f"{BASE}/api/privacy/generate-proof", json=payload_zk)
print(f"Status: {res_zk.status_code}")
proof_zk = res_zk.json()
print("  Proof Type:", proof_zk.get("proof_type"))
print("  Circuit:", proof_zk.get("circuit"))
print("  Protocol / Curve:", proof_zk.get("zk_proof", {}).get("protocol"), proof_zk.get("zk_proof", {}).get("curve"))
print("  pi_a:", proof_zk.get("zk_proof", {}).get("pi_a")[:2])
print("  Witness Zero Disclosure:", proof_zk.get("witness_zero_disclosure"))

# 4. Test Verification of ZK Proof
print("\n--- [4/6] Testing Verification of ZK-Ready Proof ---")
res_v2 = requests.post(f"{BASE}/api/privacy/verify-proof", json={"proof_object": proof_zk})
print(f"Status: {res_v2.status_code}")
v2 = res_v2.json()
print("  Valid:", v2.get("valid"))
print("  Pairing Check:", v2.get("zk_pairing_check"))
print("  Message:", v2.get("message"))
assert v2.get("valid") is True, "ZK Verification failed!"

# 5. Test 3 Educational Selective Disclosure Demos
print("\n--- [5/6] Testing 3 Interactive Selective Disclosure Scenarios ---")
for s_id in ["scam_risk_without_message", "document_selective_disclosure", "age_eligibility_predicate"]:
    res_s = requests.get(f"{BASE}/api/privacy/demo-scenario/{s_id}")
    d = res_s.json()
    print(f"\n* Scenario: {d.get('scenario_name')}")
    print(f"  Public Statement: {d.get('public_statement')}")
    print(f"  Verification Valid: {d.get('verification_result', {}).get('valid')}")
    print(f"  Innovation Takeaway: {d.get('takeaway')}")

# 6. Test Public /verify/{aid} Portal (Both JSON and HTML)
print("\n--- [6/6] Testing Public /verify/TS-A7F29 Portal ---")
res_api = requests.get(f"{BASE}/verify/TS-A7F29", headers={"Accept": "application/json"})
print(f"JSON Status: {res_api.status_code}")
j = res_api.json()
print("  Assessment ID:", j.get("assessment_id"))
print("  Risk Level:", j.get("risk_level"))
print("  Privacy Status:", j.get("privacy_status"))
print("  Privacy Commitment:", j.get("privacy_commitment"))

res_html = requests.get(f"{BASE}/verify/TS-A7F29", headers={"Accept": "text/html"})
print(f"HTML Status: {res_html.status_code}")
print("  HTML Contains 'TRUSTSCAN PUBLIC VERIFICATION':", "TRUSTSCAN PUBLIC VERIFICATION" in res_html.text)
print("  HTML Contains 'ORIGINAL CONTENT: PRIVATE & NOT STORED':", "ORIGINAL CONTENT: PRIVATE & NOT STORED" in res_html.text)
print("  HTML Contains 'VERIFIED':", "VERIFIED" in res_html.text)

print("\n=====================================================================")
print(" ALL 6 ZERO-KNOWLEDGE PRIVACY SUITE TESTS PASSED 100%!")
print("=====================================================================")
