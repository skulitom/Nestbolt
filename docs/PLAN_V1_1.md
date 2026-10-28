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

**N1 native accounting update, 2026-10-15:** the [completed H3 review](../benchmarks/results/h3-complete-20261015.md)
accounts for all 59 original projects: 48 imported originals match unit membership,
physical cutting holes, fixed shapes and cutting layers; all eleven original
rejections remain explicit. Approved repairs supply complete geometry checks for
the 122 uncached Text objects without changing the original files or labels. This
supports H2's native accounting but does not replace its complete warning/fidelity
review or remaining reserved evaluation. The original held-out success threshold
and pending denominator clarification remain unchanged. H2 is still open.

**N1 current regression review, 2026-10-15:** the [native diagnostic review](../benchmarks/results/h2-native-warning-review-20261015.md)
identifies twelve accepted training files missing expected explanatory messages.
The [current vector export replay](../benchmarks/results/h2-export-replay-20261015.md)
matches all 246 accepted libraries and validates their saved layouts, without
new searches. Of 492 exports, 491 are byte-identical; one retained byte mismatch
passes a separate geometric bound of 0.000491918 mm against the unchanged
0.01 mm limit. Native messages and the remaining reserved acceptance are still
required. Original failures, labels and the held-out denominator remain intact.

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

**Earlier N2 development checkpoint, 2026-10-15:** the [open-stroke and training audit](../benchmarks/results/h3-open-line-fix-20261015.md)
resolves repaired L17 and verifies all eight repairs, 435 original/repaired unit footprints and 114 canonical sheet diffs.
Two new native saves preserve their open paths; the five earlier native layouts revalidate. All public-surface tests pass.
At that checkpoint, the three frozen native held-out projects remained unevaluated,
so H3 was still open and completed weight was 20%.

**Earlier N2 missing-settings checkpoint, 2026-10-15:** [native defaults and training-label checks](../benchmarks/results/h3-missing-layer-native-20261015.md) resolve L36's remaining attachment mismatch. All 45 imported originals now match unit membership, physical cut holes, fixed shapes and cutting layers. Omitted T1/T2 settings keep shapes fixed, and omitted Line settings retain original cuts in sidecars. All eight repairs match membership and holes; L42's already documented native Scan+Cut-to-Scan change remains explicit. All 64 reader payloads are unchanged and 114 canonical writer comparisons pass. At that checkpoint, the three reserved native projects remained unevaluated and no gate or completed weight changed.

**H3 completed on 2026-10-15:** the [complete requirement review](../benchmarks/results/h3-complete-20261015.md)
accounts for all 59 original projects and eight approved repairs. After a committed
training calibration and frozen plan, all three reserved native projects pass
once: 199 leaves / 247 contours, exact membership/hole/layer labels, nine allowed
canonical sheet comparisons and three independently valid actual searches.
Combined evidence covers 1,749 comparable original leaves, 477 repaired leaves,
120 diagnostic sheet comparisons and 443 diagnostic units. The five native-checked
layouts revalidate on the current build with unchanged settings and contents;
all public-surface tests pass. The original 122 uncached Text objects, L42's native
repair layer change and all historical failures remain explicit. Reserved inputs
remain evaluation-only. N0/H1 + N2/H3 + N5/H6 now total **45%**; H2/H4/H5 remain open.

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

**N3 compiler follow-up, 2026-10-15:** the [isolated fat-LTO pilot](../benchmarks/results/h4-lto-probe-20261015.md)
validates all 44 layouts, but the small Chrome improvement comes with worse Firefox
material use and charged-work rate. The compiler change is not integrated. The
original failed subset remained authoritative at that checkpoint; H4 stayed open
and completion was 45%.

**N3 bounded-score checkpoint, 2026-10-15:** the [profile-led scoring change](../benchmarks/results/h4-score-pruning-20261015.md)
preserves reference arithmetic and equal-score behavior while stopping already-worse
collision scores early. All eight equal-work candidate comparisons are exact. All
99 development layouts and 18 extra public example validations pass. Chrome and
Firefox both pass the unchanged subset limits: median +0.710335% / +0.664508%,
worst +3.316424% / +3.268252%. The change is retained; full G5, the 195-run native
comparison and current-build scale confirmation remain open. All 297 workspace,
26 optimized CLI and 84 enabled browser tests pass. No geometry, search setting,
gate or held-out allocation changes; H4 remains incomplete and completion is 45%.

**N3 current-build scale confirmation, 2026-10-15:** [all four workflows pass](../benchmarks/results/h4-current-scale-20261015.md)
on the retained bounded-score build. Curve-heavy Chrome/Firefox working-set peaks
are 1.257/1.352 GB, private peaks 1.223/1.275 GB and maximum heartbeat gaps
87.8/175 ms. Original G5 also passes with quick start off and two search workers.
Every 2,000-part layout independently validates with exact metric agreement;
both curve-heavy layouts and all twelve cutting exports match the previous
passing scale bytes. The committed full development comparison has started,
retaining all thresholds and 699 new attempts plus 81 verified reused results.
Temperature readings were unavailable and are recorded as a limitation. H4
remains open pending the full results and requirement review; completion is 45%.

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

**N4 exchange follow-up, 2026-10-16:** the [72-attempt paired pilot](../benchmarks/results/h5-exchange-pilot-v2-20261016.md)
validates every outcome, but all four mechanical/kerf medians remain above +1%
material, at +4.175294% to +5.869406%. No candidate run records an exchange
proposal. Two separately planned debug observations show neither reaches the
exchange call. The isolated candidate is not integrated. A future experiment may
test the existing bounded initial relocation opportunity; the complete original
H5 conditions and failed results remain unchanged.

**N4 early-call preparation, 2026-10-16:** [the isolated candidate](../benchmarks/results/h5-early-exchange-preparation-20261016.md)
now tries exchange at the initial feasible window, before gap filling can bypass
it, within the existing bounded relocation opportunity. Seven focused and 82
optimized core tests pass, as do exact normal-mode and repeated common-mode
authored API checks. Its full-window test accepts an exchange. The [new 72-outcome
pilot](../benchmarks/results/h5-early-exchange-pilot-20261016/plan.json) is committed
before measurement and waits for the current release quality/scale sequence.
No mechanical quality result, source integration or H5 credit is claimed.

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

7. **2026-10-16, Artem — next release when ready.** After discussing a preview release following the full performance comparison, Artem said: “when you are ready feel free to make a new release. We might need to update the readme”. This authorizes preparing and publishing the next GitHub release once release checks pass, including updating the README and release notes. Describe incomplete import acceptance and common-line material limits explicitly; do not claim that the v1.1 plan is complete. Preserve existing releases and benchmark claims. Registry publication and a new final acceptance evaluation retain their separate scope and rules.

8. **2026-10-20, Artem — keep the original H2 gate.** In the [recorded answer](../benchmarks/results/h2-gate-decision-20261020.md), Artem chose “Keep the original gate and leave H2 open”. Retain the 95% exact-import requirement across all 25 held-out files, including the two deliberate negatives; do not substitute the proposed 23-positive denominator. The recorded classifications cap literal exact-import success at 23/25 (92%), so H2 receives no completion credit. Preserve the frozen split, labels and all original results. The three native evaluations remain once-only; the other 22 vectors remain unevaluated. This resolves the denominator question previously described as pending and does not waive the remaining requirements.

### Verification checkpoint — 2026-10-16

The [full bounded-score development comparison](../benchmarks/results/h4-full-development-20261016.md)
passes all recorded limits with 780 valid layouts. Native median change against
frozen v1 is 0%; browser medians are +0.150364% Chrome and +0.194317% Firefox.
Both aggregate and all three individual-seed G5 median/total checks pass.
The exact CI curve repair and [native diagnostic corrections](../benchmarks/results/native-diagnostics-surfaces-20261016.md)
are now integrated for the authorized `0.2.0-alpha.1` preview. Because the hole
index changes search cost, the final build needs its own performance confirmation.
H4 requirement review and H2/H5 work remain open; completion remains **45%**.
No threshold, held-out allocation or published v1 result is changed.

The integrated preview's completed [Chrome arm](../benchmarks/results/h4-preview-chrome-failure-20261016.md)
now has 201 valid layouts and passes full G5, but its eleven-job median is
**+1.046217%**, above the unchanged **+1%** H4 limit. Native passes with a 0%
median change across 65 jobs. The [complete original matrix](../benchmarks/results/h4-preview-development-20261016.md)
is now sealed: all 603 new layouts validate, Firefox passes its subset at
+0.788924%, and both full G5 comparisons pass. Chrome's subset failure remains;
no unchanged-build repeat or threshold adjustment is made.
The preview release remains pending, H4 is incomplete, and completion stays 45%.

The subsequent [isolated score-bound probe](../benchmarks/results/h4-score-chunks-probe-20261016.md)
passes its unchanged eleven-job limits with 99 valid layouts: Chrome +0.378238%
and Firefox +0.432882% median material. Four fixed-work baseline/candidate pairs
preserve every result field except elapsed wall time. Only bound-check granularity
changes; the original failure remains. Full comparison, scale and integration
checks are still required, so H4 and the 45% completion total remain unchanged.


**N3 integrated score-bound outcome, 2026-10-16:** the [complete current matrix](../benchmarks/results/h4-preview-score-release-20261016.md)
retains 603 new and 195 reused valid layouts. Native and full G5 aggregate and
individual-seed checks pass. Chrome's curve-subset median is +1.032679%, failing
the unchanged +1% limit; Firefox passes at +0.881781%. The conditional scale
sequence stops before measurements. Current-build profiling is diagnostic only;
no unchanged-build repeat, selected seed, threshold adjustment or release follows.
H4 remains open and completed milestone weight stays 45%.


**N4 early-exchange outcome, 2026-10-16:** the [new paired pilot](../benchmarks/results/h5-early-exchange-pilot-20261016.md)
retains 72 valid layouts. Earlier calling reaches 179 proposals and ten accepted
exchanges, but all four mechanical/kerf pairs still fail (+5.324324% to +6.390250%
material versus ordinary mode), and the laser bracket control fails at +1.251430%.
Reject this candidate for integration; do not start the full 13-job gate from
these results. Original methods, budgets and +1% limit stay fixed. Inspect the
geometry/repair failure stages before choosing another experiment. H5 stays open.


**N3 tree-depth preparation, 2026-10-16:** [the isolated candidate](../benchmarks/results/h4-quadtree-depth-preparation-20261016.md)
passes all build checks and 75 optimized core tests. Only the separator-window
base tree depth changes from four to three, retaining exact geometry and budgets.
The [single-use eleven-job pilot](../benchmarks/results/h4-quadtree-depth-probe-20261016/plan.json)
is committed before measurements, after the earlier H4 and H5 sessions finish.
No improvement, integration or H4 credit is claimed. Original thresholds and
failed results remain; completion stays 45%.


**N4 stage-diagnostic preparation, 2026-10-16:** [the isolated observer](../benchmarks/results/h5-exchange-diagnosis-preparation-20261016.md)
passes 82 optimized tests, strict lint and authored accepted/failed/disabled trace
checks. It only records exchange rejection stages, without changing the rejected
algorithm or budgets. The [four-case diagnostic plan](../benchmarks/results/h5-exchange-diagnosis-20261016/plan.json)
waits for the H4 pilot to finish and be sealed. Tracing can perturb timing; it
cannot establish a quality gain or replace the failed paired comparison.
H5 stays open and completion stays 45%.


**N3 tree-depth pilot outcome, 2026-10-16:** [all 99 layouts validate](../benchmarks/results/h4-quadtree-depth-probe-20261016.md).
Chrome's subset median is +0.689439% and Firefox's
is +0.639475%, both within the unchanged +1% limit;
every job is within +5%. Exact independent metrics, coverage, source and affinity
guards pass. The isolated candidate is eligible for integration checks and a
fresh full matrix, followed by current scale/package checks. Earlier full-run
failures are retained. No H4 closure or release; completion stays 45%.


**N4 stage-diagnostic outcome, 2026-10-16:** [all four layouts validate](../benchmarks/results/h5-exchange-diagnosis-20261016.md).
Of 37 attempted exchanges, 35 fail receiving-sheet repair and two are accepted.
Every proposal has two or three actual blockers, while the current experiment
evicts only one. Moving the full smaller obstruction set is a distinct next
hypothesis, not an established improvement. Original quality failures, budgets
and H5 limits remain. Two omitted-zero counter reader errors and a report-format
error are preserved and corrected only against saved artifacts; no search is
repeated. H5 remains open and completion stays 45%.


**N4 obstruction-set preparation, 2026-10-16:** [the isolated candidate](../benchmarks/results/h5-obstruction-set-preparation-20261016.md)
can exchange a complete smaller group of actual blockers, retaining single-part
fallbacks, deadlines and independent guards. All 85 optimized core tests, strict
lint and authored public comparisons pass. A missing fixture in the first copy
and its failed build remain preserved. No development quality run, integration
or H5 credit; a future committed pilot waits for current H4 checks to finish.


**N3 tree-depth integration, 2026-10-16:** candidate `aba989e` now
[passes local integration checks](../benchmarks/results/h4-depth-integration-20261016.md),
including 302 workspace tests, 75 optimized core tests, 27 CLI tests and 86
browser tests. An overlapping evidence write interrupted the first bundle
confinement inventory; the same bundle passes after competing writes stop,
with the original failure retained. The [fresh full plan](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
retains 603 new plus 195 verified frozen-v1 outcomes and every original limit.
Scale, complete exported-curve checks and current packages remain separate.
No H5 experiment is integrated, no H4 closure or release; completion stays 45%.


**N3/N4 sequencing, 2026-10-16:** the new 603-attempt matrix is running from its
committed plan. The [conditional scale/export plan](../benchmarks/results/h4-preview-depth-scale-plan-20261016/plan.json)
seals/reports quality first, then runs the unchanged scale workflows only on a
pass and checks all 2,000 exported curve placements in each browser. Root
sources/builds remain frozen. The [72-attempt obstruction-set pilot](../benchmarks/results/h5-obstruction-set-pilot-20261016/plan.json)
is committed but unopened; it waits for this entire sequence to finish.
No threshold changes, automatic release or additional completed gate weight.


**N3 recovered full quality, 2026-10-16:** the [completed comparison](../benchmarks/results/h4-depth-reboot-recovery-20261016.md)
preserves the servicing interruption and all 402 completed native/Chrome
outcomes, adds only the missing 201 Firefox outcomes, and retains 195 frozen-v1
outcomes. All layouts validate and all original quality limits pass: native
median +0.000614%; Chrome/Firefox subset medians +0.851159%/+0.828477%, worst
jobs +2.455588%/+2.561291%. Full G5 aggregate and each-seed bounds also pass.
The separate Firefox recovery took 27.451 minutes; no continuous original
session or general speed gain is claimed. Raw evidence is sealed. The new
conditional scale/export sequence has started; complete H4 review remains
required. No gate closure or release; completion stays 45%.


**N3/H4 complete, 2026-10-16:** [the full requirement audit](../benchmarks/results/h4-depth-complete-20261016.md)
passes every original condition on the integrated depth-three build: full
native/G5/subset quality, validity and quantities, both 2,000-part workflows
in both browsers, memory below 1.5 GB, responsiveness at most 200 ms, exact
saved curve/control-point fidelity for every curved-workload placement, and
four actual screenshot reviews. The maximum observed RSS is 1.352409 GB;
the maximum heartbeat gap is 199 ms. Original source/build/input guards,
unshared WASM memory, historical failures and the servicing interruption are
preserved. Sealed archives pass CRC, every-member length and SHA-256 checks.
N0/H1 (15%) + N2/H3 (25%) + N3/H4 (15%) + N5/H6 (5%) total **60%**. H2/H5
remain open. The recovery-aware 72-outcome H5 pilot starts only after this
complete audit; its candidate remains isolated from the qualified preview.


**N4 obstruction-set outcome, 2026-10-16:** the [72-outcome paired pilot](../benchmarks/results/h5-obstruction-set-recovered-pilot-20261016.md)
validates every original layout but fails five of eight material pairs. All
four mechanical medians remain +4.663095% to +5.962959% above ordinary mode;
mixed-bracket laser is +1.540301%. There are 147 attempts and ten accepted
exchanges, none on panel hardware. The candidate stays unintegrated and every
failed outcome/limit is preserved. This is not an infeasibility proof. H5
remains open and completed milestone weight stays 60%.


**Preview published, 2026-10-16:** [v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is published at `c36baa8` under Artem's release authorization. All five release
jobs pass; [actual downloads and all four build attestations](../benchmarks/results/preview-depth-published-20261016.md)
verify, including exact tag/source binding and unchanged stable Latest/assets.
[Published Windows CLI/MCPB feature checks](../benchmarks/results/preview-depth-published-features-20261016.md)
pass with authored inputs only. The original Python-launch and shared-cache
verification errors remain preserved alongside their limited recoveries.
The README links the preview and separates hosted v0.1.0 from newer local
browser features. No new registry version, reserved evaluation or public
competitor claim. H2/H5 remain open; completed milestone weight stays 60%.


**N4 diagnosis, 2026-10-17:** [four current-candidate traces](../benchmarks/results/h5-obstruction-stage-diagnosis-20261017.md)
validate all layouts but show zero complete blocker-set proposals: 620 sampled
sets fail the smaller-area heuristic. All 29 attempted exchanges are partial;
27 fail receiving-sheet repair and two succeed. An [independently validated
authored witness](../benchmarks/results/h5-area-witness-20261017.md) demonstrates
that returning more combined part area can preserve both validity and material.
The first incorrectly oriented witness is retained with its failed material
assertion. This motivates a separately tested complete-set eligibility change;
it proves no mechanical feasibility or quality gain. Production stays unchanged,
and H2/H5 remain open at 60% completed weight.


**N4 complete-set preparation, 2026-10-17:** [the isolated eligibility change](../benchmarks/results/h5-complete-set-preparation-20261017.md)
passes 85 core tests, strict lint and authored public comparisons. Complete
two/three-blocker sets may now be considered regardless of combined part area;
both-sheet repair and final independent geometry/material limits remain.
Equal/larger-area tests pass without extra material; impossible returns retain
the incumbent. The [committed 72-outcome pilot](../benchmarks/results/h5-complete-set-pilot-20261017/plan.json)
uses the unchanged paired method and original thresholds. It has not started
at this checkpoint. Production remains unchanged; H2/H5 are open at 60%.


**N4 complete-set outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-complete-set-pilot-20261017.md),
including an independent filled-outer audit of 133,412 same-sheet pairs in all
48 common-mode layouts. All four mechanical material pairs still fail +1%, at
+5.433792% / +6.521291% for large plates and +5.700699% / +5.764347% for panel
hardware (laser/plasma). Four control pairs meet material limits. Of 74 exchange
attempts, eleven succeed; none on panel hardware. The candidate is rejected for
integration and the full gate is not opened. Counters alone do not establish
which repair stage now limits progress. Original outcomes/limits remain;
H2/H5 are open at 60%.


**N4 return-stage diagnosis, 2026-10-17:** [all four traced outputs validate](../benchmarks/results/h5-complete-stage-diagnosis-20261017.md).
All 23 actual attempts move complete blocker sets, pass receiving-sheet repair
and fail return-sheet repair within the existing budget. There are 427 eligible
equal/larger-area samples and no smaller complete sets. No partial attempt or
acceptance occurs. Source/binary/input/trace integrity is verified. Next inspect
how returned groups are placed and repaired; these observations do not prove
feasibility or impossibility, or replace the failed quality pilot. Production
and gate limits remain unchanged; H2/H5 are open at 60%.


**N4 return-frame preparation, 2026-10-17:** [the isolated initialization change](../benchmarks/results/h5-return-frame-preparation-20261017.md)
passes 90 core tests, strict lint and authored public checks. A returned group
may rotate/reflect into the vacated incoming frame when every part permits it;
otherwise it retains the previous translation. Both repairs and exact material
limits remain. The original type error, arithmetic-test error and guarded
0.0007 mm² material increase are preserved and reviewed. Separate tests require
strict rejection and a successful exchange with a fixed envelope. The
[72-outcome comparison](../benchmarks/results/h5-return-frame-pilot-20261017/plan.json)
retains original inputs, budgets and limits. No integration or quality claim.
H2/H5 remain open at 60%.


**N4 return-frame outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-return-frame-pilot-20261017.md),
with an independent hole-reservation audit of 133,535 same-sheet
pairs across all 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.208689%; m-mechanical-large-plates at 1.5 mm: +4.649005%; m-mechanical-panel-hardware at 0.2 mm: +5.475484%; m-mechanical-panel-hardware at 1.5 mm: +5.886483%
There are 11 accepted exchanges from 71 attempts.
Reject this candidate for integration; do not open the full 13-job gate for it. Production remains unchanged. Counters alone do not establish the
remaining repair bottleneck or impossibility. H2/H5 remain open at 60%.


**N4 return-frame diagnosis, 2026-10-17:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-frame-stage-diagnosis-20261017.md)
record 23 complete-set attempts. Every reciprocal frame is permitted and every
receiving-sheet repair succeeds, but all return-sheet repairs fail. None reaches
the final geometry/material guard. Orientation fallback is not the immediate
cause in these observations. Next inspect source capacity and placement of the
larger returned groups; area ratios alone do not prove impossibility. A balanced
multi-part exchange needs a separate authored feasibility example first.
Original results/limits remain; no production change or H5 closure. Completion 60%.


**N4 balanced-group witness, 2026-10-17:** [two independently valid layouts](../benchmarks/results/h5-balanced-exchange-witness-20261017.md)
show two incoming rectangles exchanging with three return squares at identical
material and quantities. A necessary stacking bound excludes all single-incoming
choices within that explicitly scoped selection. This supports investigating
balanced groups, but proves no mechanical improvement; inspect actual source
capacity/placement before implementing a new heuristic. No optimizer run,
production change or gate relaxation. H2/H5 remain open at 60%.


**N4 capacity diagnosis, 2026-10-18:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-capacity-diagnosis-20261017.md)
record 25 complete reciprocal attempts. Independent geometry checks confirm
clear repaired receivers and overlapping repaired return sheets. Source area
occupancy is 75.281–85.554% of the actual shortened search boundary: area alone
does not prove infeasibility, and occupancy alone does not prove a packing exists.
Next seek a complete, independently valid repack of fixed saved assignments with
their original boundary and legal orientations before changing repair. Preserve
all failed outcomes; no production change, relaxed limit or H5 credit. 60% complete.


**N4 assignment feasibility, 2026-10-18:** [three independently valid source packings](../benchmarks/results/h5-assignment-repack-20261018.md)
fit the unchanged saved boundaries and quantities: both large-plate cases and
the 0.2 mm panel case. The 1.5 mm panel case remains unresolved after six retained
rounds. This proves only source-assignment feasibility, not whole-job material
improvement. Earlier traces repeat eight distinct assignments over 25 attempts
(17 repeats after first occurrence). Next test retained compatible repair progress
within the existing shared budget, preserving geometry/orientation identities,
tracker-key consistency, rollback and independent acceptance. No production change
or relaxed gate; H2/H5 remain open at 60%.


**N4 source-repair reuse outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-return-reuse-pilot-20261018.md).
The independent filled-outer audit checks 133,470 same-sheet
pairs across all 48 common-mode layouts, retaining hole reservation and kerf.
There are 6 failed material pairs out of eight under the original +1%
limit. m-mechanical-large-plates at 0.2 mm: +5.607522%; m-mechanical-large-plates at 1.5 mm: +5.124968%; m-mechanical-panel-hardware at 0.2 mm: +6.668421%; m-mechanical-panel-hardware at 1.5 mm: +5.745273%; c-bracket-mixed at 0.2 mm: +2.419752%; c-bracket-mixed at 1.5 mm: +1.016169%
The candidate records 11 accepted exchanges from 73 attempts and
37 compatible source-repair reuses. Reuse counts do not establish repair
completion or explain remaining failures. Reject this candidate for integration; do not open the full 13-job gate for it. Production, prior failures
and frozen inputs remain unchanged. H2/H5 remain open at 60%.


**N4 reuse-stage diagnosis, 2026-10-18:** [four diagnostic outputs validate](../benchmarks/results/h5-return-reuse-stage-diagnosis-20261018.md).
All 24 complete-obstruction exchanges repair the receiver, then fail source
repair. Sixteen resume a compatible saved state; seven reduce loss further,
none reaches zero, and none reaches final material/geometry acceptance.
The reader verifies original inventories and exact restored loss across each
reuse. The issue is incomplete repair, not observed cache-state corruption.
Each case spends 0.903–1.054 seconds in source repairs within the existing
early-call budget. Available windows shrink after successive attempts; three
late attempts reach source repair with an already-expired pair deadline and
return their unchanged state. These observed durations are not minimum required
repair times and do not prove that a larger allowance would solve H5.
Production and all failed results remain unchanged. H2/H5 remain open at 60%.


**N4 balanced-pair preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-balanced-group-preparation-20261018.md)
passes 97 optimized core tests, strict lint, ten authored observer outcomes,
four public CLI comparisons and five unchanged paired-harness checks. All 90
prior tests remain; seven new tests cover the two-to-three exchange, permissions,
frozen sheets, bounded pair selection, valid single fallback and rejected
attempts. The original test-assumption failures and independently valid fallback
output remain preserved. Normal output stays exact and common replay passes.

Two nearby copies can move together against their complete obstruction union,
using at most half the existing exchange window before the single-part path.
The original total budget, independent geometry/material acceptance and saved
incumbent guards stay. [The committed 72-outcome plan](../benchmarks/results/h5-balanced-group-pilot-20261018/plan.json)
retains the same cases, kerfs, seeds, matched cores, 60-second limits and +1%
condition. No measured improvement, production change or H5 credit is claimed;
the full 13-job gate remains required. H2/H5 are open at 60%.


**N4 balanced-pair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-balanced-group-pilot-20261018.md).
The independent filled-outer audit checks 133,456 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.188368%; m-mechanical-large-plates at 1.5 mm: +5.469920%; m-mechanical-panel-hardware at 0.2 mm: +6.652162%; m-mechanical-panel-hardware at 1.5 mm: +5.589744%; c-bracket-mixed at 0.2 mm: +1.501017%
The candidate accepts 19/41 total exchanges, including 13/25
two-part exchanges. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 pair-identity diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-balanced-stage-20261018.md).
There are 11 attempts and 3 accepted exchanges, including
2 pairs. 2 accepted exchanges return the
same original part types and quantities as they take; per-sheet inventory is
unchanged in those cases, although poses may change. Immediate material falls
in 0 accepted exchanges and last-sheet occupied
extent falls in 0. These traces do not reconstruct
the earlier pilot or prove a later benefit/harm from rearrangement. Retained
proposal identities, losses, material and extent are preserved. The independent
filled-outer audit checks 18,569 pairs. No gate relaxation,
production change, reserved-file access or H5 credit. H2/H5 remain open at 60%.
Source inspection also confirms that accepting an exchange short-circuits
the following gap-fill and relocation calls in that window. The next isolated
change should test whether gap filling after an accepted exchange can use its
new arrangement, while preserving the total search limit and normal-mode
behavior. This identifies a missed execution path, not a measured quality gain.


