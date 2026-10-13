# Nestbolt v1.1: real shop files — plan for an agent

*Written 2026-10-13 for Artem, after v1 closed on his acceptance (plan decision 5). Hand this whole file to the agent
that does the work. Read [PLAN.md](PLAN.md) (v1 plan, ground rules), [STATUS.md](STATUS.md) and
[BENCHMARKS.md](../BENCHMARKS.md) first.*

## 1. Goal

v1 nests well on clean, frozen benchmark files. v1.1 makes Nestbolt work on the files people actually bring from the
shop: messy DXFs from Fusion 360, LightBurn and other CAD/CAM tools. It adds the three features laser and plasma users
ask for most, and closes the browser's known gap on curve-heavy parts.

In priority order:
1. **A messy-file corpus** (data first): real and realistically broken DXF/SVG files, with every licence recorded and
   the expected result labelled by hand.
2. **Import robustness** on that corpus: gaps, duplicates, layers and colours, open contours, units.
3. **LightBurn `.lbrn2` round-trip:** open a LightBurn project, nest it, and write it back with every layer and cut
   setting intact.
4. **Curve-heavy parts in the browser:** today the WebAssembly build is 16-30% worse than native on the detailed-gear
   jobs in one worker (G5 report).
5. **Common-line cutting:** parts sharing a straight edge are cut once (deepnest-next has this as `mergeLines`).
6. **Lead-ins:** decide the scope first (section 4.6). Most of this belongs to CAM, so the likely slice is reserving
   room for lead-ins and exporting them on their own layer.

**Why this order.** Most real-world failures happen at import, before nesting starts, and v1's fidelity corpus
(196 drawings, mostly generated boxes.py files) is clean. The corpus feeds every later workstream. LightBurn is the
largest maker laser community, and a round-trip that keeps cut settings removes the main reason to stay in LightBurn's
own nesting (Quick Nest is bounding boxes only; True Nest is in 2.2 early access and Pro-only). The browser curve gap is
measured and known. Common-line is parity with deepnest-next. Lead-ins mostly belong to the CAM tool.

## 2. Starting point (what exists, 2026-10-13)

- **Import** (`crates/core/src/import.rs`) handles SVG and DXF lines, arcs, ellipses, Béziers, B-splines, blocks,
  transforms and units. It converts to mm, chains open runs whose ends meet within the tolerance (default 0.005 mm),
  repairs self-touching outlines with a warning, and records each part's source element, layer or block as
  information. It cannot choose which layers or colours are cut, and it does not heal larger gaps.
- **Export** writes one SVG and one DXF per sheet from the original curves, transformed. G6 fidelity: 196 drawings,
  within 0.0005 mm (SVG) and 0.0000045 mm (DXF). Inkscape and LibreCAD open the exports, and Artem checked five
  imports in LightBurn 2.1.01 by hand.
- **Independent validator** (`crates/validator`, Clipper2): overlap, clearance, containment, transforms, quantities and
  units. It rejects touching parts whenever clearance > 0; a v1 "exact spacing" variant failed on exactly this
  (BENCHMARKS.md).
- **Surfaces:** CLI, browser app (WebAssembly in workers, Pages), MCP server (five tools). v1's rule G7 holds here too:
  every feature works through the UI, the CLI and the MCP tools, each with an end-to-end test.
- **Benchmarks:** the final v1 results (build `75cbb32`) are published and accepted. The held-out jobs are spent.

## 3. Ground rules (carried over from PLAN.md section 8, plus these)

- **Licences:**
  - Every dataset file needs a recorded licence and source (as in `benchmarks/datasets`). Use CC0, CC-BY, CC-BY-SA,
    MIT, BSD, Apache or public domain only; anything NC/ND, or with an unclear licence, needs Artem's explicit OK.
  - Keep MIT/MPL notices for any reused code; credit sparrow and jagua-rs.
- **No closed-tool reverse engineering:** never decompile LightBurn, Fusion or anything else. Learn the `.lbrn2`
  format only from:
  - files LightBurn writes (Artem makes them);
  - public documentation and forum descriptions;
  - openly licensed parsers, with their licence respected and noted.
