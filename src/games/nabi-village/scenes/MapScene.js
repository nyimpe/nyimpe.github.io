import Phaser from "phaser";
import { ELITES, GROUPS, RELICS, YOKAI } from "../data.js";
import { newRun, reachable, gainXp } from "../run.js";
import { C, box, button, floatText, modal, muteToggle, music, sfx, text } from "../ui.js";

const ICON = { start: "nabi-face", fight: "dog-face", elite: "spirit-face", rest: "onigiri", treasure: "chest", boss: "boss-face" };
const LABEL = { fight: "잡요괴", elite: "이름난 요괴", rest: "쉬는 칸", treasure: "보물", boss: "우두머리" };

export class MapScene extends Phaser.Scene {
  constructor() {
    super("Map");
  }

  create(data = {}) {
    if (data.fresh || !this.registry.get("run")) this.registry.set("run", newRun());
    this.run = this.registry.get("run");
    this.leaving = false;
    music(this, "village");
    this.add.image(0, 0, "bg-map").setOrigin(0).setScale(3);
    this.drawHud();
    this.drawMap();
    this.drawPanel();
    if (data.toast) floatText(this, 330, 300, data.toast, "#fff3dc", 26);
    if (!this.run.started) this.intro();
  }

  drawHud() {
    const r = this.run;
    this.add.rectangle(0, 0, 960, 40, C.ink, 0.85).setOrigin(0);
    text(this, 16, 20, "마을 · 갈림길 지도", 20, C.creamText, { fontStyle: "bold" }).setOrigin(0, 0.5);
    text(this, 480, 20, `나비 체력 ${r.hp}/${r.maxHp} · 레벨 ${r.level} (${r.xp}/10)`, 20, C.creamText).setOrigin(0.5);
    this.add.image(800, 20, "coin").setScale(3);
    text(this, 816, 20, `${r.coins}`, 20, C.creamText).setOrigin(0, 0.5);
    muteToggle(this, 948, 20);
  }

  nodeKey(n) {
    return `${n.r}:${n.i}`;
  }

  drawMap() {
    const r = this.run;
    const { rows, edges } = r.map;
    const g = this.add.graphics();
    const visited = new Set(r.visited);
    for (const e of edges) {
      const [a, b] = e.split(">").map((s) => s.split(":").map(Number));
      const na = rows[a[0]][a[1]];
      const nb = rows[b[0]][b[1]];
      const walked = visited.has(`${na.r}:${na.i}`) && visited.has(`${nb.r}:${nb.i}`) && r.path?.includes(e);
      if (walked) {
        g.lineStyle(6, C.wood, 1).lineBetween(na.x, na.y, nb.x, nb.y);
      } else {
        const steps = Math.floor(Phaser.Math.Distance.Between(na.x, na.y, nb.x, nb.y) / 12);
        g.fillStyle(0x6b4a2e, 0.9);
        for (let k = 1; k < steps; k++) {
          const t = k / steps;
          g.fillCircle(na.x + (nb.x - na.x) * t, na.y + (nb.y - na.y) * t, 3);
        }
      }
    }
    const next = new Set(reachable(r).map((n) => this.nodeKey(n)));
    for (const row of rows) {
      for (const n of row) {
        const key = this.nodeKey(n);
        const isNext = next.has(key);
        const done = visited.has(key);
        const radius = n.type === "boss" ? 40 : 26;
        const plate = this.add.graphics();
        if (n.type === "boss") plate.fillStyle(C.red, 1).fillCircle(n.x, n.y, radius + 5);
        if (n.type === "elite") plate.fillStyle(C.red, 1).fillCircle(n.x, n.y, radius + 3);
        plate.fillStyle(C.ink, 1).fillCircle(n.x, n.y, radius + 2);
        plate.fillStyle(done ? 0xb8ab94 : C.cream, 1).fillCircle(n.x, n.y, radius);
        const icon = this.add.image(n.x, n.y, ICON[n.type], n.type === "treasure" ? 0 : undefined);
        icon.setScale(n.type === "boss" ? 1.9 : n.type === "rest" || n.type === "treasure" ? 2.6 : 1.15);
        if (done && n.type !== "start") icon.setAlpha(0.45);
        if (isNext) {
          const ring = this.add.circle(n.x, n.y, radius + 7).setStrokeStyle(4, C.gold);
          this.tweens.add({ targets: ring, scale: 1.12, alpha: 0.4, duration: 700, yoyo: true, repeat: -1 });
          const zone = this.add.zone(n.x, n.y, radius * 2 + 16, radius * 2 + 16).setInteractive({ useHandCursor: true });
          zone.on("pointerdown", () => this.go(n));
          zone.on("pointerover", () => this.hint.setText(`${LABEL[n.type]} 칸으로 간다`));
        }
      }
    }
    const cur = rows[r.pos.r][r.pos.i];
    const token = this.add.image(cur.x - 34, cur.y - 26, "nabi-face").setScale(1.2);
    this.tweens.add({ targets: token, y: token.y - 6, duration: 500, yoyo: true, repeat: -1 });
    this.hint = text(this, 330, 618, "금빛 고리가 있는 칸을 눌러 이동한다", 18, C.creamText, { stroke: "#131b1b", strokeThickness: 4 }).setOrigin(0.5);
  }

