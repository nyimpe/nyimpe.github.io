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
    this.initPlatforms(); // 플랫폼 초기화 (바닥 플랫폼 생성)
    this.initPlayer(); // 플레이어 초기화 (바닥 플랫폼 위에 배치)
    this.initInput(); // 입력 초기화
    this.initPhysics(); // 물리 초기화
  }

  update() {
    // 배경 맵 업데이트
    // this.updateMap();
    // 게임이 시작되지 않았으면 리턴
    if (!this.gameStarted) return;

    // 플레이어가 화면 하단 밖으로 떨어졌는지 확인
    this.checkPlayerFallOut();

    // 플레이어 위치 추적 및 새 플랫폼 생성
    this.checkPlatformGeneration();
    
    // 카메라 업데이트
    this.updateCamera();
    
    // 배경 맵 동적 확장
    this.updateBackgroundExpansion();
    
    // 점수 업데이트
    this.updateScore();
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

    this.mapOffset = 100; // 맵을 화면 위로 이동할 오프셋을 더 크게 설정
    this.mapTop = -this.mapOffset * this.tileSize; // 맵을 화면 위로 이동할 오프셋 (픽셀 단위)
    this.mapHeight = 200; // 타일 맵 높이를 더 크게 설정 (충분한 배경 제공)
    this.mapWidth = Math.ceil(this.scale.width / this.tileSize); // 타일 맵 너비 (타일 단위)
    this.scrollSpeed = 1; // 배경 스크롤 속도 (픽셀 단위)
    this.scrollMovement = 0; // 현재 스크롤 양

    this.map; // 타일 맵 참조
    this.groundLayer; // 타일 맵의 지면 레이어 참조

    // 플랫폼 생성 관련 변수
    this.highestY = this.scale.height; // 플레이어가 도달한 최고 높이
    this.lastPlatformY = 50; // 마지막으로 생성된 플랫폼의 Y 좌표
    this.platformGenerationThreshold = 200; // 새 플랫폼 생성 임계값
    
    // 카메라 관련 변수
    this.initialCameraY = 0; // 초기 카메라 Y 위치
    this.cameraFollowThreshold = this.scale.height * 0.3; // 카메라가 따라가기 시작하는 임계값
    
    // 배경 확장 관련 변수
    this.lastExpansionY = this.mapTop; // 마지막 확장된 Y 위치
    this.expansionCooldown = false; // 확장 쿨다운 플래그
    
    // 게임 리셋 관련 변수
    this.initialPlayerX = this.centreX; // 초기 플레이어 X 위치
    this.initialPlayerY = null; // 초기 플레이어 Y 위치 (initPlayer에서 설정)
    this.fallOutThreshold = 200; // 화면 하단에서 얼마나 더 떨어져야 게임오버인지
  }

  initGameUi() {
    // 튜토리얼 텍스트 생성 (카메라에 고정)
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
      .setDepth(100)
      .setScrollFactor(0); // 카메라 스크롤에 영향받지 않음

    // 점수 텍스트 생성 (카메라에 고정)
    this.scoreText = this.add
      .text(20, 20, "Score: 0", {
        fontFamily: "Arial Black",
        fontSize: 28,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
      })
      .setDepth(100)
      .setScrollFactor(0); // 카메라 스크롤에 영향받지 않음

    // 게임 오버 텍스트 생성 (카메라에 고정)
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
      .setVisible(false)
      .setScrollFactor(0); // 카메라 스크롤에 영향받지 않음
  }

  initPhysics() {
    // 플레이어와 맵 충돌 설정
    this.physics.add.collider(this.player, this.groundLayer);

    // 플레이어와 바닥 플랫폼 충돌 설정
    this.physics.add.collider(this.player, this.floorPlatform);

    // 플레이어와 플랫폼 커스텀 충돌 설정 (밑에서 위로 통과 가능)
    this.physics.add.overlap(
      this.player,
      this.platformGroup,
      this.handlePlatformCollision,
      null,
      this
    );
  }

  initPlayer() {
    // 플레이어 객체 생성 (바닥 플랫폼 위에서 시작)
    const playerY = this.floorY - 32; // 바닥 플랫폼 위에 플레이어 배치 (플레이어 높이 고려)
    this.player = new Player(this, this.centreX, playerY, 8);
    
    // 초기 위치 저장 (리셋용)
    this.initialPlayerY = playerY;
    
    // 초기 카메라 위치 저장
    this.initialCameraY = this.cameras.main.scrollY;
  }

  /**
   * 플랫폼 시스템 초기화
   * - 플랫폼 그룹 생성 및 랜덤 플랫폼 배치 수행
   */
  initPlatforms() {
    // 플랫폼 그룹 생성 (물리 충돌 처리를 위한 그룹)
    this.platformGroup = this.add.group();

    // 바닥 플랫폼 생성
    this.createFloorPlatform();

    // 랜덤 플랫폼 생성 시스템 실행
    this.generateRandomPlatforms();
  }

  createFloorPlatform() {
    // 화면 전체 너비의 바닥 플랫폼 생성
    const floorY = this.scale.height - 30; // 화면 하단에서 30픽셀 위
    const floorWidth = this.scale.width;
    const floorHeight = 30; // 바닥 플랫폼 높이
    
    // Rectangle 그래픽으로 바닥 플랫폼 생성 (확실하게 화면 전체 채우기)
    const floorGraphics = this.add.graphics();
    floorGraphics.fillStyle(0x4a4a4a); // 회색 색상
    floorGraphics.fillRect(0, floorY, floorWidth, floorHeight);
    floorGraphics.setDepth(1);
    
    // 물리 바디를 위한 static 그룹 생성
    const floorPlatform = this.physics.add.staticGroup();
    const floorBody = this.add.rectangle(floorWidth / 2, floorY + floorHeight / 2, floorWidth, floorHeight);
    floorBody.setVisible(false); // 투명하게 설정 (그래픽만 보이도록)
    this.physics.add.existing(floorBody, true); // static body로 추가
    floorPlatform.add(floorBody);
    
    // 플랫폼 그룹에 추가
    this.floorPlatform = floorPlatform;
    
    // 바닥 플랫폼 Y 좌표 저장 (플레이어 위치 계산용)
    this.floorY = floorY;
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

  updateScore() {
    // 플레이어 위치보다 아래에 있는 플랫폼 개수 계산
    const playerY = this.player.y;
    let platformsBelowCount = 0;
    
    this.platformGroup.children.entries.forEach(platform => {
      if (platform.y > playerY) {
        platformsBelowCount++;
      }
    });
    
    this.score = platformsBelowCount;
    this.scoreText.setText(`Score: ${this.score}`);
  }

  handlePlatformCollision(player, platform) {
    const playerBottom = player.body.bottom;
    const platformTop = platform.body.top;
    const playerVelocityY = player.body.velocity.y;
    
    // 이전 프레임에서의 플레이어 위치 계산 (속도 기반)
    const prevPlayerBottom = playerBottom - playerVelocityY * (1/60); // 60fps 기준
    
    // 플레이어가 하강 중일 때만 처리
    if (playerVelocityY >= 0) {
      // 이전 프레임에서는 발판 위에 있었고, 현재 프레임에서는 발판을 지나쳤는지 확인
      const wasAbovePlatform = prevPlayerBottom <= platformTop + 5;
      const isNowBelowOrOnPlatform = playerBottom >= platformTop - 5;
      
      // 플레이어가 발판의 수평 범위 내에 있는지 확인
      const playerLeft = player.body.left;
      const playerRight = player.body.right;
      const platformLeft = platform.body.left;
      const platformRight = platform.body.right;
      
      const horizontalOverlap = playerRight > platformLeft && playerLeft < platformRight;
      
      // 발판을 통과했거나 발판 위에 정확히 위치한 경우 충돌 처리
      if (wasAbovePlatform && isNowBelowOrOnPlatform && horizontalOverlap) {
        // 플레이어를 발판 위에 정확히 위치시키고 수직 속도 초기화
        player.body.y = platformTop - player.body.height;
        player.body.velocity.y = 0;
        player.body.blocked.down = true;
        player.body.touching.down = true;
        
        return true;
      }
    }
    return false;
  }

  updateCamera() {
    // 플레이어가 화면 상단 임계값에 도달했을 때만 카메라 이동
    const playerScreenY = this.player.y - this.cameras.main.scrollY;
    
    if (playerScreenY < this.cameraFollowThreshold) {
      // 플레이어가 화면 상단에 가까워지면 카메라가 부드럽게 따라감
      const targetY = this.player.y - this.cameraFollowThreshold;
      const currentY = this.cameras.main.scrollY;
      const lerpFactor = 0.05; // 부드러운 이동을 위한 lerp 팩터
      
      this.cameras.main.scrollY = Phaser.Math.Linear(currentY, targetY, lerpFactor);
    }
  }

  updateBackgroundExpansion() {
    // 플레이어가 배경 맵의 상단 근처에 도달하면 배경을 위로 확장
    const mapTopWorldY = this.mapTop;
    const expansionThreshold = 1000; // 확장 임계값
    
    // 쿨다운 중이 아니고, 플레이어가 임계값에 도달했을 때만 확장
    if (!this.expansionCooldown && this.player.y < mapTopWorldY + expansionThreshold) {
      this.expandBackgroundUp();
    }
  }

  expandBackgroundUp() {
    // 확장 쿨다운 설정
    this.expansionCooldown = true;
    
    // 배경 맵을 위로 확장
    const extensionHeight = 50; // 확장할 타일 행 수
    
    // 새로운 맵 데이터 생성
    const newMapData = [];
    
    // 위쪽에 새로운 행들 추가
    for (let y = 0; y < extensionHeight; y++) {
      const row = [];
      for (let x = 0; x < this.mapWidth; x++) {
        const tileIndex = Phaser.Math.RND.weightedPick(this.tiles);
        row.push(tileIndex);
      }
      newMapData.push(row);
    }
    
    // 기존 맵 데이터 가져오기
    const existingData = [];
    for (let y = 0; y < this.mapHeight; y++) {
      const row = [];
      for (let x = 0; x < this.mapWidth; x++) {
        const tile = this.map.getTileAt(x, y);
        row.push(tile ? tile.index : 0);
      }
      existingData.push(row);
    }
    
    // 새 데이터와 기존 데이터 결합
    const combinedData = [...newMapData, ...existingData];
    
    // 맵 재생성
    this.map.destroy();
    this.groundLayer.destroy();
    
    // 새로운 맵 상단 위치 계산
    this.mapTop -= extensionHeight * this.tileSize;
    this.mapHeight += extensionHeight;
    
    // 새 맵 생성
    this.map = this.make.tilemap({
      data: combinedData,
      tileWidth: this.tileSize,
      tileHeight: this.tileSize,
    });
    
    const tileset = this.map.addTilesetImage(ASSETS.spritesheet.tiles.key);
    this.groundLayer = this.map.createLayer(0, tileset, 0, this.mapTop);
    this.groundLayer.setCollisionByExclusion([]);
    
    // 물리 시스템 재설정
    this.physics.world.colliders.destroy();
    this.physics.add.collider(this.player, this.groundLayer);
    this.physics.add.collider(this.player, this.floorPlatform);
    this.physics.add.overlap(
      this.player,
      this.platformGroup,
      this.handlePlatformCollision,
      null,
      this
    );
    
    // 확장 완료 후 쿨다운 해제 (1초 후)
    this.time.delayedCall(1000, () => {
      this.expansionCooldown = false;
    });
  }

  checkPlatformGeneration() {
    // 플레이어가 도달한 최고 높이 업데이트
    if (this.player.y < this.highestY) {
      this.highestY = this.player.y;
    }

    // 플레이어가 화면 상단 근처에 도달하면 새 플랫폼 생성
    if (this.player.y < this.lastPlatformY + this.platformGenerationThreshold) {
      this.generateTopPlatforms();
    }
  }

  generateTopPlatforms() {
    const screenWidth = this.scale.width;
    const platformWidth = 100;
    const platformsPerLine = 2;
    const verticalGap = 80;
    const minHorizontalGap = 50;

    // 새로운 플랫폼을 현재 최고 플랫폼보다 위에 생성
    const newY = this.lastPlatformY - verticalGap;

    // 생성된 플랫폼 정보를 저장할 배열
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

      // 플랫폼 생성
      if (validPosition) {
        // Platform 클래스를 사용하여 플랫폼 생성
        const platform = new Platform(this, x, newY, platformWidth);

        // 플랫폼 그룹에 추가
        this.platformGroup.add(platform);

        // 현재 라인 플랫폼 정보에 저장
        currentLinePlatforms.push(x);
      }
    }

    // 마지막 플랫폼 Y 좌표 업데이트
    this.lastPlatformY = newY;
  }

  checkPlayerFallOut() {
    // 플레이어가 화면 하단 밖으로 떨어졌는지 확인
    const screenBottom = this.cameras.main.scrollY + this.scale.height;
    const playerY = this.player.y;
    
    // 플레이어가 화면 하단에서 fallOutThreshold만큼 더 떨어지면 게임 오버
    if (playerY > screenBottom + this.fallOutThreshold) {
      this.GameOver();
    }
  }

  GameOver() {
    // 게임 오버 처리
    this.gameStarted = false;
    this.gameOverText.setVisible(true);
    
    // 2초 후 게임 리셋
    this.time.delayedCall(2000, () => {
      this.resetGame();
    });
  }
  
  resetGame() {
    // 게임 오버 텍스트 숨기기
    this.gameOverText.setVisible(false);
    
    // 플레이어를 초기 위치로 이동
    this.player.x = this.initialPlayerX;
    this.player.y = this.initialPlayerY;
    this.player.body.velocity.x = 0; // 속도 초기화
    this.player.body.velocity.y = 0;
    
    // 카메라를 초기 위치로 리셋
    this.cameras.main.scrollY = this.initialCameraY;
    
    // 게임 상태 초기화
    this.score = 0;
    this.scoreText.setText("Score: 0");
    this.highestY = this.scale.height;
    
    
    // 튜토리얼 텍스트 다시 표시
    this.tutorialText.setVisible(true);
    
    // 플레이어 충전 상태 초기화
    this.player.resetCharge();
  }
}
