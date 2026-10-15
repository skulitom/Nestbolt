# Nestbolt v1.1: real shop files — plan for an agent

*Written 2026-10-13 for Artem, after v1 closed on his acceptance (PLAN.md decision 5). Hand this whole file to the
agent that does the work.*

*Read first:*
- [PLAN.md](PLAN.md): the v1 plan and its ground rules;
- [STATUS.md](STATUS.md);
- [BENCHMARKS.md](../BENCHMARKS.md);
- [V1_1_RESEARCH.md](V1_1_RESEARCH.md): every data source, licence, format detail and practice this plan relies on.

*Nothing here needs files or answers from Artem. Data comes from public, permissively licensed sources or is made by the
agent. Every design choice is decided below (section 3). Artem is asked only about releases, and if a stop rule in
section 8 fires.*

## 1. Goal

v1 nests well on clean benchmark files. v1.1 makes Nestbolt work on the files people actually bring from the shop:
- messy DXF and SVG files from Fusion 360, Illustrator, Inkscape, FreeCAD, KiCad, SolidWorks and LightBurn;
- LightBurn projects, nested and written back with their layers and cut settings intact.

It also adds common-line cutting and lead-in allowances, and closes the browser's measured gap on curve-heavy parts.

| # | Workstream | Why |
|---|---|---|
| N0 | Messy-file corpus | Most real failures happen at import; v1's fidelity corpus is clean generated files. Every later workstream is tested on it. |
| N1 | Import robustness | Gaps, exploded and duplicate segments, layers and colours, units, blocks, text and dimensions. |
| N2 | LightBurn `.lbrn2` round-trip | LightBurn is the main maker laser tool. Its nesting is weak: Quick Nest packs bounding boxes, True Nest is 2.2 early access and Pro-only, and Nest Selected round-trips through SVGnest.com. The one open nester for its projects (laser-layout, no licence) loses every layer on export. |
| N3 | Curve-heavy parts in the browser | Measured gap: the browser is 16.9-29.8% worse than native on the four development gear jobs at 60 s (G5 report). |
| N4 | Common-line cutting | Parity with deepnest-next, done the industrial way: kerf-spaced parts with one shared, compensated cut line. |
| N5 | Lead-in allowances | Every major cutting tool draws its own leads. The nester's job is to reserve room for them and choose where each contour starts. |

## 2. Ground rules

Everything in PLAN.md section 8 applies, plus the following.

- **Licences:**
  - Data that may be committed: CC0, CC-BY, CC-BY-SA, MIT, BSD, Apache-2.0, Unlicense, CERN-OHL-P, public domain.
    Record the source URL, the licence and where it is stated for every file.
  - GPL, LGPL and MPL data (V1_1_RESEARCH.md section 1.4) may be used only for local testing and is never committed.
  - NC, ND and unlicensed files are excluded.
  - Keep MIT/MPL notices for reused code, and credit sparrow and jagua-rs.
