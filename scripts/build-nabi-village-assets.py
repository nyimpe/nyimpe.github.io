"""Copy and prepare Ninja Adventure (CC0) assets for the Nabi village prototype.

Usage: python3 scripts/build-nabi-village-assets.py "<path to Ninja Adventure - Asset Pack>"

The pack itself is not stored in the repository. This script copies only the
sprites, UI pieces and sounds the prototype uses into
src/games/nabi-village/assets/, recolours the frog gold, and composes the
battle and map backgrounds from the nature tileset.
"""
import random
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

PACK = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "src/games/nabi-village/assets"
OUT.mkdir(parents=True, exist_ok=True)
A = PACK / "Actor"

COPIES = {
    # hero and village yokai: sprite sheet + 38x38 portrait
    "nabi.png": A / "Animal/CatOrange/SpriteSheet.png",
    "nabi-face.png": A / "Animal/CatOrange/Faceset.png",
    "dokkaebi.png": A / "Character/DemonRed/SpriteSheet.png",
    "dokkaebi-face.png": A / "Character/DemonRed/Faceset.png",
    "dog.png": A / "Animal/Dog/SpriteSheet.png",
    "dog-face.png": A / "Animal/Dog/Faceset.png",
    "oldman.png": A / "Character/OldMan3/SpriteSheet.png",
    "oldman-face.png": A / "Character/OldMan3/Faceset.png",
    "mob.png": A / "Character/Villager2/SpriteSheet.png",
    "mob-face.png": A / "Character/Villager2/Faceset.png",
    "donkey.png": A / "Animal/Donkey/SpriteSheetGrey.png",
    "horse-face.png": A / "Animal/Horse/FacesetBrown.png",
    "donkey-face.png": A / "Animal/Donkey/FacesetGrey.png",
    "spirit.png": A / "Character/Spirit/SpriteSheet.png",
    "spirit-face.png": A / "Character/Spirit/Faceset.png",
    "boss-idle.png": A / "Boss/DemonCyclop/Idle.png",
    "boss-hit.png": A / "Boss/DemonCyclop/Hit.png",
    "boss-face.png": A / "Boss/DemonCyclop/Faceset.png",
    # effects, items and UI
    "slash.png": PACK / "FX/Slash/SpriteSheetSlash01.png",
    "smoke.png": PACK / "FX/Smoke/Smoke/SpriteSheet.png",
    "chest.png": PACK / "Items/Treasure/LittleTreasureChest.png",
    "coin.png": PACK / "Items/Treasure/GoldCoin.png",
    "onigiri.png": PACK / "Items/Food/Onigiri.png",
    "branch.png": PACK / "Items/Resource/Branch.png",
    "feather.png": PACK / "Items/Resource/feather.png",
    "iron.png": PACK / "Items/Resource/BarIron.png",
    "gem.png": PACK / "Items/Resource/GemGreen.png",
    "grass.png": PACK / "Items/Resource/Grass.png",
    "gourd.png": PACK / "Items/Object/Gourd.png",
    "panel.png": PACK / "Ui/Theme/Theme Wood/nine_path_bg.png",
    "button.png": PACK / "Ui/Theme/Theme Wood/button_normal.png",
    "button-hover.png": PACK / "Ui/Theme/Theme Wood/button_hover.png",
    "button-disabled.png": PACK / "Ui/Theme/Theme Wood/button_disabled.png",
    "cell.png": PACK / "Ui/Theme/Theme Wood/inventory_cell.png",
    # sounds and music
    "hit.wav": PACK / "Audio/Sounds/Hit & Impact/Hit1.wav",
    "slash.wav": PACK / "Audio/Sounds/Whoosh & Slash/Slash.wav",
    "block.wav": PACK / "Audio/Sounds/Hit & Impact/Impact.wav",
    "select.wav": PACK / "Audio/Sounds/Menu/Accept.wav",
    "move.wav": PACK / "Audio/Sounds/Menu/Move1.wav",
    "coin.wav": PACK / "Audio/Sounds/Bonus/Coin.wav",
    "levelup.wav": PACK / "Audio/Sounds/Bonus/PowerUp1.wav",
    "heal.wav": PACK / "Audio/Sounds/Magic & Skill/Heal.wav",
    "village.ogg": PACK / "Audio/Musics/4 - Village.ogg",
    "fight.ogg": PACK / "Audio/Musics/17 - Fight.ogg",
}

