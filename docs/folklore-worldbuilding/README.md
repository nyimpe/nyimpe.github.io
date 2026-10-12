# 해명 — 산신과 왕국의 시대 · 편집 원본

`world-bible.md`가 세계관 설정집의 기준 원본이다. 해명은 산과 강의 신령들이 먼저 살던 땅, 무너진 금라 왕조의 유산을 다섯 정치권이 이어받은 세계다. 설정집은 창세 신화·대륙·민족·국가·역사·신앙을 정리하며, 개별 작품의 주인공과 줄거리는 별도로 구성한다.

기존 사이트의 「한국 괴물·귀신」 도감 항목과 요약을 소재로 삼았다. 전승에서 가져온 요소와 창작 해석은 원본의 자료 대응표에서 구분하며, 자료 확인 범위는 출처 설명을 따른다. 해명의 지도·신화·국가·연대·제도는 창작 설정이다.

저장소 루트에서 다음 명령으로 사이트 글과 다운로드를 함께 갱신한다.

```sh
python3 scripts/render-folklore-worldbuilding.py
```

- 사이트 글: `posts/korean-folklore-worldbuilding/index.html`
- 다운로드: `public/downloads/folklore-world-bible.md` — 원본과 바이트 단위로 동일한 사본
- 대륙 지도: `public/images/folklore-worldbuilding/haemyeong-map.svg`
- 원본의 절대 사이트 링크는 HTML에서만 상대경로로 변환한다. 각 장의 `{#anchor}`는 목차와 링크 대상으로 사용하며 화면에 표시하지 않는다.
- 독립된 줄의 `![지도 설명](https://nyimpe.github.io/images/folklore-worldbuilding/haemyeong-map.svg)`는 지도와 설명으로 표시한다. 지도는 화면 너비에 맞춰 축소되며 원본의 가로세로 비율을 유지한다.

생성 파일을 직접 고치지 말고 원본 또는 렌더러를 수정한다. 최종 사이트 빌드는 `npm run build`로 확인한다.
