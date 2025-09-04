import Phaser from "phaser";
import ASSETS from "../assets.js";

export default class Platform extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, width = 100) {
    const frame = Phaser.Math.Between(0, 11);
    super(scene, x, y, ASSETS.spritesheet.platforms.key, frame);

    scene.add.existing(this);
    scene.physics.add.existing(this, true);

    this.setOrigin(0, 0);

    const originalWidth = 375;
    const scale = width / originalWidth;

    this.setScale(scale);
    this.body.updateFromGameObject();
    this.setDepth(50);
    this.scene = scene;
  }

  destroy() {
    super.destroy();
  }
}
