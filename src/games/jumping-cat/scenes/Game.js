import Phaser from "phaser";
import ASSETS from "../assets.js";
import Player from "../gameObjects/Player.js";
import Platform from "../gameObjects/Platform.js";

export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
  }

  create() {
    this.initVariables();
    this.initGameUi();
    this.initMap();
    this.initPlatforms();
    this.initPlayer();
    this.initInput();
    this.initPhysics();
  }

  update() {
    if (!this.gameStarted) {
      return;
    }

    this.checkPlayerFallOut();
    this.checkPlatformGeneration();
    this.updateCamera();
    this.updateBackgroundExpansion();
    this.updateScore();
  }

  initVariables() {
    this.score = 0;
    this.centreX = this.scale.width * 0.5;
    this.centreY = this.scale.height * 0.5;

    this.tiles = [
      50, 50, 50, 50, 50, 50, 50, 50, 50, 110, 110, 110, 110, 110, 50, 50, 50,
      50, 50, 50, 50, 50, 50, 110, 110, 110, 110, 110, 36, 48, 60, 72, 84,
    ];
    this.tileSize = 32;
    this.mapOffset = 100;
    this.mapTop = -this.mapOffset * this.tileSize;
    this.mapHeight = 200;
    this.mapWidth = Math.ceil(this.scale.width / this.tileSize);
    this.scrollSpeed = 1;
    this.scrollMovement = 0;
    this.map;
    this.groundLayer;
    this.highestY = this.scale.height;
    this.lastPlatformY = 50;
    this.platformGenerationThreshold = 200;
    this.initialCameraY = 0;
    this.cameraFollowThreshold = this.scale.height * 0.3;
    this.lastExpansionY = this.mapTop;
    this.expansionCooldown = false;
    this.initialPlayerX = this.centreX;
    this.initialPlayerY = null;
    this.fallOutThreshold = 50;
  }

  initGameUi() {
    this.tutorialText = this.add
      .text(this.centreX, this.centreY, "Touch or Space to Jump!", {
        fontFamily: "Arial Black",
        fontSize: 28,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
        align: "center",
      })
      .setOrigin(0.5)
      .setDepth(100)
      .setScrollFactor(0);

    this.scoreText = this.add
      .text(20, 20, "Score: 0", {
        fontFamily: "Arial Black",
        fontSize: 28,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
      })
      .setDepth(100)
      .setScrollFactor(0);

    this.gameOverText = this.add
      .text(this.scale.width * 0.5, this.scale.height * 0.5, "Game Over", {
        fontFamily: "Arial Black",
        fontSize: 54,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
        align: "center",
      })
      .setOrigin(0.5)
      .setDepth(100)
      .setVisible(false)
      .setScrollFactor(0);
  }

  initPhysics() {
    this.physics.add.collider(this.player, this.groundLayer);
    this.physics.add.collider(this.player, this.floorPlatform);

    this.physics.add.overlap(
      this.player,
      this.platformGroup,
      this.handlePlatformCollision,
      null,
      this
    );
  }

  initPlayer() {
    const playerY = this.floorY - 132;
    this.player = new Player(this, this.centreX, playerY);
    this.initialPlayerY = playerY;
    this.initialCameraY = this.cameras.main.scrollY;
  }

  initPlatforms() {
    this.platformGroup = this.add.group();
    this.createFloorPlatform();
    this.generateRandomPlatforms();
  }

  createFloorPlatform() {
    const floorY = this.scale.height - 30;
    const floorWidth = this.scale.width;
    const floorHeight = 30;
    const floorGraphics = this.add.graphics();
    floorGraphics.fillStyle(0x4a4a4a);
    floorGraphics.fillRect(0, floorY, floorWidth, floorHeight);
    floorGraphics.setDepth(1);

    const floorPlatform = this.physics.add.staticGroup();
    const floorBody = this.add.rectangle(
      floorWidth / 2,
      floorY + floorHeight / 2,
      floorWidth,
      floorHeight
    );
    floorBody.setVisible(false);
    this.physics.add.existing(floorBody, true);
    floorPlatform.add(floorBody);
    this.floorPlatform = floorPlatform;
    this.floorY = floorY;
  }

  generateRandomPlatforms() {
    const screenHeight = this.scale.height;
    const screenWidth = this.scale.width;
    const lineCount = 10;
    const platformsPerLine = 2;
    const minHorizontalGap = 50;
    const platformHeight = 16;
    const platformWidth = 100;
    const startY = 50;
    const endY = screenHeight - 10;
    const availableHeight = endY - startY;
    const platforms = [];

    for (let lineIndex = 0; lineIndex < lineCount; lineIndex++) {
      const y = startY + (availableHeight / (lineCount + 1)) * (lineIndex + 1);
      const currentLinePlatforms = [];
      for (
        let platformIndex = 0;
        platformIndex < platformsPerLine;
        platformIndex++
      ) {
        let attempts = 0;
        let validPosition = false;
        let x;

        while (!validPosition && attempts < 100) {
          x = Phaser.Math.Between(0, screenWidth - platformWidth);

          validPosition = true;

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

        if (validPosition) {
          const platform = new Platform(this, x, y, platformWidth);
          this.platformGroup.add(platform);
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
    this.cursors = this.input.keyboard.createCursorKeys();
    this.input.on("pointerdown", () => {
      if (!this.gameStarted) {
        this.startGame();
      }
    });
    this.cursors.space.once("down", (key, event) => {
      this.startGame();
    });
  }

  initMap() {
    const mapData = [];

    for (let y = 0; y < this.mapHeight; y++) {
      const row = [];
      for (let x = 0; x < this.mapWidth; x++) {
        const tileIndex = Phaser.Math.RND.weightedPick(this.tiles);
        row.push(tileIndex);
      }
      mapData.push(row);
    }
    this.map = this.make.tilemap({
      data: mapData,
      tileWidth: this.tileSize,
      tileHeight: this.tileSize,
    });
    const tileset = this.map.addTilesetImage(ASSETS.spritesheet.tiles.key);
    this.groundLayer = this.map.createLayer(0, tileset, 0, this.mapTop);
    this.groundLayer.setCollisionByExclusion([]);
  }

  updateMap() {
    this.scrollMovement += this.scrollSpeed;

    if (this.scrollMovement >= this.tileSize) {
      let tile;
      let prev;

      for (let y = this.mapHeight - 2; y > 0; y--) {
        for (let x = 0; x < this.mapWidth; x++) {
          tile = this.map.getTileAt(x, y - 1);
          prev = this.map.getTileAt(x, y);
          prev.index = tile.index;

          if (y === 1) {
            tile.index = Phaser.Math.RND.weightedPick(this.tiles);
          }
        }
      }
      this.scrollMovement -= this.tileSize;
    }
    this.groundLayer.y = this.mapTop + this.scrollMovement;
  }

  startGame() {
    this.gameStarted = true;
    this.tutorialText.setVisible(false);
  }

  updateScore() {
    const playerY = this.player.y;
    let platformsBelowCount = 0;

    this.platformGroup.children.entries.forEach((platform) => {
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
    const prevPlayerBottom = playerBottom - playerVelocityY * (1 / 60);

    if (playerVelocityY >= 0) {
      const wasAbovePlatform = prevPlayerBottom <= platformTop + 5;
      const isNowBelowOrOnPlatform = playerBottom >= platformTop - 5;
      const playerLeft = player.body.left;
      const playerRight = player.body.right;
      const platformLeft = platform.body.left;
      const platformRight = platform.body.right;

      const horizontalOverlap =
        playerRight > platformLeft && playerLeft < platformRight;

      if (wasAbovePlatform && isNowBelowOrOnPlatform && horizontalOverlap) {
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
    const playerScreenY = this.player.y - this.cameras.main.scrollY;
    if (playerScreenY < this.cameraFollowThreshold) {
      const targetY = this.player.y - this.cameraFollowThreshold;
      const currentY = this.cameras.main.scrollY;
      const lerpFactor = 0.05;

      this.cameras.main.scrollY = Phaser.Math.Linear(
        currentY,
        targetY,
        lerpFactor
      );
    }
  }

  updateBackgroundExpansion() {
    const mapTopWorldY = this.mapTop;
    const expansionThreshold = 1000;

    if (
      !this.expansionCooldown &&
      this.player.y < mapTopWorldY + expansionThreshold
    ) {
      this.expandBackgroundUp();
    }
  }

  expandBackgroundUp() {
    this.expansionCooldown = true;
    const extensionHeight = 50;
    const newMapData = [];

    for (let y = 0; y < extensionHeight; y++) {
      const row = [];
      for (let x = 0; x < this.mapWidth; x++) {
        const tileIndex = Phaser.Math.RND.weightedPick(this.tiles);
        row.push(tileIndex);
      }
      newMapData.push(row);
    }

    const existingData = [];
    for (let y = 0; y < this.mapHeight; y++) {
      const row = [];
      for (let x = 0; x < this.mapWidth; x++) {
        const tile = this.map.getTileAt(x, y);
        row.push(tile ? tile.index : 0);
      }
      existingData.push(row);
    }

    const combinedData = [...newMapData, ...existingData];

    this.map.destroy();
    this.groundLayer.destroy();
    this.mapTop -= extensionHeight * this.tileSize;
    this.mapHeight += extensionHeight;
    this.map = this.make.tilemap({
      data: combinedData,
      tileWidth: this.tileSize,
      tileHeight: this.tileSize,
    });

    const tileset = this.map.addTilesetImage(ASSETS.spritesheet.tiles.key);
    this.groundLayer = this.map.createLayer(0, tileset, 0, this.mapTop);
    this.groundLayer.setCollisionByExclusion([]);

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

    this.time.delayedCall(1000, () => {
      this.expansionCooldown = false;
    });
  }

  checkPlatformGeneration() {
    if (this.player.y < this.highestY) {
      this.highestY = this.player.y;
    }

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
    const newY = this.lastPlatformY - verticalGap;
    const currentLinePlatforms = [];

    for (
      let platformIndex = 0;
      platformIndex < platformsPerLine;
      platformIndex++
    ) {
      let attempts = 0;
      let validPosition = false;
      let x;

      while (!validPosition && attempts < 100) {
        x = Phaser.Math.Between(0, screenWidth - platformWidth);
        validPosition = true;

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

      if (validPosition) {
        const platform = new Platform(this, x, newY, platformWidth);
        this.platformGroup.add(platform);
        currentLinePlatforms.push(x);
      }
    }

    this.lastPlatformY = newY;
  }

  checkPlayerFallOut() {
    const screenBottom = this.cameras.main.scrollY + this.scale.height;
    const playerY = this.player.y;

    if (playerY > screenBottom + this.fallOutThreshold) {
      this.GameOver();
    }
  }

  GameOver() {
    this.gameStarted = false;
    this.gameOverText.setVisible(true);
    this.time.delayedCall(3000, () => {
      this.resetGame();
    });
  }

  resetGame() {
    this.gameOverText.setVisible(false);
    this.player.x = this.initialPlayerX;
    this.player.y = this.initialPlayerY;
    this.player.body.velocity.x = 0;
    this.player.body.velocity.y = 0;
    this.cameras.main.scrollY = this.initialCameraY;
    this.score = 0;
    this.scoreText.setText("Score: 0");
    this.highestY = this.scale.height;
    this.tutorialText.setVisible(true);
    this.player.resetCharge();
  }
}
