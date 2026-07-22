import Phaser from "phaser";
import { Game } from "./scenes/Game.js";

const config = {
  type: Phaser.AUTO,
  title: "Hole.io",
  parent: "game-container",
  width: 960,
  height: 640,
  backgroundColor: "#4a6741",
  scene: [Game],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: "arcade",
    arcade: {
      debug: false,
      gravity: { y: 0 },
    },
  },
};

const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
