# 🕹️ Arcade Center

[![Deploy to GitHub Pages](https://github.com/nyimpe/nyimpe.github.io/actions/workflows/deploy.yml/badge.svg)](https://nyimpe.github.io/)

React와 Phaser 3를 활용한 아케이드 웹 게임 플랫폼입니다. 모바일에 최적화된 여러 2D 레트로 게임을 편리하게 관리하고 즐길 수 있습니다.

**👉 라이브 데모: [https://nyimpe.github.io/](https://nyimpe.github.io/)**

---

## 🎮 현재 제공하는 게임
1. **🍣 Sushi Neko (Jump):** 발판을 밟고 올라가며 높은 점수를 기록하는 타이밍 점프 게임.
2. **🧱 Tetris Classic:** 클래식 벽돌 쌓기 게임 (스무스한 터치/키보드 컨트롤 및 사운드 연출 포함).

---

## ⚙️ 주요 기술 스택
- **프레임워크:** [React 19](https://react.dev/)
- **게임 엔진:** [Phaser 3 (v3.90.0)](https://phaser.io/)
- **빌드 도구:** [Vite](https://vitejs.dev/)
- **배포:** GitHub Pages (GitHub Actions 자동 빌드 및 배포)

---

## 📂 프로젝트 폴더 구조
```text
nyimpe.github.io/
├── public/                # style.css 및 공통 정적 자산
├── src/
│   ├── games/            # 개별 게임 소스 폴더 (캡슐화 및 모듈화)
│   │   └── sushi-neko/   # 스시네코 게임 패키지
│   │       ├── assets/
│   │       ├── gameObjects/
│   │       ├── scenes/
│   │       ├── assets.js
│   │       └── main.js   # Phaser 초기화 진입점
│   ├── App.jsx           # 아케이드 메인 셸 (사이드바 메뉴 및 게임 선택기)
│   └── main.jsx          # React 앱 진입점
├── vite/                 # Vite 개발/배포용 설정 파일
└── package.json
```

---

## ➕ 새로운 게임 추가하기
새로운 Phaser 또는 React 기반 게임을 추가하는 프로세스는 매우 간편합니다.

1. **게임 소스 폴더 생성:**
   `src/games/` 아래에 새로운 게임 아이디로 폴더를 생성합니다 (예: `src/games/my-new-game/`).
2. **진입점 작성:**
   새 게임 폴더 내에 Phaser 인스턴스를 초기화하고 반환하는 `main.js` 파일을 만들고 default export로 등록합니다.
   ```javascript
   // src/games/my-new-game/main.js
   import Phaser from "phaser";
   const config = { ... };
   const StartGame = (parent) => new Phaser.Game({ ...config, parent });
   export default StartGame;
   ```
3. **게임 등록:**
   `src/App.jsx` 상단의 `GAMES` 레지스트리 배열에 새 게임 정보를 추가합니다.
   ```javascript
   const GAMES = [
     {
       id: "sushi-neko",
       title: "🍣 Sushi Neko (Jump)",
       description: "...",
       loader: () => import("./games/sushi-neko/main.js")
     },
     {
       id: "my-new-game",
       title: "👾 Space Invader",
       description: "Defend the earth from invaders!",
       loader: () => import("./games/my-new-game/main.js")
     }
   ];
   ```

---

## 🚀 로컬 실행 및 배포

### 1. 개발 서버 실행
```bash
npm install
npm run dev
```

### 2. 빌드 및 배포
`main` 브랜치에 코드를 `git push`하면, GitHub Actions 워크플로우(`.github/workflows/deploy.yml`)가 자동으로 트리거되어 빌드 결과물(`dist`)을 `gh-pages` 브랜치에 배포합니다.
