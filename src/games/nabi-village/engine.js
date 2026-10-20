// Turn-based battle rules from posts 4 and 6, kept free of rendering.
// interval = 120 / speed; everyone starts half an interval in; ties go to Nabi.
import { NABI, SKILLS, YOKAI } from "./data.js";

const interval = (unit) => 120 / Math.max(2, unit.speed - (unit.slowTurns > 0 ? 2 : 0));

let uid = 0;

function makeYokai(id, t0) {
  const def = YOKAI[id];
  const unit = {
    uid: ++uid, id, def, name: def.name, hp: def.hp, maxHp: def.hp, speed: def.speed,
    isPlayer: false, block: 0, shield: 0, slowTurns: 0, loopIndex: 0, history: [], charged: null,
  };
  unit.t = t0 ?? interval(unit) / 2;
  unit.intent = nextIntent(unit);
  return unit;
}

function pickWeighted(unit) {
  const options = unit.def.weights.filter(([, , kind]) => {
    const h = unit.history;
    return !(h.length >= 2 && h[h.length - 1] === kind && h[h.length - 2] === kind);
  });
  const total = options.reduce((s, o) => s + o[0], 0);
  let roll = Math.random() * total;
  for (const o of options) {
    roll -= o[0];
    if (roll <= 0) return o;
  }
  return options[options.length - 1];
}

function nextIntent(unit) {
  if (unit.charged != null) return { label: "혀 치기", kind: "atk", value: unit.charged };
  if (unit.def.loop) {
    const [label, kind, value] = unit.def.loop[unit.loopIndex % unit.def.loop.length];
    return { label, kind, value };
  }
  const [, label, kind, value] = pickWeighted(unit);
  return { label, kind, value };
}

// What an enemy will do on its k-th upcoming turn, if the player can know it.
function knownIntent(unit, k) {
  if (k === 0) return unit.intent;
  if (unit.def.loop && k === 1) {
    const [label, kind, value] = unit.def.loop[(unit.loopIndex + 1) % unit.def.loop.length];
    return { label, kind, value };
  }
  if (unit.intent.kind === "charge" && k === 1) return { label: "큰 공격", kind: "atk", value: unit.intent.value };
  return null;
}

export function intentText(intent) {
  if (!intent) return "?";
  switch (intent.kind) {
    case "atk": return `${intent.label} ${intent.value}`;
    case "block": return `${intent.label} · 막기 ${intent.value}`;
    case "shield": return `${intent.label} · 보호막 ${intent.value}`;
    case "guard": return `${intent.label} · 짝에게 막기 ${intent.value}`;
    case "charge": return `${intent.label} · 다음 ${intent.value}`;
    case "confuse": return `${intent.label} · 헷갈림`;
    case "heal": return `${intent.label} · 회복 ${intent.value}`;
    case "summon": return `${intent.label} · 무리 부르기`;
    case "steal": return `${intent.label} · 나비 느림`;
    case "flee_prep": return "도망 준비";
    case "flee": return "도망!";
    default: return intent.label;
  }
}

export class Battle {
  constructor(run, ids, kind) {
    this.kind = kind;
    this.run = run;
    this.log = [];
    this.player = {
      uid: ++uid, id: "nabi", name: NABI.name, isPlayer: true, hp: run.hp, maxHp: run.maxHp, speed: NABI.speed,
      block: 0, shield: 0, slowTurns: 0, confused: false, bambooUsed: false,
    };
    this.player.t = interval(this.player) / 2;
    this.enemies = ids.map((id) => makeYokai(id));
    this.result = null;
    this.now = 0;
    if (run.relics.includes("branch")) this.player.block = 4;
    if (run.relics.includes("feather")) this.player.t -= 5;
  }

  get alive() {
    return this.enemies.filter((e) => e.hp > 0);
  }

  units() {
    return [this.player, ...this.alive];
  }

  // Next unit to act: smallest time, Nabi first on ties, then left to right.
  next() {
    return this.units().reduce((best, u) => {
      if (!best) return u;
      if (u.t < best.t - 1e-9) return u;
      if (Math.abs(u.t - best.t) < 1e-9 && u.isPlayer && !best.isPlayer) return u;
      return best;
    }, null);
  }

