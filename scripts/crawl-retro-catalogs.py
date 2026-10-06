#!/usr/bin/env python3
"""Collect public game metadata/images; never fetch game binaries or players.
Usage: python scripts/crawl-retro-catalogs.py [all|lists|details|images|build]
Requires scripts/tooli-requirements.txt. Cache stays outside the repository.
"""
import hashlib
import html
import io
import json
import re
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup, SoupStrainer
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/tmp/nyimpe-retro-cache')
DATE = datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat()
SITES = {
    'playretrogames': {'name': 'Play Retro Games', 'url': 'https://www.playretrogames.com/', 'scope': '전체 게임 목록의 모든 페이지'},
    'playretro-io': {'name': 'PlayRetro.io', 'url': 'https://www.playretro.io/', 'scope': '전체 게임 목록의 모든 페이지'},
    'retrogames-onl-snes': {'name': 'RetroGames.onl SNES', 'url': 'https://www.retrogames.onl/p/play-snes-games-online.html', 'scope': '요청한 슈퍼패미콤(SNES) A–Z 목록'},
}
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
LOCAL = threading.local()
ROBOTS = {}
PACE_LOCK = threading.Lock()
NEXT_REQUEST = {}
RATE_LIMITED = set()
PLATFORMS = {
    'atari-2600': 'Atari 2600', 'atari-7800': 'Atari 7800', 'atari-lynx': 'Atari Lynx',
    'capcom-cps-1': 'Capcom CPS 1', 'capcom-cps-2': 'Capcom CPS 2', 'capcom-cps-3': 'Capcom CPS 3',
    'coin-op-arcade': '오락실', 'gb': '게임보이', 'gbc': '게임보이 컬러',
    'gba': '게임보이 어드밴스', 'mame': 'MAME', 'nec-pc-engine': 'PC 엔진',
    'nec-pc-engine-cd': 'PC 엔진 CD', 'nec-turbografx-16': 'TurboGrafx-16',
    'nec-turbografx-16-cd': 'TurboGrafx-16 CD', 'neo-geo': '네오지오',
    'nintendo': '패미컴 / NES', 'nintendo-64': 'Nintendo 64', 'sega': '메가드라이브',
    'sega-32x': 'SEGA 32X', 'sega-cd': 'SEGA CD', 'sega-game-gear': '게임기어',
    'sega-master-system': '마스터 시스템', 'sega-saturn': '세가 새턴',
    'sony-playstation': 'PlayStation', 'super-nintendo': '슈퍼패미콤 / SNES', 'browser': '웹 브라우저',
}
LIST_PLATFORMS = {
    'Atari 2600': 'atari-2600', 'Atari 7800': 'atari-7800', 'Atari Lynx': 'atari-lynx',
    'Capcom CPS 1': 'capcom-cps-1', 'Capcom CPS 2': 'capcom-cps-2', 'Capcom CPS 3': 'capcom-cps-3', 'Coin Op Arcade': 'coin-op-arcade',
    'Nintendo Game Boy': 'gb', 'Game Boy': 'gb', 'Game Boy Color': 'gbc', 'Game Boy Advance': 'gba',
    'MAME': 'mame', 'MAME - Arcade': 'mame', 'Mame - Original Arcade': 'mame', 'NEC PC Engine': 'nec-pc-engine', 'NEC PC Engine CD': 'nec-pc-engine-cd',
    'NEC TurboGrafx 16': 'nec-turbografx-16', 'NEC TurboGrafx 16 CD': 'nec-turbografx-16-cd', 'Neo Geo': 'neo-geo', 'SNK Neo Geo': 'neo-geo', 'Nintendo NES': 'nintendo',
    'Nintendo 64': 'nintendo-64', 'Sega Genesis': 'sega', 'Sega 32X': 'sega-32x', 'Sega CD': 'sega-cd',
    'Sega Game Gear': 'sega-game-gear', 'Sega Master System': 'sega-master-system',
    'Sega Saturn': 'sega-saturn', 'Sony Playstation': 'sony-playstation', 'Sony PlayStation': 'sony-playstation', 'Nintendo Super NES': 'super-nintendo',
}
# Reuse the existing catalog's Korean genre vocabulary and basic-play explanations.
import importlib.util
spec = importlib.util.spec_from_file_location('tooli_catalog', ROOT / 'scripts/build-tooli-catalog.py')
tooli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tooli)
GENRES, BASICS = tooli.GENRES, tooli.BASICS
TAG_GENRES = [
    (r'role.?playing|\brpg\b', 'RPG'), (r'fight', '대전/격투'),
    (r'puzzle|board|mahjong|chess|\b(?:cards|poker|casino|gambling)\b', '퍼즐/보드'),
    (r'strategy|simulat|management|managament|manager|economy|defen|tactics', '전략/시뮬레이션'),
    (r'rac(e|ing)|sport|driving|\b(?:football|footbal|foobatll|soccer|baseball|basketball|golf|hockey|boxing|wrestling|wresting|tennis|pool|bowling|volleyball|ski|skiing|skating|skate|snowboard|snowboarding|cricket|rugby|snooker|dodgeball|dodge ball|bmx|f1|nfl|nba|nhl|fishing|surf|surfing|track)\b', '레이싱/스포츠'),
    (r'shoot|shmup|sniper|\bfps\b', '슈팅'),
    (r'rhythm|music', '리듬'), (r'education|creativ|learning|painting|quiz|\bmath\b', '창작/교육'),
    (r'compilation|collection', '미니게임/모음'),
    (r'action|arcade|platform|casual|beat.?em.?up|brawl|pinball', '액션/아케이드'), (r'adventure', '어드벤처'),
]
# Conservative series overrides resolve broad Action/Arcade tags, without claiming source taxonomy.
SERIES = [
    (r'tetris|tetrix|tetro|breaktris|puyo|columns|dr\.? mario|bust.a.move|puzzle|lemmings|sokoban|picross|mahjong|chess|solitaire|sudoku|mine.?sweeper|2048|1000 blocks|arkanoid|breakout|bricks? break', '퍼즐/보드'),
    (r'street fighter|mortal kombat|tekken|king of fighters|fatal fury|samurai shodown|art of fighting|killer instinct|clay.?fighter|virtua fighter|world heroes|last blade|dragon ball z.*(?:butouden|dimension)', '대전/격투'),
    (r'pokemon|pokémon|final fantasy|dragon quest|dragon warrior|earthbound|chrono trigger|breath of fire|lufia|romancing saga|secret of mana|tales of|ys iii|7th saga|\brpg\b', 'RPG'),
    (r'fire emblem|langrisser|front mission|ogre battle|civilization|harvest moon|simcity|sim city|nobunaga|romance of the three kingdoms', '전략/시뮬레이션'),
    (r'gradius|r.type|darius|parodius|aero fighters|axelay|raiden|twinbee|space invaders|alien invaders|ai vendetta|ascendshaft|astrofied|duck hunter|1942|1943|asteroids|star fox|biometal|contra|metal slug|doom|wolfenstein', '슈팅'),
    (r'f.zero|mario kart|sonic.*racing|gran turismo|outrun|out run|road rash|micro machines|nba\b|nfl\b|nhl\b|fifa|soccer|baseball|tennis|golf|bowling|football|basketball|hockey|boxing|punch.out|track.*field|olympic', '레이싱/스포츠'),
    (r'zelda|clock tower|monkey island|king.s quest|maniac mansion', '어드벤처'),
    (r'mario paint|acme animation|mario is missing|mario.s time machine', '창작/교육'),
]


