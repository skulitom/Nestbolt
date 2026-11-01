# Data for "How many ornaments fit on a 12 × 12 inch sheet?"

Page: https://skulitom.github.io/Nestbolt/nesting-examples/nest-christmas-ornaments-on-one-sheet/

Measured on 2026-11-01 with the `nestbolt` command-line tool built from `main` at `379761a`, on a desktop PC.
Sheet 304.8 × 304.8 mm (12 × 12 in), margin 5 mm, part spacing 2 mm, edge spacing 1 mm, rotations 0/90/180/270°.
The drawing is [`../../../examples/ornaments.svg`](../../../examples/ornaments.svg); `gen.py` drew it and wrote the
request files and `grid.json`.

## Ready-to-cut sheets (SVG, millimetres)

| File | What it holds |
| --- | --- |
| `bauble-17-sheet.svg` | 17 round baubles |
| `star-23-sheet.svg` | 23 stars |
| `tree-26-sheet.svg` | 26 trees |
| `bell-22-sheet.svg` | 22 bells |
| `snowflake-18-sheet.svg` | 18 snowflakes |
| `stocking-26-sheet.svg` | 26 stockings |
| `mixed-18-sheet.svg` | 3 of each design |

Test-cut one ornament first: kerf, material thickness and hole sizes vary.

## Reproduce

```sh
nestbolt import ornaments.svg --output library.json
# most that fit: the default mode places every part
nestbolt nest --library library.json --request all-star-23-request.json --out-dir out --seconds 60 --repeatable --seed 0
# fill mode, seeds 0 to 4
nestbolt nest --library library.json --request fill-star-request.json --out-dir out-fill --seconds 30 --repeatable --seed 0
nestbolt validate --library library.json --request all-star-23-request.json --layout out/layout.json
```

- `most-that-fit.json`: every "place every part" attempt (quantity, sheets used, validity, time); the largest count
  on one sheet per design.
- `results.json`: the fill runs (seeds 0 to 4) and the two mixed sets (18 fit one sheet; 24 needed two).
- `grid.json`: each design's size and the bounding-box grid count (arithmetic, not a program's output).
- `check.json`, `check-fill-seed0.json`: our independent check of the exported sheets (`check.py`, Shapely and
  svgelements, no Nestbolt code): copy counts, shape areas, the 6 mm border and the 2 mm gaps.

The drawing, requests and sheets are MIT licensed, like Nestbolt.
