import Phaser from "phaser";

// ===== Puzzle Generator =====
function generatePuzzle(size) {
  const visited = Array.from({ length: size }, () => Array(size).fill(false));
  const blocks = [];
  for (let limit = 0; limit < 500; limit++) {
    let sr = -1, sc = -1;
    for (let r = 0; r < size && sr < 0; r++)
      for (let c = 0; c < size && sr < 0; c++)
        if (!visited[r][c]) { sr = r; sc = c; }
    if (sr < 0) break;
    const cands = [];
    for (let h = 1; h <= size - sr; h++) {
      for (let w = 1; w <= size - sc; w++) {
        let ok = true;
        const cells = [];
        for (let dr = 0; dr < h && ok; dr++)
          for (let dc = 0; dc < w && ok; dc++) {
            if (visited[sr + dr][sc + dc]) { ok = false; }
            else cells.push([sr + dr, sc + dc]);
          }
        if (ok) cands.push({ cells, area: h * w });
      }
    }
    if (!cands.length) return generatePuzzle(size);
    const pick = cands[Math.floor(Math.random() * cands.length)];
    for (const [r, c] of pick.cells) visited[r][c] = true;
    const np = pick.cells[Math.floor(Math.random() * pick.cells.length)];
    blocks.push({ cells: pick.cells, area: pick.area, nr: np[0], nc: np[1] });
  }
  const grid = Array.from({ length: size }, () => Array(size).fill(null));
  for (const b of blocks) grid[b.nr][b.nc] = { n: b.area };
  return grid;
}

const COLORS = [0x7c4dff, 0x4caf50, 0xff9800, 0xe91e63, 0x00bcd4, 0xffeb3b, 0x9c27b0, 0x607d8b];
const SIZE = 7;

// ===== Main Scene =====
class ShikakuScene extends Phaser.Scene {
  constructor() {
    super("ShikakuScene");
  }