- **No accounts, logins, paid tools or geometry uploads:**
  - The agent never signs up anywhere.
  - Download only files that need no login.
  - Fusion 360 and LightBurn files come from Artem.
  - Users' geometry never leaves their device.
- **Benchmark discipline is unchanged:**
  - BENCHMARKS.md is append-only.
  - Runs go on CCD0, one per physical core, at most 8 at once; builds use `output/ccd1.py`.
  - Never edit `crates/` or the batch scripts while a benchmark runs: the harness hashes its sources and refuses to
    record.
  - Python edits always pass `encoding='utf-8'` and a line-feed `newline` (the Windows default is cp1252).
- **Claims:**
  - The README claims nothing beyond the results page.
  - Solver changes here (sections 4.4 and 4.5) do not change the published v1 numbers.
  - A new quality claim needs a new final run with a fresh held-out set and fresh seeds, and only Artem starts one.
- **Release and registry** publication happen only on Artem's explicit instruction.
- **Progress** is reported only as completed milestone weights (section 6); a milestone counts once its gate has direct
  evidence.

## 4. Workstreams

### 4.1 N0: the messy-file corpus (data first)

**Sources (verify each licence before downloading):**
- ezdxf's test and example files (MIT): many DXF versions and entity types.
- KiCad demo projects' board outlines, exported locally with `kicad-cli pcb export dxf`: arcs and segments that do not
  chain in order. Check each project's licence.
- Openly licensed laser-cut designs (CC0/CC-BY/CC-BY-SA) that download without an account: Wikimedia Commons,
  OpenBuilds, Printables or Thingiverse items with such licences.
- LibreCAD, QCAD and FreeCAD sample drawings, where their licences allow it.
- **Artem's own files:** 10-20 real exports from his Fusion 360 and LightBurn use (ask him). Keep them out of the
  public repo unless he says otherwise: a gitignored `private/` folder, with only summaries published.
- **A deterministic, seeded "shop habits" generator** that damages clean drawings in documented ways. Record each habit
  with the public source that describes it:
  - polylines exploded into one LINE per edge, with shuffled order and reversed directions;
  - gaps and overlaps of 0.001-0.5 mm; duplicate and zero-length segments;
  - Fusion-style SPLINEs (degree 3, fit points only, many knots); LWPOLYLINE bulges and widths;
  - nested blocks with mirroring and non-uniform scale;
  - inch geometry with `$INSUNITS` missing;
  - TEXT, MTEXT, DIMENSION, HATCH and construction lines on other layers;
  - LightBurn-style colour-per-operation layers (cut, score, engrave);
  - a whole existing layout exported with its sheet outline.

**Ground truth:**
- For every file, a small JSON next to it: expected cut parts, holes per part, which layers or colours are cut, outer
  bounding sizes, and any expected warning.
- Write these by hand for real files; the generator writes them for generated files.

**Freeze:** checksums plus a manifest, as v1's datasets. Hold out 20% of the real (non-generated) files, never used
for tuning.

**Gate H1:** all of these:
- at least 150 files, at least 40 of them real exports from at least 5 distinct sources, including Fusion- and
  LightBurn-written DXF;
- every licence recorded;
- ground truth for every file;
- frozen and checksummed;
- the held-out split recorded before any import work starts.

### 4.2 N1: import robustness

- **Gap healing:**
  - Keep the 0.005 mm default join.
  - Offer "close gaps up to X mm" (UI field, CLI `--close-gaps`, MCP parameter), which reports each closed gap's
    location and size.
  - Never close silently beyond the default.
- **Clean-up:**
  - Remove exact duplicate and zero-length segments, and merge overlapping collinear pieces before chaining.
  - Report self-intersections clearly, or repair them where unambiguous (v1 already repairs self-touching outlines).
