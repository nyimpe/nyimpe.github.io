import Phaser from "phaser";
import { SceneMenu } from "./scenes/SceneMenu.js";
import { Game } from "./scenes/Game.js";

const config = {
  type: Phaser.AUTO,
  title: "Shikaku",
  parent: "game-container",
  width: 430,
  height: 932,
  backgroundColor: "#1a1a2e",
  scene: [SceneMenu, Game],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

const StartGame = (parent) => {
  return new Phaser.Game({ ...config, parent });
};

export default StartGame;
