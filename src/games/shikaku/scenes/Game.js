import Phaser from "phaser";

class SoundSynth {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (this.ctx) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    } catch {
      // noop
    }
  }
  playTone(freq, dur, type = "sine", vol = 0.05) {
    this.init();
    if (!this.ctx) return;
    try {
      if (this.ctx.state === "suspended") this.ctx.resume();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      gain.gain.setValueAtTime(vol, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + dur);
      osc.start();
      osc.stop(this.ctx.currentTime + dur);
    } catch {
      // noop
    }
  }
  tap() { this.playTone(440, 0.05, "triangle", 0.06); }
  place() { this.playTone(600, 0.1, "sine", 0.07); }
  win() {
    this.playTone(523, 0.1, "sine", 0.06);
    this.playTone(659, 0.1, "sine", 0.06);
    this.playTone(784, 0.1, "sine", 0.06);
  }
}

// Puzzle generator: randomly partition grid into rectangles
function generateShikaku(size) {
  const visited = Array.from({ length: size }, () => Array(size).fill(false));
  const blocks = []; // { cells: [[r,c],...], numberPos: [r,c] }
  const puzzle = Array.from({ length: size }, () => Array(size).fill(null));
  // puzzle[r][c] = { number: N } for number cells, null for empty

  let blockId = 0;

  while (true) {
    // Find first unvisited cell
    let startR = -1, startC = -1;
    for (let r = 0; r < size && startR < 0; r++) {
      for (let c = 0; c < size && startR < 0; c++) {
        if (!visited[r][c]) { startR = r; startC = c; }
      }
    }
    if (startR < 0) break; // all cells filled

    // Gather all possible rectangles anchored at (startR, startC) that only cover unvisited cells
    const candidates = [];
    for (let h = 1; h <= size - startR; h++) {
      for (let w = 1; w <= size - startC; w++) {
        let valid = true;
        const cells = [];
        for (let dr = 0; dr < h && valid; dr++) {
          for (let dc = 0; dc < w && valid; dc++) {
            const rr = startR + dr;
            const cc = startC + dc;
            if (visited[rr][cc]) { valid = false; }
            else cells.push([rr, cc]);
          }
        }
        if (valid) candidates.push({ h, w, area: h * w, cells });
      }
    }

    if (candidates.length === 0) {
      // Shouldn't happen, but regenerate if stuck
      return generateShikaku(size);
    }

    // Pick a random candidate
    const pick = candidates[Math.floor(Math.random() * candidates.length)];

    // Mark cells visited
    for (const [r, c] of pick.cells) visited[r][c] = true;

    // Choose one random cell to place the number
    const numPos = pick.cells[Math.floor(Math.random() * pick.cells.length)];

    blocks.push({
      id: blockId,
      area: pick.area,
      cells: pick.cells,
      numberPos: numPos,
    });
    blockId++;
  }

  // Build puzzle array: mark number cells
  for (const block of blocks) {
    const [nr, nc] = block.numberPos;
    puzzle[nr][nc] = { number: block.area };
  }

  return { puzzle, blocks, size };
}

// Shikaku cell colors (8 palette)
const BLOCK_COLORS = [
  0x7c4dff, 0x4caf50, 0xff9800, 0xe91e63,
  0x00bcd4, 0xffeb3b, 0x9c27b0, 0x607d8b,
];

