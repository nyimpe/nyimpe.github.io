#!/usr/bin/env python3
"""Check every image and generated card, optionally compare all deployed bytes.
Usage: python scripts/verify-retro-assets.py [https://nyimpe.github.io] [--core]
"""
import hashlib
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITES = ['playretrogames', 'playretro-io', 'retrogames-onl-snes']


def verify():
    assets = []
    for site in SITES:
        data = json.loads((ROOT / f'public/data/{site}-games.json').read_text())
        report = json.loads((ROOT / f'docs/{site}-crawl-report.json').read_text())
        page = BeautifulSoup((ROOT / f'posts/{site}/index.html').read_text(), 'html.parser')
        cards = page.select('.classic-game')
        assert [c['id'] for c in cards] == [g['id'] for g in data['games']]
        assert len(data['games']) == report['games']
        assert len(set(g['source'] for g in data['games'])) == len(cards)
        for card, game in zip(cards, data['games']):
            assert card['data-platform'] == game['platform']
            assert card['data-genre'] == game['genre']
            assert card.select_one('h2').get_text() == game['title']
            assert card.select_one('.game-source a')['href'] == game['source']
            if game['image']:
                assert card.select_one('img')['src'] == game['image']['src']
                file = ROOT / 'public' / urlsplit(game['image']['src']).path.lstrip('/')
                with Image.open(file) as image:
                    assert image.size == (game['image']['width'], game['image']['height'])
                    image.load()
                assets.append((game['image']['src'], file))
            else:
                assert card.select_one('.game-image-missing')
        print(f'{site}: {len(cards)} matching cards, {sum(bool(g["image"]) for g in data["games"])} valid images', flush=True)
        assets.append((f'/data/{site}-games.json', ROOT / f'public/data/{site}-games.json'))

    if len(sys.argv) > 1:
        base = sys.argv[1]
        if '--core' in sys.argv:
            assets = [asset for asset in assets if asset[0].startswith('/data/')]
        for site in SITES:
            file = ROOT / f'dist/posts/{site}/index.html'
            page = BeautifulSoup(file.read_text(), 'html.parser')
            assets.append((f'/posts/{site}/index.html', file))
            for element in page.select('[src], [href]'):
                route = element.get('src') or element.get('href')
                if route.startswith('/assets/'):
                    assets.append((route, ROOT / 'dist' / route.lstrip('/')))
        assets = list(dict.fromkeys(assets))
        local = threading.local()
        cooldown_lock = threading.Lock()
        resume_at = 0
        def remote(asset):
            nonlocal resume_at
            route, file = asset
            if not hasattr(local, 'session'):
                local.session = requests.Session()
            for attempt in range(5):
                while True:
                    with cooldown_lock:
                        delay = resume_at - time.monotonic()
                    if delay <= 0:
                        break
                    time.sleep(min(delay, 5))
                try:
                    response = local.session.get(urljoin(base, route), timeout=40)
                    if response.status_code in (429, 502, 503, 504):
                        retry_after = response.headers.get('Retry-After', '0')
                        retry_seconds = int(retry_after) if retry_after.isdigit() else 0
                        backoff = 30 * 2 ** attempt if response.status_code == 429 else attempt + 1
                        with cooldown_lock:
                            resume_at = max(resume_at, time.monotonic() + max(backoff, retry_seconds))
                        print(f'HTTP {response.status_code}: backing off, attempt {attempt + 1}/5: {route}', flush=True)
                        response.raise_for_status()
                    response.raise_for_status()
                    assert hashlib.sha256(response.content).digest() == hashlib.sha256(file.read_bytes()).digest(), route
                    time.sleep(.25)
                    return route
                except requests.RequestException:
                    if attempt == 4:
                        raise
                    time.sleep(attempt + 1)
        with ThreadPoolExecutor(max_workers=2) as pool:
            for index, _ in enumerate(pool.map(remote, assets), 1):
                if index % 1000 == 0 or index == len(assets):
                    print(f'deployed bytes: {index}/{len(assets)} match', flush=True)


if __name__ == '__main__':
    verify()
