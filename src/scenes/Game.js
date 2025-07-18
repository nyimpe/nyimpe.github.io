import Phaser from "phaser";

/*
 * Asset from: https://kenney.nl/assets/pixel-platformer
 *
 */

import ASSETS from "../assets.js";
import Player from "../gameObjects/Player.js";
import Platform from "../gameObjects/Platform.js";

// 메인 게임 씬 클래스 - 실제 게임플레이 담당
export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
  }

  create() {
    // 게임 초기화 순서
    this.initVariables(); // 변수 초기화
    this.initGameUi(); // UI 초기화
    this.initMap(); // 맵 초기화
    this.initPlayer(); // 플레이어 초기화
    this.initPlatforms(); // 플랫폼 초기화
    this.initInput(); // 입력 초기화
    this.initPhysics(); // 물리 초기화
  }

  update() {
    // 배경 맵 업데이트
    // this.updateMap();
    // 게임이 시작되지 않았으면 리턴
    // if (!this.gameStarted) return;
    // this.player.update();
  }

  initVariables() {
    // 게임 기본 변수 초기화
    this.score = 0;
    this.centreX = this.scale.width * 0.5;
    this.centreY = this.scale.height * 0.5;

    // tiles.png의 타일 ID 목록
    // 배열 앞쪽 요소들이 weighted() 사용 시 더 높은 확률로 선택됩니다
    this.tiles = [
      50, 50, 50, 50, 50, 50, 50, 50, 50, 110, 110, 110, 110, 110, 50, 50, 50,
      50, 50, 50, 50, 50, 50, 110, 110, 110, 110, 110, 36, 48, 60, 72, 84,
    ];
    this.tileSize = 32; // 타일 크기 (픽셀 단위)

    this.mapOffset = 10; // 맵을 화면 위로 이동할 오프셋 (타일 단위)
    this.mapTop = -this.mapOffset * this.tileSize; // 맵을 화면 위로 이동할 오프셋 (픽셀 단위)
    this.mapHeight =
      Math.ceil(this.scale.height / this.tileSize) + this.mapOffset + 1; // 타일 맵 높이 (타일 단위)
    this.mapWidth = Math.ceil(this.scale.width / this.tileSize); // 타일 맵 너비 (타일 단위)
    this.scrollSpeed = 1; // 배경 스크롤 속도 (픽셀 단위)
    this.scrollMovement = 0; // 현재 스크롤 양
    // this.spawnEnemyCounter = 0; // 다음 적 그룹 생성 전 타이머

    this.map; // 타일 맵 참조
    this.groundLayer; // 타일 맵의 지면 레이어 참조
  }

  initGameUi() {
    // 튜토리얼 텍스트 생성
    this.tutorialText = this.add
      .text(this.centreX, this.centreY, "Touch or Space to Jump!", {
        fontFamily: "Arial Black",
        fontSize: 32,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
        align: "center",
      })
      .setOrigin(0.5)
      .setDepth(100);

    // 점수 텍스트 생성
    this.scoreText = this.add
      .text(20, 20, "Score: 0", {
        fontFamily: "Arial Black",
        fontSize: 28,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
      })
      .setDepth(100);

    // 게임 오버 텍스트 생성
    this.gameOverText = this.add
      .text(this.scale.width * 0.5, this.scale.height * 0.5, "Game Over", {
        fontFamily: "Arial Black",
        fontSize: 64,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
        align: "center",
      })
      .setOrigin(0.5)
      .setDepth(100)
      .setVisible(false);
  }

  initPhysics() {
    // 플레이어와 맵 충돌 설정
    this.physics.add.collider(this.player, this.groundLayer);

    // 플레이어와 플랫폼 충돌 설정
    this.physics.add.collider(this.player, this.platformGroup);
  }

  initPlayer() {
    // 플레이어 객체 생성 (화면 최하단에서 시작)
    this.player = new Player(this, this.centreX, this.scale.height - 1, 8);
  }

  /**
   * 플랫폼 시스템 초기화
   * - 플랫폼 그룹 생성 및 랜덤 플랫폼 배치 수행
   */
  initPlatforms() {
    // 플랫폼 그룹 생성 (물리 충돌 처리를 위한 그룹)
    this.platformGroup = this.add.group();

    // 랜덤 플랫폼 생성 시스템 실행
    this.generateRandomPlatforms();
  }

  generateRandomPlatforms() {
    const screenHeight = this.scale.height;
    const screenWidth = this.scale.width;

    // === 플랫폼 생성 설정 ===
    // 생성할 라인(층) 개수
    const lineCount = 10;

    // 한 라인당 플랫폼 개수 (1-3개 사이에서 설정 가능)
    // const platformsPerLine = Phaser.Math.Between(1, 4);
    const platformsPerLine = 2;

    // === 플랫폼 간격 설정 ===
    // 고정 수직 간격 (일정한 점프 리듬 제공)
    const verticalGap = 80;

    // 플랫폼 간 최소 수평 간격
    const minHorizontalGap = 50;

    // 플랫폼 높이 (Platform 클래스와 일치해야 함)
    const platformHeight = 16;

    // 플랫폼 너비 (고정값)
    const platformWidth = 100;

    // === 플랫폼 배치 영역 설정 ===
    const startY = 50; // 시작 높이
    const endY = screenHeight - 10; // 끝 높이
    const availableHeight = endY - startY;

    // 생성된 플랫폼 정보를 저장할 배열
    const platforms = [];

    // === 라인별 플랫폼 생성 ===
    for (let lineIndex = 0; lineIndex < lineCount; lineIndex++) {
      // 각 라인의 Y 좌표 계산 (균등 분배)
      const y = startY + (availableHeight / (lineCount + 1)) * (lineIndex + 1);

      // 현재 라인에 생성된 플랫폼들의 X 좌표를 저장
      const currentLinePlatforms = [];

      // 한 라인에 여러 플랫폼 생성
      for (
        let platformIndex = 0;
        platformIndex < platformsPerLine;
        platformIndex++
      ) {
        let attempts = 0;
        let validPosition = false;
        let x;

        // 수평 위치 찾기 (같은 라인 내에서 겹치지 않게)
        while (!validPosition && attempts < 100) {
          // x 좌표: 플랫폼이 화면을 벗어나지 않도록 랜덤 설정
          x = Phaser.Math.Between(0, screenWidth - platformWidth);

          validPosition = true;

          // 같은 라인의 다른 플랫폼과 겹침 검사
          for (let existingX of currentLinePlatforms) {
            const horizontalOverlap =
              x < existingX + platformWidth + minHorizontalGap &&
              x + platformWidth + minHorizontalGap > existingX;

            if (horizontalOverlap) {
              validPosition = false;
              break;
            }
          }

          attempts++;
        }

        // === 플랫폼 생성 ===
        if (validPosition) {
          // Platform 클래스를 사용하여 플랫폼 생성
          const platform = new Platform(this, x, y, platformWidth);

          // 플랫폼 그룹에 추가
          this.platformGroup.add(platform);

          // 현재 라인과 전체 플랫폼 정보에 저장
          currentLinePlatforms.push(x);
          platforms.push({
            x: x,
            y: y,
            width: platformWidth,
            height: platformHeight,
          });
        }
      }
    }
  }

  initInput() {
    // 키보드 입력 설정
    this.cursors = this.input.keyboard.createCursorKeys();

    // 터치 입력 설정
    this.input.on("pointerdown", () => {
      if (!this.gameStarted) {
        this.startGame();
      }
    });

    // 스페이스바 한 번만 눌림 감지
    this.cursors.space.once("down", (key, event) => {
      this.startGame();
    });
  }

  // 타일 맵 데이터 생성
  initMap() {
    const mapData = [];

    for (let y = 0; y < this.mapHeight; y++) {
      const row = [];

      for (let x = 0; x < this.mapWidth; x++) {
        // this.tiles에서 타일 ID를 무작위로 선택
        // weightedPick은 배열 앞쪽 요소들을 더 선호합니다
        const tileIndex = Phaser.Math.RND.weightedPick(this.tiles);

        row.push(tileIndex);
      }

      mapData.push(row);
    }
    // 타일맵 생성
    this.map = this.make.tilemap({
      data: mapData,
      tileWidth: this.tileSize,
      tileHeight: this.tileSize,
    });
    const tileset = this.map.addTilesetImage(ASSETS.spritesheet.tiles.key);
    this.groundLayer = this.map.createLayer(0, tileset, 0, this.mapTop);

    // 모든 타일에 충돌 설정
    this.groundLayer.setCollisionByExclusion([]);
  }

  // 타일 맵 스크롤 처리
  updateMap() {
    this.scrollMovement += this.scrollSpeed;

    if (this.scrollMovement >= this.tileSize) {
      // 맨 위에 새로운 행 생성
      let tile;
      let prev;

      // 맵을 아래에서 위로 반복
      for (let y = this.mapHeight - 2; y > 0; y--) {
        // 맵을 왼쪽에서 오른쪽으로 반복
        for (let x = 0; x < this.mapWidth; x++) {
          tile = this.map.getTileAt(x, y - 1);
          prev = this.map.getTileAt(x, y);

          prev.index = tile.index;

          if (y === 1) {
            // 맨 위 행인 경우
            // this.tiles에서 타일 ID를 무작위로 선택
            // weightedPick은 배열 앞쪽 요소들을 더 선호합니다
            tile.index = Phaser.Math.RND.weightedPick(this.tiles);
          }
        }
      }

      this.scrollMovement -= this.tileSize; // 0으로 리셋
    }

    this.groundLayer.y = this.mapTop + this.scrollMovement; // 타일 하나만큼 위로 이동
  }

  startGame() {
    // 게임 시작 처리
    this.gameStarted = true;
    this.tutorialText.setVisible(false);
  }

  // updateScore(points) {
  //   // 점수 업데이트
  //   this.score += points;
  //   this.scoreText.setText(`Score: ${this.score}`);
  // }

  GameOver() {
    // 게임 오버 처리
    this.gameStarted = false;
    this.gameOverText.setVisible(true);
  }
}
