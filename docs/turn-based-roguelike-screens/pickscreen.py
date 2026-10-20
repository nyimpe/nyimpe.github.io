"""Pixel mockup of the skill pick screen after beating the village leader."""
import sys
from PIL import Image, ImageDraw
from battle import W, H, S, INK, CREAM, CREAM_D, BROWN, BROWN_D, font, outline


def village(d):
    bands = [(255, 206, 160), (255, 218, 176), (255, 228, 192), (255, 238, 210)]
    for i, c in enumerate(bands):
        d.rectangle([0, 12 + i * 12, W, 24 + i * 12], fill=c)
    d.rectangle([0, 60, W, 78], fill=(214, 196, 160))
    # far hills
    for x in range(W):
        y = 52 + int(4 * __import__("math").sin(x / 19))
        d.line([x, y, x, 60], fill=(170, 196, 140))
    # hanok houses: white walls, wooden posts, curved tiled roofs
    for x0, w in [(120, 70), (230, 84)]:
        d.rectangle([x0, 46, x0 + w, 62], fill=(244, 238, 222))
        for px in range(x0, x0 + w + 1, 14):
            d.rectangle([px, 46, px + 1, 62], fill=(140, 90, 56))
        d.polygon([(x0 - 10, 46), (x0 - 6, 38), (x0 + w + 6, 38), (x0 + w + 10, 46)], fill=(86, 92, 110))
        d.line([x0 - 10, 46, x0 + w + 10, 46], fill=(60, 64, 80))
        d.line([x0 - 12, 44, x0 - 10, 46], fill=(60, 64, 80))
        d.line([x0 + w + 12, 44, x0 + w + 10, 46], fill=(60, 64, 80))
        for rx in range(x0 - 6, x0 + w + 6, 4):
            d.line([rx, 39, rx, 45], fill=(100, 106, 126))
    # stone wall
    for x in range(0, W, 8):
        d.rectangle([x, 62, x + 7, 66], fill=(176, 170, 160), outline=(140, 134, 126))