export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
    this.sound = new SoundSynth();
  }

  init(data) {
    this.gridSize = data.size || 5;
    this.cellSize = Math.floor(380 / this.gridSize); // fit in 380px
    this.gridPx = this.gridSize * this.cellSize;
  }

  create() {
    this.cameras.main.setBackgroundColor("#1a1a2e");
    this.sound.init();

    // Generate puzzle
    const { puzzle, blocks, size } = generateShikaku(this.gridSize);
    this.puzzle = puzzle;
    this.solutionBlocks = blocks;
    this.gridSize = size;
    this.cellSize = Math.floor(380 / this.gridSize);
    this.gridPx = this.gridSize * this.cellSize;

    // Grid origin (centered)
    this.gridX = Math.floor((this.scale.width - this.gridPx) / 2);
    this.gridY = 160;

    // Player state
    this.playerPlaced = Array.from({ length: size }, () => Array(size).fill(-1));
    // -1 = empty, >=0 = placed block id
    this.playerBlockColors = {};
    this.nextColorIdx = 0;

    // Drag state
    this.isDragging = false;
    this.dragStart = null; // {r, c}
    this.dragEnd = null;   // {r, c}
    this.dragGfx = this.add.graphics();
    this.dragGfx.setDepth(10);

    // Board graphics
    this.boardGfx = this.add.graphics();
    this.boardGfx.setDepth(1);

    // Number texts
    this.numberTexts = [];

    // UI buttons
    this.createUI();

    // Input
    this.input.on("pointerdown", this.onPointerDown, this);
    this.input.on("pointermove", this.onPointerMove, this);
    this.input.on("pointerup", this.onPointerUp, this);

    // Draw initial board
    this.drawBoard();
    this.renderNumbers();

    // Back button
    this.createBackButton();

    this.gameComplete = false;
  }

  createUI() {
    const style = {
      fontFamily: "Arial, sans-serif",
      fontSize: "14px",
      color: "#b39ddb",
    };
    this.add.text(10, 10, "◧ SHIKAKU", {
      fontFamily: "Arial Black",
      fontSize: "18px",
      color: "#7c4dff",
    });
    this.add.text(10, 34, `${this.gridSize}×${this.gridSize}`, style);

    // New game button
    const btnX = this.scale.width - 90;
    const btnY = 10;
    const btnW = 80;
    const btnH = 38;

    const btnGfx = this.add.graphics();
    btnGfx.fillStyle(0x7c4dff, 0.8);
    btnGfx.fillRoundedRect(btnX, btnY, btnW, btnH, 10);
    this.add.text(btnX + btnW / 2, btnY + btnH / 2, "NEW", {
      fontFamily: "Arial Black",
      fontSize: "14px",
      color: "#fff",
    }).setOrigin(0.5);

    const btnZone = this.add.rectangle(btnX + btnW / 2, btnY + btnH / 2, btnW, btnH)
      .setInteractive({ useHandCursor: true });
    btnZone.on("pointerdown", () => {
      this.scene.restart({ size: this.gridSize });
    });
  }

  createBackButton() {
    const y = this.gridY + this.gridPx + 30;
    const cx = this.scale.width / 2;
    const btnW = 160;
    const btnH = 44;

    const gfx = this.add.graphics();
    gfx.fillStyle(0x333355, 0.8);
    gfx.fillRoundedRect(cx - btnW / 2, y, btnW, btnH, 12);
    gfx.lineStyle(2, 0x7c4dff, 0.4);
    gfx.strokeRoundedRect(cx - btnW / 2, y, btnW, btnH, 12);

    this.add.text(cx, y + btnH / 2, "◀ MENU", {
      fontFamily: "Arial Black",
      fontSize: "16px",
      color: "#b39ddb",
    }).setOrigin(0.5);

    const zone = this.add.rectangle(cx, y + btnH / 2, btnW, btnH)
      .setInteractive({ useHandCursor: true });
    zone.on("pointerdown", () => {
      this.scene.start("SceneMenu");
    });
  }

  /* ---- Coordinate helpers ---- */
  cellAt(px, py) {
    const c = Math.floor((px - this.gridX) / this.cellSize);
    const r = Math.floor((py - this.gridY) / this.cellSize);
    if (r >= 0 && r < this.gridSize && c >= 0 && c < this.gridSize) {
      return { r, c };
    }
    return null;
  }

  cellRect(r, c) {
    return {
      x: this.gridX + c * this.cellSize,
      y: this.gridY + r * this.cellSize,
      w: this.cellSize,
      h: this.cellSize,
    };
  }

  /* ---- Input ---- */
  onPointerDown(pointer) {
    if (this.gameComplete) {
      // restart on tap after win
      this.scene.restart({ size: this.gridSize });
      return;
    }
    const cell = this.cellAt(pointer.x, pointer.y);
    if (!cell) return;
    // Don't start drag on already placed cells
    if (this.playerPlaced[cell.r][cell.c] >= 0) return;

    this.isDragging = true;
    this.dragStart = cell;
    this.dragEnd = cell;
    this.sound.tap();
  }

  onPointerMove(pointer) {
    if (!this.isDragging) return;
    const cell = this.cellAt(pointer.x, pointer.y);
    if (!cell) {
      // clamp to nearest edge
      const r = Math.max(0, Math.min(this.gridSize - 1,
        Math.floor((pointer.y - this.gridY) / this.cellSize)));
      const c = Math.max(0, Math.min(this.gridSize - 1,
        Math.floor((pointer.x - this.gridX) / this.cellSize)));
      this.dragEnd = { r, c };
    } else {
      this.dragEnd = cell;
    }
    this.drawDragRect();
  }

  onPointerUp() {
    if (!this.isDragging) return;
    this.isDragging = false;
    this.dragGfx.clear();

    if (!this.dragStart || !this.dragEnd) return;

    // Normalize rectangle
    const r1 = Math.min(this.dragStart.r, this.dragEnd.r);
    const r2 = Math.max(this.dragStart.r, this.dragEnd.r);
    const c1 = Math.min(this.dragStart.c, this.dragEnd.c);
    const c2 = Math.max(this.dragStart.c, this.dragEnd.c);
    const h = r2 - r1 + 1;
    const w = c2 - c1 + 1;
    const area = h * w;

    // Validate: all cells in rect must be unplaced
    const cells = [];
    for (let r = r1; r <= r2; r++) {
      for (let c = c1; c <= c2; c++) {
        if (this.playerPlaced[r][c] >= 0) return; // overlaps placed
        cells.push([r, c]);
      }
    }

    // Validate: exactly one number in the rect, and area matches
    let numberCount = 0;
    let foundNumber = 0;
    for (const [r, c] of cells) {
      if (this.puzzle[r][c] && this.puzzle[r][c].number) {
        numberCount++;
        foundNumber = this.puzzle[r][c].number;
      }
    }

    if (numberCount !== 1) return; // must contain exactly one number cell
    if (foundNumber !== area) return; // area must match number

    // Place the block!
    const blockId = this.nextColorIdx++;
    const color = BLOCK_COLORS[blockId % BLOCK_COLORS.length];
    this.playerBlockColors[blockId] = color;

    for (const [r, c] of cells) {
      this.playerPlaced[r][c] = blockId;
    }

    this.sound.place();
    this.drawBoard();
    this.checkWin();
  }

  /* ---- Drawing ---- */
  drawDragRect() {
    if (!this.dragStart || !this.dragEnd) return;
    this.dragGfx.clear();

    const r1 = Math.min(this.dragStart.r, this.dragEnd.r);
    const r2 = Math.max(this.dragStart.r, this.dragEnd.r);
    const c1 = Math.min(this.dragStart.c, this.dragEnd.c);
    const c2 = Math.max(this.dragStart.c, this.dragEnd.c);

    const x = this.gridX + c1 * this.cellSize;
    const y = this.gridY + r1 * this.cellSize;
    const w = (c2 - c1 + 1) * this.cellSize;
    const h = (r2 - r1 + 1) * this.cellSize;

    // Semi-transparent fill
    this.dragGfx.fillStyle(0x7c4dff, 0.3);
    this.dragGfx.fillRect(x, y, w, h);

    // Border
    this.dragGfx.lineStyle(2.5, 0xb39ddb, 0.9);
    this.dragGfx.strokeRect(x, y, w, h);

    // Area hint
    this.dragGfx.lineStyle(0);

    const area = (r2 - r1 + 1) * (c2 - c1 + 1);
    // Show area in center of selection (only if it fits the number condition)
    // Just show the area as feedback
  }

  drawBoard() {
    this.boardGfx.clear();

    // Draw placed blocks
    for (let r = 0; r < this.gridSize; r++) {
      for (let c = 0; c < this.gridSize; c++) {
        const blockId = this.playerPlaced[r][c];
        if (blockId >= 0) {
          const color = this.playerBlockColors[blockId];
          const rect = this.cellRect(r, c);
          this.boardGfx.fillStyle(color, 0.5);
          this.boardGfx.fillRect(rect.x + 2, rect.y + 2, rect.w - 4, rect.h - 4);

          // Draw border between different blocks
          // Right edge
          if (c + 1 >= this.gridSize || this.playerPlaced[r][c + 1] !== blockId) {
            this.boardGfx.lineStyle(2, color, 0.9);
            this.boardGfx.strokeRect(
              rect.x, rect.y,
              rect.w, rect.h
            );
          }
        }
      }
    }

    // Draw block group borders (thick outline around each placed block)
    const drawnBlocks = new Set();
    for (let r = 0; r < this.gridSize; r++) {
      for (let c = 0; c < this.gridSize; c++) {
        const blockId = this.playerPlaced[r][c];
        if (blockId < 0 || drawnBlocks.has(blockId)) continue;
        drawnBlocks.add(blockId);

        const color = this.playerBlockColors[blockId];
        // Find bounding box
        let minR = r, maxR = r, minC = c, maxC = c;
        for (let rr = 0; rr < this.gridSize; rr++) {
          for (let cc = 0; cc < this.gridSize; cc++) {
            if (this.playerPlaced[rr][cc] === blockId) {
              minR = Math.min(minR, rr);
              maxR = Math.max(maxR, rr);
              minC = Math.min(minC, cc);
              maxC = Math.max(maxC, cc);
            }
          }
        }
        const x = this.gridX + minC * this.cellSize;
        const y = this.gridY + minR * this.cellSize;
        const w = (maxC - minC + 1) * this.cellSize;
        const hBlock = (maxR - minR + 1) * this.cellSize;

        this.boardGfx.lineStyle(3.5, color, 1.0);
        this.boardGfx.strokeRect(x + 1, y + 1, w - 2, hBlock - 2);
      }
    }

    // Draw grid lines
    this.boardGfx.lineStyle(1.5, 0x3a3a5c, 0.6);
    for (let i = 0; i <= this.gridSize; i++) {
      const px = this.gridX + i * this.cellSize;
      this.boardGfx.moveTo(px, this.gridY);
      this.boardGfx.lineTo(px, this.gridY + this.gridPx);

      const py = this.gridY + i * this.cellSize;
      this.boardGfx.moveTo(this.gridX, py);
      this.boardGfx.lineTo(this.gridX + this.gridPx, py);
    }
    this.boardGfx.strokePath();
  }

  renderNumbers() {
    // Clear existing number texts
    for (const t of this.numberTexts) t.destroy();
    this.numberTexts = [];

    const fontSize = Math.floor(this.cellSize * 0.4);
    for (let r = 0; r < this.gridSize; r++) {
      for (let c = 0; c < this.gridSize; c++) {
        const cell = this.puzzle[r][c];
        if (cell && cell.number) {
          const rect = this.cellRect(r, c);
          const txt = this.add.text(
            rect.x + rect.w / 2,
            rect.y + rect.h / 2,
            String(cell.number),
            {
              fontFamily: "Arial Black",
              fontSize: `${fontSize}px`,
              color: "#ffffff",
              stroke: "#1a1a2e",
              strokeThickness: 3,
            }
          ).setOrigin(0.5).setDepth(20);
          this.numberTexts.push(txt);
        }
      }
    }
  }

  checkWin() {
    for (let r = 0; r < this.gridSize; r++) {
      for (let c = 0; c < this.gridSize; c++) {
        if (this.playerPlaced[r][c] < 0) return;
      }
    }
    // WIN!
    this.gameComplete = true;
    this.sound.win();

    // Overlay
    const overlay = this.add.graphics().setDepth(50);
    overlay.fillStyle(0x1a1a2e, 0.85);
    overlay.fillRect(0, 0, this.scale.width, this.scale.height);

    this.add.text(this.scale.width / 2, 280, "🎉 CLEAR!", {
      fontFamily: "Arial Black",
      fontSize: "40px",
      color: "#ffd700",
      stroke: "#7c4dff",
      strokeThickness: 8,
    }).setOrigin(0.5).setDepth(51);

    this.add.text(this.scale.width / 2, 350, "완벽하게 풀었습니다!", {
      fontFamily: "Arial, sans-serif",
      fontSize: "20px",
      color: "#b39ddb",
    }).setOrigin(0.5).setDepth(51);

    const prompt = this.add.text(this.scale.width / 2, 450, "터치하여 새 게임", {
      fontFamily: "Arial, sans-serif",
      fontSize: "16px",
      color: "#7e8aa2",
    }).setOrigin(0.5).setDepth(51);

    this.tweens.add({
      targets: prompt,
      alpha: 0.3,
      duration: 800,
      yoyo: true,
      repeat: -1,
    });
  }
}