**N4 post-exchange gap-fill preparation, 2026-10-18:** [the isolated correction](../benchmarks/results/h5-post-exchange-fill-preparation-20261018.md)
passes 98 optimized core tests, strict lint/build, ten authored observer outcomes,
four public CLI comparisons and five paired-harness checks. A new known-gap
regression fails on the unchanged runtime, then passes when direct gap filling
continues after an accepted exchange. Normal output stays exact and common
fixed-work replay passes. Original exchange, repair, geometry/material rules,
search limits and all 97 earlier tests remain. Counters track the follow-up
calls and moved parts. The committed 72-outcome pilot preserves its original
paired method and +1% limit. No measured improvement, production change or
H5 credit yet. H2/H5 remain open at 60%.


**N4 post-exchange gap-fill outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-post-exchange-fill-pilot-20261018.md).
The independent filled-outer audit checks 133,374 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.484564%; m-mechanical-large-plates at 1.5 mm: +5.388338%; m-mechanical-panel-hardware at 0.2 mm: +6.386542%; m-mechanical-panel-hardware at 1.5 mm: +5.563315%
The candidate accepts 19/42 total exchanges, including 12/24
two-part exchanges. The post-exchange gap-fill step runs 19 times and moves 14 parts; these counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 productive-exchange preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-productive-exchange-preparation-20261018.md)
passes 101 optimized core tests, preserving all 98 previous tests, strict
lint/build, ten authored public outcomes, four CLI comparisons and five
paired-harness checks. It distributes bounded pairs across original part
types and rejects same-inventory swaps without material reduction. Two
new regressions fail on the unchanged runtime, while a positive witness
saving over 99.9 mm2 passes. The original rounding-only positive fixture
is preserved. Sixteen independent validations cover eight actual authored
outcomes. Normal output and common fixed-work replay pass; geometry,
budgets and the +1% material limit remain. The committed 72-outcome pilot
retains the previous paired method. No production change or H5 credit;
H2/H5 remain open at 60%.


**N4 productive-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-productive-exchange-pilot-20261018.md).
The independent filled-outer audit checks 133,603 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.483065%; m-mechanical-large-plates at 1.5 mm: +5.402498%; m-mechanical-panel-hardware at 0.2 mm: +7.022646%; m-mechanical-panel-hardware at 1.5 mm: +5.298801%
The candidate accepts 12/121 total exchanges, including 1/62
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 11 parts. The new guard rejects 45 same-inventory proposals without material improvement; these counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 productive-exchange diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-productive-stage-20261018.md).
Of 28 attempts, 18 fail source repair, seven reject unchanged
inventory, one expires after repair, one fails the material guard and one
is accepted without immediate material/extent reduction. All eight paired
attempts preserve inventory; all twenty single attempts return more recorded
item area than they remove. The large-plate source's largest item has only
one copy, excluding it from the same-item pair selector. Requested source
windows range from -0.003617 to 0.398944 seconds, with 4 already
nonpositive. Timings do not prove minimum repair time or impossibility.
The independent outer audit checks 18,669 pairs. The
next hypothesis is bounded mixed-item pairs with authored correctness checks;
budgets and every geometry/material limit remain. No integration or H5 credit;
H2/H5 remain open at 60%.


**N4 mixed-assignment witness, 2026-10-18:** [two distinct incoming rectangles](../benchmarks/results/h5-mixed-exchange-witness-20261018.md)
(30x40 and 30x50 mm) can exchange with three 30x30 mm squares. Both authored
layouts preserve all seven parts and exactly 19,700 mm2 material; frozen CLI
and independent filled-outer checks pass. Eight conservative height bounds
rule out either chosen incoming part moving alone while one filler remains
on each sheet, even if it moves. The two incoming parts have different IDs
and dimensions, so the current same-original-item selector cannot pair them.
This is a scoped geometric witness, with zero optimizer runs. It neither
proves global impossibility nor mechanical quality. The next candidate still
requires an original-runtime regression, allowed-pose/rollback tests and the
unchanged H5 quality gates. Production stays unchanged; H2/H5 remain open at 60%.


**N4 mixed-exchange preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-mixed-exchange-preparation-20261018.md)
passes 107 optimized core tests, retaining all 101 previous tests, strict
lint/build, ten public outcomes, four CLI comparisons and five pilot checks.
Six new tests and twelve actual before/after validations cover mixed parts,
per-member poses, frozen sheets, bounded choices and rollback. The original
runtime failure and first candidate's missed seed-two group placement remain
preserved; mixed-group corner anchors correct that failure without weakening
tests. Up to six mixed pairs interleave existing same-item pairs within the
original phase/budget. All geometry/material rules and paired methods remain.
No measured quality claim or integration; H2/H5 stay open at 60%.


**N4 mixed-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-mixed-exchange-pilot-20261018.md).
The independent filled-outer audit checks 133,299 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +6.069459%; m-mechanical-large-plates at 1.5 mm: +6.160993%; m-mechanical-panel-hardware at 0.2 mm: +6.770269%; m-mechanical-panel-hardware at 1.5 mm: +5.607046%
The candidate accepts 12/132 total exchanges, including 1/69
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 19 parts. The new guard rejects 49 same-inventory proposals without material improvement; mixed pairs account for 0/11 accepted/attempted exchanges. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 mixed-pair diagnosis preparation, 2026-10-18:** [the separate observer](../benchmarks/results/h5-mixed-stage-preparation-20261018.md)
passes 107 optimized tests, strict lint/build, nine actual authored traces and
22 malformed-observation checks. Each paired generation call records an exact
sample-rejection partition, retained proposals and deadline truncation;
existing traces retain choices, repair loss/time and final rejection stage.
All seven exchange counters reconcile. Insertions reverse exactly, with the
other 151 files unchanged. Four serial seed-zero mechanical observations are
planned under original 60-second limits. Logging can perturb trajectories;
this diagnoses the failed pilot without replacing it. No integration or H5
credit; production and reserved inputs remain unchanged at 60% completion.


**N4 mixed-pair diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-mixed-stage-20261018.md).
The two large-plate traces examine all 24 pair calls and 4,764 samples without
sample truncation, but retain no paired proposal. The area filter rejects
1,721 otherwise eligible samples, including 575 mixed samples. Panel traces
generate only the first same-item pair per kerf; all seven attempted paired
swaps reject unchanged inventory, and no mixed pair is generated. Their
repairs already have zero loss and each takes less than 0.0001 seconds;
remaining construction/validation time is not separately measured.
Overall, 28 attempts yield 19 failed source repairs, seven neutral rejections,
one material rejection and one accepted single swap saving 18.669 mm2
immediately. The filled-outer audit checks 18,626 pairs.
The next hypothesis targets the proposal-area filter with an authored runtime
regression; it is not a quality claim. H2/H5 remain open at 60%.

**N4 larger-return witness, 2026-10-18:** [a valid mixed pair exchange](../benchmarks/results/h5-larger-return-witness-20261018.md)
returns 2,790 mm2 of parts after removing 2,700 mm2, while keeping all seven
parts and every material metric unchanged at 19,700 mm2. Frozen CLI and
independent filled-outer checks validate both authored layouts. Eight
conservative height bounds exclude either selected incoming part moving
alone while one filler stays on each sheet. The current pair-area filter
excludes this complete return set. This proves a limitation of that filter,
with zero optimizer runs; an actual runtime regression and full candidate
checks remain necessary. It does not establish mechanical quality or H5.


**N4 larger-return candidate review, 2026-10-18:** [the first implementation is unqualified](../benchmarks/results/h5-larger-return-review-20261018.md).
The new larger-return regression first fails against unchanged runtime, then
passes after removing the paired proposal area filter. All four new tests
pass, but the complete suite reports 107 passes and four older failures.
Every original assertion, failed source and binary is preserved. Six new
actual outcomes and ten original/broader comparison observations pass 32
independent CLI validations. The broader results are equal in one case and
save 66.0529 / 266.0522 mm2 in two; the gap-filling case is 0.0388 mm2 worse
and leaves its named small part on the last sheet despite one recorded fill.
A logging-setup failure and shared-target stale executable are preserved;
recovery uses a fresh target and reuses all completed original observations.
Next inspect the intermediate fill and accepted snapshots before correcting
behavior or targeted tests. No assertion change, quality pilot, integration
or H5 credit; H2/H5 remain open at 60%.


**N4 larger-return qualification, 2026-10-18:** [the corrected isolated candidate](../benchmarks/results/h5-larger-return-preparation-20261018.md)
passes 113 optimized core tests, strict lint/build, ten public outcomes,
four CLI comparisons and five pilot checks. The original candidate's four
failures remain. An exact replay with eight validated intermediate layouts
shows gap filling moves the named part correctly; later compression moves it
again while reducing material. Four route-specific tests now target their
invariants, 103 prior tests are unchanged and six tests are added. The actual
strict material guard rejects even a one-ULP increase. A direct post-exchange
fill test and all six larger-return outcomes pass fourteen more independent
validations. Guard extraction reverses exactly; all other runtime text is
unchanged beyond the area filter and unused sum removal. The same 72-outcome
pilot is committed before measurement. No quality or integration claim;
H2/H5 remain open at 60%.


**N4 larger-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-larger-return-pilot-20261018.md).
The independent filled-outer audit checks 133,465 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.739579%; m-mechanical-large-plates at 1.5 mm: +6.431410%; m-mechanical-panel-hardware at 0.2 mm: +6.701091%; m-mechanical-panel-hardware at 1.5 mm: +4.836540%; c-bracket-mixed at 1.5 mm: +1.989411%
The candidate accepts 13/119 total exchanges, including 10/81
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 15 parts. The unchanged neutral guard rejects 33 same-inventory proposals without material improvement; mixed pairs account for 1/4 accepted/attempted exchanges. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 larger-return diagnosis preparation, 2026-10-18:** [the isolated observer](../benchmarks/results/h5-larger-stage-preparation-20261018.md)
passes all 113 unchanged core tests, strict lint/build, fourteen authored trace
cases, the direct strict-material guard and 31 malformed-observation checks.
All 154 formatted files match an exact reconstruction, with only two observed
files. Timings distinguish construction, repairs and validation; complete
after-exchange/after-fill layouts will be checked independently. The first
logger compile failure remains preserved. Four serial seed-zero mechanical
observations retain the original 60-second budgets. Logging may perturb wall
time; this diagnoses the rejected candidate without replacing its failed
quality comparison. No integration or H5 credit; completion stays 60%.


**N4 larger-return diagnosis, 2026-10-18:** [all four final and four intermediate layouts validate](../benchmarks/results/h5-larger-stage-20261018.md).
The filled-outer audits check 23,542 same-sheet pairs. Of 23 attempts, two
accept, fourteen fail source repair and seven are neutral inventory rejections.
Panel paired repairs start with zero loss; repeated validation costs 0.367 /
0.299 seconds, and no mixed pair is generated. Large-plate exchanges save only
86.418 / 40.2735 mm2 immediately; filling changes neither total and leaves
0.965 / 0.552 seconds of the original exchange opportunity. Next verify whether
neutral trials preserve exact original-item poses before considering an early
rejection. Equal inventory/material alone cannot justify skipping validation.
These instrumented observations do not replace the five failed pilot pairs;
no integration or H5 credit, and completion remains 60%.


**N4 exact-state diagnosis preparation, 2026-10-18:** [the observer passes all 116 optimized tests](../benchmarks/results/h5-exact-state-preparation-20261018.md),
strict lint/build, fourteen authored trace cases and 37 malformed-record checks.
All 113 prior tests remain unchanged. Exact reconstruction covers all 154 files;
153 are unchanged from the preceding observer. Two panel-hardware diagnostics
will compare complete internal pose multisets and independently check both
layouts saved for neutral rejections. The comparison records observations only;
all decisions, full validators, material guards and time limits remain.
No production integration, reserved access or quality claim; H2/H5 remain open
and completed weight stays 60%.


**N4 exact-state diagnosis, 2026-10-18:** [both final and all 12 saved layouts validate](../benchmarks/results/h5-exact-state-20261018.md).
1 of 6 neutral trials exactly preserve the complete internal physical state.
Independent filled-outer checks cover 111,838 same-sheet pairs.
Public pose multisets match in 1/6 pairs; exact internal comparison also
requires shared model/container identity and full float bits. All original
validators and decisions remain. This diagnostic establishes no quality gain;
the five failed pilot comparisons remain authoritative. H2/H5 stay open at 60%.

An exact-state early rejection now has an observed target, but its impact on
search quality is unproven. A separate candidate may reject only a complete
exact-state match before repeated validation, preserving shared container and
original-item identity, full transform bits, reflection and multiplicity.
Every changed state and every accepted exchange must retain the original
full geometry/material checks. Qualify the predicate and early branch with
authored regressions, preserve expired/disabled behavior and rollback, and
repeat the existing paired development protocol only for that changed build.
Do not infer a quality gain or promote it from these diagnostic timings.


**N4 exact-state candidate preparation, 2026-10-18:** [all 117 optimized tests pass](../benchmarks/results/h5-exact-reject-preparation-20261018.md),
with all 113 prior tests unchanged. The new branch regression first fails
against the original runtime; its source, executable and log are preserved.
The candidate rejects only a complete exact internal-state match before
repeated validation. Changed states and all accepted exchanges retain the
original full validators, strict material guards and budgets. Twelve branch
outcomes pass 24 frozen-CLI checks; strict lint/build, ten public outcomes,
four CLI comparisons and five adversarial pilot checks also pass. The paired
72-outcome method is unchanged and committed before measurement. No quality
result, production integration or release claim; H2/H5 remain open at 60%.
All six hosted checks on main `924336a` have passed.


**N4 exact-state early-rejection outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-exact-reject-pilot-20261018.md).
The independent filled-outer audit checks 133,535 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.349182%; m-mechanical-large-plates at 1.5 mm: +5.485080%; m-mechanical-panel-hardware at 0.2 mm: +6.767422%; m-mechanical-panel-hardware at 1.5 mm: +5.195747%; c-bracket-mixed at 0.2 mm: +1.027791%; c-bracket-mixed at 1.5 mm: +1.177346%
The candidate accepts 13/125 total exchanges, including 11/87
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 12 parts. The early exact-state and original neutral guards reject 41 same-inventory proposals without material improvement; mixed pairs account for 2/5 accepted/attempted exchanges. The neutral total includes 3 exact-state rejections before repeated validation. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

The [saved-height follow-up](../benchmarks/results/h5-exact-reject-pilot-20261018/source-review.json) reconstructs all twelve prior neutral-layout material values exactly; every sheet maximum is unchanged. It suggests qualifying an exact material-profile rejection only if this pilot still fails. No new filter or quality claim.


**N4 material-profile candidate preparation, 2026-10-18:** [all 123 optimized tests pass](../benchmarks/results/h5-material-profile-preparation-20261018.md),
with all 117 prior tests unchanged. The candidate rejects same-inventory
trials whose exact original-geometry profiles prove unchanged charged
material. It uses the existing validator footprints and preserves every
accepted geometry/material check. Budgets and coefficients are unchanged;
profile work uses the existing vertex charge. Five proofs, 23 witness pairs
and 47 frozen-CLI checks cover geometry contexts, real gains and an invalid
overlap; 12 branch outcomes pass another 24 CLI checks. The original failing
branch regression is preserved. Strict lint/build, public parity/replay,
five harness tests and exact formatted-source reconstruction pass. The
unchanged 72-outcome method is committed before measurement. No quality,
integration or release claim; H2/H5 remain open at 60%.


**N4 material-profile rejection outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-material-profile-pilot-20261018.md).
The independent filled-outer audit checks 133,235 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.169797%; m-mechanical-large-plates at 1.5 mm: +6.158488%; m-mechanical-panel-hardware at 0.2 mm: +6.407212%; m-mechanical-panel-hardware at 1.5 mm: +5.654893%; c-bracket-mixed at 0.2 mm: +1.823168%
The candidate accepts 13/147 exchanges, including 11/108 paired and 1/18 mixed-item exchanges. Follow-up gap filling runs 13 times and moves 16 parts. Of 49 neutral rejections, 3 are caught by exact internal-state equality and 46 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.

The [read-only frontier inspection](../benchmarks/results/h5-material-profile-pilot-20261018/source-review.json) finds unchanged top-defining insert poses in all six older neutral panel pairs. It uses no new search or held-out geometry and makes no claim about every current failure.


**N4 height-setting part observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-frontier-observer-preparation-20261018.md).
All 123 existing optimized tests pass. The observer records original part
families for available, visited and attempted exchange choices alongside the
validated public baseline. It changes no decision, work charge or budget.
Sixteen authored cases, sixteen malformed-record rejections and
35 frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.


**N4 height-setting part diagnosis, 2026-10-18:** [both final and baseline layouts validate](../benchmarks/results/h5-frontier-observer-20261018.md).
None of 25 attempts selects the insert family defining the credited sheet
height. Both traces visit only choices 0, 1 and 12; the insert pair at index
6 and insert singles from 73 are never visited. Twelve trials are rejected
early and thirteen stop at source repair or expiry. The independent audit
checks 31,740 filled-outer pairs and reconstructs both material values
exactly. This supports qualifying a boundary-first member ranking under the
existing choice limits, budgets and full acceptance guards. It proves no
quality gain; H2/H5 remain open at 60%.

The actual search reaches only choice indices 0, 1 and 12 in both
diagnostics: a frame pair, its mixed frame/cog alternative, and the first
frame single. The insert pair is present at index 6; insert singles start at
73. Neither is visited. Both height-setting copies are inserts on the same
last sheet that receives the material offcut credit. Removing repeated
neutral validation increased attempts but did not reach that family.

The next isolated candidate should rank incoming members by proximity to the
last sheet's upper edge before forming the existing bounded pair and single
choices. In the solver's rotated strip frame this is the placed shape's
rightmost extent. Keep area as a tie-breaker and retain stable equal ties,
the six same-item and six mixed-pair limits, sampling, repair caps, all work
budgets and full geometry/material acceptance checks. Prove that a smaller
part at the boundary outranks a larger interior part, that ties are stable,
and that disabled/expired behavior and useful existing exchanges remain.
Only after those checks should the unchanged paired quality pilot run.
This is a ranking hypothesis, not evidence of feasible improvement or a
reason to relax any H5 requirement.


**N4 boundary-priority preparation, 2026-10-18:** [all 126 optimized tests pass](../benchmarks/results/h5-boundary-priority-preparation-20261018.md),
with 123 prior tests unchanged. The isolated candidate orders incoming parts
by upper extent before area, retaining stable ties and the existing bounded
pair generators. Selected pairs keep their original member anchor order. Budgets, sampling, repairs, work charges and every full
acceptance check are unchanged. Two original ordering regressions fail as
expected and are preserved; all three new tests pass afterwards. The first
revision also exposes three existing exchange regressions; preserving pair
anchors resolves them with unchanged assertions and retained failures. The order
fixture and twelve rejection-boundary outcomes pass 25 frozen-CLI checks.
Strict lint/build, public parity/replay, five pilot tests and exact source
reconstruction pass. The unchanged 72-outcome plan is committed before
measurement. No quality or integration claim; H2/H5 remain open at 60%.


**N4 boundary-priority outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-boundary-priority-pilot-20261018.md).
The independent filled-outer audit checks 133,236 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.771660%; m-mechanical-large-plates at 1.5 mm: +4.211101%; m-mechanical-panel-hardware at 0.2 mm: +5.991880%; m-mechanical-panel-hardware at 1.5 mm: +5.770657%; c-bracket-mixed at 0.2 mm: +1.591789%; c-bracket-mixed at 1.5 mm: +1.089470%
The candidate accepts 17/100 exchanges, including 12/73 paired and 0/0 mixed-item exchanges. Follow-up gap filling runs 17 times and moves 20 parts. Of 1 neutral rejections, 0 are caught by exact internal-state equality and 1 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 exact boundary-copy observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-boundary-observer-preparation-20261018.md).
All 126 existing optimized tests pass. The observer records original part
families and exact physical poses for available, visited and attempted
exchange choices alongside the validated public baseline. Each chosen pose
matches a unique baseline copy exactly, with complete single-copy coverage. It changes no decision, work charge or budget.
Sixteen authored cases, 21 malformed-record rejections and
35 frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.


**N4 exact boundary-copy diagnosis, 2026-10-18:** [both diagnostic outcomes and every saved baseline validate](../benchmarks/results/h5-boundary-observer-20261018.md).
19 of 19 attempts select at least one actual part defining the credited sheet height; 0 select every part defining that height. 1 of the first group and 0 of the second group are accepted. The independent audit checks 31,794 filled-outer
pairs and reconstructs every material value exactly. Every selected physical
pose matches its baseline exactly. This identifies copy coverage, without
establishing final quality or packing feasibility. The six failed pilot
comparisons remain authoritative. H2/H5 remain open at 60%.


**N4 boundary-pair preparation, 2026-10-18:** [all 130 optimized tests pass](../benchmarks/results/h5-boundary-pair-preparation-20261018.md),
including all 126 prior tests unchanged. The isolated candidate includes the
two highest source members first in the appropriate same-item or mixed pair
list, removes duplicate pairs and retains the six-plus-six caps and remaining
nearby alternatives. Original pair anchors, repairs, budgets, work charges and
all full acceptance checks remain. Three expected failures are preserved.
Independent original-contour checks confirm both highest physical copies in
same-item and mixed-item witnesses. Those and twelve rejection-boundary cases
pass 26 frozen-CLI checks. Strict lint/build, public parity/replay, source
reconstruction and five pilot harness checks pass. The unchanged 72-outcome
plan is committed before measurement. No quality claim; H2/H5 remain open at 60%.


**N4 boundary-pair preflight recovery, 2026-10-18:** the first launch stops
before any measurement because the old balanced-diagnostic PID now belongs to
`svchost.exe`, whose command line is protected. Its creation time is later than
the original diagnostic's recorded start, proving PID reuse. The old runner
and committed plan are preserved in [the recovery record](../benchmarks/results/h5-boundary-pair-pilot-20261018/preflight-recovery/checks.json).
The guard now checks process creation time before attempting the command
line. Six checks cover missing/reused processes, active original-runner
rejection, the existing different-command behavior and both inaccessible
identity cases. Unresolved identity still fails closed. The two old H4 PIDs
are absent. Block, scoring, case and measurement functions are AST-identical;
no candidate, budget, input or scoring change and zero searches before repair.
The amended plan is committed before its first measurement. H2/H5 remain open
at 60%.


**N4 boundary-pair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-boundary-pair-pilot-20261018.md).
The independent filled-outer audit checks 133,454 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.750258%; m-mechanical-large-plates at 1.5 mm: +5.823218%; m-mechanical-panel-hardware at 0.2 mm: +6.614117%; m-mechanical-panel-hardware at 1.5 mm: +5.725452%; c-bracket-mixed at 0.2 mm: +1.439312%; c-bracket-mixed at 1.5 mm: +1.316785%
The candidate accepts 14/120 exchanges, including 11/77 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 15 parts. Of 3 neutral rejections, 0 are caught by exact internal-state equality and 3 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 boundary-pair observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-boundary-pair-observer-preparation-20261018.md).
All 130 existing optimized tests pass. The observer records original part
families and exact physical poses for available, visited and attempted
exchange choices alongside the validated public baseline. Each chosen pose
matches a unique baseline copy exactly, with complete single-copy coverage. It changes no decision, work charge or budget.
Sixteen authored cases, 21 malformed-record rejections and
35 frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.


**N4 boundary-pair diagnosis, 2026-10-18:** [both diagnostic outcomes and every saved baseline validate](../benchmarks/results/h5-boundary-pair-observer-20261018.md).
22 of 22 attempts select at least one actual part defining the credited sheet height; 11 select every part defining that height. 0 of the first group and 0 of the second group are accepted. The independent audit checks 31,766 filled-outer
pairs and reconstructs every material value exactly. Every selected physical
pose matches its baseline exactly. This identifies copy coverage, without
establishing final quality or packing feasibility. The six failed pilot
comparisons remain authoritative. H2/H5 remain open at 60%.


**N4 exchange-failure observation, 2026-10-18:** [the isolated failure-detail observer qualifies](../benchmarks/results/h5-exchange-failure-observer-preparation-20261018.md).
All 130 optimized tests and strict code checks pass. The original short-circuit
conditions, clock reads and work charges are unchanged; extra loss/pose or
validated-trial data is recorded only inside existing failed branches.
Sixteen authored cases, 35 public baseline checks, twelve exact parent branch
witnesses, 34 malformed-record rejections and four synthetic parser cases pass.
The same two serial panel searches retain both kerfs, seed zero and 60 seconds.
Logging can change wall trajectories; no quality comparison or integration.
The committed scope requires independent checks of captured trials. H2/H5
remain open at 60%.


**N4 exchange-failure diagnosis, 2026-10-18:** [the focused cause audit is complete](../benchmarks/results/h5-exchange-failure-observer-20261018.md).
Recorded causes are 4 material increased, 18 source loss positive. All 4 captured final-trial
layouts validate independently, with exact metrics and independently rebuilt
material. Original/final geometry and every selected physical pose also pass.
Failed source snapshots remain diagnostic states. No quality rerun or
integration follows from these observations; H2/H5 remain open at 60%.


**N4 contained-return preparation, 2026-10-18:** [the isolated return-seed change qualifies](../benchmarks/results/h5-contained-return-preparation-20261018.md).
All 133 optimized tests pass, retaining all 130 prior tests. A fitting returned
group may translate inside the existing source bounding box, with charged
geometry work and an exact second check. Other cases keep the old poses.
Existing choices, budgets, repairs and full acceptance checks remain.
Two expected old-behavior failures and the first implementation's rotated-edge
failure are preserved; its small interior-seed correction changes no assertion.
Strict lint/build, twelve branch outcomes, 29 public CLI checks, deterministic
replays, exact source reconstruction and five harness checks pass. No quality
pilot has started; its plan must be committed first. H2/H5 remain open at 60%.


