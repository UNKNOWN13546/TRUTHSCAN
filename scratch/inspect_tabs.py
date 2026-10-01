import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

tabs = re.findall(r'<div[^>]*id="([^"]+tab[^"]*)"', html)
print("Tabs:", tabs)

sections = re.findall(r'<!-- ===+ ([^=]+) ===+ -->', html)
print("Sections found:")
for s in sections:
    print(" -", s.strip())
