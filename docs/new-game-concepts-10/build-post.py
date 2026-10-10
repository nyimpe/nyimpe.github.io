"""Build the ten-concept article from reviewed text and generated art records."""
import hashlib
import json
from html import escape
from pathlib import Path
from PIL import Image

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[1]
SLUG = 'new-game-concepts-10'
PAGE = ROOT / 'posts' / SLUG / 'index.html'
DATA = json.loads((DOCS / 'concepts.json').read_text())
CONCEPTS = DATA['concepts']
assert [c['id'] for c in CONCEPTS] == list(range(1, 11))
ART = {}
for record_path in sorted(DOCS.glob('art-*.json')):
    for item in json.loads(record_path.read_text())['assets']:
        assert item['id'] not in ART
        ART[item['id']] = {**item, 'promptFile': record_path.name}
assert set(ART) == set(range(1, 11))

images = []
for c in CONCEPTS:
    asset = ART[c['id']]
    relative = f'public/images/{SLUG}/concept-{c["id"]:02}.webp'
    path = ROOT / relative
    with Image.open(path) as im:
        im.load()
        width, height = im.size
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    assert asset['sha256'] == sha, f'Stale art record: {relative}'
    images.append({
        'id': c['id'], 'title': c['title'], 'file': relative,
        'src': f'/images/{SLUG}/concept-{c["id"]:02}.webp?v={sha[:12]}',
        'width': width, 'height': height, 'bytes': path.stat().st_size,
        'sha256': sha, 'source': asset['source'],
        'sourceSha256': hashlib.sha256(Path(asset['source']).read_bytes()).hexdigest(),
        'promptFile': asset['promptFile'], 'alt': c['alt'],
    })
(DOCS / 'manifest.json').write_text(json.dumps({
    'generator': 'built-in image_gen', 'created': DATA['date'],
    'post': str(PAGE.relative_to(ROOT)),
    'encoding': {'format': 'WebP', 'maxSize': [1280, 720], 'quality': 82},
    'images': images,
}, ensure_ascii=False, indent=2) + '\n')

