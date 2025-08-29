# Jumping Cat 🐱

[![Deploy to GitHub Pages](https://github.com/nyimpe/nyimpe.github.io/actions/workflows/deploy.yml/badge.svg)](https://nyimpe.github.io/)

**👉 라이브 데모: [https://nyimpe.github.io/](https://nyimpe.github.io/)**

## 🎮 프로젝트 소개

`Jumping Cat`은 Phaser 3 게임 엔진과 React를 사용하여 만든 간단한 아케이드 웹 게임입니다. 플레이어는 고양이 캐릭터를 조종하여 계속해서 나타나는 플랫폼을 밟고 최대한 높이 올라가는 것을 목표로 합니다.

## ✨ 주요 기술 스택

-   **게임 엔진**: [Phaser 3](https://phaser.io/phaser3)
-   **프레임워크**: [React 19](https://react.dev/)
-   **빌드 도구**: [Vite](https://vitejs.dev/)
-   **언어**: JavaScript (ESM)
-   **배포**: GitHub Pages

## 📂 프로젝트 구조

-   `index.html`: 애플리케이션의 기본 HTML 진입점
-   `src/main.jsx`: React 애플리케이션을 DOM에 렌더링하는 진입점
-   `src/App.jsx`: Phaser 게임 컨테이너를 렌더링하는 메인 React 컴포넌트
-   `src/main.js`: Phaser 게임 인스턴스를 설정하고 시작하는 파일
-   `src/scenes/`: `Preloader`, `Game` 등 Phaser 게임 씬
-   `src/gameObjects/`: `Player`, `Platform` 등 재사용 가능한 게임 객체 클래스
-   `public/`: `style.css` 등 정적 에셋 포함

## 🚀 로컬에서 실행하기

### 사전 준비

-   [Node.js](https://nodejs.org/)와 npm이 설치되어 있어야 합니다.

### 설치 및 실행

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/nyimpe/nyimpe.github.io.git
    ```

2.  **프로젝트 디렉토리로 이동:**
    ```bash
    cd nyimpe.github.io
    ```

3.  **의존성 설치:**
    ```bash
    npm install
    ```

4.  **개발 서버 실행:**
    ```bash
    npm run dev
    ```
    이제 브라우저에서 `http://localhost:5173` (또는 Vite가 지정한 다른 포트)으로 접속할 수 있습니다.

## 📦 빌드 및 배포

-   **프로덕션 빌드:**
    ```bash
    npm run build
    ```
    빌드 결과물은 `dist` 디렉토리에 생성됩니다.

-   **배포:**
    `main` 브랜치에 푸시하면 GitHub Actions 워크플로우(`.github/workflows/deploy.yml`)가 자동으로 `dist` 디렉토리의 내용을 `gh-pages` 브랜치에 배포합니다.