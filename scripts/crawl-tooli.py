#!/usr/bin/env python3
"""Collect Tooli's public game boards. pip install -r scripts/tooli-requirements.txt
HTML is cached outside the repo. Only game metadata and resized screenshots ship.
"""
import argparse
import hashlib
import io
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image

BASE = 'https://www.tooli.co.kr'
PLATFORMS = {'pc': 'PC', 'lounge': '오락실', 'boy': '게임보이', 'sfc': '슈퍼패미콤', 'md': '메가드라이브', 'msx': 'MSX', 'flash': '플래시'}
ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/tmp/nyimpe-tooli-cache')
CACHE.mkdir(exist_ok=True)


def get(url):
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + '.cache')
    if path.exists():
        return path.read_bytes()
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30, headers={'User-Agent': 'nyimpe-game-catalog/1.0 (+https://nyimpe.github.io/)'})
            response.raise_for_status()
            path.write_bytes(response.content)
            time.sleep(.25)
            return response.content
        except requests.RequestException as error:
            if getattr(error.response, 'status_code', None) in (401, 403) or attempt == 2:
                raise
            time.sleep(2 ** attempt)


def soup(url):
    return BeautifulSoup(get(url), 'html.parser')


def text(element):
    return re.sub(r'\s+', ' ', element.get_text(' ', strip=True)).strip() if element else ''


def listing(mid, page):
    url = f'{BASE}/{mid}' + (f'/page/{page}' if page > 1 else '')
    s = soup(url)
    entries = []
    # Both thumbnail-list boards and the flash table use td.title.
    for row in s.select('tr'):
        cell = row.select_one('td.title')
        if not cell:
            continue
        a = next((a for a in cell.select('a') if re.fullmatch(rf'/{mid}/\d+', urlparse(a.get('href', '')).path) and not urlparse(a.get('href', '')).fragment and 'thumb' not in a.get('class', [])), None)
        if not a:
            continue
        category = text(cell.select_one('.category'))
        thumb = cell.select_one('a.thumb img')
        entries.append({'id': f'{mid}-{urlparse(a["href"]).path.split("/")[-1]}', 'platform': mid, 'title': text(a), 'source': urljoin(BASE, urlparse(a['href']).path), 'sourceCategory': category, 'notice': 'notice' in row.get('class', []), 'thumbnail': urljoin(BASE, thumb['src']) if thumb else None})
    return entries


def collect():
    # Read robots before collecting. Only public board/list/detail/image paths.
    robots = get(BASE + '/robots.txt').decode('utf-8')
    (CACHE / 'robots.txt').write_text(robots)
    inventory = {}
    listed = {}
    for mid in PLATFORMS:
        s = soup(f'{BASE}/{mid}')
        count = int(re.sub(r'\D', '', text(s.select_one('.infoSum'))))
        last = s.select_one('.pagination .nextEnd')
        pages = int(last['href'].split('/')[-1]) if last and '/page/' in last['href'] else 1
        with ThreadPoolExecutor(max_workers=3) as pool:
            rows = [e for group in pool.map(lambda page: listing(mid, page), range(1, pages + 1)) for e in group]
        unique = {e['id']: e for e in rows}
        pinned = sum(e['notice'] for e in unique.values())
        if not count <= len(unique) <= count + pinned:
            raise RuntimeError(f'{mid}: expected {count} posts, collected {len(unique)}')
        listed.update(unique)
        inventory[mid] = {'label': PLATFORMS[mid], 'boardCount': count, 'pages': pages, 'collected': len(unique), 'pinned': pinned}
        print(f'{mid}: {len(unique)} posts / {pages} pages', flush=True)
    (CACHE / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2))
    results = []

    def detail(entry):
        try:
            s = soup(entry['source'])
        except requests.HTTPError as error:
            if error.response.status_code != 403:
                raise
            entry.update({'body': '', 'lines': [], 'images': [], 'embeds': [], 'access': '원문 비공개'})
            return entry
        content = s.select_one('.xe_content')
        if content is None:
            raise RuntimeError(f'No content: {entry["source"]}')
        # Exclude comments, sharing widgets and download links from description.
        for widget in content.select('script,style,.document_popup_menu'):
            widget.decompose()
        entry['body'] = text(content).removesuffix('이 게시물을').strip()
        entry['lines'] = [line.strip() for line in content.get_text('\n', strip=True).splitlines() if line.strip()]
        entry['images'] = list(dict.fromkeys(urljoin(BASE, image['src']) for image in content.select('img[src]') if '/files/attach/' in image['src'] or '/images/' in image['src']))
        entry['embeds'] = [urljoin(BASE, e.get('src', e.get('data', ''))) for e in content.select('embed,iframe,object')]
        return entry

    with ThreadPoolExecutor(max_workers=3) as pool:
        for i, entry in enumerate(pool.map(detail, listed.values()), 1):
            results.append(entry)
            if i % 50 == 0:
                (CACHE / 'raw-progress.json').write_text(json.dumps(results, ensure_ascii=False))
                print(f'details: {i}/{len(listed)}', flush=True)
    (CACHE / 'raw.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    (CACHE / 'collected-at.txt').write_text(datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat())
    print('Metadata collection complete.', flush=True)


def image(entry):
    if not entry['images'] and not entry['thumbnail']:
        return None
    output = ROOT / 'public/images/classic-games' / (entry['id'] + '.webp')
    if output.exists():
        with Image.open(output) as im:
            return {'src': '/images/classic-games/' + output.name, 'width': im.width, 'height': im.height, 'source': entry.get('imageSource')}
    for url in entry['images'] + ([entry['thumbnail']] if entry['thumbnail'] else []):
        # Only first-party raster image paths; never ROMs, archives, SWF, video.
        if urlparse(url).hostname != 'www.tooli.co.kr':
            continue
        try:
            with Image.open(io.BytesIO(get(url))) as im:
                im.seek(0)
                if im.width < 80 or im.height < 60:
                    continue
                im = im.convert('RGB')
                im.thumbnail((320, 240), Image.Resampling.LANCZOS)
                output.parent.mkdir(parents=True, exist_ok=True)
                im.save(output, 'WEBP', quality=55, method=6)
                return {'src': '/images/classic-games/' + output.name, 'width': im.width, 'height': im.height, 'source': url}
        except (requests.RequestException, OSError, ValueError):
            continue
    return None


def images():
    rows = json.loads((CACHE / 'raw.json').read_text())
    existing = json.loads((CACHE / 'images.json').read_text()) if (CACHE / 'images.json').exists() else {}
    def run(entry):
        return entry['id'], (existing.get(entry['id']) or image(entry)) if entry['images'] or entry['thumbnail'] else None
    result = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        for i, (key, value) in enumerate(pool.map(run, rows), 1):
            result[key] = value
            if i % 50 == 0:
                (CACHE / 'images.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
                print(f'images: {i}/{len(rows)}', flush=True)
    (CACHE / 'images.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'{sum(bool(x) for x in result.values())} images collected.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['collect', 'images'])
    args = parser.parse_args()
    collect() if args.stage == 'collect' else images()
