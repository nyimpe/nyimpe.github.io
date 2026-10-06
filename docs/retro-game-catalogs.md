# 세 사이트의 고전게임 목록

수집일: 2026-10-06 (Asia/Seoul).

| 포스팅 | 수집 범위 | 게임 | 이미지 |
| --- | --- | ---: | ---: |
| [Play Retro Games](https://nyimpe.github.io/posts/playretrogames/) | 전체 목록 241쪽 | 8,432 | 8,425 |
| [PlayRetro.io](https://nyimpe.github.io/posts/playretro-io/) | 전체 목록 35쪽 | 411 | 411 |
| [RetroGames.onl SNES](https://nyimpe.github.io/posts/retrogames-onl-snes/) | 요청한 SNES A–Z 목록 1쪽 | 473 | 473 |

출처는 각각 https://www.playretrogames.com/ , https://www.playretro.io/ , https://www.retrogames.onl/p/play-snes-games-online.html 이다. 마지막 사이트의 다른 기종 목록은 이번 수집 범위에 포함하지 않는다. SNES 목록은 링크 492개에서 동일 원문 URL로 연결되는 다른 표기 19개를 합쳤다. 다른 표기는 카드와 JSON에 남겨 검색할 수 있다. SNES 목록 제목과 상세 제목이 다르면 상세 제목을 사용하고 원래 목록 제목을 보존한다. Play Retro Games는 첫 페이지의 표시 수 8,432개와 모든 페이지에서 수집한 고유 게임 수를 대조한다. 인기/추천 사이드바는 목록으로 세지 않는다.

플랫폼은 원문 목록·상세 페이지 기준이다. PlayRetro.io는 브라우저 게임을 제공하므로 ‘웹 브라우저’로 분류한다. 게임의 원작 기종을 추측해 표시하지 않는다. 장르는 기존 Tooli 도감의 한국어 공통 장르를 사용하며, 원문 장르·진행 분류 통합과 일부 시리즈의 편집 분류를 구분한다. ‘RPG elements’, ‘Puzzle elements’ 같은 보조 요소만으로 장르를 바꾸지 않는다. 확인되지 않은 게임은 ‘기타/미분류’에 남긴다. 원문 장르와 분류 근거도 JSON에 보존한다.

각 게임은 제목, 원문 썸네일, 짧은 한글 소개, 장르별 기본 진행, 원문 링크를 갖는다. 원문 소개를 바탕으로 핵심 내용을 한글로 번역·정리한다. 초벌에서는 도입부의 완결 문장과 최대 70단어를 참고하고, 일부 항목은 원문 전체와 대조해 직접 정리했다. 광고성 수식어는 일부 덜어낸다. 페이지와 배포 JSON에는 영문 소개를 함께 넣지 않는다. 원문 소개가 없는 게임에는 한글 목록 안내를 사용한다. ‘기본 진행’은 장르별 설명이며 실제 키 배치·실행 검증을 의미하지 않는다. 원문 썸네일에는 표지와 게임 화면이 포함되어 있다. 이미지는 비율을 유지하고 최대 480×360 WebP로 저장한다. 이미지 접근 실패 시 게임을 제외하지 않고 사유와 원문 링크를 표시한다.

한글 설명은 `scripts/retro-descriptions-ko.json`에 원문 설명의 SHA-256과 함께 저장한다. 생성기는 이 파일을 사용하며 원문이 변경됐거나 한글 설명이 없으면 영문을 대신 출력하지 않고 해당 게임 ID와 함께 중단한다. 새 원문을 수집했을 때는 그 항목의 한글 설명과 원문 해시를 갱신해야 한다.

이번 수집은 모든 게임의 상세 페이지를 확인했다. Play Retro Games의 원문 이미지 7개는 HTTP 404로 남아 있다. 원문 플랫폼 링크가 잘못된 Red Robin은 목록·상세의 MAME 표기를 사용한다. 원문 소개의 이중 인코딩을 복원할 수 있으면 복원하고 HTML에서 허용하지 않는 제어 문자를 제거한다.

기존 도감의 `src/classic-games.js`와 `src/classic-games.css`를 그대로 사용한다. 플랫폼·장르·검색을 조합하고 URL로 결과를 저장한다. 처음 24개를 표시하고 스크롤하면 24개씩 추가한다. 필터 변경·초기화 시 표시 목록도 다시 시작한다. JavaScript 또는 IntersectionObserver가 없는 브라우저에는 전체 목록을 제공한다.

각 사이트의 `robots.txt`를 확인하고 공개 목록·상세 HTML과 썸네일만 수집했다. 일반 브라우저 User-Agent를 사용하고, 목록·이미지와 작은 사이트의 상세는 최대 3개 동시 요청, Play Retro Games 상세는 최대 6개 동시 요청을 사용한다. 도메인별 요청 간격, 응답 후 간격, 오류 재시도와 외부 임시 캐시를 적용한다. 429 응답은 대기 후 재시도하고 반복 제한이 생기면 새 요청을 중단한다. 게임 파일·ROM·플레이어·광고 스크립트를 수집하거나 사이트에 넣지 않는다.

## 파일과 재수집

- `scripts/crawl-retro-catalogs.py`: 목록·상세·이미지 수집과 정적 페이지 생성.
- `scripts/retro-catalog-template.html`: 기존 도감 양식의 HTML 틀.
- `scripts/retro-descriptions-ko.json`: 게임별 한글 설명과 원문 해시.
- `public/data/{playretrogames,playretro-io,retrogames-onl-snes}-games.json`: 배포하는 메타데이터와 출처.
- `public/images/retro-catalogs/<site>/*.webp`: 배포하는 썸네일.
- `docs/<site>-crawl-report.json`: 목록 범위·중복·분류 수·상세/이미지 실패·robots 원문.
- `scripts/verify-retro-catalogs.cjs`: 실제 Chrome을 통한 필터·검색·표시 검증.
- `scripts/verify-retro-assets.py`: 전체 카드와 이미지 무결성, 배포한 JSON·이미지 바이트 대조.
- `scripts/verify-retro-korean-descriptions.py`: 전체 설명의 한글 여부·HTML 일치와 변경 전 데이터 보존 대조.

Python 3.9 이상과 `scripts/tooli-requirements.txt`의 의존성을 사용한다. 브라우저 검증에는 Node 22, Playwright, Chrome이 필요하다.

```sh
python3 -m venv /tmp/retro-crawl-venv
/tmp/retro-crawl-venv/bin/pip install -r scripts/tooli-requirements.txt
/tmp/retro-crawl-venv/bin/python scripts/crawl-retro-catalogs.py all
npm run build
/tmp/retro-crawl-venv/bin/python scripts/verify-retro-korean-descriptions.py
/tmp/retro-crawl-venv/bin/python scripts/verify-retro-assets.py
npm run preview
NODE_PATH=/path/to/node_modules node scripts/verify-retro-catalogs.cjs http://127.0.0.1:8080
NODE_PATH=/path/to/node_modules node scripts/verify-retro-catalogs.cjs https://nyimpe.github.io
/tmp/retro-crawl-venv/bin/python scripts/verify-retro-assets.py https://nyimpe.github.io
# 배포 HTML·JSON·JS/CSS만 대조할 때
/tmp/retro-crawl-venv/bin/python scripts/verify-retro-assets.py https://nyimpe.github.io --core
```

수집은 `lists`, `details`, `images`, `build` 단계별로 다시 실행할 수 있다. `/tmp/nyimpe-retro-cache`를 유지하면 기존 응답을 재사용한다. 원문의 새 상태를 수집하려면 해당 임시 캐시와 다시 수집할 썸네일을 별도로 정리한다. 재수집 결과와 수는 원문의 변경에 따라 달라질 수 있다.

로컬 빌드와 카드 9,316개·이미지 9,309개 무결성 검증을 통과했다. 브라우저에서는 플랫폼·장르 364개 조합 전체, 결과 수와 실제 ID, 검색·결과 없음·초기화, 첫 추가 스크롤과 작은 분류의 마지막 항목, URL 복원, 브라우저 키보드 입력, 1280/375/320px에서 밝은/어두운 테마와 가로 넘침, 표시 이미지, JavaScript/IntersectionObserver 없는 전체 목록, 콘솔 오류, 홈페이지 진입 링크를 확인했다. 브라우저 입력은 자동화 검증이며 물리 키보드·마우스 입력 테스트는 아니다.

배포 브라우저 검증은 플랫폼 양 끝과 서로 다른 대표 장르를 조합하고 검색·스크롤·화면·이미지를 확인한다. 전체 조합과 JavaScript/IntersectionObserver 없는 대체 동작은 로컬에서 검사해 큰 HTML의 반복 다운로드와 공개 CDN의 요청 폭주를 피한다. 배포 파일 검증은 브라우저 검사 후 순차 실행하며 HTML·JSON·해시된 JS/CSS를 로컬 빌드와 SHA-256으로 대조한다. 옵션 없는 파일 검증은 이미지 전체도 대조하며 `--core`는 이미지 다운로드를 생략한다. 파일 요청은 동시 2개·응답 후 250ms 간격이며, 429·502·503·504는 서버 상태에 맞춰 간격을 늘려 최대 5번 재시도한다.

이번 배포의 Play Retro Games 이미지 1,000개는 저장본과 SHA-256이 일치했다. 이미지 전체 원격 대조는 CDN 요청 제한을 고려해 표본에서 중단했다. 전체 이미지 9,309개의 디코딩·크기·카드 연결 검증은 로컬에서 완료했다.

2026-10-07 한글 소개 수정에서는 9,316개 설명의 한글 여부와 HTML·JSON 일치, 변경 전 게임명·순서·플랫폼·장르·이미지·출처 보존을 대조했다. 로컬 브라우저에서 세 페이지의 한글 검색 결과 수와 ID, 초기화, 이미지, 375px 가로 넘침, 밝은/어두운 테마와 콘솔 오류를 확인했다. 한글 소개 누락 또는 원문 해시 불일치 시 생성기가 중단되고 배포 JSON을 변경하지 않는 것도 확인했다.
