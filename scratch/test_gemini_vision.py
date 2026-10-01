import os
import io
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

env_path = Path("backend/.env")
load_dotenv(env_path)
api_key = os.environ.get("GEMINI_API_KEY", "")

img = Image.new("RGB", (200, 200), color=(73, 109, 137))
d = ImageDraw.Draw(img)
d.text((20, 90), "Sample Test", fill=(255, 255, 0))
buf = io.BytesIO()
img.save(buf, format="JPEG")
img_bytes = buf.getvalue()

from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

prompt = """
You are TrustScan's Expert AI Image & Deepfake Forensic Analyst, operating under the principles of Google DeepMind SynthID.
Evaluate whether this image is an AUTHENTIC NATURAL PHOTOGRAPH or an AI-GENERATED / SYNTHETIC IMAGE.
Return JSON:
{
  "is_ai_generated": true or false,
  "verdict": "AUTHENTIC_NATURAL_PHOTO" or "AI_GENERATED_SYNTHETIC_MEDIA",
  "confidence": 0.0 to 1.0,
  "headline": "Punchy 3-6 word human headline",
  "plain_english_explanation": "2 simple sentences in plain human language."
}
"""

resp = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=[
        prompt,
        types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")
    ],
    config=types.GenerateContentConfig(response_mime_type="application/json")
)
print("Response text:", resp.text)
