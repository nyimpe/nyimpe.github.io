import Phaser from "phaser";

const DIFFICULTIES = [
  { label: "EASY", size: 5, color: 0x4caf50, desc: "5×5" },
  { label: "MEDIUM", size: 7, color: 0xff9800, desc: "7×7" },
  { label: "HARD", size: 10, color: 0xf44336, desc: "10×10" },
];

export class SceneMenu extends Phaser.Scene {
  constructor() {
    super("SceneMenu");
  }

  create() {
    this.cameras.main.setBackgroundColor("#1a1a2e");

    const cx = this.scale.width / 2;

    this.add
      .text(cx, 140, "◧ SHIKAKU", {
        fontFamily: "Arial Black",
        fontSize: "42px",
        color: "#e0d7ff",
        stroke: "#7c4dff",
        strokeThickness: 8,
      })
      .setOrigin(0.5);

    this.add
      .text(cx, 210, "사각형으로 나눠라!", {
        fontFamily: "Arial, sans-serif",
        fontSize: "18px",
        color: "#b39ddb",
      })
      .setOrigin(0.5);

    // Rules blurb
    const rules = [
      "• 격자를 직사각형 블록으로 나누세요",
      "• 각 블록에는 숫자가 하나씩 있어야 하고",
      "• 숫자는 블록의 칸 수(면적)와 같아야 합니다",
      "• 드래그하여 직사각형을 그리고,",
      "  조건에 맞으면 자동으로 배치됩니다",
    ];
    rules.forEach((line, i) => {
      this.add
        .text(cx, 280 + i * 28, line, {
          fontFamily: "Arial, sans-serif",
          fontSize: "13px",
          color: "#7e8aa2",
          align: "center",
        })
        .setOrigin(0.5);
    });

    // Difficulty buttons
    const startY = 470;
    DIFFICULTIES.forEach((diff, i) => {
      const y = startY + i * 90;
      const btnW = 220;
      const btnH = 60;

      const gfx = this.add.graphics();
      gfx.fillStyle(diff.color, 0.85);
      gfx.fillRoundedRect(cx - btnW / 2, y, btnW, btnH, 14);
      gfx.lineStyle(3, 0xffffff, 0.3);
      gfx.strokeRoundedRect(cx - btnW / 2, y, btnW, btnH, 14);

      this.add
        .text(cx, y + 20, diff.label, {
          fontFamily: "Arial Black",
          fontSize: "22px",
          color: "#ffffff",
        })
        .setOrigin(0.5);

      this.add
        .text(cx, y + 46, diff.desc, {
          fontFamily: "Arial, sans-serif",
          fontSize: "13px",
          color: "#ffffffcc",
        })
        .setOrigin(0.5);

      const zone = this.add
        .rectangle(cx, y + btnH / 2, btnW, btnH)
        .setInteractive({ useHandCursor: true });
      zone.on("pointerover", () => {
        gfx.clear();
        gfx.fillStyle(diff.color, 1.0);
        gfx.fillRoundedRect(cx - btnW / 2, y, btnW, btnH, 14);
        gfx.lineStyle(3, 0xffffff, 0.6);
        gfx.strokeRoundedRect(cx - btnW / 2, y, btnW, btnH, 14);
      });
      zone.on("pointerout", () => {
        gfx.clear();
        gfx.fillStyle(diff.color, 0.85);
        gfx.fillRoundedRect(cx - btnW / 2, y, btnW, btnH, 14);
        gfx.lineStyle(3, 0xffffff, 0.3);
        gfx.strokeRoundedRect(cx - btnW / 2, y, btnW, btnH, 14);
      });
      zone.on("pointerdown", () => {
        this.scene.start("Game", { size: diff.size });
      });
    });
  }
}
