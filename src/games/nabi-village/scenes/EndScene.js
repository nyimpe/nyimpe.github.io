import Phaser from "phaser";
import { RELICS, TALENTS } from "../data.js";
import { C, box, button, music, sfx, text } from "../ui.js";

export class EndScene extends Phaser.Scene {
  constructor() {
    super("End");
  }

  create(data) {
    this.run = this.registry.get("run");
    music(this, "village");
    this.add.image(0, 0, "bg-map").setOrigin(0).setScale(3);
    this.add.rectangle(0, 0, 960, 640, 0x000000, 0.35).setOrigin(0);
    if (data.result === "win") this.pickTalent(data.lines || []);
    else this.lose();
  }

  restartButton(x, y) {
    return button(this, x, y, 220, 60, "다시 하기", () => this.scene.start("Map", { fresh: true }));
  }

  lose() {
    box(this, 180, 140, 600, 360, { fill: C.paper });
    this.add.sprite(480, 250, "nabi").setScale(5).play("nabi-idle");
    text(this, 480, 310, "나비가 지쳐서 툇마루로 돌아갔다", 26, C.inkText, { fontStyle: "bold" }).setOrigin(0.5);
    text(this, 480, 350, "낮잠 한숨 자고 다시 떠나자. 재주와 유물은 잊었다.", 18, C.muted).setOrigin(0.5);
    this.restartButton(370, 400);
  }

  pickTalent(lines) {
    const options = Phaser.Utils.Array.Shuffle([...TALENTS]).slice(0, 3);
    box(this, 40, 40, 880, 560, { fill: C.paper });
    this.add.sprite(110, 130, "boss-idle").setScale(2).play("boss-idle-idle");
    text(this, 170, 84, "도깨비 김서방", 18, "#2f5fa0", { fontStyle: "bold" });
    text(this, 170, 110, "졌다, 졌어! 재주 하나 가르쳐 줄게.", 26, C.inkText, { fontStyle: "bold" });
    text(this, 170, 150, lines.join(" · "), 16, C.muted, { wordWrap: { width: 700 } });
    options.forEach((t, k) => {
      const x = 80 + k * 272;
      const y = 210;
      box(this, x, y, 256, 330, { fill: C.cream, frame: C.woodLight });
      const tx = t.face ? x + 100 : x + 26;
      if (t.face) this.add.image(x + 52, y + 62, t.face).setScale(1.5);
      text(this, tx, y + 44, t.name, 22, C.inkText, { fontStyle: "bold" });
      text(this, tx, y + 74, `${t.from}에게 배움`, 15, C.muted);
      text(this, x + 26, y + 118, t.does, 17, C.inkText, { wordWrap: { width: 210, useAdvancedWrap: true } });
      text(this, x + 26, y + 176, "첫 기술", 14, C.muted);
      text(this, x + 26, y + 196, t.first, 17, "#c0392b", { fontStyle: "bold" });
      text(this, x + 26, y + 232, "길 위에서", 14, C.muted);
      text(this, x + 26, y + 252, t.road, 17, C.inkText);
      const zone = this.add.zone(x, y, 256, 330).setOrigin(0).setInteractive({ useHandCursor: true });
      const ring = this.add.graphics();
      zone.on("pointerover", () => ring.clear().lineStyle(5, C.gold, 1).strokeRoundedRect(x - 4, y - 4, 264, 338, 10));
      zone.on("pointerout", () => ring.clear());
      zone.on("pointerdown", () => {
        sfx(this, "levelup");
        this.summary(t);
      });
    });
  }

  summary(talent) {
    const r = this.run;
    this.children.removeAll(true);
    this.add.image(0, 0, "bg-map").setOrigin(0).setScale(3);
    box(this, 140, 90, 680, 460, { fill: C.paper });
    this.add.sprite(480, 190, "nabi").setScale(5).play("nabi-idle");
    text(this, 480, 250, `나비는 ${talent.name}를 배웠다!`, 28, C.inkText, { fontStyle: "bold" }).setOrigin(0.5);
    text(this, 480, 290, "시제품은 여기까지. 다음 동네는 강이다.", 18, C.muted).setOrigin(0.5);
    const relics = r.relics.length ? r.relics.map((id) => RELICS[id].name).join(", ") : "없음";
    text(this, 220, 330, [
      `레벨 ${r.level} · 체력 ${r.hp}/${r.maxHp}`,
      `엽전 ${r.coins} · 모아 둔 포인트 ${r.points}`,
      `유물: ${relics}`,
    ].join("\n"), 19, C.inkText, { lineSpacing: 8, wordWrap: { width: 520 } });
    this.restartButton(370, 460);
  }
}
