import Phaser from "phaser";
import ASSETS from "../assets.js";

export default class Platform extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, width = 100, height = 16) {
    super(scene, x, y, ASSETS.spritesheet.tiles.key, 50);

    scene.add.existing(this);

    scene.physics.add.existing(this, true);

    this.setOrigin(0, 0);

    this.setScale(width / 32, height / 32);

    this.body.setSize(width, height);

    this.setDepth(50);

    this.scene = scene;
    this.width = width;
    this.height = height;
  }

  destroy() {
    super.destroy();
  }
}
