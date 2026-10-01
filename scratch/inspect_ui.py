with open('scratch/generate_index_html.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'type="file"' in line:
        print(f"Line {idx+1}: {line.strip()}")
        for k in range(max(0, idx-5), min(len(lines), idx+10)):
            print(f"  {k+1}: {lines[k].rstrip()}")
        print("-" * 50)
