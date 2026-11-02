# Data for "LightBurn nesting without Pro, including onto offcuts"

Page: https://skulitom.github.io/Nestbolt/compare/lightburn-nesting-without-pro/

Measured on 2026-11-02 with the Nestbolt **v0.2.0-alpha.1** Windows x64 release (a preview; zip SHA-256
`06852c2d3bdf600a60c4cfc403f1a2a28b5028ec55d3a55eca7d04883b2f8b50`, checked against `SHA256SUMS` and its build
attestation), on a Windows desktop PC: `--seconds 30 --repeatable`, seed 0, part spacing 2 mm, rotations
0/90/180/270°. LightBurn was not run. Every number on the page is in `results.json`.

| File | What it is |
| --- | --- |
| `engraved-ornaments.lbrn2` | The input project: six groups, layers CUT (Line), ENGRAVE (Fill), SCORE (Line); settings are placeholders |
| `full-sheet-request.json` | 3 of each design on a 12 × 12 in sheet, margins 5 mm, edge spacing 1 mm |
| `traced-offcut-request.json` | Up to 4 of each on the traced offcut (`outline_mm`), edge spacing 5 mm, `fill_area` |
| `partly-used-request.json` | Up to 3 of each on the partly used sheet (`outline_mm` with two holes), edge spacing 2 mm, `fill_area` |
| `all-traced-offcut-13-request.json`, `all-partly-used-11-request.json`, `all-partly-used-12-request.json` | The "most found" requests (default mode; the 12 was found with `--seconds 120`) |
| `full-sheet-18-sheet.lbrn2`, `traced-offcut-13-sheet.lbrn2`, `partly-used-11-sheet.lbrn2` | The nested sheets drawn on the page, as Nestbolt wrote them |
| `browser-traced-offcut-12-sheet.lbrn2`, `browser-equivalent-request.json` | The sheet the live browser app downloaded (2 of each, 2 mm part and edge spacing), and a request with the same settings for `check.py` |
| `partly-used-sheet.svg` | The partly used sheet as a SHEET drawing, for the browser app's Remnant outline picker |
| `results.json` | Times, counts, areas, both checks, and the counts that were not found |
| `searches-2026-11-02.txt` | The five searches and what ranked |

The traced offcut is [`../../../examples/traced-offcut.svg`](../../../examples/traced-offcut.svg), from the
[scrap example](../../../nesting-examples/nest-parts-onto-scrap-offcut/).

## Scripts

- `kit.py` writes the project and the three requests. It reads the library that the release writes from the ornament
  drawing: `nestbolt import ../../../examples/ornaments.svg --output ornament-library.json`, then
  `python kit.py ornament-library.json traced-offcut.svg <out-dir>` (needs Shapely).
- `check.py` is the independent check: `python check.py engraved-ornaments.lbrn2 <request.json> <sheet.lbrn2>`.
  It uses no Nestbolt code.
- `maxfit.py` raises the ornament count in default mode until a nest fails; set `NB` to your `nestbolt` path.
- `render.py` draws the page's figures from the `.lbrn2` files; `browser_flow.mjs` drove the live app with Playwright.

Open each sheet in LightBurn and check it before you cut. Test-cut one part first.
