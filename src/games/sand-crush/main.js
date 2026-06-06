
import Phaser from "phaser";
import { Preloader } from "./scenes/Preloader.js";
import { Game } from "./scenes/Game.js";

const config = {
  type: Phaser.AUTO,
  parent: "game-container",
  width: 800,
  height: 600,
  backgroundColor: "#1a1a1a",
  physics: {
    default: "matter",
    matter: {
      debug: true,
      gravity: { y: 1 },
    },
  },
  scene: [Preloader, Game],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
