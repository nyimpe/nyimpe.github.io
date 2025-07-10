import { forwardRef, useEffect, useLayoutEffect, useRef } from "react";
import StartGame from "./main";
// import { EventBus } from "./game/EventBus";

import Phaser from "phaser";

// // Used to emit events between components, HTML and Phaser scenes
// export const EventBus = new Phaser.Events.EventEmitter();

export const PhaserGame = forwardRef(function PhaserGame(
  { currentActiveScene },
  ref
) {
  const game = useRef();

  // Create the game inside a useLayoutEffect hook to avoid the game being created outside the DOM
  useLayoutEffect(() => {
    if (game.current === undefined) {
      game.current = StartGame("game-container");

      if (ref !== null) {
        ref.current = { game: game.current, scene: null };
      }
    }

    return () => {
      if (game.current) {
        game.current.destroy(true);
        game.current = undefined;
      }
    };
  }, [ref]);

  useEffect(() => {
    new Phaser.Events.EventEmitter().on(
      "current-scene-ready",
      (currentScene) => {
        if (currentActiveScene instanceof Function) {
          currentActiveScene(currentScene);
        }
        ref.current.scene = currentScene;
      }
    );

    return () => {
      new Phaser.Events.EventEmitter().removeListener("current-scene-ready");
    };
  }, [currentActiveScene, ref]);

  return <div id="game-container"></div>;
});
