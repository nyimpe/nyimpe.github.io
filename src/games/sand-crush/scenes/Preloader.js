
import Phaser from "phaser";

export class Preloader extends Phaser.Scene {
  constructor() {
    super("Preloader");
  }

  init() {
    //  We loaded this image from our Boot Scene, so use that to display the progress bar
    const camera = this.cameras.main;
    this.add.rectangle(camera.width / 2, camera.height / 2, 468, 32).setStrokeStyle(1, 0xffffff);

    const bar = this.add.rectangle(camera.width / 2 - 230, camera.height / 2, 4, 28, 0xffffff);

    this.load.on("progress", (progress) => {
      bar.width = 4 + (460 * progress);
    });
  }

  preload() {
    // Load any assets here if needed
    // For asset-free development, this can remain empty or load minimal placeholder graphics.
  }

  create() {
    this.scene.start("Game");
  }
}
