# 귀로 시제품 그림 작업

`/posts/way-back-extraction/`(귀로 — 격자 이동 하드코어 탈출 로그라이크 기획)의 첫 시제품에 필요한 스프라이트·타일·아이콘을 Codex 내장 이미지 생성(`image_gen`)으로 만들고, 게임에 쓸 작은 픽셀 그림으로 다듬는 곳이다.
절차는 묘수 저장소의 `~/Documents/dev/myosu/art/README.md`와 같고, 격자 게임에 맞게 시트 구성만 다르다.
범위는 기획 글 11장의 **첫 시제품**까지다. 두 번째 지역, 유일 장비, 옷 외형, 야간 변형은 만들지 않는다.

## 지난 교훈

묘수에서 화면 전체를 생성했을 때는 일러스트풍이 되고 칸 수가 틀렸다. 그래서 여기서는 **화면을 생성하지 않는다.** 캐릭터 시트, 타일 시트, 아이콘 시트처럼 칸이 정해진 그림만 만들고, 화면은 코드가 조립한다.

## 스타일 기준

- **시점:** 탑다운 3/4. 타일 32×32, 캐릭터 32×48(한 칸을 차지하고 위로 솟음). 화면 640×360, 정수 배 확대.
- **분위기:** 어둡고 긴장되지만 공포물이 아니다. 피는 작게, 상처·내장·비명은 없다. 밖은 잿빛 기와와 푸른 그림자, 지하는 거의 검정에 횃불 주황, 야영지는 모닥불 주황.
- **선과 명암:** 1px 짙은 외곽선, 색마다 2~3단 평면 명암, 빛은 왼쪽 위. 그라데이션, 디더링, 반투명, 안티에일리어싱, 글자는 쓰지 않는다.
- **색 수:** 스프라이트 16색 이하, 타일 시트 32색 이하, 아이콘 12색 이하.
- **개와 고양이:** 두 발로 서는 2.5등신. 개는 늘어진 귀와 주둥이, 고양이는 뾰족한 귀와 긴 꼬리. 1배에서 실루엣으로 구별된다. 플레이어 시트는 무기를 들지 않고(코드가 무기 그림을 손 위에 얹는다), 적 시트는 무기를 든다.
- **기준 그림:** 없다. `player-dog`를 먼저 만들어 통과시키고, 그 미리보기(`out/preview/player-dog@4x.png`)를 뒤의 모든 항목에 참조로 넣는다. 팔레트도 이 그림에서 모은다.

## 시트 구성

| type | 그림 크기 | 칸 | 한 칸 | 쓰는 곳 |
| --- | --- | --- | --- | --- |
| `character` | 1024×1536 | 3행×4열 | 32×48 ×8 | 플레이어 2, 떠돌이 패 2, 탁탁귀병. 행: 아래·오른쪽·위 / 열: 대기·걷기 A·걷기 B·공격 |
| `creature` | 1024×1024 | 4행×4열 | 32×32 ×8 | 수류견. 4행은 맞음·쓰러짐·빈 칸·빈 칸 |
| `sheet2x2` | 1024×1024 또는 1024×1536 | 2×2 | 항목의 `frame` × `scale` | 보스, 어둑서니, 생사귀, 도깨비, NPC 3, 효과 |
| `tiles` | 1024×1024 | 4×4 | 32×32 ×8 | 타일 4묶음, 소품(마젠타 배경) |
| `objects` | 1024×1536 | 2열×3행 | 64×64 ×8 | 탈출구 5 + 성문 |
| `icons` | 1024×1024 | 4×4 | 16×16 ×16 | 아이템 2묶음, UI |

왼쪽을 보는 프레임은 만들지 않고 오른쪽 프레임을 코드에서 뒤집는다. 맞음은 코드의 색 번쩍임으로, 죽음은 소품 시트의 쓰러진 수색꾼으로 대신한다.

## 폴더

