# 플레이 컨셉아트 재제작 · 2026-10-06

`posts/korean-folklore-game-design/index.html`의 43개 기획을 읽고 각 장르의 핵심 조작, 괴물 대응 규칙, 시점과 UI를 담은 픽셀아트 플레이 시안을 내장 ImageGen 도구로 제작했습니다. CLI/API 대체 경로는 사용하지 않았습니다.

생성 원본: 기존 `public/images/folklore-game/concept-*.png` 43개 파일, 1672×941 PNG. 2026-10-07에 게시용 이미지를 최대 960×540으로 축소하고 더 작은 WebP 또는 AVIF로 압축했습니다. `manifest.json`은 현재 경로·크기·해시를 기록하며, 각 항목의 `optimizedFrom`과 기존 묶음별 기록은 생성 당시의 PNG 정보를 보존합니다. 게시물의 대체 설명과 캡션은 유지하고 이미지 참조의 내용 해시는 압축 결과에 맞췄습니다.

## 생성 기록

- `source-inventory.json`: 작업 시작 시점의 43개 기획과 기존 파일 해시.
- `manifest.json`: 최종 이미지 경로, 크기, 해시, 대체 설명, 캡션, 원본 생성 경로와 검토 기록.
- `prompts-1.json`, `prompt-1-retry.json`: 벽사록. 최종 생성은 재시도 프롬프트.
- `prompts-2-14.json`, `prompts-2-9-revisions.json`: 2–14번과 보정 프롬프트. 13번의 적오·일두칠계 카드 보정은 `prompt-13-edit.json`.
- `prompts-15-28.json`: 15–28번의 개별 생성 및 편집 프롬프트.
- `prompts-29-43.json`: 29–40번의 개별 생성 및 편집 기록. 파일명은 최초 작업 분담 범위에서 유지.
- `prompts-41-43.json`: 41–43번. 42번 최종 생성은 `prompt-42-retry.json`, 최종 편집은 `prompt-42-edit-final.json`.
- `manifest-*.json`: 각 제작 묶음의 상세 검토와 원본 경로.
- `page-preview.jpg`: 로컬 게시물에서 확인한 대표 화면.

## 표현 범위

이미지는 기획 검토용 시안이며 실제 게임 실행 캡처나 320×180 제작 규격을 완료한 게임 에셋이 아닙니다. 본문의 게임 제작 규격은 프로토타입 목표로 유지했습니다. 외형 기록이 비어 있는 존재는 창작적·상징적 표현이며 원전의 확정 외형으로 취급하지 않습니다.

생성 당시 PNG는 생성 도구의 출력을 그대로 복사했습니다. 외형과 표기 수정은 ImageGen 편집으로 수행했습니다. 이후의 게시용 해상도·품질 압축은 `scripts/optimize-post-images.py`로 수행하며, 기존 코드 드로잉 스크립트로 컨셉아트를 다시 그리지 않습니다.
