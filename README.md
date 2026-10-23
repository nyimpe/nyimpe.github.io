# nyimpe.github.io
## 구성

- **페이지:** HTML + CSS + 일반 JavaScript를 Vite로 빌드합니다. React나 다른 UI 프레임워크를 사용하지 않습니다.
- **테마:** 모든 페이지의 상단 버튼으로 라이트·다크 모드를 전환합니다. 기본값은 시스템 설정이고, 직접 선택한 값은 브라우저에 저장됩니다.
- **게임:** 기존 Phaser 3 게임 5개를 각각 독립 페이지로 연결했습니다. 시작 버튼을 누를 때 해당 게임을 불러옵니다.
- **꼬리 수행 시제품:** `/posts/nabi-village/`의 턴제 로그라이크 시제품(마을 한 동네)은 `src/games/nabi-village/`에 있다. 그림·소리는 Ninja Adventure Asset Pack(CC0)에서 필요한 것만 `scripts/build-nabi-village-assets.py`로 복사하고, 팩 원본은 저장소에 두지 않는다.
- **작은 발자국 시제품:** `/posts/pawprint-prototype/`는 생활형 던전 RPG 기획(`/posts/pawprint-expedition/`)의 첫 브라우저 시제품이다. 게임 본체는 의존성 없는 단일 파일 `public/posts/pawprint-prototype/play.html`이며, 글 안의 틀(iframe)과 전체 화면 링크로 연다. 그림은 모두 코드로 그린 임시 픽셀아트다.
- **턴제 로그라이크 기획:** `/posts/turn-based-roguelike-overview/` 한 글에 기획 1~11편을 합쳤다. 옛 열 편의 주소는 `public/posts/turn-based-roguelike-*/`의 넘겨주기 페이지가 새 글의 해당 절로 보낸다.
- **괴물·귀신:** `/posts/korean-folklore-research/`에 326항목의 이미지·설명·출처를 정리했습니다.
- **빌드:** Vite가 HTML 페이지와 게임 모듈을 빌드합니다. 
- **포스팅 이미지:** `npm run optimize:images`가 해상도·품질을 낮추고 WebP와 AVIF를 비교해 더 작은 파일을 선택합니다. 게시물·JSON·현재 이미지 기록의 경로, 크기, 캐시 해시를 함께 수정합니다. Pillow 11.3 이상(WebP·AVIF 지원)이 필요하며, 게시물을 다시 생성한 뒤 실행합니다. 설정과 결과는 `docs/post-image-optimization.json`에 기록하고, 이미 처리한 파일은 해시로 확인해 재압축을 건너뜁니다.
- **외부 링크:** 다른 사이트로 가는 링크는 빌드할 때 `target="_blank" rel="noopener noreferrer"`가 자동으로 붙어 새 탭에서 열립니다. HTML에 직접 쓸 필요가 없습니다(`vite.config.js`).
- **배포:** `main`에 push하면 GitHub Actions가 `dist/`를 GitHub Pages에 배포합니다.
- **알림:** 어느 브랜치든 push하면 GitHub Actions가 새 커밋마다 커밋 메시지만 `git`이라는 이름으로 디스코드에 보냅니다. 웹훅 주소는 저장소 시크릿 `DISCORD_WEBHOOK_URL`에 있습니다(`.github/workflows/discord-notify.yml`).

```text
index.html                  홈: 기술 스택 엠블렘, 기록 목록
about/index.html            소개
posts/<slug>/index.html     게임 또는 일반 기록 페이지
src/style.css            공통 스타일
public/cat.png              첨부 이미지에서 배경을 제거한 고양이
public/favicon.ico          동일 고양이 얼굴을 사용한 다중 크기 아이콘
src/game-page.js            게임 페이지의 시작·로딩·포커스 처리
src/main.js                 공통 테마 초기화·전환·선호도 저장
src/games/                  기존 Phaser 게임 소스와 자산
vite.config.js              여러 HTML 진입점 수집, 외부 링크 새 탭 처리
```

## 실행

Node.js 22.12 이상에서 실행합니다.

```sh
npm ci
npm run dev
```

개발 서버는 `http://127.0.0.1:8080`입니다.

```sh
npm run build
npm run preview
```