e = escape
title = e(DATA['title'])
description = '기존 113개 기획의 핵심 선택과 비교해 새로 제안하는 게임 10개. 종이 접기·직조·진단·부력·언어·지층·노광·측량·신문·조각을 플레이 컨셉아트, 정확한 규칙과 예시, 첫 시제품 범위로 정리합니다.'
toc = '\n'.join(f'<li><a href="#c{c["id"]}">{c["id"]:02}. {e(c["title"])}</a></li>' for c in CONCEPTS)
rows = '\n'.join(f'<tr><th scope="row"><a href="#c{c["id"]}">{c["id"]:02}. {e(c["title"])}</a></th><td>{e(c["decision"])}</td><td>{e(c["legacy"])}</td><td>{e(c["newCore"])}</td></tr>' for c in CONCEPTS)
scene_notes = {
    1: '그림은 접힘과 문 연결의 시안입니다. 방 좌표와 뒤집힘 규칙은 아래 예시를 기준으로 읽습니다.',
    2: '실 조직의 위치와 강조 표시는 시안입니다. 실제 검사는 아래의 6칸 문자열과 연속 길이를 기준으로 합니다.',
    6: '그림의 층·표본 기호는 분위기 시안이며, A–E 사건의 정확한 선후 관계는 아래 예시를 따릅니다.',
    7: '실루엣·마스크는 시안입니다. 아래 A·B·C 예시에서는 노광이 누적될수록 더 짙어집니다.',
    8: '그림의 원 크기·관측소 배치는 수치 도면이 아닙니다. 거리와 교점은 아래 좌표 예시를 기준으로 합니다.',
    9: '그림의 제목·카드 수는 시안입니다. 실제 판정에는 본문의 8칸 지면과 공개된 범위 태그를 사용합니다.',
    10: '그림은 입체와 투영을 함께 읽는 화면 구상입니다. 정확한 3×3×3 제거 위치는 아래 예시를 따릅니다.',
}
articles = []
for c, art in zip(CONCEPTS, images):
    i = c['id']
    src = e(art['src'])
    rules = '\n'.join(f'<li><strong>{e(label)}:</strong> {e(text)}</li>' for label, text in c['rules'])
    note = f'<p class="image-credit">{e(scene_notes[i])}</p>' if i in scene_notes else ''
    loading = 'loading="eager" fetchpriority="high"' if i == 1 else 'loading="lazy"'
    articles.append(f'''<article id="c{i}" class="concept" aria-labelledby="c{i}-title">
<h3 id="c{i}-title"><span class="concept-genre">{e(c['genre'])}</span> {i:02}. {e(c['title'])}</h3>
<figure class="concept-shot">
<a href="{src}" target="_blank" rel="noopener noreferrer"><img src="{src}" width="{art['width']}" height="{art['height']}" {loading} decoding="async" alt="{e(c['alt'])} AI 플레이 컨셉아트."></a>
<figcaption>{e(c['caption'])} · AI 플레이 컨셉아트</figcaption>
</figure>
{note}
<p class="concept-pitch">{e(c['pitch'])}</p>
<p class="concept-meta">{e(c['english'])} · 1인 · PC·브라우저 · 2D 픽셀아트 · 예상 {e(c['session'])}</p>
<p><strong>세계관:</strong> {e(c['world'])}</p>
<p><strong>목표:</strong> {e(c['goal'])}</p>
<p><strong>진행:</strong> {e(c['loop'])}</p>
<ul>{rules}</ul>
<p><strong>플레이 예시:</strong> {e(c['example'])}</p>
<p><strong>성장과 실패:</strong> {e(c['growth'])}</p>
<p><strong>기존 기획과의 차이:</strong> {e(c['difference'])}</p>
<p><strong>조작·접근성:</strong> {e(c['controls'])}</p>
<p><strong>첫 시제품:</strong> {e(c['prototype'])}</p>
<p class="concept-meta"><strong>먼저 검증할 것:</strong> {e(c['validation'])}</p>
<p class="concept-meta"><a href="#comparison">비교표로 돌아가기</a> · <a href="#contents">목차로 돌아가기</a></p>
</article>''')

