#!/usr/bin/env python3
"""Compress generated originals for the post and make diagnostic review sheets."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/folklore-game-concepts/2026-10-07'
DEST = ROOT / 'public/images/folklore-game-50'
DEST.mkdir(parents=True, exist_ok=True)
records = json.loads((DOCS / 'generation-records.json').read_text())
concepts = {g['id']: g for g in json.loads((DOCS / 'concepts.json').read_text())}
assert len({r['id'] for r in records}) == len(records)
previous = {a['id']: a for a in json.loads((DOCS / 'manifest.json').read_text())} if (DOCS / 'manifest.json').exists() else {}
manifest = []
for r in sorted(records, key=lambda r: r['id']):
    i = r['id']
    source = Path(r.get('revision', {}).get('source', r['source']))
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    target = DEST / f'concept-{i:02d}.webp'
    if target.exists() and previous.get(i, {}).get('sourceHash') == source_hash:
        width, height = previous[i]['width'], previous[i]['height']
    else:
        with Image.open(source) as im:
            im = im.convert('RGB')
            im.thumbnail((960, 540), Image.Resampling.LANCZOS)
            width, height = im.size
            im.save(target, 'WEBP', quality=65, method=6)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    manifest.append({'id': i, 'title': concepts[i]['title'], 'src': f'/images/folklore-game-50/{target.name}?v={digest[:12]}',
                     'width': width, 'height': height, 'bytes': target.stat().st_size,
                     'sha256': digest, 'source': str(source), 'sourceHash': source_hash,
                     'generator': 'built-in ImageGen', 'postprocess': 'resolution and WebP compression only',
                     'review': previous.get(i, {}).get('review', 'pending visual review')})
(DOCS / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
for start in range(1, 51, 10):
    ids = [a['id'] for a in manifest if start <= a['id'] < start+10]
    if not ids:
        continue
    sheet = Image.new('RGB', (2100, 530), '#172027')
    draw = ImageDraw.Draw(sheet)
    for i in ids:
        index = i-start
        x, y = (index % 5)*420, (index//5)*265
        with Image.open(DEST / f'concept-{i:02d}.webp') as im:
            im.thumbnail((420, 236))
            sheet.paste(im, (x, y+25))
        draw.text((x+8, y+7), f'{i:02d}', fill='#ffffdc')
    sheet.save(DOCS / f'review-{start:02d}-{start+9:02d}.jpg', quality=90)
print(json.dumps({'images': len(manifest), 'bytes': sum(a['bytes'] for a in manifest)}, ensure_ascii=False))
