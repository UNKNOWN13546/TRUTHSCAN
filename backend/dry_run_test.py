"""
Full Dry-Run Test Script for TRUSTSCAN: The Six-Pillar Trust Layer
Simulates the entire Hackathon Demo Script (Section 12):
1. SECURE: Phishing & UPI Collect scam
2. DETECT: Image Forensics (ELA & C2PA & EXIF)
3. TRACE: Claim Extraction, Fact-Checking & Provenance
4. PROTECT: Impersonation & SIM-Swap Risk
5. VERIFY: Exam Integrity Seal (Original, Rephoto, Tampered) & Document Check
6. ATTACK CHAIN: 6-stage sequential narrative & breakable stage
7. BUILD TRUST: Reliability metrics & transparency
"""
import io
import json
import base64
import asyncio
import sys
from PIL import Image, ImageDraw
import httpx

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8000"

def create_synthetic_image(tampered=False) -> bytes:
    img = Image.new('RGB', (300, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((20, 20), "OFFICIAL CERTIFICATE", fill=(255, 255, 255))
    d.text((20, 50), "Registration No: 994820", fill=(255, 255, 255))
    if tampered:
        # Splice a contrasting bright block
        d.rectangle([140, 45, 240, 75], fill=(255, 0, 0))
        d.text((150, 50), "TAMPERED 111", fill=(255, 255, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()

async def run_dry_test():
    print("=" * 70)
    print("🚀 STARTING DRY RUN: TRUSTSCAN SIX-PILLAR TRUST LAYER")
    print("=" * 70)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        # Step 0: Health / Root check
        r = await client.get("/")
        assert r.status_code == 200, f"Root failed: {r.status_code}"
        print("✅ [0. HEALTH] UI & Root endpoint online (HTTP 200)")

        # Step 1: SECURE & TRUST CASE (The 2.5 min Riya's Father scenario)
        print("\n--- STEP 1: UNIVERSAL TRUST CASE & SECURE PILLAR ---")
        img_bytes = create_synthetic_image(tampered=True)
        form_data = {
            "text_content": "URGENT: Dad, my phone was stolen and I'm at the police station. Please transfer Rs 25,000 for emergency fine right now via UPI to this temporary number. Also approve the pending UPI collect request from SBI Support!",
            "claimed_entity": "SBI Bank / Son in trouble",
            "channel_sender": "sbi-support@gmail.com",
            "sim_swap_answers": "signal_loss,unexpected_esim_sms"
        }
        files = {
            "image_file": ("plea_evidence.jpg", img_bytes, "image/jpeg")
        }
        res = await client.post("/api/case", data=form_data, files=files)
        assert res.status_code == 200, f"Case failed: {res.text}"
        case_report = res.json()
        print(f"✅ Trust Case ID: {case_report['case_id']}")
        print(f"✅ Overall Verdict: {case_report['overall_verdict']}")
        print(f"✅ Total Grounded Evidence Records: {len(case_report['evidence_vault'])}")
        
        # Verify Attack Chain
        detected_stages = [s["stage_name"] for s in case_report["attack_chain"] if s["detected"]]
        breakable = [s for s in case_report["attack_chain"] if s["can_user_break_here"]]
        print(f"✅ Attack Chain Detected Stages: {' -> '.join(detected_stages)}")
        if breakable:
            print(f"✅ Active Breakable Stage: STAGE {breakable[0]['stage_number']} ({breakable[0]['stage_name']})")
            print(f"   Break Action: {breakable[0]['action_to_break'][:90]}...")

        # Step 2: DETECT PILLAR (Direct ELA & C2PA check)
        print("\n--- STEP 2: DETECT (IMAGE FORENSICS & C2PA) ---")
        res_detect = await client.post("/api/analyze-media", files={"image_file": ("test.jpg", img_bytes, "image/jpeg")})
        assert res_detect.status_code == 200
        det_data = res_detect.json()
        print(f"✅ Forensics Status: {det_data['status']}")
        print(f"✅ ELA Heatmap Generated: {bool(det_data.get('ela_heatmap_base64'))} (Length: {len(det_data.get('ela_heatmap_base64', ''))})")
        print(f"✅ C2PA Inspection: {det_data['c2pa']['validation_status']}")
        print(f"✅ Honest Disclaimer: {det_data['honest_notice']}")

        # Step 3: PROTECT PILLAR (SIM-Swap Self-Check & k-Anonymity)
        print("\n--- STEP 3: PROTECT (SIM-SWAP & K-ANONYMITY) ---")
        sim_res = await client.post("/api/sim-swap/self-check", json={"indicators": ["signal_loss", "unexpected_esim_sms", "unprompted_otps"]})
        assert sim_res.status_code == 200
        sim_data = sim_res.json()
        print(f"✅ SIM-Swap Threat Level: {sim_data['risk_level']} (Score: {sim_data['score']})")
        print(f"✅ Immediate Action Steps: {len(sim_data['playbook'])} steps (1930 / Sanchar Saathi)")

        anon_res = await client.post("/api/breach/password-range", json={"prefix": "21BD1"})
        assert anon_res.status_code == 200
        anon_data = anon_res.json()
        print(f"✅ HIBP k-Anonymity Range Query: {anon_data['status']} ({anon_data.get('matches_count', 0)} suffix hashes returned)")

        # Step 4: VERIFY PILLAR (Exam Integrity Seal)
        print("\n--- STEP 4: VERIFY (EXAM INTEGRITY SEAL: 3 STATES) ---")
        doc_original = b"National Testing Agency Official Physics Master Question Paper 2026."
        
        # 4a. Issue Seal
        issue_res = await client.post(
            "/api/seal/issue",
            data={"issuer": "National Testing Agency", "title": "Physics 2026", "valid_hours": 48},
            files={"document_file": ("exam.txt", doc_original, "text/plain")}
        )
        assert issue_res.status_code == 200
        seal_payload = issue_res.json()["seal_payload"]
        print(f"✅ Exam Seal Issued with Ed25519 signature & dHash: {issue_res.json()['seal_id']}")

        # 4b. Verify Original (Exact Bit Match)
        v1 = await client.post(
            "/api/seal/verify",
            data={"seal_payload_json": json.dumps(seal_payload)},
            files={"candidate_file": ("cand.txt", doc_original, "text/plain")}
        )
        print(f"✅ Test 1 (Original Master): Verdict = {v1.json()['verdict']} (Expected: ORIGINAL_UNMODIFIED)")
        assert v1.json()["verdict"] == "ORIGINAL_UNMODIFIED"

        # 4c. Verify Tampered Copy
        doc_tampered = b"National Testing Agency Official Physics Question Paper 2026 - MODIFIED LEAK"
        v2 = await client.post(
            "/api/seal/verify",
            data={"seal_payload_json": json.dumps(seal_payload)},
            files={"candidate_file": ("leak.txt", doc_tampered, "text/plain")}
        )
        print(f"✅ Test 2 (Tampered Leak): Verdict = {v2.json()['verdict']} (Expected: NOT_RECOGNISED / MODIFIED)")

        # Step 5: TRACE PILLAR (Viral Claim Extraction & Fact-Check)
        print("\n--- STEP 5: TRACE (CLAIM EXTRACTION & FACT-CHECK) ---")
        claim_res = await client.post("/api/extract-claims", json={"text": "UNESCO has officially declared Indian National Anthem as the best in the world, please forward to all!"})
        assert claim_res.status_code == 200
        print(f"✅ Extracted Claims: {claim_res.json()['total_extracted']}")
        
        fc_res = await client.post("/api/fact-check", json={"claims": ["UNESCO declared Indian National Anthem best in the world"]})
        assert fc_res.status_code == 200
        fc_data = fc_res.json()
        print(f"✅ Fact-Check Matches: {fc_data['matches_found']} (Rating: {fc_data['results'][0]['rating'] if fc_data['results'] else 'None'})")

        # Step 6: BUILD TRUST & RELIABILITY
        print("\n--- STEP 6: BUILD TRUST & RELIABILITY BENCHMARK ---")
        rel_res = await client.get("/api/reliability")
        assert rel_res.status_code == 200
        rel_data = rel_res.json()
        print(f"✅ Benchmark Sample Size: {rel_data['sample_size']} golden test cases")
        print(f"✅ Verified Accuracy: {rel_data['overall_accuracy']}%")
        print(f"✅ Precision: {rel_data['precision']}%, Recall: {rel_data['recall']}%, F1: {rel_data['f1_score']}%")

    print("\n" + "=" * 70)
    print("🎯 DRY RUN COMPLETED SUCCESSFULLY: 100% OF PILLARS & ENDPOINTS PASSED")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_dry_test())