def read_json(path):
    return json.loads(path.read_text())


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def session():
    if not hasattr(LOCAL, 'session'):
        LOCAL.session = requests.Session()
        LOCAL.session.headers['User-Agent'] = UA
    return LOCAL.session


def fetch(url, binary=False):
    host = urlparse(url).netloc
    if host in ROBOTS and not ROBOTS[host].can_fetch(UA, url):
        raise RuntimeError('robots.txt disallows ' + url)
    digest = hashlib.sha256(url.encode()).hexdigest()
    path = CACHE / ('media' if binary else 'html') / digest
    if path.exists():
        return path.read_bytes() if binary else path.read_text()
    if host in RATE_LIMITED:
        raise RuntimeError('Source rate limited; cached metadata retained')
    for attempt in range(4):
        try:
            with PACE_LOCK:
                wait = max(0, NEXT_REQUEST.get(host, 0) - time.monotonic())
                interval = 1.25 if host == 'blogger.googleusercontent.com' else (0.4 if host == 'www.playretro.io' else 0.15)
                NEXT_REQUEST[host] = time.monotonic() + wait + interval
            if wait:
                time.sleep(wait)
            response = session().get(url, timeout=45)
            if response.status_code == 429:
                cooldown = max(30, int(response.headers.get('Retry-After', '30')))
                # FIFE can limit an individual Blogger image while other images
                # remain available; do not discard the entire host's inventory.
                if binary and urlparse(response.url).netloc == 'blogger.googleusercontent.com':
                    if attempt >= 2:
                        raise RuntimeError('Image URL is rate limited (HTTP 429)')
                    time.sleep(cooldown)
                    response.raise_for_status()
                with PACE_LOCK:
                    NEXT_REQUEST[host] = max(NEXT_REQUEST.get(host, 0), time.monotonic() + cooldown)
                print(f'Rate limit: pausing {host} for {cooldown}s', flush=True)
                if attempt >= 2:
                    RATE_LIMITED.add(host)
                    raise RuntimeError('Source rate limited; cached metadata retained')
            response.raise_for_status()
            if binary and (len(response.content) > 10_000_000 or 'image' not in response.headers.get('content-type', '')):
                raise ValueError('Response is not a small image')
            path.parent.mkdir(parents=True, exist_ok=True)
            if binary:
                path.write_bytes(response.content)
            else:
                path.write_text(response.text)
            time.sleep(0.15)
            return response.content if binary else response.text
        except (requests.RequestException, ValueError) as error:
            if isinstance(error, requests.HTTPError) and error.response.status_code in [403, 404, 410]:
                raise error
            if attempt == 3:
                raise error
            time.sleep(2 ** attempt)


