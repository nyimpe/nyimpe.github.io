import Phaser from "phaser";

// ──────────────────────────────────────────
// Sound Synthesizer (asset-free)
// ──────────────────────────────────────────
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
      // audio not supported
    }
  }
  playTone(freq, duration, type = "sine", volume = 0.04) {
    if (!this.ctx) return;
    try {
      if (this.ctx.state === "suspended") this.ctx.resume();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      gain.gain.setValueAtTime(volume, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + duration);
    } catch {
      // audio block
    }
  }
  playSwallow(sizeScale) {
    // Bigger object → lower pitch, longer sound
    const freq = 400 - sizeScale * 250;
    const dur = 0.06 + sizeScale * 0.1;
    this.playTone(Math.max(100, freq), dur, "sine", 0.05);
  }
  playGrow() {
    this.playTone(300, 0.08, "triangle", 0.03);
    setTimeout(() => this.playTone(500, 0.1, "triangle", 0.03), 50);
  }
  playTick() {
    this.playTone(800, 0.03, "square", 0.02);
  }
}

// ──────────────────────────────────────────
// Constants
// ──────────────────────────────────────────
const WORLD_W = 2400;
const WORLD_H = 1800;
const GAME_DURATION = 90; // seconds
const INITIAL_HOLE_RADIUS = 22;
const MAX_HOLE_RADIUS = 300;
const MOVE_SPEED = 280;
const GROWTH_FACTOR = 0.18;

// Object types for procedural generation
const OBJECT_TYPES = [
  // { name, shape, baseW, baseH, color, chance }
  { name: "small_rock", shape: "circle", baseW: 8, baseH: 8, color: 0x8d8d8d, chance: 0.25 },
  { name: "tree", shape: "circle", baseW: 16, baseH: 16, color: 0x2e7d32, chance: 0.20 },
  { name: "bush", shape: "circle", baseW: 12, baseH: 12, color: 0x43a047, chance: 0.15 },
  { name: "car", shape: "rect", baseW: 20, baseH: 14, color: 0xf44336, chance: 0.10 },
  { name: "small_building", shape: "rect", baseW: 36, baseH: 28, color: 0x90a4ae, chance: 0.12 },
  { name: "medium_building", shape: "rect", baseW: 52, baseH: 40, color: 0x78909c, chance: 0.08 },
  { name: "large_building", shape: "rect", baseW: 70, baseH: 56, color: 0x546e7a, chance: 0.05 },
  { name: "pool", shape: "circle", baseW: 30, baseH: 30, color: 0x1976d2, chance: 0.05 },
];

// ──────────────────────────────────────────
// Game Scene
// ──────────────────────────────────────────
export class Game extends Phaser.Scene {
  constructor() {
    super({ key: "Game" });
  }

