# Nestbolt

Free, open-source nesting for people who cut **fixed sheets**: laser cutters, CNC
routers, plasma, waterjet, fabric and leather. Nestbolt arranges parts so they use
the least material, with native tools, a browser app and an MCP server for AI
agents. **Work in progress: the optimiser, import/export, browser app and MCP
server work; hosting, release packages and the final acceptance gates are still
to come.**

The engine builds on [jagua-rs](https://github.com/JeroenGar/jagua-rs) and on
[sparrow](https://github.com/JeroenGar/sparrow) by Jeroen Gardeyn and collaborators
(arXiv [2509.13329](https://arxiv.org/abs/2509.13329)). Nestbolt adapts Sparrow's
overlap-minimising separator to fixed sheets.

## What works today

- **Import** SVG and DXF: lines, arcs, ellipses, Béziers, B-splines, blocks,
  transforms and units, converted to millimetres. Each closed outline is a part;
  outlines inside it are its holes. Outlines that touch themselves, such as the
  relief loops boxes.py draws at slot corners, nest with a covering outline while
  exports keep the exact curves.
- **Nest** on fixed sheets: margins, part and edge spacing, several sheets, stock
  limits, defects, rotations (free, stepped or a list such as 0/180 for fabric
  grain) and mirroring. Small parts can sit inside the holes of larger parts.
  The last sheet is compressed towards one end so the offcut stays usable.
- **Export** one SVG and one DXF per sheet from the original curves, transformed
  rather than re-polygonised (round trip within 0.01 mm).
- **Check** every result with an independent Clipper2 validator (overlap,
  spacing, containment, rotations, quantities). Invalid layouts are never returned.
- **MCP server** with `import_parts`, `nest`, `validate_layout`, `export_layout`
  and `estimate_sheets`. Its budgets are repeatable: same inputs, budget and seed,
  same layout. See [the agent interface](docs/AGENT_INTERFACE.md).
- **Browser app** (`web/`): the same engine compiled to WebAssembly in Web
  Workers, several seeds in parallel, projects saved in the browser or as a ZIP.
  Files never leave the computer. Tested in Chromium and Firefox; not hosted yet.

Fixed-sheet search lays the last sheets end to end as one walled strip and
shrinks the last sheet with a port of Sparrow's separator; parts move between
sheets and an emptied sheet disappears. In development runs at 60 seconds on
65 frozen jobs, all 195 layouts over three seeds were valid. At the per-job
median of three seeds, Nestbolt used **8.3% less material** at the median than
the best of Deepnest, SVGnest and Sparrow. It won or tied on 48 of 52 comparable
jobs; the four losses are single-sheet jobs where Sparrow leads, one of them by
more than 1%. These are development results, not the final acceptance gates
(the target is 10.8%); see [status](docs/STATUS.md).

## Quick start

Install Rust through rustup (the repository selects Rust 1.98.1) and build:

```sh
cargo build --release -p nestbolt-cli -p nestbolt-mcp
```

Import parts, nest them for 30 seconds, and get per-sheet SVG/DXF files:

```sh
target/release/nestbolt import examples/parts.svg --output library.json
target/release/nestbolt nest --library library.json --request examples/nest-request.json --out-dir run --seconds 30
```

A request names library parts with quantities and the sheets in millimetres:

```json
{
  "parts": [{"id": "parts-1", "quantity": 4}, {"id": "parts-2", "quantity": 12, "rotations": {"kind": "free"}}],
  "sheets": [{"width_mm": 600, "height_mm": 400, "margins_mm": {"left": 5, "right": 5, "bottom": 5, "top": 5}}],
  "spacing_mm": 1.0,
  "edge_spacing_mm": 1.0
}
```

`run/` then holds `layout.json`, `report.json` and `sheet-0.svg`/`sheet-0.dxf` and
so on. Existing files are never overwritten. `nestbolt export` re-exports a
layout; `nestbolt validate` checks a polygon job and layout. Add `--repeatable`
to `nestbolt sheets` for a deterministic work budget instead of wall-clock time.
File formats are described by the [JSON Schemas](schemas/README.md).

## Browser app

Build it locally (needs the `wasm32-unknown-unknown` target, `wasm-bindgen-cli`
0.2.129 and Node.js 24), then open the printed address:

```sh
cd web && npm ci && cd ..
python scripts/build_web.py
npm --prefix web run preview
```

`python scripts/build_web.py --test` also runs the Playwright tests in Chromium
and Firefox.

## Use from agents

Register the MCP server with an absolute path, for example in Claude Code:

```sh
claude mcp add --transport stdio --scope local nestbolt -- /path/to/target/release/nestbolt-mcp
```

The server reads and writes only inside its working directory (or
`NESTBOLT_WORKSPACE`). [docs/AGENT_INTERFACE.md](docs/AGENT_INTERFACE.md) covers
Claude Code, Codex and Claude Desktop, the request format and the rules.

## Development

```sh
python scripts/check.py
python scripts/sheets_batch.py --cpu 0 --cpu 2 --seconds 60
```

The first runs format, lint, all Rust and Python tests, WebAssembly builds,
notice and dataset checks; add `--web` for the browser build and tests. The second runs the development benchmark (held-out
jobs excluded) and writes an audited report under `benchmarks/results/`.

| Path | Purpose |
| --- | --- |
| `crates/core` | Geometry import/export, sheet search, separator, part-in-part |
| `crates/cli` | Command-line interface |
| `crates/mcp` | Native stdio MCP server |
| `crates/validator` | Independent Clipper2 checker and material scoring |
| `crates/wasm` | WebAssembly boundary for the browser app |
| `web` | Browser app (Preact, Vite) and its Playwright tests |
| `benchmarks` | Frozen datasets, competitor runners and all results |
| `docs/PLAN.md` | The full plan and its acceptance gates |
| `docs/STATUS.md` | Milestone evidence and next steps |

Every benchmark run, including failures, is logged in [BENCHMARKS.md](BENCHMARKS.md).

## Progress and licence

Progress counts finished milestones only; see [docs/STATUS.md](docs/STATUS.md).
Nestbolt is [MIT](LICENSE). jagua-rs is an unmodified MPL-2.0 dependency; the
separator in `crates/core/src/separate.rs` is adapted from Sparrow (MIT).
[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) records every dependency and licence.