def soup(url):
    return BeautifulSoup(fetch(url), 'html.parser')


def prg_metadata_soup(url):
    content = fetch(url)
    # The PHP template has large repeated menus and sidebars. Parse the three
    # metadata fragments; retain a full-parser fallback if its markup changes.
    crumb = re.search(r'<ol\b[^>]*class=["\'][^"\']*\bbreadcrumb\b[^"\']*["\'][^>]*>.*?</ol>', content, re.S | re.I)
    description = re.search(r'<h6\b[^>]*>\s*Description\s*:\s*</h6>(.*?)<h6\b[^>]*>\s*Tags\s*:\s*</h6>', content, re.S | re.I)
    tags = re.search(r'<p\b[^>]*class=["\'][^"\']*\btags\b[^"\']*["\'][^>]*>.*?</p>', content, re.S | re.I)
    if crumb and description and tags:
        fragment = crumb[0] + '<div class="single-video-info-content"><h6>Description :</h6>' + description[1] + '<h6>Tags :</h6>' + tags[0] + '</div>'
        return BeautifulSoup(fragment, 'html.parser')
    return BeautifulSoup(content, 'html.parser', parse_only=SoupStrainer(class_=lambda value: bool(value) and any(c in value.split() for c in ['breadcrumb', 'single-video-info-content'])))


def check_robots():
    for site in SITES.values():
        base = urljoin(site['url'], '/')
        url = base + 'robots.txt'
        content = fetch(url)
        rp = RobotFileParser()
        rp.parse(content.splitlines())
        ROBOTS[urlparse(base).netloc] = rp
        (CACHE / (urlparse(base).netloc + '-robots.txt')).write_text(content)


def parallel(items, worker, label, workers=3):
    result = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for index, value in enumerate(pool.map(worker, items), 1):
            result.append(value)
            if index % 100 == 0 or index == len(items):
                print(f'{label}: {index}/{len(items)}', flush=True)
    return result


def prg_cards(s):
    rows = []
    # The homepage sidebar repeats games; only the main all-games grid is inventory.
    for card in s.select('.video-card.without-ads-blocks-list'):
        a = card.select_one('.video-title a')
        if not a or not re.search(r'/\d+-', a.get('href', '')):
            continue
        image = card.select_one('.video-card-image img')
        platform = card.select_one('.video-page')
        label = platform.get_text(' ', strip=True) if platform else ''
        rows.append({'id': 'prg-' + re.search(r'/(\d+)-', a['href'])[1], 'title': re.sub(r'^Play\s+', '', a.get_text(' ', strip=True)),
                     'source': a['href'], 'platform': LIST_PLATFORMS.get(label, ''), 'sourcePlatform': label,
                     'imageSource': urljoin(a['href'], image.get('data-src') or image.get('src', '')) if image else None})
    return rows


