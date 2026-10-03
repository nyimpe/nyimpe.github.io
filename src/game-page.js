const games = {
  "jumping-cat": () => import("./games/jumping-cat/main.js"),
  tetris: () => import("./games/tetris/main.js"),
  shikaku: () => import("./games/shikaku/main.js"),
  "vampire-survivor": () => import("./games/vampire-survivor/main.js"),
  "hole-io": () => import("./games/hole-io/main.js"),
};

const stage = document.querySelector(".game-stage");
const container = document.getElementById("game-container");
const placeholder = document.querySelector(".game-placeholder");
const status = document.querySelector(".game-status");
const start = document.getElementById("start-game");
const restart = document.getElementById("restart-game");

// Keyboard controls belong to the focused game, so the article still scrolls.
container.addEventListener("pointerdown", () => container.focus({ preventScroll: true }));
restart.addEventListener("click", () => window.location.reload());

start.addEventListener("click", async () => {
  if (stage.dataset.state === "error") {
    window.location.reload();
    return;
  }
  start.disabled = true;
  stage.dataset.state = "loading";
  status.textContent = "Loading game…";
  try {
    const module = await games[stage.dataset.game]();
    module.default("game-container", {
      input: { keyboard: { target: container } },
    });
    placeholder.hidden = true;
    restart.hidden = false;
    stage.dataset.state = "running";
    container.focus({ preventScroll: true });
    stage.scrollIntoView({ block: "center" });
  } catch (error) {
    console.error("Failed to load game:", error);
    status.textContent = "Could not load the game. Please reload.";
    start.textContent = "Reload";
    start.disabled = false;
    stage.dataset.state = "error";
  }
});