- **Code reuse:**
  - Never decompile or disassemble LightBurn or any closed program. Never open `Dcs102/lightburn`.
  - Never copy code from GPL projects (boxes.py, deepnest-next's `main/deepnest.js`) or from unlicensed ones
    (laser-layout). Describe their behaviour only.
  - MIT readers such as lbrn2-to-svg may be used as independent test oracles, run from their published packages.
- **No accounts or uploads:**
  - Never sign up or log in anywhere. Onshape and Fusion 360 therefore cannot be used. Fusion-written files come from
    public repositories (V1_1_RESEARCH.md section 1.2).
  - Never upload geometry. deepnest-next's DXF export sends the SVG to `converter.deepnest.app`, so use its SVG export
    only.
- **LightBurn:**
  - LightBurn Core 2.1.01 is installed as a 30-day trial (installed 2026-10-12 for G6, ending about 2026-11-11). With
    Artem's approval, given by handing over this plan, the agent drives it in the hidden Anode desktop as it did for G6.
  - Never reinstall it or reset the trial. Never buy anything.
  - Do every LightBurn-dependent step first (section 6).
- **Benchmark discipline:**
  - BENCHMARKS.md is append-only.
  - Runs go on CCD0, one per physical core, at most 8 at once; builds use `output/ccd1.py`.
  - Never edit `crates/` or the batch scripts while a benchmark runs: the harness hashes its sources and refuses to
    record.
  - Python edits always pass `encoding='utf-8'` and a line-feed `newline`.
- **Held-out jobs:** never tune on the ten v1 held-out maker jobs (`held_out_ids` in `benchmarks/datasets/makers.json`).
  Every development subset in this plan excludes them.
- **Claims:**
  - The published v1 results (build `75cbb32`) stand unchanged. Workstreams N3-N5 change the solver; report their
    effect on development jobs only.
  - The README claims nothing beyond the results page. No new quality claim without a new final run, which needs a fresh
    held-out set and fresh seeds, and only Artem starts one.
- **Releases:** the first release and registry publication happen only on Artem's explicit instruction.
- **Surfaces:** every feature works through the UI, the CLI and the MCP tools, each with an end-to-end test (v1's G7
  rule).
- **Progress** is reported only as completed milestone weights (section 7).

## 3. Decisions made in this plan

| Topic | Decision | Basis |
|---|---|---|
| Gap healing | Keep 0.005 mm as the silent join tolerance. "Close gaps up to X mm" (default off, maximum 1 mm) closes larger gaps and reports each one with its location and size. | Fusion files show gaps in Deepnest; LightBurn's Auto-Join uses 0.05 mm (research 1.5). |
| Duplicates | Remove exact duplicate and zero-length segments, and merge overlapping collinear segments before chaining. Always report the count. | Exploded and doubled lines in Fusion, LightBurn and Illustrator files. |
| Layers and colours | Report every layer and colour with entity counts. Cut selection: the user's choice; otherwise layers named like `cut`/`outline`/`profile`; otherwise all closed contours. TEXT, MTEXT, DIMENSION, HATCH, LEADER, SOLID and bend/extent layers are ignored, with a warning. | LightBurn maps by colour and ignores layer names; Fusion flat patterns put bend lines on their own layers. |
| Units | Use `$INSUNITS` when present. When it is missing and the drawing's largest dimension is under 60 units, warn that it may be in inches and offer inches; never rescale silently. cm (`$INSUNITS=5`) is supported. | MeArm v1 is in cm; LightBurn exports carry no units. |
| Export colours | DXF layers get colours matching LightBurn's default palette: CUT colour 00, COMMON 01, LEADIN 02, SHEET the T1 tool colour. Verify the palette RGB/ACI values locally before shipping. SVG strokes use the same RGB. | LightBurn assigns layers by colour. |
| LightBurn units of nesting | (1) Each top-level Group is one rigid unit. Reject a Group mixing output-enabled artwork with Tool/output-off shapes, with instructions to ungroup in LightBurn and group movable artwork separately (reviewed decision 6). (2) Each other top-level closed shape on a Cut or Scan+Cut layer is a unit, together with the other top-level shapes (Scan, Image, Text) whose bounds lie wholly inside its outline. (3) Each remaining top-level shape is its own unit: closed paths by outline, everything else by bounding rectangle. (4) Shapes on Tool layers or on layers with output off stay where they are, in every output file. | boxes.py writes one group per part; engraving normally sits inside the part it marks. |
| LightBurn output | One file per sheet, `<name>-sheet-<k>.lbrn2`, holding that sheet's units with updated XForms. Everything else is preserved: all CutSettings, UIPrefs, Notes, VariableText, Thumbnail and unknown elements and attributes. Optionally a sheet-outline Rect on tool layer T1 (on by default; adds a T1 CutSetting if missing). | A laser runs one sheet at a time; lossless preservation is the reason to round-trip at all. |
| Shared geometry | When a sheet file omits the shape that defines a `VertID`/`PrimID` (or a Bitmap's `Data` by `SourceHash`), move the defining lists to the first kept shape with that id. Change nothing else. | Sharing rule, research 2.1. |
| Transform update | new XForm = placement transform ∘ old XForm, on each top-level member of a unit; children are untouched. The sheet's lower-left corner is the workspace origin. `MirrorX`/`MirrorY` handling is set from local samples (N2 step 1). | Research 2.1 (XForm order; mirror mapping unresolved). |
| `.lbrn` (legacy) | Import supported; output is written as `.lbrn2`. Only `.lbrn2` is gated. | `.lbrn` is only for very old versions (research 2.1). |
| Kerf from LightBurn | Read each layer's `kerf` and show it. Never change spacing automatically. | Users set kerf per layer for different jobs. |
| Common-line model | Parts sit exactly one kerf apart; one centreline toolpath (outlines offset by kerf/2) per shared straight segment goes on a COMMON layer; the closed true-size outlines stay on CUT. Defaults: off; kerf from the user (required, at least 0.05 mm); collinearity tolerance 0.01 mm; minimum shared length 10 mm; straight segments only; sheet edges and part-in-hole off. The search bonus is an option, off by default, normalised as a fraction of total cut length. | Industrial practice (ProNest, Primecut, FastNEST). Deepnest's zero-gap merge loses half a kerf per edge (research 3.1-3.2). |
| Lead-in scope | Reserve a footprint per contour and choose its start point; export the leads on a LEADIN layer for review only. No G-code, cut order or pierce sequencing. Defaults: off; line; 3 mm; 45° outside, 90° inside holes; arc length = requested length and sweep = absolute lead angle (radius = length / sweep in radians, matching LightBurn; zero-angle limit is a straight lead); shorten to fit down to 0.5 mm, then flag; pierce disc 2 × kerf; no lead-out or overcut. Placement: outer contours at the most convex corner, otherwise the middle of the longest edge; holes on the longest edge, otherwise the centre; never on a shared common-line segment. | LightBurn, SheetCam, Fusion and CypCut draw their own leads. Corner placement follows Primecut and OMAX; values from Thunder Laser and Hypertherm (research 3.3). |

## 4. Workstreams

### 4.1 N0: the messy-file corpus

**Contents:**
- **Real files:** at least 60 from at least 8 of the sources in V1_1_RESEARCH.md section 1.2, including at least 25
  Fusion-written files, identified by the section 1.1 fingerprint. Prefer whole part sets (a case, a plate, a robot's
  panels) over single drawings.
- **LightBurn-written files, made locally in Anode.** No openly licensed ones exist.
  1. Take 15 openly licensed designs from the real set.
  2. Import each into LightBurn and save it as `.lbrn2`, after setting up layers (cut, score, engrave), a text, a group,
     a bitmap, lead-ins and a start point on some, a kerf on one layer, and copies of one part (shared geometry).
  3. Export each as DXF and as SVG with LightBurn's default export settings, plus 5 more DXFs with "Convert arcs to
     lines" on.

  That gives 15 `.lbrn2` + 35 DXF/SVG. Each file keeps the source design's licence, with LightBurn 2.1.01 recorded as
  the writer.
- **Public LightBurn projects:** at least 40 `.lbrn2`/`.lbrn` files from section 2.3. Skip the lbrnts assets.
- **Robustness set:** at least 150 files from the test suites in section 1.3 (ezdxf, GDAL, ACadSharp, dxf-parser,
  CadQuery). These carry no part labels; the expectation is "imports or fails clearly".
- **Generated set:** a deterministic, seeded `scripts/shop_habits.py` applies each habit from section 1.5 to 10 clean
  base drawings (v1 fixtures and maker parts), at least 100 files. The habits:
  - exploded and shuffled segments;
  - gaps and overlaps of 0.001-0.5 mm;
  - duplicates and zero-length segments;
  - Fusion-style SPLINEs and extrusion (0,0,−1) on arcs;
  - LWPOLYLINE bulges and widths;
  - nested and mirrored blocks;
  - geometry wrapped in one block with an INSERT;
  - a missing HEADER and missing `$INSUNITS` with inch geometry; cm units;
  - TEXT, DIMENSION, HATCH and construction lines on other layers;
  - colour-per-operation layers;
  - a complete existing nest with its sheet outline.

**Labels:**
- Every file in the real, LightBurn and generated sets gets a JSON label: cut parts, holes per part, which layers or
  colours are cut, outer bounding sizes, and expected warnings.
- Real files are labelled by the agent from a rendering made with ezdxf's drawing add-on (MIT) or Inkscape, together
  with a reading of the file. Each label records how it was derived.
- Generated labels come from the generator.

**Freeze:**
- Under `benchmarks/datasets/shop/`, with a manifest (source, licence, licence location, writer and its evidence,
  sha256) and per-file attribution in a `LICENSES.md`.
- Before any import work, hold out 20% of the real and LightBurn-written files, stratified by writer. They are never
  used for tuning.

**Gate H1:** all of these:
- the counts above are met;
- every committed file has a recorded permissive licence;
- every labelled file has its label;
- the manifest is frozen with checksums;
- the held-out split is recorded in BENCHMARKS.md before any N1 change.

### 4.2 N1: import robustness

Build the section 3 import decisions:
- gap healing, de-duplication, layer and colour selection, units;
- ignoring non-geometry entities;
- blocks with extrusion −1 mirroring;
- pre-arranged nests: their sheet outline can be used as the sheet (v1 remnant outlines);
- open-contour reports: location, gap size and the tolerance that would close it.

Surfaces:
- UI: a layer/colour list with checkboxes, and a close-gaps field.
- CLI: `--layers`, `--colors`, `--close-gaps`.
- MCP `import_parts`: the same parameters, and the report returns the layer and colour list.
- Exports use the section 3 colours.

**Gate H2:**
- **Labelled, not held out:** 100% either match their label exactly (parts, holes, cut layers) or fail with a message
  that names the fix. A missing part with no warning is a failure.
- **Held out:** at least 95% of real and LightBurn files match exactly; the rest fail clearly.
- **Robustness set:** no crash, panic or hang. Each file imports or fails within 10 s natively.
- **Fuzzing:** 0 failures in 10,000 proptest cases built from the generator's habits, extending
  `crates/core/tests/search_fuzz.rs` and the importer property tests.
- **Fidelity:** every labelled file that imports re-exports within 0.01 mm (G6 method, `scripts/g6_fidelity.py`).
- **LightBurn check** in Anode, as in G6:
  - 10 nested exports (5 DXF, 5 SVG) taken from corpus files import at the exact placed sizes;
  - the CUT, COMMON and LEADIN colours land on separate LightBurn layers.
  - Record it as `benchmarks/results/h2-lightburn-*.md`, with screenshots.
- **Surfaces:** UI, CLI and MCP parity, with end-to-end tests.

### 4.3 N2: LightBurn `.lbrn2` round-trip

1. **Probe the format locally first** (before the trial ends). Make small projects in Anode that isolate:
   - each origin corner (`MirrorX`/`MirrorY`);
   - rotated and mirrored shapes in groups;
   - text with BackupPath, moved;
   - a bitmap copied twice (SourceHash sharing);
   - lead-in settings and a set start point;
   - several layer types (Cut, Scan, Scan+Cut, Offset, Image, Tool).

   Record each finding, and the file that shows it, in `docs/LBRN2.md`, starting from research section 2.1.
2. **Reader:**
   - Parse `.lbrn2` (FormatVersion 1) and `.lbrn` (FormatVersion 0).
   - Resolve shared VertList/PrimList and Bitmap data; build Rect, Ellipse, Path (line and Bézier primitives,
     multi-contour), Group, Text (BackupPath) and Bitmap; apply the XForm chain.
   - Map shapes to layers by CutIndex.
3. **Units:** form nesting units by the section 3 rules, using their outlines or bounding rectangles in mm. Allowed
   rotations and mirroring follow the user's settings (default 0/90/180/270, no mirror).
   Open-stroke bounding axes narrower than two curve tolerances are widened symmetrically to that width
   (at least two 0.000001 mm validator grid units), equally inside groups and standalone. This protects collision geometry;
   the original open paths remain unchanged in the preserving output.
4. **Writer:**
   - For each sheet, copy the document and keep the sheet's units.
   - Update the top-level XForms (placement ∘ old), re-home any omitted shared lists, and add the T1 sheet outline.
   - Leave every other byte as it was where possible. Use a canonical-XML comparison as the contract.
5. **Surfaces:**
   - UI: open `.lbrn2`/`.lbrn`; download per-sheet `.lbrn2` files, or a ZIP of them.
   - CLI: `nestbolt nest` accepts `.lbrn2` and writes per-sheet files.
   - MCP: `import_parts` and `export_layout` support `lbrn2`.

**Gate H3:**
- **Reader:** every public and local sample parses, and each shape's geometry matches lbrn2-to-svg (MIT, independent
  oracle) within 0.01 mm. Compare bounding boxes and 64 sampled points per contour.
  - **Reviewed text prerequisite (decision 5):** originals without embedded text outlines must give a clear instruction
    to re-save in LightBurn or convert text to paths. Preserve their original XML, labels, split and failed geometry
    results. Require the complete geometry comparison on the repaired files; do not claim exact geometry from the
    uncached originals or lossless equivalence of LightBurn's repair save.
- **No-op round-trip:** read then write without nesting is canonically XML-equal to the input for every sample.
- **Nesting round-trip:** a test checks the canonical diff between input and each output. It may contain only
  top-level XForm values, re-homed shared lists, removed units belonging to other sheets, and the optional T1 outline.
- **Validity:** the placed units pass the independent validator.
- **LightBurn check** in Anode, before the trial ends:
  - 5 nested projects open without warnings: groups, text, a bitmap, shared copies, at least 3 layers with different
    cut settings and lead-ins, and both a default and a mirrored origin;
  - shape positions and sizes match Nestbolt's layout (LightBurn's own position/size fields);
  - every layer's settings are unchanged (compare the cut settings dialog before and after).
  - Record it as `benchmarks/results/h3-lightburn-*.md`, with screenshots.
