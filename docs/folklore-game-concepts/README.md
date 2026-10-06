# 괴물·귀신 게임 컨셉 이미지

`/posts/korean-folklore-game-design/`의 컨셉 플레이 화면 열세 장을 만드는 스크립트입니다. 320×180 캔버스에 픽셀을 직접 찍고, 한글 UI는 2배 층에 비트맵 글꼴로 쓴 뒤 1280×720으로 정수배 확대합니다.

- `pix.py`: 팔레트, 도형·스프라이트·외곽선, 밤 조명, 텍스트 층과 내보내기
- `scene_*.py`: 장면별 그리기 (`deck` 덱빌더, `heaven` 불릿 헤븐, `metroid` 메트로배니아, `survival` 생존 제작, `bossrush` 보스 러시, `shooter` 부머 슈터(레이캐스팅), `horror` 심리 호러, `tactics` 전술 RPG, `mercy` 탄막 RPG, `gate` 서류 심사, `words` 규칙 퍼즐, `loop` 루프 RPG, `yut` 점수 로그라이크)

Python 3와 Pillow, macOS의 AppleGothic 글꼴이 필요합니다. 이 폴더에서 실행하면 PNG가 같은 폴더에 생깁니다.

```sh
python3 scene_deck.py
```

결과물은 `public/images/folklore-game/`에 복사해 사용합니다.