html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(description)}">
<title>{title} · nyimpe</title>
<link rel="canonical" href="https://nyimpe.github.io/posts/{SLUG}/">
<meta property="og:type" content="article">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="https://nyimpe.github.io/posts/{SLUG}/">
<meta property="og:image" content="https://nyimpe.github.io{e(images[0]['src'])}">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="stylesheet" href="/src/style.css">
<script type="module" src="/src/main.js"></script>
</head>
<body>
<a class="skip-link" href="#content">본문으로 이동</a>
<header class="site-header">
<div class="header-content">
<nav lang="en" class="site-nav" aria-label="Main navigation">
<a href="/">Home</a><a href="/about/">About</a><a href="https://github.com/nyimpe">GitHub</a>
<button id="theme-toggle" class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false" hidden>☾</button>
</nav><hr>
</div>
<img class="site-cat" src="/cat.png" width="88" height="160" alt="주황색과 흰색의 픽셀아트 고양이">
</header>
<main id="content">
<article class="research-post design-post">
<header class="post-header">
<h1>{title}</h1>
<time datetime="{DATA['date']}">2026.10.10</time>
<p><strong>이번에는 재료와 배경보다, 손으로 하는 판단을 바꿉니다.</strong> 기존 기획에서 다룬 배송·정원·배합·관찰·공연·원정과 다른 중심 규칙을 고른 열 가지 창작 게임입니다. 고양이·강아지와 작은 생활 공간이라는 최근 기획의 분위기는 이어가되, 매번 반복하는 행동은 접기·짜기·진단·균형·해석·발굴·노광·측량·편집·깎기로 나눴습니다.</p>
<p>여러 기획을 한 글에서 비교할 수 있도록 기존 기획 모음의 <strong>플레이 이미지 → 한 줄 소개 → 목표·규칙 → 선택 예시 → 차별점 → 첫 시제품과 검증</strong> 형식을 사용합니다. 각 안은 1인용 PC·브라우저 게임을 상정하며, 큰 생활 시뮬레이션으로 확장하기 전에 한 가지 판단이 재미있는지 확인할 수 있는 크기로 잡았습니다.</p>
<p>플레이 시간·수치·콘텐츠 수량·통과 기준은 모두 <strong>아직 플레이테스트하지 않은 설계 가정</strong>입니다. 아래 계산은 제안한 게임 규칙 안의 예시이며, 직물·선박·음향·사진·발굴을 위한 현실 전문 도구가 아닙니다.</p>
<p class="image-credit">각 기획의 이미지 1장, 총 10장은 AI로 만든 플레이 컨셉아트입니다. 실제 실행 화면이나 완성 게임 에셋은 아닙니다. 그림의 영어 UI·격자·수치는 화면 구상이며 정확한 규칙은 본문 예시를 기준으로 읽습니다. 최종 게임은 한글 UI를 전제로 합니다.</p>
</header>
<nav id="contents" class="post-toc" aria-label="목차"><ol>
<li><a href="#basis">기존 기획과 비교한 기준</a></li>
<li><a href="#comparison">열 기획 비교</a></li>
{toc}
<li><a href="#next">먼저 만들어 볼 세 가지</a></li>
<li><a href="#refs">비교한 기존 기획</a></li>
</ol></nav>

<section id="basis" aria-labelledby="basis-title">
<h2 id="basis-title">기존 기획과 비교한 기준</h2>
<p>비교 범위는 이 사이트의 기존 <strong>기획 글 9개, 아이디어 113개</strong>입니다. 한국 괴물·귀신 기획 43개와 추가 50개, 파티 RPG 6개, 보드게임 기반 9개, 생활·탐험 개별 기획 5개를 살폈습니다. 장르가 일부 같더라도 <strong>무엇을 관찰하고, 무엇을 바꾸며, 어떤 결과로 완료하는가</strong>를 다르게 설계했습니다.</p>
<ul>
<li><strong>최근 생활 기획:</strong> 물결우체국의 우편·항로, 온기골의 온도·향·휴식 공간, 유리사막의 생태 도감, 뿌리별의 빛·습도·살아 있는 길, 골목달의 배우·소리·장치 순서를 새 안의 중심으로 반복하지 않았습니다.</li>
<li><strong>기존 전략 기획:</strong> 계약·법칙·피난처·행동 예약·철수·전투 정보, 묶음 구매·계절 정원·배송 시간표·화물 덱·추가 뽑기·공유 경로·협력 복구·경매·제한 소통을 별도로 대조했습니다.</li>
<li><strong>구별이 필요한 경우:</strong> 발굴은 물건 이름 대신 사건 순서, 사진은 관찰 수집 대신 영역별 노광, 측량은 발사 각도 대신 거리 역추론, 신문은 진위 심사 대신 확인된 사실의 맥락 편집, 조각은 평면 정답 대신 여러 투영의 동시 충족을 다룹니다.</li>
</ul>
<p>이 비교는 <strong>이 사이트에서 앞서 제안한 내용과의 중복을 줄이기 위한 것</strong>입니다. 전 세계에 같은 소재나 부분 규칙을 사용한 게임이 없다는 뜻은 아닙니다.</p>
</section>

<section id="comparison" aria-labelledby="comparison-title">
<h2 id="comparison-title">열 기획 비교</h2>
<div class="table-scroll" tabindex="0" role="region" aria-label="열 기획의 핵심 판단과 기존 기획의 차이. 가로로 스크롤할 수 있습니다.">
<table><caption>각 게임에서 반복할 판단과 가장 가까운 기존 요소를 함께 비교합니다</caption>
<thead><tr><th scope="col">기획</th><th scope="col">반복하는 질문</th><th scope="col">가까운 기존 요소</th><th scope="col">이번 기획의 중심</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>
</section>

