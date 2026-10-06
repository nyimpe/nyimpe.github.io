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

게임명은 목록과 상세 화면의 잘린 제목 대신 상세 페이지의 문서 제목에서 전체 이름을 사용한다. 공개된 원문 영문 표기도 함께 보존해 검색할 수 있다. 소개는 장르가 일치하는 게임 시리즈의 짧은 편집 요약 또는 카테고리·장르 안내다. ‘기본 진행’은 장르별 안내이며, 개별 조작키라고 표시하지 않는다. 원문에 게임별 텍스트 설명이 제공되지 않아 원문 링크를 함께 안내한다. 댓글·회원 정보는 게임 JSON과 포스트에 포함하지 않는다.

실제 원문 화면 **2,488개**를 WebP로 저장했다. 원문 스크린샷 2,486개와 썸네일로 대체한 2개다. 메탈 슬러그 6은 원문에 남은 81×61 화면을 사용한다. 화면 누락은 **1,069개**: 원문 이미지 준비중 1,047개, 공개된 이미지 주소가 모두 삭제된 게임 22개다. 공개된 원문 스크린샷 미리보기 URL을 사용해 게임별 화면 하나를 WebP로 저장한다. 원문이 공통 ‘이미지 준비중’ 그림만 제공하는 1,047개는 스크린샷으로 인정하지 않으며, 화면 누락 사유와 원문 링크를 카드에 표시한다. 비율과 원문의 출처 표시를 유지하며 최대 720×540이다. 화면 확인에 실패하면 다른 공개 스크린샷, 목록 미리보기, 썸네일 순으로 시도하고, 모든 실패는 보고서에 기록한다. 공개 HTML과 이미지 외의 게임 파일·플레이어·에뮬레이터는 수집·배포하지 않는다. 원문 `robots.txt`의 전체 공개 허용을 확인했다.

기존 `src/classic-games.js`와 `src/classic-games.css`를 그대로 사용한다. 처음 24개를 표시하고 목록 끝에 가까워지면 다음 24개를 추가한다. 이미지도 브라우저의 지연 로딩을 사용한다. 카테고리·장르·검색 변경 시 새 결과의 첫 묶음부터 표시한다. JavaScript 또는 IntersectionObserver가 없으면 전체 게임 목록을 제공한다.

## 파일

- `public/data/jjang-games.json`: 게임명·원문 장르·짧은 소개·기본 진행·화면·출처.
- `public/images/jjang-games/*.webp`: 게임별 원문 화면.
- `posts/jjang-games/index.html`: 새 포스트.
- `docs/jjang-crawl-report.json`: 목록 페이지별 수, 홈페이지 요약과의 차이, 장르 대조, 이미지 실패 기록.
- `scripts/crawl-jjang.py`: 3개 동시 요청, 응답 간격·재시도, 외부 캐시를 사용하는 수집기.
- `scripts/build-jjang-catalog.py`: JSON·보고서·HTML 생성.
- `scripts/verify-jjang-catalog.py`: 원문 ID·제목·장르의 보존과 모든 이미지 디코딩 검증.
- `scripts/verify-classic-games.cjs`, `scripts/verify-classic-assets.cjs`: 기존 도감과 새 도감을 검증하는 공통 도구. 인자 없이 실행하면 기존 Tooli 도감을 검증한다.

## 재수집과 검증

Python 3.9 이상, Node 22, Chrome이 필요하다. 같은 Python 의존성을 사용하는 Tooli 수집기의 requirements를 재사용한다. Playwright는 별도 환경에서 제공한다.

```sh
python3 -m venv /tmp/tooli-crawl-venv
/tmp/tooli-crawl-venv/bin/pip install -r scripts/tooli-requirements.txt
/tmp/tooli-crawl-venv/bin/python scripts/crawl-jjang.py collect
/tmp/tooli-crawl-venv/bin/python scripts/crawl-jjang.py images
/tmp/tooli-crawl-venv/bin/python scripts/build-jjang-catalog.py
/tmp/tooli-crawl-venv/bin/python scripts/verify-jjang-catalog.py
npm run build
npm run preview
NODE_PATH=/path/to/playwright/node_modules node scripts/verify-classic-games.cjs http://127.0.0.1:8080 jjang
NODE_PATH=/path/to/playwright/node_modules node scripts/verify-classic-games.cjs https://nyimpe.github.io jjang
node scripts/verify-classic-assets.cjs https://nyimpe.github.io jjang
```

`/tmp/nyimpe-jjang-cache`에 원문 응답과 단계별 수집 결과를 보관한다. 캐시를 유지하면 중단 후 이어서 수집한다. 최신 원문을 다시 수집하려면 캐시를 별도로 비운다. 홈페이지 요약, 실제 목록과 장르는 원문의 현재 상태에 따라 변할 수 있다.

브라우저 검증은 카테고리·장르 39개 조합, 3,557개 전체 스크롤 표시, 마지막 묶음, 검색·빈 결과·초기화·저장 URL·키보드 조작, 1280·375·320px, 밝은·어두운 테마, 콘솔, JavaScript 없는 목록을 포함한다. 배포 검증은 HTML, JSON, 해시된 JS/CSS, 모든 화면의 응답을 로컬 빌드와 SHA-256으로 대조한다. Playwright 입력은 브라우저 자동화이며 물리 입력 검증은 아니다.
