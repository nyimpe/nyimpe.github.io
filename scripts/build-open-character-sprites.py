#!/usr/bin/env python3
"""Rebuild the sprite post's previews and downloads from collected CC0 originals.

Requires Pillow. No network requests; source URLs, hashes, crops, and reflections
are recorded in public/posts/open-character-sprites/catalog.json.
"""
import hashlib
import io
import json
import math
from functools import lru_cache
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageOps, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "public/posts/open-character-sprites"
ORDER = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
CELL_W, CELL_H = 144, 164
BACKGROUND = (231, 236, 242)
FONT = ImageFont.load_default(size=14)


@lru_cache(maxsize=512)
def source_image(reference):
    filename, separator, member = reference.partition("!")
    if separator:
        with ZipFile(ASSETS / filename) as archive:
            data = archive.read(member)
    else:
        data = (ASSETS / filename).read_bytes()
    image = Image.open(io.BytesIO(data)).convert("RGBA")
    # Only this original has an opaque two-color cell background.
    if filename.endswith("/Skeleton.png"):
        image.putdata([
            (*pixel[:3], 0) if pixel[:3] in {(54, 81, 64), (81, 73, 54)} else pixel
            for pixel in image.getdata()
        ])
    return image


def sprite(frame):
    image = source_image(frame["file"])
    x, y, width, height = frame["rect"]
    assert x >= 0 and y >= 0 and x + width <= image.width and y + height <= image.height
    result = image.crop((x, y, x + width, y + height))
    if frame.get("flip"):
        result = ImageOps.mirror(result)
    assert result.getbbox(), frame
    return result


def render(preview):
    sequences = preview["sequences"]
    order = ORDER if len(sequences) == 8 else ["S", "E", "N", "W"]
    assert set(order) == set(sequences)
    count = math.lcm(*(len(sequence) for sequence in sequences.values()))
    frames = []
    for tick in range(count):
        canvas = Image.new("RGB", (CELL_W * 4, CELL_H * (len(order) // 4)), BACKGROUND)
        draw = ImageDraw.Draw(canvas)
        for index, direction in enumerate(order):
            x, y = index % 4 * CELL_W, index // 4 * CELL_H
            sequence = sequences[direction]
            image = sprite(sequence[tick % len(sequence)])
            scale = min(6, max(1, 128 // max(image.size)))
            image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
            canvas.paste(image, (x + (CELL_W - image.width) // 2, y + (138 - image.height) // 2), image)
            draw.text((x + CELL_W / 2, y + 144), direction, fill=(40, 49, 65), font=FONT, anchor="mt")
        frames.append(canvas)
    assert len({frame.tobytes() for frame in frames}) > 1, preview["id"]
    return frames


def write_zip(path, files):
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo(name, date_time=(2026, 10, 27, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, data)


def main():
    catalog = json.loads((ASSETS / "catalog.json").read_text())
    downloads = ASSETS / "downloads"
    downloads.mkdir(exist_ok=True)
    credits = [
        "Collected character sprite assets — checked 2026-10-27",
        "All listed downloaded artwork: CC0 1.0 Universal",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        "Attribution is not required by CC0; creators are credited here voluntarily.",
        "This applies to the listed files, not every linked product by an author.",
        "GIFs: custom preview timing, integer nearest-neighbor enlargement,",
        "reflections where documented, Skeleton cell background removal.",
        "Original downloaded files are unchanged. Not tested inside a game engine.",
        "",
    ]
    all_files = {}
    hero_tiles = []
    report = []
    for pack in catalog["packs"]:
        pack_credit = [f'{pack["title"]} — {pack["author"]}', pack["source"], "CC0-1.0", pack["license_url"], pack["note"]]
        files = {}
        for original in pack["originals"]:
            data = (ASSETS / original["file"]).read_bytes()
            assert hashlib.sha256(data).hexdigest() == original["sha256"]
            assert len(data) == original["bytes"]
            name = Path(original["file"]).name
            files[name] = data
            pack_credit.extend([f'File: {name}', f'Source: {original["url"]}', f'SHA256: {original["sha256"]}'])
        files["CREDITS.txt"] = ("\n".join(pack_credit) + "\n").encode()
        credits.extend(pack_credit + [""])
        write_zip(downloads / f'{pack["id"]}.zip', files)
        all_files.update({f'{pack["id"]}/{name}': data for name, data in files.items()})
        for preview in pack["previews"]:
            name = f'{pack["id"]}-{preview["id"]}'
            frames = render(preview)
            frames[0].save(ASSETS / f'{name}.png', optimize=True)
            frames[0].save(ASSETS / f'{name}.gif', save_all=True, append_images=frames[1:], duration=preview["duration_ms"], loop=0, disposal=2, optimize=False)
            with Image.open(ASSETS / f'{name}.gif') as gif:
                assert gif.n_frames > 1 and gif.info["loop"] == 0
                for index in range(gif.n_frames):
                    gif.seek(index)
                    assert gif.info.get("duration", 0) > 0
                report.append({"id": name, "frames": gif.n_frames, "size": list(gif.size), "directions": len(preview["sequences"])})
            if preview is pack["previews"][0]:
                character = frames[0].crop((0, 0, CELL_W, 138)).resize((288, 276), Image.Resampling.NEAREST)
                tile = Image.new("RGB", (288, 328), BACKGROUND)
                tile.paste(character, (0, 0))
                ImageDraw.Draw(tile).text((144, 307), pack["id"], fill=(40, 49, 65), font=FONT, anchor="mm")
                hero_tiles.append(tile)
    credit_text = "\n".join(credits).rstrip() + "\n"
    (ASSETS / "CREDITS.txt").write_text(credit_text)
    all_files["CREDITS.txt"] = credit_text.encode()
    all_files["catalog.json"] = (ASSETS / "catalog.json").read_bytes()
    write_zip(downloads / "all-cc0-character-sprites.zip", all_files)
    cover = Image.new("RGB", (1152, 984), BACKGROUND)
    for index, tile in enumerate(hero_tiles):
        cover.paste(tile, (index % 4 * 288, index // 4 * 328))
    cover.save(ASSETS / "overview.png", optimize=True)
    (ROOT / "docs/open-character-sprites-validation.json").write_text(json.dumps({"checked_at": catalog["checked_at"], "packs": len(catalog["packs"]), "previews": report}, indent=2) + "\n")
    print(f'Built {len(catalog["packs"])} packs, {len(report)} animated previews, and 12 downloads.')


if __name__ == "__main__":
    main()