- **Surfaces:** UI, CLI and MCP parity, with end-to-end tests.

**N2 development checkpoint, 2026-10-15:** the [open-stroke and training audit](../benchmarks/results/h3-open-line-fix-20261015.md)
resolves repaired L17 and verifies all eight repairs, 435 original/repaired unit footprints and 114 canonical sheet diffs.
Two new native saves preserve their open paths; the five earlier native layouts revalidate. All public-surface tests pass.
The three frozen native held-out projects remain unevaluated, so H3 is still open and completed weight remains 20%.

### 4.4 N3: curve-heavy parts in the browser

- **Development subset** (never the v1 held-out jobs):
  - m-public-gear-1 to 4 (about 965-1,057 vertices per part);
  - m-sign-1 to 4;
  - m-mechanical-cog-washers;
  - the browser examples `gears` and `letters`.
- **Baseline:** the G5 report. Native vs Chrome and Firefox at 60 s: gear-1 +29.8%, gear-2 +20.6%, gear-3 +16.9%,
  gear-4 +21.4%; signs −0.3% to +2.4%.
- **Levers, measured one at a time** and logged in BENCHMARKS.md, kept or rejected on evidence:
  1. Error-bounded, outward-only simplification of collision proxies, with a vertex budget per part. Exports keep the
     exact curves, and the independent validator still checks the original geometry.
  2. Adaptive flattening tolerance for proxies.
  3. Per-orientation proxy caching.
  4. WebAssembly SIMD.
  5. Worker-count heuristics within 1.5 GB.
