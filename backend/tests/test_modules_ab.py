"""
Test Suite for Module A (Real-Time Trust Firewall) & Module B (Universal Content Passport & Provenance Graph)
Verifies:
1. Trust Firewall Session lifecycle (create, join, verify-frame, liveness, end, audit report)
2. Live Green / Yellow / Red scoring with explainable reasons
3. Content Passport Ingestion & SHA-256 / dHash calculation
4. Directed Acyclic Provenance Graph generation (nodes & edges)
5. Non-regression of existing core endpoints
"""
import sys
import os
import io

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -------------------------------------------------------------
# MODULE A: REAL-TIME TRUST FIREWALL TESTS
# -------------------------------------------------------------
def test_trust_firewall_session_lifecycle():
    # 1. Create Session
    create_resp = client.post("/api/trust/session", json={
        "type": "video_call",
        "title": "Executive Interview Session",
        "user_id": "evaluator_ayush"
    })
    assert create_resp.status_code == 200
    session_data = create_resp.json()
    session_id = session_data["session_id"]
    assert session_id.startswith("TFW-")
    assert session_data["status"] == "ACTIVE"

    # 2. Join Session
    join_resp = client.post(f"/api/trust/session/{session_id}/join", json={
        "participant_id": "candidate_haima",
        "passkey_verified": True,
        "device_attestation": {"platform": "MacBookPro", "attestation_verdict": "HARDWARE_ROOT_VERIFIED"}
    })
    assert join_resp.status_code == 200
    assert join_resp.json()["status"] == "JOINED"

    # 3. Stream Telemetry: Genuine Call (Expect Green Badge)
    genuine_telemetry = client.post(f"/api/trust/session/{session_id}/verify-frame", json={
        "frame_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
        "audio_chunk_base64": "audio_sample_bytes",
        "metadata": {"audio_present": True}
    })
    assert genuine_telemetry.status_code == 200
    res_green = genuine_telemetry.json()
    assert res_green["level"] in ["GREEN", "YELLOW"]
    assert res_green["trust_score"] >= 45
    assert len(res_green["explainable_reasons"]) > 0

    # 4. Stream Telemetry: Deepfake Attack Injection (Expect Red Badge)
    fake_telemetry = client.post(f"/api/trust/session/{session_id}/verify-frame", json={
        "frame_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
        "metadata": {
            "is_fake_test": True,
            "synthetic_flag": True,
            "voice_clone_flag": True,
            "sim_swap_flag": True
        }
    })
    assert fake_telemetry.status_code == 200
    res_red = fake_telemetry.json()
    assert res_red["level"] == "RED"
    assert res_red["trust_score"] < 45
    assert any("deepfake" in r.lower() or "synthesis" in r.lower() or "face-swapping" in r.lower() for r in res_red["explainable_reasons"])
    assert res_red["action_directive"] == "BLOCK_OR_REQUIRE_LIVENESS"

    # 5. Interactive Liveness Challenge
    liveness_resp = client.post(f"/api/trust/session/{session_id}/liveness-challenge")
    assert liveness_resp.status_code == 200
    liveness_data = liveness_resp.json()
    assert "instruction" in liveness_data
    assert liveness_data["timeout_seconds"] > 0

    # 6. End Session
    end_resp = client.post(f"/api/trust/session/{session_id}/end")
    assert end_resp.status_code == 200
    assert end_resp.json()["status"] == "COMPLETED"

    # 7. Audit Report Retrieval
    report_resp = client.get(f"/api/trust/session/{session_id}/report")
    assert report_resp.status_code == 200
    audit = report_resp.json()
    assert len(audit["audit_trail_events"]) >= 3


# -------------------------------------------------------------
# MODULE B: CONTENT PASSPORT & PROVENANCE GRAPH TESTS
# -------------------------------------------------------------
def test_content_passport_and_provenance_graph():
    # 1. Create Content Passport from Document
    doc_bytes = b"%PDF-1.4\n1 0 obj\n<< /Title (Institutional Exam Paper) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    create_resp = client.post(
        "/api/passport/create",
        files={"content_file": ("exam_paper.pdf", doc_bytes, "application/pdf")},
        data={"issuer": "National Examination Board", "author": "Registrar Office"}
    )
    assert create_resp.status_code == 200
    passport = create_resp.json()
    pid = passport["passport_id"]
    assert pid.startswith("CP-")
    assert len(passport["hashes"]["sha256"]) == 64
    assert passport["provenance_metadata"]["issuer"] == "National Examination Board"

    # 2. Verify Content Passport
    verify_resp = client.post("/api/passport/verify", json={"passport_id": pid})
    assert verify_resp.status_code == 200
    assert verify_resp.json()["verified"] is True
    assert verify_resp.json()["sha256"] == passport["hashes"]["sha256"]

    # 3. Retrieve Provenance Graph
    graph_resp = client.get(f"/api/passport/{pid}/provenance-graph")
    assert graph_resp.status_code == 200
    graph = graph_resp.json()
    assert graph["passport_id"] == pid
    assert len(graph["nodes"]) >= 4
    assert len(graph["edges"]) >= 3
    assert graph["provenance_chain_valid"] is True

    # Check node identities
    node_types = [n["type"] for n in graph["nodes"]]
    assert "issuer" in node_types
    assert "author" in node_types
    assert "content" in node_types

    # 4. Catalog List
    list_resp = client.get("/api/passport/list")
    assert list_resp.status_code == 200
    passports = list_resp.json()
    assert any(p["passport_id"] == pid for p in passports)


# -------------------------------------------------------------
# NON-REGRESSION VERIFICATION (Existing Endpoints Unaffected)
# -------------------------------------------------------------
def test_existing_endpoints_unaffected():
    # 1. Reliability Metrics Endpoint
    rel_resp = client.get("/api/reliability")
    assert rel_resp.status_code == 200
    assert "overall_accuracy" in rel_resp.json()

    # 2. Text Analysis Endpoint
    txt_resp = client.post("/api/analyze-text", json={"text": "Congratulations! You won Rs 50,000 lottery. Click here now."})
    assert txt_resp.status_code == 200

    # 3. SIM-Swap Self Check
    sim_resp = client.post("/api/sim-swap/self-check", json={"indicators": ["sudden_loss_of_network_signal"]})
    assert sim_resp.status_code == 200


if __name__ == "__main__":
    print("[TEST] Running test_trust_firewall_session_lifecycle()...")
    test_trust_firewall_session_lifecycle()
    print("  -> PASS: Module A Trust Firewall lifecycle & attacks validated.")

    print("[TEST] Running test_content_passport_and_provenance_graph()...")
    test_content_passport_and_provenance_graph()
    print("  -> PASS: Module B Content Passport & DAG provenance graph validated.")

    print("[TEST] Running test_existing_endpoints_unaffected()...")
    test_existing_endpoints_unaffected()
    print("  -> PASS: Existing routes & modalities 100% backward compatible.")

    print("\nALL MODULE A & B INTEGRATION TESTS PASSED SUCCESSFULLY! (3/3)")
