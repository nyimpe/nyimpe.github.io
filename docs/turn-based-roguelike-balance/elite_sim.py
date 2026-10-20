"""Monte Carlo check of named yokai (elites) for the cat yokai roguelike plan (post 9).

Same Nabi policy as minion_sim.py: crouch (block 6) when the attacks known
to land before her next turn add up to 6 or more, otherwise hit. She aims at
the leader of a group when it can be hit, else the weakest yokai. Against
a yokai that flees she never crouches and races it instead. Elites
follow fixed action loops, so their next two actions are known.
"""
import random
import statistics

# kind, value; loops repeat from the first entry
ELITES = {
    "백죽모": dict(hp=22, speed=10, loop=[("summon", "무리"), ("atk", 5), ("atk", 5)], leader=True),
    "구업": dict(hp=26, speed=10, loop=[("atk", 9), ("heal", 5), ("block", 8)]),
    "야광": dict(hp=20, speed=12, loop=[("steal", 2), ("atk", 4), ("atk", 4), ("atk", 4), ("flee_prep", 0), ("flee", 0)]),
    "거해": dict(hp=30, speed=8, loop=[("atk", 6), ("atk", 6), ("shield", 6)], shield=12, molt=True),
    "회음": dict(hp=28, speed=12, loop=[("slowatk", 4), ("hide", 0), ("charge", 0), ("atk", 14)]),
    "수부선인": dict(hp=15, speed=10, loop=[("atk", 5), ("allyblock", 6), ("atk", 5)], pair=True),
    "육덕위": dict(hp=30, speed=12, loop=[("hide", 0), ("atk", 12), ("slowatk", 5), ("atk", 6)]),
    "백포건": dict(hp=40, speed=10, loop=[("block", 10), ("summon", "새끼 호랑이"), ("atk", 10)], leader=True),
    "산령": dict(hp=44, speed=8, loop=[("atk", 10), ("block", 8), ("atk", 10)], passive=True),
}
MINIONS = {
    "무리": dict(hp=5, speed=10, loop=[("atk", 2)]),
    "새끼 호랑이": dict(hp=8, speed=12, loop=[("atk", 5)]),
}
AREAS = {
    "마을": (["백죽모", "구업", "야광"], (33, 10, 0)),
    "강": (["거해", "회음", "수부선인"], (39, 12, 14)),
    "산": (["육덕위", "백포건", "산령"], (45, 12, 20)),
}


class Foe:
    def __init__(self, name, spec, t0=None):
        self.name, self.hp, self.max_hp, self.speed = name, spec["hp"], spec["hp"], spec["speed"]
        self.loop, self.i = spec["loop"], 0
        self.leader = spec.get("leader", False)
        self.shield, self.block, self.hidden = spec.get("shield", 0), 0, False
        self.molt, self.molted = spec.get("molt", False), False
        self.passive, self.dig = spec.get("passive", False), 0
        self.bonus = 0
        self.t = 60 / self.speed if t0 is None else t0

    def intents(self, n=2):
        if self.passive:
            return [("dig", 0)] * n
        return [self.loop[(self.i + k) % len(self.loop)] for k in range(n)]


def hit(foe, dmg):
    if foe.hidden:
        return
    take = min(dmg, foe.block)
    foe.block -= take
    dmg -= take
    take = min(dmg, foe.shield)
    foe.shield -= take
    dmg -= take
    foe.hp -= dmg
    if foe.molt and not foe.molted and foe.shield == 0 and take > 0:
        foe.molted, foe.speed, foe.bonus = True, foe.speed + 4, 3
    if foe.passive:
        foe.passive = False


def run(area, name):
    hp, speed, dash = AREAS[area][1]
    start = hp
    spec = ELITES[name]
    foes = [Foe(name, spec)]
    if spec.get("pair"):
        foes.append(Foe(name, spec))
    t_n, block, cooldown, slow, stolen, turns = 60 / speed, 0, 0, 0, 0, 0
    fled = False
    while hp > 0 and turns < 80:
        alive = [f for f in foes if f.hp > 0]
        main = [f for f in alive if f.name == name]
        if not main:
            break
        nxt = min(alive, key=lambda f: f.t)
        if t_n <= nxt.t:
            block = 0
            interval = 120 / max(2, speed - slow - (2 if stolen else 0))
            stolen = max(0, stolen - 1)
            incoming = 0
            for f in alive:
                tf, k = f.t, 0
                for kind, value in f.intents(3):
                    if tf >= t_n + interval:
                        break
                    if kind in ("atk", "slowatk"):
                        incoming += value + f.bonus + (f.dig if kind == "atk" and k == 0 else 0)
                    tf += 120 / f.speed
                    k += 1
            cooldown = max(0, cooldown - 1)
            can_dash = dash and cooldown == 0
            visible = [f for f in alive if not f.hidden]
            racing = any(k == "flee" for f in alive for k, _ in f.loop)
            if (incoming >= 6 and not racing) or not visible:
                block = 6
            else:
                leaders = [f for f in visible if f.leader]
                target = leaders[0] if leaders else min(visible, key=lambda f: f.hp)
                if can_dash:
                    hit(target, dash)
                    cooldown = 3
                else:
                    hit(target, 6)
            t_n += interval
            turns += 1
        else:
            f = nxt
            f.block, f.hidden = 0, False
            if f.passive:
                f.dig = min(9, f.dig + 3)
                f.t += 120 / f.speed
                continue
            kind, value = f.loop[f.i % len(f.loop)]
            f.i += 1
            if kind in ("atk", "slowatk"):
                dmg = value + f.bonus + f.dig
                f.dig = 0
                hp -= max(0, dmg - block)
                block = max(0, block - dmg)
                if kind == "slowatk":
                    slow = 2
            elif kind == "block":
                f.block = value
            elif kind == "shield":
                if not f.molted:
                    f.shield += value
            elif kind == "heal":
                f.hp = min(f.max_hp, f.hp + value)
            elif kind == "hide":
                f.hidden = True
            elif kind == "allyblock":
                mates = [m for m in foes if m.hp > 0 and m is not f] or [f]
                mates[0].block += value
            elif kind == "summon":
                if sum(1 for m in foes if m.hp > 0 and m.name == value) < 1:
                    foes.append(Foe(value, MINIONS[value], t0=f.t + 120 / MINIONS[value]["speed"] / 2))
            elif kind == "steal":
                stolen = value
            elif kind == "flee":
                fled = True
                break
            f.t += 120 / f.speed
            # partner rage for the dragon palace guards
            if spec.get("pair"):
                pair = [m for m in foes if m.name == name]
                if sum(1 for m in pair if m.hp > 0) == 1:
                    for m in pair:
                        m.bonus = 2
    won = hp > 0 and not fled and not [f for f in foes if f.name == name and f.hp > 0]
    return start - max(hp, 0), won, fled, turns


if __name__ == "__main__":
    random.seed(2)
    for area, (names, _) in AREAS.items():
        for name in names:
            rs = [run(area, name) for _ in range(500)]
            lost = statistics.mean(r[0] for r in rs)
            win = sum(r[1] for r in rs) / len(rs)
            fled = sum(r[2] for r in rs) / len(rs)
            turns = statistics.mean(r[3] for r in rs)
            print(f"{area}\t{name}\tlost {lost:.1f}\twin {win:.0%}\tfled {fled:.0%}\tturns {turns:.1f}")