- **Constraints:**
  - No WebAssembly threads: GitHub Pages cannot send COOP/COEP headers.
  - v1 rejected a simplified-Sparrow trial because marques no longer fit (BENCHMARKS.md). The rule here: no job that
    fitted before may stop fitting.

**Gate H4:**
- **Quality:** Chrome and Firefox, 60 s, G5 method (`scripts/g5_browser.py`: one worker per job, physical cores only,
  seeds 0-2).
  - Median difference from native on the subset: at most 1%.
  - Every subset job within 5%.
  - The full G5 development set still within its v1 bounds: median within 2%.
- **Scale:** a 2,000-part curve-heavy job (letters and gears, generated like `tests/scale.spec.ts`) imports, nests and
  exports with peak memory under 1.5 GB and no main-thread task over 200 ms.
- **Native:** the 65-job development matrix (60 s, seeds 0-2) keeps every layout valid, with its median material within
  0.5% of `75cbb32`'s development results.

**N3 scale baseline, 2026-10-15:** the required [frozen letters/gears workload](../benchmarks/datasets/browser-curves/README.md)
now runs through the actual app. Both browsers fail to complete initial packing
within 60 seconds; memory stays below 1.5 GB, but no browser export is reached.
The [retained baseline and native diagnosis](../benchmarks/results/h4-curve-scale-baseline-20261015.md)
include an independently valid three-sheet feasibility layout and a valid
300-second native result. Neither is an H4 pass. An earlier conservative starting
layout is the next hypothesis; production defaults and all gate thresholds remain
unchanged.

