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
