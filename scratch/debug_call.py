import asyncio, os, sys
sys.path.insert(0, os.path.abspath('backend'))
from app.services.gemini_service import GeminiService
from google.genai import types

ai_img = r'C:\Users\Ayush C S\.gemini\antigravity\brain\915c4e95-d713-43d1-970e-448ec19a032f\ai_cyborg_portrait_1790839038320.jpg'
with open(ai_img, 'rb') as f:
    b = f.read()

client = GeminiService.get_client()
print('Client obtained:', client is not None)

# Run GeminiService.analyze_image_synthid directly
async def run():
    res = await GeminiService.analyze_image_synthid(b)
    print("Result:", res)

asyncio.run(run())
