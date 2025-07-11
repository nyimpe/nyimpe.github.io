import Phaser from "phaser";
import ASSETS from "../assets.js";

// 프리로더 씬 클래스 - 게임 에셋 로딩 및 진행률 표시
export class Preloader extends Phaser.Scene {
  constructor() {
    super("Preloader");
  }

  init() {
    // 화면 중앙 좌표 계산
    const centreX = this.scale.width * 0.5;
    const centreY = this.scale.height * 0.5;

    // 진행률 바 설정
    const barWidth = 468;
    const barHeight = 32;
    const barMargin = 4;
    // 부트 씬에서 로드한 이미지를 여기서 표시할 수 있습니다

    // 간단한 진행률 바 - 바의 외곽선
    this.add
      .rectangle(centreX, centreY, barWidth, barHeight)
      .setStrokeStyle(1, 0xffffff);

    // 진행률 바 자체 - 진행률에 따라 왼쪽에서부터 크기가 증가합니다
    const bar = this.add.rectangle(
      centreX - barWidth * 0.5 + barMargin,
      centreY,
      barMargin,
      barHeight - barMargin,
      0xffffff
    );

    // LoaderPlugin의 'progress' 이벤트를 사용하여 로딩 바 업데이트
    this.load.on("progress", (progress) => {
      // 진행률 바 업데이트 (바 너비는 464px이므로 100% = 464px)
      bar.width = barMargin + (barWidth - barMargin * 2) * progress;
    });
  }

  preload() {
    // 게임 에셋 로드 - ./src/assets.js 참조
    for (let type in ASSETS) {
      for (let key in ASSETS[type]) {
        let args = ASSETS[type][key].args.slice();
        args.unshift(ASSETS[type][key].key);
        this.load[type].apply(this.load, args);
      }
    }
  }

  create() {
    // 모든 에셋이 로드되면 게임의 다른 부분에서 사용할 전역 객체를 생성합니다.
    // 예를 들어, 다른 씬에서 사용할 전역 애니메이션을 여기서 정의할 수 있습니다.

    // 메인 메뉴로 이동. 카메라 페이드 같은 씬 전환 효과로 대체할 수도 있습니다.
    this.scene.start("Game");
  }
}
