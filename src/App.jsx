import { useState, useEffect, useRef } from "react";

// Games list registry
const GAMES = [
  {
    id: "jumping-cat",
    title: "🐈 Jumping Cat (Jump)",
    description: "Touch or Space to jump and climb the platforms!",
    loader: () => import("./games/jumping-cat/main.js")
  },
  {
    id: "tetris",
    title: "🧱 Tetris Classic",
    description: "Classic block-stacking puzzle game with smooth touch controls!",
    loader: () => import("./games/tetris/main.js")
  },

  {
    id: "shikaku",
    title: "◧ Shikaku (四角に切れ)",
    description: "Divide the grid into rectangles — each block must contain exactly one number matching its area!",
    loader: () => import("./games/shikaku/main.js")
  },
  {
    id: "vampire-survivor",
    title: "🧛 Vampire Survivor Lite",
    description: "Survive the endless horde! Auto-attack, collect XP, level up!",
    loader: () => import("./games/vampire-survivor/main.js")
  },
  {
    id: "hole-io",
    title: "🕳️ Hole.io",
    description: "Swallow everything! Grow your black hole by consuming the city!",
    loader: () => import("./games/hole-io/main.js")
  },

];

const App = () => {
  const [selectedGameId, setSelectedGameId] = useState("jumping-cat");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const gameInstanceRef = useRef(null);

  useEffect(() => {
    // If there is an existing game instance, destroy it first
    if (gameInstanceRef.current) {
      gameInstanceRef.current.destroy(true);
      gameInstanceRef.current = null;
    }

    const selectedGame = GAMES.find((g) => g.id === selectedGameId);
    if (!selectedGame) return;

    let active = true;

    selectedGame
      .loader()
      .then((module) => {
        if (!active) return;
        const StartGame = module.default;
        const container = document.getElementById("game-container");
        if (container) {
          container.innerHTML = ""; // Clear existing DOM contents
          gameInstanceRef.current = StartGame("game-container");
        }
      })
      .catch((err) => {
        console.error("Failed to load game:", err);
      });

    return () => {
      active = false;
      if (gameInstanceRef.current) {
        gameInstanceRef.current.destroy(true);
        gameInstanceRef.current = null;
      }
    };
  }, [selectedGameId]);

  const handleGameSelect = (id) => {
    setSelectedGameId(id);
    setIsSidebarOpen(false); // Close mobile sidebar after selection
  };

  return (
    <div className="app-layout">
      {/* Mobile Toggle Button */}
      <button
        className="menu-toggle-btn"
        onClick={() => setIsSidebarOpen(true)}
        aria-label="Open menu"
      >
        ☰
      </button>

      {/* Sidebar Overlay (Mobile only) */}
      <div
        className={`sidebar-overlay ${isSidebarOpen ? "open" : ""}`}
        onClick={() => setIsSidebarOpen(false)}
      ></div>

      {/* Sidebar */}
      <aside className={`sidebar ${isSidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <h1 className="sidebar-title">🕹️ Arcade Center</h1>
          <button
            className="sidebar-close-btn"
            onClick={() => setIsSidebarOpen(false)}
            aria-label="Close menu"
          >
            ✕
          </button>
        </div>

        <ul className="game-list">
          {GAMES.map((game) => (
            <li
              key={game.id}
              className={`game-item ${
                selectedGameId === game.id ? "active" : ""
              }`}
              onClick={() => handleGameSelect(game.id)}
            >
              <h3 className="game-item-title">{game.title}</h3>
              <p className="game-item-desc">{game.description}</p>
            </li>
          ))}
        </ul>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {selectedGameId ? (
          <div className="game-wrapper">
            <div id="game-container"></div>
          </div>
        ) : (
          <div className="empty-state">
            <h2>Select a Game</h2>
            <p>Choose a game from the sidebar to start playing!</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
