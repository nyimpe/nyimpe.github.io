import Phaser from "phaser";
import ASSETS from "../assets.js";

export default class Platform extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, x, y, width = 100) {
    // 0~11 사이의 랜덤 프레임 선택
    const frame = Phaser.Math.Between(0, 11);
    super(scene, x, y, ASSETS.spritesheet.platforms.key, frame);

    scene.add.existing(this);
    scene.physics.add.existing(this, true);

    this.setOrigin(0, 0);

    // 원본 스프라이트의 크기는 375x95 입니다.
    const originalWidth = 375;

    // 원하는 너비(width)에 맞춰 스케일 계산
    const scale = width / originalWidth;

    // 계산된 스케일 적용
    this.setScale(scale);

    // 스케일이 적용된 게임 오브젝트의 상태를 물리 바디에 업데이트
    this.body.updateFromGameObject();

    this.setDepth(50);

    this.scene = scene;
  }

  destroy() {
    super.destroy();
  }
}