  // Upcoming turns for the order bar, without changing state.
  preview(n = 8) {
    const sim = this.units().map((u) => ({ u, t: u.t, k: 0, slow: u.slowTurns }));
    const out = [];
    while (out.length < n) {
      const s = sim.reduce((best, x) => {
        if (!best) return x;
        if (x.t < best.t - 1e-9) return x;
        if (Math.abs(x.t - best.t) < 1e-9 && x.u.isPlayer && !best.u.isPlayer) return x;
        return best;
      }, null);
      out.push({ unit: s.u, intent: s.u.isPlayer ? null : knownIntent(s.u, s.k) });
      s.t += 120 / Math.max(2, s.u.speed - (s.slow > 0 ? 2 : 0));
      if (s.slow > 0) s.slow -= 1;
      s.k += 1;
    }
    return out;
  }

  say(text) {
    this.log.push(text);
  }

  damageEnemy(target, amount) {
    let dmg = amount;
    const fromBlock = Math.min(dmg, target.block);
    target.block -= fromBlock;
    dmg -= fromBlock;
    const fromShield = Math.min(dmg, target.shield);
    target.shield -= fromShield;
    dmg -= fromShield;
    target.hp = Math.max(0, target.hp - dmg);
    return { dealt: dmg, absorbed: fromBlock + fromShield };
  }

  damagePlayer(amount) {
    const p = this.player;
    const fromBlock = Math.min(amount, p.block);
    p.block -= fromBlock;
    const dealt = amount - fromBlock;
    const before = p.hp;
    p.hp = Math.max(0, p.hp - dealt);
    let bamboo = false;
    if (this.run.relics.includes("bamboo") && !p.bambooUsed && before >= p.maxHp / 2 && p.hp < p.maxHp / 2 && p.hp > 0) {
      p.bambooUsed = true;
      p.block += 10;
      bamboo = true;
    }
    return { dealt, absorbed: fromBlock, bamboo };
  }

  // Player turn. Returns an event describing what happened.
  playerAct(skillId, target) {
    const p = this.player;
    p.block = 0;
    let used = skillId;
    let confused = false;
    if (p.confused) {
      used = skillId === "scratch" ? "crouch" : "scratch";
      p.confused = false;
      confused = true;
    }
    const ev = { actor: p, skill: used, confused };
    if (used === "scratch") {
      const tgt = target && target.hp > 0 ? target : this.alive[0];
      const r = this.damageEnemy(tgt, SKILLS.scratch.damage);
      Object.assign(ev, { target: tgt, ...r });
      if (tgt.hp <= 0) ev.defeated = this.defeat(tgt);
    } else {
      p.block += SKILLS.crouch.block;
      ev.block = SKILLS.crouch.block;
    }
    p.t += interval(p);
    if (p.slowTurns > 0) p.slowTurns -= 1;
    this.checkEnd();
    return ev;
  }

  defeat(unit) {
    const gone = [unit];
    if (unit.def.leader) {
      for (const e of this.alive) {
        if (e.def.summon) {
          e.hp = 0;
          gone.push(e);
        }
      }
    }
    return gone;
  }

  enemyAct(unit) {
    unit.block = 0;
    const intent = unit.intent;
    const ev = { actor: unit, intent };
    unit.history.push(intent.kind);
    if (unit.charged != null) unit.charged = null;
    switch (intent.kind) {
      case "atk": {
        Object.assign(ev, this.damagePlayer(intent.value));
        break;
      }
      case "confuse":
        this.player.confused = true;
        break;
      case "block":
        unit.block = intent.value;
        break;
      case "shield":
        unit.shield += intent.value;
        break;
      case "guard": {
        const mate = this.alive.find((e) => e !== unit) || unit;
        mate.block += intent.value;
        ev.mate = mate;
        break;
      }
      case "charge":
        unit.charged = intent.value;
        break;
      case "summon": {
        if (!this.alive.some((e) => e.id === intent.value)) {
          const m = makeYokai(intent.value, unit.t + 120 / YOKAI[intent.value].speed / 2);
          this.enemies.push(m);
          ev.summoned = m;
        }
        break;
      }
      case "heal":
        unit.hp = Math.min(unit.maxHp, unit.hp + intent.value);
        break;
      case "steal":
        this.player.slowTurns = intent.value;
        break;
      case "flee":
        if (!this.run.relics.includes("sieve")) {
          this.result = "fled";
          ev.fled = true;
        }
        break;
      default:
        break;
    }
    if (unit.def.loop) unit.loopIndex += 1;
    unit.t += interval(unit);
    unit.intent = nextIntent(unit);
    this.checkEnd();
    return ev;
  }

  checkEnd() {
    if (this.result) return;
    if (this.player.hp <= 0) this.result = "lose";
    else if (!this.alive.some((e) => !e.def.summon)) this.result = "win";
  }
}
