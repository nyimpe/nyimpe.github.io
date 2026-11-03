# tooli의 고전게임 정리

수집일: 2026-10-06 (Asia/Seoul). 출처: https://www.tooli.co.kr/ 고전게임 메뉴.
페이지: https://nyimpe.github.io/posts/classic-games/

7개 게시판의 모든 목록 페이지와 공개 게시물 본문을 확인했다. 목록에서 수집한 고유 게시물 865개 중 공지·실행기·기기 소개 20개를 제외해 게임 845개를 정리했다. 원문 게시판의 글 수는 공지 포함 방식이 달라서 게시판 글 수, 실제 고유 목록 수, 공지 수를 각각 기록했다.

| 플랫폼 게시판 | 게임 |
| --- | ---: |
| PC | 424 |
| 오락실 | 193 |
| 게임보이 | 13 |
| 슈퍼패미콤 | 15 |
| 메가드라이브 | 40 |
| MSX | 34 |
| 플래시 | 126 |

플랫폼은 Tooli 게시판 기준이다. 게임보이에는 GBA가 포함되며, PC의 ‘팩/오락기’ 분류도 원래 게시판 위치를 보존했다. PC의 원문 장르를 11개 공통 장르로 통합하고 다른 게시판은 편집 분류했다. 제목·원문 분류·출처 URL은 JSON에 함께 보존했다. 본문은 짧게 발췌하거나 게임 시리즈별로 요약했으며, 정보가 부족한 글에는 게시판·장르 안내를 사용했다. 장르별 기본 진행과 원문에서 확인한 조작법 145건을 구분해 표시한다.

화면 830개: 원문 스크린샷 715개, 플래시 시작·도입 화면 캡처 115개. WebP로 저장하고 원본 비율을 유지한다. 최대 720×540, 캡처는 700×500이다. 원문 이미지가 없는 글, 비공개 글, 없어진 외부 파일, Shockwave 형식 및 캡처되지 않는 게임 등 15개는 목록에서 제외하지 않고 사유와 원문 링크를 표시한다. 상세 목록과 캡처 실패 원인은 `tooli-crawl-report.json`에 있다. 검은 화면과 오류 화면을 게임 이미지로 저장하지 않는다.

`robots.txt`를 확인해 공개 목록·상세 페이지·이미지만 수집했다. 비공개 본문에 접근하지 않았다. 게임 파일과 SWF, 런타임은 배포하지 않는다. 이미지와 설명의 출처는 각 게임의 Tooli 원문 링크이며, JSON에는 이미지 출처도 기록했다.

목록은 처음 24개를 표시하고 끝에 가까워지면 다음 24개를 자동으로 추가한다. 이미지는 브라우저의 지연 로딩을 유지한다. 필터·검색 변경 시 해당 결과의 처음부터 다시 표시하며, JavaScript 또는 IntersectionObserver를 사용할 수 없으면 전체 목록을 제공한다.

## 파일

- `public/data/tooli-games.json`: 배포하는 게임 정보와 출처.
- `public/images/classic-games/*.webp`: 배포하는 화면.
- `docs/tooli-crawl-report.json`: 수집 범위, 제외 항목, 누락 화면, 실패 원인.
- `docs/tooli-genre-overrides.json`: 게시물 ID별 편집 장르.
- `scripts/crawl-tooli.py`: 목록·본문·이미지 수집. 3개 동시 요청, 응답 후 간격과 재시도, `/tmp/nyimpe-tooli-cache` 캐시.
- `scripts/capture-tooli-flash.cjs`: 임시 Ruffle 환경에서 화면 캡처. 바깥 네트워크와 ActionScript의 스크립트 접근을 차단하며, 런타임은 사이트에 포함하지 않는다. 게임 시작 화면을 기다리기 위해 캡처용 프레임 속도를 조정한다.
- `scripts/build-tooli-catalog.py`: 저장 데이터와 HTML 생성.
- `src/classic-games.js`, `src/classic-games.css`: 필터·검색·스크롤 지연 표시·화면.
- `scripts/verify-classic-games.cjs`: 실제 브라우저로 필터와 표시 검증.

## 재수집

Python 3.9 이상과 Node 22, Chrome이 필요하다. 도구 의존성은 별도 임시 환경에 설치한다.

```sh
python3 -m venv /tmp/tooli-crawl-venv
/tmp/tooli-crawl-venv/bin/pip install -r scripts/tooli-requirements.txt
/tmp/tooli-crawl-venv/bin/python scripts/crawl-tooli.py collect
/tmp/tooli-crawl-venv/bin/python scripts/crawl-tooli.py images
npm install --prefix /tmp/tooli-capture-deps playwright sharp @ruffle-rs/ruffle
NODE_PATH=/tmp/tooli-capture-deps/node_modules node scripts/capture-tooli-flash.cjs
/tmp/tooli-crawl-venv/bin/python scripts/build-tooli-catalog.py
npm run build
```

캐시를 유지하면 이미 수집한 HTML과 미디어를 다시 요청하지 않는다. 새 원문을 수집하려면 해당 캐시를 별도로 비운다. 특정 플래시 화면만 새로 찍으려면 캡처 명령 뒤에 `flash-472129`처럼 게시물 ID를 전달한다. 수집 결과는 원문의 현재 상태에 따라 달라질 수 있다.

## 검증

```sh
npm run preview
NODE_PATH=/tmp/tooli-capture-deps/node_modules node scripts/verify-classic-games.cjs http://127.0.0.1:8080
NODE_PATH=/tmp/tooli-capture-deps/node_modules node scripts/verify-classic-games.cjs https://nyimpe.github.io
node scripts/verify-classic-assets.cjs https://nyimpe.github.io
```

플랫폼·장르 조합 96개, 한국어·영어 검색, 결과 없음, 초기화, 스크롤 추가 표시와 마지막 결과, 저장 URL, 키보드 입력, 1280·375·320px 폭, 밝은·어두운 테마, 콘솔, JavaScript 없는 전체 목록, 홈페이지 진입 링크를 확인한다. 브라우저 키보드 입력은 Playwright 자동화이며 물리 입력 테스트는 아니다. 배포 후에는 새 HTML과 해시 자산이 실제로 제공되는지 확인하고, JSON 및 모든 이미지의 배포 응답도 대조한다.
