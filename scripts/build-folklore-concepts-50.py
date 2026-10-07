#!/usr/bin/env python3
"""Render the 2026-10-07 design post from its reviewed concepts and provenance."""
from html import escape
from pathlib import Path
from urllib.parse import quote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/folklore-game-concepts/2026-10-07'
SLUG = 'korean-folklore-game-design-50'
TITLE = '한국 괴물·귀신 게임 기획 50선'
CONCEPTS = json.loads((DOCS / 'concepts.json').read_text())
CREATURES = json.loads((DOCS / 'creature-evidence.json').read_text())
assert [g['id'] for g in CONCEPTS] == list(range(1, 51))
assert len({g['title'] for g in CONCEPTS}) == 50
CATALOGS = {}
for dataset, slug in [('playretrogames-games', 'playretrogames'),
                      ('retrogames-onl-snes-games', 'retrogames-onl-snes'),
                      ('tooli-games', 'classic-games'), ('jjang-games', 'jjang-games'),
                      ('playretro-io-games', 'playretro-io')]:
    for g in json.loads((ROOT / f'public/data/{dataset}.json').read_text())['games']:
        CATALOGS[g['id']] = (g, slug, dataset)
LOGIC_NAMES = {'bridges': '브릿지', 'slitherlink': '슬리더 링크',
               'nonograms': '노노그램', 'shikaku': '시카쿠'}
ASSETS = {a['id']: a for a in json.loads((DOCS / 'manifest.json').read_text())} if (DOCS / 'manifest.json').exists() else {}


def link(url, label):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def reference(g):
    if g['reference'].startswith('logic:'):
        anchor = g['reference'].split(':')[1]
        return link(f'/posts/logic-puzzles/#{anchor}', LOGIC_NAMES[anchor]), None
    game, slug, _ = CATALOGS[g['reference']]
    return link(f'/posts/{slug}/?q={quote(game["title"])}#{game["id"]}', game['title']), game


groups = ['격자·낙하·굴착 퍼즐', '연결 논리·미로·유인', '이동·반사·예측 액션',
          '장치·관성·지형 슈팅', '대전·스포츠·협동']
parts = []
base = (ROOT / 'posts/korean-folklore-game-design/index.html').read_text()
head = base[:base.index('        <header class="post-header">')]
head = head.replace('한국 괴물·귀신 게임 기획', TITLE)
head = head.replace('/posts/korean-folklore-game-design/', f'/posts/{SLUG}/')
head = head.replace('한국 괴물·귀신 326항목을 바탕으로 한 2D 픽셀아트 게임 기획. 장르 시장 조사와 마흔세 가지 컨셉 플레이 화면.',
                    '수집한 레트로·아케이드·논리 퍼즐에서 발전시킨 새로운 한국 괴물·귀신 게임 기획 50개. 플레이 규칙·예시·조작·데모 범위와 AI 플레이 컨셉아트.')
