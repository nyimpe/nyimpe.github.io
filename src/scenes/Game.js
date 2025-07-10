/*
 * Asset from: https://kenney.nl/assets/pixel-platformer
 *
 */
import ASSETS from "../assets.js";
import ANIMATION from "../animation.js";
import Player from "../gameObjects/Player.js";
import PlayerBullet from "../gameObjects/PlayerBullet.js";
import EnemyFlying from "../gameObjects/EnemyFlying.js";
import EnemyBullet from "../gameObjects/EnemyBullet.js";
import Explosion from "../gameObjects/Explosion.js";

// 메인 게임 씬 클래스 - 실제 게임플레이 담당
export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
  }

  create() {
    // 게임 초기화 순서
    this.initVariables(); // 변수 초기화
    this.initGameUi(); // UI 초기화
    this.initAnimations(); // 애니메이션 초기화
    this.initPlayer(); // 플레이어 초기화
    this.initInput(); // 입력 초기화
    this.initPhysics(); // 물리 초기화
    this.initMap(); // 맵 초기화
  }

  update() {
    // 배경 맵 업데이트
    this.updateMap();

    // 게임이 시작되지 않았으면 리턴
    if (!this.gameStarted) return;

    // 플레이어 업데이트
    this.player.update();
    // 적 스폰 카운터 관리
    if (this.spawnEnemyCounter > 0) this.spawnEnemyCounter--;
    else this.addFlyingGroup();
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
    this.spawnEnemyCounter = 0; // 다음 적 그룹 생성 전 타이머

    this.map; // 타일 맵 참조
    this.groundLayer; // 타일 맵의 지면 레이어 참조
  }

  initGameUi() {
    // 튜토리얼 텍스트 생성
    this.tutorialText = this.add
      .text(this.centreX, this.centreY, "Tap to shoot!", {
        fontFamily: "Arial Black",
        fontSize: 42,
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

  initAnimations() {
    // 폭발 애니메이션 생성
    this.anims.create({
      key: ANIMATION.explosion.key,
      frames: this.anims.generateFrameNumbers(
        ANIMATION.explosion.texture,
        ANIMATION.explosion.config
      ),
      frameRate: ANIMATION.explosion.frameRate,
      repeat: ANIMATION.explosion.repeat,
    });
  }

  initPhysics() {
    // 게임 오브젝트 그룹 생성
    this.enemyGroup = this.add.group();
    this.enemyBulletGroup = this.add.group();
    this.playerBulletGroup = this.add.group();

    // 충돌 감지 설정
    // 플레이어와 적 총알 충돌
    this.physics.add.overlap(
      this.player,
      this.enemyBulletGroup,
      this.hitPlayer,
      null,
      this
    );
    // 플레이어 총알과 적 충돌
    this.physics.add.overlap(
      this.playerBulletGroup,
      this.enemyGroup,
      this.hitEnemy,
      null,
      this
    );
    // 플레이어와 적 충돌
    this.physics.add.overlap(
      this.player,
      this.enemyGroup,
      this.hitPlayer,
      null,
      this
    );
  }

  initPlayer() {
    // 플레이어 객체 생성
    this.player = new Player(this, this.centreX, this.scale.height - 100, 8);
  }

  initInput() {
    // 키보드 입력 설정
    this.cursors = this.input.keyboard.createCursorKeys();

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
    this.addFlyingGroup();
  }

  fireBullet(x, y) {
    // 플레이어 총알 발사
    const bullet = new PlayerBullet(this, x, y);
    this.playerBulletGroup.add(bullet);
  }

  removeBullet(bullet) {
    // 플레이어 총알 제거
    this.playerBulletGroup.remove(bullet, true, true);
  }

  fireEnemyBullet(x, y, power) {
    // 적 총알 발사
    const bullet = new EnemyBullet(this, x, y, power);
    this.enemyBulletGroup.add(bullet);
  }

  removeEnemyBullet(bullet) {
    // 적 총알 제거
    this.playerBulletGroup.remove(bullet, true, true);
  }

  // 비행 적 그룹 추가
  addFlyingGroup() {
    this.spawnEnemyCounter = Phaser.Math.RND.between(5, 8) * 60; // x초 후 다음 그룹 생성
    const randomId = Phaser.Math.RND.between(0, 11); // tiles.png에서 이미지 선택할 ID
    const randomCount = Phaser.Math.RND.between(5, 15); // 생성할 적의 수
    const randomInterval = Phaser.Math.RND.between(8, 12) * 100; // 각 적 생성 간 지연 시간
    const randomPath = Phaser.Math.RND.between(0, 3); // 경로 선택 (그룹은 같은 경로 사용)
    const randomPower = Phaser.Math.RND.between(1, 4); // 적의 강도 (데미지 및 총알 이미지 결정)
    const randomSpeed = Phaser.Math.RND.realInRange(0.0001, 0.001); // 적의 pathSpeed 증가량

    this.timedEvent = this.time.addEvent({
      delay: randomInterval,
      callback: this.addEnemy,
      args: [randomId, randomPath, randomSpeed, randomPower], // addEnemy()에 전달할 매개변수
      callbackScope: this,
      repeat: randomCount,
    });
  }

  addEnemy(shipId, pathId, speed, power) {
    // 적 추가
    const enemy = new EnemyFlying(this, shipId, pathId, speed, power);
    this.enemyGroup.add(enemy);
  }

  removeEnemy(enemy) {
    // 적 제거
    this.enemyGroup.remove(enemy, true, true);
  }

  addExplosion(x, y) {
    // 폭발 효과 추가
    new Explosion(this, x, y);
  }

  hitPlayer(player, obstacle) {
    // 플레이어 피격 처리
    this.addExplosion(player.x, player.y);
    player.hit(obstacle.getPower());
    obstacle.die();

    this.GameOver();
  }

  hitEnemy(bullet, enemy) {
    // 적 피격 처리
    this.updateScore(10);
    bullet.remove();
    enemy.hit(bullet.getPower());
  }

  updateScore(points) {
    // 점수 업데이트
    this.score += points;
    this.scoreText.setText(`Score: ${this.score}`);
  }

  GameOver() {
    // 게임 오버 처리
    this.gameStarted = false;
    this.gameOverText.setVisible(true);
  }
}
