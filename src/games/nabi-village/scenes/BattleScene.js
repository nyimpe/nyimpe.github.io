import Phaser from "phaser";
import { RELICS, REWARD, SKILLS, YOKAI } from "../data.js";
import { Battle, intentText } from "../engine.js";
import { gainXp } from "../run.js";
import { C, box, button, floatText, hpBar, modal, muteToggle, music, sfx, text } from "../ui.js";

const FIELD_Y = 104;
const FEET_Y = 404;
const KIND_LABEL = { fight: "잡요괴", elite: "이름난 요괴", boss: "우두머리" };
const BADGE = {
  atk: [C.red, (i) => `${i.value}`],
  block: [C.blue, () => "막"],
  shield: [C.blue, () => "보"],
  guard: [C.blue, () => "지"],
  charge: [0xe08a2c, () => "!"],
  confuse: [0x8a5ad6, () => "?"],
  heal: [C.green, () => "+"],
  summon: [0x9b513c, () => "부"],
  steal: [0x8a5ad6, () => "신"],
  flee_prep: [0x666666, () => "…"],
  flee: [0x666666, () => "도"],
};

export class BattleScene extends Phaser.Scene {
  constructor() {
    super("Battle");
  }

  create(data) {
    this.run = this.registry.get("run");
    this.kind = data.kind;
    this.coins = data.coins ?? 0;
    this.battle = new Battle(this.run, data.ids, data.kind);
    this.busy = true;
    this.sprites = new Map();
    this.target = this.battle.alive[0];
    music(this, "fight");

    this.add.image(0, FIELD_Y, "bg-battle").setOrigin(0).setScale(3);
    this.add.rectangle(0, 0, 960, 40, C.ink, 0.92).setOrigin(0);
    text(this, 16, 20, `마을 · ${KIND_LABEL[this.kind]}`, 20, C.creamText, { fontStyle: "bold" }).setOrigin(0, 0.5);
    this.turnLabel = text(this, 480, 20, "", 20, C.creamText).setOrigin(0.5);
    this.add.image(800, 20, "coin").setScale(3);
    text(this, 816, 20, `${this.run.coins}`, 20, C.creamText).setOrigin(0, 0.5);
    muteToggle(this, 948, 20);

    this.add.rectangle(0, 40, 960, 64, 0x2a2129, 1).setOrigin(0);
    text(this, 16, 72, "순서", 18, "#ffc43a", { fontStyle: "bold" }).setOrigin(0, 0.5);
    this.orderLayer = this.add.container(0, 0);

    this.add.rectangle(0, 464, 960, 176, C.olive, 1).setOrigin(0);
    this.add.rectangle(0, 464, 960, 4, C.ink, 1).setOrigin(0);
    this.logText = text(this, 24, 486, "", 19, C.creamText).setOrigin(0, 0.5);
    this.buttons = this.add.container(0, 0);

    this.player = this.add.sprite(230, FEET_Y, "nabi").setOrigin(0.5, 1).setScale(4).play("nabi-idle");
    this.sprites.set(this.battle.player.uid, this.player);
    this.plates = this.add.container(0, 0);
    this.layoutEnemies();

    this.input.keyboard?.on("keydown-ONE", () => this.choose("scratch"));
    this.input.keyboard?.on("keydown-TWO", () => this.choose("crouch"));
    this.input.keyboard?.on("keydown-LEFT", () => this.cycleTarget(-1));
    this.input.keyboard?.on("keydown-RIGHT", () => this.cycleTarget(1));

    const names = this.battle.alive.map((e) => e.name).join(", ");
    this.say(`${names}${this.kind === "boss" ? "이(가) 길을 막았다!" : "와(과) 겨룬다!"}`);
    if (this.kind === "elite") this.say(this.battle.alive[0].def.blurb);
    this.refresh();
    this.time.delayedCall(500, () => this.advance());
  }

  enemyX(index, count) {
    const slots = { 1: [700], 2: [620, 810], 3: [560, 700, 840] };
    return (slots[count] || slots[3])[index] ?? 840;
  }

  makeEnemySprite(unit, x) {
    const def = YOKAI[unit.id];
    let s;
    if (def.body === "boss") {
      s = this.add.sprite(x, FEET_Y + 6, "boss-idle").setOrigin(0.5, 1).setScale(3.2).play("boss-idle-idle");
    } else {
      s = this.add.sprite(x, FEET_Y, def.sheet).setOrigin(0.5, 1).setScale(5).play(`${def.sheet}-idle`);
      if (def.body === "animal") s.setFlipX(true);
    }
    s.setInteractive({ useHandCursor: true });
    s.on("pointerdown", () => this.setTarget(unit));
    return s;
  }