def dokkaebi():
    lay = Image.new("RGBA", (56, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    skin, shade = (112, 162, 226), (84, 126, 198)
    # club over the shoulder
    d.polygon([(34, 20), (52, 2), (55, 6), (38, 24)], fill=(150, 98, 56))
    for x, y in [(48, 6), (45, 10), (51, 9), (42, 14)]:
        d.point((x, y), fill=(200, 200, 210))
    # legs and baggy trousers
    d.rectangle([14, 46, 23, 58], fill=(176, 120, 70))
    d.rectangle([27, 46, 36, 58], fill=(176, 120, 70))
    d.rectangle([13, 57, 24, 60], fill=skin)
    d.rectangle([26, 57, 37, 60], fill=skin)
    # belly and vest
    d.ellipse([10, 26, 40, 50], fill=skin)
    d.ellipse([16, 32, 34, 48], fill=(160, 196, 240))
    d.polygon([(10, 34), (16, 28), (18, 46), (11, 44)], fill=(80, 150, 100))
    d.polygon([(40, 34), (34, 28), (32, 46), (39, 44)], fill=(80, 150, 100))
    # waving arm and club arm
    d.ellipse([2, 18, 10, 30], fill=skin)
    d.ellipse([1, 14, 8, 21], fill=skin)
    d.ellipse([36, 22, 44, 32], fill=skin)
    # head
    d.ellipse([10, 4, 40, 30], fill=skin)
    d.pieslice([10, 4, 40, 30], 200, 340, fill=shade)
    d.ellipse([10, 6, 40, 30], fill=skin)
    # hair tuft and horn
    for hx in range(14, 37, 4):
        d.polygon([(hx, 9), (hx + 2, 2), (hx + 4, 9)], fill=(60, 50, 70))
    d.polygon([(23, 4), (25, -2), (28, 4)], fill=(250, 210, 90))
    # face
    d.ellipse([15, 12, 22, 19], fill=(255, 255, 255))
    d.ellipse([28, 12, 35, 19], fill=(255, 255, 255))
    d.rectangle([18, 14, 20, 17], fill=INK)
    d.rectangle([30, 14, 32, 17], fill=INK)
    d.chord([16, 16, 34, 28], 0, 180, fill=(150, 40, 50))
    d.polygon([(19, 22), (21, 22), (20, 25)], fill=(255, 255, 255))
    d.polygon([(29, 22), (31, 22), (30, 25)], fill=(255, 255, 255))
    d.ellipse([12, 19, 16, 22], fill=(240, 140, 160))
    d.ellipse([34, 19, 38, 22], fill=(240, 140, 160))
    return outline(lay)


def dog_icon():
    lay = Image.new("RGBA", (34, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    red, black = (206, 82, 58), (52, 44, 52)
    # tail curling up
    d.arc([1, 2, 9, 12], 150, 330, fill=red, width=2)
    # legs
    for lx in (7, 11, 18, 22):
        d.rectangle([lx, 15, lx + 2, 21], fill=red)
        d.rectangle([lx, 20, lx + 2, 21], fill=black)
    # body with a black saddle patch
    d.rounded_rectangle([5, 8, 25, 17], radius=4, fill=red)
    d.ellipse([10, 8, 18, 13], fill=black)
    # head, ear and snout
    d.ellipse([20, 3, 30, 12], fill=red)
    d.polygon([(21, 5), (22, -1), (25, 4)], fill=black)
    d.rectangle([28, 8, 32, 11], fill=red)
    d.point((32, 8), fill=INK)
    d.point((26, 6), fill=INK)
    return outline(lay)


def horse_icon():
    lay = Image.new("RGBA", (34, 26), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    blue, mane = (90, 150, 222), (240, 248, 255)
    d.ellipse([4, 9, 24, 19], fill=blue)
    d.polygon([(18, 12), (24, 2), (28, 4), (24, 14)], fill=blue)
    d.polygon([(24, 2), (32, 6), (31, 9), (25, 7)], fill=blue)
    d.polygon([(20, 8), (23, 1), (25, 2), (22, 10)], fill=mane)
    d.point((28, 4), fill=INK)
    for lx in (6, 10, 17, 21):
        d.rectangle([lx, 18, lx + 1, 24], fill=(60, 96, 170))
    d.polygon([(4, 11), (0, 18), (2, 19), (6, 13)], fill=mane)
    return outline(lay)


def turtle_icon():
    lay = Image.new("RGBA", (36, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for lx in (7, 20):
        d.ellipse([lx, 16, lx + 6, 21], fill=(150, 196, 120))
    d.chord([4, 4, 28, 26], 180, 360, fill=(84, 150, 92))
    d.line([6, 15, 26, 15], fill=(60, 110, 70))
    for x in (10, 16, 22):
        d.line([x, 8, x, 15], fill=(60, 110, 70))
    d.ellipse([24, 9, 33, 16], fill=(150, 196, 120))
    d.point((30, 11), fill=INK)
    lay = outline(lay)
    d = ImageDraw.Draw(lay)
    for x, y in [(2, 4), (32, 2), (34, 7), (1, 10)]:
        d.point([(x, y), (x + 1, y), (x, y + 1)], fill=(255, 255, 255))
    return lay


CARDS = [
    {"name": "개 재주", "src": "귀구", "icon": dog_icon, "band": (200, 76, 56), "does": "막고, 막은 만큼 되갚는다",
     "first": "되갚기 · 막기 8", "road": "이름난 요괴를 미리 안다", "branch": "짝꿍 / 버티기"},
    {"name": "말 재주", "src": "용마", "icon": horse_icon, "band": (90, 150, 222), "does": "먼저 움직이고 여러 번 친다",
     "first": "돌진 · 피해 14", "road": "칸 하나를 건너뛴다", "branch": "돌진 / 잰걸음"},
    {"name": "거북 재주", "src": "현구", "icon": turtle_icon, "band": (84, 150, 92), "does": "흰 기운으로 지키고 낫게 한다",
     "first": "등껍질 · 보호막 6", "road": "쉬는 칸에서 더 회복한다", "branch": "등껍질 / 흰 기운"},
]
SELECTED = 1


def main():
    lo = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(lo)
    village(d)
    d.rectangle([0, 72, W, H], fill=CREAM)
    d.rectangle([0, 72, W, 73], fill=CREAM_D)
    gob = dokkaebi()
    lo.alpha_composite(gob, (10, 10))
    boxes = []
    for i, c in enumerate(CARDS):
        x0 = 8 + i * 103
        y0 = 78 if i != SELECTED else 75
        box = [x0, y0, x0 + 98, y0 + 96]
        boxes.append(box)
        if i == SELECTED:
            d.rectangle([box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3], fill=INK)
            d.rectangle([box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2], fill=(255, 196, 40))
        d.rectangle(box, fill=INK)
        d.rectangle([box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1], fill=(255, 252, 242))
        d.rectangle([box[0] + 1, box[1] + 1, box[2] - 1, box[1] + 4], fill=c["band"])
        d.rectangle([box[0] + 6, box[1] + 9, box[0] + 40, box[1] + 35], fill=(244, 236, 214))
        ic = c["icon"]()
        lo.alpha_composite(ic, (box[0] + 23 - ic.width // 2, box[1] + 22 - ic.height // 2))
    # locked reroll button
    d.rectangle([222, 28, 314, 42], fill=(214, 206, 190), outline=(150, 130, 100))
    d.rectangle([226, 33, 231, 38], fill=(150, 130, 100))
    d.arc([226, 29, 231, 35], 180, 360, fill=(150, 130, 100))
    # HUD
    d.rectangle([0, 0, W, 11], fill=(255, 250, 236))
    d.line([0, 11, W, 11], fill=BROWN)
    d.ellipse([289, 2, 296, 9], fill=(250, 200, 60), outline=BROWN_D)
    d.rectangle([292, 5, 293, 6], fill=BROWN_D)

    big = lo.resize((W * S, H * S), Image.NEAREST).convert("RGB")
    t = ImageDraw.Draw(big)

    def text(xy, s, size, fill=INK, bold=True, anchor="la"):
        t.text((xy[0] * S, xy[1] * S), s, font=font(size, bold), fill=fill, anchor=anchor)

    text((4, 1.6), "마을 · 우두머리를 이겼다", 26)
    text((160, 1.6), "재주 고르기", 26, anchor="ma")
    text((250, 1.6), "꼬리 3", 26)
    text((298, 1.6), "58", 26)

    sx, sy = 66, 22
    t.polygon([((sx + 1) * S, (sy + 8) * S), ((sx - 6) * S, (sy + 12) * S), ((sx + 1) * S, (sy + 12) * S)], fill=INK)
    t.rounded_rectangle([sx * S, sy * S, (sx + 116) * S, (sy + 22) * S], radius=12, fill=(255, 255, 255), outline=INK, width=4)
    t.text(((sx + 5) * S, (sy + 3) * S), "도깨비 김서방", font=font(20), fill=(70, 110, 190))
    t.text(((sx + 5) * S, (sy + 10.5) * S), "졌다, 졌어! 재주 하나 가르쳐 줄게.", font=font(23), fill=INK)
    text((234, 32), "다시 뽑기 · 꼬리 4에서 열림", 19, fill=(130, 110, 90), bold=False)

    for c, b in zip(CARDS, boxes):
        x0, y0 = b[0], b[1]
        text((x0 + 44, y0 + 10), c["name"], 30)
        text((x0 + 44, y0 + 19.5), f"{c['src']}에게 배움", 19, fill=(130, 110, 90), bold=False)
        text((x0 + 6, y0 + 40), c["does"], 21)
        rows = [("첫 기술", c["first"], c["band"]), ("길 위에서", c["road"], (110, 90, 70)), ("두 갈래", c["branch"], (110, 90, 70))]
        for k, (label, value, col) in enumerate(rows):
            text((x0 + 6, y0 + 50 + k * 14), label, 18, fill=(150, 130, 110), bold=False)
            text((x0 + 6, y0 + 55.5 + k * 14), value, 21, fill=col)
    big.save(sys.argv[1])


if __name__ == "__main__":
    main()