<section id="concepts" aria-labelledby="concepts-title">
<h2 id="concepts-title">게임 기획 열 가지</h2>
{''.join(articles)}
</section>

<section id="next" aria-labelledby="next-title">
<h2 id="next-title">먼저 만들어 볼 세 가지</h2>
<p>아래 순서는 시장성과 판매량 예측이 아니라, <strong>규칙을 작게 구현해 핵심 판단을 확인하기 쉬운 정도</strong>에 따른 제작 제안입니다.</p>
<ol>
<li><strong><a href="#c7">겹빛 사진실</a>:</strong> 영역별 정수 3개와 가림 선택만으로 첫 퍼즐을 만들 수 있습니다. 정확한 노광 예시가 이해되는지 확인한 뒤 복잡한 원판을 늘립니다.</li>
<li><strong><a href="#c3">잔향 수리점</a>:</strong> 물건 하나와 고장 후보 3개로 ‘부품 교체 전에 시험을 고르는 재미’를 확인할 수 있습니다. 자유 물리 없이도 가설과 결과의 논리를 검증할 수 있습니다.</li>
<li><strong><a href="#c10">속빈 조각실</a>:</strong> 27칸의 상태와 두 투영으로 입체 추론의 핵심을 확인할 수 있습니다. 여러 정답을 인정하면서 조작이 이해되는지 먼저 살핍니다.</li>
</ol>
<p>첫 검증에서는 진행 시간, 사용한 힌트, 되돌린 행동, 완료 후 규칙 설명을 기록합니다. 수집 개수·계절·경제·관계 서사를 늘리는 일은 이 판단이 명확하게 전달된 다음에 정합니다.</p>
</section>

<section id="refs" aria-labelledby="refs-title">
<h2 id="refs-title">비교한 기존 기획</h2>
<p>본문의 새 게임 규칙은 이번에 작성한 창작 제안입니다. 아래 링크는 같은 사이트에서 중복 여부와 양식을 확인한 기존 문서입니다.</p>
<ul class="ref-list">
<li><a href="/posts/board-game-concepts/">인기 보드게임에서 출발한 게임 기획 9선</a> — 비교표·개별 이미지·규칙·턴 예시·시제품 형식.</li>
<li><a href="/posts/party-deckbuilding-rpg-concepts/">파티·덱 구축·원정 RPG 기획 6선</a> — 중심 선택, 성장·실패, 검증 범위.</li>
<li><a href="/posts/korean-folklore-game-design/">한국 괴물·귀신 게임 기획 43개</a> · <a href="/posts/korean-folklore-game-design-50/">추가 기획 50선</a> — 기존 퍼즐·액션·전략의 중심 규칙.</li>
<li><a href="/posts/tidepost/">물결우체국</a> · <a href="/posts/warmrest/">온기골 온천집</a> · <a href="/posts/glasswild/">유리사막 도감차</a> · <a href="/posts/rootstar/">뿌리별 균사정원</a> · <a href="/posts/alleymoon/">골목달 장난감극장</a> — 최근 생활 기획의 주인공·공간·행동 차이.</li>
</ul>
</section>
<p class="post-back"><a href="/">← 모든 글</a></p>
</article>
</main>
<footer class="site-footer">Small things, made and remade. <a href="https://github.com/nyimpe/nyimpe.github.io">Source code</a></footer>
</body>
</html>
'''
PAGE.parent.mkdir(parents=True, exist_ok=True)
PAGE.write_text(html)
print(json.dumps({'page': str(PAGE), 'concepts': len(CONCEPTS), 'images': len(images), 'imageBytes': sum(x['bytes'] for x in images)}, ensure_ascii=False))