def collect_lists():
    # Inventory, detail and images are separate, resumable phases.
    s = soup(SITES['playretrogames']['url'])
    total = int(re.search(r'Retro Games:\s*(\d+)', s.get_text(' ', strip=True))[1])
    last = next(a['href'] for a in s.select('a[href]') if a.get_text(strip=True) == 'Last')
    pages = int(last.rstrip('/').rsplit('/', 1)[1])
    rows = prg_cards(s)
    for batch in parallel(list(range(2, pages + 1)), lambda p: prg_cards(soup(f'https://www.playretrogames.com/{p}')), 'PRG lists'):
        rows.extend(batch)
    unique = {r['id']: r for r in rows}
    if len(unique) != total:
        raise RuntimeError(f'PRG inventory incomplete: {len(unique)} unique, source advertises {total}')
    save_json(CACHE / 'playretrogames-list.json', {'pages': pages, 'advertisedGames': total, 'listedLinks': len(rows), 'games': list(unique.values())})

    rows, page, seen = [], 1, set()
    while True:
        url = 'https://www.playretro.io/' + (f'?page={page}' if page > 1 else '')
        s = soup(url)
        current = []
        for a in s.select('.games > a.game_thumb'):
            image = a.select_one('img')
            title = a.select_one('.game_name')
            source = urljoin(url, a['href'])
            current.append({'id': 'io-' + source.rsplit('/', 1)[1], 'title': title.get_text(' ', strip=True), 'source': source,
                            'platform': 'browser', 'sourcePlatform': '웹 브라우저', 'imageSource': urljoin(url, image['src']) if image else None})
        if not current or all(r['source'] in seen for r in current):
            raise RuntimeError(f'IO empty or repeated inventory page {page}')
        rows.extend(current)
        seen.update(r['source'] for r in current)
        next_link = next((a for a in s.select('a[href]') if a.get_text(strip=True) == '〉'), None)
        if not next_link:
            break
        next_page = int(re.search(r'[?&]page=(\d+)', next_link['href'])[1])
        if next_page != page + 1:
            raise RuntimeError('Unexpected IO pagination')
        page = next_page
    save_json(CACHE / 'playretro-io-list.json', {'pages': page, 'listedLinks': len(rows), 'games': list({r['source']: r for r in rows}.values())})
    print(f'IO lists: {page} pages, {len(seen)} games', flush=True)

    s = soup(SITES['retrogames-onl-snes']['url'])
    rows, repeated = {}, []
    for a in s.select('#azlist a[href]'):
        title = a.get_text(' ', strip=True)
        source = urljoin(SITES['retrogames-onl-snes']['url'], a['href'])
        if not title or not source.startswith('https://') or not source.endswith('.html'):
            continue
        if source in rows:
            rows[source]['aliases'].append(title)
            repeated.append({'title': title, 'source': source})
            continue
        rows[source] = {'id': 'snes-' + source.rsplit('/', 1)[1].removesuffix('.html'), 'title': title,
                        'source': source, 'platform': 'super-nintendo', 'sourcePlatform': 'Super Nintendo (SNES)', 'aliases': [], 'imageSource': None}
    save_json(CACHE / 'retrogames-onl-snes-list.json', {'pages': 1, 'listedLinks': len(s.select('#azlist a[href]')), 'duplicateAliases': repeated, 'games': list(rows.values())})
    print(f'ONL lists: {len(rows)} unique games, {len(repeated)} duplicate aliases', flush=True)