**N3 early-start checkpoint, 2026-10-15:** the [six-trial probe and public-surface implementation](../benchmarks/results/h4-quick-start-20261015.md)
add an optional Quick initial layout, off by default. The frozen 2,000-part job
gets a checked native incumbent in 7.38 seconds; both browsers now finish and
export valid three-sheet layouts. Scale still fails: working memory peaks at
2.19/2.12 GB and heartbeat gaps at 2,862/1,620 ms. A concurrent CLI test build
changes the validator binary and correctly fails the final harness guard;
unchanged browser assets and separate pinned-binary artifact checks are recorded
without relabelling that run. Preview caching, export assembly and worker memory
are the next measured levers. H4 quality/native matrices and all original gate
conditions remain open; completion stays 20%.

**N3 preview checkpoint, 2026-10-15:** [exact preview reuse](../benchmarks/results/h4-preview-cache-20261015.md)
reduces Chrome's nesting/preview Long Task from 1,608 to 111 ms; the same saved
layouts and native-validated metrics are retained in both browsers. Whole scale
still fails memory and responsiveness: nesting heartbeat gaps are 209/370 ms,
export gaps 2,801/1,569 ms, and working sets 2.099/2.074 GB. All source/executable
guards pass; all 66 enabled browser tests pass. Keep the cache, then measure
worker count and off-thread ZIP assembly separately. Quality/native gates and
the 20% completed milestone total are unchanged.

