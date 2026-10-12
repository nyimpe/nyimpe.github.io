# 두모습 — 사람과 동물, 두 모습으로 사는 세상

`world-bible.md`가 편집 원본이다. 쉬운 말과 세 가지 규칙으로 가족·집·학교·일터를 설명하고, 장르 8가지와 매체 4가지에서 같은 세계를 쓰는 예를 담았다. 특정 주인공·적·임무·결말을 고정하지 않는다.

## 생성과 확인

```sh
python3 scripts/render-folklore-dumoseup.py
npm run build
```

- 게시글: `posts/korean-folklore-dumoseup/index.html`
- 다운로드: `public/downloads/folklore-dumoseup-bible.md` — 편집 원본과 바이트 단위로 동일
- 도식: `public/images/folklore-dumoseup/two-forms.svg` — 직접 작성한 1200×900 설명 그림
- 기존 해동 글의 제한된 Markdown 파서를 재사용한다. 생성된 HTML과 다운로드 파일을 직접 수정하지 않는다.
- 지리·역사·변신 규칙·풍습·인물은 창작이다. 참고 자료 세 항목과 각각의 확인 범위는 원고 12장에 있다.

## 기존 글 검토 범위

독립 설정집 3개, 생활 게임 글 5개, 민속 게임 기획 글 2개와 나머지 기획 묶음 3개를 확인했다.

| 글 경로 | 중심 소재 |
| --- | --- |
| `korean-folklore-worldbuilding` | 여울국의 괴이 법칙·기관·지역. 현재 HTML 제목은 괴이록이며 홈 목록의 해명 표기는 기존 상태를 유지했다. |
| `korean-folklore-haedong` | 다섯 부적을 고치는 모험. |
| `korean-folklore-deulme` | 서리띠와 걷는 집, 이주와 정착. |
| `tidepost` | 섬의 물때와 우편 배달. |
| `warmrest` | 온천집과 휴식 공간. |
| `glasswild` | 이동식 도감차와 생물 관찰. |
| `rootstar` | 빛·물로 길을 기르는 지하 정원. |
| `alleymoon` | 도시에서 모은 재료로 작은 공연 만들기. |
| `korean-folklore-game-design` | 43개 게임 기획. 가까운 소재인 둔갑.io는 타인·물건으로 숨는 경기다. |
| `korean-folklore-game-design-50` | 전승 존재별 별도 게임 기획 50개. |
| `party-deckbuilding-rpg-concepts` | 계약·법·피난·행동 순서·귀환·조사 중심의 원정. |
| `board-game-concepts` | 구매·정원·배송·거래·인양·축제·정전·경매·무전. |
| `new-game-concepts-10` | 접기·직조·수리·조선·언어·발굴·사진·측량·신문·조각. |

두모습은 변신 소재 자체의 독창성을 주장하지 않는다. 모든 주민이 자신의 두 몸을 공개하고 살아가는 사회가 중심이라는 점으로 구분한다. 동물 종류가 혈통·성격·직업·계급을 자동으로 정하지 않는다.

## 검증 기록

`verification.json`에 게시 전 구조·다운로드·링크·데스크톱/모바일 표시 확인 결과를 남긴다. 공개 배포 성공 여부는 GitHub Actions와 실제 공개 URL을 따로 확인한다.
