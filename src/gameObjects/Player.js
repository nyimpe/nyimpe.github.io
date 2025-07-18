import Phaser from "phaser";

export default class Player extends Phaser.Physics.Arcade.Sprite {
  baseMoveSpeed = 200;
  moveSpeed = 200;
  moveDirection = 1;
  gravity = 1200;
  isGrounded = false;
  pressStartTime = null;

  constructor(scene, x, y, shipId) {
    super(scene, x, y, "", shipId);
    scene.add.existing(this);
    scene.physics.add.existing(this);

    this.scene = scene;
    this.body.setGravityY(this.gravity);
    this.setCollideWorldBounds(true);
    this.setDepth(100);

    this.moveDirection = Math.random() < 0.5 ? -1 : 1;

    this.jumpPowerText = this.scene.add
      .text(this.x, this.y - 50, "0", {
        fontSize: "24px",
        color: "#ffcc00",
        stroke: "#000",
        strokeThickness: 3,
      })
      .setOrigin(0.5)
      .setDepth(200)
      .setVisible(false);

    this.registerInput();
  }

  registerInput() {
    const input = this.scene.input;
    input.keyboard.on("keydown-SPACE", this.onPressStart, this);
    input.keyboard.on("keyup-SPACE", this.onPressRelease, this);
    input.on("pointerdown", this.onPressStart, this);
    input.on("pointerup", this.onPressRelease, this);
  }

  onPressStart() {
    if (!this.isGrounded) return;
    this.pressStartTime = this.scene.time.now;
    this.jumpPowerText.setVisible(true);
  }

  onPressRelease() {
    if (!this.isGrounded || this.pressStartTime === null) return;

    const duration = this.scene.time.now - this.pressStartTime;
    const power = this.calculateJumpPower(duration);
    const jumpVelocity = -300 - (power - 1) * 100;

    this.jump(jumpVelocity);
    this.play(`jump${power}`, true);

    this.jumpPowerText.setVisible(false);
    this.pressStartTime = null;

    // 속도 복구는 preUpdate에서 자동 처리됨
  }

  calculateJumpPower(duration) {
    if (duration < 100) return 1;
    else if (duration < 200) return 2;
    else if (duration < 300) return 3;
    else if (duration < 400) return 4;
    else return 5;
  }

  jump(jumpVelocity) {
    this.body.velocity.y = jumpVelocity;
  }

  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    this.updateMovement();
    this.updateJumpPowerText();
  }

  updateMovement() {
    // 지면 체크
    this.isGrounded = this.body.blocked.down || this.body.touching.down;

    // 속도 감소 적용
    if (this.pressStartTime !== null && this.isGrounded) {
      const duration = this.scene.time.now - this.pressStartTime;
      const power = this.calculateJumpPower(duration);
      const factor = 1 - power * 0.1; // 0~5 → 0~0.5 감소
      this.moveSpeed = this.baseMoveSpeed * factor;
    } else {
      this.moveSpeed = this.baseMoveSpeed;
    }

    // 이동 처리
    this.body.setVelocityX(this.moveSpeed * this.moveDirection);

    // 벽 충돌 시 방향 반전
    if (this.x <= this.width / 2) {
      this.moveDirection = 1;
    } else if (this.x >= this.scene.scale.width - this.width / 2) {
      this.moveDirection = -1;
    }
  }

  updateJumpPowerText() {
    if (this.pressStartTime !== null) {
      if (!this.isGrounded) {
        this.pressStartTime = null;
        this.jumpPowerText.setVisible(false);
        return;
      }

      const duration = this.scene.time.now - this.pressStartTime;
      const power = this.calculateJumpPower(duration);
      this.jumpPowerText.setText(power.toString());
      this.jumpPowerText.setPosition(this.x, this.y - 50);
    }
  }
}