**N3 archive checkpoint, 2026-10-15:** the [separate one-worker diagnostic and background ZIP change](../benchmarks/results/h4-background-archive-20261015.md)
reduce export heartbeat gaps from 2,614/1,621 ms to 52/51 ms. All four saved
layouts and all twelve compared cutting files remain identical and independently
valid. The worker override is diagnostic; production defaults stay unchanged.
Scale still fails: Chrome private memory peaks at 1.822 GB during nesting and
Firefox records a 202 ms nesting heartbeat gap. All source/executable guards and
74 enabled browser tests pass. Next profile search-worker memory and the
remaining Firefox delay. No thresholds or open quality/native gates change;
completion remains 20%.

**N3 memory checkpoint, 2026-10-15:** [collision-layout lifetime reduction](../benchmarks/results/h4-layout-lifetimes-20261015.md)
removes redundant collision-index copies without changing search operations.
Chrome search-engine memory falls from 694 to 390 MB; both browsers pass scale
with one explicitly selected worker. The unchanged default two-worker setting
still fails memory, with Firefox also reaching a 290 ms heartbeat gap. All saved
layouts and 24 compared cutting files are byte-identical; eight repeatable pairs
retain every result field except elapsed wall time. All 287 workspace and 74
enabled browser tests pass. Next adjust and verify the worker policy; no gate
thresholds or outstanding quality/native requirements change. Completion is 20%.

**N3 automatic-worker checkpoint, 2026-10-15:** [complexity-based worker selection](../benchmarks/results/h4-worker-policy-20261015.md)
caps dense drawings at one search worker and retains two for simpler high-copy
jobs. Both browsers pass the frozen H4 scale workflow with Quick initial layout
enabled: working sets 1.198/1.350 GB, private peaks 1.261/1.276 GB and heartbeat
gaps 68/176 ms. The original G5 scale job also passes with Quick initial layout
off and two effective workers. All four layouts independently validate; H4 layout
bytes and twelve cutting-file comparisons remain identical. All 80 enabled
browser tests pass. The threshold is a heuristic, not a universal memory
guarantee. H4 quality/full-G5/native-matrix requirements remain open; completion
is still 20% and no gate thresholds change.

**N3 quality checkpoint, 2026-10-15:** [all 99 subset layouts validate](../benchmarks/results/h4-quality-checkpoint-20261015.md). Firefox passes at +0.486636% median material; Chrome narrowly misses at +1.014665% against +1%. All individual jobs remain within +5%. The complete G5 and 195-run native comparisons are still open. The original thresholds and completed weight of 20% are unchanged.

### 4.5 N4: common-line cutting

Build the section 3 model:
- **Mode:** spacing = kerf in common-line mode, and the validator is unchanged. Parts are at least one kerf apart, and
  shared edges are those whose kerf/2 centrelines coincide within 0.01 mm.
- **Export:**
  - Detect shared straight segments between neighbours: collinear within 0.01 mm, at least 10 mm long.
  - Write COMMON: centreline toolpaths with each shared segment written once, chained into the fewest paths.
  - CUT keeps the closed true-size outlines.
  - The report gives the total cut length and contour count, with and without common lines.
- **Optional search bonus:** reward merged length as a fraction of total cut length in the placement cost.
  Off by default.
- **Surfaces:** UI (a common-line toggle and kerf field), CLI (`--common-line --kerf <mm>`), MCP parameters. The docs
  state the plasma caveats (good side, pierce at edges, small-part tip-up) and that CAM kerf compensation must be off
  for the COMMON layer.

**Gate H5**, on a common-line set made for N4. Development only: m-box-batch-500, -desktop, -long, -mini, -storage and
-tool, m-mechanical-large-plates and m-mechanical-panel-hardware, plus 5 new jobs of rectangles and brackets. Kerf 0.2 mm (laser) and 1.5 mm (plasma).
- **Geometry:** COMMON paths are exactly the outlines offset by kerf/2. No shared segment appears twice, and chain gaps
  are at most 0.01 mm. Checked by a test with an independent Clipper2 offset.
- **Savings:** with the bonus on, the median cut-length reduction on the set is at least 10%, with material within 1% of
  normal mode at the same spacing. With it off, savings are reported but not gated.
- **Comparison:** deepnest-next's `mergeLines` on the same jobs (its required spacing 0, SVG export), with its merged
  length reported next to ours. Informational.
- **LightBurn check** in Anode: one exported DXF and one SVG open with COMMON on its own layer, at the exact sizes.
- **Surfaces:** UI, CLI and MCP parity, with end-to-end tests.

