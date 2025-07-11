import Phaser from "phaser";

// 시작 씬 클래스 - 게임 시작 화면 담당
export class Start extends Phaser.Scene {
  constructor() {
    super("Start");
  }

  create() {
    // 배경 타일 스프라이트 생성 (주석 처리됨)
    // this.background = this.add.tileSprite(640, 360, 1280, 720, 'background');
    // 로고 이미지 추가 (주석 처리됨)
    // const logo = this.add.image(640, 200, 'logo');
    // 우주선 스프라이트 추가 (주석 처리됨)
    // const ship = this.add.sprite(640, 360, 'ship');
    // 우주선 날기 애니메이션 생성 (주석 처리됨)
    // ship.anims.create({
    //     key: 'fly',
    //     frames: this.anims.generateFrameNumbers('ship', { start: 0, end: 2 }),
    //     frameRate: 15,
    //     repeat: -1
    // });
    // 애니메이션 재생 (주석 처리됨)
    // ship.play('fly');
    // 로고 트윈 애니메이션 추가 (주석 처리됨)
    // this.tweens.add({
    //     targets: logo,
    //     y: 400,
    //     duration: 1500,
    //     ease: 'Sine.inOut',
    //     yoyo: true,
    //     loop: -1
    // });
  }

  // 매 프레임 업데이트 함수 (현재 비어있음)
  update() {}
}