**N4 contained-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-contained-return-pilot-20261018.md).
The independent filled-outer audit checks 133,170 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.219533%; m-mechanical-large-plates at 1.5 mm: +5.440022%; m-mechanical-panel-hardware at 0.2 mm: +5.617328%; m-mechanical-panel-hardware at 1.5 mm: +5.658268%; c-bracket-mixed at 0.2 mm: +2.014519%
The candidate accepts 14/111 exchanges, including 12/74 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 14 parts. Of 3 neutral rejections, 0 are caught by exact internal-state equality and 3 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 free-space return preparation, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-free-return-preparation-20261018.md)
tries at most 256 translations per returned part against the source and earlier
returns, keeping each orientation and reflection. It checks filled-hole collision
geometry, charges work, observes the shared deadline, and always retains every
part with the previous seed as fallback. Original choices, repairs and strict
acceptance remain. All 137 optimized tests pass: 130 prior tests are unchanged,
three former no-improvement expectations now require strict material reduction
or exact incumbent retention, and four new regressions retain their expected
old-behavior failures. The first implementation's three failures remain with six
independent CLI checks proving the new authored improvement; runtime guards remain.
Four new frozen-CLI checks and independent filled-outer checks qualify two authored
outputs; 12 original branch outcomes, 24 branch validations, 10 public outcomes,
four public comparisons and five adversarial harness tests pass. Exact source
reconstruction, lint and build pass. The same matched pilot is ready to be planned;
no quality measurement has begun and no integration or H5 credit is earned.
H2/H5 remain open at 60%.


**N4 free-space-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-free-return-pilot-20261018.md).
The independent filled-outer audit checks 133,284 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.281226%; m-mechanical-large-plates at 1.5 mm: +5.706866%; m-mechanical-panel-hardware at 0.2 mm: +6.604732%; m-mechanical-panel-hardware at 1.5 mm: +5.890184%; c-bracket-mixed at 1.5 mm: +1.090957%
The candidate accepts 16/93 exchanges, including 13/62 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 16 times and moves 17 parts. Of 6 neutral rejections, 0 are caught by exact internal-state equality and 5 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 actual return-seed observation preparation, 2026-10-18:** the [isolated diagnostic](../benchmarks/results/h5-free-return-observer-preparation-20261018.md)
records actual contained/placed return poses, original source members, charged
work, repair losses and validated material outcomes including acceptance. It
reconstructs the failed candidate exactly after removing observations; all 137
tests remain unchanged and pass, as do lint and build. Sixteen authored cases,
35 frozen-CLI baselines, 32 trial validations,
twelve exact parent branch witnesses and 44 malformed-record checks qualify the
reader. Four serial mechanical diagnostics are planned; no measurement has begun.
Logging can affect wall trajectories and supports no quality claim. No production
change, reserved-input access or H5 credit. H2/H5 remain open at 60%.


**N4 actual return-seed diagnosis, 2026-10-18:** [four original-job outputs validate](../benchmarks/results/h5-free-return-observer-20261018.md).
The seed stage incurs work but changes none of 43 observed return poses. Of 24
attempts, two valid large-plate exchanges save only 28.887/132.567 mm², seventeen
panel source repairs retain positive loss and actual filled-outer violations,
and five valid panel trials increase material and are correctly rejected.
Four baselines/finals pass 37,119 filled-outer pair checks; all seven captured
material trials pass independent validation and exact material reconstruction.
The one-success-per-window caller motivates a bounded continuation experiment
under the same absolute deadline, after authored correctness checks. This is
not yet implemented and does not solve the panel repair failures. Original
limits, failed evidence, production and reserved inputs remain; H2/H5 stay open at 60%.


**N4 exchange-continuation preparation, 2026-10-18:** the [qualified isolated candidate](../benchmarks/results/h5-exchange-chain-preparation-20261018.md)
allows up to four exchanges under the original absolute deadline, continuing only
after a strict material gain. Rejection or an accepted flat result stops it. All
single-step guards and the preceding return initializer remain. All 141 optimized
tests pass, with 137 unchanged prior tests and four new regressions. The expected
two old-behavior failures and an earlier source assembly syntax failure remain.
Seven saved chain outputs pass fourteen frozen-CLI checks and independent geometry;
twelve original branch outcomes, 24 branch checks, ten public outcomes, four public
comparisons and five harness tests pass. Source reconstruction, lint and build pass.
The four-job matched pilot is ready to be planned; no new quality run has begun.
This does not resolve panel repair failures or earn H5 credit. H2/H5 remain open
at 60%; production and release claims are unchanged.


**N4 exchange-continuation outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-exchange-chain-pilot-20261018.md).
The independent filled-outer audit checks 133,153 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.359062%; m-mechanical-large-plates at 1.5 mm: +5.690931%; m-mechanical-panel-hardware at 0.2 mm: +6.541327%; m-mechanical-panel-hardware at 1.5 mm: +5.555891%
The candidate accepts 28/169 exchanges, including 25/101 paired and 2/5 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 22 parts. Of 6 neutral rejections, 0 are caught by exact internal-state equality and 5 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 continuous-repair qualification failure, 2026-10-18:** the [isolated allocation](../benchmarks/results/h5-continuous-repair-failure-20261018.md)
passes 142 tests and fails three unchanged exchange regressions. It uses the
existing relocation allowance and lets each source repair use its phase remainder.
The new source-repair witness validates, but the old larger-return and mixed-item
examples lose required swaps. Six independent validations confirm valid retained
incumbents with the same material as the preceding accepted results. The authored
delay is explicitly simulated; no wall-time or quality claim follows. All failures
remain, no assertions change, and no quality pilot starts. Next preserve the
original short phase, then allow strictly improving continuous repairs with the
remaining allowance. Production is unchanged; H2/H5 remain open at 60%.


**N4 two-phase repair qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-extended-repair-preparation-20261018.md)
retains the original short exchange phase, then uses the remaining existing
relocation allowance for longer source repairs. Both phases share four accepted
exchanges; the extended phase requires strict material gains. The original guards,
overall budget and validation reserve remain. All 148 optimized tests pass:
141 old bodies unchanged and seven new regressions. The three opportunities lost
by the rejected direct-long-source allocation match their prior witnesses exactly.
Both red runs and a corrected new frozen-sheet fixture are preserved. Thirteen
saved extended outcomes pass 26 CLI checks and independent geometry; the actual
source-repair fixture, original branch checks, public replay, source reconstruction,
lint, build and five harness tests also pass. A matched four-job pilot is ready
to be planned. No quality improvement, integration or H5 closure is claimed.
H2/H5 remain open at 60%; production and release claims are unchanged.


**N4 extended-repair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-extended-repair-pilot-20261018.md).
The independent filled-outer audit checks 133,152 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.499695%; m-mechanical-large-plates at 1.5 mm: +6.491064%; m-mechanical-panel-hardware at 0.2 mm: +5.679440%; m-mechanical-panel-hardware at 1.5 mm: +5.568800%; c-bracket-mixed at 1.5 mm: +1.594065%
The candidate accepts 44/472 exchanges, including 32/239 paired and 1/47 mixed-item exchanges. Follow-up gap filling runs 16 times and moves 27 parts. Of 24 neutral rejections, 0 are caught by exact internal-state equality and 23 by the material profile before full validation. Counts do not establish time saving or improved final quality. The extended phase accepts 20/322 attempts and rejects 191 material-flat trials. Six extended acceptances are mechanical; all flat rejections are bracket cases. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 provisional assignment qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-assignment-bridge-preparation-20261018.md)
keeps the original short search, then may cross validated material-flat steps
when last-sheet filled area strictly decreases. Only a final material gain commits
the sequence; incomplete steps roll back with their accepted counters. An actual
old-policy fixture demonstrates two flat steps followed by a valid material gain.
All 156 native tests pass: 148 old bodies, that witness and seven new policy tests.
Five expected old-behavior failures remain. Eight initial and 24 new-output CLI
checks, independent filled geometry, exact old witnesses, public replay, source
reconstruction, lint, build and five harness tests pass. The original four-step
cap, total deadline, validation reserve and geometry guards remain. No quality
comparison has begun, and no production change or H5 credit is claimed.
H2/H5 stay open at 60%.


**N4 assignment-bridge outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-assignment-bridge-pilot-20261018.md).
The independent filled-outer audit checks 133,388 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.936840%; m-mechanical-large-plates at 1.5 mm: +4.638902%; m-mechanical-panel-hardware at 0.2 mm: +6.747151%; m-mechanical-panel-hardware at 1.5 mm: +6.156172%
The candidate accepts 44/505 exchanges, including 32/267 paired and 4/44 mixed-item exchanges. Follow-up gap filling runs 17 times and moves 23 parts. Of 29 neutral rejections, 0 are caught by exact internal-state equality and 28 by the material profile before full validation. Counts do not establish time saving or improved final quality. The extended phase attempts 309 repairs and records 21 steps, including 5 flat steps. 18 steps belong to committed sequences; 3 roll back across 3 rollbacks. The canonical area guard rejects 189 flat trials. Committed intermediate steps need not each improve material; their sequence ends with strict whole-job improvement. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 joint-repair witness, 2026-10-18:** the [unchanged-runtime authored test](../benchmarks/results/h5-joint-repair-witness-20261018.md)
shows why repairing fixed sheet assignments can fail: two source rectangles cannot
fit together even in the full usable sheet. The existing separator finds a valid
joint rearrangement by moving the extra source part to the receiver. Material
drops from 29,699.9994 to 28,799.9993 mm², with the earlier sheet exactly fixed.
Five independent CLI checks retain three valid outputs and two expected invalid
proposals; eight filled-outer pairs pass. One audit error compared authored f64
and converted f32 coordinates as byte-identical; it is preserved, and the corrected
audit reuses the same saved outputs without changing tolerance or rerunning search.
All runtime code and 156 prior test bodies remain unchanged; only the new test ran.
This proves a constructed case, not policy selection or development-job quality.
Next qualify a bounded joint-repair policy before any new matched pilot. H2/H5
remain open at 60%.


**N4 joint-repair qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-joint-repair-preparation-20261018.md)
retains the short phase, then repairs only the selected receiver/source pair
within the remaining original allowance. It rechecks the exact cropped source,
lowers parts into freed space with existing bounded sampling, and commits a joint sequence only
after strict final whole-job material improvement. Incomplete sequences restore
their layout, tracker and accepted counters. All 165 native tests pass, including
157 unchanged prior tests and eight new policy tests. Independent validation covers
32 saved native layouts and 93 filled-outer pairs;
ten public outcomes, four CLI comparisons and six common-mode hole-reservation
checks pass. Source reconstruction, exact prior witnesses, lint and build pass.
The two insufficient-gain repairs, one newly invalid flat-fixture assumption,
initial compile error and audit error remain preserved. The rollback fixture uses the previously validated compacted output and
retains every assertion; runtime, guards and earlier tests are unchanged
by that fixture correction. A new committed pilot plan and harness checks are
still required before quality measurement. Production is unchanged; H2/H5 remain
open at 60%.

**N4 joint-repair pilot plan, 2026-10-18:** the [72-outcome plan](../benchmarks/results/h5-joint-repair-pilot-20261018/plan.json)
is prepared for the qualified isolated candidate. Four unchanged development jobs,
both kerfs, three seeds and three arms retain the original 60-second budgets and
rotating matched physical cores. Six execution/scoring functions are AST-identical
to the preceding pilot; all five existing adversarial harness tests pass. The
finisher retains archive/metric checks and adds joint-repair completion, expiry,
acceptance and rollback counter checks. Every outcome is retained; no search has
started at this checkpoint. Only a passing original material limit on every pilot
pair can open the full 13-job comparison. Production is unchanged; H2/H5 remain
open at 60%.

**N4 joint-repair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-joint-repair-pilot-20261018.md).
The independent filled-outer audit checks 133,466 same-sheet
pairs across all 48 common-mode layouts. Five of eight material pairs fail the
original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.612886%; m-mechanical-large-plates at 1.5 mm: +4.680766%; m-mechanical-panel-hardware at 0.2 mm: +6.781641%; m-mechanical-panel-hardware at 1.5 mm: +5.716098%; c-bracket-mixed at 1.5 mm: +1.481353%
There are 55/789 accepted/attempted exchanges. Joint repair attempts 589 pairs: 270 complete, 300 fail and 19 expire. It records 35 provisional steps, including 10 flat steps; 28 steps commit and 7 roll back across 4 rollbacks. Only committed counts survive rollback. Pair completion alone does not mean whole-job acceptance or final quality improvement. Reject this candidate for integration; do not open the full 13-job gate for it. The isolated candidate retains its 165 passing native tests,
prior witnesses and complete qualification evidence. Production remains unchanged.
The next diagnostic will trace actual accepted joint repairs and their material
gain before choosing another policy. H2/H5 remain open at 60%.

**N4 joint-repair observation plan, 2026-10-18:** the [diagnostic observer](../benchmarks/results/h5-joint-observer-preparation-20261018.md)
passes all 165 unchanged tests and preserves 86 exact native witnesses. Its 48
linked native trace records pass structural checks; nine malformed records are
rejected. Independent checks validate 23 saved layouts and 53 filled-outer pairs.
Four public fixed-work outcomes match the unobserved candidate exactly except
elapsed time. All 157 source files reconstruct, with 155 unrelated files unchanged;
lint/build pass. The first public reference-path error is preserved and its saved
outcome reused. The [four-case plan](../benchmarks/results/h5-joint-observer-20261018/plan.json)
retains both mechanical jobs, both kerfs, seed zero, 60 seconds and serial physical
CCD0 CPU 8. It records actual pair membership, material gains, repair/lowering
times, expiry, rejection and rollback. No development observation has started at
this checkpoint. Logging can change wall trajectories; no quality comparison,
pilot retry or integration follows. Production and the released preview remain
unchanged; H2/H5 remain open at 60%.

**N4 actual joint-repair diagnosis, 2026-10-18:** [all four serial diagnostics validate](../benchmarks/results/h5-joint-observer-20261018.md).
Fifteen attempts yield ten completed repairs, five committed steps, five
material-increase rejections and five expiries. Eight completed repairs move
extra members beyond the proposed swap, including all five accepted repairs.
Independent checking validates 40 saved layouts and 173,333 filled-outer pairs;
all 21 whole-job material values reconstruct exactly. Panel lowering never
reduces the source top in six observed stages. Four selected panel top pairs
expose a 10.901367 mm band when removed, before returns are placed. This motivates
an explicit source-boundary target, subject to an actual valid witness and full
qualification; it does not establish feasibility. Original limits, failures and
production remain unchanged. All six checks on pushed main `e0945cd` pass.
No quality/release claim or H5 credit; H2/H5 remain open at 60%.

**N4 source-frontier qualification, 2026-10-18:** [the explicit witness and automatic policy pass](../benchmarks/results/h5-frontier-preparation-20261018.md).
The original helper leaves the authored source at 87.200677 mm with its old crop
and finds 51.000558 mm under the exposed boundary. Automatic selection also finds
a valid strict gain and rolls back unfinished flat steps. All 171 native tests,
166 unchanged earlier tests, 139 exact earlier outputs, strict lint/build and six
public checks pass. Independent audits preserve quantities, fixed sheets and
reserved holes, including 856 public filled-outer pairs. The extra target scan
is charged; empty sources keep the original crop. All deadlines, the shared cap,
material limits and production remain unchanged. A new matched pilot is still
required; no H5 or release credit. H2/H5 remain open at 60%.

**Browser curve-test follow-up, 2026-10-18:** [the d414824 trace and local correction](../benchmarks/results/browser-curve-initial-layout-20261018.md)
preserve a Chromium import/export failure: no complete eight-part layout within
five seconds. This fidelity test now explicitly uses quick initial layout,
retaining the five-second allowance and all original assertions, with added checks
for all eight parts and the saved option. The full local suite passes 86 tests
with four skips, two workers and zero retries; hosted confirmation is pending.
Application source, benchmark limits and release assets are unchanged. H2/H5
remain open at 60%.

**N4 source-frontier pilot plan, 2026-10-18:** the [72-outcome matched plan](../benchmarks/results/h5-source-frontier-pilot-20261018/plan.json)
is ready for the qualified isolated policy. The same four jobs, two kerfs, three
seeds, ordinary/common baseline engines, 60-second allowance and rotating physical
cores remain. Six execution/scoring functions are AST-identical to the preceding
pilot; all five adversarial harness checks pass. The verified preflight confirms
that earlier local measurements are finished. Archive, metric, hole and rollback
checks remain; a separate counter identifies proposals with a tighter source crop.
No measurement has started at this checkpoint. Every original failure and threshold
remains. The full 13-job comparison still requires every pilot material pair to
pass. Production is unchanged; H2/H5 remain open at 60%.

**N4 source-frontier outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-source-frontier-pilot-20261018.md),
but five of eight material pairs fail the original +1% limit: m-mechanical-large-plates at 0.2 mm: +6.496681%; m-mechanical-large-plates at 1.5 mm: +4.989335%; m-mechanical-panel-hardware at 0.2 mm: +6.588633%; m-mechanical-panel-hardware at 1.5 mm: +5.416304%; c-bracket-mixed at 0.2 mm: +2.829306%
Independent checking covers all 48 common layouts and 132,966 filled-outer
pairs. The candidate records 63/347 accepted/attempted exchanges. Joint repair has 145 attempts: 63 complete, 61 fail and 21 expire. There are 143 proposed calls with tighter source crops, 35 committed joint steps and 5 rolled-back steps. All accepted counts exclude rolled-back steps. No candidate pair beats its matched common-baseline median.
Reject this candidate for integration. The next investigation checks saved layouts
for geometrically constructed transfers into narrow gaps missed by uniform sampling;
it must produce actual validated layouts before another policy is justified.
All limits and production remain unchanged; H2/H5 remain open at 60%.

**Hosted browser confirmation, 2026-10-18:** [main 4b13a85 passes the browser job](../benchmarks/results/browser-curve-hosted-confirmation-20261018.md):
86 tests pass with four opt-in skips, including the corrected curve import/export
test in Chromium and Firefox. The original failed job remains preserved. This
confirms the test-only correction; the separate Windows workflow checks are
still pending. Product source, release assets and gate limits remain unchanged.

**N4 saved-gap diagnosis, 2026-10-18:** [four saved mechanical layouts](../benchmarks/results/h5-saved-gap-diagnosis-20261018.md)
produce no fixed-neighbour transfers into earlier sheets in the tested convex-hull
or concave constructions. A direct-target source pass moves one insert without
material gain. Four smaller source moves per case save 0.054057–1.572117 mm of
height, recovering only 0.0348–0.7374% of the remaining material gap. All 33 public
CLI checks (21 unique layouts) and independent filled-outer checks pass. These are
post-hoc finite-angle geometry diagnostics, not quality/speed evidence or a proof
of infeasibility. Preserve them and investigate validated multi-part constructions
before proposing another runtime change. Production, budgets, four-step cap,
material limits and the published preview remain unchanged; completion stays 60%.

**N4 mixed-pattern diagnosis, 2026-10-18:** [verified component constructions](../benchmarks/results/h5-pattern-construction-20261018.md)
find compact two-bracket/one-insert groups and smaller free-angle round-part pairs.
All 446 component CLI checks and independent checks of 948 incomplete placement
attempts pass their stated scope. The component checks use subset quantities and
may enlarge stock; they do not validate a whole original job. Both large-plate
cases pass the refined finite-catalog area check, but no complete target placement
is found; the panel catalogs still exceed available area. Keep all failures and
test actual-outline placement and joint assignment before any runtime proposal.
No global infeasibility, quality or speed claim follows. Production, budgets,
repair cap, material limits and the preview remain unchanged; completion is 60%.

**N4 actual-outline construction, 2026-10-18:** [the retained beam and backfill](../benchmarks/results/h5-outline-construction-20261018.md)
test actual filled outer contours. All 159,819 beam additions replay; both panel
diagnostic timeouts remain explicit. Backfill adds 74 parts without moving existing
poses. The closest case places 63/66 parts, missing three cogs; every case remains
incomplete. Eight original public checks reject exactly the missing quantities.
The audit's null-metrics handling failure is preserved and repaired without new
packing searches. Next investigate collective repair of these saved partials,
first accounting for the native conversion guard, rather than treating physical
clearance as proof of zero native proxy loss. No runtime, gate limit or release
change; H2/H5 remain open at 60%.

**N4 saved-partial joint repair, 2026-10-18:** [four bounded native attempts](../benchmarks/results/h5-pattern-joint-diagnosis-20261018.md)
restore every missing original copy in explicit overlapping proposals; all original
partial poses remain exact. All four existing helper calls expire under seed 0
and their original 12-work-second diagnostic allowance, producing no complete
target layout. Every physically legal partial part already has positive native
collision loss. Next inspect exact native polygons and collision partners before
attributing this solely to conversion margins or designing another construction.
Rankings of all 308,326 recorded scores are checked; independent geometry checks
cover 32,527 original pairs and 5,395 selected-insertion comparisons. Input/build/audit harness failures remain
preserved; no native repair or quality run was repeated. Runtime, guard, budgets,
thresholds and release assets are unchanged; H2/H5 remain open at 60%.

**N4 native-margin diagnosis, 2026-10-18:** [exact native polygons and tracker entries](../benchmarks/results/h5-native-collision-diagnosis-20261018.md)
agree on all 51,175 checked pairs. The saved physical gaps are too tight for the
unchanged native inflation/edge margins. Translations below 0.18 mm produce four
partials with exactly zero native loss on each sheet and the joined strip; all
original sizes, rotations, assignments and stock targets remain. The extra
0.001 mm construction cushion still misses its declared limit and is preserved
as failed. Original public checks reject only the unchanged missing quantities;
13,566 additional filled-outer pairs pass. Restoring the same missing poses still
expires all four original-budget repair calls. Next observe the retained best
snapshot on expiry for the closest case, without accepting it or changing limits.
The f32 audit correction, original linearization failure and all failed repairs
remain preserved. Runtime/release assets stay unchanged; H2/H5 remain open at 60%.

**N4 terminal repair diagnosis, 2026-10-18:** [one fixed observational replay](../benchmarks/results/h5-terminal-repair-diagnosis-20261018.md)
reproduces the previous failure's exact work, statistics and expiry. The retained
best state reduces physical overlap 78.8441%, but has ten pair overlaps and one cog
47.7152 mm outside stock. All residual overlaps involve cogs; all 15 cogs move and
no frame moves. Original identities/quantities, budgets and rejection remain.
All 380 sampled fixed-neighbour cog free regions are empty. A collective local
linear step also fails actual geometry at all five tested fractions and accepts
no move. Independent original-shape checks cover 2,953 terminal-state pairs plus
7,485 collective-trial pairs; the original CLI rejects both terminal states and
the full collective proposal. Preserve these restricted failures, then investigate
joint selection of compatible actual-outline placements and alternative frame
allocations before another runtime proposal. All six prior main `cb5e23c` hosted
checks pass. Runtime, release assets and accurate READMEs remain unchanged;
H2/H5 stay open at 60%.

**N4 joint saved-placement selection, 2026-10-18:** [a finite binary construction](../benchmarks/results/h5-saved-placement-selection-20261018.md)
selects among 2,614 original-outline poses, including all 25 prior frame
configurations. The known 63-part partial certifies model feasibility; all frame
locations are selectable. The 120-second solve ends at its limit with a different
63-part arrangement, still missing three cogs. An independent reconstruction
enumerates 2,700,951 candidate pairs and verifies the exact 332,265-edge conflict
graph; all 1,303 selected-part pairs pass, and the original CLI rejects only the
missing quantity. The solver's finite-pool bound is recorded without a global
infeasibility claim. Preserve the timeout and generate new contact positions
before any further selection attempt; no unchanged-pool or native search repeat.
Production, targets, limits, release assets and accurate READMEs stay unchanged;
H2/H5 remain open at 60%.

**N4 expanded contact selection, 2026-10-18:** [8,798 verified poses](../benchmarks/results/h5-contact-selection-20261018.md)
include 3,600 new outline contacts and sheet half-turns. Independent enumeration
of 29,902,803 pairs reproduces all 2,517,051 conflicts and verifies the equivalent
17,097-clique model. Three bounded MILP mechanism attempts preserve their timeouts
and the same 63-part partial. Disabling expensive presolve reaches the first
relaxation quickly but gives no better layout. Exact-inventory CP-SAT requires all
66 parts; its initial runtime crash and failing tiny probe are retained. Standard
CPython, with the same package versions, passes the probe and solves the identical
model bytes to UNKNOWN at 120 seconds, returning no complete layout. Independent
model parsing verifies every exact quantity and nonbinding hint. Next investigate
coordinated multi-cog components from actual contacts, retaining full original-job
validation before any feasibility claim. All six prior main `5743a32` checks pass.
No native quality run, runtime, gate, release or README change; H2/H5 remain at 60%.

**N4 coherent cog groups, 2026-10-18:** [162 alternating lattices](../benchmarks/results/h5-cog-lattices-20261018.md)
produce 1,134 verified components and pass 45,360 independent pair checks.
All 504,000 fixed-column whole-job constructions finish without a full layout;
the greatest filled-area result is 52/66, missing fourteen inserts. Eight distinct
outline-gap continuations add fifteen parts total but remain partial; all 144
proposed additions and 10,915 final pairs independently check, with original CLI
quantity failures only. A separate exact-inventory rectangle model frees all
frame positions and chooses one of five full cog decompositions. Independent
parsing verifies all 471 variables and 517 constraints. The one 120-second search
ends UNKNOWN, not infeasible, without a full selection. The earlier 63/66 partial
remains better. Next investigate ragged staggered cog rows with actual contact
pitches; preserve all quantities, stock targets and full-layout validation.
No native packing, quality run, production, gate, release or README change;
H2/H5 remain open at 60%.

**N4 ragged cog pockets, 2026-10-18:** [54 staggered variants](../benchmarks/results/h5-ragged-pockets-20261018.md)
produce 324 valid groups with 20,034 independently checked pairs. Filling their
actual inter-part pockets produces 48 verified components: 1,197 proposed
additions, 6,301 final pairs and 237 accepted additions across variants. Four
complete original-inventory recipes pass their restricted rectangle-area test;
two area failures remain preserved. Three serial 120-second models test free
rectangle placement, proven full-width separator symmetry, and normal subset-sum
coordinates. Independent parsing verifies exact quantities, targets and every
model difference; independent enumeration verifies all reduced coordinate domains.
All three return UNKNOWN without a full selection. The earlier 63/66 partial is
not improved. Next inspect the documented cumulative/area propagation flags with
one controlled same-model experiment, preserving all limits and failures. All six
main 67e77b1 checks pass. No native packing, quality run, production integration,
gate credit, release or README change; H2/H5 remain open at 60%.

**N4 contact direction and outline construction, 2026-10-18:** [actual-outline investigations](../benchmarks/results/h5-outline-contact-direction-20261018.md)
retain the unchanged-model propagation timeout and all unsuccessful fixed/adaptive
constructions. Caching exact primitive exclusions lets all eighteen fixed-order
searches finish their original allowances; cached primitives and translation terms
audit exactly. Retained-layout checks cover 30,621 pairs; all best layouts remain
incomplete. The empty-sheet audit failure and corrected unknown return-code
metadata are preserved. A directed-contact probe exposes a better global rotation.
The subsequent declared 36-phase scan gives 324 verified components and 13,860
pair checks at minimum 0.225123442 mm. Its 15-cog rectangle is 5.6804% smaller than
the earlier sampled-angle component; this is not whole-job material savings.
Next use contact-aligned staggered rows and the retained bracket-pattern aspect
choices in a complete original-inventory construction. No native packing, quality
run, runtime integration, release, README change or gate credit; H2/H5 remain 60%.

