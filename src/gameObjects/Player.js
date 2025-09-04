import Phaser from "phaser";
import ASSETS from "../assets.js";

export default class Player extends Phaser.Physics.Arcade.Sprite {
  baseMoveSpeed = 100;
  moveSpeed = 150;
  moveDirection = 1;
  gravity = 1200;
  isGrounded = false;

  chargePower = 0;
  chargeInterval = 100;
  pressStartTime = null;
  lastChargeTime = null;
  blinkingTween = null;

  constructor(scene, x, y) {
    super(scene, x, y, ASSETS.spritesheet.run.key);
    scene.add.existing(this);
    scene.physics.add.existing(this);

    this.body.setSize(24, 24);
    this.body.setOffset(23, 23);

    this.scene = scene;
    this.body.setGravityY(this.gravity);
    this.setCollideWorldBounds(false);
    this.setDepth(100);
    this.setScale(2);
    this.moveDirection = Math.random() < 0.5 ? -1 : 1;

    this.powerSprite = this.scene.add
      .sprite(this.x, this.y - 10, "power1")
      .setDepth(200)
      .setVisible(false)
      .setScale(0.08);

    this.registerInput();
    this.createAnimations();
  }

  createAnimations() {
    this.anims.create({
      key: "run",
      frames: this.anims.generateFrameNumbers(ASSETS.spritesheet.run.key, {
        frames: [0, 1, 2, 3, 4, 5, 6, 7],
      }),
      frameRate: 10,
      repeat: -1,
    });

    this.anims.create({
      key: "jump",
      frames: this.anims.generateFrameNumbers(ASSETS.spritesheet.jump.key, {
        frames: [0, 1, 2],
      }),
      frameRate: 3,
      repeat: 1,
    });

    this.powerChargeAnim = this.anims.create({
      key: "power-charge",
      frames: [
        { key: "power1" },
        { key: "power2" },
        { key: "power3" },
        { key: "power4" },
        { key: "power5" },
        { key: "power6" },
        { key: "power7" },
      ],
      frameRate: 10,
      repeat: 0,
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
    this.powerSprite.setVisible(true);
    const frame = this.powerChargeAnim.frames[0];
    this.powerSprite.setTexture(frame.textureKey);
  }

  onPressRelease() {
    if (!this.isGrounded || this.pressStartTime === null) return;

    const jumpVelocity = -500 - this.chargePower * 80;
    this.jump(jumpVelocity);

    this.play("jump", true);

    this.resetCharge();
  }

  resetCharge() {
    this.pressStartTime = null;
    this.lastChargeTime = null;
    this.chargePower = 0;
    this.powerSprite.setVisible(false);
  }

  jump(jumpVelocity) {
    this.body.velocity.y = jumpVelocity;
  }

  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    this.updateBlinkingEffect();
    this.updateGrounded();
    this.updateCharging(time);
    this.updateMovement();
    this.updatePowerSprite();
    this.updateAnimation();
  }

  updateBlinkingEffect() {
    if (this.chargePower > 0 && this.isGrounded && !this.blinkingTween) {
      this.blinkingTween = this.scene.tweens.add({
        targets: this,
        alpha: 0.5,
        ease: "Power2",
        duration: 100,
        yoyo: true,
        repeat: -1,
      });
    } else if (
      (this.chargePower === 0 || !this.isGrounded) &&
      this.blinkingTween
    ) {
      this.blinkingTween.stop();
      this.blinkingTween = null;
      this.setAlpha(1);
    }
  }

  updateAnimation() {
    if (this.isGrounded) {
      if (this.anims.currentAnim?.key !== "run") {
        this.play("run");
      }
    } else {
      if (this.anims.currentAnim?.key === "run") {
        this.play("jump");
      }
    }
  }

  updateGrounded() {
    this.isGrounded = this.body.blocked.down || this.body.touching.down;
    if (!this.isGrounded && this.pressStartTime !== null) {
      this.resetCharge();
    }
  }

  updateCharging(currentTime) {
    if (this.pressStartTime !== null && this.isGrounded) {
      if (
        currentTime - this.lastChargeTime >= this.chargeInterval &&
        this.chargePower < 6
      ) {
        this.chargePower++;
        this.lastChargeTime = currentTime;
        const frame = this.powerChargeAnim.frames[this.chargePower];
        this.powerSprite.setTexture(frame.textureKey);
      }
    }
  }

  updateMovement() {
    if (this.pressStartTime !== null && this.isGrounded) {
      const factor = 1 - this.chargePower * 0.1;
      this.moveSpeed = this.baseMoveSpeed * factor;
    } else {
      this.moveSpeed = this.baseMoveSpeed;
    }

    this.body.setVelocityX(this.moveSpeed * this.moveDirection);

    if (this.moveDirection < 0) {
      this.flipX = false;
    } else {
      this.flipX = true;
    }

    if (this.x <= this.width / 2) this.moveDirection = 1;
    else if (this.x >= this.scene.scale.width - this.width / 2)
      this.moveDirection = -1;
  }

  updatePowerSprite() {
    if (this.pressStartTime !== null) {
      this.powerSprite.setPosition(this.x, this.y - 25);
    }
  }
}
