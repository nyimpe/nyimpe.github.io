import Phaser from "phaser";

const TETROMINOS = {
  I: {
    shape: [
      [0, 0, 0, 0],
      [1, 1, 1, 1],
      [0, 0, 0, 0],
      [0, 0, 0, 0]
    ],
    color: 0x00f0f0 // Cyan
  },
  O: {
    shape: [
      [1, 1],
      [1, 1]
    ],
    color: 0xf0f000 // Yellow
  },
  T: {
    shape: [
      [0, 1, 0],
      [1, 1, 1],
      [0, 0, 0]
    ],
    color: 0xa000f0 // Purple
  },
  S: {
    shape: [
      [0, 1, 1],
      [1, 1, 0],
      [0, 0, 0]
    ],
    color: 0x00f000 // Green
  },
  Z: {
    shape: [
      [1, 1, 0],
      [0, 1, 1],
      [0, 0, 0]
    ],
    color: 0xf00000 // Red
  },
  J: {
    shape: [
      [1, 0, 0],
      [1, 1, 1],
      [0, 0, 0]
    ],
    color: 0x0000f0 // Blue
  },
  L: {
    shape: [
      [0, 0, 1],
      [1, 1, 1],
      [0, 0, 0]
    ],
    color: 0xf0a000 // Orange
  }
};

class SoundSynth {
  constructor() {
    this.ctx = null;
  }

  init() {
    if (this.ctx) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    } catch (e) {
      console.warn("Web Audio API not supported:", e);
    }
  }

  playTone(freq, duration, type = "sine", startOffset = 0, volume = 0.05) {
    this.init();
    if (!this.ctx) return;
    try {
      if (this.ctx.state === "suspended") {
        this.ctx.resume();
      }
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime + startOffset);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      gain.gain.setValueAtTime(volume, this.ctx.currentTime + startOffset);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + startOffset + duration);
      osc.start(this.ctx.currentTime + startOffset);
      osc.stop(this.ctx.currentTime + startOffset + duration);
    } catch {
      // Ignore
    }
  }

  playMove() {
    this.playTone(180, 0.04, "triangle", 0, 0.06);
  }

  playRotate() {
    this.playTone(320, 0.06, "sine", 0, 0.08);
  }

  playLand() {
    this.playTone(110, 0.1, "sawtooth", 0, 0.04);
  }

  playClear() {
    this.playTone(523.25, 0.08, "sine", 0, 0.08); // C5
    this.playTone(659.25, 0.08, "sine", 0.06, 0.08); // E5
    this.playTone(783.99, 0.08, "sine", 0.12, 0.08); // G5
    this.playTone(1046.50, 0.15, "sine", 0.18, 0.1); // C6
  }

  playGameOver() {
    this.playTone(200, 0.5, "sawtooth", 0, 0.08);
    this.playTone(150, 0.5, "sawtooth", 0.15, 0.08);
    this.playTone(100, 0.8, "sawtooth", 0.3, 0.1);
  }
}