  create() {
    const self = this;
    this.sfx = new SoundSynth();

    // ── State ──
    this.score = 0;
    this.holeRadius = INITIAL_HOLE_RADIUS;
    this.timeLeft = GAME_DURATION;
    this.gameOver = false;
    this.swallowing = new Set(); // objects currently being swallowed (tweening)

    // ── World bounds ──
    this.physics.world.setBounds(0, 0, WORLD_W, WORLD_H);

    // ── Draw world background ──
    this.drawWorld();

    // ── Hole (player) ──
    this.hole = this.createHole(INITIAL_HOLE_RADIUS);
    this.hole.x = WORLD_W / 2;
    this.hole.y = WORLD_H / 2;
    this.physics.add.existing(this.hole);
    this.hole.body.setCircle(INITIAL_HOLE_RADIUS);
    this.hole.body.setOffset(-INITIAL_HOLE_RADIUS, -INITIAL_HOLE_RADIUS);
    this.hole.body.setCollideWorldBounds(true);

    // ── Objects group ──
    this.objects = this.physics.add.group();

    // ── Overlap detection (hole vs objects) ──
    this.physics.add.overlap(this.hole, this.objects, this.onHoleOverlap, null, this);

    // ── Spawn objects ──
    this.spawnObjects();

    // ── Camera ──
    this.cameras.main.setBounds(0, 0, WORLD_W, WORLD_H);
    this.cameras.main.startFollow(this.hole, true, 0.08, 0.08);

    // ── Input ──
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = {
      up: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),
      down: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
      left: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
      right: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D),
    };

    // Touch/mouse movement target
    this.moveTarget = null;
    this.moveTargetGfx = this.add.graphics().setDepth(999).setAlpha(0);
    this.input.on("pointerdown", (pointer) => {
      // pointer.x/y are screen coords — need world coords for camera offset
      self.moveTarget = { x: pointer.worldX, y: pointer.worldY };
      self.moveTargetGfx.setAlpha(0.6);
      self.moveTargetGfx.clear();
      self.moveTargetGfx.lineStyle(2, 0xffffff, 0.8);
      self.moveTargetGfx.strokeCircle(pointer.worldX, pointer.worldY, 14);
      self.sfx.init(); // unlock audio
    });
    this.input.on("pointermove", (pointer) => {
      if (pointer.isDown) {
        self.moveTarget = { x: pointer.worldX, y: pointer.worldY };
        self.moveTargetGfx.clear();
        self.moveTargetGfx.lineStyle(2, 0xffffff, 0.8);
        self.moveTargetGfx.strokeCircle(pointer.worldX, pointer.worldY, 14);
      }
    });
    this.input.on("pointerup", () => {
      self.moveTarget = null;
      self.moveTargetGfx.setAlpha(0);
    });

    // ── UI (fixed to camera) ──
    this.uiScore = this.add.text(16, 16, "Score: 0", {
      fontFamily: "monospace",
      fontSize: "22px",
      color: "#ffffff",
      stroke: "#000000",
      strokeThickness: 3,
    }).setScrollFactor(0).setDepth(1000);

    this.uiSize = this.add.text(16, 46, "Size: ●●", {
      fontFamily: "monospace",
      fontSize: "16px",
      color: "#eeeeee",
      stroke: "#000000",
      strokeThickness: 2,
    }).setScrollFactor(0).setDepth(1000);

    this.uiTimer = this.add.text(960 - 16, 16, "1:30", {
      fontFamily: "monospace",
      fontSize: "24px",
      color: "#ffeb3b",
      stroke: "#000000",
      strokeThickness: 3,
    }).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);

    // End-game overlay (hidden)
    this.uiGameOver = this.add.text(480, 320, "", {
      fontFamily: "monospace",
      fontSize: "36px",
      color: "#ffffff",
      stroke: "#000000",
      strokeThickness: 4,
      align: "center",
    }).setOrigin(0.5).setScrollFactor(0).setDepth(2000).setAlpha(0);

    // ── Periodic tick sound for last 10 seconds ──
    this.lastTickTime = 0;
  }

  // ──────────────────────────────────────
  // WORLD RENDERING
  // ──────────────────────────────────────
  drawWorld() {
    const bg = this.add.graphics();
    // Base grass
    bg.fillStyle(0x5a8f3c, 1);
    bg.fillRect(0, 0, WORLD_W, WORLD_H);

    // Dirt patches for variety
    const patchCount = 60;
    for (let i = 0; i < patchCount; i++) {
      const x = Phaser.Math.Between(0, WORLD_W);
      const y = Phaser.Math.Between(0, WORLD_H);
      const r = Phaser.Math.Between(15, 50);
      const shade = Phaser.Math.Between(0, 2);
      const colors = [0x6b9b3a, 0x4a7a2e, 0x527a32];
      bg.fillStyle(colors[shade], 0.5);
      bg.fillCircle(x, y, r);
    }

    // Roads (horizontal and vertical lines)
    bg.fillStyle(0x555555, 1);
    const roadSpacing = 400;
    for (let x = roadSpacing; x < WORLD_W; x += roadSpacing) {
      bg.fillRect(x - 15, 0, 30, WORLD_H);
    }
    for (let y = roadSpacing; y < WORLD_H; y += roadSpacing) {
      bg.fillRect(0, y - 15, WORLD_W, 30);
    }

    // Road dashes (center lines)
    bg.fillStyle(0xcccc44, 0.8);
    for (let x = roadSpacing; x < WORLD_W; x += roadSpacing) {
      for (let y = 0; y < WORLD_H; y += 60) {
        bg.fillRect(x - 2, y, 4, 30);
      }
    }
    for (let y = roadSpacing; y < WORLD_H; y += roadSpacing) {
      for (let x = 0; x < WORLD_W; x += 60) {
        bg.fillRect(x, y - 2, 30, 4);
      }
    }

    bg.setDepth(-10);
  }

  // ──────────────────────────────────────
  // HOLE
  // ──────────────────────────────────────
  createHole(radius) {
    const g = this.add.graphics();
    this.drawHoleGraphic(g, radius);
    g.setDepth(10);
    // Store radius on the object for collision sizing
    g.holeRadius = radius;
    return g;
  }

  drawHoleGraphic(g, radius) {
    g.clear();
    // Dark outer ring (shadow)
    g.fillStyle(0x000000, 0.3);
    g.fillCircle(0, 0, radius + 3);
    // Main black hole
    g.fillStyle(0x0a0a0a, 1);
    g.fillCircle(0, 0, radius);
    // Dark purple inner glow for depth effect
    g.fillStyle(0x1a0a2e, 0.6);
    g.fillCircle(0, 0, radius * 0.85);
    // Deepest point
    g.fillStyle(0x000000, 0.9);
    g.fillCircle(0, 0, radius * 0.5);
    // Swirl edge (subtle gradient ring)
    g.lineStyle(2, 0x333355, 0.4);
    g.strokeCircle(0, 0, radius * 0.9);
    // Highlight edge
    g.lineStyle(1, 0x444477, 0.3);
    g.strokeCircle(0, 0, radius);
  }

  resizeHole(newRadius) {
    const clamped = Math.min(newRadius, MAX_HOLE_RADIUS);
    if (clamped === this.holeRadius) return;

    this.holeRadius = clamped;
    this.hole.holeRadius = clamped;
    this.drawHoleGraphic(this.hole, clamped);

    // Update physics body
    this.hole.body.setCircle(clamped);
    this.hole.body.setOffset(-clamped, -clamped);

    // Size UI
    const dots = Math.min(10, Math.max(1, Math.floor((clamped - INITIAL_HOLE_RADIUS) / 15) + 1));
    this.uiSize.setText("Size: " + "●".repeat(dots));
  }

  // ──────────────────────────────────────
  // OBJECT SPAWNING
  // ──────────────────────────────────────
  spawnObjects() {
    const totalObjects = 180;

    for (let i = 0; i < totalObjects; i++) {
      // Pick random type weighted by chance
      const roll = Math.random();
      let cumulative = 0;
      let chosenType = OBJECT_TYPES[0];
      for (const t of OBJECT_TYPES) {
        cumulative += t.chance;
        if (roll <= cumulative) {
          chosenType = t;
          break;
        }
      }

      // Random size variation
      const sizeMult = 0.7 + Math.random() * 0.6;
      const objW = Math.round(chosenType.baseW * sizeMult);
      const objH = Math.round(chosenType.baseH * sizeMult);

      // Avoid spawning on roads and on top of each other (simple approach: random placement)
      const g = this.add.graphics();
      const x = Phaser.Math.Between(40, WORLD_W - 40);
      const y = Phaser.Math.Between(40, WORLD_H - 40);

      g.objSize = Math.max(objW, objH); // Size metric for swallowing check
      g.objColor = chosenType.color;

      if (chosenType.shape === "circle") {
        this.drawCircleObject(g, objW / 2, chosenType.color);
      } else {
        this.drawRectObject(g, objW, objH, chosenType.color);
      }

      g.setPosition(x, y);
      g.setDepth(1);

      this.physics.add.existing(g);
      g.body.setSize(objW, objH);
      g.body.setOffset(-objW / 2, -objH / 2);
      g.body.setImmovable(true);
      g.body.setAllowGravity(false);
      this.objects.add(g);
    }
  }

  drawCircleObject(g, radius, color) {
    g.clear();
    const r = Math.round(radius);
    // Shadow
    g.fillStyle(0x000000, 0.15);
    g.fillCircle(1, 1, r);
    // Main
    g.fillStyle(color, 1);
    g.fillCircle(0, 0, r);
    // Highlight
    g.fillStyle(0xffffff, 0.2);
    g.fillCircle(-r * 0.25, -r * 0.25, r * 0.35);
    // Border
    g.lineStyle(1, Phaser.Display.Color.GetColor(
      Phaser.Display.Color.IntegerToColor(color).darken(20).color
    ), 0.6);
    g.strokeCircle(0, 0, r);
  }

  drawRectObject(g, w, h, color) {
    g.clear();
    const halfW = Math.round(w / 2);
    const halfH = Math.round(h / 2);
    // Shadow
    g.fillStyle(0x000000, 0.15);
    g.fillRect(-halfW + 2, -halfH + 2, w, h);
    // Main body
    g.fillStyle(color, 1);
    g.fillRect(-halfW, -halfH, w, h);
    // Top edge highlight
    g.fillStyle(0xffffff, 0.25);
    g.fillRect(-halfW + 1, -halfH + 1, w - 2, 3);
    // Left edge highlight
    g.fillStyle(0xffffff, 0.1);
    g.fillRect(-halfW + 1, -halfH + 1, 3, h - 2);
    // Bottom shadow
    g.fillStyle(0x000000, 0.2);
    g.fillRect(-halfW + 1, halfH - 4, w - 2, 3);
    // Border
    g.lineStyle(1, 0x000000, 0.3);
    g.strokeRect(-halfW, -halfH, w, h);

    // For buildings: add windows
    if (w >= 36 && h >= 28) {
      g.fillStyle(0xfdd835, 0.6);
      const cols = Math.max(2, Math.floor(w / 18));
      const rows = Math.max(2, Math.floor(h / 18));
      const cellW = (w - 12) / cols;
      const cellH = (h - 12) / rows;
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          if (Math.random() > 0.3) {
            const wx = -halfW + 8 + c * cellW + cellW / 2;
            const wy = -halfH + 10 + r * cellH + cellH / 2;
            g.fillRect(wx - cellW * 0.25, wy - cellH * 0.3, cellW * 0.5, cellH * 0.6);
          }
        }
      }
    }

    // For cars: add windows
    if (w <= 24 && h <= 18 && w >= 16) {
      g.fillStyle(0xbbdefb, 0.7);
      g.fillRect(-halfW + 5, -halfH + 2, w - 10, h - 6);
    }
  }

  // ──────────────────────────────────────
  // SWALLOW MECHANIC
  // ──────────────────────────────────────
  onHoleOverlap(hole, obj) {
    const self = this;
    // Skip if already swallowing this object
    if (self.swallowing.has(obj)) return;
    // Only swallow if hole is bigger than object
    if (hole.holeRadius < obj.objSize * 0.85) return;

    self.swallowing.add(obj);

    // Remove physics body to stop further overlaps
    obj.body.enable = false;

    // Calculate size scale for sound
    const sizeScale = Math.min(1, obj.objSize / 100);

    // Play swallow sound
    self.sfx.playSwallow(sizeScale);

    // Suck animation: shrink and move toward hole center
    self.tweens.add({
      targets: obj,
      x: hole.x,
      y: hole.y,
      scaleX: 0.05,
      scaleY: 0.05,
      alpha: 0,
      duration: 180 + sizeScale * 150,
      ease: "Quad.easeIn",
      onComplete: () => {
        // Increase score
        const points = Math.max(1, Math.round(obj.objSize));
        self.score += points;
        self.uiScore.setText(`Score: ${self.score}`);

        // Grow the hole
        const growth = obj.objSize * GROWTH_FACTOR;
        self.resizeHole(self.holeRadius + growth);

        // Remove object
        obj.destroy();
        self.swallowing.delete(obj);

        // Occasional growth sound for big objects
        if (sizeScale > 0.5) {
          self.sfx.playGrow();
        }
      },
    });
  }

  // ──────────────────────────────────────
  // END GAME
  // ──────────────────────────────────────
  endGame() {
    if (this.gameOver) return;
    this.gameOver = true;

    // Freeze the hole
    this.hole.body.setVelocity(0, 0);

    // Show game over overlay
    const self = this;
    this.uiGameOver.setText(`Game Over!\nFinal Score: ${this.score}\n\nTap to Restart`);
    this.uiGameOver.setAlpha(1);

    // Darken screen
    this.cameras.main.fade(400, 0, 0, 0);

    // Restart on click/tap
    this.time.delayedCall(500, () => {
      self.input.once("pointerdown", () => {
        self.scene.restart();
      });
    });
  }

  // ──────────────────────────────────────
  // UPDATE LOOP
  // ──────────────────────────────────────
  update(time, delta) {
    if (this.gameOver) return;

    // ── Timer ──
    this.timeLeft -= delta / 1000;
    if (this.timeLeft <= 0) {
      this.timeLeft = 0;
      this.endGame();
      return;
    }

    const totalSec = Math.ceil(this.timeLeft);
    const min = Math.floor(totalSec / 60);
    const sec = totalSec % 60;
    this.uiTimer.setText(`${min}:${String(sec).padStart(2, "0")}`);

    // Timer color change in last 15 seconds
    if (this.timeLeft <= 15) {
      this.uiTimer.setColor("#ff1744");
      // Tick sound in last 10
      if (this.timeLeft <= 10 && time - this.lastTickTime > 1000) {
        this.sfx.playTick();
        this.lastTickTime = time;
      }
    }

    // ── Player movement ──
    let vx = 0;
    let vy = 0;

    // Keyboard
    if (this.cursors.left.isDown || this.wasd.left.isDown) vx = -1;
    if (this.cursors.right.isDown || this.wasd.right.isDown) vx = 1;
    if (this.cursors.up.isDown || this.wasd.up.isDown) vy = -1;
    if (this.cursors.down.isDown || this.wasd.down.isDown) vy = 1;

    // Touch/mouse (only if no keyboard input)
    if (vx === 0 && vy === 0 && this.moveTarget) {
      const dx = this.moveTarget.x - this.hole.x;
      const dy = this.moveTarget.y - this.hole.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > 8) {
        vx = dx / dist;
        vy = dy / dist;
      } else {
        this.moveTarget = null;
        this.moveTargetGfx.setAlpha(0);
      }
    }

    // Normalize diagonal movement
    if (vx !== 0 && vy !== 0) {
      const norm = 1 / Math.SQRT2;
      vx *= norm;
      vy *= norm;
    }

    // Speed decreases as hole grows (bigger = slower)
    const speedPenalty = 1 - Math.min(0.5, (this.holeRadius - INITIAL_HOLE_RADIUS) / (MAX_HOLE_RADIUS - INITIAL_HOLE_RADIUS) * 0.5);
    const currentSpeed = MOVE_SPEED * speedPenalty;

    this.hole.body.setVelocity(vx * currentSpeed, vy * currentSpeed);
  }
}