**N4 aligned pockets and frame rows, 2026-10-18:** [verified contact-aligned components](../benchmarks/results/h5-aligned-pockets-and-rows-20261018.md)
include a fifteen-cog group with three inserts, preserving every original outline
and all group bounds. Checks cover 224 filled alternatives, 5,511 proposed
additions and 29,724 component pairs. The independent-bracket-aspect model remains
UNKNOWN. Column and row constructions retain 2,711,981 attempted arrangements;
the row cap leaves 60,583 unattempted. Twenty-four outline continuations preserve
27,954 checked pairs, but all remain incomplete. The best new 58-part layout lacks
eight inserts and still has less filled area than the earlier 63-part partial.
A diagnostic census supplies 261 new geometric signatures for the next exact-count
placement-selection pool; original coordinates remain untouched. All six f825cab
checks pass, and c9b0176 is pushed to main. Original failures, native-margin caveats
and all gate limits remain; no runtime/release/README change or gate credit. 60%.

**N4 coordinated contact selection, 2026-10-20:** [the completed model audit](../benchmarks/results/h5-coordinated-contact-selection-20261020.md) preserves three earlier bounded selections and
adds 2,260 exact cog-contact poses. Independent checks reproduce 774,312 new
conflicts over 10,571,998 added same-sheet pairs and verify all 24,750 model
constraints. The changed 120-second construction returns the identical 58-part
partial, missing eight inserts; its original CLI rejection and measured
121.154159-second elapsed time remain. The insert bound stays 21, so no full
layout or impossibility is proved. Next inspect necessary local area capacities
before another changed-model attempt; do not repeat these models or extend
their limits. All six c9b0176 checks pass and c824e5a is pushed to main.
No runtime, native-quality, release, README or gate change. H2/H5 remain at 60%.

**N4 local-area bounds, 2026-10-20:** [58 necessary stock capacities](../benchmarks/results/h5-area-capacity-relaxations-20261020.md)
pass exact rational checks on 75,957 positive coefficients, preserving the
complete 58-part hint. All six continuous relaxations finish within their declared
limits; the four cases fixing each cog arrangement remain fractional. Exact
independent dual reconstruction keeps the insert bound at 21 in every case,
with only the original quantity cap active. No full layout or impossibility
is established and no integer search is repeated. The original preparation
syntax failure is retained. Next investigate a bounded whole-placement
construction guided by these fractions, retaining every branch and the original
acceptance rules. Remote landing pages and READMEs are reconciled exactly and
pushed as 8a81205; the hosted main preview is verified. H2/H5 remain open at 60%.

**N4 whole-group diagnosis, 2026-10-20:** [bounded branching and fixed-group completion](../benchmarks/results/h5-whole-group-diagnosis-20261020.md)
retain all 421 LP branches, 227 checked fractional solutions and 41 unvisited
frontier entries. No branch completes 18 frames. A separate census finds 26
retained complete frame sets, of which only six combinations with the four cog
sets are compatible. Six independently reconstructed fixed-group models solve
in under 0.6 seconds each, with solver-reported maxima of 12, 12, 10, 11, 13 and
13 inserts. All 21 returned partial layouts pass original geometry checks and
fail the frozen CLI only for missing inserts. No improvement, full-layout credit
or unrestricted impossibility claim. Original environment/auditor failures are
preserved and no solver run is repeated. Next investigate new complete frame
arrangements while relaxing only the smaller-part choices, explicitly excluding
the 26 reviewed exact frame sets before bounded completion checks. H2/H5 remain
open at 60%; runtime and README contents are unchanged.

**N4 frame/bracket capacity, 2026-10-20:** [four new frame constructions and exact bracket bounds](../benchmarks/results/h5-frame-bracket-diagnosis-20261020.md)
follow four preserved 30-second mixed-model timeouts. A changed frame-only
heuristic finds four new final frame sets; all 19 returned frame/cog proposals
pass original geometry checks. Four independently reconstructed completion
models reject these sets without a layout. Removing inserts and reconstructing
exact rational dual bounds proves that their surviving finite poses allow at
most 7, 7, 10 and 10 brackets, below the required 12. This does not prove the
unrestricted job impossible. Individual pose availability is insufficient;
next select all 18 frames and 12 brackets together before exact insert
completion. No expired model is extended, no quality run occurs and no gate
changes. H2/H5 remain open at 60%; runtime and README contents are unchanged.

**N4 certified reduction and starting layouts, 2026-10-20:** [joint construction and safe pose substitution](../benchmarks/results/h5-dominated-poses-and-seeds-20261020.md)
preserve eight bounded searches without incumbents. Independent set checks
verify 4,105 same-family substitutions across four cases, preserving future
insert compatibility and frame exclusions while removing 26–30% of joint
variables. Direct substitution of known partials produces six valid partials
using three distinct new exact frame sets. Their bounded insert completions retain 12, 12, 10, 11, 13 and 13
inserts; all twelve original CLI checks fail only the required insert quantity.
Exact checks across 57,374 constraints establish complete feasible starting
hints for all four reduced joint models. Next optimize actual whole-insert
count with these hints, retaining all conflicts and original acceptance rules.
No full layout or improvement is claimed; H2/H5 remain open at 60%.

**N4 seeded search and local-move bounds, 2026-10-20:** [the complete audit](../benchmarks/results/h5-seeded-search-and-move-bounds-20261020.md)
preserves four seeded fixed-cog searches and one search with all cog positions
movable; none improves its 12/13-insert starting count. Independent checks verify
2247 safe pose substitutions and all returned geometry. Exhaustive enumeration
and clique certificates prove that all 331 zero/one/two-core moves about the
mapped seed allow at most 13 inserts within the retained finite pool. A changed
three-to-six-move search for at least 14 inserts times out without a candidate;
larger moves and new continuous positions remain unresolved. Next diagnose
compatible insert sets and their exact core blockers before generating changed
contact positions. No unchanged search is repeated and no full-job credit is
awarded. Prior local 6cde1bd and 56f818a are pushed to main; all six f6edfb7
checks pass. The README accurately describes the existing preview. H2/H5
remain open at 60%; runtime and release assets are unchanged.

**N4 complete-insert blockers and new frame contacts, 2026-10-20:** [the full audit](../benchmarks/results/h5-insert-blockers-and-frame-contacts-20261020.md)
verifies a 21-insert diagnostic after temporarily removing two frames. Exact
clique certificates over all 1036 zero/one/two-core deletions prove that at
least two saved core poses must be removed within this insert pool; they do
not independently prove the secondary area tie. The 64-part diagnostic packs
less filled area than the known 58-part partial and receives no improvement
credit. Two bounded completion searches, the second adding 240 new exact frame
contacts and restoring original core choices, both retain only 16 frames.
Independent geometry verifies all ten returned layouts, 179,683 new conflicts
and complete clique coverage. Both original missing frames remain required.
Next check frame-only capacity before selecting a different insert arrangement
or diagnosing bracket/cog obstructions. All six 56f818a hosted checks pass and
f321537 is pushed to main. H2/H5 remain open at 60%; runtime, README and release
assets are unchanged.

**N4 frame capacity and joint small parts, 2026-10-20:** [the complete audit](../benchmarks/results/h5-frame-capacity-and-joint-small-parts-20261020.md)
finds two geometry-verified 18-frame arrangements around all 21 inserts. Their
fixed-group small-part optima are 16 and 13; independent clique certificates
allow at most 8 and 6 cogs, below the required 15. A changed joint model keeps
all 18 frames and increases its own seed from 16 to 21 small parts, ending with
all 12 brackets and 9 cogs after one 30-second limit. All 18 returned layouts
pass original geometry and retain their quantity-only CLI failures. Six cogs
are still missing, and filled area remains below the known 58-part partial.
Next construct new cog contacts around the final 51 non-cog poses; do not
repeat expired searches. Remote abeb2739's comparison page and README link
merge cleanly as 09f59894, preserving 11 incoming and 25 local files. Its push
cancelled f321537's remaining Windows/Linux checks. No complete CI success
or release is inferred. H2/H5 remain open at 60%; core source is unchanged.

**N4 cog free regions and continuous capacity, 2026-10-20:** [the independently audited certificate](../benchmarks/results/h5-cog-free-regions-and-continuous-capacity-20261020.md)
proves at most **13 cogs** fit around the current 51 fixed non-cog poses,
even allowing arbitrary angles and continuous positions. The original job
requires 15, so at least one frame, bracket or insert must move. Earlier
finite sampling adds 437 cog poses but still selects nine; both returned
layouts pass original geometry and retain their six-missing-cog CLI failures.
The weaker finite cover of 14, continuous box bound of 18 and band bound of 16
are preserved. Exact reachable-area checks allow 10 cogs on the first sheet;
an independently verified diameter cover allows 3 on the last. This is a
conditional upper bound, not an attainable 13-cog layout or a claim after other parts move.
Next audit which single non-cog releases can remove this obstruction;
do not repeat the ruled-out cog-only search. Core source and all three README
hashes remain unchanged. No native quality run or new release is qualified.
H2/H5 remain open at 60% under the original requirements.

**N4 single non-cog release census, 2026-10-20:** [all 51 independently audited cases](../benchmarks/results/h5-single-non-cog-release-census-20261020.md)
rule out completing the current arrangement by moving only one bracket or
insert: all 12 bracket and 21 insert choices have cog capacity below the
required 15, even when the removed part is omitted entirely. All 121 center
components and 242 diameter covers verify. A separate component certificate
tightens the last insert case from 15 to 14; its original loose result remains.
The 18 frame releases remain inconclusive at bounds of 15–17, with no new
layout or feasibility claim. Next analyze changed frame positions while
preserving the other 50 non-cog poses; multiple-part changes remain possible.
All six hosted checks on remote abeb2739 now pass. Core source, README and
release assets are unchanged; no native quality or held-out run occurs.
H2/H5 remain open at 60%.

**N4 continuous single-frame regions, 2026-10-20:** [the complete audited record](../benchmarks/results/h5-single-frame-continuous-regions-20261020.md)
covers all 72 frame/size-class/sheet queries and retains all 18 original frame
poses. Guaranteed occupied rectangles exclude 16 of 52 whole center regions.
A changed midpoint subdivision stops at its declared 120-second boundary
after 165 new cases, preserving 49 pending nodes. Independent exact geometry,
area and tree-coverage checks rule out ten of the eighteen single-frame moves.
Together with the previous small-part certificates, 43 single non-cog changes
are excluded and eight frame choices remain unresolved. No unfinished tree
is treated as a proof. Next construct and audit changed frame/cog candidates
within the remaining regions; do not extend the expired tree unchanged.
Core source, README and releases remain unchanged. H2/H5 remain open at 60%.

**N4 joint frame/cog constructions, 2026-10-20:** [all eight changed models and audits](../benchmarks/results/h5-joint-frame-cog-construction-20261020.md)
combine one movable frame with free cog choices around the other 50 fixed
non-cog poses. The 80 queries add 853 frame and 641 cog poses across the conditional
sets; every proposal, filter and relevant pair conflict is independently checked.
All eight finite-pool models report an optimum of nine cogs, without hitting
their 20-second limits. All 16 returned layouts pass original geometry and
retain the six-missing-cog CLI failure; 12 CLI calls are fresh and four exact
results are reused. No partial improves and no unrestricted impossibility is
claimed. Next investigate coordinated whole groups with all small-part families
free, after reviewing prior frame-group results; do not repeat these models.
Core source, README and releases remain unchanged. H2/H5 stay open at 60%.


**N4 joint frame-group selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-group-choice-20261023.md)
chooses among 26 complete frame groups while all bracket, cog and insert poses
remain free. A recomputed 5,302-pose graph and complete model pass independent
checks. One 60-second search returns a 62-part partial: all 18 frames and 12
brackets, 13 cogs and 19 inserts. Filled area reaches 4,342,015.346194 mm² within
the original material allowance, but two cogs and two inserts remain missing.
All four returned layouts pass original geometry and retain quantity-only CLI
failures. The final bound is unresolved; no optimum or full-job pass is claimed.
Next diagnose free regions and construct changed contacts, preserving the new
seed; do not repeat the expired model. Incoming e9046d53’s comparison index and
both pending evidence commits are merged and pushed as 44ff9cc4. Its checks are
recorded separately. Core source and all three READMEs remain unchanged; the
published preview is still accurate and no new release is qualified. H2/H5
remain open at 60%, with original gates and held-out isolation preserved.


**N4 continuous capacity and cog/insert contacts, 2026-10-23:** [the complete audit](../benchmarks/results/h5-cog-insert-regions-20261023.md)
checks three continuous cog-capacity bounds (18, 22 and 35), all inconclusive.
Around the saved 30 frame/bracket poses, 12 queries add 196 cog and 72 insert
poses. All 259,549 conflicts, full clique coverage and the model pass independent
checks. One bounded solve reports a finite-pool optimum with the same 62 parts;
both returned layouts pass geometry and retain their two-cog/two-insert CLI
shortfalls. No filled-area improvement or unrestricted impossibility is claimed.
A distinct three-column/six-row group of all 18 wider frames and 11 optional
side-strip inserts passes 406 geometry pairs. Next complete its small families
with newly audited candidates and conflicts; do not retry the fixed-core model.
Core source, README and releases remain unchanged. H2/H5 stay open at 60%.


**N4 wider-frame small-part selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-wide-small-selection-20261023.md)
checks 10,066 poses and all 5,286,767 conflicts. Certified same-family substitutions
retain 7,776 choices; every dropped alternative preserves counts and filled area.
The insert cap, 834 pending lists, compression cap and reduction cap are preserved.
One bounded 60-second solve places 62/66 parts, missing four cogs; its filled area
is below the prior best. All nine hint/returned layouts pass geometry and retain
their original CLI quantity failures. No optimum or full witness is claimed.
A finite audit of saved denser cog groups finds 488 absent poses and verifies
135 placed subassemblies. Next combine those coordinates with new small-part
contacts under fresh declared limits; do not repeat the expired model. All six
44ff9cc4 hosted checks pass and the prior checkpoint is pushed as 37edb1d2.
Core source, accurate READMEs and releases remain unchanged. H2/H5 stay open at 60%.


**N4 denser-cog progress, 2026-10-23:** [the complete audit](../benchmarks/results/h5-dense-wide-progress-20261023.md)
improves the retained partial to 64/66 original parts, missing two cogs. Filled
area is 4,381,615.346194 mm², 39,600 mm² above the previous best, under the same
material target. All 750 new contact queries, 7,910,375 conflicts, fresh safe
substitutions and 3,000 group-based starting layouts are checked. One bounded
solve reaches 63 parts; a new gap query appends an insert without moving any
of them. All original geometry checks pass and the frozen CLI retains the two-cog
quantity failure. Native margins remain unqualified. The new fixed-non-cog
continuous capacity bound is 19 (18 first sheet, one last), inconclusive for 15.
Next construct and audit a changed cog-only pool against those exact 51 non-cogs;
do not retry the expired all-small model or capped lists. Original requirements,
source, accurate READMEs and release assets remain; H2/H5 stay open at 60%.


**N4 fixed-part cog limit, 2026-10-23:** [the complete audit](../benchmarks/results/h5-dense-cog-limit-20261023.md)
preserves the best 64/66 partial. Sixteen new queries and all compatible prior
poses give 2,846 cog choices. All 1,169,914 conflicts and model fields are checked;
one bounded solve proves a finite-pool optimum of 13 cogs with all 51 non-cogs
fixed. The two-cog CLI shortfall remains. No unrestricted impossibility is claimed.
An independent 165-case complete-cog census finds that these particular groups
require at least eight small-part moves. The selected checked 58-part subassembly
contains all frames/cogs and needs three brackets plus five inserts; it does not
improve the retained partial. Next test a newly bounded completion of those eight
parts, preserving original geometry, production repair limits and full H5 scope.
Prior checkpoints are pushed as 2333dd2c. Source, accurate READMEs and releases
remain unchanged; H2/H5 stay open at 60%.


**N4 complete-cog small-part relocation, 2026-10-23:** [the complete audit](../benchmarks/results/h5-complete-cog-small-relocation-20261023.md)
preserves the best 64/66 partial. Around the checked 58-part subassembly, all 20
new queries finish; 99 insert choices yield a finite optimum of three additional
inserts. A distinct model fixes only the 18 frames and all 15 cogs, freeing every
bracket and insert. Its 2,045 choices, 342,611 conflicts and full model pass
independent checks. One bounded solve retains 61 parts, missing three brackets
and two inserts. Its bound excludes the complete inventory in this finite pool;
no continuous impossibility or optimum is claimed. All returned original layouts
are audited and their quantity-only CLI failures retained. No pending list is
resumed and no solve repeated. Next compare other saved complete-cog arrangements
with small parts free, using fresh declared limits. Source, accurate READMEs and
releases remain unchanged; H2/H5 stay open at 60%.


**N4 complete-cog group choice, 2026-10-23:** [the complete audit](../benchmarks/results/h5-complete-cog-group-choice-20261023.md)
preserves the best 64/66 partial. All 1,670 newly declared group/contact queries
and 3,300 starting layouts complete. The 9,089 choices, 165 group decisions,
3,051,661 conflicts and full model pass independent checks. One bounded solve
reaches 63 parts, missing three brackets; its filled area remains below the
retained result and its bound is unresolved. All four original layouts pass
geometry and retain quantity-only CLI failures. The 980 capped lists remain
pending. A new 210-combination coverage audit identifies 200 additional complete
cog groups, including 12+3 and 10+5 distributions across sheets. Next test those
changed group choices under fresh limits; do not repeat the expired model.
All six prior-main checks pass and both saved checkpoints are pushed as 37b671d3.
Source, accurate READMEs and releases remain unchanged; H2/H5 stay open at 60%.


**N4 two-sheet cog progress, 2026-10-23:** [the complete audit](../benchmarks/results/h5-two-sheet-cog-progress-20261023.md)
improves retained filled area by 325.437876 mm² with a checked 63-part layout,
missing two brackets and one insert. The previous 64-part result remains the
highest-count partial. All 365 groups, 500 new contact queries, 6,603,323 conflicts,
fresh group-preserving substitutions and 7,300 starting layouts are checked.
One bounded solve and all four original layouts retain quantity-only failures;
the full-inventory bound remains unresolved. All 541,132 residual edges and 322
capped lists are preserved. Twenty new fixed-layout gap queries are empty under
positive padding. A separate 18-frame/15-cog subassembly in four tall columns
with 8+4+3 cogs passes original geometry and the expected CLI quantity failure.
Next complete its brackets/inserts under fresh limits; it is not a new best
partial or production repair. Source, accurate READMEs and releases remain
unchanged. H2/H5 stay open at 60%.


**N4 alternate-frame compound limits, 2026-10-23:** [the full audit](../benchmarks/results/h5-frame-compound-limits-20261023.md)
checks actual-outline bracket/insert compounds around the tall 8+4+3 and mixed
9+1+5 cog cores. Both fresh finite models reach optimal area below full inventory;
neither improves the saved 63-part area or 64-part count partials. All 616 queries,
3,337,889 conflicts, fresh reductions, model fields and 14 original layouts are
checked; only expected missing quantities fail. The original preflight reader
failure and 97 capped lists remain preserved. A new coverage audit retains every
earlier all-family choice plus 8,914 compatible additions around the 18 wide
frames. Next build its complete graph and select cogs/brackets/inserts together
under fresh limits, preserving both checked seeds. All six checks passed on
37b671d3, then queued checkpoints were pushed to main 4592d97c; its checks are
recorded separately. Source, accurate READMEs and releases remain unchanged.
H2/H5 stay open at 60%; no reserved files or production quality runs are used.


**N4 improved joint partial, 2026-10-23:** [the complete audit](../benchmarks/results/h5-latest-wide-joint-progress-20261023.md)
places all frames, cogs and inserts: 64/66 parts, lacking two brackets. Filled
area improves by 19,800 mm² over the previous best; all older partials remain.
The complete 21,468-choice graph, 20,223,984 conflicts, fresh substitutions,
1,877,444 retained residual edges and every model field are checked. One bounded
solve returns feasible; all five original layouts pass geometry with expected
quantity-only failures. Sixteen new fixed-layout bracket regions are empty under
positive padding. The next checked 33-part core has four changed cog poses and
preserves the new 64-part seed for fresh actual-compound bracket/insert contacts.
No previous solve, capped list or unchanged gap check is resumed. Main's current
checks remain separately recorded; queued commits await their successful finish.
Source, accurate READMEs and releases remain unchanged. H2/H5 stay open at 60%.


**N4 improved-core compound limits, 2026-10-23:** [the full audit](../benchmarks/results/h5-wide-core-compound-limits-20261023.md)
preserves the 64-part baseline through two newly bounded compound models. Both
reach a finite optimum with two brackets missing; no unrestricted impossibility
is claimed. All 536 queries, complete graphs, fresh reductions, model fields and
six original layouts are checked. The reflection census verifies 114 geometries
absent from previous queries; all 190 capped lists and 1,336,544 residual edges
remain preserved. A new 29-frame-group coverage audit checks every membership
and retains 29,631 compatible small poses plus the exact 64-part seed. Next build
its complete mutual graph and choose frames/cogs/brackets/inserts together under
fresh limits. Main's 7cd00432 checks remain separately recorded. Source, accurate
READMEs and releases remain unchanged; H2/H5 stay open at 60%.


**N4 expanded frame-group selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-expanded-frame-joint-20261023.md)
checks a fresh 29,631-pose graph with 33,489,837 conflicts across all 29
whole frame groups. Group-preserving substitutions retain the 64-part baseline;
all residual edges and pending work remain. The first bounded solve returns
`UNKNOWN` during presolve. A changed exact implication encoding preserves
every edge, reduces constraints from 12,149,516 to
40,193, and returns `UNKNOWN`
during presolve. A fresh, cheaper clique cover retains all edges, reduces
residuals to 5,257,882, and its separately bounded changed
model returns `UNKNOWN`. Every original layout is audited;
an independently verified no-presolve strategy then reaches search on the
byte-identical model and returns `FEASIBLE`.
No full 66-copy witness is found. A separate coverage audit exposes 2,358
additional individual frame poses and 3,358
additional small poses by removing the whole-frame-group restriction. The next
model needs a fresh complete four-family graph. Previous checkpoint 955cc87e is
pushed after all six 7cd00432 checks pass. Product source, accurate READMEs and
releases remain unchanged; H2/H5 stay open at 60%.


**N4 individual-frame joint selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-individual-frame-joint-20261023.md)
frees every original frame pose and all three small families across the full
35,488-pose pool. All 38,969,399 new four-family conflicts, original
transforms/stock bounds and both 64-part seeds are independently checked.
Fresh substitutions and first-fit constraints preserve every induced edge;
all model and parameter fields are verified. One unchanged-allowance solve
returns `FEASIBLE`. Best checked inventory: 64/66;
missing {"bracket": 2}. Native and complete H5
qualification remain open. All 16 conservative bracket insertion regions for
the distinct final layout are empty. Thirty fresh repair cores, each freeing
one cog plus all brackets and inserts, preserve both 64-part layouts and all
989,670 independently checked memberships; their conditional selection is
pending. The earlier 752b1c60 checkpoint is pushed after
all six 955cc87e checks pass. Source, accurate READMEs and releases remain
unchanged; H2/H5 stay open at 60%.


**N4 one-cog repair selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-one-cog-release-joint-20261023.md)
selects one of 30 checked 18-frame/14-cog cores and jointly relocates a cog,
all brackets and all inserts. Every original conflict, core membership,
substitution, model field and parameter is verified. Fresh reduction completes
at 6,641 variable poses; complete first-fit compression preserves all 4,686,314
reduced conflicts with no residual edges. One 60-second solve reaches search
and returns `FEASIBLE`; all three original layouts remain 64/66, missing two
brackets. The full bound is unresolved. No native or production qualification
is inferred. Main 752b1c60 awaits its last Windows check, with d49d0ff6 committed
locally. Source, READMEs and releases remain unchanged; H2/H5 stay open at 60%.


**N4 continuous cog contacts, 2026-10-23:** [the complete audit](../benchmarks/results/h5-one-cog-continuous-regions-20261023.md)
preserves a failed mitre-buffer equivalence check and a failed round-buffer
alternative, then verifies an explicit circumscribed 128-gon clearance helper.
All 120 new one-cog region queries complete; 4,000 new poses pass original
geometry and all 120,000 memberships across 30 fixed cores. There are 3,971
new centers beyond 0.05 mm and 2,075 poses opening old bracket choices, which
are candidate diagnostics rather than additional placed parts. All 60 capped
proposal lists remain recorded. The 20,058-choice joint graph and selection
are pending; best checked inventory remains 64/66. Both queued checkpoints
are pushed to main facf0f38 after all six 752b1c60 checks pass. Source, READMEs,
releases and gate requirements are unchanged; H2/H5 stay open at 60%.


**N4 continuous-cog joint selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-continuous-cog-joint-20261023.md)
checks all 20,058 choices, 6,917,176 new geometric conflicts and a separately
justified count-derived cog clique. Fresh substitutions retain 6,808 choices,
including 197 new cogs, with all 30 baselines preserved. Complete compression
and every model/parameter field verify. One bounded solve reaches active
search and returns `FEASIBLE`; all three original layouts remain 64/66,
missing two brackets, with the full bound unresolved. Five new 33-part cores
are checked for a fresh bracket/insert contact investigation; their old
candidate-count rankings are not inventory gains. Main facf0f38 checks are
pending and 5e88ac91 is committed locally. Source, READMEs, releases and gate
requirements remain unchanged; H2/H5 stay open at 60%.


