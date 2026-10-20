"""Monte Carlo check of ordinary yokai groups for the cat yokai roguelike plan (post 8).

Nabi reads the turn bar: if the attacks known to land before her next turn
add up to 6 or more she crouches (block 6); otherwise she hits the weakest
visible yokai, with dash (14, two-turn cooldown) when she has it. Turn order
follows post 6: interval = 120 / speed, everyone starts at half an interval,
ties go to Nabi. Yokai pick actions by weight and never repeat one three
times in a row.
"""
import random
import statistics

YOKAI = {
    # name: (hp, speed, [(weight, action, value), ...])
    "도깨비": (10, 12, [(50, "atk", 4), (30, "confuse", 0), (20, "block", 4)]),
    "귀구": (8, 10, [(60, "atk", 3), (40, "guard", 4)]),
    "금두꺼비": (14, 8, [(50, "atk", 4), (30, "shield", 4), (20, "charge", 8)]),
    "가사어": (8, 12, [(60, "atk", 3), (40, "slow", 0)]),
    "자라": (20, 8, [(40, "atk", 5), (35, "block", 8), (25, "charge", 9)]),
    "용마": (18, 12, [(50, "atk", 6), (30, "atk2", 4), (20, "charge", 10)]),
    "목객": (12, 12, [(50, "atk", 5), (30, "hide", 0), (20, "confuse", 0)]),
    "현구": (34, 8, [(40, "atk", 8), (30, "shield", 8), (30, "slowatk", 5)]),
    "삼각록": (18, 12, [(50, "atk", 8), (25, "pull", 5), (25, "heal", 4)]),
}

GROUPS = {
    "마을": [["도깨비"], ["귀구", "귀구"], ["금두꺼비"], ["금두꺼비", "귀구"]],
    "강": [["가사어", "가사어", "가사어"], ["자라", "가사어"], ["용마"], ["자라"]],
    "산": [["목객", "목객"], ["현구"], ["삼각록", "목객"], ["삼각록"]],
}

NABI = {"마을": (30, 10, 0), "강": (36, 12, 14), "산": (42, 12, 14)}  # hp, speed, dash


class Yokai:
    def __init__(self, name):
        hp, speed, actions = YOKAI[name]
        self.name, self.hp, self.speed, self.actions = name, hp, speed, actions
        self.block = self.shield = 0
        self.hidden = False
        self.history = []
        self.charged = None
        self.t = 60 / speed
        self.intent = self.pick()

    def pick(self):
        if self.charged is not None:
            return ("atk", self.charged)
        while True:
            w, kind, value = random.choices(self.actions, weights=[a[0] for a in self.actions])[0]
            if self.history[-2:] != [kind, kind]:
                return (kind, value)


def run(area, group):
    hp, speed, dash = NABI[area]
    start_hp = hp
    foes = [Yokai(n) for n in group]
    t_n, block, cooldown, slow, confused, turns = 60 / speed, 0, 0, 0, False, 0
    while hp > 0 and any(f.hp > 0 for f in foes) and turns < 80:
        alive = [f for f in foes if f.hp > 0]
        nxt = min(alive, key=lambda f: f.t)
        if t_n <= nxt.t:
            block = 0
            for f in alive:
                if f.hidden and f.t > t_n:
                    pass
            interval = 120 / max(2, speed - slow)
            incoming = sum(f.intent[1] * (2 if f.intent[0] == "atk2" else 1)
                           for f in alive if f.t < t_n + interval and f.intent[0] in ("atk", "atk2", "slowatk"))
            cooldown = max(0, cooldown - 1)
            options = ["scratch", "crouch"] + (["dash"] if dash and cooldown == 0 else [])
            if confused:
                choice = random.choice(options)
                confused = False
            elif incoming >= 6:
                choice = "crouch"
            else:
                choice = "dash" if "dash" in options else "scratch"
            targets = [f for f in alive if not f.hidden] or alive
            target = min(targets, key=lambda f: f.hp)
            if choice == "crouch":
                block = 6
            elif not target.hidden:
                dmg = dash if choice == "dash" else 6
                if choice == "dash":
                    cooldown = 3
                absorbed = min(dmg, target.block + target.shield)
                take_block = min(dmg, target.block)
                target.block -= take_block
                target.shield -= max(0, absorbed - take_block)
                target.hp -= dmg - absorbed
            t_n += interval
            turns += 1
        else:
            f = nxt
            f.block, f.hidden = 0, False
            kind, value = f.intent
            f.history.append(kind)
            f.charged = None
            if kind in ("atk", "slowatk"):
                hp -= max(0, value - block)
                block = max(0, block - value)
                if kind == "slowatk":
                    slow = 2
            elif kind == "atk2":
                for _ in range(2):
                    hp -= max(0, value - block)
                    block = max(0, block - value)
            elif kind == "confuse":
                confused = True
            elif kind == "slow":
                slow = 2
            elif kind == "block":
                f.block = value
            elif kind == "shield":
                f.shield += value
            elif kind == "guard":
                mates = [m for m in foes if m.hp > 0 and m is not f] or [f]
                mates[0].block += value
            elif kind == "charge":
                f.charged = value
            elif kind == "hide":
                f.hidden = True
            elif kind == "heal":
                for m in foes:
                    if m.hp > 0:
                        m.hp = min(YOKAI[m.name][0], m.hp + value)
            f.t += 120 / f.speed - (value if kind == "pull" else 0)
            f.intent = f.pick()
    return start_hp - max(hp, 0), hp > 0, turns


if __name__ == "__main__":
    random.seed(1)
    for area, groups in GROUPS.items():
        for group in groups:
            results = [run(area, group) for _ in range(2000)]
            lost = statistics.mean(r[0] for r in results)
            win = sum(r[1] for r in results) / len(results)
            turns = statistics.mean(r[2] for r in results)
            print(f"{area}\t{'+'.join(group)}\tlost {lost:.1f}\twin {win:.0%}\tturns {turns:.1f}")
