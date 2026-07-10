import Phaser from "phaser";
import { Game } from "./scenes/Game.js";

const config = {
  type: Phaser.AUTO,
  title: "Vampire Survivor Lite",
  parent: "game-container",
  width: 960,
  height: 640,
  backgroundColor: "#1a1a2e",
  scene: [Game],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: "arcade",
    arcade: {
      debug: false,
    },
  },
};

const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
