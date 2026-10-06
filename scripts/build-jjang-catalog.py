#!/usr/bin/env python3
"""Build Jjang's saved catalog and a post using the existing lazy gallery."""
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/tmp/nyimpe-jjang-cache')
PLATFORMS = {'2d': '2D 게임', 'old': '오락실 게임'}
GENRES = ['액션', '격투', '슈팅', '레이싱', '스포츠', '퍼즐', '어드벤쳐', '롤플레잉', '퀴즈', '미로', '아케이드', '미분류']
BASICS = {
    '액션': '캐릭터를 움직여 적과 장애물에 대응하고 스테이지의 목표를 달성합니다.',
    '격투': '상대의 움직임을 살피고 공격·방어·기술을 조합해 대결합니다.',
    '슈팅': '적의 공격을 피하면서 조준하거나 발사해 적과 보스를 공격합니다.',
    '레이싱': '속도와 방향을 조절하며 코스를 주행하고 기록이나 순위를 겨룹니다.',
    '스포츠': '종목의 규칙에 따라 선수나 팀을 조작해 점수와 승리를 겨룹니다.',
    '퍼즐': '화면의 규칙을 파악하고 블록·그림·말을 선택하거나 배치해 문제를 해결합니다.',
    '어드벤쳐': '여러 장소와 스테이지를 탐험하며 장애물·적·단서에 대응해 모험을 진행합니다.',
    '롤플레잉': '탐험과 대화, 전투를 통해 캐릭터를 성장시키며 이야기를 진행합니다.',
    '퀴즈': '제시되는 문제와 선택지를 읽고 답을 골라 점수나 다음 단계에 도전합니다.',
    '미로': '주변 경로와 장애물을 살피며 목표를 모으거나 출구에 도달합니다.',
    '아케이드': '이동과 타이밍을 활용해 화면의 목표를 달성하고 다음 스테이지에 도전합니다.',
    '미분류': '게임 화면의 목표·규칙과 원문 안내에 따라 진행합니다. 개별 게임의 조작법은 원문에서 확인해 주세요.',
}
# Rules are restricted by source genre so a spin-off never inherits the wrong gameplay.
SERIES = [
    ('격투', r'철권|블러디 로어|킹 오브 파이터|스트리트 파이터|아랑전설|용호의 권|사무라이 쇼다운|월화의 검사', '캐릭터마다 다른 공격과 기술을 활용해 상대를 제압하는 대전 격투 게임입니다.'),
    ('슈팅', r'스트라이커즈|라이덴|건버드|도돈파치|배틀 가레가|드래곤 블레이즈', '기체를 움직여 적의 탄막을 피하고 적기와 보스를 공격하는 스크롤 슈팅 게임입니다.'),
    ('아케이드', r'메탈슬러그|메탈 슬러그', '병사와 탈것을 조작하며 적의 부대를 돌파하는 횡스크롤 액션 슈팅 게임입니다.'),
    ('아케이드', r'버블보블|버블버블|보글보글', '거품에 적을 가두고 터뜨리며 화면 안의 적을 모두 없애는 액션 게임입니다.'),
    ('아케이드', r'스노우 브라더', '적을 눈덩이로 만든 뒤 굴려 화면을 정리하는 스테이지형 액션 게임입니다.'),
    ('퍼즐', r'퍼즐 버블|퍼즐버블', '색깔 공을 발사해 같은 색끼리 연결하고 없애는 퍼즐 게임입니다.'),
    ('퍼즐', r'테트리스|헥사', '떨어지는 블록을 적절히 배치해 줄이나 같은 색의 조합을 없애는 퍼즐 게임입니다.'),
    ('어드벤쳐', r'슈퍼 마리오|슈퍼마리오|마리오 월드', '이동과 점프를 활용해 장애물을 넘고 스테이지를 진행하는 마리오 시리즈입니다.'),
    ('어드벤쳐', r'소닉', '빠르게 달리고 점프하며 링을 모으고 코스를 돌파하는 소닉 시리즈입니다.'),
    ('롤플레잉', r'크로노 트리거', '시간을 넘나드는 모험과 동료들의 연계 전투가 중심인 RPG입니다.'),
    ('미로', r'팩맨|팍맨', '미로의 점을 모으면서 유령을 피하고 파워 아이템으로 반격하는 게임입니다.'),
]


