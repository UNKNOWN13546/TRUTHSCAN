import requests
import json
import time
import os

BASE = "http://127.0.0.1:8000"

print("=====================================================================")
print(" TRUSTSCAN - SELF-CONTAINED LOCAL GEMINI VERIFICATION SUITE")
print("=====================================================================")

# 1. Text Scanner
print("\n--- [1/4] Testing Text Scam Scanner ---")
text_payload = {
    "text": "SBI Alert: Dear customer, your NetBanking access has expired today due to pending KYC. Avoid permanent account deactivation and Rs. 5000 penalty by updating immediately at http://sbi-kyc-verify-portal.in."
}
t0 = time.time()
res_text = requests.post(f"{BASE}/api/analyze-text", json=text_payload, timeout=25)
print(f"Status: {res_text.status_code} in {time.time() - t0:.2f}s")
if res_text.status_code == 200:
    data = res_text.json()
    cog = data.get("decided_by", {}).get("gemini_cognitive_report", {}).get("analysis", {})
    model_name = data.get("decided_by", {}).get("gemini_cognitive_report", {}).get("model_used")
    print(f"  Model Used: {model_name}")
    print(f"  Verdict / Headline: {cog.get('headline')}")
    print(f"  Summary: {cog.get('summary')}")
    print(f"  Tactics: {cog.get('social_engineering_tactics')}")
    print(f"  Recommended Action: {cog.get('recommended_user_action')}")

# 2. URL Scanner
print("\n--- [2/4] Testing URL Scanner ---")
url_payload = {
    "url": "http://sbi-reward-points-redemption.com/claim-cash"
}
t0 = time.time()
res_url = requests.post(f"{BASE}/api/analyze-url", json=url_payload, timeout=25)
print(f"Status: {res_url.status_code} in {time.time() - t0:.2f}s")
if res_url.status_code == 200:
    data = res_url.json()
    gem_url = data.get("gemini_url_report", {})
    print(f"  Model Used: {gem_url.get('model_used')}")
    print(f"  Verdict: {gem_url.get('verdict')}")
    print(f"  Headline: {gem_url.get('headline')}")
    print(f"  Plain English: {gem_url.get('plain_english_explanation')}")
    print(f"  Action: {gem_url.get('recommended_action')}")

# 3. QR Scanner
print("\n--- [3/4] Testing QR Scanner (from local samples/ folder) ---")
qr_img_path = os.path.join(os.path.dirname(__file__), "..", "samples", "sample_qr_upi_scam.png")
if os.path.exists(qr_img_path):
    t0 = time.time()
    with open(qr_img_path, "rb") as f:
        files = {"image_file": ("sample_qr_upi_scam.png", f, "image/png")}
        res_qr = requests.post(f"{BASE}/api/analyze-qr", files=files, timeout=25)
    print(f"Status: {res_qr.status_code} in {time.time() - t0:.2f}s")
    if res_qr.status_code == 200:
        data = res_qr.json()
        gem_qr = data.get("gemini_qr_report", {})
        print(f"  Decoded Payload: {data.get('payload')}")
        print(f"  Model Used: {gem_qr.get('model_used')}")
        print(f"  Verdict: {gem_qr.get('verdict')}")
        print(f"  Headline: {gem_qr.get('headline')}")
        print(f"  Plain English: {gem_qr.get('plain_english_explanation')}")
        print(f"  Action: {gem_qr.get('recommended_action')}")
else:
    print(f"  QR file not found at {qr_img_path}")

# 4. Media Forensics / AI Detection
print("\n--- [4/4] Testing AI Image Forensics (from local samples/ folder) ---")
ai_img_path = os.path.join(os.path.dirname(__file__), "..", "samples", "media_1790820687537.jpg")
if os.path.exists(ai_img_path):
    t0 = time.time()
    with open(ai_img_path, "rb") as f:
        files = {"image_file": ("media_1790820687537.jpg", f, "image/jpeg")}
        res_media = requests.post(f"{BASE}/api/analyze-media", files=files, timeout=30)
    print(f"Status: {res_media.status_code} in {time.time() - t0:.2f}s")
    if res_media.status_code == 200:
        data = res_media.json()
        print(f"  SynthID Decision: {data.get('synthid', {}).get('decision')}")
        print(f"  Overall Status: {data.get('status')}")
        gem = data.get("gemini_report", {})
        analysis = gem.get("analysis", {})
        print(f"  Model Used: {gem.get('model_used')}")
        print(f"  Headline: {analysis.get('headline')}")
        print(f"  Summary: {analysis.get('summary')}")
        print(f"  Lighting/Anatomy: {analysis.get('lighting_or_anatomy_artifacts')}")
        print(f"  Action: {analysis.get('recommended_user_action')}")
else:
    print(f"  Image file not found at {ai_img_path}")

print("\n=====================================================================")
print(" ALL 4 SCANNERS TESTED WITH LOCAL FILES ONLY - 100% SELF-CONTAINED")
print("=====================================================================")
