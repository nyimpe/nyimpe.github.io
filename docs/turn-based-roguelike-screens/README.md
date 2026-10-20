# 묘수 화면 시안

`/posts/turn-based-roguelike-overview/`(턴제 로그라이크 기획 — 묘수)에 실린 화면 시안 세 장의 출처와 다시 만드는 법이다.
지금 게시된 그림은 Pillow로 직접 찍은 픽셀 목업이다. 다음 판은 myosu 게임 저장소에서 만든 스프라이트와 배경을 같은 스크립트에 넣어 다시 짠다.
화면 속 숫자와 배치는 기획 글의 규칙을 보여 주기 위한 예시이며, 실제 게임 화면이 아니다.

| 화면 | 스크립트 | 게시 이미지 | 글에서 쓰는 곳 |
| --- | --- | --- | --- |
| 재주 고르기 | `pickscreen.py` | `public/images/turn-based-roguelike-screens/01-pick-skill.webp` | `#skills` 절의 첫 그림 |
| 강 동네 지도 | `mapscreen.py` | `public/images/turn-based-roguelike-screens/02-river-map.webp` | `#run` 절의 “지도와 칸” |
| 강 우두머리전 | `battle.py` | `public/images/turn-based-roguelike-screens/03-river-leader.webp` | 글 맨 위 그림, `og:image`. `#turn-order`와 “강 우두머리전 예시”가 이 그림을 가리킨다 |

## Pillow 목업 다시 만들기

320×180 캔버스에 픽셀을 그린 뒤 4배로 키우고, 글자만 최종 해상도(1280×720)에서 Apple SD Gothic Neo로 얹는다.
지금 판의 나비는 `public/cat.png`를 줄여 팔레트에 맞춘 것이다.

```sh
cd docs/turn-based-roguelike-screens
python3 battle.py /tmp/battle.png
python3 mapscreen.py /tmp/map.png
python3 pickscreen.py /tmp/pick.png
```

PNG를 손실 없는 WebP로 저장해 게시 이미지를 바꾼다. 픽셀 경계가 뭉개지지 않도록 `npm run optimize:images`의 손실 압축은 거치지 않는다.
macOS의 `/System/Library/Fonts/AppleSDGothicNeo.ttc`와 Pillow 11 이상이 필요하다.

## myosu 에셋으로 다시 짜기

### 지난 시도

2026-10-20에 Codex 내장 이미지 생성으로 화면 세 장을 통째로 그려 보았다.
결과가 세밀한 일러스트풍이라, 작은 스프라이트와 타일 배경으로 된 게임 시안(`myosu/concept/nabi-pixellab/battle-mock.png`)과 어울리지 않았다.
지도는 네 번 모두 칸 수가 틀렸다. 그래서 쓰지 않았고 그 프롬프트도 지웠다. 원본은 gitignore된 `logs/turn-based-roguelike-screens/`에 남아 있다.

### 방법

화면 전체를 생성하지 않는다. 대신 myosu에서 만든 스프라이트와 배경을 지금 스크립트에 붙인다.
- 에셋 위치는 `~/Documents/dev/myosu/art/out/`이고, 만드는 법은 그 저장소의 `art/README.md`에 있다.
- 화면 구성, 순서 막대, 지도 칸 수, 한글 문구는 스크립트가 그대로 그리므로 틀어지지 않는다.
- 에셋은 마을, 강, 산 묶음이 먼저 있어야 한다. 재주 카드에 강의 용마와 산의 현구가 들어간다.

| 화면 | 배경 | 스프라이트 |
| --- | --- | --- |
| 01 재주 고르기 | `village-battle` (위쪽 마을 거리) | 김서방 `kimseobang` 대기 1. 카드 그림: `guigu-red`와 `guigu-black` 한 쌍, `yongma`, `hyeongu` |
| 02 강 동네 지도 | `river-map` | 우두머리 칸과 오른쪽 위 상자에 `river-fish`. 지금 칸 옆 표식은 `nabi` 머리. 가진 재주 아이콘은 `yongma` |
| 03 강 우두머리전 | `river-battle` | `nabi` 대기 1, `river-fish` 대기 1. 순서 막대 얼굴은 두 스프라이트의 머리를 잘라 쓴다 |

- 스프라이트는 원래 크기나 정수배로만 붙인다. 정수배가 아닌 확대나 부드러운 축소는 하지 않는다.
- 스프라이트 시트는 가로 띠이고, 프레임 순서는 대기 1, 대기 2, 공격, 맞음이다.
- 새 나비는 꼬리가 하나다. 세 화면의 “꼬리 3”을 “꼬리 1”로 바꾼다. “다시 뽑기 · 꼬리 4에서 열림”은 그대로 둔다.
- 지도 칸 그림(잡요괴, 이름난 요괴, 쉬는 칸, 상점, 사건, 보물)은 지금 스크립트의 것을 그대로 쓴다.

### Codex 요청

myosu 에셋이 생긴 뒤 이 저장소에서 Codex를 열고 아래를 붙여 넣는다.

```text
docs/turn-based-roguelike-screens/README.md를 읽고 "myosu 에셋으로 다시 짜기"를 해 줘.
battle.py, mapscreen.py, pickscreen.py가 손으로 그린 캐릭터와 배경 대신 ~/Documents/dev/myosu/art/out/의 스프라이트와 배경을 쓰게 고쳐.
README의 표대로 붙이고, 화면 구성, 순서 막대, 지도 칸 수, 한글 문구는 그대로 둬. "꼬리 3"만 "꼬리 1"로 바꿔.
결과 PNG는 logs/turn-based-roguelike-screens/에 01-pick-skill.png, 02-river-map.png, 03-river-leader.png로 저장하고 세 장을 보여 줘.
게시 이미지 교체와 커밋은 하지 마.
```

### 바꿔 끼우기

결과를 보고 괜찮으면 이어서 한다.

- PNG를 손실 없는 WebP로 저장해 표의 게시 이미지를 덮어쓴다. 크기가 1280×720 그대로라 글의 `src`, `width`, `height`, `og:image`는 고치지 않는다.
- `posts/turn-based-roguelike-overview/index.html`에서 세 그림의 `alt`와 `figcaption`을 새 그림에 맞게 고친다.
- 같은 글의 “강 우두머리전 예시” 절(나비 속도 12 → 느림 10, 돌진 쉬는 턴 2, 비 부르기 다음 물살 18, 막대 순서)이 03 그림과 맞는지 본다.
- 같은 글의 “만든 것과 남은 것” 절에서 화면 시안 설명을 바꾼다. 캐릭터와 배경은 AI로 만들어 픽셀로 다듬었고, 화면은 코드로 짰다는 내용이다.
- 이 README의 맨 위 설명을 고친다.
- `npm run build`가 되는지, 글에서 세 그림이 제대로 뜨는지 확인한다.
