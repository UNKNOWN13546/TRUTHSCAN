import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import io

load_dotenv('backend/.env')
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

ai_img = r'C:\Users\Ayush C S\.gemini\antigravity\brain\915c4e95-d713-43d1-970e-448ec19a032f\ai_cyborg_portrait_1790839038320.jpg'
with Image.open(ai_img) as pil_im:
    pil_im.thumbnail((512, 512))
    buf = io.BytesIO()
    pil_im.save(buf, format='JPEG', quality=80)
    b = buf.getvalue()

models = ['gemini-3.5-flash', 'gemini-3.6-flash', 'gemini-2.5-flash-image', 'gemini-3.1-flash-image', 'gemini-2.0-flash']

for m in models:
    try:
        r = client.models.generate_content(
            model=m,
            contents=['Is this AI-generated or real? Answer one word.', types.Part.from_bytes(data=b, mime_type='image/jpeg')]
        )
        print(f'{m}: SUCCESS -> {r.text.strip()}', flush=True)
        break
    except Exception as e:
        print(f'{m}: FAIL -> {type(e).__name__}: {str(e)[:70]}', flush=True)