```text
docs/way-back-extraction/art/
  README.md        이 문서
  prompts.json     항목 26개. group: player, enemy, camp, tiles, props, items, ui. priority 1~3
  tools/           pixelize.py (처음 작업할 때 myosu의 것을 복사해 고친다)
  ref/             palette.png (player-dog에서 모은 팔레트)
  out/
    <group>/       <id>.png  투명 배경(타일은 불투명), 원래 크기, 시트 그대로
    preview/       <id>@4x.png, contact-<group>.png
  log.json         생성 기록
logs/way-back-extraction/art/raw/<group>/<id>.png   image_gen 원본 (gitignore)
```

시제품을 어디에 만들지(브라우저 또는 Godot) 정해지면 `out/`을 그 저장소로 옮긴다. 이 폴더는 원본 기록이다.

## 만드는 법

### 1. 생성

`prompts.json`의 항목마다 `common`, 빈 줄, `style[type]`(`{frame}`과 `{scale}`을 그 항목의 값으로 바꾼 것), 빈 줄, `prompt`를 이어 붙여 `image_gen`에 넘긴다.
그림 크기는 항목의 `image`를 쓴다. `refs`의 그림을 참조 이미지로 함께 넘기고, 도구가 참조 이미지를 받지 못하면 먼저 그 그림들을 직접 열어 보고 스타일을 맞춘다.
원본은 `rawPath`에 PNG로 그대로 저장한다.

순서는 `priority`대로 한다.
- **1:** player-dog → player-cat → tiles-alley → props → extracts → items-gear → items-loot → ui-icons → suryugyeon → gwibong-mimic → taktak-soldier. 이것만 있으면 기획의 B·C 단계(전투, 원정)를 돌릴 수 있다.
- **2:** 떠돌이 패 2, 어둑서니 2, 생사귀, NPC 3, tiles-camp, tiles-market, tiles-cellar. D 단계(야영지)와 세 구역.
- **3:** 두억시니, 도깨비불, 도깨비 장수, 효과. E 단계.

### 2. 다듬기 (`tools/pixelize.py`)

처음 작업할 때 `~/Documents/dev/myosu/art/tools/pixelize.py`를 복사해 아래처럼 고친다. 묘수 것은 2×2 시트에서 캐릭터 영역을 찾아 배율을 맞추지만, 여기서는 **칸과 배율이 고정**이라 더 단순하다.

```sh
python3 tools/pixelize.py sprite  <raw> <out> --grid 3x4 --frame 32x48 --scale 8
python3 tools/pixelize.py tiles   <raw> <out> --grid 4x4 --frame 32x32 --scale 8
python3 tools/pixelize.py icons   <raw> <out> --grid 4x4 --frame 16x16 --scale 16
python3 tools/pixelize.py palette <sprite...>     # ref/palette.png를 만든다
python3 tools/pixelize.py contact <group>         # out/preview/contact-<group>.png
```

공통:
1. 그림을 `--grid`대로 같은 크기 칸으로 자른다. 칸마다 `--scale`×`--scale` 블록 단위로 줄인다. 블록 경계가 어긋나 있으면(생성기가 정확히 8배로 그리지 않는다) 블록 크기와 위치를 먼저 추정하고, 블록마다 가운데 색을 쓴다. 추정이 안 되면 최빈값으로 줄인다. 이중선형·바이큐빅 축소는 쓰지 않는다.
2. `ref/palette.png`의 가장 가까운 색으로 맞춘다. 팔레트는 통과한 `player-dog`에서 모으고, 항목마다 2~3색까지 더할 수 있다(어둑서니의 노란 눈, 도깨비불의 청록).
3. 디더링 없이 색 수를 줄인다. 외톨이 1픽셀 잡티는 둘레 색으로 정리한다.