og = ASSETS.get(1, {}).get('src', '/images/folklore-game-50/concept-01.webp')
head = re.sub(r'(<meta property="og:image" content=")[^"]+', rf'\g<1>https://nyimpe.github.io{og}', head)
parts.append(head)
parts.append(f'''        <header class="post-header">
          <h1>{TITLE}</h1>
          <time datetime="2026-10-07">2026.10.07</time>
          <p class="image-credit">바탕 자료: {link('/posts/korean-folklore-research/', '한국 괴물·귀신')} 326항목 · 레퍼런스: 앞서 수집한 게임 도감과 논리 퍼즐 · 이미지: 개별 규칙을 바탕으로 새로 제작한 AI 픽셀아트 플레이 시안</p>
          <p>{link('/posts/korean-folklore-game-design/', '한국 괴물·귀신 게임 기획 [2026.10.06]')}의 공통 세계관과 글 구성을 이어받은 후속 기획입니다. 기존 43개는 그대로 두고, 새로운 50개를 추가합니다.</p>
        </header>
        <nav class="post-toc" aria-label="목차"><ol>
          <li><a href="#source">자료에서 읽은 것</a></li><li><a href="#core">공통 기획: 괴이록</a></li>
          <li><a href="#reference">수집 게임 레퍼런스 비교</a></li><li><a href="#concepts">새 컨셉 쉰 가지</a></li>
          <li><a href="#next">우선순위</a></li><li><a href="#refs">출처</a></li>
        </ol></nav>
        <section id="source" aria-labelledby="source-title">
          <h2 id="source-title">1. 자료에서 읽은 것</h2>
          <p>앞서 모은 {link('/posts/classic-games/', 'tooli')}, {link('/posts/jjang-games/', '짱게임')}, {link('/posts/playretrogames/', 'Play Retro Games')}, {link('/posts/playretro-io/', 'PlayRetro.io')}, {link('/posts/retrogames-onl-snes/', 'RetroGames.onl')}과 {link('/posts/logic-puzzles/', '온라인 논리 퍼즐 41종')}을 함께 검토했습니다. 같은 작품의 이식판과 중복 등록은 별개의 성공 사례로 세지 않았습니다. 아래 기획은 장르명을 바꾸는 대신, 한 판에서 반복하는 행동과 승패 조건을 새로 정한 것입니다.</p>
          <ul>
            <li><strong>규칙 하나를 먼저 읽게 한다.</strong> 폭발 뒤 피하기, 적을 가둔 뒤 터뜨리기, 바닥을 판 뒤 떨어지는 돌처럼 원인과 결과가 한 화면에서 이어지는 구조를 가져옵니다.</li>
            <li><strong>괴물 성질이 선택을 바꾼다.</strong> 쇠를 먹는 불가살이 때문에 강한 무기를 멈추고, 시선에 멈추는 공주산 때문에 관측 방향을 바꾸며, 체를 세는 야광 때문에 시간을 벌게 합니다.</li>
            <li><strong>처음에는 짧은 완성 단위를 만든다.</strong> 한 화면, 고정 문제, 3~5분 구간, 봇 한 명으로 핵심 재미를 검토합니다. 아래 규모는 목표 범위이며 제작 완료 상태가 아닙니다.</li>
          </ul>
        </section>
        <section id="core" aria-labelledby="core-title">
          <h2 id="core-title">2. 공통 기획: 괴이록(가제)</h2>
          <p><strong>문헌 속 괴물을 기록하고 그 성질로 문제를 푸는 사람들</strong>이라는 기존 세계관을 유지합니다. 50개를 한 게임에 모두 넣기보다, 독립된 작은 후보로 비교합니다. 전승 기록은 각 항목의 ‘전승에서 가져온 것’에, 수치·목표·장비·변신 조작 등 새로운 설정은 ‘창작 규칙’에 구분합니다.</p>
          <ol>
            <li><strong>도감은 공통 진행 자원.</strong> 처음 만난 존재의 기록과 대응 조건을 남깁니다. 성능을 무한히 올리는 영구 강화는 기본 전제로 삼지 않습니다.</li>
            <li><strong>경영·자동화·방치·크리처 수집은 이번에도 제외.</strong> 반복적인 관리나 수집량보다 조작, 추론, 짧은 승패를 중심에 둡니다.</li>
            <li><strong>플레이 예시로 규칙 검증.</strong> 한 장면에서 입력 → 상태 변화 → 다음 선택을 설명합니다. 본문의 조작은 새 기획의 제안이며 참고 게임의 원래 키 배치가 아닙니다.</li>
            <li><strong>전승의 한계를 보존.</strong> 외형이 불명인 거악·착착귀신은 그림자나 파동으로 표현합니다. 실제 인물·질병·자연현상 기록은 해설의 맥락을 유지합니다.</li>
          </ol>
          <p>프로토타입은 기존 글처럼 320×180 기본 화면, 16~24px 캐릭터, 한지·먹·이끼·주홍·밤 남색 팔레트를 목표로 합니다. 논리 퍼즐은 정답 검증을, 액션은 입력과 충돌의 일치를 먼저 확인합니다. 아래 그림은 규칙과 장면을 설명하는 고해상도 컨셉아트이며 실행 화면이나 완성 에셋이 아닙니다. 작은 HUD 숫자·표시는 시안이므로 정확한 조건은 본문을 기준으로 읽습니다.</p>
        </section>
        <section id="reference" aria-labelledby="reference-title">
          <h2 id="reference-title">3. 수집 게임 레퍼런스 비교</h2>
          <p>이번에는 수집 자료의 규칙을 제작 관점에서 비교합니다. 판매량·가격·시장 도달률을 새로 추정하지 않습니다. ‘부담’과 우선순위는 문제 수, 입력 종류, 충돌·AI·물리·해답 검증을 고려한 기획 판단입니다. 원작의 캐릭터·맵·이미지는 새 게임 에셋으로 사용하지 않습니다.</p>
          <div class="table-scroll"><table><caption>다섯 묶음의 빌려 온 재미와 새 대응 규칙</caption>
            <thead><tr><th scope="col">묶음</th><th scope="col">수집 레퍼런스</th><th scope="col">빌려 온 재미</th><th scope="col">새로 바뀐 선택</th><th scope="col">부담</th></tr></thead>
            <tbody>
              <tr><th scope="row">01–10 격자·낙하</th><td>Neo Bomberman, Bubble Bobble, Snow Bros, Puyo Pop, Sokoban</td><td>위치와 제거 순서</td><td>쇠가 적을 키움 · 포획 뒤 봉인 · 시선이 밀기를 제한</td><td>낮음~중간</td></tr>
              <tr><th scope="row">11–20 논리·미로</th><td>Pipe Dream, 브릿지, 슬리더 링크, 노노그램, Pac-Man, Lode Runner</td><td>조건을 겹쳐 유일한 길 찾기</td><td>수결 문 · 고리의 안팎 · 다른 두 귀구의 추격</td><td>낮음~중간</td></tr>
              <tr><th scope="row">21–30 이동·반사</th><td>Frogger, Bionic Commando, Ice Climber, Marble Madness, Kurukuru Kururin, Arkanoid</td><td>궤적과 안전한 타이밍</td><td>귀환 보폭 · 긴 팔 관성 · 바람과 회전 몸체</td><td>중간</td></tr>
              <tr><th scope="row">31–40 슈팅</th><td>R-Type, Pop’n TwinBee, Gradius II, Sub-Terrania, Contra, Metal Slug</td><td>장치·방향·위치의 교환</td><td>쇠등불 분리 · 두 몸 간격 · 포를 내려야 하는 적</td><td>중간~높음</td></tr>
              <tr><th scope="row">41–50 대전·협동</th><td>Samurai Shodown, WindJammers, Super Dodge Ball, Worms, Rampart, Spy vs Spy, The Lost Vikings</td><td>간격·상대 의도·역할 조합</td><td>착지 응시 · 긴 팔 고정 · 돌 상태 · 세 존재의 출구</td><td>중간~높음</td></tr>
            </tbody></table></div>
          <p class="table-note">각 기획의 참고 링크는 실제 수집 항목 또는 기존 규칙 글로 연결합니다. 원작의 이식판마다 세부 규칙은 다를 수 있으며, 여기서 빌린 것은 표에 적은 핵심 구조입니다. 논리 퍼즐의 추가 조건은 새 문제 설계가 필요합니다.</p>
        </section>
        <section id="concepts" aria-labelledby="concepts-title">
          <h2 id="concepts-title">4. 새 컨셉 쉰 가지</h2>
          <details class="io-common"><summary>50개 기획 바로가기</summary><ol>''')
