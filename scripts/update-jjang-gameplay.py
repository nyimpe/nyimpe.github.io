#!/usr/bin/env python3
"""Download reviewed external gameplay screenshots without collecting game files.
Run before build-jjang-catalog.py. Selection and provenance live in docs, not /tmp.
"""
import hashlib
import io
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs/jjang-gameplay-images.json'
CACHE = Path('/tmp/nyimpe-jjang-gameplay-cache')


def update():
    manifest = json.loads(MANIFEST.read_text())
    catalog = json.loads((ROOT / 'public/data/jjang-games.json').read_text())
    ids = {game['id'] for game in catalog['games']}
    assert set(manifest['entries']).isdisjoint(manifest['unresolved'])
    assert set(manifest['entries']) | set(manifest['unresolved']) == ids
    CACHE.mkdir(exist_ok=True)
    def save(pair):
        uid, entry = pair
        url = entry['source']
        assert urlparse(url).scheme == 'https'
        cached = CACHE / hashlib.sha256(url.encode()).hexdigest()
        if not cached.exists():
            for attempt in range(4):
                response = requests.get(url, timeout=45)
                if response.status_code in (429, 502, 503, 504):
                    time.sleep(max(float(response.headers.get('Retry-After', 0)), 5 * 2 ** attempt))
                    continue
                response.raise_for_status()
                cached.write_bytes(response.content)
                break
            assert cached.exists(), url
            # Vizzed explicitly requests a five-second crawl interval.
            time.sleep(5 if urlparse(url).hostname == 'www.vizzed.com' else .2)
        original = cached.read_bytes()
        assert hashlib.sha256(original).hexdigest() == entry['sha256'], (uid, 'Source bytes changed')
        if entry.get('gitBlobSha'):
            assert hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest() == entry['gitBlobSha']
        with Image.open(io.BytesIO(original)) as source:
            source.load()
            assert source.width >= 100 and source.height >= 80
            image = source.convert('RGB')
            image.thumbnail((320, 240), Image.Resampling.LANCZOS)
            target = ROOT / 'public/images/jjang-games' / (uid + '.webp')
            image.save(target, 'WEBP', quality=55, method=6)
        entry['savedSha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        entry['image'] = {'src': '/images/jjang-games/' + uid + '.webp?v=' + entry['savedSha256'][:12],
                          'width': image.width, 'height': image.height,
                          'source': url, 'sourcePage': entry['sourcePage'],
                          'kind': 'external-gameplay', 'matchedTitle': entry['matchedTitle'],
                          'selectionBasis': entry['selectionBasis'], 'matchType': entry['matchType']}
        if entry.get('displayNote'):
            entry['image']['displayNote'] = entry['displayNote']
        return uid, entry
    # Sequential Vizzed requests respect robots; independent raw GitHub assets use 3 workers.
    entries = manifest['entries']
    github = [(uid, e) for uid, e in entries.items() if urlparse(e['source']).hostname == 'raw.githubusercontent.com']
    others = [(uid, e) for uid, e in entries.items() if urlparse(e['source']).hostname != 'raw.githubusercontent.com']
    with ThreadPoolExecutor(max_workers=3) as pool:
        for uid, entry in pool.map(save, github):
            entries[uid] = entry
    for pair in others:
        uid, entry = save(pair)
        entries[uid] = entry
    for file in (ROOT / 'public/images/jjang-games').glob('*.webp'):
        if file.stem not in entries:
            file.unlink()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'gameplayScreenshots': len(entries), 'unresolved': len(manifest['unresolved'])}))


if __name__ == '__main__':
    update()
