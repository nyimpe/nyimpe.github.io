---
name: game-idea-research
category: gaming
description: >
  Research and propose 2D pixel art game ideas. Using popular games from 2000s onwards
  or currently trending indie titles as references, generate 3 distinct genre ideas
  optimized for Phaser JS and save them structured for the nyimpe.github.io project.
---

## Goal

Derive **3 distinctly different genre** ideas for 2D pixel art + Phaser JS games based on market trends.
Each idea must inherit the essence of a reference game while innovating with an original twist and modern mechanics.

---

## Workflow

### Step 1 — Market Research (in priority order)

Explore the sources below in order. Move to the next step once you have good results.

**A. Use `web_search` first:**
```
"best pixel art indie games 2025 trending"
"itch.io top pixel art games 2025"
"phaser js game ideas popular genres"
"reddit r/indiegaming most upvoted 2024 2025"
```

**B. If `web_search` fails, navigate directly:**
- `https://itch.io/games/tag-pixel-art` (sorted by popular)
- `https://itch.io/games/made-with-phaser`
- `https://store.steampowered.com/tags/en/Pixel+Art/`
- `https://www.reddit.com/r/indiegaming/top/?t=year`

> ⚠️ **Strategy switch trigger:** If search results are dominated by asset packs or tutorials, immediately pivot to direct itch.io navigation.

---

### Step 2 — Trend Analysis

Extract the following from research results:

| Analysis Item | What to Look For |
|---------------|-----------------|
| **Popular Genres** | Top-ranking genres on Steam/itch.io right now |
| **Core Game Loop** | The core repeated action players take |
| **Differentiators** | Common innovation points among hit titles |
| **Phaser Suitability** | Mechanics implementable in browser 2D |
| **Asset Lightness** | Whether it's achievable with minimal custom assets |

**Genre pool to pick from (choose 3, no overlaps):**
- Roguelite / Roguelike
- Metroidvania
- Deckbuilder / Card Battler
- Auto-battler Lite
- Puzzle-Platformer
- Top-down Shooter (Bullet Hell)
- Tower Defense
- Farming / Life Sim Lite
- Turn-based Tactics

**Genre selection criteria (in priority order):**
1. Currently trending on Steam/itch.io
2. Complexity implementable in Phaser JS
3. All 3 must have distinctly different play patterns

---

### Step 3 — Idea Generation (the critical step)

Each idea must pass the following **idea quality checklist** before proceeding:

```
✅ Does a clear reference game exist? (post-2000s)
✅ Is there a clear innovation twist beyond simple copying?
✅ Can the core game loop be explained in one sentence?
✅ Is it playable in a browser with just mouse/keyboard?
✅ Can it be expressed with 16x16~32x32 pixel art sprites?
✅ Is it implementable with Phaser's built-in features alone (no external libraries)?
✅ Does a single session complete within 5–15 minutes?
```

**How to generate the innovation twist:**

Combine the reference game's core mechanic with one of the following:
- **Genre Crossover**: Fuse core mechanics from Genre A + Genre B
- **Perspective/Control Inversion**: Enemy POV, reverse progression, environment manipulation
- **Resource Dilemma**: Restructure the existing resource system as zero-sum / trade-off
- **Time Mechanic**: Time limit, rewind, prediction-based play
- **Information Asymmetry**: Fog of war, memory-based, partially revealed map

---

### Step 4 — Idea Documentation

**All game idea content must be written in Korean markdown.**
(Skill instructions remain in English; only the output game ideas are in Korean.)

Required fields for each idea:

```markdown
## Idea N: [Title]

### Basic Info
- **id**: "kebab-case-id"
- **title**: "Emoji + Catchy Title"
- **description**: "One-line summary (under 50 characters)"
- **loader**: "() => import('./games/[id]/main.js')"

### Reference Game
- **Original**: Game title (release year, developer)
- **Genre**: Genre name
- **Why it worked**: 1–2 sentences on why the original succeeded

### Innovation Twist
> Clearly describe what is different from the original
- **Twist type**: (Genre Crossover / Perspective Inversion / Resource Dilemma / Time Mechanic / Information Asymmetry)
- **Key change**: Specific mechanical difference explained
- **Player experience**: What feelings/decisions will the player experience?

### Core Game Loop
```
[Action] → [Outcome] → [Choice] → [Repeat]
e.g. Explore dungeon → Gain resources → Choose upgrade → Next floor
```

### Pixel Art Visual Guide
- **Resolution**: 16x16 / 32x32 sprites
- **Palette**: Color count limit (e.g. 4–8 colors), key tone keywords
- **Animation**: Frame count needed, list of key animations
- **Background style**: How the tilemap is structured

### Phaser JS Implementation Notes
- **Physics**: Why arcade or matter.js was chosen
- **Scene structure**: List of required scenes (Boot → Preload → Menu → Game → UI)
- **Core systems**: Main classes/modules to implement
- **Reusable modules**: Components shareable across other games
- **Difficulty**: ⭐~⭐⭐⭐⭐⭐ (implementation complexity)

### Market Viability
- **Target audience**: Primary player demographic
- **Session length**: Expected single-play duration
- **Replayability**: Low / Medium / High (with reason)
- **Comparable hits**: Successful indie games with similar concept
```

---

### Step 5 — Save File

1. Confirm today's date:
   ```bash
   date +%Y%m%d
   ```

2. Create the `idea/` directory if it doesn't exist:
   ```bash
   mkdir -p idea
   ```

3. Save the file:
   ```bash
   # Filename: idea/game_idea_YYYYMMDD.md
   ```

4. **Always verify the actual filename with `ls` before proceeding:**
   ```bash
   ls idea/game_idea_*.md
   ```

---

### Step 6 — Git Commit & Push

```bash
# 1. Confirm actual filename (required)
FILENAME=$(ls idea/game_idea_*.md | tail -1)
echo "File to commit: $FILENAME"

# 2. Git add
git add "$FILENAME"

# 3. Commit with date-based message
DATE=$(date +%Y%m%d)
git commit -m "feat: ${DATE} 게임 아이디어 추가"

# 4. Push
git push origin main
```

---

## Quality Standards

### ✅ What makes a good idea
- The core loop can be explained in 5 seconds
- Can answer "why this game, why now?"
- The pixel art style connects organically to the gameplay
- Implementable with Phaser basics only (Arcade Physics, Tilemap, Tween, Group)

### ❌ Ideas to avoid
- Simple clones of existing games (no mechanical innovation)
- Games requiring 3D, complex physics, or large-scale AI
- Games needing 10+ minute tutorials before the first session
- Games that don't function without a large volume of custom assets

---

## Pitfalls & Countermeasures

| Situation | Response |
|-----------|----------|
| Search results dominated by asset packs / tutorials | Immediately pivot to direct itch.io navigation |
| All 3 ideas converging on similar genres | Revisit genre selection criteria, verify play pattern diversity |
| Filename mismatch on git add | **Always confirm actual filename with `ls` before git add** |
| Innovation twist is vague | Explicitly pick one of the 5 twist types |
| Phaser implementation is overly complex | Reduce scope to built-in features only, no external libraries |
| All 3 ideas have identical difficulty | Spread implementation difficulty across ⭐~⭐⭐⭐⭐⭐ |
