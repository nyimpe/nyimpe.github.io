# 들메 — 걸어가는 집들의 시대

`world-bible.md`가 독립 세계관 설정집의 기준 원본이다. 서리띠를 피해 집과 마을이 이동하는 생활에서 지리·역사·마법·생업·정치·신앙을 전개한다. 해동·해명과 연결되지 않으며, 특정 주인공과 사건 순서·결말은 정하지 않는다.

## 생성

저장소 루트에서 실행한다.

```sh
python3 scripts/render-folklore-deulme.py
npm run build
```

- 웹 문서: `posts/korean-folklore-deulme/index.html`
- 다운로드: `public/downloads/folklore-deulme-bible.md` — 편집 원본과 동일한 바이트
- 지도: `public/images/folklore-deulme/deulme-map.svg` — 1200×900, 축척 없는 창작 관계도
- 지도에서 푸른 화살표는 서리띠의 진행 순서다. 가구는 보통 인접한 두 분지의 터를 왕복한다.
- 렌더러는 기존 `render-folklore-haedong.py`의 제한된 Markdown 파서를 재사용한다. 생성 HTML과 다운로드를 직접 수정하지 않는다.
- 16장 설정집이며 지리·신화·조직·역사·집신·보행 규칙은 창작이다. 네 전승 소재의 확인 범위는 원본 마지막 장에 명시한다.

검수 범위와 결과는 `verification.json`을 따른다. 공개 사이트 배포는 별도로 확인해야 한다.
