"""Package the generated art for the post; preserve composition and record provenance."""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[1]
TARGET = ROOT / 'public/images/board-game-concepts'
PAGE = ROOT / 'posts/board-game-concepts/index.html'
TARGET.mkdir(parents=True, exist_ok=True)
records = []
for name in ('art-01-03.json', 'art-04-06.json', 'art-07-09.json'):
    data = json.loads((DOCS / name).read_text())
    for item in data.get('assets', data.get('items', [])):
        number = int(item.get('id', item.get('number')))
        source = Path(item.get('original_path', item.get('source')))
        filename = f'concept-{number:02}.webp'
        destination = TARGET / filename
        with Image.open(source) as opened:
            original_size = opened.size
            output = opened.convert('RGB')
            output.thumbnail((960, 540), Image.Resampling.LANCZOS)
            output.save(destination, 'WEBP', quality=80, method=6)
            width, height = output.size
        raw = destination.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        records.append({
            'id': f'{number:02}', 'title': item['title'],
            'file': str(destination.relative_to(ROOT)),
            'src': f'/images/board-game-concepts/{filename}?v={sha[:12]}',
            'width': width, 'height': height, 'bytes': len(raw), 'sha256': sha,
            'source': str(source), 'sourceWidth': original_size[0],
            'sourceHeight': original_size[1], 'sourceBytes': source.stat().st_size,
            'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'promptFile': name,
        })
records.sort(key=lambda row: row['id'])
assert [row['id'] for row in records] == [f'{i:02}' for i in range(1, 10)]
(DOCS / 'manifest.json').write_text(json.dumps({
    'generator': 'built-in image_gen', 'created': '2026-10-07',
    'post': 'posts/board-game-concepts/index.html',
    'encoding': {'format': 'WebP', 'maxSize': [960, 540], 'quality': 80},
    'images': records,
}, ensure_ascii=False, indent=2) + '\n')
if PAGE.exists():
    html = PAGE.read_text()
    for row in records:
        base = row['src'].split('?')[0]
        html = re.sub(re.escape(base) + r'(?:\?v=[a-f0-9]+)?', row['src'], html)
        pattern = r'<img\b[^>]*src="' + re.escape(row['src']) + r'"[^>]*>'
        def update_image(match):
            tag = match[0]
            tag = re.sub(r'\bwidth="\d+"', f'width="{row["width"]}"', tag)
            return re.sub(r'\bheight="\d+"', f'height="{row["height"]}"', tag)
        html = re.sub(pattern, update_image, html)
    PAGE.write_text(html)
print(json.dumps({'images': len(records), 'totalBytes': sum(row['bytes'] for row in records),
                  'dimensions': sorted({(row['width'], row['height']) for row in records})}))
