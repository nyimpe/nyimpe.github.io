"""Rough leader-fight check for the cat yokai roguelike plan (posts 4, 6 and 7).

Nabi reads the turn bar: she crouches (block 6) on the turn right before a
hit of 10 or more, uses dash whenever it is off cooldown, and scratches
otherwise. Status effects other than slow are not modelled.
"""


def fight(boss_hp, boss_speed, pattern, nabi_speed, nabi_hp, dash):
    t_n, t_b = 60 / nabi_speed, 60 / boss_speed
    hp, bhp, block, bblock, i, turns, cooldown, slow = nabi_hp, boss_hp, 0, 0, 0, 0, 0, 0
    while hp > 0 and bhp > 0 and turns < 60:
        if t_n <= t_b:
            block = 0
            next_time = t_n + 120 / max(1, nabi_speed - slow)
            upcoming, tb, j = [], t_b, i
            while tb < next_time:
                upcoming.append(pattern[j % len(pattern)])
                tb += 120 / boss_speed
                j += 1
            big = any(kind in ("atk", "slowatk") and value >= 10 for kind, value in upcoming)
            cooldown = max(0, cooldown - 1)
            if big:
                block = 6
            elif dash and cooldown == 0:
                bhp -= max(0, dash - bblock)
                bblock, cooldown = 0, 3
            else:
                bhp -= max(0, 6 - bblock)
                bblock = 0
            t_n = next_time
            turns += 1
        else:
            bblock = 0
            kind, value = pattern[i % len(pattern)]
            if kind in ("atk", "slowatk"):
                hp -= max(0, value - block)
                block = max(0, block - value)
                if kind == "slowatk":
                    slow = 2
            elif kind == "block":
                bblock = value
            i += 1
            t_b += 120 / boss_speed
    return hp, bhp, turns


VILLAGE = [("atk", 8), ("trick", 0), ("block", 10)]
RIVER = [("slowatk", 5), ("atk", 10), ("charge", 0), ("atk", 18)]

if __name__ == "__main__":
    print("village, no skill, hp 30:", fight(40, 10, VILLAGE, 10, 30, 0))
    print("village, no skill, hp 36:", fight(40, 10, VILLAGE, 10, 36, 0))
    for hp in (30, 36, 39):
        for dash in (14, 20):
            print(f"river, dash {dash}, hp {hp}:", fight(55, 8, RIVER, 12, hp, dash))
