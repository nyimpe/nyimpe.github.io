# 프로젝트 컨텍스트: "Jumping Cat"

이 프로젝트는 고양이가 플랫폼을 계속 점프해서 올라가는 아케이드 웹 게임입니다.

## 💻 기술 스택

- **게임 엔진**: Phaser 3
- **프레임워크**: React 19 (Phaser 캔버스 래퍼 역할)
- **빌드 도구**: Vite
- **언어**: JavaScript (ESM)
- **배포**: GitHub Pages (GitHub Actions을 통해 자동화)

## 📂 주요 파일 구조

- `package.json`: 프로젝트 의존성 및 스크립트 관리
- `vite.config.js`: Vite 빌드 설정
- `index.html`: 애플리케이션의 기본 HTML 진입점
- `src/main.jsx`: React 애플리케이션을 DOM에 렌더링하는 진입점
- `src/App.jsx`: Phaser 게임 컨테이너를 렌더링하는 메인 React 컴포넌트
- `src/main.js`: Phaser 게임 인스턴스를 설정하고 시작하는 파일
- `src/scenes/`: Phaser 게임 씬
  - `Preloader.js`: 에셋을 미리 로드하는 씬
  - `Game.js`: 핵심 게임 플레이 로직 포함
- `src/gameObjects/`: 플레이어, 플랫폼 등 재사용 가능한 게임 객체 클래스
- `src/assets.js`: 게임에 사용되는 모든 에셋(이미지, 스프라이트시트)을 관리
- `public/`: `style.css` 등 정적 에셋 포함
- `.github/workflows/deploy.yml`: GitHub Pages 배포를 위한 자동화 워크플로우

## ✏️ 코딩 규칙

- **컴포넌트**: React 컴포넌트 파일명은 PascalCase (`MyComponent.jsx`)를 사용합니다.
- **게임 객체**: Phaser 게임 객체 클래스 파일명은 PascalCase (`Player.js`)를 사용합니다.
- **상태 관리**: 게임의 핵심 상태는 `Game.js` 씬 내에서 관리됩니다. React는 주로 게임 캔버스를 렌더링하는 역할만 합니다.
- **에셋 관리**: 모든 에셋 경로는 `src/assets.js`에서 중앙 관리하므로, 에셋을 추가/수정할 때는 이 파일을 업데이트해야 합니다.

## ❌ 금지 사항

- React의 `useState`나 `useEffect` 같은 훅을 복잡한 게임 로직 관리에 사용하지 마세요. 게임 상태는 Phaser 씬 내부에서 처리하는 것을 원칙으로 합니다.
- Phaser 게임 로직과 React UI 로직을 과도하게 섞지 마세요. React는 게임을 담는 컨테이너 역할에 집중합니다.
