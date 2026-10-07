#!/usr/bin/env python3
"""Optimize referenced post images, then synchronize HTML, data and provenance.

Requires Pillow >= 11.3 with WebP and AVIF support. Run after regenerating posts.
Unchanged output hashes are skipped, so repeated runs never recompress them.
"""
import hashlib
import io
import json
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image, ImageOps, features

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/post-image-optimization.json'
SETTINGS = {
    'webpQuality': 55,
    'avifQuality': 45,
    'catalogMaxSize': [320, 240],
    'puzzleMaxSize': [320, 320],
    'conceptMaxSize': [960, 540],
    'atlasMaxSize': [1152, 1152],
}
IMAGE_TAG = re.compile(r'<img\b[^>]*>', re.I)
URL_ATTR = re.compile(r'\b(src|href)="(/images/[^"\s]+)"')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def limit(route):
    if route.startswith('/images/folklore-game/'):
        return SETTINGS['conceptMaxSize']
    if route.startswith('/images/korean-folklore/'):
        return SETTINGS['atlasMaxSize']
    if route.startswith('/images/logic-puzzles/'):
        return SETTINGS['puzzleMaxSize']
    return SETTINGS['catalogMaxSize']


def optimize():
    assert features.check('webp') and features.check('avif'), 'Pillow needs both WebP and AVIF encoders'
    pages = sorted((ROOT / 'posts').glob('*/index.html'))
    routes = sorted({urlsplit(match[1]).path for page in pages
                     for match in URL_ATTR.findall(page.read_text())})
    previous = read_json(REPORT) if REPORT.exists() else {}
    hashes = previous.get('outputHashes', {}) if previous.get('settings') == SETTINGS else {}
    changes = {}
    group_stats = defaultdict(Counter)
    new_hashes = {}
    skipped = 0
    # Finish encoding all files before updating site references or deleting originals.
    with tempfile.TemporaryDirectory(prefix='nyimpe-post-images-') as temp:
        staging = Path(temp)

        def convert(route):
            source = ROOT / 'public' / route.lstrip('/')
            original = source.read_bytes()
            original_hash = digest(original)
            if hashes.get(route) == original_hash:
                return route, None, original_hash
            with Image.open(io.BytesIO(original)) as opened:
                assert getattr(opened, 'n_frames', 1) == 1, f'Animated image needs a separate policy: {route}'
                original_size = opened.size
                image = ImageOps.exif_transpose(opened)
                image = image.convert('RGBA' if 'A' in image.getbands() or 'transparency' in image.info else 'RGB')
                image.thumbnail(tuple(limit(route)), Image.Resampling.LANCZOS)
                candidates = []
                for fmt, options in [
                    ('WEBP', {'quality': SETTINGS['webpQuality'], 'method': 6}),
                    ('AVIF', {'quality': SETTINGS['avifQuality'], 'speed': 6,
                              'subsampling': '4:4:4', 'max_threads': 1}),
                ]:
                    encoded = io.BytesIO()
                    image.save(encoded, fmt, **options)
                    candidates.append((encoded.getvalue(), fmt.lower()))
                if image.size == original_size and opened.format in ('WEBP', 'AVIF'):
                    candidates.append((original, opened.format.lower()))
                data, extension = min(candidates, key=lambda candidate: len(candidate[0]))
                # Some already tiny assets need no replacement at all.
                target_route = str(Path(route).with_suffix('.' + extension))
                output_hash = digest(data)
                target = staging / target_route.lstrip('/')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                with Image.open(target) as saved:
                    saved.load()
                    assert saved.size == image.size
                return route, {
                    'route': target_route, 'width': image.width, 'height': image.height,
                    'bytes': len(data), 'sha256': output_hash,
                    'original': {'file': 'public' + route, 'width': original_size[0],
                                 'height': original_size[1], 'bytes': len(original), 'sha256': original_hash},
                }, output_hash

        with ThreadPoolExecutor(max_workers=8) as pool:
            for index, (route, result, sha) in enumerate(pool.map(convert, routes), 1):
                if result:
                    changes[route] = result
                    group = route.split('/')[2]
                    group_stats[group]['images'] += 1
                    group_stats[group]['beforeBytes'] += result['original']['bytes']
                    group_stats[group]['afterBytes'] += result['bytes']
                    group_stats[group]['resized'] += (result['width'], result['height']) != (result['original']['width'], result['original']['height'])
                    new_hashes[result['route']] = sha
                else:
                    skipped += 1
                    new_hashes[route] = sha
                if index % 1000 == 0 or index == len(routes):
                    print(f'Encoded {index}/{len(routes)}; skipped {skipped}', flush=True)

        if not changes:
            print('All post images already optimized; no files changed.', flush=True)
            return
        for change in changes.values():
            destination = ROOT / 'public' / change['route'].lstrip('/')
            shutil.copyfile(staging / change['route'].lstrip('/'), destination)

    def updated_url(url):
        change = changes.get(urlsplit(url).path)
        return change['route'] + '?v=' + change['sha256'][:12] if change else url

    for page in pages:
        original = page.read_text()

        def image_tag(match):
            tag = match[0]
            src = re.search(r'\bsrc="([^"]+)"', tag)
            change = changes.get(urlsplit(src[1]).path) if src else None
            if change:
                for key in ('width', 'height'):
                    attr = f'{key}="{change[key]}"'
                    if re.search(rf'\b{key}="[^"]*"', tag):
                        tag = re.sub(rf'\b{key}="[^"]*"', attr, tag)
                    else:
                        tag = tag.replace('<img', '<img ' + attr, 1)
            return tag

        html = IMAGE_TAG.sub(image_tag, original)
        html = URL_ATTR.sub(lambda m: f'{m[1]}="{updated_url(m[2])}"', html)
        if html != original:
            page.write_text(html)

    def update_records(value):
        if isinstance(value, list):
            for item in value:
                update_records(item)
        elif isinstance(value, dict):
            src = value.get('src')
            file = value.get('file')
            route = urlsplit(src).path if isinstance(src, str) else '/' + file.removeprefix('public/') if isinstance(file, str) and file.startswith('public/images/') else None
            change = changes.get(route)
            if change:
                if src:
                    value['src'] = updated_url(src)
                if file:
                    value.setdefault('optimizedFrom', change['original'])
                    value['file'] = 'public' + change['route']
                for key in ('width', 'height', 'bytes', 'sha256'):
                    if key in value:
                        value[key] = change[key]
            image = value.get('image')
            if 'savedSha256' in value and isinstance(image, dict):
                change = changes.get(urlsplit(image['src']).path)
                if change:
                    value['savedSha256'] = change['sha256']
            for key, item in list(value.items()):
                if key != 'optimizedFrom' and isinstance(item, (dict, list)):
                    update_records(item)

    # Update current manifests; historical generation batches remain provenance.
    records = sorted((ROOT / 'public/data').glob('*.json')) + [
        ROOT / 'docs/jjang-gameplay-images.json',
        ROOT / 'docs/korean-folklore-images.json',
        ROOT / 'docs/folklore-game-concepts/redraw-2026-10-06/manifest.json',
    ]
    for path in records:
        data = read_json(path)
        before = json.dumps(data, ensure_ascii=False)
        update_records(data)
        if path.name == 'manifest.json':
            data['total_image_bytes'] = sum(asset['bytes'] for asset in data['assets'])
        if json.dumps(data, ensure_ascii=False) != before:
            write_json(path, data)

    # Delete replaced formats only after their HTML and metadata point to outputs.
    for route, change in changes.items():
        if route != change['route']:
            (ROOT / 'public' / route.lstrip('/')).unlink()
    stats = {group: dict(values) for group, values in sorted(group_stats.items())}
    report = {
        'settings': SETTINGS,
        'selection': 'Smallest of WebP, AVIF and an already smaller modern original; no upscaling.',
        'groups': stats,
        'processedImages': len(changes), 'skippedImages': skipped,
        'beforeBytes': sum(values['beforeBytes'] for values in stats.values()),
        'afterBytes': sum(values['afterBytes'] for values in stats.values()),
        'formats': dict(Counter(Path(route).suffix[1:] for route in new_hashes)),
        'outputHashes': dict(sorted(new_hashes.items())),
    }
    write_json(REPORT, report)
    print(json.dumps({key: value for key, value in report.items() if key != 'outputHashes'}, indent=2), flush=True)


if __name__ == '__main__':
    optimize()