  drawPanel() {
    const r = this.run;
    box(this, 640, 52, 308, 168, { fill: C.paper });
    text(this, 660, 66, "이 동네 우두머리", 18, "#c0392b", { fontStyle: "bold" });
    this.add.image(700, 140, "boss-face").setScale(1.6);
    text(this, 742, 100, YOKAI.kim.name, 20, C.inkText, { fontStyle: "bold" });
    text(this, 742, 128, "체력 40 · 속도 10", 16, C.muted);
    text(this, 742, 152, "방망이 8 → 장난 → 숨기", 16, C.muted);
    text(this, 742, 176, "이기면 재주를 배운다", 16, C.muted);

    box(this, 640, 228, 308, 186, { fill: C.paper });
    text(this, 660, 242, "나비", 18, "#c0392b", { fontStyle: "bold" });
    const lines = [
      `체력 ${r.hp}/${r.maxHp}`,
      `레벨 ${r.level} · 경험치 ${r.xp}/10`,
      `모아 둔 포인트 ${r.points}`,
      `엽전 ${r.coins}`,
    ];
    lines.forEach((l, k) => text(this, 660, 270 + k * 24, l, 17, C.inkText));
    text(this, 660, 370, "유물", 16, C.muted);
    if (!r.relics.length) text(this, 700, 370, "아직 없음", 16, C.muted);
    r.relics.forEach((id, k) => {
      const icon = this.add.image(712 + k * 34, 380, RELICS[id].icon).setScale(1.8).setInteractive();
      icon.on("pointerover", () => this.hint.setText(`${RELICS[id].name}: ${RELICS[id].text}`));
    });

    box(this, 640, 422, 308, 206, { fill: C.paper });
    text(this, 660, 436, "칸 안내", 18, "#c0392b", { fontStyle: "bold" });
    ["fight", "elite", "rest", "treasure", "boss"].forEach((t, k) => {
      const y = 480 + k * 30;
      this.add.image(680, y, ICON[t], t === "treasure" ? 0 : undefined).setScale(t === "rest" || t === "treasure" ? 1.6 : t === "boss" ? 0.75 : 0.7);
      text(this, 704, y, LABEL[t], 17, C.inkText).setOrigin(0, 0.5);
    });
  }

