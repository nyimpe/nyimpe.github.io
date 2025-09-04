import Phaser from "phaser";
import { Preloader } from "./scenes/Preloader.js";
import { Game } from "./scenes/Game.js";

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
      gravity: { y: 300 },
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
