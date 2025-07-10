// Phaser 게임 엔진 및 씬 모듈 임포트
import Phaser from "phaser";
import { Boot } from "./scenes/Boot.js";
import { Preloader } from "./scenes/Preloader.js";
import { Start } from "./scenes/Start.js";
import { Game } from "./scenes/Game.js";
import { GameOver } from "./scenes/GameOver.js";

// 게임 설정 객체
const config = {
  type: Phaser.AUTO, // 자동으로 렌더러 타입 결정 (WebGL 또는 Canvas)
  title: "Shmup", // 게임 제목
  description: "", // 게임 설명
  parent: "game-container", // 게임을 렌더링할 DOM 요소 ID
  width: 430, // 게임 캔버스 폭
  height: 932, // 게임 캔버스 높이
  backgroundColor: "#000000", // 배경색 (검은색)
  pixelArt: false, // 픽셀 아트 스타일 설정
  physics: {
    default: "arcade", // 아케이드 물리 엔진 사용
    arcade: {
      debug: false, // 디버그 모드 비활성화
      gravity: { y: 0 }, // 중력 설정 (y축 중력 없음)
    },
  },
  scene: [Boot, Preloader, Start, Game, GameOver], // 씬 배열 순서
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