**N4 changed-core small-part selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-shifted-core-small-joint-20261023.md)
checks 4,000 fresh small-part poses across seven fixed cores, all 211,995
memberships and a new complete 19,719,151-conflict graph. Certified reduction
retains 4,739 choices, including 1,246 new poses; every constraint and model
field verifies. One bounded solve finds a different 63/66 layout: 11 brackets,
19 inserts, all 18 frames and 15 cogs. It fills 400 mm² more but misses one
bracket and two inserts. Both original 64-part baselines remain preserved.
All four original layout audits pass geometry and fail only original missing
quantities. Forty fresh padded insertion regions are empty, without an
impossibility claim; coordinated small-part moves are the next investigation.
All 1,950 capped member lists and the unresolved full bound remain preserved.
Main facf0f38 passes all six checks, and checkpoints 5e88ac91/0526421e are pushed.
Source, READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 pair-contact selection and repository refresh, 2026-10-25:** [the complete audit](../benchmarks/results/h5-small-pair-joint-20261025.md)
checks 60 paired-release neighborhoods, 600 regions and 3,435 new small-part
positions. All memberships and the complete 28,976,111-conflict graph verify.
Certified reduction preserves both 64-part and both 63-part baselines. One
bounded search returns the same 63-part area result, missing one bracket and
two inserts; all three original layout checks fail only on quantities. The
full bound remains unresolved and all 27 deferred insert lists remain saved.
The next investigation is a continuous occupied-area relaxation for the seven
fixed cores, with conservative coverage checks before any negative conclusion.
Merge 55835d7c preserves the nine incoming Inkbolt example/website files and
all 37 local checkpoint files byte for byte, and is pushed to main. Main
4045822e passed all six checks and Pages; the refreshed upstream stop rule
does not fire. Engine source, READMEs and releases remain unchanged; H2/H5 stay open
at 60% completed milestone weight.


**N4 continuous occupied-area audit, 2026-10-25:** [the independent audit](../benchmarks/results/h5-occupied-area-relaxation-20261025.md)
checks all 168 queries, twelve permitted orientation/reflection classes and
seven fixed arrangements. All 99,983 known compatible polygon/translation
memberships and four prior baselines are covered. Every combined and family
area upper bound exceeds the required inventory; no core is excluded and no
packing feasibility is established. A failed round-offset assertion and its
repaired subset check are preserved without regenerating geometry. A separate
source-derived distance census finds only core 0 meets both conservative pair
and stock screens; actual native qualification remains required. Next build
an exact-count direct-coordinate model for its 12 brackets and 21 inserts,
with independently checked inward rounding, original outlines and new declared
limits. No solver retry, native packing, quality run or held-out evaluation
occurs. Engine source, accurate READMEs and releases remain unchanged; H2/H5
remain open at 60% completed milestone weight.


**N4 direct-coordinate domain preparation, 2026-10-25:** [the original-geometry and rational audit](../benchmarks/results/h5-direct-coordinate-domains-20261025.md)
checks all 20 orientation/sheet regions around fixed core 0, representing all
twelve permitted orientation/reflection cases. New placements retain 0.22 mm
separation and 0.02 mm extra stock margin. Every inward-rounded halfspace and
all 3,884 source faces verify. Certified consolidation retains 3,703 nonempty
grid domains, including all source-face lineages, with 55,992 per-copy choices
for the full 12 brackets and 21 inserts. No solver has run and no complete
layout is claimed. Next encode and independently check the exact-count model,
using only certified containment removal if needed before its one declared
60-second solve. Both prior checkpoints are pushed as 8f941426; its CI is
pending and the older main run is cancelled. Engine source, accurate READMEs
and releases are unchanged. H2/H5 stay open at 60% completed milestone weight.


**N4 exact-count coordinate result, 2026-10-25:** [the complete model audit](../benchmarks/results/h5-direct-coordinate-selection-20261025.md)
certifies 26 domain-containment removals and preserves all 3,677 retained
domains. Every field of the 60,537-variable/306,319-constraint model verifies,
including exact original quantities and all 978 cross-part arm pairs. One
declared 60-second search reports INFEASIBLE for the restricted grid/domain
model with fixed core 0, finishing at 59.73 seconds with 60.354444 seconds
actual elapsed time. No layout is returned and no solve is repeated. This
does not prove the unrestricted continuous problem impossible or that the
fixed core must move. Next verify an outer coordinate relaxation covering
all original continuous placements before drawing any conditional negative
conclusion. Engine source, accurate READMEs and releases remain unchanged;
H2/H5 stay open at 60%, with all original counts and acceptance limits retained.


**N4 continuous-coverage outer result, 2026-10-25:** [the complete audit](../benchmarks/results/h5-outer-coordinate-relaxation-20261025.md)
checks 24 source regions, all twelve permitted orientation/reflection cases,
953 outward domains and all 14,734 known compatible core-0 poses. Exact rational
containment and rounding cover the full source regions, not just saved samples.
Every field of the 22,290-variable/128,377-constraint exact-count model verifies.
One bounded outer search reports INFEASIBLE in 13.950743 seconds. Within the
recorded geometry/coverage model this excludes the full inventory with core 0
unchanged; it does not exclude different frame/cog arrangements. A single
projected cog in saved core 5 yields a new arrangement passing all 438 original
pair and 132 stock-boundary screens, with the other 32 placements unchanged.
Next check its complete outer regions and exact-count feasibility before any
accepted-layout claim. Actual native qualification and all H5 requirements
remain. Source, accurate READMEs and releases are unchanged; H2/H5 stay open
at 60% completed milestone weight.


**N4 guarded alternative and unrestricted relaxation, 2026-10-25:**
[The evidence](../benchmarks/results/h5-guarded-core-and-global-relaxation-20261025.md) rebuilds and audits all 24
continuous regions around the guarded core-5 alternative: 864 outward domains,
18,724 coverage vertices and all 12,860 compatible saved small-part poses.
Its independently checked exact-count model reports INFEASIBLE in 9.923168
seconds, conditionally excluding that fixed arrangement. A new necessary
relaxation lets all 66 parts move and represents each freely rotating cog by
a polygon strictly inside its certified 109.1157 mm inscribed disk. Original
non-cog components, orientations, counts and target sheet domains remain.
Independent geometry and complete 31,467-variable/37,061-constraint encoding
audits pass. One 60-second call returns UNKNOWN in 60.152007 seconds with no
incumbent or proof; the preserved 64-part sanity check still lacks two brackets.
Both completed calls and the initial failed geometry preparation are retained.
Next investigate audited original-area bounds and global packing propagation;
do not retry unchanged calls or weaken acceptance. No full target witness,
native qualification, production-budget run or H5 matrix result is obtained.
Source, accurate READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 global packing propagation and compound proxies, 2026-10-25:**
[The evidence](../benchmarks/results/h5-global-propagation-and-compound-proxy-20261025.md) independently verifies original
filled-area bounds, outward sheet capacities and floor-safe inner rectangles
for every part. Adding two global NoOverlap2D and four cumulative constraints
to the all-movable polygon model yields 31,935 variables/37,849 constraints,
fully audited. One bounded call remains UNKNOWN in 60.188312 seconds. A distinct
smaller model replaces pairwise polygon disjunctions with five disjoint inner
rectangles per cog, preserving full original-area charges and all66 counts.
Its 1,806 variables/2,824 constraints also audit completely; one call remains
UNKNOWN in 60.176534 seconds. Neither search returns an incumbent or proof.
Both original64-part sanity checks pass the new conditions but still miss two
brackets. Next audit exact orientation aliases and source-derived, nonbinding
hints before considering a different bounded construction test. All original
limits, native checks and H5 matrix requirements remain. Source, accurate
READMEs and releases are unchanged; H2/H5 stay open at 60%.


**N4 exact orientation aliases and audited source hints, 2026-10-25:**
[The evidence](../benchmarks/results/h5-orientation-aliases-and-source-hints-20261025.md) checks exact representative and
inverse maps for all 28 original modes, retaining 22 representatives and all
16 original orientation/reflection classes. All bracket cases stay distinct.
The original 66-part layout passes 1,456 polygon-pair checks but exceeds the
target at the same seven recorded parts. Only 59 compatible poses supply
nonbinding hints; all 66 parts remain required and every position stays free.
Every field of the 1,686-variable/2,584-constraint model and all 1,482 hint values
verify independently. One bounded call returns UNKNOWN in 60.101281 seconds
without an incumbent or proof. A source census prepares a different finite
orientation-inventory construction, with two additional brackets mandatory;
no search of that inventory occurs yet. After all six previous main checks
passed, five checkpoints were pushed normally through 247e823a. Its new CI
40233299884 remains distinct from the completed previous run. Source, accurate
READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 source orientation inventory and exact proxy-slot coverage, 2026-10-25:**
[The evidence](../benchmarks/results/h5-source-inventory-and-proxy-slot-coverage-20261025.md) checks a finite source-derived
orientation inventory with all 66 parts mandatory and every position free.
Its 1,486-variable/2,178-constraint model and 1,406 nonbinding hint values audit
completely; one bounded call remains UNKNOWN in 60.111765 seconds. Separately,
all 16 missing-bracket mode domains around the fixed 64-part proxy layout are
covered exactly: 1,950 forbidden rectangles cover 266,545,630,376 integer
mode/anchor pairs, independently checked across 145,251 critical cells.
No extra bracket fits while those existing poses stay fixed, including at
touching boundaries. A complete single-part release census records all 64
parts and 33 frame/cog cases; released parts must be restored in any next
63-plus-3 construction. This is conditional evidence, not unrestricted
infeasibility or a full target witness. All original acceptance requirements
remain; source, accurate READMEs and releases are unchanged. H2/H5 stay open
at 60% completed milestone weight.


**N4 complete single-core relocation exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/h5-single-core-relocation-exclusion-20261025.md) covers all 33 recorded frame/cog
releases, with 63 source poses fixed and the released part plus two brackets
mandatory. All 576 queries and 3,462 integer free cells audit completely; 1,152
exact allocation inequalities exclude 28 cases. The other five cog cases have
an independently reconstructed 1,111-variable/2,118-constraint model, including
all 416 cell options and 120 component pairs. One bounded call returns
INFEASIBLE in 0.150878 seconds with no incumbent; no LRAT certificate is claimed.
All 66 original counts are retained. These 33 conditional neighborhoods are
closed; broader coordinated moves remain unresolved. No unrestricted
impossibility, target witness or H5 qualification is claimed. Source, accurate
READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 complete pair relocation census and outline diagnosis, 2026-10-25:**
[The evidence](../benchmarks/results/h5-pair-core-relocation-and-outline-diagnosis-20261025.md) completes all 528 core-pair
releases and 9,984 mode queries. Independent coverage and 53,424 allocation
inequalities exclude 299 cases; all 229 survivors and 424 allocations enter
one fully audited 73,266-variable/141,477-constraint model. One bounded call
finds a complete 66-part proxy arrangement in 7.952451 seconds. Independent
reconstruction verifies all copies, 138 inner rectangles and 6,456 component
pairs. The original-outline lift fails seven pair and two stock checks. Two
certified-disk conflicts remain after every cog angle and full floor-center
uncertainty, rejecting those selected coordinates. Broader cells and
neighborhoods remain unresolved. Next strengthen necessary collision geometry
against actual fixed original outlines; no unchanged retry or acceptance
reduction. Source, accurate READMEs and releases stay unchanged. No original
target witness or H5 qualification; H2/H5 remain open at 60%.


**N4 original-outline collision regions, 2026-10-25:**
[The evidence](../benchmarks/results/h5-original-outline-collision-regions-20261025.md) verifies a stronger floor-safe
16-gon for all cog angles against the actual fixed original outlines. Exact
subset checks and an independent triangle oracle verify all 100 obstacle caches;
all 43 source poses and 2,000 compatible pairs remain valid. A mixed-dimensional
GEOS guard failure is preserved; 1,262 completed queries are reused unchanged
and only 1,388 unfinished queries resume within the original work budget.
All 2,650 queries finish. Independent outward covers account for every whole
prior cell: 42,226 cells including 3,081 points/lines. They reject three prior
false anchors and exclude another 22 cases, leaving 207 cases/286 allocations.
Next construct fully covered convex domains and a joint model using the stronger
cog polygon itself. No solver call, accepted target layout or H5 qualification
is claimed. Source, accurate READMEs and releases stay unchanged; H2/H5 remain
open at 60% completed milestone weight.


**N4 stronger two-core relocation exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/h5-strong-pair-relocation-exclusion-20261025.md) covers all 207 remaining cases
and 286 allocations with 32,626 convex domains, 165,640 outward halfplanes and
960,962 exact vertex tests. The empty-set guard failure is preserved; 40 completed
queries are reused unchanged within the original work budget. An exact support
atlas audits 324 convex Minkowski hulls and every relevant edge normal. The full
56,046-variable/356,662-constraint model uses the stronger cog 16-gon directly.
One bounded call returns INFEASIBLE in 20.878256 seconds with no incumbent or
LRAT certificate. Together with prior 299 area and 22 empty-role exclusions,
all 528 recorded two-core neighborhoods are closed, conditionally on the source
poses/inventory. A distinct conflict-owner census prepares 57 fixed plus nine
mandatory movable originals, preserving all 66 parts. All six existing main
checks now pass; accumulated commits are ready for the next normal push.
No unrestricted impossibility, accepted target or H5 qualification is claimed.
Source, accurate READMEs and releases stay unchanged; H2/H5 remain open at 60%.


**N4 complete conflict-owner neighborhood, 2026-10-25:**
[The evidence](../benchmarks/results/h5-conflict-owner-neighborhood-20261025.md) restores seven originals and both missing brackets with
57 source transforms fixed, retaining all 66 required parts. All 20 original-stock
queries complete with 199 convex domains; independent checks cover 3,638 outward
halfplanes, 82,650 rational vertex tests and 361 component Minkowski hulls.
The fully audited 1,871-variable/10,774-constraint model finds a necessary-model
arrangement in 1.133719 seconds. Its original-outline trial fails 17 clearance
checks and three stock bounds; all failures are preserved. Exact 109.1 mm whole
circles reject five selected cog conflicts, and a separately certified 139.2707 mm
all-angle stock support rejects three anchors while retaining all 15 valid source
cog centers. The hull support is not used as filled collision geometry. These
conditions prepare the next stronger model; no completed call is retried.
The previous six checkpoints are on main 51fe56c0; its new CI remains separate
from the prior successful run. No accepted target, native qualification or H5
completion is claimed. Source, accurate READMEs and releases stay unchanged;
H2/H5 remain open at 60% completed milestone weight.


**N4 stronger circles and full-original construction, 2026-10-25:**
[The evidence](../benchmarks/results/h5-circle-stock-neighborhood-20261025.md) strengthens the same 57-fixed/nine-moving neighborhood
with a certified 128-vertex cog proxy, exact circle separation for all 15 cog
pairs and the all-angle stock bounds. All 20 queries complete; 18 are reused
unchanged. Independent checks cover 274 domains, 4,204 outward halfplanes,
85,992 rational vertex tests and 361 exact component Minkowski hulls.
The fully audited 9,549-variable/22,313-constraint model returns UNKNOWN in
60.174056 seconds, with no incumbent; the completed call stays closed.
A distinct full-original preparation retains every cog tooth at its known source
angle, all bracket choices and 20 inward stock-grid queries. Its 57 starting
originals meet the 0.2 mm requested clearance, but nine pairs and four stock
margins fall below the current native conservative guards. These shortfalls
must be addressed and independently checked before that source is frozen for
an original-outline construction. No guard, material cap or count is reduced.
No accepted target or H5 qualification is claimed. Source, accurate READMEs and
releases stay unchanged; H2/H5 remain open at 60% completed milestone weight.


**N4 corrected source guards and original-outline regions, 2026-10-25:**
[The evidence](../benchmarks/results/h5-guarded-source-adjustment-20261025.md) corrects all nine pair and four stock-margin shortfalls
without changing original shapes, counts, orientations, sheets or the material
target. One audited 228-variable/695-constraint bounded adjustment finishes in
0.027011 seconds. Fifteen originals move by at most 0.023 mm per axis. Independent
checks cover all 1,246 original pairs and 228 stock edges; the minimum gap is
0.2125 mm and extra stock margin 0.0125 mm, both above unchanged native guards.
The baseline still contains only 57 originals; all nine others remain mandatory.
All 100 full-original collision obstacles and 20 free-region queries are rebuilt
and independently checked using 11,872 raw triangle hulls and 2,491 expanded
triangle hulls. Every cog tooth is preserved, with no outward region padding.
Next is a joint full-original nine-part model using this adjusted source.
No complete target, native full-job validation or H5 qualification is claimed.
Source, accurate READMEs and releases stay unchanged; H2/H5 remain open at 60%.


**N4 complete original-shape joint searches, 2026-10-25:**
[The evidence](../benchmarks/results/h5-full-original-joint-20261025.md) audits all 20 actual-original placement regions, 82 mutual
collision cases, 3,525 raw allowed faces and 512 forbidden pieces. All nine
moving originals remain mandatory alongside the adjusted 57-part source.
The full-original joint model returns UNKNOWN in 60.875060 seconds; a smaller
conservative moving-cog-hull model is conditionally INFEASIBLE in 8.862555 seconds.
A distinct original-shape constraint-generation experiment shares 60 seconds
across construction, audits and eight calls, ending UNKNOWN in 60.102165 seconds.
All seven relaxed 66-original proposals are independently reconstructed: 11,191
pair checks and 1,848 stock-edge checks preserve every failure. Fixed clearances
and stock margins pass; none passes moving-part collisions. The best recorded
overlap diagnosis still has seven overlapping pairs, so no native call is made.
All bounded searches stay closed. Next investigate certified whole-domain pair
exclusions or a structurally larger neighborhood, without relaxing counts,
material limits, clearance guards or H5. Source, accurate READMEs and releases
are unchanged; H2/H5 remain open at 60%.


**N4 whole-domain conflicts and three-cog exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/h5-original-domain-conflicts-20261025.md) independently checks all 8,449,813 domain pairs and
5,453,534 original-shape collision exclusions. Lossless row grouping preserves
23,481,818 physical exclusions in 4,580 group constraints. A necessary-region
model finds a candidate in 8.094902 seconds; its complete original-coordinate
model is INFEASIBLE in 0.030771 seconds for that selected combination only.
The ordinary interval replay reaches a fixed point without proving a conflict.
A separate core diagnostic identifies three cog domains, then an independent
228-segment exact-rational no-fit disk certificate proves a broader three-region
exclusion. Groups containing 12/2/29 complete domains exclude 696 triples across
all six moving cogs, without changing any original count or material limit.
Next add that verified global occupancy clause before another declared search.
Four checkpoints are pushed normally to main 4f359ff7 after all six previous CI
jobs pass; new CI 40240715636 is tracked separately. No native acceptance,
quality run or new release is claimed. H2/H5 remain open at 60%.


**N4 complete convex conflicts and second-sheet capacity, 2026-10-25:**
[The evidence](../benchmarks/results/h5-convex-domain-conflicts-20261025.md) scans all 2,996,279 pairs left open by the box table and
independently verifies 108,041 additional whole-convex original-shape exclusions.
The complete table now has 5,561,575 exclusions, represented losslessly as
24,091,856 physical exclusions. A first three-region assignment is rejected by
a whole-convex bracket/cog collision. The refined master finds a necessary
assignment, but its full original-coordinate model is INFEASIBLE. Exact replay
then proves a second-sheet pair conflict independently of the solver core.
All 51 unresolved second-sheet pairs receive bounded exact interval checks:
32 conflicts are proved, 19 fixed points stay non-proofs, and all 1,920 events
are independently replayed. A separate original no-fit-disk argument proves
that at most two moving cogs fit the complete second-sheet region inventory.
The next master includes all 480 physical new pair clauses and this capacity;
its coordinate check still fails, having placed five cogs in one first-sheet
domain. Next derive independently certified regional occupancy limits across
all six copies. All original counts, material limits and native guards remain
unchanged; no complete target, native call, quality run or release is claimed.
Main CI40240715636 has 4/6 successful jobs and remains in_progress in the
saved snapshot. Accurate READMEs remain unchanged. H2/H5 remain open at 60%.


**N4 regional cog capacity and simultaneous anchors, 2026-10-25:**
[The evidence](../benchmarks/results/h5-cog-region-capacities-20261025.md) certifies 1,215 whole integer boxes and independently
checks every membership, cell diagonal and dominance witness. Thirty-five
retained bounds (30 capacity-one, five capacity-two) count all six cogs and
eliminate the prior five-in-one-region assignment. A first master/coordinate
pipeline finishes within 11.416324 seconds of a shared60-second allowance; its
selected original-coordinate model is INFEASIBLE. A second pipeline adds all
six simultaneous cog anchors and a certified strict inner32-gon of the original
collision disk, finishing in43.440899 seconds. Its necessary assignment still
has four actual original cog collisions, and the full selected-coordinate model
is INFEASIBLE. Next strengthen simultaneous geometry with the complete original
cog obstacle (61 pieces/2,720 edges), retaining all counts, guards and material
limits. Both bounded pipelines stay closed; no full target or native acceptance
is claimed. Main's new15-file scrap/offcut documentation change is merged as
da4ced0f, preserving all15 remote and73 local evidence files byte-exact. The older
CI was cancelled after five passes; new main CI40242602102 is independently
tracked. Production and accurate READMEs are unchanged. H2/H5 remain open at60%.


**N4 complete guarded cog model and original-outline core, 2026-10-25:**
[The evidence](../benchmarks/results/h5-full-cog-coordinates-20261025.md) independently reconstructs a52,790-variable/66,018-constraint
model with all original cog collision pieces and existing domain/occupancy limits.
Its single call returns UNKNOWN without an incumbent. Shared elapsed60.870843s
exceeds the declared60s by0.870843s; the solver soft-limit overshoot is also
preserved, with no budget-pass claim, retry or follow-up coordinate call.
All200,309 remaining cog-domain pairs receive complete guarded-region checks:
146 raw-table exclusions are independently verified;16 overlap earlier proofs,
so130 ordered pairs (1,950 physical clauses) are newly available to the master.
A separately prepared complete original-outline collision core has71 convex
pieces and352 necessarily rounded edges, reducing the direction upper bound
from39,540 to5,280 while retaining tooth geometry. Its full union, strict raw
containment and exact necessary rounding are independently audited. Next use
this smaller preliminary model with the new pair exclusions; every positive
still needs full guarded-original, native and H5 validation. Main CI40242602102
is independently tracked; source, accurate READMEs, releases and all acceptance
limits are unchanged. H2/H5 remain open at60%; no reserved vectors are evaluated.


**N4 original-core search and complete second-sheet cog pairs, 2026-10-25:**
[The evidence](../benchmarks/results/h5-original-core-search-20261025.md) preserves a full 18,530-variable / 34,068-constraint original-core
master UNKNOWN with no incumbent. Its single 45-second call takes 45.305899s;
the soft-limit overshoot is explicit, while shared 47.844358s stays within 60s.
No full-coordinate or native follow-up is opened. A separate bounded diagnostic
resolves all 15 remaining second-sheet pairs. Five have original-shape witnesses;
ten receive independent exact proofs covering 74 nodes / 540 events / 32 splits.
Together with prior certificates, all 1,024 pairs are classified:1,019 excluded,
five feasible. All 75 original pair and 40 stock-edge checks pass for those five
two-cog witnesses, but seven other moving originals are absent and still required.
The first geometry audit's metadata lookup failure is preserved alongside its
corrected read-back. The ten proofs provide 150 new physical pair clauses for
the next full 66-original search; verified coordinates may guide optional hints.
Production source, READMEs, material/native limits and releases are unchanged.
H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched. Main's own
CI40242602102 remains tracked before the next normal push.


**N4 guided full original-core search, 2026-10-25:** [the evidence](../benchmarks/results/h5-second-sheet-guided-search-20261025.md)
adds all 150 clauses from the ten proved second-sheet exclusions and 14 optional
values from a verified two-cog placement. The independent model audit covers
18,530 variables / 34,218 constraints, all hints and all 66 required originals;
no placement is fixed by a hint. The sole call finishes UNKNOWN without an
incumbent in 45.537740s; the 0.537740s soft-cap overshoot is preserved. Shared
47.986694s remains within 60s. No full-coordinate or native follow-up is opened.
Next investigate a different collision-free displacement-cell representation,
proving every retained cell safe against all original guarded inequalities
before use. That representation is not built yet. H2/H5 remain open at 60%;
production source, READMEs, releases, original counts, material target and guards
are unchanged. All 22 reserved H2 vectors remain untouched. Main CI40242602102
is still tracked before the next normal push.


**N4 exact guarded displacement cells, 2026-10-25:** [the evidence](../benchmarks/results/h5-cog-displacement-cells-20261025.md)
prepares 229 first-sheet and four second-sheet allowed relative-position cells.
It reconstructs all 122 bounded source-clause failure regions exactly, then
independently proves all 233 whole cells safe with 13,531 rational separating-axis
certificates and 831 inward halfplanes. All five known second-sheet witnesses
remain represented. The selected first-sheet simplification uses 0.005 mm
tolerance and 0.010 mm outward failure padding, an explicit stricter construction
restriction; negative results cannot exclude unrestricted packing. All nine
measured candidates, initial faces and discards remain preserved. At most 3,495
cell flags replace the earlier guarded model's 39,540 direction variables, but
no new solver model or runtime improvement is claimed yet. Next integrate these
proved cells with all 66 originals and unchanged material/native/H5 requirements.
Production source, READMEs and releases are unchanged. H2/H5 stay open at 60%;
all 22 reserved H2 vectors remain untouched. Main CI40242602102 is still tracked
before the next normal push.


**N4 guarded cell search and six-cog witness, 2026-10-25:** [the evidence](../benchmarks/results/h5-guarded-cell-search-20261025.md)
preserves a full 16,775-variable / 46,383-constraint guarded master UNKNOWN,
without an incumbent. Shared 48.579203s is within 60s; the 45-second soft-cap
overshoot is retained. A distinct four-cog first-sheet diagnostic succeeds in
7.753828s (shared 8.201210s), with every domain, bound, cell and full original
guarded clause independently verified. Combined with the known second-sheet
pair, all 63 currently placed originals pass 1,467 pair and 252 stock-edge checks.
Two brackets 28/29 and insert 50 are explicitly missing, so no full target/native
pass is claimed. A complete declared finite sample regenerates 162,863 points;
103,028 exact rejection certificates leave zero bracket and eight insert poses.
This does not prove continuous impossibility. Next keep all six cogs movable,
use their verified positions only as hints, and add 9,204 exact selected-domain
box bounds to the full model. All 66 parts, material/native limits and H5 gates
remain required. Production source, READMEs and releases are unchanged; H2/H5
remain open at 60%, with 22 reserved H2 vectors untouched. Main CI40242602102
is tracked before normal push.


**N4 guided search and exact selected-domain rejection, 2026-10-25:** [the evidence](../benchmarks/results/h5-six-cog-guided-search-20261025.md)
records a candidate from the 16,775-variable / 55,587-constraint master in
11.009201s after adding 9,204 exact domain bounds and 79 advisory hints. All 66
originals remain mandatory (nine movable, 57 fixed). The full selected-coordinate
follow-up is INFEASIBLE in 0.225323s; total pipeline time is 15.872994s within 60s.
Nineteen interval traces reach fixed points, not feasibility. A separate exact
clause tree then certifies this selected combination's rejection: 1,316 nodes,
415 complete branches, 901 contradictory leaves and 4,851 independently replayed
events, with no open leaves. Its 56.946915s proof budget is separate from the
closed solver pipeline. Other domain combinations and unrestricted packing
remain open. The early read-back failure and separate completed audit are
preserved. Next integrate the bracket/insert coordinates with the guarded cog
search using independently proved compact representations for the remaining
original profile pairs. No target/native or production pass is claimed. All
six jobs of main CI 40242602102 now pass; checkpoints can be pushed normally
after preserving any newer remote work. Production, READMEs and releases are
unchanged. H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched.


