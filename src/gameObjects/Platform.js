import Phaser from "phaser";
import ASSETS from "../assets.js";

export default class Platform extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, width = 100, height = 16) {
    super(scene, x, y, ASSETS.spritesheet.tiles.key, 50);

    scene.add.existing(this);

    scene.physics.add.existing(this, true);

    this.setOrigin(0, 0);

    // 타일 크기가 32x32이므로 적절히 스케일링
    this.setScale(width / 32, height / 32);

    // 물리 바디 크기를 정확히 설정
    this.body.setSize(width, height);
    this.body.setOffset(0, 0);

    this.setDepth(50);

    this.scene = scene;
    this.width = width;
    this.height = height;
  }

  destroy() {
    super.destroy();
  }
}