  layoutEnemies() {
    const alive = this.battle.alive;
    alive.forEach((u, k) => {
      const x = this.enemyX(k, alive.length);
      let s = this.sprites.get(u.uid);
      if (!s) {
        s = this.makeEnemySprite(u, x);
        this.sprites.set(u.uid, s);
      } else {
        this.tweens.add({ targets: s, x, duration: 250 });
      }
      s.homeX = x;
    });
  }

  say(line) {
    this.logText.setText(line);
  }

  setTarget(unit) {
    if (unit.hp <= 0) return;
    this.target = unit;
    sfx(this, "move", 0.3);
    this.refresh();
  }

  cycleTarget(step) {
    const alive = this.battle.alive;
    if (!alive.length) return;
    const k = alive.indexOf(this.target);
    this.setTarget(alive[(k + step + alive.length) % alive.length]);
  }

  refresh() {
    const b = this.battle;
    if (!this.target || this.target.hp <= 0) this.target = b.alive.find((e) => e.def.leader) || b.alive[0];
    this.drawOrder();
    this.drawPlates();
    this.drawButtons();
  }

  drawOrder() {
    this.orderLayer.removeAll(true);
    const order = this.battle.preview(8);
    let x = 70;
    order.forEach((slot, k) => {
      const size = k === 0 ? 56 : 46;
      const y = 72 - size / 2;
      const rim = k === 0 ? C.gold : slot.unit.isPlayer ? C.wood : C.red;
      const g = this.add.graphics();
      g.fillStyle(C.ink, 1).fillRect(x - 3, y - 3, size + 6, size + 6);
      g.fillStyle(rim, 1).fillRect(x, y, size, size);
      g.fillStyle(0xfff3dc, 1).fillRect(x + 3, y + 3, size - 6, size - 6);
      const face = slot.unit.isPlayer ? "nabi-face" : YOKAI[slot.unit.id].face;
      const img = this.add.image(x + size / 2, y + size / 2, face).setScale((size - 8) / 38);
      this.orderLayer.add([g, img]);
      if (slot.intent && BADGE[slot.intent.kind]) {
        const [color, label] = BADGE[slot.intent.kind];
        const bx = x + size - 14;
        const by = y + size - 12;
        const badge = this.add.graphics();
        badge.fillStyle(C.ink, 1).fillRoundedRect(bx - 2, by - 2, 24, 22, 6);
        badge.fillStyle(color, 1).fillRoundedRect(bx, by, 20, 18, 5);
        const t = text(this, bx + 10, by + 9, label(slot.intent), 13, "#ffffff", { fontStyle: "bold" }).setOrigin(0.5);
        this.orderLayer.add([badge, t]);
      }
      x += size + 14;
    });
    const p = this.battle.player;
    const speedNote = p.slowTurns > 0 ? `나비 속도 ${p.speed - 2} (느림 ${p.slowTurns}차례)` : `나비 속도 ${p.speed}`;
    const enemySpeeds = this.battle.alive.map((e) => `${e.name} ${e.speed}`).join(" · ");
    this.orderLayer.add(text(this, x + 10, 62, speedNote, 15, C.creamText).setOrigin(0, 0.5));
    this.orderLayer.add(text(this, x + 10, 84, enemySpeeds, 15, "#d8c8b0", { wordWrap: { width: 940 - x - 10 } }).setOrigin(0, 0.5));
  }

  plate(unit, x, top) {
    const w = 170;
    const g = this.add.graphics();
    g.fillStyle(C.ink, 0.9).fillRoundedRect(x - w / 2, top, w, 52, 8);
    const items = [g];
    items.push(text(this, x - w / 2 + 10, top + 8, unit.name, 16, C.creamText, { fontStyle: "bold" }));
    items.push(text(this, x + w / 2 - 10, top + 8, `${unit.hp}/${unit.maxHp}`, 15, C.creamText).setOrigin(1, 0));
    items.push(hpBar(this, x - w / 2 + 10, top + 32, w - 20, unit.hp / unit.maxHp, unit.isPlayer ? C.green : C.red));
    const tags = [];
    if (unit.block) tags.push(`막기 ${unit.block}`);
    if (unit.shield) tags.push(`보호막 ${unit.shield}`);
    if (unit.isPlayer && unit.confused) tags.push("헷갈림");
    if (unit.isPlayer && unit.slowTurns > 0) tags.push("느림");
    if (tags.length) {
      const t = text(this, x, top + 66, tags.join(" · "), 15, "#ffffff", { backgroundColor: "#2f5fa0", padding: { x: 6, y: 2 } }).setOrigin(0.5);
      items.push(t);
    }
    return items;
  }

