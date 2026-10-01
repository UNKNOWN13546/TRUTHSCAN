import json
import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    for _ in range(15):
        try:
            r = requests.get(BASE_URL + "/", timeout=1)
            if r.status_code == 200:
                print("Server is UP!")
                return True
        except Exception:
            time.sleep(1)
    return False

if not wait_for_server():
    print("Server failed to respond!")
    exit(1)

results = {}

# 1. Trust Case
try:
    r = requests.post(BASE_URL + "/api/case", data={"text_content": "URGENT: SBI Account locked. Click to update PAN."})
    data = r.json()
    gem = data.get("gemini_human_report")
    has_gem = gem is not None and "headline" in gem
    results["1. Trust Case"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["1. Trust Case"] = ("ERROR", str(e))

# 2. Text Scanner
try:
    r = requests.post(BASE_URL + "/api/analyze-text", json={"text": "Congratulations, you won Rs 50,000 lottery! Send OTP."})
    data = r.json()
    gem = data.get("gemini_human_report")
    has_gem = gem is not None and "headline" in gem
    results["2. Text Scanner"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["2. Text Scanner"] = ("ERROR", str(e))

# 3. URL Threat & VirusTotal
try:
    r = requests.post(BASE_URL + "/api/analyze-url", json={"url": "http://sbi-kyc-update.xyz/login"})
    data = r.json()
    gem = data.get("gemini_url_report")
    has_gem = gem is not None and "headline" in gem and "plain_english_explanation" in gem
    results["3. URL & VirusTotal"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["3. URL & VirusTotal"] = ("ERROR", str(e))

# 4. QR Scanner
try:
    # Synthetic 1x1 png or real qr
    files = {"image_file": ("test.png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82", "image/png")}
    r = requests.post(BASE_URL + "/api/analyze-qr", files=files)
    data = r.json()
    results["4. QR Scanner Endpoint"] = ("PASS", f"found={data.get('found')}")
except Exception as e:
    results["4. QR Scanner Endpoint"] = ("ERROR", str(e))

# 5. Media Detect
try:
    files = {"image_file": ("test.jpg", b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9", "image/jpeg")}
    r = requests.post(BASE_URL + "/api/analyze-media", files=files)
    data = r.json()
    gem = data.get("gemini_report", {}).get("analysis", {})
    results["5. Deepfake & Forensics"] = ("PASS", gem.get("headline") or gem.get("summary"))
except Exception as e:
    results["5. Deepfake & Forensics"] = ("ERROR", str(e))

# 6. Protect (SIM-Swap)
try:
    r = requests.post(BASE_URL + "/api/sim-swap/self-check", json={"indicators": ["signal_loss", "unexpected_esim_sms"]})
    data = r.json()
    gem = data.get("gemini_sim_report")
    has_gem = gem is not None and "headline" in gem and "plain_english_explanation" in gem
    results["6. Protect (SIM-Swap)"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["6. Protect (SIM-Swap)"] = ("ERROR", str(e))

# 7. Protect (k-Anonymity Breach)
try:
    r = requests.post(BASE_URL + "/api/breach/password-range", json={"prefix": "21BD1"})
    data = r.json()
    gem = data.get("gemini_breach_report")
    has_gem = gem is not None and "headline" in gem and "plain_english_explanation" in gem
    results["7. Protect (Breach)"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["7. Protect (Breach)"] = ("ERROR", str(e))

# 8. Exam Seal (Verify)
try:
    files = {"candidate_file": ("paper.pdf", b"%PDF-1.4 header", "application/pdf")}
    manifest = json.dumps({"issuer": "National Testing Agency", "title": "Physics Master 2026", "perceptual_hash": "0000000000000000"})
    r = requests.post(BASE_URL + "/api/seal/verify", files=files, data={"seal_payload_json": manifest})
    data = r.json()
    gem = data.get("gemini_seal_report")
    has_gem = gem is not None and "headline" in gem and "plain_english_explanation" in gem
    results["8. Exam Seal (Verify)"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["8. Exam Seal (Verify)"] = ("ERROR", str(e))

# 9. Trace (Extract & Fact-Check)
try:
    r = requests.post(BASE_URL + "/api/extract-claims", json={"text": "UNESCO declared Indian Anthem best in world! Forward to 10 friends immediately."})
    data = r.json()
    gem = data.get("gemini_trace_report")
    has_gem = gem is not None and "headline" in gem and "plain_english_explanation" in gem
    results["9. Trace (Claims & Fact-Check)"] = ("PASS", gem.get("headline")) if has_gem else ("FAIL", str(gem))
except Exception as e:
    results["9. Trace (Claims & Fact-Check)"] = ("ERROR", str(e))

print("\n--- TEST SUMMARY ACROSS ALL 9 MODULES ---")
for k, v in results.items():
    print(f"[{v[0]}] {k}: {v[1]}")