**Development checkpoint 2026-10-15:** the optional bonus is implemented, off by
default, with UI/CLI/MCP round trips. After the retained [78-run pilot](../benchmarks/results/h5-common-bonus-checkpoint-20261015.md),
the [60-second, three-seed measurement](../benchmarks/results/h5-cutting-development-20261015.md)
validates all 234 Nestbolt layouts. Median cut savings are 13.0311% laser and
13.1005% plasma, meeting the savings condition. Both mechanical jobs exceed the
material guard: +5.219% / +6.508% laser and +4.345% / +5.596% plasma; every other
job is within +1%. Normal mode uses 21 and 49 hole riders, versus zero in common
mode. The native Deepnest SVG comparison is complete: 35 valid runs and four
unscored no-layout outcomes. H5 remains open on material; no gate or input
requirement is changed.

**N4 material follow-up, 2026-10-15:** [48 diagnostic runs](../benchmarks/results/h5-material-probes-20261015.md) validate, but longer initial packing and rigid complementary-bracket pairs both worsen the mechanical-job medians. Neither lever is integrated. H5 remains open on the original +1% material condition; these results do not prove it unreachable.

### 4.6 N5: lead-in allowances

Build the section 3 lead-in scope:
- **Footprint:** each contour's lead path widened by kerf/2, plus a pierce disc of 2 × kerf. It joins that part's
  collision geometry, so no lead crosses another part, another lead or the sheet margin.
- **Placement:** each lead is placed by the section 3 rules, shortening to fit.
  Native 2.1.01 entry precision is 0.1 mm for length and 0.01° for angle: round each length trial down before constructing/validating its paths, and reject angle settings that cannot be entered exactly. Preserve the [native precision failure and mixed-settings check](../benchmarks/results/h6-lead-settings-checkpoint-20261015.md); this refines the implementation, not the H6 gate.
- **Export:**
  - Every contour starts at its lead's attachment point, so LightBurn's own leads land in the reserved space (with
    "Choose best starting point" off; say so in the docs).
  - LEADIN geometry goes on its own layer and colour, for review only.

**Gate H6:**
- the validator checks every footprint against parts, other footprints and margins;
- exported contour start points equal the attachment points;
- in Anode, LightBurn with its own lead-ins at the same length shows no lead crossing a neighbour on 3 nested exports
  (screenshots);
- the material cost of the allowance on the common-line set is reported;
- UI, CLI and MCP parity, with end-to-end tests.

The [independent source-validation checkpoint](../benchmarks/results/h6-lead-source-checkpoint-20261015.md)
now derives coverage from the original job, independently evaluates original
curve attachments and checks owner material as well as neighbours and stock.
The final check is shared by all public surfaces. Explicit flags remain unresolved
contours. The [rigid-group checkpoint](../benchmarks/results/h6-lead-group-checkpoint-20261015.md)
adds multipart planning and separate cutting files under reviewed decision 4.
**H6 completed on 2026-10-15:** [gate evidence and material-cost report](../benchmarks/results/h6-complete-20261015.md)
cover all five requirements. All 156 development layouts validate; median material
cost is +1.0696% for laser and +6.0951% for plasma, with unresolved small-hole
contours explicitly flagged. Original native-previewed starts/plans revalidate
unchanged. No gate threshold, held-out split or published v1 claim changed.

## 5. Tests and evidence

- Rust unit and property tests for every new geometry routine.
- Playwright tests for every UI feature in Chromium and Firefox.
- CLI feature tests in `crates/cli/tests/features.rs`.
- An MCP stdio test per new tool parameter.
- Every gate's evidence goes in `benchmarks/results/` (JSON plus Markdown) and a BENCHMARKS.md entry, failures
  included.
- Update STATUS.md at each milestone.

## 6. Sequencing and dates

The LightBurn trial ends about 2026-11-11. Finish every LightBurn step by 2026-11-06.

1. **Days 1-3:** the N2 format probe (step 1), and the N0 LightBurn-written files and samples, in Anode.
2. **N0:** the rest of the corpus; freeze it and record the hold-out (H1).
3. **N1:** import robustness. Its LightBurn check runs as soon as exports carry colours (H2).
4. **N2:** the round-trip, with its LightBurn check (H3) before 2026-11-06.
5. **N3:** browser curves (H4). It may run alongside N2, but never while a benchmark runs.
6. **N4:** common-line (H5); its LightBurn check before the trial ends if possible, otherwise see section 8.
7. **N5:** lead-ins (H6); its LightBurn check likewise.

## 7. Milestones (progress weights)

