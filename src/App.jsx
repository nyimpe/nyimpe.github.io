import { useLayoutEffect } from "react";
import StartGame from "./main";

const App = () => {
  useLayoutEffect(() => {
    StartGame("game-container");
  }, []);

  return (
    <div id="app">
      <div id="game-container"></div>
    </div>
  );
};

export default App;