스프라이트(`sprite`, `sheet2x2`, `creature`, `objects`, 소품):
4. 마젠타(#FF00FF 근처)를 투명으로 바꾸고 가장자리의 분홍 찌꺼기를 지운다.
5. 끊긴 외곽선을 1px 짙은 색으로 메운다.
6. 칸마다 발 높이를 찾아 맨 아랫줄에서 1px 위로 맞추고, 가로는 가운데로 맞춘다. 같은 시트의 발 높이가 모두 같아야 한다.
7. 칸 배치를 그대로 둔 시트로 저장한다(3행×4열이면 128×144).

타일(`tiles`):
4. 마젠타 처리와 발 맞춤을 하지 않는다. 16칸을 4×4 그대로 128×128로 저장한다.
5. 바닥 타일(1~3번)은 자기 자신과 이어 붙여 이음새를 본다.

아이콘(`icons`):
4. 마젠타를 투명으로 바꾸고 16×16 안에서 가운데로 맞춘다. 64×64로 저장한다.

### 3. 확인

group마다 `out/preview/contact-<group>.png`를 만든다. 스프라이트는 player-dog 옆에 1배와 4배로, 타일은 4×4를 2배로, 아이콘은 4배로 놓는다. 타일 위에 player-dog 한 칸을 세워 크기를 본다.

- 1배에서 무엇인지 알아볼 수 있다. 외곽선이 끊기지 않았고 분홍 찌꺼기가 없다.
- 시트의 모든 칸이 같은 캐릭터, 같은 크기, 같은 발 높이다. 아래·오른쪽·위 행이 같은 인물로 보인다.
- 개는 귀가 늘어지고 주둥이가 있다. 고양이는 귀가 뾰족하고 꼬리가 보인다. 플레이어 시트에 무기가 없다. 적 시트에는 무기가 있다.
- 탁탁귀병과 생사귀는 얼굴이 모자에 가려 있다. 두억시니·어둑서니에 상처나 피가 없다.
- 타일: 바닥이 이어 붙여도 이음새가 안 보인다. 벽 top과 front가 위아래로 맞는다. 문 세 종류(닫힘·열림·잠김)가 한눈에 구별된다. 글자가 없다.
- 아이콘: 16×16에서 열여섯 개가 서로 구별된다. 단검·투척 단검, 창고 열쇠·지하문 열쇠, 작은 배낭·큰 배낭이 특히.
- 소품의 쓰러진 수색꾼에 핏자국이 없다.

어긋나면 같은 프롬프트로 다시 만든다. 한 항목이 세 번 넘게 어긋나면 그 항목은 멈추고 이유를 기록한다. 다듬기만 문제면 `pixelize.py`를 고쳐 원본에서 다시 다듬는다.
캐릭터가 거듭 2.5등신 개·고양이로 나오지 않으면 PixelLab에 같은 설명과 통과한 player-dog를 스타일 그림으로 넣는 편이 낫다.

### 4. 기록

`log.json`에 항목마다 날짜, 도구, 그림 크기, 시도 횟수, 고른 시도, 원본과 결과의 SHA-256, 확인 결과(통과 또는 실패)와 한 줄 메모를 적는다.

## Codex 요청

이 저장소(`~/Documents/dev/nyimpe.github.io`)에서 Codex를 열고 아래를 붙여 넣는다. 처음에는 priority 1만 만들고, 결과를 보고 나서 2, 3으로 넘어간다.

```text
docs/way-back-extraction/art/README.md를 읽고 그대로 해 줘.
1) ~/Documents/dev/myosu/art/tools/pixelize.py를 docs/way-back-extraction/art/tools/pixelize.py로 복사해 README의 "2. 다듬기"대로 고쳐. 칸과 배율은 고정이고, sprite·tiles·icons·palette·contact 명령이 있어야 해.
2) docs/way-back-extraction/art/prompts.json에서 priority가 1인 항목을 README의 "1. 생성" 순서대로 만들어.
   common, style[type], prompt를 이어 붙여 내장 image_gen에 넘기고, refs 그림을 참조로 함께 넘겨. 프롬프트는 고치지 마.
   player-dog가 통과하면 그 미리보기로 ref/palette.png를 만들고 나서 다음 항목으로 가.
   원본은 rawPath에, 다듬은 결과는 outPath에 저장해.
3) group마다 out/preview/contact-<group>.png를 만들고 README의 "3. 확인" 목록으로 직접 봐.
   어긋난 항목은 같은 프롬프트로 다시 만들고, 세 번 넘게 어긋나면 그 항목은 멈춰.
4) log.json에 기록하고, 항목별 결과를 표로 알려 줘.
posts/, src/, public/은 건드리지 말고, 커밋하지 마.
```

다음은 `priority가 1인`을 `2인`, `3인`으로 바꿔 같은 요청을 한다. 1)의 도구 만들기는 이미 있으면 건너뛴다.
