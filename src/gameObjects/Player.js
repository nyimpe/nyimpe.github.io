import Phaser from "phaser";
import ASSETS from "../assets.js";

export default class Player extends Phaser.Physics.Arcade.Sprite {
  baseMoveSpeed = 100;
  moveSpeed = 150;
  moveDirection = 1;
  gravity = 1200;
  isGrounded = false;

  chargePower = 0; // 현재 충전된 단계 (0~5)
  chargeInterval = 100; // 💡 충전 간격(ms)
  pressStartTime = null; // 누르기 시작한 시간
  lastChargeTime = null; // 마지막 충전 시간

  constructor(scene, x, y) {
    super(scene, x, y, ASSETS.spritesheet.player.key);
    scene.add.existing(this);
    scene.physics.add.existing(this);

    this.scene = scene;
    this.body.setGravityY(this.gravity);
    this.setCollideWorldBounds(false); // 세계 경계 충돌 비활성화로 위로 계속 올라갈 수 있게 함
    this.setDepth(100);
    this.setScale(0.5);
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
    this.createAnimations();
  }

  createAnimations() {
    this.anims.create({
      key: "walk",
      frames: this.anims.generateFrameNumbers(ASSETS.spritesheet.player.key, {
        frames: [9, 10],
      }),
      frameRate: 10,
      repeat: -1,
    });

    this.anims.create({
      key: "jump",
      frames: this.anims.generateFrameNumbers(ASSETS.spritesheet.player.key, {
        frames: [0, 1, 2, 3],
      }),
      frameRate: 5,
      repeat: 1,
    });
  }

  registerInput() {
    const input = this.scene.input;
    input.keyboard.on("keydown-SPACE", this.onPressStart, this);
    input.keyboard.on("keyup-SPACE", this.onPressRelease, this);
    input.on("pointerdown", this.onPressStart, this);
    input.on("pointerup", this.onPressRelease, this);
  }

  onPressStart() {
    if (!this.isGrounded || this.pressStartTime !== null) return;

    this.pressStartTime = this.scene.time.now;
    this.lastChargeTime = this.pressStartTime;
    this.chargePower = 0;
    this.jumpPowerText.setVisible(true);
  }

  onPressRelease() {
    if (!this.isGrounded || this.pressStartTime === null) return;

    const jumpVelocity = -500 - (this.chargePower - 1) * 100;
    this.jump(jumpVelocity);

    this.play(`jump${this.chargePower}`, true);

    this.resetCharge();
  }

  resetCharge() {
    this.pressStartTime = null;
    this.lastChargeTime = null;
    this.chargePower = 0;
    this.jumpPowerText.setVisible(false);
  }

  jump(jumpVelocity) {
    this.body.velocity.y = jumpVelocity;
  }

  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    this.updateGrounded();
    this.updateCharging(time);
    this.updateMovement();
    this.updateJumpPowerText();
    this.updateAnimation();
  }

  updateAnimation() {
    if (this.isGrounded) {
      if (this.anims.currentAnim?.key !== "walk") {
        this.play("walk");
      }
    } else {
      if (this.anims.currentAnim?.key === "walk") {
        this.play("jump");
      }
    }
  }

  updateGrounded() {
    this.isGrounded = this.body.blocked.down || this.body.touching.down;
    if (!this.isGrounded && this.pressStartTime !== null) {
      this.resetCharge(); // 공중에서 강제 초기화
    }
  }

  updateCharging(currentTime) {
    if (this.pressStartTime !== null && this.isGrounded) {
      if (
        currentTime - this.lastChargeTime >= this.chargeInterval &&
        this.chargePower < 5
      ) {
        this.chargePower++;
        this.lastChargeTime = currentTime;
      }
    }
  }

  updateMovement() {
    // 충전 중이면 속도 감소
    if (this.pressStartTime !== null && this.isGrounded) {
      const factor = 1 - this.chargePower * 0.1;
      this.moveSpeed = this.baseMoveSpeed * factor;
    } else {
      this.moveSpeed = this.baseMoveSpeed;
    }

    this.body.setVelocityX(this.moveSpeed * this.moveDirection);

    if (this.moveDirection < 0) {
      this.flipX = true;
    } else {
      this.flipX = false;
    }

    if (this.x <= this.width / 2) this.moveDirection = 1;
    else if (this.x >= this.scene.scale.width - this.width / 2)
      this.moveDirection = -1;
  }

  updateJumpPowerText() {
    if (this.pressStartTime !== null) {
      this.jumpPowerText.setText(this.chargePower.toString());
      this.jumpPowerText.setPosition(this.x, this.y - 50);
    }
  }
}