def build():
    raw = json.loads((CACHE / 'raw.json').read_text())
    gameplay_path = ROOT / 'docs/jjang-gameplay-images.json'
    gameplay = json.loads(gameplay_path.read_text()) if gameplay_path.exists() else None
    if gameplay:
        images = {}
        for row in raw:
            replacement = gameplay['entries'].get(row['id'])
            images[row['id']] = {'image': replacement['image'] if replacement else None,
                                 'reason': '' if replacement else gameplay['unresolved'][row['id']]['reason'],
                                 'failures': []}
    else:
        images = json.loads((CACHE / 'images.json').read_text())
    inventory = json.loads((CACHE / 'inventory.json').read_text())
    collected = inventory['collectedAt'][:10]
    games = []
    for row in raw:
        genre = row['sourceCategory'] or '미분류'
        assert genre in BASICS, ('Unmapped source genre', genre, row['source'])
        description = f'짱게임의 {PLATFORMS[row["platform"]]} 카테고리에 소개된 {genre} 게임입니다.'
        basis = '원문 카테고리·장르 안내'
        for expected, pattern, summary in SERIES:
            if genre == expected and re.search(pattern, row['title'], re.I):
                description, basis = summary, '편집 요약'
                break
        game = {key: row[key] for key in ['id', 'platform', 'title', 'source', 'sourceCategory']}
        game['sourceAlias'] = row.get('sourceAlias', '')
        game.update(genre=genre, genreBasis='원문 장르' if row['sourceCategory'] else '원문 장르 미지정', description=description, descriptionBasis=basis,
                    basicMethod=BASICS[genre], image=images[row['id']]['image'])
        if not game['image']:
            game['imageStatus'] = images[row['id']]['reason']
        games.append(game)
    games.sort(key=lambda game: (list(PLATFORMS).index(game['platform']), game['title'], game['id']))
    counts = Counter(game['platform'] for game in games)
    genres = Counter(game['genre'] for game in games)
    assert len({game['id'] for game in games}) == len(games)
    for platform in PLATFORMS:
        assert counts[platform] == inventory['platforms'][platform]['count']
    report = {'source': 'https://www.jjanggame.co.kr/', 'collectedAt': inventory['collectedAt'], 'inventory': inventory,
        'games': len(games), 'platformCounts': dict(counts), 'genreCounts': dict(genres),
        'screenshots': sum(bool(game['image']) for game in games),
        'imageKinds': dict(Counter(game['image']['kind'] for game in games if game['image'])),
        'missingScreenshots': [{'id': game['id'], 'title': game['title'], 'source': game['source'], 'reason': game['imageStatus']} for game in games if not game['image']],
        'imageFailures': [{'id': uid, 'attempts': result['failures']} for uid, result in images.items() if result['failures']],
        'classification': '플랫폼은 짱게임의 2D 게임·고전 오락실게임 카테고리 기준입니다. 장르는 각 상세 페이지의 원문 분류이며, 비어 있는 항목은 미분류로 보존합니다.',
        'descriptionBasis': '시리즈별 편집 요약 또는 원문 카테고리·장르 안내. 기본 진행은 장르별 안내이며 개별 게임의 조작키 설명이 아닙니다.'}
    payload = {'collectedAt': collected, 'platforms': PLATFORMS, 'games': games}
    if gameplay:
        report['gameplayImages'] = {'collectedAt': gameplay['collectedAt'], **gameplay['summary']}
    (ROOT / 'public/data').mkdir(parents=True, exist_ok=True)
    (ROOT / 'public/data/jjang-games.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'docs/jjang-crawl-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    esc = lambda value: html.escape(str(value), quote=True)
    buttons = ''.join(f'<button type="button" data-platform="{key}" data-label="{label}" aria-pressed="false">{label} <span>{counts[key]}</span></button>' for key, label in PLATFORMS.items())
    options = ''.join(f'<option value="{esc(genre)}">{esc(genre)} ({genres[genre]})</option>' for genre in GENRES if genres[genre])
    cards = []
    for game in games:
        image = game['image']
        screen = f'<a class="game-screenshot" href="{esc(image["src"])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(game["title"])} 화면 크게 보기"><img src="{esc(image["src"])}" width="{image["width"]}" height="{image["height"]}" loading="lazy" decoding="async" alt="{esc(game["title"])} 게임 화면"></a>' if image else f'<span class="game-image-missing">{esc(game["imageStatus"])}<br>자세한 내용은 원문 링크에서 확인해 주세요.</span>'
        cards.append(f'''<section id="{game['id']}" class="classic-game" data-platform="{game['platform']}" data-genre="{esc(game['genre'])}" aria-labelledby="{game['id']}-title">
{screen}
<p class="game-tags">{PLATFORMS[game['platform']]} · {esc(game['genre'])}</p>
<h2 id="{game['id']}-title">{esc(game['title'])}</h2>
{'<p class="game-tags" lang="en">' + esc(game['sourceAlias']) + '</p>' if game['sourceAlias'] and game['sourceAlias'] != game['title'] else ''}
<p>{esc(game['description'])}</p>
<p class="game-method"><strong>기본 진행</strong> {esc(game['basicMethod'])}</p>
<p class="game-source"><a href="{esc(game['source'])}">짱게임 원문</a> · {esc(game['genreBasis'])}</p>
{'<p class="game-source"><a href="' + esc(image['sourcePage']) + '">플레이 화면 출처</a> · ' + esc(image.get('displayNote') or ('영문명 일치' if image['matchType'] == 'exact' else '동일 게임의 대표 화면 · 지역·개정판 차이 가능')) + '</p>' if image and image.get('sourcePage') else ''}
</section>''')
    page = f'''<!doctype html>
<html lang="ko"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="짱게임의 2D·오락실 게임 {len(games)}개를 게임 화면과 설명으로 살펴보세요. 카테고리·장르 필터와 검색, 스크롤 지연 표시.">
<title>짱게임 2D·오락실 게임 도감 · nyimpe</title>
<link rel="canonical" href="https://nyimpe.github.io/posts/jjang-games/">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="stylesheet" href="/src/style.css">
<link rel="stylesheet" href="/src/classic-games.css">
<script type="module" src="/src/main.js"></script>
<script type="module" src="/src/classic-games.js"></script>
</head><body>
<a class="skip-link" href="#content">본문으로 이동</a>
<header class="site-header">
<div class="header-content"><nav lang="en" class="site-nav" aria-label="Main navigation">
<a href="/">Home</a><a href="/about/">About</a><a href="https://github.com/nyimpe">GitHub</a>
<button id="theme-toggle" class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false" hidden>☾</button>
</nav><hr></div><img class="site-cat" src="/cat.png" width="88" height="160" alt="주황색과 흰색의 픽셀아트 고양이">
</header>
<main id="content"><article class="classic-post">
<header class="post-header"><h1>짱게임 2D·오락실 게임 도감</h1><time datetime="{collected}">{collected.replace('-', '.')}</time>
<p>2D와 오락실의 추억을 게임 화면으로 찾아보세요.</p></header>
<p class="classic-intro">출처: <a href="https://www.jjanggame.co.kr/list.php?gtype=2d">짱게임 2D 게임</a> · <a href="https://www.jjanggame.co.kr/list.php?gtype=old">고전 오락실게임</a> · {len(games):,}개 게임 · {report['screenshots']:,}개 화면. 플랫폼은 짱게임의 카테고리 기준이며 같은 게임의 지역판·버전도 원문 항목별로 보존했습니다.</p>
<p class="classic-intro">장르는 상세 페이지의 원문 분류이며, 원문 장르가 비어 있는 {genres['미분류']}개는 ‘미분류’로 표시했습니다. 설명은 시리즈 요약 또는 카테고리·장르 안내이며, ‘기본 진행’은 장르별 안내입니다. 화면은 외부 게임 자료의 실제 플레이 스크린샷입니다. 표지·타이틀 화면·짱게임 캡처는 사용하지 않습니다. 각 카드에 화면 출처를 표시했으며, 대표 화면은 지역·개정판이 원문과 다를 수 있습니다. 기존 <a href="/posts/classic-games/">고전게임 도감</a>도 함께 살펴보세요.</p>
<p class="classic-intro">게임·개조판을 정확히 대응할 수 없거나 외부 플레이 화면을 확인하지 못한 {len(report['missingScreenshots']):,}개도 목록에 포함하고 사유를 표시했습니다.</p>
<form class="classic-filter" aria-label="게임 필터" hidden>
<fieldset class="game-platforms"><legend>플랫폼 / 카테고리</legend><div class="game-platform-buttons">
<button type="button" data-platform="" data-label="전체" aria-pressed="true">전체 <span>{len(games)}</span></button>{buttons}
</div></fieldset>
<div class="game-filter-fields"><label for="game-genre">장르<select id="game-genre"><option value="">전체 장르</option>{options}</select></label>
<label for="game-search">게임 검색<input id="game-search" type="search" placeholder="게임명 또는 설명" autocomplete="off"></label>
<button class="game-reset" type="reset">필터 초기화</button></div></form>
<p class="game-count" id="game-count" role="status" aria-atomic="true">전체 · {len(games)}개 게임</p>
<p class="game-empty" id="game-empty" hidden>일치하는 게임이 없습니다. 검색어를 바꾸거나 필터를 초기화해 주세요.</p>
<noscript><p>JavaScript를 켜면 플랫폼·장르 필터와 검색을 사용할 수 있습니다. 아래에서 전체 게임을 볼 수 있습니다.</p></noscript>
<div class="classic-games">{''.join(cards)}</div>
<p class="game-load-status" id="game-load-status" role="status" aria-atomic="true" hidden></p>
<div class="game-load-trigger" id="game-load-trigger" aria-hidden="true" hidden></div>
<p class="classic-intro"><a href="/data/jjang-games.json">수집한 게임 정보 JSON</a> · 개별 조작키와 자세한 정보는 원문 링크에서 확인할 수 있습니다.</p>
<p class="post-back"><a href="/">← Home</a></p>
</article></main>
<footer class="site-footer">Small things, made and remade. <a href="https://github.com/nyimpe/nyimpe.github.io">Source code</a></footer>
</body></html>
'''
    target = ROOT / 'posts/jjang-games/index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page)
    print(json.dumps({key: report[key] for key in ['games', 'platformCounts', 'genreCounts', 'screenshots', 'imageKinds', 'missingScreenshots']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
