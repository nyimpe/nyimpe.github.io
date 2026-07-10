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
  playHit() { this.playTone(200, 0.05, "square", 0.03); }
  playKill() { this.playTone(400, 0.06, "triangle", 0.04); }
  playShoot() { this.playTone(600, 0.04, "sine", 0.02); }
  playLevelUp() {
    this.playTone(523, 0.10, "sine", 0.03);
    setTimeout(() => this.playTone(659, 0.10, "sine", 0.03), 60);
    setTimeout(() => this.playTone(783, 0.15, "sine", 0.04), 120);
  }
}

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
    this.killCount = 0;
    this.gameTime = 0;
    this.level = 1;
    this.xpToNext = 10;
    this.xpCurrent = 0;
    this.fireRate = 400;   // ms between shots
    this.lastFireTime = 0;
    this.moveSpeed = 220;
    this.projectileSpeed = 400;
    this.projectileDamage = 1;
    this.spawnInterval = 1200; // ms
    this.lastSpawnTime = 0;
    this.enemyBaseHp = 3;
    this.enemySpeed = 80;
    this.gameOver = false;

    // ── World bounds ──
    this.physics.world.setBounds(0, 0, 960, 640);

    // ── Player (procedural circle) ──
    this.player = this.add.graphics();
    this.drawPlayer();
    this.physics.add.existing(this.player);
    this.player.body.setSize(24, 24);
    this.player.body.setOffset(-12, -12);
    this.player.body.setCollideWorldBounds(true);

    // ── Groups ──
    this.enemies = this.physics.add.group();
    this.projectiles = this.physics.add.group();
    this.xpGems = this.physics.add.group();

    // ── Collisions ──
    this.physics.add.overlap(this.player, this.enemies, this.onPlayerHit, null, this);
    this.physics.add.overlap(this.projectiles, this.enemies, this.onProjectileHit, null, this);
    this.physics.add.overlap(this.player, this.xpGems, this.onCollectXp, null, this);

    // ── Input ──
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd = {
      up: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),
      down: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
      left: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
      right: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D),
    };

    // ── UI ──
    this.uiKills = this.add.text(16, 16, "Kills: 0", {
      fontFamily: "monospace",
      fontSize: "20px",
      color: "#fff",
    }).setScrollFactor(0).setDepth(100);

    this.uiLevel = this.add.text(16, 42, "Lv.1", {
      fontFamily: "monospace",
      fontSize: "18px",
      color: "#ffdd57",
    }).setScrollFactor(0).setDepth(100);

    this.uiXpBarBg = this.add.graphics().setScrollFactor(0).setDepth(99);
    this.uiXpBarFg = this.add.graphics().setScrollFactor(0).setDepth(100);

    this.uiTimer = this.add.text(960 - 16, 16, "0:00", {
      fontFamily: "monospace",
      fontSize: "20px",
      color: "#aaa",
    }).setOrigin(1, 0).setScrollFactor(0).setDepth(100);

    // ── Spawn initial enemies ──
    for (let i = 0; i < 6; i++) {
      this.spawnEnemy();
    }

    // Initial audio resume on first interaction
    this.input.once("pointerdown", () => {
      self.sfx.init();
    });
  }

  // ──────────────────────────────────────
  // DRAWING
  // ──────────────────────────────────────
  drawPlayer() {
    const g = this.player;
    g.clear();
    // Body (blue circle)
    g.fillStyle(0x4fc3f7, 1);
    g.fillCircle(0, 0, 14);
    // Border
    g.lineStyle(2, 0x0288d1, 1);
    g.strokeCircle(0, 0, 14);
    // Inner highlight
    g.fillStyle(0xb3e5fc, 0.4);
    g.fillCircle(-3, -3, 6);
  }

  drawEnemy(g, hp, maxHp) {
    g.clear();
    const color = 0xe53935;
    const pct = hp / maxHp;
    const radius = 10 + (1 - pct) * 2; // smaller when damaged
    g.fillStyle(color, 0.7 + pct * 0.3);
    g.fillCircle(0, 0, radius);
    g.lineStyle(2, 0xab000d, 1);
    g.strokeCircle(0, 0, radius);
    // Eyes
    g.fillStyle(0xffffff, 1);
    g.fillCircle(-4, -3, 3);
    g.fillCircle(4, -3, 3);
    g.fillStyle(0x000000, 1);
    g.fillCircle(-4, -2, 1.5);
    g.fillCircle(4, -2, 1.5);
  }

  drawProjectile(g) {
    g.clear();
    g.fillStyle(0xffeb3b, 1);
    g.fillCircle(0, 0, 4);
    g.lineStyle(1, 0xf9a825, 1);
    g.strokeCircle(0, 0, 4);
  }

  drawXpGem(g) {
    g.clear();
    g.fillStyle(0x66bb6a, 1);
    // Diamond shape
    g.fillRect(-3, -3, 6, 6);
    g.fillStyle(0xa5d6a7, 0.5);
    g.fillRect(-1, -1, 2, 2);
  }

  // ──────────────────────────────────────
  // SPAWNING
  // ──────────────────────────────────────
  spawnEnemy() {
    // Spawn from edges, outside view
    const side = Phaser.Math.Between(0, 3);
    let x, y;
    const margin = 30;
    switch (side) {
      case 0: x = Phaser.Math.Between(0, 960); y = -margin; break;     // top
      case 1: x = Phaser.Math.Between(0, 960); y = 640 + margin; break; // bottom
      case 2: x = -margin; y = Phaser.Math.Between(0, 640); break;      // left
      case 3: x = 960 + margin; y = Phaser.Math.Between(0, 640); break; // right
    }

    const g = this.add.graphics();
    const maxHp = this.enemyBaseHp + Math.floor(this.level / 3);
    const hp = maxHp;
    g.enemyHp = hp;
    g.enemyMaxHp = maxHp;
    this.drawEnemy(g, hp, maxHp);
    g.setPosition(x, y);

    this.physics.add.existing(g);
    g.body.setSize(20, 20);
    g.body.setOffset(-10, -10);
    this.enemies.add(g);
  }

  // ──────────────────────────────────────
  // COMBAT
  // ──────────────────────────────────────
  fireProjectile() {
    const self = this;
    if (this.enemies.getLength() === 0) return;

    // Find nearest enemy
    let nearest = null;
    let nearestDist = Infinity;
    const px = this.player.x;
    const py = this.player.y;

    this.enemies.getChildren().forEach((e) => {
      const dx = e.x - px;
      const dy = e.y - py;
      const dist = dx * dx + dy * dy;
      if (dist < nearestDist) {
        nearestDist = dist;
        nearest = e;
      }
    });

    if (!nearest) return;

    const angle = Phaser.Math.Angle.Between(px, py, nearest.x, nearest.y);
    const g = this.add.graphics();
    this.drawProjectile(g);
    g.setPosition(px, py);

    this.physics.add.existing(g);
    g.body.setSize(8, 8);
    g.body.setOffset(-4, -4);
    g.body.enemyTarget = nearest; // track target for homing-optional
    this.projectiles.add(g);

    this.physics.moveTo(g, nearest.x, nearest.y, this.projectileSpeed);
    this.sfx.playShoot();
  }

  onProjectileHit(proj, enemy) {
    // Remove projectile
    proj.destroy();
    // Damage enemy
    enemy.enemyHp -= this.projectileDamage;
    if (enemy.enemyHp <= 0) {
      this.killEnemy(enemy);
    } else {
      this.drawEnemy(enemy, enemy.enemyHp, enemy.enemyMaxHp);
    }
  }

  killEnemy(enemy) {
    // Drop XP gem
    const gem = this.add.graphics();
    this.drawXpGem(gem);
    gem.setPosition(enemy.x, enemy.y);
    this.physics.add.existing(gem);
    gem.body.setSize(10, 10);
    gem.body.setOffset(-5, -5);
    this.xpGems.add(gem);

    // Remove enemy
    enemy.destroy();

    this.killCount++;
    this.uiKills.setText(`Kills: ${this.killCount}`);
    this.sfx.playKill();

    // XP gain
    this.xpCurrent++;
    if (this.xpCurrent >= this.xpToNext) {
      this.levelUp();
    }
  }

  onPlayerHit(player, enemy) {
    enemy.destroy();
    this.sfx.playHit();
    // Flash player red
    this.drawPlayerDamaged();
    this.time.delayedCall(150, () => {
      if (!this.gameOver) this.drawPlayer();
    });
  }

  drawPlayerDamaged() {
    const g = this.player;
    g.clear();
    g.fillStyle(0xff1744, 1);
    g.fillCircle(0, 0, 14);
    g.lineStyle(2, 0xffffff, 1);
    g.strokeCircle(0, 0, 14);
  }

  onCollectXp(player, gem) {
    gem.destroy();
  }

  levelUp() {
    this.level++;
    this.xpCurrent = 0;
    this.xpToNext = Math.floor(this.xpToNext * 1.4);
    this.fireRate = Math.max(100, this.fireRate - 15);
    this.projectileDamage++;
    this.moveSpeed += 8;
    this.spawnInterval = Math.max(400, this.spawnInterval - 80);
    this.enemySpeed += 6;

    this.uiLevel.setText(`Lv.${this.level}`);
    this.sfx.playLevelUp();

    // Flash screen
    this.cameras.main.flash(300, 255, 221, 87);
  }

  // ──────────────────────────────────────
  // UPDATE LOOP
  // ──────────────────────────────────────
  update(time, delta) {
    if (this.gameOver) return;

    this.gameTime += delta;

    // ── Timer ──
    const totalSec = Math.floor(this.gameTime / 1000);
    const min = Math.floor(totalSec / 60);
    const sec = totalSec % 60;
    this.uiTimer.setText(`${min}:${String(sec).padStart(2, "0")}`);

    // ── XP Bar ──
    this.drawXpBar();

    // ── Player movement ──
    let vx = 0;
    let vy = 0;
    if (this.cursors.left.isDown || this.wasd.left.isDown) vx = -1;
    if (this.cursors.right.isDown || this.wasd.right.isDown) vx = 1;
    if (this.cursors.up.isDown || this.wasd.up.isDown) vy = -1;
    if (this.cursors.down.isDown || this.wasd.down.isDown) vy = 1;

    // Normalize diagonal
    if (vx !== 0 && vy !== 0) {
      const norm = 1 / Math.SQRT2;
      vx *= norm;
      vy *= norm;
    }

    this.player.body.setVelocity(vx * this.moveSpeed, vy * this.moveSpeed);

    // ── Fire projectile ──
    if (time - this.lastFireTime > this.fireRate) {
      this.fireProjectile();
      this.lastFireTime = time;
    }

    // ── Spawn enemies ──
    if (time - this.lastSpawnTime > this.spawnInterval) {
      this.spawnEnemy();
      this.lastSpawnTime = time;
      // Occasional double spawn
      if (Math.random() < 0.3) this.spawnEnemy();
    }

    // ── Move enemies toward player ──
    this.enemies.getChildren().forEach((e) => {
      this.physics.moveToObject(e, this.player, this.enemySpeed);
    });

    // ── Move XP gems slowly toward player ──
    this.xpGems.getChildren().forEach((gem) => {
      const dx = this.player.x - gem.x;
      const dy = this.player.y - gem.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 150 && dist > 1) {
        gem.x += (dx / dist) * 100 * (delta / 1000);
        gem.y += (dy / dist) * 100 * (delta / 1000);
      }
    });

    // ── Clean up off-screen projectiles ──
    this.projectiles.getChildren().forEach((p) => {
      if (p.x < -50 || p.x > 1010 || p.y < -50 || p.y > 690) {
        p.destroy();
      }
    });
  }

  drawXpBar() {
    const self = this;
    const barX = 16;
    const barY = 68;
    const barW = 200;
    const barH = 10;

    this.uiXpBarBg.clear();
    this.uiXpBarBg.fillStyle(0x333333, 0.8);
    this.uiXpBarBg.fillRect(barX, barY, barW, barH);

    this.uiXpBarFg.clear();
    const pct = Math.min(1, this.xpCurrent / this.xpToNext);
    this.uiXpBarFg.fillStyle(0x66bb6a, 1);
    this.uiXpBarFg.fillRect(barX, barY, barW * pct, barH);
  }
}
