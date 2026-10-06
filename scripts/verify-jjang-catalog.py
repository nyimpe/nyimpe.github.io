#!/usr/bin/env python3
"""Audit conserved source records, source genre totals and decoded saved screenshots."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/tmp/nyimpe-jjang-cache')


def read(path):
    return json.loads(path.read_text())


def verify():
    source = read(CACHE / 'raw.json')
    listed = read(CACHE / 'listed.json')
    inventory = read(CACHE / 'inventory.json')
    data = read(ROOT / 'public/data/jjang-games.json')
    report = read(ROOT / 'docs/jjang-crawl-report.json')
    gameplay_path = ROOT / 'docs/jjang-gameplay-images.json'
    gameplay = read(gameplay_path) if gameplay_path.exists() else None
    games = data['games']
    if gameplay:
        assert set(gameplay['entries']).isdisjoint(gameplay['unresolved'])
        assert set(gameplay['entries']) | set(gameplay['unresolved']) == {game['id'] for game in games}
    by_id = {row['id']: row for row in source}
    assert len(by_id) == len(source) == len(games) == len(listed)
    assert set(by_id) == {row['id'] for row in listed} == {game['id'] for game in games}
    assert set(data['platforms']) == {'2d', 'old'}
    for platform in data['platforms']:
        audit = inventory['platforms'][platform]
        rows = [game for game in games if game['platform'] == platform]
        assert len(rows) == audit['count'] == audit['uniqueListed'] == sum(page['items'] for page in audit['pages'])
        counts = Counter(game['sourceCategory'] for game in rows)
        assert counts == audit['detailGenreCounts']
        assert all(counts[genre] == count for genre, count in audit['sourceGenreCounts'].items())
        assert counts.get('', 0) + sum(audit['sourceGenreCounts'].values()) == len(rows)
    images = 0
    for game in games:
        row = by_id[game['id']]
        assert game['title'] == row['title'] and game['title'].strip() and '\ufffd' not in game['title']
        assert game['sourceCategory'] == row['sourceCategory']
        assert game['sourceAlias'] == row['sourceAlias']
        assert game['genre'] == (row['sourceCategory'] or '미분류')
        parsed = urlparse(game['source'])
        assert parsed.hostname == 'www.jjanggame.co.kr' and parsed.path == '/view.php'
        assert parse_qs(parsed.query) == {'u': [row['uid']], 'gtype': [game['platform']]}
        if game['image']:
            image = game['image']
            if gameplay:
                entry = gameplay['entries'][game['id']]
                assert image == entry['image']
                assert image['kind'] == 'external-gameplay'
                assert image['source'] == entry['source']
                assert urlparse(image['source']).hostname != 'img.jjanggame.co.kr'
                assert entry['matchedTitle'] and entry['selectionBasis'] and entry['sha256']
                assert image['matchType'] in {'exact', 'representative'}
                assert entry['sourcePage']
                assert parse_qs(urlparse(image['src']).query) == {'v': [entry['savedSha256'][:12]]}
                assert hashlib.sha256((ROOT / 'public' / urlparse(image['src']).path.lstrip('/')).read_bytes()).hexdigest() == entry['savedSha256']
            else:
                assert image['source'] in row['screenshots'] + row['screenThumbnails'] + [row['preview'], row['thumbnail']]
            assert Path(urlparse(image['source']).path).name not in {'snap_big.gif', 'snap_small.gif'}
            assert urlparse(image['src']).path == '/images/jjang-games/' + game['id'] + '.webp'
            with Image.open(ROOT / 'public' / urlparse(image['src']).path.lstrip('/')) as saved:
                saved.load()
                assert saved.format == 'WEBP' and saved.size == (image['width'], image['height'])
            images += 1
        else:
            assert game['imageStatus']
            if gameplay:
                assert game['imageStatus'] == gameplay['unresolved'][game['id']]['reason']
    page = BeautifulSoup((ROOT / 'posts/jjang-games/index.html').read_text(), 'html.parser')
    cards = page.select('.classic-game')
    assert [card['id'] for card in cards] == [game['id'] for game in games]
    assert len(page.select('.classic-game img')) == images == report['screenshots']
    if gameplay:
        for card, game in zip(cards, games):
            if game['image']:
                assert any(link.get('href') == game['image']['sourcePage'] and link.get_text() == '플레이 화면 출처' for link in card.select('a'))
    assert {path.stem for path in (ROOT / 'public/images/jjang-games').glob('*.webp')} == {game['id'] for game in games if game['image']}
    assert len(games) == report['games']
    assert dict(Counter(game['genre'] for game in games)) == report['genreCounts']
    print(json.dumps({'games': len(games), 'imagesDecoded': images, 'sourceIdsPreserved': True,
                      'sourceGenreCountsMatch': True, 'onlyRequestedCategories': True}, indent=2))


if __name__ == '__main__':
    verify()
