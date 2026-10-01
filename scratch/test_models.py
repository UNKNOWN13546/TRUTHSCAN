import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv('backend/.env')
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

candidates = ['gemini-2.5-flash', 'gemini-3.5-flash', 'gemini-3.6-flash', 'gemini-flash-latest', 'gemini-3.7-flash', 'gemini-3.8-flash']
for m in candidates:
    try:
        r = client.models.generate_content(
            model=m,
            contents='Return JSON {"ok": true}',
            config=types.GenerateContentConfig(response_mime_type='application/json')
        )
        print(f'{m}: OK -> {r.text.strip()[:40]}', flush=True)
    except Exception as e:
        print(f'{m}: ERR -> {type(e).__name__}: {str(e)[:60]}', flush=True)
