# Open character sprites collection

- Post: `/posts/open-character-sprites/`
- Research date: 2026-10-27 (Asia/Seoul)
- Scope: 11 CC0 packs, 20 character previews; five 4-direction packs and six 8-direction packs.
- Sources, creators, licenses, original URLs, SHA-256 hashes, crop rectangles, and reflections: `public/posts/open-character-sprites/catalog.json`.
- Download credits: `public/posts/open-character-sprites/CREDITS.txt`.

All ten OpenGameArt item pages were opened and their actual `License(s): CC0` fields checked. Ninja Adventure's creator itch.io page declares CC0, permits commercial use, and links the creator's Godot repository. Its two collected sheets are pinned to repository commit `6ac78232d5aedcc85ce5f27d060ea92366f7c24a`; this is a small sample, not the full itch.io asset pack. Tiny RPG's CC0 claim applies to its free demo archive, not the linked paid workshops. Source pages are linked beside each pack in the post.

## Rebuild

Requires Python 3 and Pillow 11.3 or newer:

```sh
python3 scripts/build-open-character-sprites.py
npm run build
```

The builder works offline from collected originals, verifies their hashes, generates GIFs plus still PNGs, creates 11 per-pack ZIPs and one complete ZIP, and writes `docs/open-character-sprites-validation.json`. Original downloaded files remain byte-for-byte unchanged. Bundle ZIPs add a credits file; ZIP downloads originally published by creators are nested unchanged.

GIF directions use S/E/N/W for four views and S/SE/E/NE/N/NW/W/SW for eight views. Human Male and Square Characters have five drawn views and three reflected views. 8-Bit Character has three drawn views and one reflected view. Only the Skeleton preview removes its two opaque cell background colors. Square uses the four `idle` frames, not an invented walking animation. GIF timing is a custom 140 ms per frame.

## Verification completed

- Production build passed. The existing large Phaser chunk warning remains unrelated to this post.
- Every direction of all 20 previews contains changing source pixels; all GIFs contain multiple frames, positive durations, and infinite loops.
- All original SHA-256 hashes match the collected files. All 12 ZIPs pass CRC validation and are served byte-for-byte correctly over the local preview server.
- All post IDs are unique, local anchors resolve, and local linked resources return HTTP 200 from the production preview server.
- Browser UI on the built page: four-direction filter shows five packs; eight-direction filter shows six; the table of contents reveals a filtered-out target and restores all 11 packs.
- All 14 selectable character options update both the displayed GIF and its download URL. Six other packs have one fixed preview each.
- Global pause switches all 11 displayed previews to still PNGs; resume restores GIFs. Desktop screenshot inspected; no horizontal page overflow.

## Limits

These are source-sheet and browser-preview checks. Game-engine imports, combat transitions, equipment overlays, physical mobile-device behavior, and the OS reduced-motion preference path have not been exercised. Preview speed is not an assertion about the creator's intended game animation speed. Not every extra image included in a pack is a multidirectional character (notably Skeleton's extra bosses/effects).

Pure top-down single-view assets intended for rotation were excluded: Top Down Astronaut and Top Down Male Character Sheet. This post makes no claim that a single rotatable view is a four- or eight-view sprite set.
