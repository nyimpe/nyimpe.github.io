# 짱게임 2D·오락실 게임 도감

수집일: 2026-10-06 (Asia/Seoul). 원문: https://www.jjanggame.co.kr/.
페이지: https://nyimpe.github.io/posts/jjang-games/.

2D 게임(`gtype=2d`)과 고전 오락실게임(`gtype=old`)만 수집한다. 홈페이지 인기 목록과 다른 카테고리의 링크는 수집 범위에 포함하지 않는다. 홈페이지 요약은 각각 2,161개·1,506개지만, 실제 목록에서 확인한 게임은 **2,145개·1,412개, 총 3,557개**다. 2D 43페이지와 오락실 29페이지를 모두 읽고 각 다음 페이지가 비어 있는지 확인했다. 모든 목록 ID는 중복 없이 보존하며, 지역판·버전별 원문 항목도 합치지 않는다.

플랫폼 버튼은 원문의 두 카테고리 구분이다. 실제 하드웨어 플랫폼을 추정하지 않는다. 장르는 상세 페이지의 분류를 그대로 보존한다. 2D의 원문 장르가 비어 있는 397개는 ‘미분류’로 표시한다. 원문 메뉴의 장르별 검색 결과 수와 상세 페이지에서 집계한 장르별 게임 수를 대조했다.

| 원문 장르 | 2D 게임 | 오락실 게임 |
| --- | ---: | ---: |
| 액션 | 179 | 0 |
| 격투 | 0 | 157 |
| 슈팅 | 142 | 472 |
| 레이싱 | 92 | 72 |
| 스포츠 | 395 | 176 |
| 퍼즐 | 176 | 119 |
| 어드벤쳐 | 470 | 0 |
| 롤플레잉 | 294 | 0 |
| 퀴즈 | 0 | 48 |
| 미로 | 0 | 167 |
| 아케이드 | 0 | 201 |
| 미분류 | 397 | 0 |

게임명은 목록과 상세 화면의 잘린 제목 대신 상세 페이지의 문서 제목에서 전체 이름을 사용한다. 공개된 원문 영문 표기도 함께 보존해 검색할 수 있다. 소개는 장르가 일치하는 게임 시리즈의 짧은 편집 요약이 있는 120개에만 표시한다. 카테고리·장르만 되풀이하던 3,437개의 자동 안내 문장은 제거하고, 해당 설명과 근거는 빈 값으로 저장한다. ‘기본 진행’은 장르별 안내이며, 개별 조작키라고 표시하지 않는다. 원문에 게임별 텍스트 설명이 제공되지 않아 원문 링크를 함께 안내한다. 댓글·회원 정보는 게임 JSON과 포스트에 포함하지 않는다.

화면을 외부 자료의 실제 플레이·진행 장면 **3,525개**로 교체했다. 기존 누락 1,069개 중 **1,048개를 보충**하고, 기존 이미지 중 **2,477개를 교체**했다. 나머지 11개의 원문 이미지는 외부 플레이 화면을 확정하지 못해 제거했다. 현재 화면 누락은 **32개**이며 목록과 사유를 보존한다. 모든 오락실 항목 1,412개에는 화면이 있다.

