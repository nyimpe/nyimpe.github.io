# 괴물·귀신 게임 컨셉 이미지

현재 게시물 이미지는 `redraw-2026-10-06/`에 기록한 내장 ImageGen 프롬프트로 새로 제작한 플레이 컨셉아트입니다. 생성 원본은 PNG이며, 게시용 이미지는 `public/images/folklore-game/`의 같은 이름을 가진 WebP 또는 AVIF로 압축합니다. 현재 경로·크기·해시는 `redraw-2026-10-06/manifest.json`, 압축 전 정보는 각 항목의 `optimizedFrom`에 기록합니다. 장르별 시점·핵심 조작·괴물 대응 규칙을 시각화한 시안이며, 실행 가능한 게임의 캡처가 아닙니다.

아래 Python 스크립트는 이전 임시 이미지의 제작 기록입니다. 실행 결과를 현재 게시물 이미지 위에 복사하면 새 컨셉아트가 덮어써지므로 별도 출력으로 보관합니다.

`/posts/korean-folklore-game-design/`의 컨셉 플레이 화면 마흔세 장을 만드는 스크립트입니다. 320×180 캔버스에 픽셀을 직접 찍고, 한글 UI는 2배 층에 비트맵 글꼴로 쓴 뒤 1280×720으로 정수배 확대합니다.

- `pix.py`: 팔레트, 도형·스프라이트·외곽선, 밤 조명, 텍스트 층과 내보내기
- `scene_*.py`: 장면별 그리기 (`deck` 덱빌더, `heaven` 불릿 헤븐, `metroid` 메트로배니아, `survival` 생존 제작, `bossrush` 보스 러시, `shooter` 부머 슈터(레이캐스팅), `horror` 심리 호러, `tactics` 전술 RPG, `mercy` 탄막 RPG, `gate` 서류 심사, `words` 규칙 퍼즐, `loop` 루프 RPG, `yut` 점수 로그라이크, `io_*` 실시간 io 다섯 가지, `indie_*` 2000~2010년대 인디·레트로 열 가지, `itch_*` itch.io 인기작 다섯 가지, `turn_*` 국내·해외 턴제 열 가지)
- `io_ui.py`: io 화면 공통 요소(순위표, 미니맵, 알림 태그)

Python 3와 Pillow, macOS의 AppleGothic 글꼴이 필요합니다. 이 폴더에서 실행하면 PNG가 같은 폴더에 생깁니다.

```sh
python3 scene_deck.py
```

위 스크립트의 결과는 과거 제작 기록으로만 보관합니다. 현재 ImageGen 컨셉아트의 게시용 압축에는 저장소 루트의 `npm run optimize:images`를 사용합니다.
