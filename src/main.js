// Phaser 게임 엔진 및 씬 모듈 임포트
import Phaser from "phaser";
import { Preloader } from "./scenes/Preloader.js";
import { Game } from "./scenes/Game.js";

// 게임 설정 객체
const config = {
  type: Phaser.AUTO,
  title: "Jump",
  description: "",
  parent: "game-container",
  width: 430,
  height: 932,
  backgroundColor: "#000000",
  pixelArt: false, // 픽셀 아트 스타일 설정
  physics: {
    default: "arcade", // 아케이드 물리 엔진 사용
    arcade: {
      debug: true, // 디버그 모드 비활성화
      gravity: { y: 300 }, // 중력 설정 (y축 중력 없음)
    },
  },
  scene: [Preloader, Game], // 씬 배열 순서
  scale: {
    mode: Phaser.Scale.FIT, // 화면에 맞춤 모드
    autoCenter: Phaser.Scale.CENTER_BOTH, // 자동 중앙 정렬
  },
};

// 게임 시작 함수
const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent }); // 설정과 부모 요소로 게임 인스턴스 생성
};

export default StartGame;
