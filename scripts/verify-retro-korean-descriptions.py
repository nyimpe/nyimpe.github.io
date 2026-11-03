#!/usr/bin/env python3
"""Verify all Korean descriptions and optionally preserve the pre-edit inventory.
Usage: python scripts/verify-retro-korean-descriptions.py [baseline.json]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITES = ['playretrogames', 'playretro-io', 'retrogames-onl-snes']
baseline = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else None
translations = json.loads((ROOT / 'scripts/retro-descriptions-ko.json').read_text())['games']
allowed_changes = {'description', 'descriptionLanguage', 'descriptionBasis'}

for site in SITES:
    data = json.loads((ROOT / f'public/data/{site}-games.json').read_text())
    page = BeautifulSoup((ROOT / f'posts/{site}/index.html').read_text(), 'html.parser')
    cards = page.select('.classic-game')
    assert [c['id'] for c in cards] == [g['id'] for g in data['games']]
    if baseline:
        old = baseline[site]
        assert {k: v for k, v in data.items() if k != 'games'} == {k: v for k, v in old.items() if k != 'games'}
        assert len(data['games']) == len(old['games'])
    for index, (game, card) in enumerate(zip(data['games'], cards)):
        description = game['description']
        assert game['descriptionLanguage'] == 'ko', game['id']
        assert len(re.findall(r'[가-힣]', description)) >= 5, game['id']
        assert not re.search(r'\b[A-Za-z]{2,}(?:\s+[A-Za-z]{2,}){9,}\b', description), game['id']
        assert all(not c.isalpha() or any(script in unicodedata.name(c, '') for script in ('HANGUL', 'LATIN')) for c in description), game['id']
        assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', description), game['id']
        assert card.select_one('h2 ~ p:not([class])').get_text() == description, game['id']
        if game['descriptionBasis'] == '원문 소개 한글 번역':
            translated = translations[site + ':' + game['id']]
            assert translated['description'] == description
            if game.get('descriptionSource'):
                assert game['descriptionSource'] == translated['descriptionSource']
                assert card.select_one('.game-source a:nth-of-type(2)')['href'] == game['descriptionSource']
        else:
            assert game['descriptionBasis'] == '목록 안내'
        if baseline:
            previous = old['games'][index]
            assert {k: v for k, v in game.items() if k not in allowed_changes} == {k: v for k, v in previous.items() if k not in allowed_changes}, game['id']
    assert '원문 소개 짧은 발췌' not in page.get_text()
    print(f'{site}: {len(cards)} Korean descriptions match HTML; inventory preserved', flush=True)