for g in CONCEPTS:
    parts.append(f'<li>{link("#c"+str(g["id"]), g["title"])} — {escape(g["genre"])}</li>')
parts.append('</ol></details>')
provenance = []
for g in CONCEPTS:
    i = g['id']
    if (i-1) % 10 == 0:
        group = (i-1)//10
        parts.append(f'<h3 id="group-{group+1}" class="concept-group">{i:02d}–{i+9:02d}. {groups[group]}</h3>')
    ref, game = reference(g)
    if game:
        provenance.append({'conceptId': i, 'referenceId': game['id'], 'referenceTitle': game['title'],
                           'dataset': CATALOGS[g['reference']][2], 'source': game['source']})
    else:
        provenance.append({'conceptId': i, 'referenceId': g['reference'], 'source': '/posts/logic-puzzles/'})
    parts.append(f'<article id="c{i}" class="concept" aria-labelledby="c{i}-title"><h3 id="c{i}-title"><span class="concept-genre">{escape(g["genre"])}</span> {i:02d}. {escape(g["title"])}</h3>')
    if i in ASSETS:
        a = ASSETS[i]
        parts.append(f'<figure class="concept-shot"><a href="{escape(a["src"])}" target="_blank" rel="noopener noreferrer"><img src="{escape(a["src"])}" width="{a["width"]}" height="{a["height"]}" loading="lazy" decoding="async" alt="{escape(g["alt"])}"></a><figcaption>{escape(g["caption"])} · AI 플레이 컨셉아트</figcaption></figure>')
    parts.append(f'<p class="concept-pitch">{escape(g["pitch"])}</p><ul>')
    parts.append(f'<li><strong>루프</strong>: {escape(g["loop"])}</li>')
    evidence = ' '.join(link('/posts/korean-folklore-research/#'+c, CREATURES[c]['name'])+' — '+escape(CREATURES[c]['description']) for c in g['creatures'])
    parts.append(f'<li><strong>전승에서 가져온 것</strong>: {evidence}</li>')
    parts.append(f'<li><strong>창작 규칙·승패</strong>: {escape(g["rule"])}</li>')
    parts.append(f'<li><strong>플레이 예시</strong>: {escape(g["example"])}</li>')
    parts.append(f'<li><strong>조작 제안</strong>: {escape(g["controls"])}</li></ul>')
    original = (' · '+link(game['source'], '수집 원문')) if game else ''
    parts.append(f'<p class="concept-meta">참고: {ref}{original} · 빌린 재미: {escape(g["borrowed"])}<br>최소 데모: {escape(g["scope"])} · 제작 쟁점: {escape(g["risk"])}</p></article>')