**N4 complete guarded coordinates and table projection, 2026-10-25:** [the evidence](../benchmarks/results/h5-all-original-cell-search-20261025.md)
adds all 162 remaining query-pair representations for 364 physical pair/mode
uses. Their 6,174 cells and 19,329 inward planes pass 38,211 exact separation
certificates; all 29 stricter simplifications and 11 inset/grid discards remain
explicit. The full 35,469-variable / 181,700-constraint model now includes all
nine moving originals and every one of their 36 direct guarded pair relations,
with all 66 original counts required. Its single 45-second-cap call returns
UNKNOWN in 52.627968s: the 7.627968s soft overrun is retained, while total
57.609353s stays inside the shared 60s budget. No layout/native pass is claimed.
A separately audited projection removes only the obsolete 1,572,932-literal
table and 3,395 private variables, preserving every direct geometry/count/area
constraint. All 32,074 remaining variables and 173,814 constraints inverse-map
exactly to the parent; actual solver import/export passes. That projection has
not been solved. Next use a distinct bounded call with a 10s shutdown reserve;
offline preparation is not production qualification. The prior ten checkpoints
are pushed to main 728b2db2; its own CI 40246226212 remains tracked before the
next normal push. Production, READMEs and releases are unchanged. H2/H5 remain
open at 60%, with all 22 reserved H2 vectors untouched.


**N4 direct-model negative and complete integer outer cover, 2026-10-26:** [the evidence](../benchmarks/results/h5-direct-original-search-20261025.md)
records the distinct 32,074-variable / 173,814-constraint full-coordinate model
INFEASIBLE in 42.634289s, shared 44.271944s, within its 45s cap and 60s budget
with a 10s shutdown reserve. This rejects only the fixed-57/source-angle/inward-
domain construction with stricter pair cells, not unrestricted packing. A new
necessary outer cover retains every integer displacement satisfying the original
guarded pair rules: all 164 cases / 394 physical uses, 16,210 complete slabs,
22,063 proved-invalid rectangles and 9,129 retained boxes. Independent rational
partition checks and 6,485,956 exact corner inequalities pass. Retained boxes
are not safe placements. No outer-cover model or solver has run; next replace
all stricter pair-cell constraints and audit the complete transformation before
a distinct bounded diagnostic. All originals, material/native limits and H5
production requirements remain unchanged. The provenance-lookup failure and
separate corrected audit are preserved. Main 728b2db2's own CI 40246226212 is
still tracked before pushing local checkpoints. Production, READMEs and releases
are unchanged; H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched.


**N4 complete source-clause search and rejected relaxation, 2026-10-26:** [the evidence](../benchmarks/results/h5-bounded-source-search-20261026.md)
verifies complete replacement of all strict safe cells, including 54 empty-cell
sums, by the necessary integer outer cover. Its sole call finds a candidate in
16.162402s, shared 18.195138s; independent full-source and 66-original geometry
readback rejects six moving-pair failures, including four overlaps. All 90
cutouts, original copies/areas, 1,540 same-sheet pairs and 264 stock edges are
checked. The initial false no-cutouts assertion and separate repair are retained.
A distinct complete source-clause model replaces all outer boxes, retains every
original domain/count/area/capacity rule and applies only exact rectangle-bound
simplifications. Its 167,044 variables/376,363 constraints and all 394 pair modes
pass independent reconstruction, 218,048 exact corner evaluations and actual
solver import/export. One 45s-cap call ends UNKNOWN in 45.471545s, shared 48.583887s;
the 0.471545s soft-cap overrun is preserved, the shared 60s budget holds, and no
feasibility/impossibility or native qualification is claimed. Both calls remain
closed. Next test whole-domain completion against the verified six-cog positions
with replayable exact certificates; the previous finite pose census is not a
continuous proof. Any exclusion must remain conditional on fixed witness poses.
H2/H5 stay open at 60%; production, READMEs, releases and 22 reserved H2 vectors
remain unchanged. Main 728b2db2's existing CI is allowed to finish before pushing.


**N4 exact completion obstruction and single-cog release census, 2026-10-26:** [the evidence](../benchmarks/results/h5-fixed-six-completion-20261026.md)
proves that the verified six fixed cog poses leave none of the 2,418 original
bracket domains continuously feasible; the insert retains one domain with 89
fragments. All 2,756 domains and 1,136 exact clipping events pass independent
replay, including boundaries and 5,816,904 integer corner checks. Six distinct
single-cog releases cover all 14,508 bracket domains in 13.630690s, with no
pending cases. Releasing cogs 54 or 62 leaves no bracket space. Releasing cog
58 opens individual regions, but all 196 exact ordered region-pair differences
are empty: at most one bracket fits, while two are required. Cogs 57, 64 and 65
remain the useful single-position releases to investigate in focused four-mover,
62-fixed-original models. All 66 parts and original/native/material requirements
remain mandatory. These are conditional source-pose/domain proofs, not general
packing impossibility or H5 qualification. No solver/native/quality call occurs.
The provenance lookup failure and zero-counter aggregation failure are preserved;
completed proof work is reused without reruns. Three prior checkpoints were
normally pushed to verified main 822a5f67 after all six prior CI jobs passed;
new CI 40248595273 is tracked. H2/H5 remain open at 60%; production, READMEs,
releases and all 22 reserved H2 vectors remain unchanged.


**N4 single-cog obstruction completed, 2026-10-26:** [the exact proof](../benchmarks/results/h5-single-cog-obstruction-20261026.md)
examines all 3,315 insert/released-cog domain cases for original cogs 57, 64
and 65 and independently excludes all 2,362 bracket/cog fragment pairs.
All boundaries and original source pair directions are retained. Combined
with the prior proofs for 54, 58 and 62, no single-cog-position change can
complete this layout within the recorded source angles/domains and fixed
57 poses. The empty focused models are not sent to a solver. Next widen to
at least two cog positions (five mandatory movers, 61 fixed originals), or
another fixed pose/orientation/domain inventory; never apply these conditional
exclusions when their fixed poses move. This is not unrestricted impossibility
or H5 qualification. No solver/native/quality call occurs. Full original/native
material evidence, production integration and the full matrix remain required.
H2/H5 remain open at 60%; original gate limits, production, READMEs, releases
and all 22 reserved H2 vectors remain unchanged. Main CI 40248595273 is tracked
before the next normal push.


**N4 two-cog focused source search, 2026-10-26:** [the retained result](../benchmarks/results/h5-two-cog-source-focus-20261026.md)
releases original cogs 64/65, preserving both brackets, insert and every original
part (five movers, 61 fixed). All 3,523 original domain cases finish exact clipping
and independent replay; 173 domains/261 fragments remain. Both brackets and
released cogs must use the second sheet in these source conditions. The full
parent model is preserved exactly, with eight fixed-coordinate equalities and
6,364 independently verified empty-domain exclusions appended. One bounded
call returns INFEASIBLE in 5.966434s, 9.166805s total; actual model/parameters and
terminal state pass readback. This conditional solver negative is not an
independent unrestricted geometry proof, and the call is closed. Next examine
first-sheet cogs 57/58 with new regions and correct pair ordering. No previous
conditional obstruction may be transferred. The pre-search prose-substitution
failure and recovery are preserved; no solver repeated. Production integration,
full original/native target and complete H5 matrix remain required. H2/H5 stay
open at 60%; original limits, production, READMEs, releases and 22 reserved H2
vectors are unchanged. Main CI 40248595273 is tracked before the next normal push.


**N4 first-sheet neighborhoods and area capacities, 2026-10-26:** [the evidence](../benchmarks/results/h5-first-sheet-cog-neighborhoods-20261026.md)
retains three distinct original-part searches: cogs 57/58 and 57/58/62 return
INFEASIBLE; all four first-sheet cogs return UNKNOWN. Every region and focused
model is independently audited, with all 66 originals retained. The UNKNOWN
call's 0.682462s soft-limit overrun is preserved; total time is 48.884638s within
the shared 60 seconds. All calls are closed. Separate exact area proofs yield
14 necessary source-region inequalities, independent of cog witness poses,
excluding 28 of 42 all-nine sheet allocations. Two brackets plus two cogs
cannot share sheet 2 in these source domains (180,124 versus 174,476 mm²);
the seven-part first-sheet case remains unresolved. Next add the verified
inequalities to the full nine-mover source model, with no focused witness locks
or exclusions. Original/native target, production integration and the complete
H5 matrix remain required. All six prior main checks pass; the queued batch is
ready for a normal push. H2/H5 remain open at 60%; original limits, production,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.


**N4 source area propagation and shared directions, 2026-10-26:** [the evidence](../benchmarks/results/h5-source-area-and-direction-sharing-20261026.md)
retains two closed full nine-mover searches, both UNKNOWN. Fourteen verified
area rules exclude nine allocations beyond the original global-area bounds.
An independently verified equivalent representation shares exact direction
predicates across modes, removing 55,334 variables and 110,668 constraints;
all 66 originals, 394 source pair modes and original guards remain required.
The calls finish in 49.698399s and 51.313156s within their shared 60 seconds;
their 1.532948s/3.508436s soft solver overruns are preserved. Neither result
proves impossibility or supplies a native-valid target. Next independently
verify whether complement clauses can be removed under an exact existential
assignment proof before any distinct bounded call. All earlier calls remain
closed. Prior checkpoints are on main 68c82ae1; five CI jobs pass and Windows
checks are still running at the retained snapshot. Production, READMEs,
releases and the 22 reserved H2 vectors remain unchanged. H2/H5 stay open at 60%.


**N4 one-sided directions and restored conflicts, 2026-10-26:** [the evidence](../benchmarks/results/h5-one-sided-conflict-propagation-20261026.md)
retains two closed UNKNOWN calls. Exact monotone completion permits removal
of 101,455 complement clauses. A second model restores all 5,561,575 proven
domain conflicts across all families, adding only 3,395 auxiliaries and 7,886
constraints. Complete model and bit-matrix audits pass. Both total budgets
pass at 47.741708s/48.140666s; soft overruns of 0.486188s/0.358075s remain recorded.
No target layout or impossibility proof is obtained. A visually inspected
63-original partial identifies adjacent fixed cogs 53/56/61 for a broader
12-mover/54-fixed geometry investigation. Its domains, area bounds and capacities
must be recomputed; prior fixed57 restrictions cannot be carried over. All
earlier calls remain closed. All six checks on main 68c82ae1 now pass, allowing
the queued checkpoints to be pushed normally. H2/H5 remain open at 60%; source,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.


**N4 expanded cog neighborhood, 2026-10-26:** [the evidence](../benchmarks/results/h5-expanded-cog-neighborhood-20261026.md)
releases original cogs 53/56/61 for a fresh 12-mover/54-fixed construction,
retaining all 66 required originals and native guards. All 20 recomputed free
regions and 3,716 inward domains pass independent checks; no old fixed57
conditional restrictions are imported. Cog 53's original constructive-anchor
exclusion is preserved. A complete 729-triple local grid census yields 54 valid
partial repairs; the selected shifts pass all 1,467 original pair and 252 stock
checks. All nine partial cog anchors are represented in the new domains, while
brackets 28/29 and insert 50 remain missing and mandatory. The fresh geometry
covers 66 physical pairs/538 query-pair modes. Next build and audit the complete
12-part coordinate model; no solver or native call occurred here. Prior
checkpoints are on main d1645404, whose CI is running with four jobs passed at
the retained snapshot. H2/H5 stay open at 60%; production, READMEs, releases and
the 22 reserved H2 vectors remain unchanged.


**N4 expanded full-source search, 2026-10-26:** [the evidence](../benchmarks/results/h5-expanded-source-search-20261026.md)
independently verifies the complete 12-mover/54-fixed model: all 66 originals,
214,901 variables, 281,731 constraints, 538 full source pair modes, two exact
area rules and a fresh second-sheet cog capacity of two. Its one call reaches
the hard shared deadline without a saved solver response or candidate, returning
after 60.029781 seconds. The 0.029781-second outer overrun and the ordinary
readback auditor's missing-result failure are preserved; a separate timeout
audit verifies closure without assigning UNKNOWN/INFEASIBLE or claiming native
acceptance. No retry is permitted. A census identifies 16,082 exact pair/normal
projection groups that could remove 495,561 repeated matrix terms; this needs
a separate whole-model audit before another distinct bounded call. The expanded
geometry checkpoint d85f2b2a is on main after all six prior checks passed; its
own CI has four jobs passed at 02:31 UTC. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors remain unchanged.


**N4 projected models and fresh conflicts, 2026-10-26:** [the evidence](../benchmarks/results/h5-projected-source-and-fresh-conflicts-20261026.md)
verifies exact signed projections for all 201,575 source direction definitions,
removing 534,782 repeated terms, and a separate exact unary truth-channel encoding.
Both full 12-mover/54-fixed models preserve all 66 required originals and pass
independent equivalence/import audits. Their separate calls return UNKNOWN in
48.289739 and 48.865027 shared seconds; no candidate is saved and both calls are
closed. Solver soft-limit overshoots remain recorded. A fresh complete census
checks 9,437,545 domain pairs and independently proves 3,948,295 raw-original
collision exclusions. Exact row grouping preserves 25,189,075 physical uses,
ready for independently audited integration into a complete source model.
No old fixed57 table is transferred and no unmarked pair is called feasible.
At 02:49 UTC main d85f2b2a has five CI jobs passed with Windows checks running;
queued evidence awaits terminal CI before a normal push. H2/H5 remain open at
60%; product source, READMEs, releases and the 22 reserved H2 vectors are unchanged.


**N4 domain selection and three-part certificate, 2026-10-26:** [the evidence](../benchmarks/results/h5-domain-selection-and-triple-certificate-20261026.md)
retains a closed full-source UNKNOWN and refines 27,798 additional raw collision
exclusions. A verified necessary master selects domains, but its exact-coordinate
subproblem is INFEASIBLE for that tuple only. All 46 pair subproblems have checked
source witnesses; the complete bounded 120-triple census gives 87 checked
witnesses, 32 UNKNOWN and one conditional negative. Independently of solver
status, exact-rational original geometry proves that insert 50 in query16/row0
permits at most one of the nine cogs in query18/row3, covering all 36 copy pairs.
Next add and audit this single conditional-capacity rule in the necessary master;
all 169 calls here remain closed. The initial readback helper failure and repaired
audit are preserved, as are all soft-limit overruns; all outer budgets pass.
No full target/native/production qualification is claimed. All six checks on main
6a27fec0 pass, permitting a normal push. H2/H5 remain open at 60%; production,
READMEs, releases and the 22 reserved H2 vectors are unchanged.


**N4 conditional selection and original 64-part partial, 2026-10-26:** [the evidence](../benchmarks/results/h5-conditional-selection-and-partial64-20261026.md)
adds and independently audits the raw three-part capacity in the necessary master.
Its new selection moves only the insert; exact coordinates remain INFEASIBLE for
that tuple. Only the 45 changed pair/triple subsets are called: 43 witnesses and
two UNKNOWN. Four larger groups isolate the bracket region and provide an
insert/seven-cog witness. Independent reconstruction verifies a 64-original partial
with 84 cutouts / 9,294 vertices, 1,521 pair and 256 stock-edge checks; brackets 28/29 remain
missing. A new full 66-required model frees both brackets across 16 queries / 2,548 domains
each while keeping ten non-bracket domains and 60 nonbinding partial hints. Its
single call is INFEASIBLE in 27.443101 shared seconds, scoped only to that condition.
Next reopen the two bottom-strip cog domains and audit the broader source model.
All 52 calls stay closed; all shared budgets pass and soft overruns remain recorded.
Main b8535505 CI has four jobs passed at 03:46 UTC; preserve it before a normal push.
H2/H5 stay open at 60%; production, READMEs, releases and 22 reserved vectors are unchanged.


**N4 focused original-geometry obstruction, 2026-10-26:** [the evidence](../benchmarks/results/h5-focused-partial-obstruction-20261026.md)
retains the broader 54-fixed call as UNKNOWN in 47.721778 shared seconds,
including its 0.423204-second solver soft overrun. A fresh 62-fixed construction
is excluded by exact original-geometry checks: both mandatory cogs must occupy
two separate pockets, and every available bracket position collides with the
left cog. A separate rebuild frees middle cog61, giving five mandatory movers
and 61 fixed originals. All geometry, 2,118 inward domains and the complete
22,545-variable/39,619-constraint model pass independent checks; its one call is
INFEASIBLE in 18.006190 shared seconds. These are conditional results, not an
unrestricted impossibility claim. Both calls are closed and failures retained.
Next also release upper-right bracket27/cog58 and rebuild the 59-fixed geometry.
Main679e97e0 is pushed after all six prior checks passed; its own CI40267513191
is live. H2/H5 remain open at 60%; source, READMEs, releases and the 22 reserved
vectors are unchanged. No complete target layout or new release is qualified.


**N4 seven-part obstruction and broader source, 2026-10-26:** [the evidence](../benchmarks/results/h5-seven-part-obstruction-and-broader-source-20261026.md)
retains the full 59-fixed/seven-mover call as UNKNOWN (47.245034 shared seconds,
0.719084-second solver soft overrun). A new independently reconstructed census
checks all 3,644,823 domain pairs and certifies 2,369,711 raw-original conflicts.
Lossless grouping and verified family ordering yield a necessary master, which
is INFEASIBLE in 2.518526 shared seconds. The complete implication audit excludes
that finite source arrangement; it does not claim unrestricted impossibility.
Both calls stay closed. A distinct broader construction now fixes 53 originals
and moves 13, including all nine previously moving cogs and the insert. Its
geometry, 3,599 inward domains, 78-pair/954-mode inventory, physical-region
broadening and freshly derived second-sheet capacity pass independent checks.
No broader-source solver call is opened yet. Next rebuild its conflict tables
and necessary master; no old conditional exclusions transfer. Main679e97e0 has
four checks passed and two live; fec3cd72 is queued. H2/H5 remain open at 60%,
with production, READMEs, releases and all 22 reserved vectors unchanged.


**N4 thirteen-part selection and first-sheet exclusion, 2026-10-26:** [the evidence](../benchmarks/results/h5-thirteen-part-selection-and-sheet-exclusion-20261026.md)
audits the full 53-fixed/13-mover source and all 8,836,883 fresh domain pairs,
including 3,938,040 raw-original conflicts. The necessary master selects a tuple,
but its exact coordinate model is INFEASIBLE. Six distinct subset calls yield
four checked partial witnesses and two UNKNOWNs; both soft overruns and all
failures are retained. A complete sheet-separation audit verifies independent
second-sheet coordinates and derives an eleven-domain first-sheet exclusion.
Adding that one scoped clause yields a new insert-domain selection, whose exact
coordinate model is also INFEASIBLE. All ten calls are closed; all shared limits
pass. No old raw box proof transfers and the unrestricted full source is untested.
Next allow all three brackets every current domain while retaining the ten
verified partial-domain memberships, including insert query16 row181. No new
call is opened yet. The previous two checkpoints are pushed as c22d3e39 after
all six prior main checks pass; its new CI40270374068 is live with three passed
at04:48UTC. H2/H5 stay open at60%; production, READMEs, releases and all22reserved
vectors remain unchanged. No complete target layout or new release is claimed.


**N4 short-sheet capacity and insert exchange, 2026-10-26:** [the evidence](../benchmarks/results/h5-second-strip-capacity-and-insert-exchange-20261026.md)
retains the three-free-bracket source call and three whole-strip calls as
UNKNOWN, with all soft overruns recorded and all shared budgets honored.
A new necessary band model independently verifies 42,399 exact area bounds
over 673 vertical cells and 63 bands, then returns INFEASIBLE. An independently
checked integer certificate extends to continuous positions in the whole usable
stock and excludes four brackets, two inserts and four cogs at the current cog
angle; other compositions, cog angles and the full job remain open. Its strict
adjusted margin is 84,052,628 weighted integer units. A distinct exchange places
insert36 inside cog53's old first-sheet outline with 3.641264 mm clearance to
that outline; all 55 retained first-sheet originals pass 1,485 pairs and 220
stock edges. Next test four brackets, one insert and four cogs on the second
sheet, keeping all nine originals mandatory; originals28/29 also remain required.
All five CP-SAT and one LP certificate calls are closed. Main c22d3e39 has five
checks passed and Windows live at 05:15 UTC; checkpoint4817feff is queued.
H2/H5 stay open at 60%; production, READMEs, releases and all 22 reserved vectors
are unchanged. No full target layout or new release is claimed.


**N4 changed composition and bracket orientations, 2026-10-26:** [the evidence](../benchmarks/results/h5-eight-part-composition-and-orientations-20261026.md)
checks the nine-part necessary band model (INFEASIBLE), then the eight-part
allocation (OPTIMAL). The latter is not a placement: its chosen bracket pattern
is excluded by a full guarded coordinate model. A broader model includes all
eight approved bracket orientations and518 pair modes; its single bounded call
is UNKNOWN. Independently verified sharing of repeated pair planes reduces
95,748 variables/97,636 constraints to40,450/42,338 without changing feasible
coordinates, but its separate bounded call is also UNKNOWN. All five calls are
closed; all shared budgets pass and both soft overruns remain recorded. A
preflight audit typo and downstream failures are preserved with zero opened
solver calls. All66 identities remain mandatory:55 checked first-sheet originals,
eight second-sheet originals and pending first-sheet28/29/37. Next inspect
allowed cog rotations geometrically; no full layout or global impossibility is
claimed. Main81cc4186 CI40273506020 has five checks passed and one live at05:38UTC.
H2/H5 stay open at60%; production, READMEs, releases and22 reserved vectors remain
unchanged. No new release is qualified.


**N4 aligned cog and cover limit, 2026-10-26:** [the evidence](../benchmarks/results/h5-aligned-cog-capacity-and-cover-limit-20261026.md)
screens original cog rotations and verifies a 56.25-degree profile that reduces
width/height by 1.407411 mm. A newly audited 675-variable band model for four
brackets, one insert and four cogs is positive, but its selected full-coordinate
pattern is INFEASIBLE. All 66 identities remain mandatory, with first-sheet
brackets 28/29 still pending. Conservative component covers preserve original
clearance and yield a fully audited 52-variable / 2,732-constraint model with
1,326 rectangles. Its only call is stopped by the 60-second watchdog without a
solver result; 0.016700 seconds of controller overhead is retained, with no
budget pass or retry. Next audit an exact conditional profile-count exclusion
for the failed coordinate pattern. A production review finds no valid ordinary
hole-rider fallback under the existing common-line requirements. All three
calls are closed. Main 81cc4186 passes all six checks, allowing the queued
checkpoints to be pushed normally. H2/H5 stay open at 60%; production, READMEs,
releases and the 22 reserved vectors remain unchanged.


**N4 aligned profile-family exclusions, 2026-10-26:** [the evidence](../benchmarks/results/h5-aligned-profile-family-exclusions-20261026.md)
closes the tested branch with all four short-sheet cogs fixed at 56.25 degrees.
Full-stock coordinate checks reject the selected fixed pattern, its broader
mirror family, and balanced brackets with each of the two insert orientations.
Exact conditional count exclusions preserve the parent capacity model; the
final 692-variable / 104-constraint master is INFEASIBLE. This result is limited
to the guarded source representations and micrometre grid, not unrestricted
original packing. All 20 audits pass and eight calls close within their declared
budgets without overruns. All 66 original identities remain required, including
pending first-sheet brackets 28/29. Next examine independently rotated cogs;
no current exclusion transfers to that changed geometry. Full native/material
validation, production integration and the H5 matrix remain open. Main
88e1dc19 has five successful checks while Windows CI runs, so this checkpoint
is queued for a normal push after that run succeeds. H2/H5 remain open at 60%;
production, READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 mixed cog rotations, 2026-10-26:** [the evidence](../benchmarks/results/h5-mixed-cog-rotations-and-capacity-20261026.md)
verifies the original 20-tooth geometry and a second cog angle of 65.25 degrees,
9 degrees beyond 56.25. Four original-pair screens show no local width benefit
from this half-tooth phase, but a new 709-variable / 67-constraint capacity model
with at least one new-angle cog is positive. Complete coordinate models reject
the selected two/two and three/one cog-phase families with all bracket mirrors.
A checked conditional exclusion preserves the first negative without copying
old single-angle cuts. All 12 audits pass; all four calls close within declared
budgets without overruns. The original run-description 66-constraint typo is
preserved with an erratum; the actual initial model and audits use 67. Next test
balanced bracket types with both insert choices and independent 9/11 cog choices
in one audited 144-mode model. All 66 identities remain mandatory; first-sheet
brackets 28/29, full native/material checks and the H5 matrix remain open.
Main 88e1dc19 passes all six CI checks, so queued 1299e16b and this checkpoint may
be pushed normally after verification. H2/H5 remain open at 60%; production,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.


**N4 two-phase band and spacing exclusions, 2026-10-26:** [the evidence](../benchmarks/results/h5-two-phase-band-and-spacing-exclusions-20261026.md)
closes the tested 56.25°/65.25° source branch. Complete 144-mode balanced and
repeated-bracket families include both insert choices and every cog-angle mix
with at least one new-phase cog. Exact vertical-cell area links preserve all
source-coordinate choices; certified full-height forbidden rectangles add
necessary cog spacing of 257.862–260.232 mm. Both strengthened coordinate
families are INFEASIBLE, and audited conditional exclusions leave the final
721-variable / 94-constraint capacity master INFEASIBLE. This conclusion is
limited to the conservative source geometry and micrometre grid. All 16 audits
pass and six calls are closed within shared budgets; two UNKNOWN calls retain
soft overruns of 0.113378 and 1.477276 seconds. One helper-generation failure
before any solver call is preserved with its separate recovery. Next screen
additional original cog rotations across the tooth period; no current exclusion
transfers to changed angles. All 66 identities and full H5 validation remain
required. Main 50cdc07e has five passing checks while Windows CI runs, so queue
this checkpoint for a later normal push. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved vectors remain unchanged.


