// One run of the village: map, Nabi's state and progress. Lives in the game registry.
import { NABI } from "./data.js";

const ROW_SIZES = [1, 3, 2, 3, 2, 3, 1];
const ROW_TYPES = [
  null,
  [["fight", 1]],
  [["fight", 60], ["treasure", 40]],
  [["fight", 40], ["elite", 40], ["rest", 20]],
  [["fight", 50], ["rest", 30], ["treasure", 20]],
  [["rest", 40], ["elite", 30], ["fight", 30]],
  null,
];

function pick(options) {
  const total = options.reduce((s, o) => s + o[1], 0);
  let r = Math.random() * total;
  for (const [v, w] of options) {
    r -= w;
    if (r <= 0) return v;
  }
  return options[0][0];
}

export function makeMap() {
  const left = 60;
  const right = 580;
  const rows = ROW_SIZES.map((n, r) => {
    const y = 580 - r * 78;
    return Array.from({ length: n }, (_, i) => {
      const x = n === 1 ? (left + right) / 2 : left + 30 + ((right - left - 60) * i) / (n - 1) + (Math.random() * 30 - 15);
      let type = "fight";
      if (r === 0) type = "start";
      else if (r === ROW_SIZES.length - 1) type = "boss";
      else type = pick(ROW_TYPES[r]);
      return { r, i, x: Math.round(x), y, type };
    });
  });
  // at least one rest in the row before the boss, and at least one elite on the map
  const row5 = rows[5];
  if (!row5.some((n) => n.type === "rest")) row5[Math.floor(Math.random() * row5.length)].type = "rest";
  if (!rows.flat().some((n) => n.type === "elite")) rows[3][1].type = "elite";

  const edges = new Set();
  const key = (a, b) => `${a.r}:${a.i}>${b.r}:${b.i}`;
  for (let r = 0; r < rows.length - 1; r++) {
    const cur = rows[r];
    const nxt = rows[r + 1];
    const near = (node, list) => list.reduce((best, n) => (Math.abs(n.x - node.x) < Math.abs(best.x - node.x) ? n : best));
    for (const n of nxt) edges.add(key(near(n, cur), n));
    for (const c of cur) {
      edges.add(key(c, near(c, nxt)));
      for (const n of nxt) {
        if (Math.abs(n.x - c.x) < 200 && Math.random() < 0.45) edges.add(key(c, n));
      }
    }
  }
  return { rows, edges: [...edges] };
}

export function newRun() {
  return {
    hp: NABI.hp,
    maxHp: NABI.hp,
    level: 1,
    xp: 0,
    points: 0,
    coins: 0,
    relics: [],
    map: makeMap(),
    pos: { r: 0, i: 0 },
    visited: ["0:0"],
    usedElites: [],
    lastGroup: -1,
    fights: 0,
    started: false,
  };
}

export function reachable(run) {
  const from = `${run.pos.r}:${run.pos.i}>`;
  return run.map.edges.filter((e) => e.startsWith(from)).map((e) => {
    const [r, i] = e.split(">")[1].split(":").map(Number);
    return run.map.rows[r][i];
  });
}

// Returns how many levels were gained.
export function gainXp(run, amount) {
  run.xp += amount;
  let ups = 0;
  while (run.xp >= 10) {
    run.xp -= 10;
    run.level += 1;
    run.maxHp += 3;
    run.hp = Math.min(run.maxHp, run.hp + (run.relics.includes("iron") ? 8 : 3));
    run.points += 1;
    ups += 1;
  }
  return ups;
}