  drawPlates() {
    this.plates.removeAll(true);
    const p = this.battle.player;
    this.plates.add(this.plate(p, 230, 128));
    for (const e of this.battle.alive) {
      const s = this.sprites.get(e.uid);
      const x = s ? s.homeX ?? s.x : 700;
      const top = e.def.body === "boss" ? 128 : 182;
      this.plates.add(this.plate(e, x, top));
      // intent bubble
      const bubble = text(this, x, top - 22, intentText(e.intent), 16, C.inkText, {
        backgroundColor: "#fff3dc", padding: { x: 8, y: 4 }, fontStyle: "bold",
      }).setOrigin(0.5);
      this.plates.add(bubble);
      if (e === this.target && this.battle.alive.length > 1) {
        const arrow = this.add.triangle(x, FEET_Y + 26, -12, 0, 12, 0, 0, -14, C.gold).setStrokeStyle(3, C.ink);
        this.tweens.add({ targets: arrow, y: arrow.y + 6, duration: 400, yoyo: true, repeat: -1 });
        this.plates.add(arrow);
      }
      const zone = this.add.zone(x, top + 26, 170, 52).setInteractive({ useHandCursor: true });
      zone.on("pointerdown", () => this.setTarget(e));
      this.plates.add(zone);
    }
  }

  drawButtons() {
    this.buttons.removeAll(true);
    const myTurn = !this.busy;
    const mk = (x, id, key) => {
      const s = SKILLS[id];
      return button(this, x, 516, 210, 96, s.name, () => this.choose(id), { sub: `${s.kind} · ${s.text}`, disabled: !myTurn, key });
    };
    this.buttons.add(mk(24, "scratch", "1"));
    this.buttons.add(mk(250, "crouch", "2"));
    this.buttons.add(button(this, 476, 516, 210, 96, "재주 칸", () => {}, { sub: "마을 끝에서 배움", disabled: true }));
    this.buttons.add(button(this, 702, 516, 234, 96, "재주 칸", () => {}, { sub: "강 끝에서 배움", disabled: true }));
  }

  choose(skillId) {
    if (this.busy || this.battle.result) return;
    this.busy = true;
    const ev = this.battle.playerAct(skillId, this.target);
    this.animatePlayer(ev, () => this.afterAction());
  }

  advance() {
    const b = this.battle;
    if (b.result) return this.finish();
    const u = b.next();
    if (u.isPlayer) {
      this.busy = false;
      this.turnLabel.setText("나비 차례");
      if (u.confused) this.say("나비가 헷갈린다! 고른 기술 대신 다른 기술이 나간다.");
      this.refresh();
      return;
    }
    this.busy = true;
    this.turnLabel.setText(`${u.name} 차례`);
    this.refresh();
    this.time.delayedCall(450, () => {
      const ev = b.enemyAct(u);
      this.animateEnemy(ev, () => this.afterAction());
    });
  }

  afterAction() {
    this.layoutEnemies();
    this.refresh();
    this.time.delayedCall(350, () => this.advance());
  }

  animatePlayer(ev, done) {
    const p = this.player;
    if (ev.skill === "crouch") {
      sfx(this, "block");
      this.say(ev.confused ? "헷갈려서 웅크렸다! 막기 6." : "나비가 웅크렸다. 막기 6.");
      this.tweens.add({ targets: p, scaleY: 3.4, duration: 120, yoyo: true, onComplete: done });
      floatText(this, p.x, p.y - 90, "막기 6", "#9cc8ff");
      return;
    }
    const tgt = ev.target;
    const s = this.sprites.get(tgt.uid);
    this.tweens.add({
      targets: p, x: p.x + 70, duration: 130, yoyo: true,
      onYoyo: () => {
        sfx(this, "slash");
        const fx = this.add.sprite(s.x, s.y - s.displayHeight / 2, "slash").setScale(3).play("slash");
        fx.once("animationcomplete", () => fx.destroy());
        if (ev.dealt > 0) {
          sfx(this, "hit");
          floatText(this, s.x, s.y - s.displayHeight - 10, `-${ev.dealt}`, "#ff8a7a");
          this.flash(s);
        }
        if (ev.absorbed) floatText(this, s.x + 40, s.y - s.displayHeight + 10, `막음 ${ev.absorbed}`, "#9cc8ff", 20);
      },
      onComplete: () => {
        this.say(`${ev.confused ? "헷갈려서 " : ""}나비의 할퀴기! ${tgt.name}에게 ${ev.dealt}${ev.absorbed ? ` (막기로 ${ev.absorbed} 줄임)` : ""}.`);
        if (ev.defeated) this.surrender(ev.defeated, done);
        else done();
      },
    });
  }

