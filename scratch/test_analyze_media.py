import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.abspath("backend"))

from app.services.gemini_service import GeminiService
from app.services.synthid_service import SynthIDService
from app.services.forensics_service import ForensicsService
from app.services.c2pa_service import C2PAService

async def test_image(img_path):
    print(f"=== TESTING IMAGE: {os.path.basename(img_path)} ===")
    with open(img_path, "rb") as f:
        content = f.read()

    gemini_synthid = await GeminiService.analyze_image_synthid(content)
    print("Gemini SynthID Result:")
    print("  is_ai_generated:", gemini_synthid.get("is_ai_generated"))
    print("  verdict:", gemini_synthid.get("verdict"))
    print("  confidence:", gemini_synthid.get("confidence"))
    print("  headline:", gemini_synthid.get("headline"))
    print("  explanation:", gemini_synthid.get("plain_english_explanation"))
    print("  cues:", gemini_synthid.get("synthetic_cues_found"))
    print("  auth indicators:", gemini_synthid.get("authenticity_indicators"))

    synthid_res = SynthIDService.inspect_ai_generation(content, gemini_result=gemini_synthid)
    print("\nSynthID Service Result:")
    print("  verdict:", synthid_res.get("verdict"))
    print("  is_ai_generated:", synthid_res.get("is_ai_generated"))
    print("  confidence:", synthid_res.get("confidence"))
    print("  signals:", synthid_res.get("signals"))

    exif_meta, exif_ev = ForensicsService.inspect_exif(content)
    ela_bytes, ela_ev, boxes = ForensicsService.generate_ela(content)
    cm_ev = ForensicsService.detect_copy_move(content)
    c2pa_meta, c2pa_ev = C2PAService.inspect_credentials(content)

    is_ai_generated = synthid_res.get("is_ai_generated", False)
    has_tamper = is_ai_generated or any(e.severity == "CRITICAL" for e in (cm_ev + c2pa_ev + exif_ev))
    status = "AI_GENERATED" if is_ai_generated else ("POTENTIALLY_MANIPULATED" if has_tamper else "AUTHENTIC_NATURAL_PHOTO")
    print(f"\nFinal Status: {status} (has_tamper={has_tamper})")

if __name__ == "__main__":
    portrait_path = r"C:\Users\Ayush C S\.gemini\antigravity\brain\915c4e95-d713-43d1-970e-448ec19a032f\.user_uploaded\media_1790820687537.jpg"
    asyncio.run(test_image(portrait_path))