parts.append('''        </section>
        <section id="next" aria-labelledby="next-title">
          <h2 id="next-title">5. 우선순위</h2>
          <p>우선순위는 시장 성과 예측이 아니라 <strong>괴물 성질이 규칙을 바꾸는 정도, 한 화면으로 검토 가능한 범위, 기존 코드 재사용 가능성</strong>을 기준으로 정했습니다.</p>
          <ol>
            <li><strong><a href="#c9">공주산을 옮겨라</a></strong> — 관측 조건이 밀기 퍼즐의 선택을 직접 바꿉니다. 첫 검토는 산 한 개·거울 한 개·문제 네 개로 줄이고, 모든 문제가 풀리며 되돌리기가 정확한지 확인합니다.</li>
            <li><strong><a href="#c13">공리비사 바람테두리</a></strong> — 하나의 고리와 안팎 조건으로 창작 규칙이 명확합니다. 6×6 문제 네 개의 유일 해답과 모바일 선 입력부터 확인합니다.</li>
            <li><strong><a href="#c1">도깨비 화승고</a></strong> — 익숙한 폭발 규칙에 쇠먹이의 반대 효과가 붙습니다. 창고 세 개에서 폭발 예고·성장·통로 막힘·재시작을 검토합니다.</li>
            <li><strong><a href="#c28">박위의 밤 역참</a></strong> — 네 귀를 청각 단서와 경로 선택으로 옮길 수 있습니다. 갈림길 한 번, 위험 두 종류로 소리와 시각 안내의 동등성을 확인합니다.</li>
            <li><strong><a href="#c43">장비인 풍환</a></strong> — 팔을 펼 때 이동을 포기하는 선택을 짧은 경기로 검토합니다. 봇 한 명과 기본 코트에서 받기 판정·반사·7점 종료를 확인합니다.</li>
          </ol>
          <p><a href="#c14">네 눈의 복원도</a>와 <a href="#c15">망량의 방 나누기</a>는 고정 문제 제작이 먼저입니다. <a href="#c22">장비인의 처마걸이</a>와 <a href="#c25">거해 등껍질 길</a>는 관성과 충돌 조율이 필요해 그다음에 둡니다. 슈팅 열 개는 짧은 한 구간으로 적 패턴을 검토한 뒤 확장하고, <a href="#c50">세 그림자의 출구</a>는 세 역할을 모두 재시작·되돌리기와 함께 검증해야 하므로 후순위입니다.</p>
          <p>이번 결과물은 50개 기획과 플레이 컨셉아트입니다. 다음 제작 단계에서는 후보 하나를 골라 위의 최소 검토 범위로 실제 웹 데모를 만듭니다.</p>
        </section>
        <section id="refs" aria-labelledby="refs-title">
          <h2 id="refs-title">6. 출처</h2>
          <ul class="ref-list">
            <li>기존 세계관·형식: <a href="/posts/korean-folklore-game-design/">한국 괴물·귀신 게임 기획 [2026.10.06]</a></li>
            <li>전승 요약·해설 연결: <a href="/posts/korean-folklore-research/">한국 괴물·귀신 326항목</a>. 각 기획의 괴물 이름을 누르면 항목별 문헌과 해설로 이어집니다.</li>
            <li>수집 도감: <a href="/posts/classic-games/">tooli</a> · <a href="/posts/jjang-games/">짱게임</a> · <a href="/posts/playretrogames/">Play Retro Games</a> · <a href="/posts/playretro-io/">PlayRetro.io</a> · <a href="/posts/retrogames-onl-snes/">RetroGames.onl</a>. 기획별 참고와 수집 원문을 함께 표시했습니다.</li>
            <li>논리 퍼즐 규칙: <a href="/posts/logic-puzzles/">온라인 논리 퍼즐 41종</a>의 브릿지·슬리더 링크·노노그램·시카쿠와 항목별 공식 규칙 링크.</li>
            <li>포획 후 터뜨리기 규칙: <a href="https://www.nintendo.com/en-gb/Games/NES/Bubble-Bobble--276555.html">Nintendo — Bubble Bobble</a> · <a href="https://www.nintendo.co.jp/clv/manuals/en/pdf/CLV-P-NABKE_en.pdf">공식 설명서</a>.</li>
            <li>폭탄 설치 기본 구조: <a href="https://www.konami.com/games/asia/en/products/bomberman_r/">KONAMI — Super Bomberman R</a> · <a href="https://dds.konami.com/games/manual/pcemini/en_Bomber93.pdf">Bomberman ’93 공식 설명서</a>.</li>
            <li>같은 색 네 개 연결: <a href="https://www.nintendo.com/es-es/Juegos/Juegos-de-Nintendo-Switch/Puyo-Puyo-Tetris--1177193.html">Nintendo — Puyo Puyo Tetris</a>. 고정 표적과 두 조각 패: <a href="https://www.nintendo.co.jp/clv/manuals/en/pdf/CLV-P-NAAXE_en.pdf">Dr. Mario 공식 설명서</a>.</li>
            <li>블록 밀기 기본 구조: <a href="https://arcarc.xmission.com/PDF_Arcade_Manuals_and_Schematics/Pengo_Owners_Manual_%28420-0811%29.pdf">SEGA — Pengo 원본 운영 설명서 보관본</a>.</li>
          </ul>
          <p class="table-note">레퍼런스 규칙은 2026.10.07에 수집 데이터와 공개 설명을 대조했습니다. 각 기획의 수치·승패·장비·추가 단서는 새로 제안한 설정입니다. 컨셉아트는 내장 ImageGen으로 기획별로 생성했습니다.</p>
        </section>
        <p class="post-back"><a href="/posts/korean-folklore-game-design/">← 앞선 게임 기획</a> · <a href="/">전체 글 목록</a></p>
      </article>
    </main>
    <footer lang="en" class="site-footer">Small things, made and remade. <a href="https://github.com/nyimpe/nyimpe.github.io">Source code</a></footer>
  </body>
</html>
''')
dest = ROOT / f'posts/{SLUG}/index.html'
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text('\n'.join(parts))
(DOCS / 'reference-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2)+'\n')
print(f'Rendered {len(CONCEPTS)} concepts, {len(ASSETS)} figures: {dest}')
