#!/usr/bin/env python3
"""Build the saved metadata, collection report and static filterable page.
Run after crawl-tooli.py collect / images, then optional Flash capture.
"""
import html
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/tmp/nyimpe-tooli-cache')
PLATFORMS = {'pc': 'PC', 'lounge': '오락실', 'boy': '게임보이', 'sfc': '슈퍼패미콤', 'md': '메가드라이브', 'msx': 'MSX', 'flash': '플래시'}
GENRES = ['액션/아케이드', '대전/격투', '슈팅', '퍼즐/보드', '전략/시뮬레이션', 'RPG', '레이싱/스포츠', '어드벤처', '리듬', '창작/교육', '미니게임/모음', '기타/미분류']
SOURCE_GENRES = {'액션/아케이드': '액션/아케이드', '퍼즐/보드': '퍼즐/보드', '전략시뮬': '전략/시뮬레이션', '시뮬레이션': '전략/시뮬레이션', '롤플레잉': 'RPG', '레이싱/스포츠': '레이싱/스포츠', '어드벤쳐': '어드벤처'}
BASICS = {
    '액션/아케이드': '캐릭터를 움직여 장애물과 적을 피하거나 공격하며 스테이지의 목표를 달성합니다.',
    '대전/격투': '공격과 방어, 기술을 조합해 상대와 대결합니다.',
    '슈팅': '적의 공격을 피하면서 조준하거나 발사해 적을 처치합니다.',
    '퍼즐/보드': '화면의 규칙을 파악하고 블록·그림·말을 배치하거나 선택해 문제를 해결합니다.',
    '전략/시뮬레이션': '자원과 행동을 계획하고 상황에 맞게 선택해 목표를 달성합니다.',
    'RPG': '탐험과 대화, 전투를 통해 캐릭터를 성장시키며 이야기를 진행합니다.',
    '레이싱/스포츠': '주행이나 경기의 규칙에 따라 기록과 점수를 겨룹니다.',
    '어드벤처': '장소를 탐색하고 대화·단서·아이템을 활용해 사건과 퍼즐을 풀어갑니다.',
    '리듬': '박자나 화면의 신호에 맞춰 입력합니다.',
    '창작/교육': '그리기나 학습 등 화면에 제시된 활동을 진행합니다.',
    '미니게임/모음': '수록된 게임을 선택하고 각 게임의 규칙과 목표에 따라 진행합니다.',
    '기타/미분류': '게임별 진행 방식과 조작은 원문을 확인해 주세요.'
}
# Short editorial descriptions for recurring game series with sparse source text.
SERIES = [
 ('틀린그림|히든캐치', '두 그림을 비교하며 제한 시간 안에 서로 다른 부분을 찾는 관찰 퍼즐입니다.'),
 ('서치아이', '그림 속에 숨은 대상을 찾아내는 관찰 게임입니다.'),
 ('킹 오브 파이터|아랑전설|용호의 권|스트리트 파이터|철권|뱀파이어|사무라이 쇼다운|월화의 검사|호열사|소울 엣지', '캐릭터마다 다른 공격과 기술을 활용해 상대를 제압하는 대전 격투 게임입니다.'),
 ('메탈슬러그', '병사와 탈것을 조작하며 적의 부대를 돌파하는 횡스크롤 액션 슈팅 게임입니다.'),
 ('스트라이커즈|라이덴|건버드|도돈파치|배틀 가레가|울트라 X|프로기어|드래곤 블레이즈', '적의 탄막을 피하면서 적기와 보스를 공격하는 스크롤 슈팅 게임입니다.'),
 ('버블보블|버블버블|보글보글|보블버블', '거품에 적을 가두고 터뜨리며 화면 안의 적을 모두 없애는 액션 게임입니다.'),
 ('스노우 브라더|스노우브라더', '적을 눈덩이로 만든 뒤 굴려 화면을 정리하는 스테이지형 액션 게임입니다.'),
 ('퍼즐버블|퍼즐 버블|버블슈터', '색깔 공을 발사해 같은 색끼리 연결하고 없애는 퍼즐 게임입니다.'),
 ('소닉', '빠르게 달리고 점프하며 링을 모으고 코스를 돌파하는 액션 게임입니다.'),
 ('마리오 카트|마리오카트', '코스를 달리면서 아이템을 활용해 순위를 겨루는 카트 레이싱 게임입니다.'),
 ('슈퍼마리오|슈퍼 마리오', '이동과 점프를 활용해 장애물을 넘고 스테이지를 진행하는 마리오 시리즈입니다.'),
 ('킹스밸리', '피라미드 안에서 보석을 모으고 미라를 피하며 탈출 경로를 찾는 퍼즐 액션 게임입니다.'),
 ('남극탐험', '펭귄을 조작해 구멍과 장애물을 피하며 남극의 코스를 달리는 게임입니다.'),
 ('몽대륙', '펭귄이 여러 지역을 탐험하며 장애물을 넘고 아이템을 모으는 모험 액션 게임입니다.'),
 ('역전재판', '사건을 조사해 증거를 모으고 법정에서 증언의 모순을 밝혀내는 추리 어드벤처입니다.'),
 ('목장이야기|하베스트문', '농작물을 기르고 가축을 돌보며 마을 사람들과 교류하는 목장 생활 게임입니다.'),
 ('home sheep', '몸집이 다른 세 마리 양의 능력을 활용해 장애물을 넘고 출구까지 함께 이동하는 퍼즐입니다.'),
 ('스테판 울프', '장소를 조사하고 아이템과 단서를 모아 위기를 해결하는 에피소드형 어드벤처입니다.'),
 ('방탈출', '주변의 물건과 단서를 조사하고 퍼즐을 해결해 갇힌 장소에서 탈출하는 게임입니다.'),
 ('풍선타워|Kingdom Rush|템플 가디언|Xeno Tactic', '방어 시설을 배치하고 강화해 경로를 따라 들어오는 적을 막는 타워 디펜스 게임입니다.'),
 ('풍선 터트리기', '발사 방향과 힘을 조절해 제한된 횟수 안에 풍선을 터뜨리는 퍼즐입니다.'),
 ('바이크|업힐 러쉬', '속도와 균형을 조절하면서 경사와 장애물이 있는 코스를 통과하는 주행 게임입니다.'),
 ('테트리스|헥사', '떨어지는 블록을 적절히 배치해 줄이나 같은 색의 조합을 없애는 퍼즐 게임입니다.'),
 ('삼국지|삼국기', '장수와 도시, 부대를 운영하며 세력을 확장하는 삼국시대 전략 게임입니다.'),
 ('프린세스.*메이커', '교육과 활동을 계획해 딸을 성장시키고 다양한 결말을 만나는 육성 시뮬레이션입니다.'),
 ('대항해시대', '항해와 교역, 탐험을 통해 바다를 누비며 목표를 달성하는 시뮬레이션입니다.'),
 ('파이널 파이트|황금도끼|던전 & 드래곤|캐딜락스|천지를 먹다|캡틴 코만도|가디언즈|전국전승', '적들과 싸우며 길을 따라 전진하는 횡스크롤 액션 게임입니다.'),
 ('푸얀', '리프트를 타고 오르내리며 풍선을 타고 접근하는 늑대들을 활로 막아내는 게임입니다.'),
 ('장미와 동백', '상대의 움직임을 살피고 공격과 회피 타이밍을 맞추는 대결 게임입니다.'),
 ('46억년전', '생물의 몸을 진화시키며 여러 시대의 환경을 탐험하는 액션 RPG입니다.'),
 ('크로노 트리거', '시간을 넘나드는 모험과 동료들의 연계 전투가 중심인 RPG입니다.'),
 ('마리오 페인트', '그림 그리기와 음악 만들기 등 다양한 창작 활동을 즐기는 게임입니다.'),
 ('팩맨', '미로의 점을 모으면서 유령을 피하고 파워 아이템으로 반격하는 게임입니다.'),
 ('파이프 연결', '관을 이어 흐름이 끊기지 않도록 경로를 만드는 퍼즐입니다.'),
 ('공 생산 공장', '공에 색과 도구를 순서대로 적용해 제시된 모양을 재현하는 퍼즐입니다.'),
 ('매직펜', '도형을 그려 물체를 움직이고 목표 지점에 도달하게 하는 물리 퍼즐입니다.'),
 ('메가 붐버맨|네오 붐버맨|크래이지 아케이드', '폭탄이나 물풍선을 배치해 장애물을 없애고 상대를 가두는 액션 게임입니다.'),
]


