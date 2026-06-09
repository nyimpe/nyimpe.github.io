---
name: game-idea-research
category: gaming
description: Research and propose game ideas suitable for 2D pixel art games using Phaser JS, based on games from the 2000s onwards or popular modern titles, and fitting the nyimpe.github.io project structure.
---

### Goal
To generate 1-2 game ideas for 2D pixel art games using Phaser JS, based on games from the 2000s onwards or popular modern titles, with modernized concepts and structured to fit the nyimpe.github.io project.

### Workflow

1.  **Initial Search (Fallback from `web_search`):**
    *   If `web_search` is unavailable or yields poor results, use `browser_navigate` to go to a search engine (e.g., Google).
    *   Use `browser_type` to input a comprehensive query (e.g., "popular 2D games 2000s onwards suitable for modernization phaser js pixel art", "trending indie 2D games phaser js pixel art", "modernized classic 2D games phaser js pixel art").
    *   Use `browser_press` with "Enter" to submit the search.

2.  **Browse Search Results:**
    *   Use `browser_snapshot` to review the search results.
    *   Identify promising links (e.g., game review sites, indie game showcases, Phaser community examples).
    *   Use `browser_navigate` to visit relevant links.

3.  **Information Gathering:**
    *   On visited pages, use `browser_snapshot(full=True)` or `browser_scroll(direction='down')` followed by `browser_snapshot()` to gather comprehensive information about potential reference games.
    *   Look for games from the 2000s onwards, or recent popular indie titles, with simple 2D mechanics that can be easily adapted to a pixel art style and Phaser JS.
    *   Identify core gameplay loops, popular elements, and potential areas for modernization, keeping in mind the need for asset/library simplification.

4.  **Idea Generation & Structuring:**
    *   Based on the gathered information, propose 1-2 distinct game ideas.
    *   For each idea, include the following fields, adhering to the nyimpe.github.io project's game list structure (id, title, description, loader):
        *   **id:** A unique, hyphen-separated identifier (e.g., "pixel-dungeon-crawler").
        *   **title:** A catchy, descriptive title (e.g., "✨ Pixel Dungeon: Legacy").
        *   **description:** A concise summary of the game (e.g., "Explore procedurally generated dungeons!").
        *   **loader:** A placeholder for the game's main script path (e.g., "() => import('./games/pixel-dungeon/main.js')").
        *   **Modernized Concept:** How the reference game concept is updated with new mechanics, features, or twists.
        *   **Pixel Art Style Notes:** Specific visual themes, color palettes, or animation considerations for a pixel art aesthetic.
        *   **Phaser JS Implementation Considerations:** Brief notes on how core mechanics might be implemented using Phaser's features (e.g., physics, scenes, sprites, input handling), and how common modules could be reused.

5.  **Output and Saving:**
    *   Format the game ideas in markdown.
    *   Save the complete output to a file named `game_idea_<YYYYMMDD>.md` in the current working directory.
    *   Save the content of the *first* proposed game idea to a file named `.hermes/current_week_game_idea.md` for potential future use by a development cron job.

### Pitfalls and Considerations

*   **`web_search` Unavailability:** Be prepared to use browser tools for web research if `web_search` is not available. This requires more steps but achieves the same goal.
*   **Information Overload:** Wikipedia lists or general gaming articles can be extensive. Focus on identifying core mechanics and visual styles relevant to 2D pixel art and Phaser JS.
*   **Reference vs. Innovation:** Ensure the idea builds upon the reference game with significant innovation and a clear modernization path, rather than just copying. Focus on simplified assets and libraries to maintain a lightweight project.
*   **Asset/Library Simplification:** Prioritize game ideas that can be implemented with minimal custom assets and external libraries (e.g., using tilemaps, simple sprites, built-in Phaser features, basic sound effects).