주요 자료는 [Libretro thumbnails](https://github.com/libretro-thumbnails/libretro-thumbnails)의 `Named_Snaps`(게임 진행 화면)이다. 표지 폴더 `Named_Boxarts`와 타이틀 폴더 `Named_Titles`는 제외한다. SNES·Satellaview·Sufami Turbo와 MAME·FBNeo의 영문명을 원문 한글명·영문 별칭과 대조했다. 같은 게임의 지역판·개정판 대표 화면을 사용하는 경우 카드에서 차이를 표시한다. 합본·데모 4개는 원문에 명시된 개별 게임의 일반판 대표 장면임을 따로 표시한다. 개조판은 원작으로 대체하지 않는다.

Vizzed의 목록·상세 페이지에서 실제로 공개된 주소와 이용자가 올린 플레이 화면을 확인했다. 캐릭터·코스 선택 화면과 타이틀 화면은 시각 검토 후 제외하거나 실제 대전·주행 장면으로 교체한다. `robots.txt`의 5초 간격을 준수한다. LaunchBox는 `Screenshot - Gameplay` 분류, Emuparadise는 `Game Snap` 분류를 사용하며, OpenRetro와 Kotaku 갤러리도 실제 경기 장면을 확인했다. 원본 비율을 유지한 WebP를 최대 640×480으로 저장한다. 외부 서버에 의존하는 핫링크 대신 로컬 이미지를 사용한다. 이미지 주소에 저장 파일 해시를 포함해 이전 브라우저 캐시와 구분한다.

`docs/jjang-gameplay-images.json`은 항목별 이미지 주소·출처 페이지·대응 영문명·선정 근거·대표판 여부·원본 SHA-256·저장 이미지 SHA-256을 기록한다. Libretro 파일은 Git blob 해시도 검증한다. 남은 32개는 희귀 개조판·잘린 이름·자료집/영상 데모이거나 외부 자료에 타이틀/선택/방송 대기 화면만 남은 항목이다. 공개 검색으로 게임·판본과 플레이 화면을 확정하지 못한 경우 다른 게임 화면을 임의로 넣지 않는다. 상세 목록과 사유는 같은 JSON의 `unresolved`와 수집 보고서에 남긴다. 게임 파일·플레이어·에뮬레이터는 수집·배포하지 않는다.

기존 `src/classic-games.js`와 `src/classic-games.css`를 그대로 사용한다. 처음 24개를 표시하고 목록 끝에 가까워지면 다음 24개를 추가한다. 이미지도 브라우저의 지연 로딩을 사용한다. 카테고리·장르·검색 변경 시 새 결과의 첫 묶음부터 표시한다. JavaScript 또는 IntersectionObserver가 없으면 전체 게임 목록을 제공한다.

## 파일

- `public/data/jjang-games.json`: 게임명·원문 장르·짧은 소개·기본 진행·화면·출처.
- `public/images/jjang-games/*.webp`: 게임별 외부 플레이 화면.
- `posts/jjang-games/index.html`: 새 포스트.
- `docs/jjang-crawl-report.json`: 목록 페이지별 수, 홈페이지 요약과의 차이, 장르 대조, 이미지 실패 기록.
- `scripts/crawl-jjang.py`: 3개 동시 요청, 응답 간격·재시도, 외부 캐시를 사용하는 수집기.
- `docs/jjang-gameplay-images.json`: 검토된 외부 화면과 출처·해시·미해결 항목.
- `scripts/update-jjang-gameplay.py`: 출처 해시 검증, WebP 변환과 저장.
- `scripts/build-jjang-catalog.py`: JSON·보고서·HTML 생성.
- `scripts/verify-jjang-catalog.py`: 원문 ID·제목·장르의 보존과 모든 이미지 디코딩 검증.
- `scripts/verify-classic-games.cjs`, `scripts/verify-classic-assets.cjs`: 기존 도감과 새 도감을 검증하는 공통 도구. 인자 없이 실행하면 기존 Tooli 도감을 검증한다.

## 재수집과 검증

Python 3.9 이상, Node 22, Chrome이 필요하다. 같은 Python 의존성을 사용하는 Tooli 수집기의 requirements를 재사용한다. Playwright는 별도 환경에서 제공한다.

```sh
python3 -m venv /tmp/tooli-crawl-venv
/tmp/tooli-crawl-venv/bin/pip install -r scripts/tooli-requirements.txt
/tmp/tooli-crawl-venv/bin/python scripts/crawl-jjang.py collect
/tmp/tooli-crawl-venv/bin/python scripts/update-jjang-gameplay.py
/tmp/tooli-crawl-venv/bin/python scripts/build-jjang-catalog.py
/tmp/tooli-crawl-venv/bin/python scripts/verify-jjang-catalog.py
npm run build
npm run preview
NODE_PATH=/path/to/playwright/node_modules node scripts/verify-classic-games.cjs http://127.0.0.1:8080 jjang
NODE_PATH=/path/to/playwright/node_modules node scripts/verify-classic-games.cjs https://nyimpe.github.io jjang
node scripts/verify-classic-assets.cjs https://nyimpe.github.io jjang
```

`/tmp/nyimpe-jjang-cache`에 원문 응답과 단계별 수집 결과를 보관한다. 캐시를 유지하면 중단 후 이어서 수집한다. 외부 화면 원본 캐시는 `/tmp/nyimpe-jjang-gameplay-cache`에 보관한다. 최신 원문을 다시 수집하려면 원문 캐시를 별도로 비우고, 변경된 ID가 있으면 외부 화면 대응표도 먼저 검토한다. 원본 이미지 주소의 내용이 바뀌면 해시 검증이 실패하므로 대응표를 확인해야 한다. 홈페이지 요약, 실제 목록과 장르는 원문의 현재 상태에 따라 변할 수 있다.

로컬 브라우저 검증은 카테고리·장르 39개 조합, 3,557개 전체 스크롤 표시, 마지막 묶음, 검색·빈 결과·초기화·저장 URL·키보드 조작, 1280·375·320px, 밝은·어두운 테마, 콘솔, JavaScript 없는 목록을 포함한다. 배포 검증은 HTML, JSON, 해시된 JS/CSS, 모든 화면의 응답을 로컬 빌드와 SHA-256으로 대조한다. Playwright 입력은 브라우저 자동화이며 물리 입력 검증은 아니다.

공개 서버 검증은 브라우저와 파일 대조를 순차 실행한다. 로컬에서 전체 필터·스크롤을 검증하고, 공개 브라우저에서는 24→48 지연 표시, 카테고리·장르·검색·키보드, 1280·375·320px의 두 테마, 출처 링크와 대표 외부 화면 9개를 확인한다. 공개 전체 스크롤 도구를 추가 실행할 때에는 간격을 두며, 파일 대조는 동시 요청 2개·요청 후 250ms 간격을 사용한다. HTTP 429가 오면 최소 30초부터 간격을 늘리며 서버의 Retry-After 값도 반영한다. 일시적인 502·503·504도 간격을 두고 최대 5번 시도하며, 실패하면 해당 URL과 함께 검증을 중단한다.
