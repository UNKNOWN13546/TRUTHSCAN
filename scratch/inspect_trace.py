with open('scratch/generate_index_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r"toolKey === 'trace'", text)]
for idx in matches:
    print(text[idx-50:idx+600])
    print('='*50)

matches2 = [m.start() for m in re.finditer(r"activeTool === 'trace'", text)]
for idx in matches2:
    print(text[idx-50:idx+400])
    print('='*50)
