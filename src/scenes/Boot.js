// 부트 씬 클래스 - 게임 시작 전 초기 로딩 담당
export class Boot extends Phaser.Scene {
  constructor() {
    super("Boot");
  }

  preload() {
    // 부트 씬은 일반적으로 프리로더에 필요한 에셋(로고, 배경 등)을 로드합니다.
    // 부트 씬 자체에는 프리로더가 없으므로 파일 크기가 작을수록 좋습니다.
    // this.load.image('background', 'assets/background.png');
  }

  create() {
    // 프리로더 씬으로 전환
    this.scene.start("Preloader");
  }
}
