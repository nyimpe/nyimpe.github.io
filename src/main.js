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
  pixelArt: true,
  physics: {
    default: "arcade",
    arcade: {
      debug: true,
      gravity: { y: 300 }, // 중력 설정 (y축 중력 없음)
    },
  },
  scene: [Preloader, Game],
  scale: {
    mode: Phaser.Scale.FIT, // 화면에 맞춤 모드
    autoCenter: Phaser.Scale.CENTER_BOTH, // 자동 중앙 정렬
  },
};

// 게임 시작 함수
const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