def summary(row, genre):
    for pattern, description in SERIES:
        if re.search(pattern, row['title'], re.I):
            # Mario RPG / farming should not receive a platforming description.
            if pattern == '슈퍼마리오|슈퍼 마리오' and genre == 'RPG':
                continue
            return description, '편집 요약'
    body = row['body']
    body = re.sub(r'^[:\s\[\],~^]+', '', body)
    body = re.sub(r'다운로드[^\[]*\[[^\]]*\]', '', body)
    body = re.sub(r'https?://\S+|\S+\.(?:zip|rar|alz|7z|exe|swf)\b', '', body, flags=re.I)
    sentences = re.split(r'(?<=[.!?。])\s+', body)
    useful = [s.strip() for s in sentences if len(s.strip()) > 15 and not re.search(r'다운로드|보내주신|요청|도스박스|DOSBOX|실행기|마메|ROM|로그인|추천|덧글|댓글|압축|폴더|설치|사용법|감사|자료|tool[iy]|패스워드|암호|파일|보안|VM웨어|윈도우|Windows|실행|스크린샷|촬영|치트|테스트|제가|저는|저도|올렸|업로드|생각되|기억|재생버튼|type=|안영기|네요|군요|모르겠', s, re.I)]
    if useful:
        return (useful[0][:200] + ('…' if len(useful[0]) > 200 else '')), '원문 발췌'
    return f'{PLATFORMS[row["platform"]]} 게시판에 소개된 {genre} 게임입니다.', '게시판·장르 안내'


