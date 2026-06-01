import Phaser from "phaser";
import { Game } from "./scenes/Game.js";

const config = {
  type: Phaser.AUTO,
  title: "Tetris Classic",
  parent: "game-container",
  width: 430,
  height: 932,
  backgroundColor: "#111216",
  scene: [Game],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