**N4 eight-phase geometry and relative-height spacing, 2026-10-26:** [the evidence](../benchmarks/results/h5-eight-phase-geometry-and-spacing-20261026.md)
adds six exact original cog rotations, sampling one tooth period at 2.25-degree
steps. All 64 ordered cog pairs and 184 balanced-family source cases verify;
the full source retains 744 physical orientation modes. A 909-variable necessary
capacity allocation is positive. Complete band links and proven spacing give
a 233,563-variable source model; 2,191 additional full-domain rectangle proofs
add relative-height spacing, reaching 233,773 variables. Both bounded coordinate
calls return UNKNOWN. All 10 audits pass and all three calls close within shared
budgets; the two coordinate soft overruns (0.256623 / 0.249901 seconds) and two
preparation failures with separate recoveries are preserved. No new exclusion
follows. Next investigate a compact sufficient cog-pair representation with
full-domain separation proof; current large calls remain closed. All 66 originals
and full H5 validation remain required. Main 50cdc07e passes all six checks,
allowing queued 6927ae7d and this checkpoint to be pushed normally after review.
H2/H5 remain open at 60%; production, READMEs, releases and 22 reserved vectors
remain unchanged.


**N4 compact cog bin planes, 2026-10-26:** [the evidence](../benchmarks/results/h5-compact-cog-bin-planes-20261026.md)
proves 150,952 original source-face implications across 2,191 complete cog
profile/relative-Y bins. Exact dominance reduces 44,588 positive source edges
to 2,407 sloping requirements. The compact model removes 148,074 auxiliary
variables while retaining every other parent field exactly; its 85,699-variable /
103,151-constraint model implies the full source on a positive. Reverse
equivalence is not claimed. Its sole bounded call is UNKNOWN at 46.077775 solver /
47.517578 shared seconds; the 1.077775-second soft overrun is preserved. All four
audits pass; no full-source exclusion follows. Next investigate both directional
alternatives for bracket/cog and insert/cog pairs with independent full-bin
proofs. All 66 originals and full H5 validation remain required. Main 7271cc8b
has three successful CI jobs and three running, so queue this checkpoint for a
later normal push. H2/H5 remain open at 60%; production, READMEs, releases and
all 22 reserved vectors remain unchanged.


**N4 necessary direction/rectangle exclusion, 2026-10-26:** [the evidence](../benchmarks/results/h5-necessary-direction-and-rectangle-exclusion-20261026.md)
records two closed UNKNOWN searches and a stronger necessary geometry result.
All 80 original non-cog/cog cases support audited horizontal disjunctions;
15 necessary side-order clauses and complete area cells produce a 2,732-variable
projection. Its initial positive contains 11 overlapping pairs. Adding 98
independently verified inner rectangles closes the new-phase branch as
INFEASIBLE in 3.748729 solver / 4.468353 shared seconds,
with all four declared call budgets honored and all 11 audits passing.
Together with the separately closed old two-phase branch, this excludes the
fixed nine-original short-sheet composition at the eight declared cog angles,
with every bracket orientation and both inserts, under source guards and the
micrometre grid. Arbitrary cog angles and other compositions remain open.
Next derive orientation-independent inner cog geometry before another bounded
diagnostic. All 66 originals and full H5 validation remain required. Main
7271cc8b now passes all six checks; queued checkpoints can be pushed normally
after staged byte/ancestry checks. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved vectors are unchanged.


**N4 all-angle continuous composition exclusion, 2026-10-26:** [the evidence](../benchmarks/results/h5-all-angle-continuous-composition-exclusion-20261026.md)
proves an inner cog polygon valid at every real rotation and maps every
continuous original anchor to quantization-safe inner subsets. Exact stock
support, 11 expanded forbidden-rectangle proofs and 42,525 fresh band coefficients
support two independently audited necessary models. The nine-original model
is INFEASIBLE in 3.816914 solver / 4.592091 shared seconds;
removing the insert gives a separate eight-original INFEASIBLE result in
3.932667 / 4.690825 seconds. All seven audits pass,
both 20/30-second calls are closed, and no overruns occur. Four brackets and
four cogs are excluded at this short-sheet target even with continuous positions,
all cog angles and 0.020 mm outward stock relaxation. Therefore the two-sheet
target requires at least nine brackets or twelve cogs on the first sheet.
All 66 identities remain mandatory; six of 70 remaining family-count allocations
are excluded and 64 remain unproved. Next select a different complete sheet
composition, preserving every unselected short-sheet part as a first-sheet
obligation. Main 6246967c has five successful checks and Windows remains live;
queue this checkpoint for a later normal push. H2/H5 remain open at 60%; no
production, README, release or reserved-vector change is claimed.


**N4 complete composition selection and original support, 2026-10-26:** [the evidence](../benchmarks/results/h5-complete-composition-selection-and-support-20261026.md)
accounts for all eleven remaining originals with explicit first-sheet complements.
Two complete necessary selectors find eight-part allocations without proving
optimality or original geometry. Exact original-tip support raises the all-angle
continuous cog-center lower bound to 247.444 mm and rounded X spacing to 245.034 mm;
full-height stems strengthen 192 bracket/cog endpoints. The nine-or-more decision
and its 116-variable geometry-only relaxation both remain UNKNOWN. All four
20/30-second calls are closed, all shared limits and eleven audits pass, and
soft overruns are preserved. No maximum selected count or new count exclusion
is claimed. A common Y=160 mm stem-line proof supports the next audited
formulation: replace the five old bracket anchor-order constraints before adding
conditional stem ordering, never impose both. All 66 originals and full H5
validation remain required. Main 6246967c now passes all six checks, enabling
a normal push of queued checkpoints after staged-byte/ancestry checks.
H2/H5 remain open at 60%; production, READMEs, releases and reserved vectors
are unchanged.


**N4 exact short-sheet count bound and original eight, 2026-10-26:** [the evidence](../benchmarks/results/h5-short-sheet-count-bound-and-original-eight-20261026.md)
proves at most eight remaining parts can fit the target short sheet for the
checked 55-part continuation. Three of four exhaustive >=9 count cases are INFEASIBLE;
the remaining six-bracket/one-insert/two-cog case is excluded by an independent
exact horizontal projection, even with the insert omitted. All 81 pair bounds,
768 guaranteed-Y rectangle pairs, 149 forward states, 1,159 transitions and 149
backward states are verified. The six bounded solver calls are closed; all
shared limits pass and UNKNOWN results remain preserved. A new original
eight-part strip contains all six remaining brackets, insert 37 and cog 53.
Together with the unchanged first 55, the 63-part partial passes 1,513 original
pairs, 252 stock edges and preservation of 87 cutouts/9,426 hole vertices.
Cogs 63/64/65 remain mandatory first-sheet additions; all 66 identities are
accounted for. This bound does not exclude other first-sheet arrangements.
All 16 audits pass. Main 9842e4c1 has 5/6 checks passed and is still running;
queue this checkpoint until CI succeeds. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 exact cog coverage and two-insert strip, 2026-10-26:** [the evidence](../benchmarks/results/h5-exact-cog-coverage-and-two-insert-strip-20261026.md)
proves no additional cog fits the former fixed 55 first-sheet placements at
any angle or continuous center. An exact 483-node partition covers the full
center-stock rectangle with 242 cells; 222 source points/disks and three
rotation angles pass rational membership, Taylor-interval and corner checks.
A revised allocation stacks inserts 36/37 on the short sheet with six brackets
and cog 65, restores cog 53 first, and independently verifies 64 originals,
1,521 pairs, 256 stock edges and 88 cutouts/9,626 hole vertices. The old eight-part
bound is not applied after this allocation change. Cogs 63/64 remain mandatory.
Exact insert-in-cog containment transfers the no-extra-cog result to the new
fixed 55, requiring a first-sheet rearrangement. The next audited inventory
fixes 43 non-cog first originals and nine short originals, with all 14 first-sheet
cogs mandatory movers. Three diagnostic maps are replayed but do not prove
source feasibility. All five audits pass, with zero new solver calls. Main
9842e4c1 now passes all six checks, permitting a normal push of queued
checkpoints. H2/H5 remain open at 60%; production, READMEs, releases and all
22 reserved H2 vectors are unchanged.


**N4 fourteen-cog exclusion and twelve-part strip, 2026-10-26:** [the evidence](../benchmarks/results/h5-fourteen-cog-exclusion-and-twelve-part-strip-20261026.md)
excludes the previous 43-fixed/non-cog and nine-short-original neighborhood:
all fourteen first-sheet cogs are mandatory in an audited all-angle necessary
model, which returns INFEASIBLE in 8.613520 solver / 9.451583 shared seconds.
The sole call is closed. Exact support rectangles and source-point disks cover
all continuous centers with 135 conservative domains; all 91 cog pairs and
2,409 capacity-one conflicts are verified. A changed original short-sheet
construction fits twelve parts: six brackets, five inserts and one cog.
The initial wrong-arm construction and dependent audit failure are preserved;
the repaired copy passes independent checks of 64 originals, 1,392 pairs,
256 stock edges and 88 cutouts/9,626 hole vertices. Inserts 32/34/35 move off
the first sheet. Cogs 63/64 remain mandatory; the next inventory has 40 fixed
first non-cogs, fourteen moving cogs and twelve fixed short originals.
The old exclusion and domain constraints are not transferred. All eight audits
pass. Main 5928270d now passes all six checks, permitting a normal checkpoint
push. H2/H5 remain open at 60%; production, READMEs, releases and all 22
reserved H2 vectors are unchanged.


**N4 full-circle cog spacing and fifteen-part strip, 2026-10-26:** [the evidence](../benchmarks/results/h5-full-circle-cog-spacing-and-fifteen-part-strip-20261026.md)
proves a 254.3 mm minimum original cog-center distance at every rotation, improving
the prior 247.444 mm bound. Independent exact checks cover 720 angle cells,
28,840 robust horizontal segments,2,307,200 capsule/edge tests and all 518,400
ordered angle-cell pairs without assuming rotational symmetry. Six separately
bounded calls are closed: four complete-coordinate formulations UNKNOWN and two
occupancy-only projections positive. No 40-fixed exclusion or full target witness
is claimed. A changed short sheet fits six brackets and nine inserts, freeing
29,137.281062 mm² net first-sheet area while returning cog 65 to first obligations.
This alternative places 63 originals and leaves cogs 63/64/65 mandatory; the earlier
64-original partial is preserved. Independent checks pass 1,233 pairs,252 stock
edges and 87 cutouts/9,426 hole vertices. The next inventory has 36 fixed first
non-cogs, all 15 first cogs mandatory, and 15 fixed short originals. Rebuild domains
and capacities for that changed allocation. All 21 audits pass. Main5ab344f5 has
five successful jobs and Windows checks pending, so the next push is queued until
all six pass. H2/H5 remain open at 60%; production, READMEs, release assets and
all 22 reserved H2 vectors are unchanged.

Subsequent [main 5ab344f5 confirmation](../benchmarks/results/h5-full-circle-cog-spacing-and-fifteen-part-strip-20261026/main-ci-5ab344f5-success.json)
passes all six checks; the checkpoint is eligible for a normal push after
staged-byte and ancestry verification.


**N4 original cog pool and central-notch core, 2026-10-26:** [the evidence](../benchmarks/results/h5-original-cog-pool-and-central-notch-core-20261026.md)
checks all 4,770 source cog poses and all 11,374,065 pair combinations in a fresh
36-fixed neighborhood. The sole selection call is OPTIMAL at twelve cogs;
this finite pool does not exclude unrestricted placements of the required fifteen.
The 63-original readback preserves all cutouts and leaves cogs 63/64/65 mandatory.
Two failed audits and their final finite-segment repair are preserved. A changed
frame arrangement creates a central opening holding two brackets and four inserts.
Its independently checked 39-original core fixes 24 first-sheet parts and the
unchanged fifteen short-sheet parts; all remaining four brackets, eight inserts
and fifteen cogs are mandatory movers. Checks pass 381 original pairs, 156 stock
edges and 55 cutouts/4,586 hole vertices. The separate four-bracket notch model
is INFEASIBLE only within its declared grid/axis-gap construction. Both calls
are closed; old domains and finite limits do not transfer to the changed core.
All eleven audits pass. The earlier 64-original partial is preserved. Main
07c17806 now passes all six checks, permitting a normal checkpoint push.
H2/H5 remain open at 60%; production, READMEs, releases and all 22 reserved H2
vectors are unchanged.


**N4 joint source graph and compact domains, 2026-10-26:** [the evidence](../benchmarks/results/h5-joint-source-graph-and-compact-domains-20261026.md)
independently verifies 20,000 original poses, all 199,990,000 candidate pairs and
30,557,608 conflicts around the changed 24-original first-sheet core. Certified
substitutions retain exact feasibility with 15,165 poses. The sole model requires
all four remaining brackets, eight inserts and fifteen cogs; it closes UNKNOWN
after presolve with zero branches. Internal solver / returned-call / shared
times are 60.515847 / 61.015893 / 63.909778 seconds. Soft overruns and the failed
clock-scope assertion are preserved; no retry or exclusion is claimed. Fresh
exact cog-center coverage has 38 domains, with all twelve moving non-cogs still
required in the next joint geometric model. Old world-circle coordinates were
rejected and reprojected through current owners before independent verification.
All seven audits pass, with three failed attempts preserved. Main 4e1549ad now
passes all six checks, permitting a normal checkpoint push. H2/H5 remain open
at 60%; production, READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 compact joint model and nine-insert core, 2026-10-26:** [the evidence](../benchmarks/results/h5-compact-joint-model-and-nine-insert-core-20261026.md)
proves necessary inner-component geometry for every allowed quarter turn/mirror
and continuous non-cog anchor, using 112 corners and 448 exact edge tests.
All twelve non-cogs and fifteen cogs remain mandatory in the audited 6,658-variable,
8,244-constraint model. Its sole call explores 288,549 branches and closes UNKNOWN
in 60.068638 returned-call / 60.876190 shared seconds, with soft overruns recorded.
No source witness or neighborhood exclusion is claimed. A different checked core
puts nine inserts in the central opening, reducing remaining first-sheet filled
demand by 19,000 mm². Its 42 originals pass 456 pair checks, 168 stock edges and
54 cutouts/4,464 hole vertices. All six remaining brackets, three inserts and
fifteen cogs stay mandatory; rebuild domains for the new 27-fixed first sheet.
The prior 64-original partial is preserved. Main 32282158 CI is still running
at review, so the next push is queued until all six checks pass. H2/H5 remain
open at 60%; production, READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 finite cog-phase obstruction, 2026-10-26:** [the evidence](../benchmarks/results/h5-original-cog-phase-wheel-20261026.md)
checks all fifteen required cogs on five declared triangular pitches with 36
original half-degree angles. Independent source reconstruction verifies 194,400
near-pair combinations. The 16-variable/30-constraint phase model closes
INFEASIBLE in 0.170663 returned-call/1.124359 shared seconds, within 20/30 limits.
An independent enumeration of 618 prefixes reproduces 458 reachability records:
the contained seven-cog wheel has no assignment at any tested pitch, although
some triangles fit. This excludes only the finite construction; arbitrary
angles, moved centers and the fixed27 neighborhood remain open. All six
brackets, three inserts and fifteen cogs stay required for the complete layout.
All four audits pass. Main 6c5bf878 was pushed after all six prior checks passed;
its new CI is running, so queue this checkpoint. H2/H5 remain open at 60%;
production, READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 staggered frame strip and joint contacts, 2026-10-26:** [the evidence](../benchmarks/results/h5-staggered-frame-core-and-joint-contacts-20261026.md)
verifies a different 41-original core with three brackets in the frame-side strip
and five inserts in adjacent gaps. Remaining first-sheet filled demand falls by
40,800 mm²; one insert extends 10.45 mm beyond the prior top. Independent checks
cover 430 pairs, 164 stock edges and 59 cutouts/5,074 vertices. All three remaining
brackets, seven inserts and fifteen cogs stay mandatory. A fresh 2,000-pose pool
has all 1,999,000 source pairs and 573,329 conflicts independently verified.
Its single joint call closes INFEASIBLE in 0.960597 returned/2.098136 shared seconds.
Search advances beyond presolve; worker counters are reported separately.
The finite pool is closed, with no unrestricted exclusion. All five audits pass;
four failed checker attempts are preserved. Main 6c5bf878 passes all six checks,
allowing the queued two-commit push. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 paired bracket strip and clearance capacity, 2026-10-26:** [the evidence](../benchmarks/results/h5-paired-strip-clearance-capacity-20261026.md)
verifies a changed 49-original core: all twelve brackets and nineteen inserts
fit beside eighteen frames, leaving two inserts and fifteen cogs mandatory.
Independent checks cover 666 pairs, 196 stock edges and 73 cutouts/6,782 vertices.
Fresh continuous all-angle domains yield 1,111 capacity cells and 127,947 verified
conflicts. Two distinct necessary positives fail their finite source preflights;
all 9,828 sampled events are independently checked. Separate exact oblique-support
proofs exclude 61 cells. Using the required 0.2 mm clearance joins fixed exclusion
regions through 833 audited union atoms and proves five further cell exclusions.
The stronger 1,818-constraint model closes UNKNOWN after search in 20.026862
returned/20.772295 shared seconds, with its 0.026862-second soft overrun recorded.
All three calls are closed, without retries. No full layout or unrestricted
exclusion is claimed. All fifteen audits pass. Main 4e3b316c passes all six checks,
allowing the next normal checkpoint push. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors are unchanged.


**N4 clipped capacity and short-strip allocation, 2026-10-26:** [the evidence](../benchmarks/results/h5-clipped-capacity-and-short-strip-20261026.md)
clips all certified forbidden integer points from the surviving cog cells.
Independent checks cover 1,313 atomic regions, 4,268 hull corners and all
545,490 cell pairs, proving 139 new conflicts. The stronger 1,045-variable,
1,747-constraint model closes UNKNOWN after search in 20.044475 returned/
21.306630 shared seconds; its 0.044475-second soft overrun is recorded.
A distinct six-bracket/six-insert/cog short-strip attempt checks four fixed
variants and144 finite translation queries, finding no candidate. Fixed source
geometry is independently validated; empty conservative query records are read
back, not promoted to an independent exclusion. Both attempts are closed.
All four audits pass. H2/H5 remain open at60%; production, READMEs, releases
and all22 reserved H2 vectors are unchanged. Preserve main's CI40359411459
and wait for all six checks before the next push.


**N4 complete joint insert/cog necessities, 2026-10-26:** [the evidence](../benchmarks/results/h5-paired-strip-joint-geometry-20261026.md)
retains every source cog center in 29 exact merged domains, independently checking
3,632 integer atoms. All four insert modes pass 16 corner and 64 exact edge tests.
Both remaining inserts and all fifteen cogs are mandatory in the independently
reconstructed 8,440-variable/10,044-constraint model. Current clearance regions,
105 cog pairs, 30 cog/insert circle pairs, 60 support strips and 840 support-vertex
boxes supply necessary geometry. The sole call closes UNKNOWN after search in
60.060177 returned/60.999099 shared seconds, with its 0.060177-second soft overrun
preserved. The returned worker records 1,526,058 branches and 250,475 conflicts.
No source witness or exclusion is claimed; the call is closed. All three audits
pass. Main cb7f7b1f now passes all six checks, allowing a normal two-commit push.
H2/H5 remain open at 60%; production, READMEs, releases and all 22 reserved H2
vectors are unchanged.


**N4 mixed frame rows and source contacts, 2026-10-26:** [the evidence](../benchmarks/results/h5-mixed-rows-source-contacts-20261026.md)
checks a changed 18-frame core and the preserved 15-part short sheet against
258 pairs, 132 stock edges and all 45 cutouts. Every remaining bracket, insert
and cog stays mandatory (6/12/15). A fresh 4,200-pose pool adds mutual bracket/
insert contacts and rejects 1,280 obstacle-interior proposals before quotas.
Independent checks reproduce all 8,817,900 candidate pairs and 1,998,405 conflicts;
25,736 verified cliques preserve the complete graph. The exact 4,200-variable,
25,739-constraint model closes UNKNOWN after search in 60.071975 returned/
61.044539 shared seconds. Its soft overrun and initial cover overrun remain
recorded. All four independent audits pass; a failed log-precision checker is
preserved and repaired without rerunning the search. No source witness or
exclusion is claimed. H2/H5 remain open at 60%; production, READMEs, releases
and all 22 reserved H2 vectors are unchanged. Wait for all six checks on main
e158daa2 before the next push.


**N4 global short-sheet frontier and eight-bracket construction, 2026-10-26:** [the evidence](../benchmarks/results/h5-global-short-frontier-and-eight-brackets-20261026.md)
uses the full-circle cog certificate to strengthen short-sheet horizontal
spacing to 251.956 mm. Independent forward/backward recurrences check 222 states,
1,998 transitions and all 81 pair bounds without fixing a first-sheet layout.
All 4,576 bracket/insert/cog allocations are covered: 3,850 fail the necessary
ordering and 272 more fail exact filled-outer area; 454 remain necessary-only.
A new actual eight-bracket/five-insert short sheet carries 800 mm² more filled
area than the former six-bracket/nine-insert option. Its 42-original core passes
484 pairs, 168 stock edges and all 58 cutouts; four brackets, five inserts and
fifteen cogs stay mandatory. Both independent audits pass, with one repaired
checker expectation preserved. No solver/native call or full target witness.
All six main e158daa2 checks pass, allowing the queued two-commit push. H2/H5
remain open at 60%; production, READMEs, releases and all 22 reserved H2 vectors
are unchanged.


**N4 bounded source sliding, 2026-10-26:** [the evidence](../benchmarks/results/h5-source-sliding-and-guided-penalties-20261026.md)
records three closed searches: 24 movers with 29 fixed first parts, all 53 first
parts movable, and adaptive positive penalties on all 53. Independent original
geometry readers retain all 66 identities, 90 cutouts and 10,026 hole vertices,
but find 40/52/50 pair failures and 5/9/10 stock failures respectively. Lower
overlap penalties are not material or valid part-count improvements. Neither
all-part search accepts a frame turn; no global impossibility is claimed.
Three preflight and three final checks pass; one diagnostic-summation checker
failure is preserved and repaired without changing physical tolerances or
rerunning a search. All six main ea4f2ebf checks now pass after the browser-only
retry of a dependency-download timeout. The failed attempt is preserved.
H2/H5 remain open at 60%; no native/full-quality run or new release qualifies.
The next distinct allocation must first repair the older 64-part partial's
short-sheet clearance; all 22 reserved H2 vectors remain unopened.


**N4 retained-64 allocation and full first-sheet search, 2026-10-26:** [the evidence](../benchmarks/results/h5-retained64-allocation-source-search-20261026.md)
repairs the older four-bracket/two-insert/three-cog short sheet to current
clearances, independently passing 36 pairs, 36 edges and all17 cutouts.
Its exact cog angle is reconstructed from source, without a symmetry assumption.
All57 first originals remain mandatory and movable; the two missing brackets
are seeded from 22,640 deterministic proposals. The sole guided call closes
ITERATION_LIMIT in29.220400 optimization/30.492711 shared seconds. All66 source
identities, 90 cutouts and10,026 hole vertices are retained, but final readback
finds60 pair failures and10 stock failures. Lower overlap penalty is not a
material improvement. No native/full-quality run or release is qualified.
Both independent audits pass; all6 main ea4f2ebf checks pass, permitting a
normal two-commit checkpoint push. H2/H5 stay open at60%; all22 reserved H2
vectors stay unopened. Closed searches will not be extended or reseeded.


**N4 coordinated frame blocks and source obstruction, 2026-10-26:** [the evidence](../benchmarks/results/h5-frame-blocks-source-cells-and-displacement-20261026.md)
closes four joint frame-orientation alternatives; all66 source originals remain
mandatory, but each full result fails geometry. A separate685-variable model
uses571 verified source-clearance cells and2,056 exact integer halfplanes for
all57 first parts; its sole call closes INFEASIBLE in presolve in0.026760 returned/
1.184046 shared seconds, excluding only the finite sufficient cell subset.
An independent exact source certificate is stronger: four turned frames and one
vertical insert require1,509.990 mm of width versus1,487 mm stock. All10 vertical
interval pairs must intersect under any movement up to180 mm. At least one of
those five originals must change mode or move vertically more than180 mm;
horizontal positions and the other61 parts were not fixed. This is not a whole-job
exclusion. Five independent audits pass; two diagnostic-reader failures are
preserved and resolved without changing geometry or physical thresholds. H2/H5
remain open at60%; no native/full-quality run or release qualifies. Preserve
main f2322ccd's live checks and wait for all6 before the next push.


**N4 full-stock source feasibility, 2026-10-26:** [the evidence](../benchmarks/results/h5-full-stock-source-cell-feasibility-20261026.md)
removes every local movement bound and retains all 57 first originals plus the
verified short nine. All 1,596 source pairs yield 38,287 conservative free cells
and 136,401 exact integer halfplanes; independent checking covers 174,688 source
samples. Another 65 source-contained rectangles provide necessary non-overlap
and cumulative strip constraints. Every one of the 38,401 variables and 138,177
serialized constraints is checked, with whole-stock domains and no position
hints. The sole call closes UNKNOWN after search: 179,798 returned branches,
5,060 conflicts, 60.089808 returned/61.906913 shared seconds. Its soft overrun is
preserved; there is no assignment or exclusion. Four independent audits pass.
Prior main f2322ccd passed all six checks and checkpoint db4d2309 was pushed
normally. Preserve its live CI40386947038 before the next push. H2/H5 remain
open at 60%; no native/full-quality run or new release qualifies, and all 22
reserved H2 vectors remain unopened.


**N4 source-cut attempts and constructive seed, 2026-10-26:** [the evidence](../benchmarks/results/h5-lazy-source-cuts-and-constructed-seed-20261026.md)
records two distinct pipelines, each CLOSED UNKNOWN in its first round without
returning a candidate or adding new source cuts. The first uses 114 variables/
180 necessary constraints; a separate direct construction satisfies all of them
but has 38 actual source collisions. Its 54-source-valid partial contains every
frame, bracket and insert plus the short three cogs; the other 12 cogs remain
present and mandatory. This is not a new best partial count or full source fit.
The second starts with the 38 actual failing-pair disjunctions and 90 non-cog
hints, fixes no first original, and closes UNKNOWN with 3,880 variables/13,246
constraints. Returned/shared times are 15.014221/16.716055 and
15.056194/18.386994 seconds; small soft overruns are preserved. Four independent
audits pass. A stronger source-contained cog representation is the next distinct
hypothesis; neither closed search may be extended or reseeded. H2/H5 remain open
at 60%; no native/full-quality run or release qualifies and all 22 reserved H2
vectors remain unopened. Wait for all six main CI40386947038 checks before the
next normal checkpoint push.


