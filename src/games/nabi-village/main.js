import Phaser from "phaser";
import { Boot } from "./scenes/Boot.js";
import { MapScene } from "./scenes/MapScene.js";
import { BattleScene } from "./scenes/BattleScene.js";
import { EndScene } from "./scenes/EndScene.js";

const config = {
  type: Phaser.AUTO,
  title: "꼬리 수행 · 마을",
  parent: "game-container",
  width: 960,
  height: 640,
  backgroundColor: "#2a2129",
  pixelArt: true,
  scene: [Boot, MapScene, BattleScene, EndScene],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

const StartGame = (parent, options = {}) => {
  const game = new Phaser.Game({ ...config, ...options, parent });
  // Lets the dev server's browser checks read the running game; stripped from builds.
  if (import.meta.env.DEV) window.__nabiGame = game;
  return game;
};

export default StartGame;
