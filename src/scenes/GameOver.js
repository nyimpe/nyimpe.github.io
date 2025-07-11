import Phaser from "phaser";

// 게임 오버 씬 클래스 - 게임 종료 화면 담당
export class GameOver extends Phaser.Scene {
  constructor() {
    super("GameOver");
  }

  create() {
    // 배경 이미지 생성
    this.background1 = this.add.image(0, 0, "background").setOrigin(0);

    // 게임 오버 텍스트 생성
    this.add
      .text(this.scale.width * 0.5, this.scale.height * 0.5, "Game Over", {
        fontFamily: "Arial Black",
        fontSize: 64,
        color: "#ffffff",
        stroke: "#000000",
        strokeThickness: 8,
        align: "center",
      })
      .setOrigin(0.5);
  }
}