- **Layers and colours:**
  - The import report lists every layer and colour with its entity count.
  - The user chooses which ones are cut (UI checkboxes, CLI `--layers`/`--colors`, MCP parameter).
  - Default: layers whose names look like cut or outline layers if any exist, otherwise every closed contour.
  - TEXT, DIMENSION and HATCH entities are ignored, with a warning.
- **Open contours:** list each one with its location and gap size; suggest the closing tolerance that would fix it.
- **Units:** when `$INSUNITS` is missing and the sizes look like inches, warn and offer inches. Never rescale silently.
- **Pre-arranged layouts:** a file that is already a nested sheet (sheet outline plus parts) imports as parts. The
  outline can optionally be used as the sheet (v1 already supports remnant outlines).

**Gate H2:** on the frozen corpus:
- every non-held-out file either imports exactly to its ground truth (parts, holes, cut layers) or fails with a message
  that names the fix;
- at least 95% of the held-out real files import exactly, and the rest fail clearly;
- no crash or hang under fuzzing (extend `crates/core/tests/search_fuzz.rs` and the importer property tests with the
  generator's habits);
- exported outlines stay within 0.01 mm of the imports (G6 method, `scripts/g6_fidelity.py`);
- UI, CLI and MCP parity, with end-to-end tests.

### 4.3 N2: LightBurn `.lbrn2` round-trip

- **Learn the format** from projects Artem saves in LightBurn 2.1:
  - a small set covering rectangles, ellipses, paths with Bézier segments, groups, text, an image, several layers and
    cut settings, and a few shapes with rotation and mirroring;
  - write down what was learned in `docs/LBRN2.md`, with which file showed each point;
  - check for an openly licensed parser before writing one.
- **Import:**
  - Read closed vector shapes with their transforms (`XForm`) and their layer (cut setting index).
  - Text, images and fills either ride with the closed shape they sit inside (a rigid group) or are placed as a block
    by their outline. Ask Artem which he wants.
- **Export:**
  - Write the same document back, changing only the transforms of moved shapes.
  - Optionally add sheet outlines on a dedicated layer.
  - Preserve everything else, including unknown elements and attributes: cut settings, notes, ordering.
  - Several sheets go side by side in one project, or one file each; ask Artem.
- **Gate H3:**
  - automated tests: parse then write with no changes gives an XML-equivalent file; nest then write changes only
    transforms;
  - the placed geometry passes the independent validator;
  - Artem opens at least 5 nested projects in LightBurn and confirms positions, layers and cut settings, recorded like
    v1's LightBurn check;
  - UI, CLI and MCP support, with end-to-end tests.

### 4.4 N3: curve-heavy parts in the browser

- **Baseline:**
  - Define a curve-heavy development subset: gears, signs and letters from set M (never the v1 held-out jobs), plus new
    curve-heavy examples.
  - Measure native vs WebAssembly at 60 s and the time per collision check by vertex count.
- **Levers, measured one at a time** and logged in BENCHMARKS.md, kept or rejected on evidence:
  - error-bounded, outward-only simplification of collision proxies with a vertex budget per part (exports keep the
    exact curves);
  - adaptive flattening tolerance;
  - per-orientation proxy caching;
  - WebAssembly SIMD;
  - worker-count heuristics within the 1.5 GB memory cap.
- **Constraints:**
  - No WebAssembly threads: GitHub Pages cannot send COOP/COEP headers (PLAN.md section 3).
  - A v1 trial with a simplified Sparrow model was rejected because marques no longer fit (BENCHMARKS.md). Any
    simplification must pass the validator and must not lose a job that fit before.
- **Gate H4:**
  - on the curve-heavy subset, the browser at 60 s with default workers is within 2% material of native at 60 s,
    median over 3 development seeds;
  - a 2,000-curve file imports and shows its first layout with no main-thread task over 200 ms, and peak memory stays
    under 1.5 GB;
  - the G5 quality set does not regress beyond noise;
  - the native development matrix stays within 0.5% of its median.

### 4.5 N4: common-line cutting

What it is: parts placed with zero gap along straight edges share one cut. deepnest-next implements it as
`mergeLines`: the merged collinear length times a time ratio is subtracted from the placement fitness, and merged
segments appear in the export.

1. **Export:**
   - Detect collinear, overlapping segments between neighbouring parts, with a tolerance tied to the curve tolerance.
   - Write a "cut paths" layer in which shared segments appear once, and keep the full per-part outlines on another
     layer for CAM tools that compensate kerf per contour.
   - Report the total cut length before and after.
2. **Validator mode:**
   - Allow zero-gap contact along edges while rejecting any overlap area.
   - Clearance is 0 in this mode; the kerf is the cutter's job.
   - The validator's touch handling must stay a separate, tested code path.
3. **Search preference:**
   - An optional bonus for merged length in the placement cost, off by default.
   - Measure the trade-off between material and cut length.

**Gate H5:**
- on rectangle- and bracket-heavy development jobs, the cut length falls by a margin set from the first measurements
  (start the bar at 15%, adjust once measured, record the decision), with material within 1% of normal mode;
- exports open in Inkscape, LibreCAD and LightBurn with each shared line present once and no gaps;
- compared on the same jobs with deepnest-next's `mergeLines`, run locally at its pinned revision;
- UI, CLI and MCP support, with end-to-end tests.

### 4.6 N5: lead-ins (decide scope first)

- **First, a one-page memo** for Artem:
  - who needs lead-ins from a nester (plasma and waterjet more than diode or CO2 lasers);
  - what the usual CAM tools already do (SheetCam, LightBurn's own cut settings, controller software);
  - what Nestbolt would have to provide.
- **Likely slice:**
  - a per-part lead-in allowance: a line or arc footprint of length L at a chosen corner or edge, inside holes and
    outside outlines;
  - the footprint is added to the collision geometry, so a lead-in never crosses a neighbour or the sheet margin;
  - lead-ins are exported on their own layer.
  - Cut order and pierce sequencing stay out of scope (CAM).
- **Gate H6** (only if Artem approves the slice):
  - the validator checks the lead-in footprints;
  - exports open in LightBurn and LibreCAD;
  - the material cost of the allowance is reported;
  - UI, CLI and MCP support.

## 5. Sequencing

N0 → N1 → then N2 and N3 in parallel → N4 → N5.

- N2 depends on Artem's sample projects, so ask for them on day one.
- N3 and N4 change the solver: run the development matrix after each kept change.
- Do not overlap benchmark runs with source edits.

## 6. Milestones (progress weights)

| # | Milestone | Weight | Done when |
|---|---|---:|---|
| N0 | Messy-file corpus | 15% | H1 |
| N1 | Import robustness | 25% | H2 |
| N2 | LightBurn round-trip | 25% | H3, including Artem's manual check |
| N3 | Curve-heavy browser | 15% | H4 |
| N4 | Common-line cutting | 15% | H5 |
| N5 | Lead-ins | 5% | Artem's scope decision recorded, and H6 if he approves the slice |

## 7. What the agent needs from Artem

1. 10-20 of his own Fusion 360 and LightBurn exports, and whether they may be published or stay private.
2. LightBurn 2.1 sample projects (list in section 4.3), and later a manual check of at least 5 nested projects.
3. Two LightBurn choices: how text and images should move, and whether sheets come as one file or one each.
4. The lead-in scope decision, after the memo.
5. Whether common-line's search bonus may become a default, once measured.

## 8. Risks

- **The `.lbrn2` format is undocumented and may change between LightBurn versions.** Preserve unknown content verbatim
  and test on files from the version Artem uses.
- **Licences of shop files are often unclear.** Exclude rather than guess.
- **Zero-gap validation can weaken the validator.** Keep the strict mode as the default, give the touch mode its own
  tests, and never use it to score benchmarks.
- **Proxy simplification has failed once before.** Measure each lever against the validator and the "nothing that fit
  before stops fitting" rule.
- **Scope creep into CAM.** Lead-ins stay a reserved-space feature unless Artem decides otherwise.