export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
    this.soundSynth = new SoundSynth();
  }

  create() {
    this.cameras.main.setBackgroundColor("#11121c");

    // Dimensions
    this.gridCols = 10;
    this.gridRows = 20;
    this.cellSize = 25;
    this.gridWidth = this.gridCols * this.cellSize;
    this.gridHeight = this.gridRows * this.cellSize;
    this.gridX = (this.scale.width - this.gridWidth) / 2;
    this.gridY = 120; // leaves space at top

    // State Variables
    this.board = Array.from({ length: this.gridRows }, () => Array(this.gridCols).fill(0));
    this.score = 0;
    this.level = 1;
    this.lines = 0;
    this.gameStarted = false;
    this.gameOver = false;

    // Piece Spawning State
    this.currentPiece = null;
    this.nextPiece = null;

    // Input Control Timers (for smooth DAS hold movement)
    this.btnStates = { left: false, right: false, down: false };
    this.justPressed = { left: true, right: true };
    this.nextMoveTime = { left: 0, right: 0, down: 0 };

    // Setup visual components
    this.gameGraphics = this.add.graphics();
    
    // UI HUD elements
    this.initUi();

    // Controls setup
    this.initControls();

    // Show Start Screen overlay
    this.showStartScreen();
  }

  initUi() {
    const headingStyle = {
      fontFamily: "Courier New, monospace, sans-serif",
      fontSize: "14px",
      fontWeight: "bold",
      color: "#8a9fc4",
    };

    const valueStyle = {
      fontFamily: "Courier New, monospace, sans-serif",
      fontSize: "22px",
      fontWeight: "bold",
      color: "#ffffff",
    };

    // Score display
    this.scoreLabel = this.add.text(20, 25, "SCORE", headingStyle);
    this.scoreText = this.add.text(20, 42, "000000", valueStyle);

    // Level display
    this.levelLabel = this.add.text(175, 25, "LEVEL", headingStyle);
    this.levelText = this.add.text(175, 42, "01", valueStyle);

    // Lines display
    this.linesLabel = this.add.text(175, 75, "LINES", headingStyle);
    this.linesText = this.add.text(175, 92, "000", valueStyle);

    // Next piece display frame
    this.nextLabel = this.add.text(310, 25, "NEXT", headingStyle);
  }

  initControls() {
    this.cursors = this.input.keyboard.createCursorKeys();
    
    // Additional manual keyboards bindings
    this.keys = this.input.keyboard.addKeys({
      space: Phaser.Input.Keyboard.KeyCodes.SPACE,
      w: Phaser.Input.Keyboard.KeyCodes.W,
      a: Phaser.Input.Keyboard.KeyCodes.A,
      s: Phaser.Input.Keyboard.KeyCodes.S,
      d: Phaser.Input.Keyboard.KeyCodes.D,
      up: Phaser.Input.Keyboard.KeyCodes.UP
    });

    // Handle single tap actions (like rotate and hard drop via keyboard)
    this.input.keyboard.on("keydown-SPACE", () => {
      if (this.gameStarted && !this.gameOver) {
        this.hardDrop();
      }
    });

    this.input.keyboard.on("keydown-UP", () => {
      if (this.gameStarted && !this.gameOver) {
        this.rotatePiece();
      }
    });

    this.input.keyboard.on("keydown-W", () => {
      if (this.gameStarted && !this.gameOver) {
        this.rotatePiece();
      }
    });

    // Setup on-screen mobile buttons
    this.createMobileButtons();
  }

  createMobileButtons() {
    const self = this;

    const drawButton = (textStr, x, y, size, color, isCircle = true) => {
      const graphics = self.add.graphics();
      const label = self.add.text(x, y, textStr, {
        fontFamily: "Arial Black",
        fontSize: size * 0.45,
        color: "#ffffff",
        stroke: "#11121c",
        strokeThickness: 5
      }).setOrigin(0.5).setDepth(20);

      const normalAlpha = 0.65;
      const activeAlpha = 1.0;

      const redraw = (pressed) => {
        graphics.clear();
        graphics.fillStyle(color, pressed ? activeAlpha : normalAlpha);
        if (isCircle) {
          graphics.fillCircle(x, y, size);
          graphics.lineStyle(4, 0xffffff, pressed ? 1.0 : 0.6);
          graphics.strokeCircle(x, y, size);
        } else {
          const w = size * 1.8;
          const h = size * 1.0;
          graphics.fillRoundedRect(x - w/2, y - h/2, w, h, 14);
          graphics.lineStyle(4, 0xffffff, pressed ? 1.0 : 0.6);
          graphics.strokeRoundedRect(x - w/2, y - h/2, w, h, 14);
        }
      };

      redraw(false);

      // Interactive hit zone
      let hitZone;
      if (isCircle) {
        hitZone = self.add.circle(x, y, size).setInteractive();
      } else {
        const w = size * 1.8;
        const h = size * 1.0;
        hitZone = self.add.rectangle(x, y, w, h).setInteractive();
      }
      hitZone.setDepth(25).setScrollFactor(0);
      hitZone.setVisible(false);

      return { hitZone, redraw, label };
    };

    // Movement Buttons (Left/Right/Soft Drop)
    const leftBtnInfo = drawButton("←", 60, 770, 36, 0x4d5370);
    leftBtnInfo.hitZone.on("pointerdown", () => {
      self.btnStates.left = true;
      leftBtnInfo.redraw(true);
      self.soundSynth.playMove();
    });
    const stopLeft = () => {
      self.btnStates.left = false;
      leftBtnInfo.redraw(false);
    };
    leftBtnInfo.hitZone.on("pointerup", stopLeft);
    leftBtnInfo.hitZone.on("pointerout", stopLeft);

    const rightBtnInfo = drawButton("→", 170, 770, 36, 0x4d5370);
    rightBtnInfo.hitZone.on("pointerdown", () => {
      self.btnStates.right = true;
      rightBtnInfo.redraw(true);
      self.soundSynth.playMove();
    });
    const stopRight = () => {
      self.btnStates.right = false;
      rightBtnInfo.redraw(false);
    };
    rightBtnInfo.hitZone.on("pointerup", stopRight);
    rightBtnInfo.hitZone.on("pointerout", stopRight);

    const downBtnInfo = drawButton("↓", 115, 860, 36, 0x4d5370);
    downBtnInfo.hitZone.on("pointerdown", () => {
      self.btnStates.down = true;
      downBtnInfo.redraw(true);
      self.soundSynth.playMove();
    });
    const stopDown = () => {
      self.btnStates.down = false;
      downBtnInfo.redraw(false);
    };
    downBtnInfo.hitZone.on("pointerup", stopDown);
    downBtnInfo.hitZone.on("pointerout", stopDown);

    // Action Buttons (Rotate / Hard Drop)
    const rotateBtnInfo = drawButton("ROT", 335, 755, 46, 0xff5252);
    rotateBtnInfo.hitZone.on("pointerdown", () => {
      rotateBtnInfo.redraw(true);
      self.rotatePiece();
    });
    const stopRotate = () => {
      rotateBtnInfo.redraw(false);
    };
    rotateBtnInfo.hitZone.on("pointerup", stopRotate);
    rotateBtnInfo.hitZone.on("pointerout", stopRotate);

    const hardBtnInfo = drawButton("HARD DROP", 335, 855, 44, 0x3d70ff, false);
    hardBtnInfo.hitZone.on("pointerdown", () => {
      hardBtnInfo.redraw(true);
      self.hardDrop();
    });
    const stopHard = () => {
      hardBtnInfo.redraw(false);
    };
    hardBtnInfo.hitZone.on("pointerup", stopHard);
    hardBtnInfo.hitZone.on("pointerout", stopHard);
  }

  showStartScreen() {
    this.overlayGraphics = this.add.graphics();
    this.overlayGraphics.fillStyle(0x0e0f14, 0.9);
    this.overlayGraphics.fillRect(0, 0, this.scale.width, this.scale.height);
    this.overlayGraphics.setDepth(50);

    this.startTitle = this.add.text(this.scale.width / 2, 280, "🧱 TETRIS", {
      fontFamily: "Arial Black",
      fontSize: "44px",
      fontWeight: "bold",
      color: "#ffffff",
      stroke: "#3d70ff",
      strokeThickness: 10,
      align: "center"
    }).setOrigin(0.5).setDepth(51);

    this.startSub = this.add.text(this.scale.width / 2, 340, "CLASSIC", {
      fontFamily: "Arial Black",
      fontSize: "24px",
      fontWeight: "bold",
      color: "#3d70ff",
      align: "center"
    }).setOrigin(0.5).setDepth(51);

    this.startPrompt = this.add.text(this.scale.width / 2, 480, "Tap Screen or Press SPACE\nto Start Playing", {
      fontFamily: "Courier New, monospace, sans-serif",
      fontSize: "16px",
      fontWeight: "bold",
      color: "#a4b5d6",
      align: "center",
      lineSpacing: 10
    }).setOrigin(0.5).setDepth(51);

    // Pulse effect on prompt
    this.tweens.add({
      targets: this.startPrompt,
      alpha: 0.4,
      duration: 1000,
      yoyo: true,
      repeat: -1
    });

    // Make the screen clickable to start
    this.input.once("pointerdown", this.startGame, this);
    this.input.keyboard.once("keydown-SPACE", this.startGame, this);
  }

  startGame() {
    // Unlocked Audio
    this.soundSynth.init();

    // Clean start menu elements
    if (this.startTitle) this.startTitle.destroy();
    if (this.startSub) this.startSub.destroy();
    if (this.startPrompt) this.startPrompt.destroy();
    if (this.overlayGraphics) this.overlayGraphics.destroy();

    // Clear board and stats
    this.board = Array.from({ length: this.gridRows }, () => Array(this.gridCols).fill(0));
    this.score = 0;
    this.level = 1;
    this.lines = 0;
    this.gameOver = false;
    this.gameStarted = true;

    this.updateStatsUi();

    // Spawning pieces
    this.nextPiece = this.generateRandomPiece();
    this.spawnPiece();

    // Setup core drop timer loop
    if (this.dropTimer) this.dropTimer.destroy();
    this.dropTimer = this.time.addEvent({
      delay: this.getDropDelay(),
      callback: this.onDropTick,
      callbackScope: this,
      loop: true
    });
  }

  getDropDelay() {
    return Math.max(80, 1000 - (this.level - 1) * 90);
  }

  onDropTick() {
    if (!this.gameStarted || this.gameOver) return;
    this.moveDown();
  }

  spawnPiece() {
    this.currentPiece = this.nextPiece;
    
    const shapeW = this.currentPiece.shape[0].length;
    this.currentPiece.x = Math.floor((this.gridCols - shapeW) / 2);
    // Align block perfectly
    this.currentPiece.y = this.currentPiece.type === "I" ? -1 : 0;

    this.nextPiece = this.generateRandomPiece();

    // If spawned piece is blocked, Game Over!
    if (this.checkCollision(this.currentPiece.x, this.currentPiece.y, this.currentPiece.shape)) {
      this.triggerGameOver();
    }
  }

  generateRandomPiece() {
    const keys = Object.keys(TETROMINOS);
    const randKey = keys[Math.floor(Math.random() * keys.length)];
    const proto = TETROMINOS[randKey];
    
    // Deep copy of shape matrix
    const shape = proto.shape.map(row => [...row]);
    
    return {
      type: randKey,
      shape: shape,
      color: proto.color
    };
  }

  checkCollision(px, py, shape) {
    for (let r = 0; r < shape.length; r++) {
      for (let c = 0; c < shape[r].length; c++) {
        if (shape[r][c]) {
          const boardX = px + c;
          const boardY = py + r;

          // Border collision checks
          if (boardX < 0 || boardX >= this.gridCols || boardY >= this.gridRows) {
            return true;
          }

          // Grid block collision checks
          if (boardY >= 0) {
            if (this.board[boardY][boardX] !== 0) {
              return true;
            }
          }
        }
      }
    }
    return false;
  }

  moveLeft() {
    if (!this.gameStarted || this.gameOver) return;
    if (!this.checkCollision(this.currentPiece.x - 1, this.currentPiece.y, this.currentPiece.shape)) {
      this.currentPiece.x--;
      this.soundSynth.playMove();
    }
  }

  moveRight() {
    if (!this.gameStarted || this.gameOver) return;
    if (!this.checkCollision(this.currentPiece.x + 1, this.currentPiece.y, this.currentPiece.shape)) {
      this.currentPiece.x++;
      this.soundSynth.playMove();
    }
  }

  moveDown() {
    if (!this.gameStarted || this.gameOver) return;
    if (!this.checkCollision(this.currentPiece.x, this.currentPiece.y + 1, this.currentPiece.shape)) {
      this.currentPiece.y++;
    } else {
      this.lockPiece();
      this.clearLines();
      this.spawnPiece();
    }
  }

  moveDownSoft() {
    if (!this.gameStarted || this.gameOver) return;
    if (!this.checkCollision(this.currentPiece.x, this.currentPiece.y + 1, this.currentPiece.shape)) {
      this.currentPiece.y++;
      this.score += 1;
      this.updateStatsUi();
      this.soundSynth.playMove();
    }
  }

  rotatePiece() {
    if (!this.gameStarted || this.gameOver) return;
    const rotated = this.rotateMatrix(this.currentPiece.shape);
    
    // Quick kick options: [currentX, kick left 1, kick right 1, kick left 2, kick right 2]
    const kicks = [0, -1, 1, -2, 2];
    for (let kick of kicks) {
      if (!this.checkCollision(this.currentPiece.x + kick, this.currentPiece.y, rotated)) {
        this.currentPiece.x += kick;
        this.currentPiece.shape = rotated;
        this.soundSynth.playRotate();
        return;
      }
    }
  }

  rotateMatrix(matrix) {
    const n = matrix.length;
    let result = Array.from({ length: n }, () => Array(n).fill(0));
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        result[c][n - 1 - r] = matrix[r][c];
      }
    }
    return result;
  }

  hardDrop() {
    if (!this.gameStarted || this.gameOver) return;
    const ghostY = this.getGhostY();
    const droppedRows = ghostY - this.currentPiece.y;
    
    this.currentPiece.y = ghostY;
    this.score += droppedRows * 2;
    
    this.lockPiece();
    this.clearLines();
    this.spawnPiece();
  }

  getGhostY() {
    let gy = this.currentPiece.y;
    while (!this.checkCollision(this.currentPiece.x, gy + 1, this.currentPiece.shape)) {
      gy++;
    }
    return gy;
  }

  lockPiece() {
    const shape = this.currentPiece.shape;
    const px = this.currentPiece.x;
    const py = this.currentPiece.y;

    for (let r = 0; r < shape.length; r++) {
      for (let c = 0; c < shape[r].length; c++) {
        if (shape[r][c]) {
          const boardX = px + c;
          const boardY = py + r;
          if (boardY >= 0 && boardY < this.gridRows) {
            this.board[boardY][boardX] = this.currentPiece.color;
          }
        }
      }
    }
    this.soundSynth.playLand();
  }

  clearLines() {
    let clearedCount = 0;
    
    for (let r = this.gridRows - 1; r >= 0; r--) {
      const isComplete = this.board[r].every(val => val !== 0);
      if (isComplete) {
        this.board.splice(r, 1);
        this.board.unshift(Array(this.gridCols).fill(0));
        clearedCount++;
        r++; // check same index again since lines shifted down
      }
    }

    if (clearedCount > 0) {
      // Score values scaling with line clears
      const scores = [0, 100, 300, 500, 800];
      const basePoints = scores[Math.min(clearedCount, 4)] || 800;
      this.score += basePoints * this.level;
      this.lines += clearedCount;

      // Increase level every 10 lines
      const nextLevel = Math.floor(this.lines / 10) + 1;
      if (nextLevel !== this.level) {
        this.level = nextLevel;
        // Reset/speed up drop timer
        this.dropTimer.reset({
          delay: this.getDropDelay(),
          callback: this.onDropTick,
          callbackScope: this,
          loop: true
        });
      }

      this.updateStatsUi();
      this.soundSynth.playClear();
    }
  }

  updateStatsUi() {
    this.scoreText.setText(String(this.score).padStart(6, "0"));
    this.levelText.setText(String(this.level).padStart(2, "0"));
    this.linesText.setText(String(this.lines).padStart(3, "0"));
  }

  triggerGameOver() {
    this.gameOver = true;
    this.soundSynth.playGameOver();
    if (this.dropTimer) this.dropTimer.destroy();

    // Create Game Over Box overlay
    this.gameOverOverlay = this.add.graphics();
    this.gameOverOverlay.fillStyle(0x0e0f14, 0.85);
    this.gameOverOverlay.fillRect(0, 0, this.scale.width, this.scale.height);
    this.gameOverOverlay.setDepth(60);

    this.gameOverTitle = this.add.text(this.scale.width / 2, 280, "GAME OVER", {
      fontFamily: "Arial Black",
      fontSize: "40px",
      fontWeight: "bold",
      color: "#ff3d3d",
      stroke: "#ffffff",
      strokeThickness: 4,
      align: "center"
    }).setOrigin(0.5).setDepth(61);

    this.gameOverStatsText = this.add.text(this.scale.width / 2, 380, `Final Score\n${String(this.score).padStart(6, "0")}`, {
      fontFamily: "Courier New, monospace, sans-serif",
      fontSize: "20px",
      fontWeight: "bold",
      color: "#ffffff",
      align: "center",
      lineSpacing: 10
    }).setOrigin(0.5).setDepth(61);

    this.gameOverPromptText = this.add.text(this.scale.width / 2, 480, "Tap Screen or Press SPACE\nto Play Again", {
      fontFamily: "Courier New, monospace, sans-serif",
      fontSize: "15px",
      fontWeight: "bold",
      color: "#a4b5d6",
      align: "center"
    }).setOrigin(0.5).setDepth(61);

    // Pulse effect on retry prompt
    this.tweens.add({
      targets: this.gameOverPromptText,
      alpha: 0.4,
      duration: 1000,
      yoyo: true,
      repeat: -1
    });

    // Tap/space to retry
    this.input.once("pointerdown", this.restartGame, this);
    this.input.keyboard.once("keydown-SPACE", this.restartGame, this);
  }

  restartGame() {
    // Destroy gameover texts & overlays
    if (this.gameOverTitle) this.gameOverTitle.destroy();
    if (this.gameOverStatsText) this.gameOverStatsText.destroy();
    if (this.gameOverPromptText) this.gameOverPromptText.destroy();
    if (this.gameOverOverlay) this.gameOverOverlay.destroy();

    this.startGame();
  }

  update() {
    // Draw/Clear logic
    this.gameGraphics.clear();

    // 1. Draw Grid Frame
    this.gameGraphics.lineStyle(4, 0x3d70ff, 1);
    this.gameGraphics.strokeRect(this.gridX - 2, this.gridY - 2, this.gridWidth + 4, this.gridHeight + 4);

    // 2. Draw Subtle Inner Grid Cells
    for (let r = 0; r < this.gridRows; r++) {
      for (let c = 0; c < this.gridCols; c++) {
        const x = this.gridX + c * this.cellSize;
        const y = this.gridY + r * this.cellSize;
        
        this.gameGraphics.fillStyle(0x1a1b28, 1);
        this.gameGraphics.fillRect(x, y, this.cellSize, this.cellSize);

        this.gameGraphics.lineStyle(1, 0x272a3d, 0.4);
        this.gameGraphics.strokeRect(x, y, this.cellSize, this.cellSize);
      }
    }

    // 3. Draw Locked Blocks on Board
    for (let r = 0; r < this.gridRows; r++) {
      for (let c = 0; c < this.gridCols; c++) {
        const color = this.board[r][c];
        if (color !== 0) {
          const x = this.gridX + c * this.cellSize;
          const y = this.gridY + r * this.cellSize;
          this.drawBevelBlock(x, y, this.cellSize, color);
        }
      }
    }

    // If game has not started, skip active drawing
    if (!this.gameStarted) return;

    // 4. Draw Ghost Piece (Aiming assistance)
    if (this.currentPiece && !this.gameOver) {
      const ghostY = this.getGhostY();
      const shape = this.currentPiece.shape;
      
      for (let r = 0; r < shape.length; r++) {
        for (let c = 0; c < shape[r].length; c++) {
          if (shape[r][c]) {
            const boardX = this.currentPiece.x + c;
            const boardY = ghostY + r;
            if (boardY >= 0 && boardY < this.gridRows) {
              const x = this.gridX + boardX * this.cellSize;
              const y = this.gridY + boardY * this.cellSize;
              
              // Draw hollow outline for ghost piece
              this.gameGraphics.lineStyle(2, this.currentPiece.color, 0.5);
              this.gameGraphics.strokeRect(x + 2, y + 2, this.cellSize - 4, this.cellSize - 4);
            }
          }
        }
      }
    }

    // 5. Draw Active Piece
    if (this.currentPiece && !this.gameOver) {
      const shape = this.currentPiece.shape;
      const px = this.currentPiece.x;
      const py = this.currentPiece.y;

      for (let r = 0; r < shape.length; r++) {
        for (let c = 0; c < shape[r].length; c++) {
          if (shape[r][c]) {
            const boardX = px + c;
            const boardY = py + r;
            if (boardY >= 0 && boardY < this.gridRows) {
              const x = this.gridX + boardX * this.cellSize;
              const y = this.gridY + boardY * this.cellSize;
              this.drawBevelBlock(x, y, this.cellSize, this.currentPiece.color);
            }
          }
        }
      }
    }

    // 6. Draw Next Piece Preview
    if (this.nextPiece) {
      const previewX = 310;
      const previewY = 45;
      const previewBoxSize = 80;

      // Draw neat next preview frame
      this.gameGraphics.lineStyle(3, 0x4d5370, 0.8);
      this.gameGraphics.strokeRect(previewX, previewY, previewBoxSize, previewBoxSize);
      this.gameGraphics.fillStyle(0x1a1b28, 0.6);
      this.gameGraphics.fillRect(previewX, previewY, previewBoxSize, previewBoxSize);

      const shape = this.nextPiece.shape;
      const shapeW = shape[0].length;
      const shapeH = shape.length;
      
      // Calculate centering offset in the preview box
      const blockS = 14;
      const centerOffsetX = previewX + (previewBoxSize - shapeW * blockS) / 2;
      const centerOffsetY = previewY + (previewBoxSize - shapeH * blockS) / 2;

      for (let r = 0; r < shape.length; r++) {
        for (let c = 0; c < shape[r].length; c++) {
          if (shape[r][c]) {
            const bx = centerOffsetX + c * blockS;
            const by = centerOffsetY + r * blockS;
            this.drawBevelBlock(bx, by, blockS, this.nextPiece.color);
          }
        }
      }
    }

    // 7. Process Input autorepeat (DAS) inside active updates
    if (this.gameStarted && !this.gameOver) {
      const timeNow = this.time.now;

      // Left movement checks
      if (this.cursors.left.isDown || this.keys.a.isDown || this.btnStates.left) {
        if (timeNow > this.nextMoveTime.left) {
          this.moveLeft();
          this.nextMoveTime.left = timeNow + (this.justPressed.left ? 220 : 60);
          this.justPressed.left = false;
        }
      } else {
        this.justPressed.left = true;
        this.nextMoveTime.left = 0;
      }

      // Right movement checks
      if (this.cursors.right.isDown || this.keys.d.isDown || this.btnStates.right) {
        if (timeNow > this.nextMoveTime.right) {
          this.moveRight();
          this.nextMoveTime.right = timeNow + (this.justPressed.right ? 220 : 60);
          this.justPressed.right = false;
        }
      } else {
        this.justPressed.right = true;
        this.nextMoveTime.right = 0;
      }

      // Down (Soft Drop) checks
      if (this.cursors.down.isDown || this.keys.s.isDown || this.btnStates.down) {
        if (timeNow > this.nextMoveTime.down) {
          this.moveDownSoft();
          this.nextMoveTime.down = timeNow + 60;
        }
      } else {
        this.nextMoveTime.down = 0;
      }
    }
  }

  drawBevelBlock(x, y, size, colorInt) {
    this.gameGraphics.fillStyle(colorInt, 1);
    this.gameGraphics.fillRect(x, y, size, size);

    // Bevel highlights
    this.gameGraphics.fillStyle(0xffffff, 0.4);
    this.gameGraphics.fillRect(x, y, size, 2);
    this.gameGraphics.fillRect(x, y, 2, size);

    // Bevel shadow
    this.gameGraphics.fillStyle(0x000000, 0.35);
    this.gameGraphics.fillRect(x, y + size - 2, size, 2);
    this.gameGraphics.fillRect(x + size - 2, y, 2, size);
  }
}