  flash(sprite) {
    sprite.setTintFill(0xffffff);
    this.time.delayedCall(90, () => sprite.clearTint());
    if (sprite.texture.key === "boss-idle") {
      sprite.play("boss-hit");
      sprite.once("animationcomplete", () => sprite.play("boss-idle-idle"));
    }
  }

  surrender(units, done) {
    units.forEach((u, k) => {
      const s = this.sprites.get(u.uid);
      if (!s) return;
      this.time.delayedCall(k * 120, () => {
        floatText(this, s.x, s.y - s.displayHeight - 20, u.def.summon ? "물러남" : "항복!", "#ffe27a", 24);
        const puff = this.add.sprite(s.x, s.y - s.displayHeight / 2, "smoke").setScale(3).play("smoke");
        puff.once("animationcomplete", () => puff.destroy());
        this.tweens.add({ targets: s, alpha: 0, y: s.y - 30, duration: 400, onComplete: () => s.destroy() });
        this.sprites.delete(u.uid);
      });
    });
    this.time.delayedCall(450 + units.length * 120, done);
  }

  animateEnemy(ev, done) {
    const u = ev.actor;
    const s = this.sprites.get(u.uid);
    const i = ev.intent;
    const p = this.player;
    const say = (line) => this.say(`${u.name}의 ${i.label}! ${line}`);
    switch (i.kind) {
      case "atk":
        this.tweens.add({
          targets: s, x: s.x - 80, duration: 140, yoyo: true,
          onYoyo: () => {
            sfx(this, ev.dealt > 0 ? "hit" : "block");
            if (ev.dealt > 0) {
              floatText(this, p.x, p.y - 90, `-${ev.dealt}`, "#ff8a7a");
              this.flash(p);
              this.cameras.main.shake(120, 0.004);
            }
            if (ev.absorbed) floatText(this, p.x + 50, p.y - 70, `막음 ${ev.absorbed}`, "#9cc8ff", 20);
            if (ev.bamboo) floatText(this, p.x, p.y - 140, "대나무 잎! 막기 10", "#b9f28a", 22);
          },
          onComplete: () => {
            say(`나비에게 ${ev.dealt}${ev.absorbed ? ` (막기로 ${ev.absorbed} 줄임)` : ""}.`);
            done();
          },
        });
        return;
      case "confuse":
        sfx(this, "move");
        floatText(this, p.x, p.y - 100, "?", "#d3b8ff", 40);
        say("나비가 헷갈렸다. 다음 차례에 다른 기술이 나간다.");
        break;
      case "block":
        sfx(this, "block");
        floatText(this, s.x, s.y - s.displayHeight, `막기 ${i.value}`, "#9cc8ff");
        say(`자기 다음 차례까지 막기 ${i.value}.`);
        break;
      case "shield":
        sfx(this, "block");
        floatText(this, s.x, s.y - s.displayHeight, `보호막 ${i.value}`, "#9cc8ff");
        say(`사라지지 않는 보호막 ${i.value}.`);
        break;
      case "guard":
        sfx(this, "block");
        say(`${ev.mate.name}에게 막기 ${i.value}.`);
        break;
      case "charge":
        floatText(this, s.x, s.y - s.displayHeight, "!", "#ffb35c", 40);
        say(`다음 차례에 ${i.value}짜리 큰 공격이 온다.`);
        break;
      case "summon":
        if (ev.summoned) {
          this.layoutEnemies();
          const m = this.sprites.get(ev.summoned.uid);
          const puff = this.add.sprite(m.x, m.y - 40, "smoke").setScale(3).play("smoke");
          puff.once("animationcomplete", () => puff.destroy());
          say("따라온 무리가 끼어든다.");
        } else say("무리가 이미 곁에 있다.");
        break;
      case "heal":
        sfx(this, "heal");
        floatText(this, s.x, s.y - s.displayHeight, `+${i.value}`, "#b9f28a");
        say(`체력 ${i.value} 회복.`);
        break;
      case "steal":
        sfx(this, "move");
        floatText(this, p.x, p.y - 100, "신발!", "#d3b8ff", 28);
        say("신발을 빼앗겼다. 나비의 다음 두 차례 동안 속도 −2.");
        break;
      case "flee_prep":
        say("슬금슬금 뒷걸음질 친다. 다음 차례에 도망친다!");
        break;
      case "flee":
        this.tweens.add({ targets: s, x: 1100, duration: 500 });
        this.say(`${u.name}이(가) 신발을 들고 도망쳤다…`);
        break;
      default:
        break;
    }
    this.tweens.add({ targets: s, y: s.y - 10, duration: 120, yoyo: true, onComplete: done });
  }