def method(row):
    # Keep factual source-specific controls when available. Generic genre help is separately labelled.
    lines = row['lines']
    for i, line in enumerate(lines):
        if not re.search(r'재생|로딩|설치|윈도우|Windows', line, re.I) and re.search(r'조작\s*(방법|법|키)|게임\s*방법|방향키|화살표|스페이스|사용키|이동\s*:|공격\s*:|마우스.*(클릭|사용|조작)|키보드.*(사용|제어)', line):
            snippet = ' '.join(lines[i:i+3]) if len(line) < 25 else line
            snippet = snippet.replace('이 게시물을', '')
            snippet = re.sub(r'https?://\S+', '', snippet).strip()
            return snippet[:180] + ('…' if len(snippet) > 180 else '')
    return None


def build():
    collected_at = (CACHE / 'collected-at.txt').read_text().strip() if (CACHE / 'collected-at.txt').exists() else datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat()
    raw = json.loads((CACHE / 'raw.json').read_text())
    images = json.loads((CACHE / 'images.json').read_text())
    flash_images = json.loads((CACHE / 'flash-images.json').read_text()) if (CACHE / 'flash-images.json').exists() else {}
    groups = json.loads((ROOT / 'docs/tooli-genre-overrides.json').read_text())
    overrides = {f'{mid}-{id}': genre for mid, gs in groups.items() for genre, ids in gs.items() for id in ids.split()}
    excluded = []
    games = []
    for row in raw:
        if row['notice'] or re.search(r'휴대용 게임기|실행기\s*자료|문제가 되는자료', row['title']):
            excluded.append({'id': row['id'], 'title': row['title'], 'source': row['source'], 'reason': '공지·실행기·기기 소개'})
            continue
        genre = overrides.get(row['id'], SOURCE_GENRES.get(row['sourceCategory'], '액션/아케이드' if row['platform'] != 'pc' else '기타/미분류'))
        desc, kind = summary(row, genre)
        game = {k: row[k] for k in ['id','platform','title','source','sourceCategory']}
        if row.get('access'):
            game['access'] = row['access']
        game.update({'genre': genre, 'genreBasis': '원문 카테고리' if row['sourceCategory'] in SOURCE_GENRES and row['id'] not in overrides else '편집 분류', 'description': desc, 'descriptionBasis': kind, 'basicMethod': BASICS[genre], 'sourceMethod': method(row), 'image': flash_images.get(row['id']) or images.get(row['id'])})
        if game['image']:
            game['image'].setdefault('kind', 'source-screenshot')
        else:
            game['imageStatus'] = '원문 비공개' if row.get('access') else ('원문에 스크린샷 없음' if not row['embeds'] else '원문 게임 파일의 화면 확인 불가')
        games.append(game)
    games.sort(key=lambda g: (list(PLATFORMS).index(g['platform']), g['title']))
    counts = Counter(g['platform'] for g in games)
    genres = Counter(g['genre'] for g in games)
    report = {'source': 'https://www.tooli.co.kr/', 'collectedAt': collected_at, 'platformBasis': 'Tooli 고전게임 메뉴의 게시판 분류. 게임보이 게시판은 GBA 게임을 포함합니다.', 'inventory': json.loads((CACHE / 'inventory.json').read_text()), 'restrictedPosts': [{'id': r['id'], 'title': r['title'], 'source': r['source']} for r in raw if r.get('access')], 'listedPosts': len(raw), 'games': len(games), 'platformCounts': dict(counts), 'genreCounts': dict(genres), 'screenshots': sum(bool(g['image']) for g in games), 'imageKinds': dict(Counter(g['image']['kind'] for g in games if g['image'])), 'flashCaptureFailures': json.loads((CACHE / 'flash-failures.json').read_text()) if (CACHE / 'flash-failures.json').exists() else [], 'missingScreenshots': [{'id': g['id'], 'title': g['title'], 'source':g['source'], 'reason':g['imageStatus']} for g in games if not g['image']], 'excluded': excluded, 'classification': 'PC 원문 카테고리를 통합하고 다른 게시판의 장르는 편집 분류했습니다. 기본 진행은 장르별 안내이며, 원문 조작법이 있는 경우 별도로 표시합니다.'}
    payload = {'collectedAt': report['collectedAt'], 'platforms':PLATFORMS, 'games': games}
    (ROOT / 'public/data/tooli-games.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'docs/tooli-crawl-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    esc = lambda v: html.escape(str(v), quote=True)
    buttons = ''.join(f'<button type="button" data-platform="{mid}" data-label="{label}" aria-pressed="false">{label} <span>{counts[mid]}</span></button>' for mid, label in PLATFORMS.items())
    options = ''.join(f'<option value="{esc(g)}">{esc(g)} ({genres[g]})</option>' for g in GENRES if genres[g])
    cards = []
    for game in games:
        img = game['image']
        screenshot = f'<a class="game-screenshot" href="{esc(img["src"])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(game["title"])} 화면 크게 보기"><img src="{esc(img["src"])}" width="{img["width"]}" height="{img["height"]}" loading="lazy" decoding="async" alt="{esc(game["title"])} 게임 화면"></a>' if img else f'<span class="game-image-missing">{esc(game["imageStatus"])}<br>자세한 내용은 원문 링크에서 확인해 주세요.</span>'
        controls = f'<p class="game-method"><strong>원문 조작법</strong> {esc(game["sourceMethod"])}</p>' if game['sourceMethod'] else ''
        cards.append(f'''<section id="{game['id']}" class="classic-game" data-platform="{game['platform']}" data-genre="{esc(game['genre'])}" aria-labelledby="{game['id']}-title">
{screenshot}
<p class="game-tags">{PLATFORMS[game['platform']]} · {esc(game['genre'])}</p>
<h2 id="{game['id']}-title">{esc(game['title'])}</h2>
<p>{esc(game['description'])}</p>
<p class="game-method"><strong>기본 진행</strong> {esc(game['basicMethod'])}</p>
{controls}{'<p class="game-method">원문 본문은 비공개입니다.</p>' if game.get('access') else ''}<p class="game-source"><a href="{esc(game['source'])}">Tooli 원문</a> · {esc(game['genreBasis'])}</p>
</section>''')
    page = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Tooli의 고전게임 {len(games)}개를 게임 화면과 함께 살펴보세요. PC, 오락실, 게임보이, 슈퍼패미콤, 메가드라이브, MSX, 플래시의 플랫폼·장르 필터와 검색.">
<title>tooli의 고전게임 정리 · nyimpe</title>
<link rel="canonical" href="https://nyimpe.github.io/posts/classic-games/">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="stylesheet" href="/src/style.css">
<link rel="stylesheet" href="/src/classic-games.css">
<script type="module" src="/src/main.js"></script>
<script type="module" src="/src/classic-games.js"></script>
</head>
<body>
<a class="skip-link" href="#content">본문으로 이동</a>
<header class="site-header">
<div class="header-content"><nav lang="en" class="site-nav" aria-label="Main navigation">
<a href="/">Home</a><a href="/about/">About</a><a href="https://github.com/nyimpe">GitHub</a>
<button id="theme-toggle" class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false" hidden>☾</button>
</nav><hr></div>
<img class="site-cat" src="/cat.png" width="88" height="160" alt="주황색과 흰색의 픽셀아트 고양이">
</header>
<main id="content"><article class="classic-post">
<header class="post-header"><h1>tooli의 고전게임 정리</h1><time datetime="{collected_at}">{collected_at.replace("-", ".")}</time>
<p>추억 속 게임을 플랫폼과 장르로 찾아보세요.</p></header>
<p class="classic-intro">출처: <a href="https://www.tooli.co.kr/pc">Tooli의 고전게임</a> · 7개 플랫폼 · {len(games)}개 게임 · {report['screenshots']}개 화면. 플랫폼은 Tooli 게시판 기준이며 게임보이는 GBA를 포함합니다. 공지·실행기·기기 소개는 제외했습니다.</p>
<p class="classic-intro">장르는 원문 분류와 편집 분류를 함께 사용했습니다. ‘기본 진행’은 장르별 안내이며, 확인 가능한 원문 조작법은 따로 표시했습니다. 이미지는 원문 스크린샷 또는 실제 플래시 화면 캡처입니다.</p>
<form class="classic-filter" aria-label="게임 필터" hidden>
<fieldset class="game-platforms"><legend>플랫폼</legend><div class="game-platform-buttons">
<button type="button" data-platform="" data-label="전체" aria-pressed="true">전체 <span>{len(games)}</span></button>{buttons}
</div></fieldset>
<div class="game-filter-fields"><label for="game-genre">장르<select id="game-genre"><option value="">전체 장르</option>{options}</select></label>
<label for="game-search">게임 검색<input id="game-search" type="search" placeholder="게임명 또는 설명" autocomplete="off"></label>
<button class="game-reset" type="reset">필터 초기화</button></div>
</form>
<p class="game-count" id="game-count" role="status" aria-atomic="true">전체 · {len(games)}개 게임</p>
<p class="game-empty" id="game-empty" hidden>일치하는 게임이 없습니다. 검색어를 바꾸거나 필터를 초기화해 주세요.</p>
<noscript><p>JavaScript를 켜면 플랫폼·장르 필터와 검색을 사용할 수 있습니다. 아래에서 전체 게임을 볼 수 있습니다.</p></noscript>
<div class="classic-games">{''.join(cards)}</div>
<p class="game-load-status" id="game-load-status" role="status" aria-atomic="true" hidden></p>
<div class="game-load-trigger" id="game-load-trigger" aria-hidden="true" hidden></div>
<p class="classic-intro"><a href="/data/tooli-games.json">수집한 게임 정보 JSON</a> · 게임별 자세한 정보는 원문 링크에서 확인할 수 있습니다.</p>
<p class="post-back"><a href="/">← Home</a></p>
</article></main>
<footer class="site-footer">Small things, made and remade. <a href="https://github.com/nyimpe/nyimpe.github.io">Source code</a></footer>
</body></html>
'''
    (ROOT / 'posts/classic-games/index.html').write_text(page)
    print(json.dumps({k: report[k] for k in ['games','platformCounts','genreCounts','screenshots','missingScreenshots']}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    build()