  intro() {
    const m = modal(this, 600, 330);
    const { x, y, w } = m.inner;
    m.add(text(this, x + w / 2, y + 44, "꼬리 수행 · 마을", 30, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
    m.add(text(this, x + 40, y + 84, [
      "꼬리 하나뿐인 고양이 요괴 나비가 수행 길에 나섰다.",
      "갈림길 지도에서 칸을 골라 요괴와 겨루고,",
      "끝에서 도깨비 김서방을 이기면 재주를 배운다.",
      "",
      "전투에서는 위쪽 순서 막대에 다음 여덟 차례가 보인다.",
      "큰 공격 바로 앞 차례에 웅크려서 막는 게 요령이다.",
    ].join("\n"), 18, C.inkText, { lineSpacing: 6 }));
    m.add(button(this, x + w / 2 - 90, y + 250, 180, 54, "출발", () => {
      this.run.started = true;
      m.destroy();
    }));
  }

  go(n) {
    // one move per visit to the map, even on a double click
    if (this.leaving) return;
    this.leaving = true;
    const r = this.run;
    sfx(this, "move");
    r.path = r.path || [];
    r.path.push(`${r.pos.r}:${r.pos.i}>${n.r}:${n.i}`);
    r.pos = { r: n.r, i: n.i };
    r.visited.push(this.nodeKey(n));
    if (n.type === "fight") {
      const pool = n.r <= 2 ? [0, 1] : [2, 3, 0, 1];
      let g = pool[Math.floor(Math.random() * pool.length)];
      if (g === r.lastGroup) g = pool.find((x) => x !== g) ?? g;
      r.lastGroup = g;
      this.scene.start("Battle", { ids: GROUPS[g].ids, kind: "fight", coins: GROUPS[g].coins });
    } else if (n.type === "elite") {
      const left = ELITES.filter((e) => !r.usedElites.includes(e));
      const id = left[Math.floor(Math.random() * left.length)] || "guup";
      r.usedElites.push(id);
      this.scene.start("Battle", { ids: [id], kind: "elite" });
    } else if (n.type === "boss") {
      this.scene.start("Battle", { ids: ["kim"], kind: "boss" });
    } else if (n.type === "rest") {
      this.rest();
    } else if (n.type === "treasure") {
      this.treasure();
    }
  }

  rest() {
    const r = this.run;
    const heal = Math.round(r.maxHp * 0.3);
    const m = modal(this, 560, 300);
    const { x, y, w } = m.inner;
    m.add(this.add.image(x + w / 2, y + 60, "onigiri").setScale(4));
    m.add(text(this, x + w / 2, y + 110, "쉬는 칸 · 툇마루 같은 그늘", 24, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
    m.add(button(this, x + 50, y + 170, 210, 80, "낮잠", () => {
      r.hp = Math.min(r.maxHp, r.hp + heal);
      sfx(this, "heal");
      this.scene.restart({ toast: `체력 ${heal} 회복` });
    }, { sub: `체력 ${heal} 회복` }));
    m.add(button(this, x + w - 260, y + 170, 210, 80, "수련", () => {
      const ups = gainXp(r, 5);
      sfx(this, ups ? "levelup" : "select");
      this.scene.restart({ toast: ups ? "레벨업!" : "경험치 5" });
    }, { sub: "경험치 5" }));
  }

  treasure() {
    const r = this.run;
    const left = Object.keys(RELICS).filter((id) => !r.relics.includes(id));
    Phaser.Utils.Array.Shuffle(left);
    this.relicChoice(left.slice(0, 3), "보물 상자", () => this.scene.restart({}));
  }

  relicChoice(ids, title, done) {
    const r = this.run;
    const m = modal(this, 760, 360);
    const { x, y, w } = m.inner;
    m.add(text(this, x + w / 2, y + 40, `${title} · 유물 하나를 고른다`, 24, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
    if (!ids.length) {
      m.add(text(this, x + w / 2, y + 150, "더 받을 유물이 없다", 20, C.muted).setOrigin(0.5));
      m.add(button(this, x + w / 2 - 80, y + 260, 160, 54, "확인", done));
      return;
    }
    ids.forEach((id, k) => {
      const cx = x + 40 + k * 232;
      const card = box(this, cx, y + 80, 216, 250, { fill: C.cream, frame: C.woodLight });
      m.add(card);
      m.add(this.add.image(cx + 108, y + 140, RELICS[id].icon).setScale(4));
      m.add(text(this, cx + 108, y + 196, RELICS[id].name, 20, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
      m.add(text(this, cx + 108, y + 236, RELICS[id].text, 16, C.inkText, { wordWrap: { width: 180, useAdvancedWrap: true }, align: "center" }).setOrigin(0.5, 0));
      const zone = this.add.zone(cx, y + 80, 216, 250).setOrigin(0).setInteractive({ useHandCursor: true });
      zone.on("pointerdown", () => {
        r.relics.push(id);
        sfx(this, "coin");
        m.destroy();
        done();
      });
      m.add(zone);
    });
  }
}
