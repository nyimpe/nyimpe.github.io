# nyimpe.github.io
## 구성

- **페이지:** HTML + CSS + 일반 JavaScript를 Vite로 빌드합니다. React나 다른 UI 프레임워크를 사용하지 않습니다.
- **테마:** 모든 페이지의 상단 버튼으로 라이트·다크 모드를 전환합니다. 기본값은 시스템 설정이고, 직접 선택한 값은 브라우저에 저장됩니다.
- **게임:** 기존 Phaser 3 게임 5개를 각각 독립 페이지로 연결했습니다. 시작 버튼을 누를 때 해당 게임을 불러옵니다.
- **빌드:** Vite가 HTML 페이지와 게임 모듈을 빌드합니다. 
- **배포:** `main`에 push하면 GitHub Actions가 `dist/`를 GitHub Pages에 배포합니다.

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
vite.config.js              여러 HTML 진입점을 자동 수집하는 빌드 설정
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