  finish() {
    const b = this.battle;
    const r = this.run;
    r.hp = b.player.hp;
    this.busy = true;
    this.drawButtons();
    if (b.result === "lose") {
      this.time.delayedCall(700, () => this.scene.start("End", { result: "lose" }));
      return;
    }
    if (b.result === "fled") {
      this.time.delayedCall(900, () => this.scene.start("Map", { toast: "야광이 도망쳤다. 보상 없음" }));
      return;
    }
    const reward = REWARD[this.kind];
    let coins = this.kind === "fight" ? this.coins : reward.coins;
    coins += b.enemies.filter((e) => e.def.bonusCoins).reduce((s, e) => s + e.def.bonusCoins, 0);
    const lines = [`경험치 +${reward.xp}`, `엽전 +${coins}`];
    r.coins += coins;
    if (r.relics.includes("porridge")) {
      r.hp = Math.min(r.maxHp, r.hp + 2);
      lines.push("흰죽 한 그릇: 체력 +2");
    }
    if (this.kind === "elite" && r.relics.includes("scale")) {
      r.maxHp += 4;
      r.hp += 4;
      lines.push("용손의 비늘: 최대 체력 +4");
    }
    const ups = gainXp(r, reward.xp);
    if (ups) lines.push(`레벨업! 레벨 ${r.level} · 최대 체력 ${r.maxHp} · 포인트 +${ups}`);
    sfx(this, ups ? "levelup" : "coin");
    if (this.kind === "boss") {
      this.time.delayedCall(600, () => this.scene.start("End", { result: "win", lines }));
      return;
    }
    this.time.delayedCall(500, () => this.rewardModal(lines));
  }

  rewardModal(lines) {
    const m = modal(this, 520, 300);
    const { x, y, w } = m.inner;
    m.add(text(this, x + w / 2, y + 44, "이겼다!", 30, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
    m.add(text(this, x + w / 2, y + 80, "요괴들이 웃으며 친구가 되어 물러났다.", 18, C.muted).setOrigin(0.5));
    m.add(text(this, x + 70, y + 112, lines.join("\n"), 20, C.inkText, { lineSpacing: 8 }));
    m.add(button(this, x + w / 2 - 90, y + 226, 180, 54, this.kind === "elite" ? "유물 고르기" : "지도로", () => {
      if (this.kind === "elite") {
        m.destroy();
        this.eliteRelic();
      } else this.scene.start("Map", {});
    }));
  }

  eliteRelic() {
    const r = this.run;
    const left = Object.keys(RELICS).filter((id) => !r.relics.includes(id));
    Phaser.Utils.Array.Shuffle(left);
    // reuse the map scene's chooser layout
    const m = modal(this, 760, 360);
    const { x, y, w } = m.inner;
    m.add(text(this, x + w / 2, y + 40, "이름난 요괴의 선물 · 유물 하나를 고른다", 24, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
    const ids = left.slice(0, 3);
    if (!ids.length) {
      m.add(button(this, x + w / 2 - 80, y + 260, 160, 54, "지도로", () => this.scene.start("Map", {})));
      return;
    }
    ids.forEach((id, k) => {
      const cx = x + 40 + k * 232;
      m.add(box(this, cx, y + 80, 216, 250, { fill: C.cream, frame: C.woodLight }));
      m.add(this.add.image(cx + 108, y + 140, RELICS[id].icon).setScale(4));
      m.add(text(this, cx + 108, y + 196, RELICS[id].name, 20, C.inkText, { fontStyle: "bold" }).setOrigin(0.5));
      m.add(text(this, cx + 108, y + 236, RELICS[id].text, 16, C.inkText, { wordWrap: { width: 180, useAdvancedWrap: true }, align: "center" }).setOrigin(0.5, 0));
      const zone = this.add.zone(cx, y + 80, 216, 250).setOrigin(0).setInteractive({ useHandCursor: true });
      zone.on("pointerdown", () => {
        r.relics.push(id);
        sfx(this, "coin");
        this.scene.start("Map", { toast: `${RELICS[id].name}을(를) 얻었다` });
      });
      m.add(zone);
    });
  }
}