  create() {
    this.cameras.main.setBackgroundColor("#1a1a2e");
    const self = this;

    const CELL = 50;
    const GRID_PX = SIZE * CELL;
    const GX = Math.floor((430 - GRID_PX) / 2);
    const GY = 200;

    const puzzle = generatePuzzle(SIZE);
    const placed = Array.from({ length: SIZE }, () => Array(SIZE).fill(-1));
    const blockColors = {};
    let colorIdx = 0;
    let dragging = false, dragStart = null, dragEnd = null;
    let finished = false;

    const gfx = this.add.graphics();
    const dragGfx = this.add.graphics().setDepth(10);
    const numTexts = [];

    function cellAt(px, py) {
      const c = Math.floor((px - GX) / CELL);
      const r = Math.floor((py - GY) / CELL);
      return (r >= 0 && r < SIZE && c >= 0 && c < SIZE) ? { r, c } : null;
    }

    function drawBoard() {
      gfx.clear();
      const drawn = new Set();
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          const bid = placed[r][c];
          if (bid < 0) continue;
          const x = GX + c * CELL, y = GY + r * CELL;
          gfx.fillStyle(blockColors[bid], 0.45);
          gfx.fillRect(x + 1, y + 1, CELL - 2, CELL - 2);
          if (!drawn.has(bid)) {
            drawn.add(bid);
            let mr = r, Mr = r, mc = c, Mc = c;
            for (let rr = 0; rr < SIZE; rr++)
              for (let cc = 0; cc < SIZE; cc++)
                if (placed[rr][cc] === bid) {
                  mr = Math.min(mr, rr); Mr = Math.max(Mr, rr);
                  mc = Math.min(mc, cc); Mc = Math.max(Mc, cc);
                }
            gfx.lineStyle(3, blockColors[bid], 1);
            gfx.strokeRect(GX + mc * CELL + 1, GY + mr * CELL + 1,
              (Mc - mc + 1) * CELL - 2, (Mr - mr + 1) * CELL - 2);
          }
        }
      }
      gfx.lineStyle(1.5, 0x3a3a5c, 0.6);
      for (let i = 0; i <= SIZE; i++) {
        gfx.beginPath();
        gfx.moveTo(GX + i * CELL, GY);
        gfx.lineTo(GX + i * CELL, GY + GRID_PX);
        gfx.strokePath();
        gfx.beginPath();
        gfx.moveTo(GX, GY + i * CELL);
        gfx.lineTo(GX + GRID_PX, GY + i * CELL);
        gfx.strokePath();
      }
    }

    function drawNumbers() {
      for (const t of numTexts) t.destroy();
      numTexts.length = 0;
      const fs = Math.floor(CELL * 0.4);
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          if (puzzle[r][c]) {
            const x = GX + c * CELL + CELL / 2;
            const y = GY + r * CELL + CELL / 2;
            const t = self.add.text(x, y, String(puzzle[r][c].n), {
              fontFamily: "Arial Black", fontSize: `${fs}px`,
              color: "#fff", stroke: "#1a1a2e", strokeThickness: 3,
            }).setOrigin(0.5).setDepth(20);
            numTexts.push(t);
          }
        }
      }
    }

    function checkWin() {
      for (let r = 0; r < SIZE; r++)
        for (let c = 0; c < SIZE; c++)
          if (placed[r][c] < 0) return;
      finished = true;
      const ov = self.add.graphics().setDepth(50);
      ov.fillStyle(0x1a1a2e, 0.85);
      ov.fillRect(0, 0, 430, 932);
      self.add.text(215, 300, "🎉 CLEAR!", {
        fontFamily: "Arial Black", fontSize: "40px", color: "#ffd700",
        stroke: "#7c4dff", strokeThickness: 8,
      }).setOrigin(0.5).setDepth(51);
      const p = self.add.text(215, 380, "탭하여 새 게임", {
        fontFamily: "Arial", fontSize: "18px", color: "#b39ddb",
      }).setOrigin(0.5).setDepth(51);
      self.tweens.add({ targets: p, alpha: 0.3, duration: 800, yoyo: true, repeat: -1 });
    }

    // Header
    this.add.text(10, 10, "◧ SHIKAKU 7×7", {
      fontFamily: "Arial Black", fontSize: "18px", color: "#7c4dff",
    });

    // New game button
    const bx = 340, by = 8, bw = 82, bh = 38;
    const bg = this.add.graphics();
    bg.fillStyle(0x7c4dff, 0.8);
    bg.fillRoundedRect(bx, by, bw, bh, 10);
    this.add.text(bx + bw / 2, by + bh / 2, "NEW", {
      fontFamily: "Arial Black", fontSize: "14px", color: "#fff",
    }).setOrigin(0.5);
    this.add.rectangle(bx + bw / 2, by + bh / 2, bw, bh)
      .setInteractive({ useHandCursor: true })
      .on("pointerdown", () => this.scene.restart());

    // Big NEW GAME
    const bby = GY + GRID_PX + 40;
    const bg2 = this.add.graphics();
    bg2.fillStyle(0x7c4dff, 0.8);
    bg2.fillRoundedRect(135, bby, 160, 44, 12);
    this.add.text(215, bby + 22, "🔄 NEW GAME", {
      fontFamily: "Arial Black", fontSize: "16px", color: "#fff",
    }).setOrigin(0.5);
    this.add.rectangle(215, bby + 22, 160, 44)
      .setInteractive({ useHandCursor: true })
      .on("pointerdown", () => this.scene.restart());

    // Input
    this.input.on("pointerdown", (ptr) => {
      if (finished) { this.scene.restart(); return; }
      const c = cellAt(ptr.x, ptr.y);
      if (!c || placed[c.r][c.c] >= 0) return;
      dragging = true; dragStart = c; dragEnd = c;
    });
    this.input.on("pointermove", (ptr) => {
      if (!dragging) return;
      let c = cellAt(ptr.x, ptr.y);
      if (!c) {
        c = {
          r: Phaser.Math.Clamp(Math.floor((ptr.y - GY) / CELL), 0, SIZE - 1),
          c: Phaser.Math.Clamp(Math.floor((ptr.x - GX) / CELL), 0, SIZE - 1),
        };
      }
      dragEnd = c;
      dragGfx.clear();
      const r1 = Math.min(dragStart.r, c.r), r2 = Math.max(dragStart.r, c.r);
      const c1 = Math.min(dragStart.c, c.c), c2 = Math.max(dragStart.c, c.c);
      const x = GX + c1 * CELL, y = GY + r1 * CELL;
      const w = (c2 - c1 + 1) * CELL, h = (r2 - r1 + 1) * CELL;
      dragGfx.fillStyle(0x7c4dff, 0.3);
      dragGfx.fillRect(x, y, w, h);
      dragGfx.lineStyle(2.5, 0xb39ddb, 0.9);
      dragGfx.strokeRect(x, y, w, h);
    });
    this.input.on("pointerup", () => {
      if (!dragging) return;
      dragging = false;
      dragGfx.clear();
      if (!dragStart || !dragEnd) return;
      const r1 = Math.min(dragStart.r, dragEnd.r), r2 = Math.max(dragStart.r, dragEnd.r);
      const c1 = Math.min(dragStart.c, dragEnd.c), c2 = Math.max(dragStart.c, dragEnd.c);
      const area = (r2 - r1 + 1) * (c2 - c1 + 1);
      for (let r = r1; r <= r2; r++)
        for (let c = c1; c <= c2; c++)
          if (placed[r][c] >= 0) return;
      let cnt = 0, val = 0;
      for (let r = r1; r <= r2; r++)
        for (let c = c1; c <= c2; c++)
          if (puzzle[r][c]) { cnt++; val = puzzle[r][c].n; }
      if (cnt !== 1 || val !== area) return;
      const bid = colorIdx++;
      blockColors[bid] = COLORS[bid % COLORS.length];
      for (let r = r1; r <= r2; r++)
        for (let c = c1; c <= c2; c++)
          placed[r][c] = bid;
      drawBoard();
      checkWin();
    });

    drawBoard();
    drawNumbers();
  }
}

// ===== Phaser Config =====
const config = {
  type: Phaser.AUTO,
  title: "Shikaku",
  parent: "game-container",
  width: 430,
  height: 932,
  backgroundColor: "#1a1a2e",
  scene: [ShikakuScene],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
