# Nestbolt: build plan for an agent

*Written 2026-10-11 by compass-advisor for Artem. Hand this whole file to the agent that builds the project. Name
**Nestbolt** and licence **MIT**, both decided by Artem on 2026-10-11 (the MIT choice is to build reputation and trust
first).*

## 1. Goal

A free, open-source 2D nesting tool for people who cut **fixed sheets**: laser cutters, CNC routers, plasma and
waterjet, plus fabric and leather. It arranges parts so that they use the least material. The core is the 2025 state of
the art in nesting. It runs entirely in the browser: no server, no account, and files never leave the user's device.
It is hosted on GitHub Pages.

**The gap it fills:**
- **The research is ahead of the tools.** [sparrow](https://github.com/JeroenGar/sparrow) (MIT; paper
  [arXiv 2509.13329](https://arxiv.org/abs/2509.13329)) leads published results by a wide margin, but only for
  **strip packing**: one strip of fixed width, minimising its length.
- **Its browser app is strip-only.** [sparrow/studio](https://github.com/JeroenGar/sparrow-studio) (MIT, launched
  2026-09) brings sparrow to the browser, but its README says it has no fixed sheets, no multi-sheet allocation and
  no parts inside holes.
- **The engine is ready, the optimiser isn't.** The collision engine underneath,
  [jagua-rs](https://github.com/JeroenGar/jagua-rs) (MPL-2.0), supports bin packing (feature `bpp`) and holes and
  defect zones in containers. Its only bin-packing optimiser is a one-pass constructive demo (`lbf`) whose quality the
  README calls "chaotic".
- **The sheet tools makers use are older or limited:**
  - [deepnest-next](https://github.com/deepnest-next/deepnest): Electron, the community fork of Deepnest.
  - [SVGnest](https://github.com/Jack000/SVGnest): JavaScript, last pushed 2024-02.
  - LightBurn: Quick Nest is bounding boxes only; True Nest is in 2.2 early access and Pro-only.

**The product:** sparrow-grade optimisation for fixed sheets, with the production features sheet users need. It also
has an **MCP server**, so AI agents can call Nestbolt as a tool ("lay out these parts on 600×400 sheets"), like
Artem's Cutbolt, Inkbolt and PixelForge.

## 2. Definition of done (100%)

The project is complete when every gate in section 6 passes in one frozen, reproducible benchmark run. The headline gate
is G2: on fixed-sheet jobs, the tool uses **substantially less material than the best tool available**, at the same
time budget on the same machine.

"Best tool available" means the best result for each job among the tools we can run without paying:
- deepnest-next;
- SVGnest;
- sparrow/studio and the sparrow CLI, wherever a strip result can be read as a single sheet;
- LightBurn True Nest is **not available now** (Artem, 2026-10-11: no budget for it). Revisit only if Nestbolt gets
  real traction.

Commercial industrial nesters (SigmaNEST, ProNest, Lantek, TruNest and similar) are out of scope: we can't test them,
so we never claim to beat them.

## 3. Architecture (decided)

- **Engine:** Rust, as one Cargo workspace.
  - `core`: the problem model, the optimiser and the import/export geometry. It builds on jagua-rs as an unmodified
    dependency (upstream any fixes) with features `bpp` and `spp`.
  - `cli`: the native solver, used for benchmarks and batch jobs, with JSON in and JSON/SVG/DXF out.
  - `wasm`: `wasm-bindgen` bindings for the browser.
  - `mcp`: a stdio MCP server binary on the same core, using `rmcp`, the official Rust MCP SDK. It is native only,
    because a web page can't be an MCP server.
- **Agent distribution:**
  - Prepare, don't publish: a tag-triggered release workflow (Windows, Linux and macOS binaries with SHA-256 sums), an
    MCPB bundle, `server.json` for the official MCP Registry, and a dispatch-only OIDC registry-publish workflow.
  - Model all four on Artem's [Cutbolt #2](https://github.com/skulitom/Cutbolt/pull/2) and
    [Inkbolt #1](https://github.com/skulitom/Inkbolt/pull/1).
  - Link the Windows build's C runtime statically.
  - The first release and registry publish happen when Artem says so.
- **Browser:** WebAssembly in Web Workers. Use **portfolio parallelism**: each worker runs an independent search (its
  own seed and settings), and the UI keeps the best.
  - Workers need no SharedArrayBuffer, so the site needs no COOP/COEP headers, which GitHub Pages can't set.
  - A threaded build behind `coi-serviceworker` is optional, and only if it measurably wins. sparrow/studio already
    ships SIMD and threaded builds with fallbacks; read how it does it (MIT, keep notices if you copy code).
- **UI:** TypeScript with a light framework, and canvas or SVG rendering.
  - Import SVG and DXF: units, layers, arcs, Béziers and splines.
  - Edit quantities, rotations and sheets.
  - Show live progress.
  - Export one SVG and one DXF per sheet, with the original curves transformed (not re-polygonised).
  - Save projects in IndexedDB and as a project ZIP.
- **Why not pure JavaScript:** collision detection and the optimiser are compute-bound. SVGnest and Deepnest are
  JavaScript-era designs, Rust→WebAssembly runs close to native, and both sparrow and jagua-rs are already Rust.
- **Hosting:** GitHub Pages only, deployed by a GitHub Actions workflow that builds and tests first. No server and no
  uploads. Analytics: none, or privacy-friendly page counts only; never geometry or file names.
- **Licences:**
  - Ours: MIT (decided by Artem).
  - jagua-rs is MPL-2.0: file-level copyleft, so changes to its files stay open, and upstream them.
  - sparrow and sparrow/studio are MIT: keep their notices for anything reused. sparrow's README invites forks that
    "expand the functionality".
  - Credit sparrow and jagua-rs prominently.
  - Check and record every other dependency's licence in `THIRD_PARTY_NOTICES`.

## 4. Scope

**v1 features (all required for 100%):**
1. **Sheets:** fixed sizes, margins, several stock sizes in one job, and an unlimited or capped count of each.
2. **Multi-sheet allocation:** every part placed on the fewest sheets, with the last sheet's waste pushed to one end, so
   the offcut is reusable.
3. **Part-in-part:** small parts placed inside the holes of larger parts. jagua-rs 1.0 rejects items with holes, so
   model it in our layer: hole interiors become extra containers, or contribute through a two-level search.
4. **Sheet defects and remnants:** keep-out zones, through jagua-rs container holes or quality zones.
5. **Spacing:** minimum clearance between parts (kerf plus margin) and to the sheet edge.
6. **Rotation:** free, stepped (for example 90°) or a fixed list (for example 0/180 for fabric grain), per part.
   Mirroring is allowed per part or denied.
7. **Quantities:** from 1 to thousands, and jobs of up to 2,000 parts.
8. **Fill mode:** when not everything fits on the sheets allowed, maximise the placed area or a priority score.
9. **Import and export:** SVG and DXF in, as above.
10. **The native CLI:** the same features as the browser.
11. **The MCP server:** a few clear tools that are easy for an agent to use.
    - `import_parts`: SVG/DXF in; parts with areas, bounding boxes and import warnings out.
    - `nest`: parts, quantities, sheets, spacing, rotations, `time_budget_s` (capped at 300) and `seed` in; per-sheet
      placements, the material and utilisation metrics, the validator's report and the export file paths out. It
      sends progress notifications while it runs.
    - `validate_layout`: checks any layout against the sheets and constraints.
    - `export_layout`: SVG/DXF per sheet.
    - `estimate_sheets`: a fast lower bound on sheets, for planning and quotes.

    Rules for the tools:
    - Heavy geometry goes to files, never inline, and each tool reply stays under about 50 KB.
    - The same seed and budget give the same result.
    - Errors say what to fix.
12. **Agent-readable docs:** an `llms.txt`, a JSON Schema for jobs and results, and a README section on using it from
    Claude Code, Codex and Claude Desktop.

**Later (not part of 100%):** common-line cutting, lead-ins, LightBurn `.lbrn2` import and export, and a PWA for
offline install.

## 5. Benchmarks and comparison method

### 5.1 Datasets (frozen, checksummed, each item's licence recorded)

- **S, standard strip instances:** the ESICUP set that sparrow uses (in sparrow's `data/input` and Oscar Oliveira's
  [OR-Datasets](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D-Irregular)).
- **B, standard sheet instances:**
  - Find, cite and convert published 2D irregular bin-packing instances. Start with jagua-rs's bundled
    bin-packing examples, López-Camacho et al. (2013), and Martínez-Sykora et al. (2017, free rotation). Record any
    best-known published results.
  - Also derive fixed-sheet variants of set S, with each sheet the strip's width times a stated length.
- **M, maker jobs:** at least 40 realistic jobs built only from permissively licensed or generated sources:
  - flat-pack boxes from boxes.py output;
  - garment patterns from FreeSewing (MIT; grain 0/180);
  - lettering and signs from OFL fonts;
  - gears and brackets from procedural generators;
  - public CC0 or CC-BY DXF/SVG parts.

  Cover:
  - **sheet sizes:** 300×200 (diode laser), 600×400 (CO2 bed), 1220×2440 (plywood), 1250×2500 and 1500×3000 (sheet
    metal), and a 1500-wide fabric roll;
  - **part mixes:** parts with holes (for part-in-part), mixed quantities, and large jobs of 500 to 2,000 parts.

  Keep 10 of the 40 as a held-out set, never used for tuning.

### 5.2 Tools compared (versions pinned in the results)

| Tool | How it's run | Comparisons |
|---|---|---|
| deepnest-next | automated: its JSON/CSV project loading if released, otherwise Playwright's Electron support, otherwise its GUI driven in an Anode seat (Artem's Anode) | sheet jobs |
| SVGnest | a local copy driven by Playwright | sheet jobs |
| sparrow CLI | native | strip parity (G3); single-sheet jobs where the strip fits the sheet |
| sparrow/studio | the CLI result serves as its result (the same solver) | single-sheet only |
| LightBurn True Nest | not run for now: Artem has no licence (2026-10-11); a manual 10-job check later, only with traction | not gated |
| ours | native CLI, plus the WebAssembly build in headless Chrome | everything |

- **"Deepnest" means deepnest-next.** The original Deepnest (Jack000, unmaintained since 2020) is its predecessor and is
  not run.
- **Both deepnest-next and SVGnest are targets.** The G2 gate compares Nestbolt with **whichever of them (or sparrow,
  where it applies) did best on each job**, so beating only the weaker one never counts.
- **Report each tool separately too.** The results page shows Nestbolt against each tool, so a claim like "vs SVGnest"
  is backed by its own numbers.

### 5.3 Rules for a fair comparison

- **Identical inputs:** the same part polygons after one shared, conservative curve tolerance, plus the same spacing,
  rotation sets, sheets and quantities.
- **Two settings per tool:** each run twice, once with identical constraints (for example 4 rotations for everyone) and
  once with each tool's best settings. Report both; the gate uses the better competitor result.
- **Same hardware:** Artem's PC, a Ryzen 9 7950X3D. Each run is single-threaded, with at most 8 runs at once. Also
  report an all-core run for ours.
- **Time budgets:** 60 s on everything, and 300 s on a fixed 12-job subset. Use 3 seeds while developing and 5 for
  the final gate. Report the median and interquartile range.
- **Independent validation:** one validator scores every tool's output, never the tool's own report. It is a separate
  code path from jagua-rs (for example Clipper2 or the `geo` crate). It checks:
  - overlap area at most 1e-6 of part area;
  - clearance, by polygon offset;
  - containment in the sheet minus margins and defects;
  - rigid transforms only, with allowed rotations and mirroring;
  - exact quantities, and units.

  An invalid layout counts as a failure for that tool.
- **Metric for sheet jobs:** material used = (sheets used − 1) + (used length of the last sheet ÷ its length). Lower is
  better. Also report utilisation = part area ÷ (full sheets plus the used part of the last sheet). Fill mode is scored
  by placed area.
- **Metric for strip jobs:** strip length (sparrow's own metric).

### 5.4 Heat and runtime

This PC has overheated under long loads. Cap concurrency at 8 runs, keep each benchmark session under about 4 hours,
and check temperatures between sessions.

## 6. Acceptance gates (all must pass: 100%)

- **G1, validity:** 100% of our outputs pass the validator on every dataset and seed. Geometry has property tests and
  fuzzing, covering collinear and duplicate points, slivers, near-touching parts, arcs and very small features. There
  are no crashes across the full matrix.
- **G2, quality on sheet jobs, the headline gate:**
  - **Datasets:** sets B and M, including the held-out 10.
  - **Comparison:** at equal 60 s and 300 s budgets, against the best available tool on each job.
  - **Pass:** all three of these must hold.
    1. Median material reduction is **at least 5%**.
    2. We win or tie on **at least 90%** of jobs.
    3. We are never more than **1% worse** on any job.
  - **If the baseline gap is far larger** (M1 shows it), raise the 5% target to half the measured gap, so "substantial"
    stays honest.
- **G3, strip parity:** on set S, the median is within 1% of the sparrow CLI's length at the same budget, and never more
  than 2% worse. The point is to show we didn't break what we build on.
- **G4, speed:** on at least 80% of sheet jobs, we reach the best competitor's 300 s result within 30 s.
- **G5, browser:**
  - **Quality:** in current Chrome and Firefox on Windows, the WebAssembly build at 60 s comes within 2% material of the
    native build at 60 s.
  - **Responsiveness:** no main-thread task over 200 ms while solving.
  - **Scale:** a 2,000-part job imports, solves and exports with memory under 1.5 GB.
  - **Hosting:** it works from GitHub Pages with no special headers.
- **G6, fidelity:**
  - Exported parts match the imported ones within 0.01 mm (Hausdorff distance, after the inverse transform).
  - Arcs and curves are preserved, and mm and inch units are correct.
  - Exports open in Inkscape and LibreCAD.
  - Artem checks LightBurn by hand on 5 exports.
- **G7, features:** every v1 item in section 4 works through both the UI and the CLI, each with an end-to-end test
  (Playwright for the UI).
  - **MCP:** a real client passes. Claude Code, run with `claude -p --mcp-config <file> --strict-mcp-config`, lists
    the tools, imports a sample SVG, runs `nest` with a 10 s budget and exports, and the result passes the independent
    validator.
  - **Packaging:** the MCPB bundle builds and validates, and `server.json` passes `mcp-publisher validate`.
- **G8, reproducibility:**
  - One command rebuilds the datasets, runs the matrix and writes the results table and charts.
  - A results page on GitHub Pages shows every number, tool version, seed and the hardware.
  - The README claims nothing beyond that page.

## 7. Milestones (with progress weights)

| # | Milestone | Weight | Done when |
|---|---|---|---|
| M0 | Groundwork | 5% | workspace, CI, licence notices; sparrow's published strip results reproduced natively within 1% |
| M1 | Baseline | 15% | validator, datasets S/B/M, the harness, and the deepnest-next and SVGnest runners automated; a baseline table of every competitor against jagua-rs's `lbf`, which measures the gap |
| M2 | Sheet optimiser | 25% | multi-sheet search (for example sparrow-style feasibility repair while sheets are removed and the last sheet is compressed), fill mode, defects, rotation and mirror rules; G1, G3 and G4 green |
| M3 | Part-in-part and import/export | 15% | holes as nested containers; SVG and DXF import and export with curve fidelity; G6 green |
| M4 | Browser app and MCP server | 20% | WebAssembly in Workers, UI, IndexedDB and ZIP, deployed to Pages; the MCP server, bundle and release workflows ready; G5 and G7 green |
| M5 | Final gate | 20% | the tuning loop reaches G2 on the frozen datasets, the held-out set included; the results page and README are out; G8 green |

Report progress as the sum of finished milestone weights. A milestone only counts once its gates are green.

## 8. Ground rules for the agent

- Re-read the competitors at the start of each milestone: sparrow, sparrow/studio, deepnest-next and LightBurn
  release notes. **If sparrow/studio ships fixed sheets or part-in-part, stop and tell Artem before continuing.** The
  target moves to beating that, or we contribute upstream instead.
- **No tuning on the held-out jobs.** Tune on set B and the 30 non-held-out maker jobs only.
- Never copy code from closed tools, and don't decompile anything. Use papers, MIT/MPL code with notices kept, and our
  own work.
- Tests: unit and property tests in Rust, Playwright end-to-end tests for the UI, and the benchmark smoke subset in CI
  (a few jobs at a 5 s budget). Full benchmark runs stay local.
- If the repo gets a file-type guard like Cutbolt's and Inkbolt's `tools/check_repo.py`, allow `.yml` in
  `.github/workflows/` and the bundle's script type in `mcpb/` from the start. Leaving them out blocked both repos'
  distribution PRs on 2026-10-11.
- Keep a `BENCHMARKS.md` log: each run's date, commit, tool versions and summary. Never overwrite earlier results.
- Ask Artem only about anything that needs an account or costs money. The name, the licence and LightBurn are settled
  (section 9).

## 9. Decisions (Artem, 2026-10-11 and later)

1. **Name:** Nestbolt, next to Cutbolt and Inkbolt.
2. **Licence:** MIT. Reputation and trust come before sales, and an open tool is its own marketing.
3. **LightBurn:** not provided now. Its True Nest comparison waits until Nestbolt has traction. Until then, claims
   name only the tools actually measured.
4. **G2 median target (2026-10-12):** the raise to half the measured gap (10.77%, frozen in M1) is waived after a
   feasibility analysis showed that about ten of the 52 development jobs cannot reach it by any tool (packing densities
   at or above 95-100%, near-optimal rectangle stacking, or a sheet fewer than the published bin counts). G2's median
   condition is the base **at least 5%**; the development median is 8.77%. The 90% wins/ties and never-more-than-1%-worse
   conditions are unchanged, at both budgets, on the final run with the held-out jobs.
5. **Final results accepted (2026-10-13):** Artem accepts the final acceptance run as published (build `75cbb32`,
   seeds 1000-1004, held-out jobs included). G1, G3, G4 and G2 at 300 s are met; G2 at 60 s is not met as written
   (median 8.52%, 48 of 56 jobs won or tied, two jobs more than 1% worse, every loss against Sparrow). M5 closes on
   this acceptance. The results page and README state the shortfall, and nothing is tuned against the final records.