| # | Milestone | Weight | Done when |
|---|---|---:|---|
| N0 | Messy-file corpus | 15% | H1 |
| N1 | Import robustness | 25% | H2 |
| N2 | LightBurn round-trip | 25% | H3 |
| N3 | Curve-heavy browser | 15% | H4 |
| N4 | Common-line cutting | 15% | H5 |
| N5 | Lead-in allowances | 5% | H6 |

## 8. Stop rules (tell Artem, then wait)

- **The LightBurn trial has expired** before a gate's LightBurn check. Never reinstall, reset or buy. Report which
  checks remain; all non-LightBurn evidence stands.
- **A source's licence turns out not to be permissive** after its files were committed. Remove the files and report.
- **A lever in N3 or N4 would change the published v1 numbers' meaning** (for example by changing defaults that the
  benchmark relies on). Keep it behind an option and report.
- **sparrow/studio ships fixed sheets or part-in-part** (v1 rule): stop and tell Artem before continuing.

## 9. Risks

- **The `.lbrn2` format is undocumented and could change in 2.2** (multi-page projects). Preserve unknown content
  verbatim, gate on canonical XML, and test on 2.1.01 files.
- **Real-file labels are judgement calls.** Record how each label was derived, and use two readers (ezdxf and Inkscape)
  where they disagree.
- **Proxy simplification has failed once before.** Gate on "nothing that fit before stops fitting" and on the validator.
- **Common-line savings depend on how often parts meet edge to edge at exactly one kerf.** The bonus exists for that.
  If 10% proves unreachable with material within 1%, report the measured trade-off rather than lowering the bar
  silently.
- **Scope creep into CAM.** Leads stay a reserved-space and start-point feature.


## 10. Reviewed decisions

1. **2026-10-13, Artem — R43 scoring exception.** Score the frozen training Iris PE MX/Alps switch plate as one part with 37 holes. The extra labelled part is a duplicate cutout differing by 6.96e-13 mm. Preserve the frozen label, split and failed result. The [approved exception](../benchmarks/results/h2-r43-scoring-exception-20261013.md) pins the exact source/label/manifest hashes; all other H2 requirements and files are unchanged.

2. **2026-10-13, Artem — periodic pushes to main.** Commit and push verified checkpoints to `origin/main` from time to time while pursuing this goal. Fetch and reconcile remote changes first, preserve unrelated work, and use ordinary non-forced pushes. This authorizes repository updates; releases, registry publication and a new final acceptance run still follow their existing approval rules.

3. **2026-10-15, Artem — match LightBurn arc length.** Native 2.1.01 calibration shows that a 3 mm arc uses radius about 3.82 mm at 45° and 1.91 mm at 90°. Artem chose “Match LightBurn’s arc length and update the plan.” This supersedes the original `radius = length / 2` rule: use arc length `L`, sweep `abs(angle)` and radius `L / abs(angle in radians)`, with the zero-angle straight limit. Preserve the native calibration, original rule and failed assumptions in the [calibration report](../benchmarks/results/h6-lead-native-calibration-20261015.md). This changes no milestone gate or held-out allocation; native hole/corner/direction coverage and searched-export checks remain required.

4. **2026-10-15, Artem — separate cutting exports for LightBurn leads.** Keep the editable `.lbrn2` sheet export under N2's preservation rules. For a lead-enabled imported LightBurn project, place new contour starts and LEADIN review paths in separate SVG/DXF cutting files alongside that preserved project. Those cutting files contain original cutting curves; engraving, images and their bounding rectangles must not become cut outlines. Group membership remains rigid. This resolves the output-format choice without permitting changes to the preserved project's child geometry or settings.

5. **2026-10-15, Artem — documented repair prerequisite for uncached Text.** Artem chose “Accept documented repair prerequisite” for the eight original projects with 122 uncached text objects. H3 accepts clear repair instructions on those originals and requires full geometry checks after a native re-save or conversion to paths. Keep original files, labels, split and failed checks unchanged. The [native repair evidence](../benchmarks/results/h3-text-cache-20261014T005902Z.md) already distinguishes the repaired files from lossless preservation: native saving changes some settings. This approval supersedes its historical “not approved” status, not its original measurements or failures. It does not waive checks on any repaired geometry.

6. **2026-10-15, Artem — reject mixed fixed/active groups.** Artem chose “Reject with instructions to regroup in LightBurn.” A Group combining output-enabled artwork and Tool/output-disabled shapes must fail nesting with instructions to ungroup and group the movable artwork separately. Do not split the source Group automatically, move fixed children, or silently keep active cuts fixed on every output sheet. Inspection and byte-preserving no-op reading remain available.