for name, src in COPIES.items():
    shutil.copyfile(src, OUT / name)


def gold(src, dst):
    """Recolour the green frog into a golden toad."""
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and g > r + 10 and g > b + 10:
                lum = (r + g + b) / 3
                if lum < 70:
                    px[x, y] = (120, 74, 18, a)
                elif lum < 120:
                    px[x, y] = (196, 132, 30, a)
                elif lum < 170:
                    px[x, y] = (238, 180, 48, a)
                else:
                    px[x, y] = (255, 226, 112, a)
    im.save(dst)


gold(A / "Animal/Frog/SpriteSheet.png", OUT / "toad.png")
gold(A / "Animal/Frog/Faceset.png", OUT / "toad-face.png")

nature = Image.open(PACK / "Backgrounds/Tilesets/TilesetNature.png").convert("RGBA")
PIECES = {
    "tree": (0, 0, 32, 32),
    "pine": (32, 0, 64, 32),
    "triple": (64, 32, 128, 80),
    "blossom": (192, 32, 256, 80),
    "pink": (0, 288, 48, 336),
    "orange": (144, 288, 192, 336),
}
piece = {k: nature.crop(v) for k, v in PIECES.items()}
GRASS, GRASS_DARK, GRASS_LIGHT = (150, 190, 82), (128, 170, 66), (176, 208, 104)
DIRT, DIRT_DARK = (222, 182, 124), (198, 156, 102)


def grass_field(w, h, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (w, h), GRASS + (255,))
    d = ImageDraw.Draw(im)
    for _ in range(w * h // 18):
        x, y = rnd.randrange(w), rnd.randrange(h)
        d.point((x, y), fill=rnd.choice([GRASS_DARK, GRASS_LIGHT]))
    for _ in range(w * h // 260):
        x, y = rnd.randrange(w), rnd.randrange(h)
        d.line([x, y, x + 1, y - 2], fill=GRASS_DARK)
    return im, d, rnd


# battle background: 320x120, scaled x3 to 960x360 in game
bg, d, rnd = grass_field(320, 120, 7)
d.rectangle([0, 70, 320, 104], fill=DIRT)
for x in range(0, 320, 3):
    d.point((x, 70 + rnd.randrange(2)), fill=DIRT_DARK)
    d.point((x + 1, 103 - rnd.randrange(2)), fill=DIRT_DARK)
for _ in range(60):
    d.point((rnd.randrange(320), rnd.randrange(72, 102)), fill=DIRT_DARK)
row = [("blossom", -14, -10), ("tree", 46, -2), ("triple", 74, -18), ("pine", 136, -4), ("pink", 164, -14),
       ("tree", 210, -2), ("blossom", 236, -12), ("pine", 296, -6)]
for name, x, y in row:
    bg.alpha_composite(piece[name], (x, y)) if x >= 0 and y >= 0 else bg.paste(piece[name], (x, y), piece[name])
for name, x, y in [("orange", -16, 92), ("tree", 300, 98)]:
    bg.paste(piece[name], (x, y), piece[name])
bg.save(OUT / "bg-battle.png")

# map background: 320x214, scaled x3 to 960x642 in game
mp, d, rnd = grass_field(320, 214, 11)
for name, x, y in [("blossom", -20, -14), ("pine", 40, -8), ("tree", 270, -6), ("pink", 286, 20),
                   ("triple", -24, 70), ("tree", 8, 150), ("orange", -10, 180), ("blossom", 280, 120),
                   ("pine", 296, 170), ("tree", 250, 190), ("pink", 200, -20)]:
    mp.paste(piece[name], (x, y), piece[name])
mp.save(OUT / "bg-map.png")

(OUT / "CREDITS.md").write_text(
    "# Assets\n\n"
    "Sprites, UI, effects, sounds and music come from the Ninja Adventure Asset Pack by Pixel-boy and AAA,\n"
    "released under CC0 1.0 (https://pixel-boy.itch.io/ninja-adventure-asset-pack).\n"
    "toad.png and toad-face.png are recoloured from the pack's frog. bg-battle.png and bg-map.png are\n"
    "composed from the pack's nature tileset by scripts/build-nabi-village-assets.py.\n",
    encoding="utf-8",
)
print("wrote", len(list(OUT.iterdir())), "files to", OUT)
