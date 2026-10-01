with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for tab in ['case-tab', 'text-tab', 'screenshot-tab', 'url-tab', 'qr-tab', 'detect-tab', 'protect-tab', 'verify-tab', 'trace-tab']:
        if f'id="{tab}"' in l:
            print(f'{tab}: line {i+1}')
