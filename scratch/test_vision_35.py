import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv('backend/.env')
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

ai_img = r'C:\Users\Ayush C S\.gemini\antigravity\brain\915c4e95-d713-43d1-970e-448ec19a032f\ai_cyborg_portrait_1790839038320.jpg'
with open(ai_img, 'rb') as f:
    b = f.read()

prompt = """
You are TrustScan's Senior AI Image & Deepfake Forensic Analyst, operating under Google DeepMind SynthID principles.
Examine this image and determine if it is an AUTHENTIC NATURAL PHOTOGRAPH or an AI-GENERATED / SYNTHETIC IMAGE.
Return JSON:
{
  "is_ai_generated": true or false,
  "verdict": "AUTHENTIC_NATURAL_PHOTO" or "AI_GENERATED_SYNTHETIC_MEDIA",
  "confidence": 0.0 to 1.0,
  "headline": "...",
  "plain_english_explanation": "...",
  "synthetic_cues_found": ["..."],
  "authenticity_indicators": ["..."]
}
"""

resp = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        prompt,
        types.Part.from_bytes(data=b, mime_type="image/jpeg")
    ],
    config=types.GenerateContentConfig(response_mime_type="application/json")
)
print("gemini-3.5-flash vision result:\n", resp.text, flush=True)