**N4 source cog strips and timing failure, 2026-10-26:** [the evidence](../benchmarks/results/h5-cog-source-strips-and-timing-20261026.md)
adds 728 disjoint cog strips covering 90.150340%/90.767855% of the two actual cog
modes. With the unchanged non-cogs, 781 source-contained rectangles
add necessary constraints to the prior model, whose 13,246 constraints remain byte-exact; all
14,811 new-model constraints are independently verified. Both new cumulative
constraints alone reject the earlier constructed invalid witness. The sole
search closes UNKNOWN with 20,248 branches/5,401 conflicts and no assignment.
Its 87.617085 solver/87.625742 returned/88.877085 shared seconds exceed the
requested 60-second solver limit by 27.617085 seconds: timing is explicitly
unqualified despite the 90-second process boundary being met. Four independent
audits pass without claiming H5 acceptance, and the closed call cannot be
extended or reseeded. All six main db4d2309 checks now pass, allowing the next
normal checkpoint push. H2/H5 remain open at 60%; no native/full-quality run or
new release qualifies and all 22 reserved H2 vectors remain unopened.


**N4 exact source capacity profiles, 2026-10-26:** [the evidence](../benchmarks/results/h5-source-capacity-profiles-20261026.md)
verifies all 114 original/axis profiles on 2,315 integer slabs and preserves both
781-rectangle source-strip capacities using 1,218 projection intervals. A different
staged model has 114 whole-stock coordinates/1,400 constraints, 90 non-cog hints,
no first part fixed, and no initial source-cell selectors or additional global
strip non-overlap. Its only round closes UNKNOWN: 155,233 branches, 22,875 conflicts,
30.043256 returned/32.950780 shared seconds, no candidate or new source cut.
Small soft overruns remain recorded; the 60/90-second total boundaries are met.
The previously overlong fj worker is explicitly excluded. Profile and complete
model/response audits pass without a full-source claim. All prior three
checkpoints were pushed normally as ff5036af after six successful main checks;
preserve its live CI 40393931732 before the next push. H2/H5 remain open at 60%;
no native/full-quality run or release qualifies, and all 22 reserved H2 vectors
remain unopened.


**N4 variable-allocation geometry, 2026-10-26:** [the evidence](../benchmarks/results/h5-allocation-aware-geometry-20261026.md)
prepares all 66 originals for a coupled two-sheet model with all 454 surviving
short count vectors and their first-sheet complements. Thirteen source proxy
variants cover all bracket modes, both rectangular frame/insert footprints and
every real cog rotation; 24 of 26 sheet/mode domains are allowed. An independent
audit verifies 28 quantization-safe non-cog rectangles, 132 integer disk corners,
104 domain endpoints and every count vector. Cog source strips use the proved
109.113 mm inner disk. Separate 127.148 mm virtual separation disks follow from
the 254.297 mm rounded-center bound and may constrain cogs only, never mixed
families. Mathematical stock relaxations do not change the source/material
acceptance target. No allocation-aware model or solver has opened yet. Prior
calls remain closed. H2/H5 stay open at 60%; no native/full-quality run or release
qualifies and all 22 reserved H2 vectors remain unopened. Preserve main
ff5036af CI40393931732 until all six checks pass before the next normal push.


**N4 coupled two-sheet model, 2026-10-26:** [the evidence](../benchmarks/results/h5-coupled-allocation-model-20261026.md)
links every one of the 66 originals to exactly one sheet/mode choice, with 342
options, all 454 short count rows, no fixed short allocation and all-angle cog
necessities. The independent reader verifies all 609 variables/5,016 constraints,
1,368 stock guards, 1,686 optional rectangles, both source-area constraints and
separate source/cog-only virtual capacities. Filled source area excludes four
further count vectors, without excluding the job. The sole call closes UNKNOWN:
87,096 branches, 62,265 conflicts, 60.056339 returned/61.456279 shared seconds.
Small soft overruns are preserved; no assignment or source/native witness exists.
The model and response audits pass, and the closed call cannot be extended or
reseeded. H2/H5 remain open at 60%; no full-quality run or new release qualifies,
and all 22 reserved H2 vectors remain unopened. Preserve main ff5036af
CI40393931732 until all six checks pass before the next normal push.


**N4 retained64 proxy witness and all-angle obstruction, 2026-10-26:** [the evidence](../benchmarks/results/h5-retained64-proxy-witness-and-disk-proof-20261026.md)
constructs both missing bracket copies without changing the 64 retained source
transforms. All 609 domains/5,016 constraints of the closed coupled model pass,
proving that necessary model feasible without another solve. Original-ring
readback still fails: eight new physical intersections plus six retained gap
failures and three retained stock-guard failures. An independent exact disk
certificate covers all 26 complete coarse-free bracket cells across all eight
modes, even with arbitrary cog angles. Thus at least one existing non-cog pose
or cog center must change; phase-only repair and fixed64 insertion cannot work.
Four audits pass; one auxiliary list-order reader failure is preserved. No solver
or native call occurs. All six main ff5036af checks now pass, allowing the next
normal push. H2/H5 stay open at 60%; no full-quality run or release qualifies and
all 22 reserved H2 vectors remain unopened.


**N4 mixed all-angle separation, 2026-10-26:** [the evidence](../benchmarks/results/h5-mixed-octagon-separation-20261026.md)
verifies a source-contained cog octagon and 24 exact bracket-component forbidden
polygons. They detect all eight demonstrated collisions and cover all 26 fixed
anchor cells. The strengthened all-original model leaves positions, sheets and
modes free, preserves the entire previous model, and adds 384 conditional
separation clauses/4,608 facets. All 5,217 variables/10,008 constraints and 609
advisory hints are audited; the old hint violates the new rules. The sole call
closes UNKNOWN: 127,806 branches, 54,245 conflicts, 60.063253 returned/61.378682
shared seconds, with small soft overruns preserved. Three independent audits
pass, but no source/native witness or unrestricted exclusion exists. No retry
or reseeding is permitted. H2/H5 stay open at 60%; no release qualifies and all
22 reserved vectors remain unopened. Preserve main36f162d0 CI40400314122 until
all six checks pass before the next normal push.


**N4 fixed-noncog capacity, 2026-10-26:** [the evidence](../benchmarks/results/h5-fixed-noncog-cog-capacity-20261026.md)
excludes the saved 51 non-cog poses even when all 15 cog centers, real rotations
and sheet assignments are free. The exact whole-domain cover checks 33,275
closed cells and preserves boundary centers. Independent graph/branch readers
prove lower/small/short capacities of 6/1/3. A new necessary five-center upper
model, with all 1,370 variables/1,439 constraints audited, closes INFEASIBLE in
0.413757 returned/1.759713 shared seconds. The combined capacity is 6+4+1+3=14,
below 15: at least one non-cog pose or orientation must change. This is a fixed
arrangement exclusion, not unrestricted impossibility or a source witness.
Three audits pass; no native call, H5 credit or release follows. H2/H5 remain
open at 60% and all 22 reserved vectors are unopened. Main36f162d0 browser CI
timed out after slow Ubuntu dependency downloads; raw failure evidence is kept.
Preserve its live Windows check before retrying only the browser job, and require
all six successful jobs before pushing the queued checkpoints.


**N4 retained49 source-guard repair, 2026-10-26:** [the evidence](../benchmarks/results/h5-retained49-source-guard-repair-20261026.md)
repairs all six retained pair-clearance and three stock failures. The first
50 µm construction stays preserved with its exact −29 µm, seven-insert cycle.
A separately bounded correction derived from that cycle allows only those
seven inserts up to79 µm in positive Y; all source thresholds stay unchanged.
The independent reader verifies all49 originals, 918 source pairs, 196 stock
edges, 69 cutouts and6,294 hole vertices: zero failures, minimum gap0.2256789543 mm,
extra stock0.0131 mm. All17 remaining originals (two brackets and15 cogs) are
still mandatory. Rebuild geometry from the corrected poses; the old fixed51
capacity exclusion does not transfer. This is not a66-part witness, native
pass or H5 credit; H2/H5 remain open at60%. All22 reserved vectors stay unopened.
Main36f162d0's other five jobs passed before its browser-only attempt2 retry;
preserve that live retry and require all six successes before the queued push.


**N4 corrected49 geometry and cog flat-edge support, 2026-10-26:**
[The evidence](../benchmarks/results/h5-corrected49-flat-edge-20261026.md) rebuilds all fixed-obstacle geometry from the corrected
source-valid49. All17 movers remain mandatory. Exact all-angle source-vertex
support proves186 new flat-edge forbidden strips and removes552 more whole
cog-center cells while preserving every boundary center and all15 prior cells.
Seven audits pass. The base15,797-variable and stronger21,557-variable models
both end UNKNOWN in one60-second call each; raw timing, failures and results
remain preserved and both searches are closed. There is no full66 witness,
fixed49 exclusion, native call or H5 credit. H2/H5 stay open at60%; all22 reserved
vectors remain unopened. Main36f162d0 browser attempt2 also timed out before tests,
with18m07s checkout; prepare and validate a CI checkout repair on an isolated
branch before the queued main push. Production and READMEs are unchanged.


**CI checkout repair, 2026-10-26:** [the diagnosis and local checks](../benchmarks/results/ci-sparse-evidence-checkout-20261026.md)
preserve main36f162d0's second browser timeout:18m07s checkout, tests never started.
The four CI checkouts now omit only historical result ZIPs, avoiding3.51GB while
retaining all9,504 other files byte-for-byte. No evidence is deleted and all test
commands/timeouts remain unchanged. All31 existing Python CI commands pass in an
isolated sparse checkout. Full six-job validation will run on the working branch
before the normal main push; old runs remain preserved. H2/H5 remain open at60%,
all22 reserved vectors remain unopened and no release qualifies.


**N4 exact capacity and actual-tooth corner support, 2026-10-26:**
[The evidence](../benchmarks/results/h5-cog-corner-support-20261026.md) verifies 9,420,646 cell pairs and replays 199,989 completed
certificate nodes. Short-sheet capacity is at most three cogs; first-sheet13
remains unresolved at the closed shared200,000-node cap, and14/15 receive no
nodes. The costly first reader is preserved; an equivalent bitset reader passes
without repeating the search. A separate all-angle actual-source-vertex theorem
certifies1,116 rectangle-corner boxes and removes34 more whole cells, leaving4,514
while retaining all15 prior centers and legal boundary coverage. This modest
tightening does not open another feasibility call. There is no full66 witness,
fixed49 exclusion or native validation. H2/H5 remain open at60%; all22 reserved
vectors remain unopened and no release qualifies.

Publication update2026-10-28: remote main's14 layered-kit example files are
preserved in a clean merge with the five queued checkpoints. Both parent heads
pass all six jobs; product source, READMEs and upstream releases are unchanged.
The combined main head will receive its own checks after the normal push.


**N4 oblique original-source construction, 2026-10-28:** [the evidence](../benchmarks/results/h5-oblique-source-construction-20261028.md)
independently verifies3,888 contact cases and a new source-valid64 layout with
all15 cogs and21 inserts. All1,353 source pairs and256 stock edges pass; minimum
gap0.2148269833mm and extra stock0.025mm exceed the unchanged guards. Two bracket
copies remain mandatory. Eighteen conservative anchor-pocket regions are rebuilt
from original world polygons; empty pockets are not source-impossibility proofs.
A new17-mover phase7 joint call closes at a local minimum after128 evaluations
in0.046184 search/2.960379 shared seconds. Its complete66 candidate fails33 source
pairs and2 stock edges, preserved with all90 holes/10,026 hole vertices. Four
independent audits pass, but there is no complete valid66 or native/H5 pass.
All searches stay closed; next change the structural arrangement, not the guard.
Mainf4f6f1fe preserves the layered-kit example and has five passing CI jobs, with
Windows still running; defer the next main push until all six pass. Production,
READMEs and upstream releases are unchanged. H2/H5 remain open at60%; all22
reserved vectors stay unopened and no new release qualifies.


**N4 short-sheet cog transfer, 2026-10-28:** [the evidence](../benchmarks/results/h5-short-cog-transfer-20261028.md)
tests7 brackets/5 inserts/1 cog while retaining three existing bracket-pair/insert
groups. The finite source construction exhausts47 bracket poses,115 cog-pair
poses and1,270 second-insert checks in0.152079 search/0.565650 shared seconds;
it finds no13-part witness and is closed. All635 prefixes with only one added
insert independently pass41,910 source pairs and30,480 stock edges. The retained
7-bracket/4-insert/1-cog prefix yields a valid62-part whole inventory, with three
brackets and one insert still mandatory; it does not improve the prior64 count.
No infeasibility, native pass or H5 credit is claimed. Next free all13 short
placements in a source-supported necessary model rather than repeat the fixed
construction. Mainf4f6f1fe now passes all six CI jobs, enabling the next normal
push after a fresh remote/live-run check. Production, READMEs and upstream
releases remain unchanged. H2/H5 stay open at60%;22 reserved vectors are unopened
and no release qualifies.


**N4 all-free short13 necessities, 2026-10-28:** [the evidence](../benchmarks/results/h5-short13-necessary-20261028.md)
frees every position for7 brackets/5 inserts/1 cog, covering all allowed modes
and all real cog angles. Exact source inner/edge/corner geometry, all12,197
variables and15,458 constraints pass independent audits. All635 known valid
source12 prefixes satisfy238,125 mixed rules and7,620 stock domains. The sole
60-second solver call closes UNKNOWN after2,869,712 branches/39,823 conflicts,
60.102096 returned/62.228226 shared seconds; small soft overruns are retained.
No assignment, source13 witness, count exclusion or native/H5 pass exists, and
the call will not be retried or extended. Next seek a stronger exact structural
projection or different complete source construction. Main390fb2d3 contains both
prior checkpoints; its newCI40676201231 has four passing jobs and two live checks.
Preserve it until all six pass before the next main push. Production, READMEs
and upstream releases are unchanged. H2/H5 stay open at60%;22 reserved vectors
remain unopened and no new release qualifies.


**N4 all-source short13 and band-area bounds, 2026-10-28:** [the evidence](../benchmarks/results/h5-short13-source-band-20261028.md)
retains one new search with all 13 original placements free. All 196,850 initial
grid scores are replayed; the sole local call closes after 123 evaluations in
2.218165 search / 5.856514 shared seconds. The original-shape audit finds 15 pair
failures and two stock failures. A separate exact all-angle cog-area proof
strengthens 275 of 350 band bounds; 44,800 rational triangle caps and 6,350
known-source band checks pass. The audited stronger model preserves the prior
model byte for byte and totals 18,640 variables / 23,549 constraints. Its sole
bounded call returns UNKNOWN after 67,352 branches / 40,926 conflicts in
60.120701 returned / 61.081026 shared seconds; the small soft overrun is retained.
Both searches are closed. No source13 witness, count exclusion, full66 or native
pass exists. Next derive a stronger exact structural projection or change the
complete source construction. Main390fb2d3 now passes all six CI jobs, enabling
the queued checkpoint push after fresh remote/live-run checks. Production,
READMEs and upstream releases are unchanged. H2/H5 remain open at 60%; all 22
reserved vectors remain unopened, and no new release qualifies.


**N4 short-sheet 7/5/1 exclusion, 2026-10-28:** [the evidence](../benchmarks/results/h5-short13-x-exclusion-20261028.md)
certifies stronger horizontal source spacing across all 983,930 integer relative
Y values and every real cog angle. Eight mixed directions improve by up to
23.375 mm; the core-only frontier still has 454 survivors. Including every
mandatory insert and source height in a reduced X-capacity model gives 158
variables / 4,372 independently verified constraints. Its sole call returns
INFEASIBLE after 68,907 branches / 25,215 conflicts in 2.037863 returned /
2.713545 shared seconds, without overrun. Source mapping and positive controls
pass: all 635 valid source12 prefixes satisfy 41,910 pair-spacing checks and
26,035 source-rectangle capacity checks. Seven brackets/five inserts/one cog is
excluded on the target short sheet; upward closure also excludes 7/6/1. The
complete frontier retains 452 possible count allocations. This is not a full66
exclusion or witness. Stop both excluded allocation branches and return to a
different full source construction, such as freeing all 24 first-sheet packet
parts around the valid 42-part core. Main541d5bc9 has five passing CI jobs and
Windows still running; preserve it before the next main push. Production,
READMEs and upstream releases are unchanged. H2/H5 stay open at 60%; all 22
reserved vectors remain unopened, and no new release qualifies.


**N4 whole upper-group source search, 2026-10-28:** [the evidence](../benchmarks/results/h5-oblique24-baseline-review-20261028.md)
frees all 24 upper-group originals around the independently valid 42-part core,
including the two existing corner brackets and five inserts fixed previously.
All source-mode, free-region and 48 gradient checks pass. The sole local call
closes after 212 evaluations / one mode change in 0.074719 search / 2.892560 shared
seconds. Original all66 readback retains 34 pair failures and eight stock failures;
this is no source witness or infeasibility proof. A read-only nine-archive baseline
review confirms 21 insert hole-riders in each normal layout and none in common
mode, so the normal layout is not a reusable PIH-OFF witness. The original
4,988,890.353495 mm² material target remains unchanged. Next use the verified
X-capacity formulation on distinct remaining maximal short-count vectors,
retaining unknown/unprocessed cases and all 452 current candidates until excluded.
Main541d5bc9 now passes all six CI jobs; the two queued checkpoints may be normally
pushed after fresh remote/live-run checks. Production, READMEs and upstream
releases are unchanged. H2/H5 stay open at 60%; all 22 reserved vectors remain
unopened, and no new release qualifies.


**N4 remaining short-count screen, 2026-10-28:** [the evidence](../benchmarks/results/h5-short-count-x-screen-20261028.md)
independently checks all 6,649 variables / 85,989 constraints before one bounded
pass over the 32 predeclared maximal count vectors. Four cases are INFEASIBLE,
27 remain UNKNOWN, and 7/4/1 has a fully checked relaxed assignment. The four
new exclusions are 0/10/5, 1/8/5, 2/9/4 and 4/7/3 (brackets/inserts/cogs).
All 4,576 original rows remain recorded; 448 count candidates survive. All 32
calls finish in 85.249128 shared seconds; the largest 3-second return overrun is
0.034838 seconds and is preserved. This pass is closed without retries. Known
source-valid 7/4/1 and 8/5/0 remain allowed; no full66 or native pass follows.
Next inspect a full-geometry 8/6/0 short-sheet construction to free first-sheet
space, auditing a new model before any bounded call. Main f9629063 passes all
six CI jobs. Production, READMEs and upstream releases are unchanged. H2/H5
remain open at 60%; the 22 reserved vectors stay unopened and no release qualifies.


**N4 source stem-gap exclusion, 2026-10-28:** [the evidence](../benchmarks/results/h5-short-stem-gap-exclusion-20261028.md)
rules out actual short-sheet 8/6/0 and 8/7/0 independently of the preserved
conservative source call, which closed UNKNOWN in 60.104262 returned /
60.912529 shared seconds. Source stems divide the sheet into nine gaps.
Exhaustive scheduling and independent readback cover all 12,925 task orders,
94,348 earliest-start steps, 42 gap bounds and 2,380 chain transitions; a backward
recurrence agrees. Eight brackets/six inserts need 1,489.948 mm, exceeding the
relaxed stock width by 2.908 mm. All original modes and the valid 8/5/0 control
pass. All 4,576 count rows remain recorded and 446 candidates survive. No full66
or native pass exists. Both excluded branches are closed. Next predeclare and
audit the larger gap cases for remaining seven-bracket allocations, reusing
existing bounds exactly. Main f61f25d6 passes all six CI jobs. Production,
READMEs and upstream releases are unchanged. H2/H5 remain open at 60%; all
22 reserved vectors remain unopened and no new release qualifies.


**N4 seven-bracket bound and source construction, 2026-10-28:** [the evidence](../benchmarks/results/h5-seven-bracket-source-and-bound-20261028.md)
reuses all existing gap bounds exactly and audits 194,944 new task orders /
2,033,536 earliest-start steps. The complete recurrence excludes 7/8/0 and
7/9/0, leaving 444 candidates with all 4,576 original rows preserved. A direct
7/7/0 short14 construction passes original-shape readback: 91 pairs, 56 stock
edges and all 28 holes, with 0.225 mm minimum separation. Moving two inserts
from the first sheet leaves a valid63 alternative, missing brackets7/10/11;
the earlier valid64 is unchanged. One fixed49 probe closes after all eight
conservative bracket regions are empty, without claiming infeasibility. Next
reconstruct the first-sheet23-part packet with actual contact geometry and
changed cog phases/row structure; closed local calls stay closed. Main db26d120
has five passing jobs and its Windows check is live; wait for allsix before
pushing. Production, READMEs and upstream releases are unchanged. H2/H5 remain
open at 60%; all 22 reserved vectors remain unopened and no release qualifies.


**N4 cog topology checks, 2026-10-28:** [the evidence](../benchmarks/results/h5-cog-topology-source-checks-20261028.md) audits
2,592 new contact cases and one finite mixed-phase model. Its sole call returns
OPTIMAL at 278.84 mm pitch; all 31 incumbents and 105 original cog pairs pass,
but the packet is 47.819 mm too wide. A new aligned-row source58 passes, then
one bounded insertion sequence places one bracket and three inserts. Final
source62 passes 1,219 source pairs and all 78 holes; brackets8–11 remain
unplaced and the earlier valid64 is preserved. Both calls are closed, with no
native or global infeasibility claim; the necessary frontier remains 444.
Next allow independent mover positions or change the retained frame arrangement.
Main db26d120 passes all six CI jobs, permitting a normal guarded checkpoint
push. Sparrow6f7b9d35 changes only README/wordmark assets; the upstream stop rule
does not fire. Production, READMEs and upstream releases remain unchanged.
H2/H5 stay open at 60%, all 22 reserved vectors remain unopened, and no release
qualifies.


**N4 independent-coordinate source model, 2026-10-28:** [the evidence](../benchmarks/results/h5-independent-source-placement-20261028.md)
audits 77 source-conservative domains, 1,124 convex cells and 4,079 integer
halfplanes. All 23 remaining originals have independent coordinates; all
58,151 variables and 210,518 constraints are read back. The corrected source62
partial control passes original-ring and integer-cell checks; its earlier
buffer failure is retained. The sole60-second call closes UNKNOWN after
143,475 branches, with a retained0.151582-second returned soft overrun and no
assignment. No native or infeasibility claim follows; the valid64 and444-count
frontier remain unchanged. Next audit source-contained rectangles and necessary
cumulative sheet-capacity constraints in a new formulation; do not restart the
closed call. Main a23ee783 passes allsix jobs. Production, READMEs and upstream
heads/releases are unchanged. H2/H5 remain open at60%, all22 reserved vectors
remain unopened, and no release qualifies.


**N4 source capacity and core-height bound, 2026-10-28:** [the evidence](../benchmarks/results/h5-source-capacity-and-core-height-20261028.md)
verifies source-contained rectangles and adds necessary X/Y capacities without
changing the prior independent-position constraints. The sole call closes
UNKNOWN. A separate 29-part core-height call is FEASIBLE, with nine audited
incumbents, but lowers the core by only 0.017 mm. Original source43 passes 497
pairs and all 57 holes. An exact 214-pattern section-weight certificate covers
arbitrary positions and all quarter turns of the same 18-frame/11-insert core:
its top is at least 2,102.189571 mm, allowing at most another 5.443429 mm reduction.
Both calls stay closed, including their soft overruns; the invalid first audit
timer and corrected check are preserved. Next change the core composition using
the source-valid staggered arrangement and a new independent-coordinate model,
rebuilding owner-dependent geometry. The best valid64 and 444-count frontier
remain unchanged. Main d71c9c85 has five passing jobs and Windows live; wait for
all six before pushing. Production, READMEs and upstream releases are unchanged.
H2/H5 remain open at 60%; all 22 reserved vectors remain unopened and no release
qualifies.


**N4 changed-core independent placement, 2026-10-28:** [the evidence](../benchmarks/results/h5-staggered-core-independent-placement-20261028.md)
revalidates the staggered41 source core and a56-part cog control, rebuilds all
owner-dependent regions, and audits all25 mandatory movers /50 independent
coordinates. Necessary source-rectangle capacities bring the model to173,538
constraints. Its sole bounded call closes UNKNOWN; the0.076915s returned soft
overrun is retained. The saved control has no conservative bracket-insertion
region, which is not an actual/global exclusion. Next review and optimize the
26-part core composition itself (18 frames,3 brackets,5 inserts), with source
L geometry and the actual short15 preserved. Existing searches stay closed.
The best valid64,444-count frontier, H2 gate and22 unopened reserved vectors
remain unchanged. Main d71c9c85 now has allsix CI jobs passing; push verified
queued checkpoints after fresh guards. Production/READMEs and upstream releases
are unchanged. H2/H5 remain open at60%; no release qualifies.


**N4 mixed-core height and exact bounds, 2026-10-28:** [the evidence](../benchmarks/results/h5-mixed-core-height-and-section-bounds-20261028.md)
verifies a mixed 26-part core at 2,157.409 mm, 10.466 mm shorter, with all seven
source-valid incumbents preserved. The sole search stays closed, including its
0.047559 s returned soft overrun. Rebuilt cog-anchor area grows only about 0.20%.
Three independent exact section-weight certificates check 11,741 patterns.
Adding the two missing brackets to the old 18-frame/11-insert lower core requires
a top of at least 2,144.593263 mm, exceeding its old height by 36.943263 mm;
this excludes that core-only repair, not the full job. The current mixed26 core
has a 2,113.619939 mm lower bound; all first-sheet non-cogs under short6/9 need
at least 2,249.796028 mm. Next investigate an independently positioned cog packet
with a height objective and fully audited positive control, preserving all other
original obligations. Best valid64, 444 necessary counts, the H2 gate and 22
unopened reserved vectors stay unchanged. Main 2adfa569 has four passing CI jobs
and Ubuntu/Windows checks live; wait for all six before pushing. Production,
READMEs and upstream releases are unchanged. H2/H5 remain open at 60%.


**N4 independent cog-height result, 2026-10-28:** [the evidence](../benchmarks/results/h5-independent-cog-height-20261028.md) audits
all 15 independent cog positions, 13,051 variables, 48,046 constraints and the
complete positive control. The sole phase7 height call is CLOSED FEASIBLE;
all five incumbents pass original-source checks. Actual height is 772.202399 mm,
only 0.126980 mm shorter than the old valid64 cog packet, while width increases
by 41.066861 mm. The 0.258 mm model-top change includes 0.012 mm translation;
physical compression from the guarded control is 0.246 mm. Preserve the
0.057713 s returned soft overrun; no optimum or full66 claim follows. Next add
independent cog angles in a new direct-source formulation, with audited positive
control and one declared bounded call; never reuse phase7 obstacles at changed
angles. The other 51 originals remain required. Best valid64, 444 necessary
counts, H2 gate and 22 unopened reserved vectors stay unchanged. Main 2adfa569
has five passing jobs and Windows live; queued commits wait for all six before
normal push. Production/READMEs and upstream releases are unchanged. H2/H5
remain open at 60%; no release qualifies.
