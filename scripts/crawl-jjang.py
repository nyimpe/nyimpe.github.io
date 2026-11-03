#!/usr/bin/env python3
"""Collect only Jjang's public 2D and arcade catalogs; resume from an external cache."""
import argparse
import hashlib
import io
import html
import json
import math
import re
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.robotparser import RobotFileParser
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.jjanggame.co.kr/'
CACHE = Path('/tmp/nyimpe-jjang-cache')
PLATFORMS = {'2d': '2D 게임', 'old': '오락실 게임'}
LOCAL = threading.local()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def fetch(url):
    path = CACHE / 'responses' / hashlib.sha256(url.encode()).hexdigest()
    if path.exists():
        return path.read_bytes()
    if not hasattr(LOCAL, 'session'):
        LOCAL.session = requests.Session()
        LOCAL.session.headers.update({'User-Agent': 'nyimpe-game-catalog/1.0 (+https://nyimpe.github.io/)', 'Referer': BASE})
    for attempt in range(3):
        try:
            response = LOCAL.session.get(url, timeout=30)
            response.raise_for_status()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.content)
            time.sleep(0.15)
            return response.content
        except requests.RequestException as error:
            if error.response is not None and 400 <= error.response.status_code < 500 and error.response.status_code not in {408, 429}:
                raise
            if attempt == 2:
                raise
            time.sleep(1 + attempt)


def soup_for(raw):
    # Legacy unescaped &gtype must not be decoded as the HTML entity &gt.
    return BeautifulSoup(raw.decode('cp949', errors='replace').replace('&gtype', '&amp;gtype'), 'html.parser')


def listing(platform, page=1, genre=''):
    url = BASE + 'list.php?' + urlencode({'gtype': platform, 'gcate': genre, 'page': page, 'page_num': 50})
    soup = soup_for(fetch(url))
    count_node = soup.select_one('.s_title .s_r')
    assert count_node, ('Missing catalog count', url)
    count = int(count_node.get_text().replace(',', '').strip())
    entries = []
    for img in soup.select('.thumbnail_i img'):
        link = img.find_parent('a')
        query = parse_qs(urlparse(link['href']).query)
        assert query.get('gtype') == [platform], ('Unexpected category', link['href'])
        uid = query['u'][0]
        assert re.fullmatch(r'\d+', uid), uid
        preview = re.search(r"showPreviewImg\('([^']+)'", img.get('onmousemove', ''))
        entries.append({'id': platform + '-' + uid, 'uid': uid, 'platform': platform,
                        'listedTitle': img.get('title', ''), 'thumbnail': urljoin(BASE, img['src']),
                        'preview': urljoin(BASE, preview[1]) if preview else None,
                        'source': BASE + 'view.php?' + urlencode({'u': uid, 'gtype': platform})})
    genres = {}
    for link in soup.select('a[title]'):
        query = parse_qs(urlparse(link.get('href', '')).query)
        if 'list.php' in link.get('href', '') and query.get('gtype') == [platform] and query.get('gcate'):
            genres[query['gcate'][0]] = link['title']
    return {'url': url, 'count': count, 'entries': entries, 'genres': genres}


def detail(row):
    path = CACHE / 'details' / (row['id'] + '.json')
    if path.exists():
        cached = json.loads(path.read_text())
        if cached.get('titleSource') == 'document-title' and 'screenThumbnails' in cached:
            return cached
    raw = fetch(row['source']).decode('cp949', errors='replace')
    # Parse just game metadata/screenshots, never visitor comments or member profiles.
    text = re.search(r'<!--game text S-->(.*?)<!--game text E-->', raw, re.S)
    assert text, ('Missing game metadata', row['source'])
    soup = BeautifulSoup(text[1], 'html.parser')
    title = soup.select_one('.detail_t')
    assert title and title.get_text(strip=True), row['source']
    document_title = re.search(r'<title>(.*?)</title>', raw, re.S | re.I)
    assert document_title, ('Missing complete title', row['source'])
    full_title = BeautifulSoup(document_title[1], 'html.parser').get_text(' ', strip=True)
    full_title = re.split(r'\s+- 짱게임 -|\s+>\s+고전게임\s+>\s+짱게임$', full_title)[0]
    assert full_title and not full_title.endswith('짱게임'), ('Unknown title format', row['source'])
    alias = re.search(r'confirm\("\[([^\]]+)\] 게임을 찜리스트', raw)
    genre = next((node.select_one('font').get_text(strip=True) for node in soup.select('.left_detail')
                  if '게임분류' in node.get_text() and node.select_one('font')), None)
    assert genre is not None, ('Missing source genre field', row['source'])
    screen = re.search(r'<!--스크린샷 S-->(.*?)<!--스크린샷 E-->', raw, re.S)
    screenshots = []
    thumbnails = []
    if screen:
        for img in BeautifulSoup(screen[1], 'html.parser').select('img'):
            preview = re.search(r"showPreviewImg\('([^']+)'", img.get('onmousemove', ''))
            if preview:
                screenshots.append(urljoin(BASE, preview[1]))
                thumbnails.append(urljoin(BASE, img['src']))
    row = dict(row, title=full_title, titleSource='document-title',
               sourceAlias=html.unescape(alias[1]).replace('\\"', '"').replace("\\'", "'") if alias else '', sourceCategory=genre,
               screenshots=list(dict.fromkeys(screenshots)), screenThumbnails=list(dict.fromkeys(thumbnails)))
    save(path, row)
    return row


