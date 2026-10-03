# nyimpe.github.io

작은 게임과 실험을 기록하는 개인 홈페이지입니다. [scd31.com](https://www.scd31.com/)의 흰 배경, 간결한 글 목록, 작은 배지와 고양이 그림에서 UI 방향을 참고했습니다. 소개·그림·배지는 이 프로젝트에 맞게 작성했습니다.

## 구성

- **페이지:** HTML + CSS + 일반 JavaScript를 Vite로 빌드합니다. React나 다른 UI 프레임워크를 사용하지 않습니다.
- **테마:** 모든 페이지의 상단 버튼으로 라이트·다크 모드를 전환합니다. 기본값은 시스템 설정이고, 직접 선택한 값은 브라우저에 저장됩니다.
- **게임:** 기존 Phaser 3 게임 5개를 각각 독립 페이지로 연결했습니다. 시작 버튼을 누를 때 해당 게임을 불러옵니다.
- **빌드:** Vite가 HTML 페이지와 게임 모듈을 빌드합니다. React, Ruby on Rails, 별도 서버나 데이터베이스가 필요하지 않습니다.
- **배포:** `main`에 push하면 GitHub Actions가 `dist/`를 GitHub Pages에 배포합니다.

```text
index.html                  홈: 기술 스택 엠블렘, 기록 목록
about/index.html            영어 소개
posts/<slug>/index.html     게임 또는 일반 기록 페이지
public/style.css            공통 스타일
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

`preview`는 빌드한 사이트를 같은 주소에서 확인합니다. 개발 서버와 동시에 실행하면 Vite가 다른 포트를 선택할 수 있으므로 터미널의 실제 주소를 확인하세요.

## 기록 추가

1. `posts/my-note/index.html`을 만듭니다. 기존 게시글의 `<head>`, 사이트 헤더, 푸터를 복사하면 같은 UI를 사용할 수 있습니다.
2. `<main>` 안에 글을 작성하고 제목, 설명, 날짜를 바꿉니다.
3. 일반 글이라면 게임 영역과 `game-page.js` 스크립트를 제거합니다. 공통 테마를 위해 `main.js` 스크립트와 헤더의 테마 버튼은 유지합니다.
4. 홈 `index.html`의 `.post-list`에 링크와 `<time datetime="YYYY-MM-DD">`를 추가합니다. 최신 기록을 위에 놓습니다.
5. `npm run build` 후 페이지를 확인합니다. `posts/`의 각 하위 폴더는 빌드 시 자동으로 포함됩니다.

게시글 주소는 `/posts/my-note/`처럼 폴더 기반입니다. GitHub Pages에서 직접 접속하거나 새로고침할 수 있습니다.

## 게임 추가

1. `src/games/<id>/main.js`에서 Phaser 게임을 생성하는 기본 export를 작성합니다. 기존 게임처럼 `StartGame(parent, options = {})`가 설정을 받아 `new Phaser.Game({ ...config, ...options, parent })`를 반환하도록 합니다.
2. `src/game-page.js`의 `games`에 동적 import를 등록합니다.
3. 기존 게임 게시글을 복사해 `data-game`과 소개, 조작법을 수정합니다. 가로형 게임은 `.game-stage`에 `landscape` 클래스를 붙입니다.
4. 홈의 기록 목록에 추가합니다.

키보드 입력은 게임 컨테이너에 연결됩니다. 게임을 시작하면 컨테이너에 포커스를 주고, 게임 화면을 클릭하거나 Tab으로 다시 선택할 수 있습니다. 화면 밖에서는 페이지 스크롤과 링크 탐색이 가능합니다. 다시 시작 버튼은 페이지를 새로고침해 게임과 오디오 상태를 초기화합니다.

기존 게임의 날짜는 게임 폴더에 영향을 준 마지막 Git 커밋 날짜를 사용했습니다. 게임 규칙·자산은 유지했고, 진입점에 공통 입력 설정을 전달하는 옵션을 추가했습니다. Jumping Cat의 물리 디버그 표시는 껐으며, 발판은 이미지에 실제로 존재하는 프레임만 무작위 선택하도록 수정했습니다. Tetris는 숨겨진 입력 영역 때문에 화면 버튼이 동작하지 않던 문제를 수정했습니다. 입력 영역은 투명하게 그리되 Phaser 입력 시스템에서는 활성 상태로 유지합니다.

## 고양이 이미지

사용자가 제공한 `IMG_4173.png`를 built-in imagegen으로 배경 제거했습니다. PNG의 투명도를 유지하며 헤더용 크기로 저장하고, 같은 누끼 이미지의 얼굴에서 16·32·48·64·128·256px ICO를 만들었습니다.

사용 프롬프트:

> Use case: background-extraction. Edit target: the attached pixel-art orange-and-white sitting cat. Asset type: website mascot cutout. Remove ONLY the entire background (wall, floor, rug, flowers, cast shadow). Preserve the exact original cat, full body, ears, whiskers, feet, tail, orange and white patches, black pixel outlines, proportions, pose and pixel-art edges. Do not redesign or redraw. Isolate the cat alone on actual transparent alpha, with modest transparent padding. No added objects, no text, no ground shadow.
