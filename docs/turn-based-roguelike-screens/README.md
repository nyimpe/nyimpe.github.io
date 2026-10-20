# 턴제 로그라이크 기획 5 — 플레이 화면 시안

`/posts/turn-based-roguelike-screens/`에 실린 세 장의 화면 시안을 만드는 스크립트다.
AI 이미지 생성이 아니라 Pillow로 320×180 캔버스에 픽셀을 직접 그린 뒤 4배로 키우고,
글자만 최종 해상도(1280×720)에서 Apple SD Gothic Neo로 얹었다.
주인공 나비는 `public/cat.png`를 줄여 팔레트에 맞춘 것이다.

| 스크립트 | 화면 | 게시 이미지 |
| --- | --- | --- |
| `pickscreen.py` | 마을 우두머리를 이긴 뒤 재주 고르기 | `public/images/turn-based-roguelike-screens/01-pick-skill.webp` |
| `mapscreen.py` | 강 동네 갈림길 지도 | `public/images/turn-based-roguelike-screens/02-river-map.webp` |
| `battle.py` | 강 우두머리와의 전투 | `public/images/turn-based-roguelike-screens/03-river-leader.webp` |

다시 만들 때는 이 폴더에서 실행해 PNG를 얻고, 손실 없는 WebP로 저장한다.
픽셀 경계가 뭉개지지 않도록 `npm run optimize:images`의 손실 압축은 거치지 않았다.

```sh
cd docs/turn-based-roguelike-screens
python3 battle.py /tmp/battle.png
python3 mapscreen.py /tmp/map.png
python3 pickscreen.py /tmp/pick.png
```

macOS의 `/System/Library/Fonts/AppleSDGothicNeo.ttc`와 Pillow 11 이상이 필요하다.
화면 속 숫자와 배치는 1~4편의 규칙을 보여 주기 위한 예시이며, 실제 구현된 게임 화면이 아니다.