def detail(site, row):
    row = dict(row)
    row['listedTitle'] = row['title']
    if site == 'playretrogames':
        row['platform'] = LIST_PLATFORMS.get(row['sourcePlatform'], row['platform'])
    try:
        s = prg_metadata_soup(row['source']) if site == 'playretrogames' else soup(row['source'])
        if site == 'playretrogames':
            crumb = s.select_one('.breadcrumb-item:nth-child(2) a')
            if crumb:
                row['sourcePlatform'] = crumb.get_text(' ', strip=True)
                linked_platform = urlparse(crumb['href']).path.strip('/').split('/')[0]
                # Red Robin's MAME breadcrumb incorrectly links to /all/all.
                row['platform'] = linked_platform if linked_platform in PLATFORMS else LIST_PLATFORMS.get(row['sourcePlatform'], row['platform'])
            row['sourceGenres'] = [a.get_text(strip=True).lower() for a in s.select('.tags a')]
            body = s.select_one('.single-video-info-content')
            if not crumb or not body:
                raise ValueError('Missing game detail metadata')
            heading = body.find('h6', string=re.compile('Description')) if body else None
            texts = []
            if heading:
                for sibling in heading.next_siblings:
                    if getattr(sibling, 'name', '') == 'h6':
                        break
                    texts.append(sibling.get_text(' ', strip=True) if hasattr(sibling, 'get_text') else str(sibling).strip())
            row['sourceDescription'] = ' '.join(texts).strip()
        elif site == 'playretro-io':
            meta = s.select_one('.meta')
            if not meta:
                h = next((h for h in s.find_all('h4') if h.get_text(strip=True) == row['title']), None)
                body = h.parent if h else None
            else:
                body = meta.parent
            if not body:
                raise ValueError('Missing game detail heading')
            row['sourceGenres'] = [a.get_text(strip=True).lower() for a in body.select('.meta a')]
            p = body.select_one('.summary') or body.find('p')
            row['sourceDescription'] = p.get_text(' ', strip=True) if p else ''
        else:
            body = s.select_one('.post-body')
            if not body:
                # One SNES index link points to GAM.ONL's public landing page.
                if urlparse(row['source']).netloc == 'gam.onl' and s.find('h1'):
                    image = s.select_one('img[src][alt]')
                    row['imageSource'] = urljoin(row['source'], image['src']) if image else None
                    row['sourceGenres'] = []
                    row['sourceDescription'] = ''
                    row['detailStatus'] = 'ok'
                    return row
                raise ValueError('Missing game post body')
            label = body.find(['b', 'strong'], string=re.compile(r'^Genre:'))
            genre_text = label.parent.get_text(' ', strip=True).removeprefix('Genre:').strip() if label else ''
            row['sourceGenres'] = [v.strip().lower() for v in re.split(r'[,/]', genre_text) if v.strip()]
            gameplay = body.find(['b', 'strong'], string=re.compile(r'^Gameplay:'))
            row['sourceGameplay'] = gameplay.parent.get_text(' ', strip=True).removeprefix('Gameplay:').strip() if gameplay else ''
            text = body.select_one('#descrgame')
            if text:
                row['sourceMetadata'] = text.get_text(' ', strip=True)
                text.decompose()
            for element in body.select('script, style, iframe, button'):
                element.decompose()
            row['sourceDescription'] = body.get_text(' ', strip=True)
            image = body.select_one('img[src]')
            if image:
                row['imageSource'] = urljoin(row['source'], image['src'])
            heading = s.select_one('.post-title')
            if heading:
                actual = re.sub(r'\s*\(SNES\)\s*$', '', heading.get_text(' ', strip=True)).strip()
                row['detailTitle'] = actual
                if actual and actual.casefold() != row['title'].casefold():
                    row['aliases'].append(row['title'])
                    row['title'] = actual
        row['detailStatus'] = 'ok'
    except Exception as error:
        row['detailStatus'] = str(error)
        row.setdefault('sourceGenres', [])
        row.setdefault('sourceDescription', '')
    return row


def collect_details():
    for site in ['playretro-io', 'retrogames-onl-snes', 'playretrogames']:
        rows = read_json(CACHE / f'{site}-list.json')['games']
        rows = parallel(rows, lambda row: detail(site, row), site + ' details', workers=6 if site == 'playretrogames' else 3)
        save_json(CACHE / f'{site}-details.json', rows)


def image_for(site, row):
    target = ROOT / 'public/images/retro-catalogs' / site / (row['id'] + '.webp')
    if not row.get('imageSource'):
        return row['id'], {'image': None, 'imageStatus': '원문에 썸네일 없음'}
    try:
        if not target.exists():
            with Image.open(io.BytesIO(fetch(row['imageSource'], binary=True))) as original:
                image = ImageOps.exif_transpose(original).convert('RGB')
                image.thumbnail((480, 360), Image.Resampling.LANCZOS)
                target.parent.mkdir(parents=True, exist_ok=True)
                image.save(target, 'WEBP', quality=78)
        with Image.open(target) as image:
            width, height = image.size
        return row['id'], {'image': {'src': '/' + str(target.relative_to(ROOT / 'public')), 'width': width, 'height': height, 'source': row['imageSource'], 'kind': 'source-thumbnail'}}
    except Exception as error:
        return row['id'], {'image': None, 'imageStatus': '원문 이미지 접근 불가', 'imageError': str(error)}