def collect():
    robots = fetch(BASE + 'robots.txt').decode()
    policy = RobotFileParser()
    policy.parse(robots.splitlines())
    assert all(policy.can_fetch('nyimpe-game-catalog', BASE + endpoint) for endpoint in ['list.php', 'view.php']), 'Source crawling policy disallows the requested catalog'
    home = soup_for(fetch(BASE)).get_text(' ', strip=True)
    inventory = {'collectedAt': datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),
                 'robots': robots.strip(), 'homeReportedCounts': {
                     '2d': int(re.search(r'2D 게임\s*:\s*([\d,]+)', home)[1].replace(',', '')),
                     'old': int(re.search(r'고전 오락실게임\s*:\s*([\d,]+)', home)[1].replace(',', ''))}, 'platforms': {}}
    # Homepage totals are a separate legacy summary, not the catalog's acceptance count.
    rows = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for platform in PLATFORMS:
            first = listing(platform)
            pages = math.ceil(first['count'] / 50)
            results = [first] + list(pool.map(lambda page: listing(platform, page), range(2, pages + 1)))
            beyond = listing(platform, pages + 1)
            assert not beyond['entries'], ('Nonempty page after expected last page', beyond['url'])
            assert all(r['count'] == first['count'] for r in results), 'Catalog changed while crawling'
            items = [row for result in results for row in result['entries']]
            assert len(items) == len({row['id'] for row in items}) == first['count'], 'Incomplete or duplicate catalog'
            genre_counts = {label: listing(platform, genre=code)['count'] for code, label in first['genres'].items()}
            inventory['platforms'][platform] = {'count': first['count'], 'uniqueListed': len(items),
                'pages': [{'page': i + 1, 'url': result['url'], 'items': len(result['entries'])} for i, result in enumerate(results)],
                'emptyNextPage': beyond['url'], 'sourceGenreCounts': genre_counts, 'genreCodes': first['genres']}
            rows.extend(items)
            print(platform, len(items), genre_counts, flush=True)
        save(CACHE / 'inventory.json', inventory)
        save(CACHE / 'listed.json', rows)
        details = []
        for row in pool.map(detail, rows):
            details.append(row)
            if len(details) % 100 == 0:
                print(f'Details {len(details)}/{len(rows)}', flush=True)
    for platform in PLATFORMS:
        actual = dict(Counter(row['sourceCategory'] for row in details if row['platform'] == platform))
        expected = inventory['platforms'][platform]['sourceGenreCounts']
        assert all(actual.get(label, 0) == count for label, count in expected.items()), (platform, actual, expected)
        assert set(actual) - set(expected) <= {''}, ('Unknown source genre outside menu', actual)
        assert sum(expected.values()) + actual.get('', 0) == inventory['platforms'][platform]['count']
        inventory['platforms'][platform]['detailGenreCounts'] = actual
    save(CACHE / 'inventory.json', inventory)
    save(CACHE / 'raw.json', details)
    print('Catalog and every detail genre match source counts', flush=True)


def screenshot(row):
    def placeholder(url):
        return Path(urlparse(url).path).name in {'snap_big.gif', 'snap_small.gif'}

    manifest = CACHE / 'images' / (row['id'] + '.json')
    if manifest.exists():
        result = json.loads(manifest.read_text())
        if result.get('image') and not placeholder(result['image']['source']) and (ROOT / 'public' / result['image']['src'].lstrip('/')).exists():
            return row['id'], result
    candidates = list(dict.fromkeys(row['screenshots'] + row['screenThumbnails'] + [url for url in [row['preview'], row['thumbnail']] if url]))
    failures = []
    for url in candidates:
        if placeholder(url):
            failures.append({'url': url, 'reason': '원문 공통 이미지 준비중 안내'})
            continue
        try:
            with Image.open(io.BytesIO(fetch(url))) as original:
                original.load()
                assert original.width >= 60 and original.height >= 40, 'Image too small to be a game screen'
                img = ImageOps.exif_transpose(original).convert('RGB')
                img.thumbnail((320, 240), Image.Resampling.LANCZOS)
                src = '/images/jjang-games/' + row['id'] + '.webp'
                output = ROOT / 'public' / src.lstrip('/')
                output.parent.mkdir(parents=True, exist_ok=True)
                img.save(output, 'WEBP', quality=55, method=6)
                result = {'image': {'src': src, 'width': img.width, 'height': img.height, 'source': url,
                    'kind': 'source-thumbnail' if url == row['thumbnail'] or url in row['screenThumbnails'] else 'source-screenshot'}, 'failures': failures}
                save(manifest, result)
                return row['id'], result
        except (requests.RequestException, OSError, AssertionError) as error:
            failures.append({'url': url, 'reason': str(error)})
    output = ROOT / 'public/images/jjang-games' / (row['id'] + '.webp')
    if output.exists():
        output.unlink()
    result = {'image': None, 'failures': failures, 'reason': '원문 이미지 준비중' if candidates and all(placeholder(url) for url in candidates) else ('원문 화면 이미지 확인 불가' if candidates else '원문에 화면 이미지 없음')}
    save(manifest, result)
    return row['id'], result


def images():
    rows = json.loads((CACHE / 'raw.json').read_text())
    results = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        for uid, result in pool.map(screenshot, rows):
            results[uid] = result
            if len(results) % 100 == 0:
                print(f'Screenshots {len(results)}/{len(rows)}', flush=True)
    save(CACHE / 'images.json', results)
    print('Screenshots', sum(bool(row['image']) for row in results.values()), 'of', len(rows), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['collect', 'images'])
    args = parser.parse_args()
    {'collect': collect, 'images': images}[args.stage]()