def collect_images():
    for site in ['playretro-io', 'retrogames-onl-snes', 'playretrogames']:
        rows = read_json(CACHE / f'{site}-details.json')
        images = parallel(rows, lambda row: image_for(site, row), site + ' images')
        save_json(CACHE / f'{site}-images.json', dict(images))


def classify(row):
    title = row['title'].lower()
    tags = ', '.join(row.get('sourceGenres', []))
    # A specific source genre takes priority over the series name (e.g. Pokémon puzzles).
    for pattern, genre in TAG_GENRES[:-2]:
        if re.search(pattern, tags):
            return genre, '원문 장르 통합'
    gameplay = re.sub(r'\b(?:rpg|puzzle) elements\b', '', row.get('sourceGameplay', '').lower())
    for pattern, genre in TAG_GENRES[:-2]:
        if re.search(pattern, gameplay):
            return genre, '원문 진행 분류 통합'
    for pattern, genre in SERIES:
        if re.search(pattern, title):
            return genre, '편집 분류'
    for pattern, genre in TAG_GENRES:
        if re.search(pattern, tags + ', ' + gameplay):
            return genre, '원문 장르 통합'
    return '기타/미분류', '장르 확인 필요'


def excerpt(text):
    # A few original descriptions already contain double-encoded UTF-8.
    if re.search(r'[ÃÂÅâ]', text):
        for encoding in ['latin-1', 'cp1252']:
            try:
                text = text.encode(encoding).decode('utf-8')
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    # At most 20 source words per game; do not reproduce complete descriptions.
    words = text.split()
    return ' '.join(words[:20]) + (' …' if len(words) > 20 else '')


def build(sites=None):
    translations = read_json(ROOT / 'scripts/retro-descriptions-ko.json')
    for site in sites or SITES:
        config = SITES[site]
        rows = read_json(CACHE / f'{site}-details.json')
        images = read_json(CACHE / f'{site}-images.json')
        games = []
        for row in rows:
            genre, basis = classify(row)
            if row['platform'] not in PLATFORMS:
                raise ValueError('Unknown platform: ' + repr(row['platform']) + ' ' + row['source'])
            game = {k: row[k] for k in ['id', 'title', 'source', 'platform', 'sourcePlatform', 'sourceGenres', 'detailStatus']}
            game['listedTitle'] = row['listedTitle']
            if row.get('sourceGameplay'):
                game['sourceGameplay'] = row['sourceGameplay']
            if row.get('aliases'):
                game['aliases'] = list(dict.fromkeys(row['aliases']))
            desc = excerpt(row['sourceDescription'])
            if desc:
                translated = translations['games'].get(site + ':' + row['id'])
                source_hash = hashlib.sha256(row['sourceDescription'].encode('utf-8')).hexdigest()
                if not translated or translated['sourceHash'] != source_hash:
                    raise ValueError('Korean description needs translation: ' + site + ':' + row['id'])
                description = translated['description']
                if not re.search(r'[가-힣]', description):
                    raise ValueError('Korean description missing: ' + site + ':' + row['id'])
            else:
                description = '원문 목록에 소개된 게임입니다. 자세한 소개는 원문에서 확인해 주세요.'
            game.update({'genre': genre, 'genreBasis': basis, 'description': description,
                         'descriptionLanguage': 'ko', 'descriptionBasis': '원문 소개 한글 번역' if desc else '목록 안내', 'basicMethod': BASICS[genre]})
            game.update(images[row['id']])
            if not game['image']:
                game['imageSource'] = row.get('imageSource')
            if row.get('sourceMetadata'):
                game['sourceMetadata'] = row['sourceMetadata']
            games.append(game)
        used = {p: PLATFORMS[p] for p in PLATFORMS if any(g['platform'] == p for g in games)}
        games.sort(key=lambda g: (list(used).index(g['platform']), g['title'].casefold()))
        payload = {'collectedAt': DATE, 'source': config['url'], 'scope': config['scope'], 'platforms': used, 'games': games}
        save_json(ROOT / f'public/data/{site}-games.json', payload)
        inventory = read_json(CACHE / f'{site}-list.json')
        report = {'collectedAt': DATE, 'source': config['url'], 'scope': config['scope'],
                  'inventory': {k: v for k, v in inventory.items() if k != 'games'}, 'games': len(games),
                  'platformCounts': dict(Counter(g['platform'] for g in games)), 'genreCounts': dict(Counter(g['genre'] for g in games)),
                  'images': sum(bool(g['image']) for g in games),
                  'detailFailures': [{'source': g['source'], 'reason': g['detailStatus']} for g in games if g['detailStatus'] != 'ok'],
                  'missingImages': [{'id': g['id'], 'source': g['source'], 'reason': g.get('imageError', g.get('imageStatus'))} for g in games if not g['image']],
                  'renamedFromDetail': [{'listedTitle': r['listedTitle'], 'detailTitle': r['detailTitle'], 'source': r['source']} for r in rows if r.get('detailTitle') and r['listedTitle'] != r['detailTitle']],
                  'robots': (CACHE / (urlparse(config['url']).netloc + '-robots.txt')).read_text()}
        save_json(ROOT / f'docs/{site}-crawl-report.json', report)
        render(site, config, payload, report)
        print(f'{site}: {len(games)} games, {report["images"]} images, {len(report["detailFailures"])} detail failures', flush=True)


def render(site, config, payload, report):
    esc = lambda value: html.escape(str(value), quote=True)
    games, platforms = payload['games'], payload['platforms']
    counts, genres = Counter(g['platform'] for g in games), Counter(g['genre'] for g in games)
    buttons = ''.join(f'<button type="button" data-platform="{p}" data-label="{esc(label)}" aria-pressed="false">{esc(label)} <span>{counts[p]}</span></button>' for p, label in platforms.items())
    options = ''.join(f'<option value="{esc(g)}">{esc(g)} ({genres[g]})</option>' for g in GENRES if genres[g])
    cards = []
    for g in games:
        img = g['image']
        media = f'<a class="game-screenshot" href="{esc(img["src"])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(g["title"])} 이미지 크게 보기"><img src="{esc(img["src"])}" width="{img["width"]}" height="{img["height"]}" loading="lazy" decoding="async" alt="{esc(g["title"])} 원문 썸네일"></a>' if img else f'<span class="game-image-missing">{esc(g["imageStatus"])}<br>원문 링크에서 확인해 주세요.</span>'
        labels = list(dict.fromkeys([g['listedTitle'], *g.get('aliases', [])]))
        other_labels = [label for label in labels if label != g['title']]
        aliases = f'<p class="game-method">원문 목록 표기: {esc(" · ".join(other_labels))}</p>' if other_labels else ''
        cards.append(f'''<section id="{esc(g['id'])}" class="classic-game" data-platform="{g['platform']}" data-genre="{esc(g['genre'])}" aria-labelledby="{esc(g['id'])}-title">
{media}<p class="game-tags">{esc(platforms[g['platform']])} · {esc(g['genre'])}</p>
<h2 id="{esc(g['id'])}-title">{esc(g['title'])}</h2>{aliases}<p>{esc(g['description'])}</p>
<p class="game-method"><strong>기본 진행</strong> {esc(g['basicMethod'])}</p>
<p class="game-source"><a href="{esc(g['source'])}">{esc(config['name'])} 원문</a> · {esc(g['genreBasis'])} · {esc(g['descriptionBasis'])}</p>
</section>''')
    # Shared page chrome and filter layout are kept in a small checked-in template.
    template = (ROOT / 'scripts/retro-catalog-template.html').read_text()
    substitutions = {
        'TITLE': esc(config['name']), 'SLUG': site, 'DATE': DATE, 'DISPLAY_DATE': DATE.replace('-', '.'),
        'SOURCE': esc(config['url']), 'SOURCE_NAME': esc(config['name']), 'SCOPE': esc(config['scope']),
        'TOTAL': str(len(games)), 'PLATFORM_COUNT': str(len(platforms)), 'IMAGE_COUNT': str(report['images']),
        'BUTTONS': buttons, 'OPTIONS': options, 'CARDS': '\n'.join(cards),
    }
    for key, value in substitutions.items():
        template = template.replace('{{' + key + '}}', value)
    target = ROOT / f'posts/{site}/index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(template)


if __name__ == '__main__':
    CACHE.mkdir(parents=True, exist_ok=True)
    command = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if command != 'build':
        check_robots()
    for name, action in [('lists', collect_lists), ('details', collect_details), ('images', collect_images), ('build', build)]:
        if command in ['all', name]:
            action()
