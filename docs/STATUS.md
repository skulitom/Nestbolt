# Status — 2026-10-13

## v1.1 — real shop files

**Completion: 15%.** The goal is active under [PLAN_V1_1.md](PLAN_V1_1.md).
Only completed gate weights count. N0/H1 is complete: the labelled corpus and
writer-stratified held-out allocation are frozen. N1 implementation is in progress;
explicit gap repair, layer/colour selection, segment cleanup, byte decoding,
units reports, rejection of incomplete selected cuts and the locally verified
export palette and imported stock outlines now work through the UI, CLI and MCP.
No N1 importer changes may precede the H1 freeze. LightBurn-dependent evidence is
due by 2026-11-06. Release and registry publication still require Artem's instruction.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| N0 — Messy-file corpus | 15% | **H1 complete.** [Frozen corpus and split](../benchmarks/results/h1-freeze-20261013.md): 534 inputs, 338 labels, 148 renders, 1,181 attributed/checksummed files; 15 real + 10 native held out with lineage isolation |
| N1 — Import robustness | 25% | In progress: [incomplete-drawing checkpoint](../benchmarks/results/h2-completeness-checkpoint-20261013.md) across three surfaces; 245/257 training vectors match counts, 11 reject with repair instructions (including all nine negatives), the single frozen-label count discrepancy now has an approved, hash-scoped scoring exception (246 reviewed matches). Robustness 183/183 without crash/timeout. [Ten native exports and palette](../benchmarks/results/h2-lightburn-20261013T195848Z.md): saved dimensions within 0.000033 mm; eight exact rounded UI sizes, two spline display differences retained. [Cut layers](../benchmarks/results/h2-cut-layer-audit-20261013.json) match all 246 prior imports; [full vector fidelity sweep](../benchmarks/results/h2-fidelity-20261013T202338Z.md): 239 pass, 11 reject, four time out and three error; [closed-path repair](../benchmarks/results/h2-closed-retrace-checkpoint-20261013.md) now passes the ARC SVG/DXF rerun, with four timeouts and two nesting errors still open. [Imported stock outlines](../benchmarks/results/h2-sheet-checkpoint-20261013.md) work across all surfaces; all ten labelled pre-arranged nests match their stock geometry. Full fidelity, warning coverage, fuzz and native-project support remain pending. Two held-out negatives cap literal success at 92%; the held-out denominator clarification remains pending, with split unchanged |
| N2 — LightBurn round-trip | 25% | [Local probes](LBRN2.md) establish origins, shared geometry/bitmaps, text, leads, StartV and layer sub-settings. Reader/writer and H3 pending |
| N3 — Curve-heavy browser | 15% | Pending; H4 requires measured browser/native quality and scale. Native export preparation also exposed a dense legacy two-copy job exceeding a 20 s cooperative limit and 90 s external limit; the unchanged workload completes in 117–126 s with longer limits. Startup/deadline handling remains open |
| N4 — Common-line cutting | 15% | Pending; H5 requires compensated geometry, savings and surface evidence |
| N5 — Lead-in allowances | 5% | Pending; H6 requires footprint validation, start points and surface evidence |

## v1 — accepted

**Completion: 100% on Artem's acceptance (plan decision 5, 2026-10-13).** M0-M4 met their gates. M5 closed when Artem accepted the published final run: G1, G3, G4 and G2 at 300 s are met; G2 at 60 s is not met as written (85.7% wins or ties against the 90% required, two jobs more than 1% worse, every loss against Sparrow).
Percentages count completed milestones only. Development results do not establish the final acceptance gates. All failures and earlier trials remain in
[BENCHMARKS.md](../BENCHMARKS.md). The ten held-out maker jobs were used once, in the final acceptance run, and never for tuning.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| M0 — Groundwork and reproduction | 5% | Complete: 39 valid runs; all 13 means within the frozen 1% threshold |
| M1 — Baseline | 15% | Complete: all 1,878 declared slots audited; [target frozen at 10.77231474%](M1_BASELINE.md) |
| M2 — Sheet optimiser | 25% | Complete: [development matrix](../benchmarks/results/sheets-m2-60s-s0-20261012T144634Z-10b9520f.md) 225/225 valid at 60 s and 300 s; G3 strip parity median −0.039%, worst +1.65%; G4 8/9 (88.9%). 60 s medians: 48/52 wins/ties, median 8.44% (G2 is M5) |
| M3 — Part-in-part and import/export | 15% | Complete: [fidelity](../benchmarks/results/g6-fidelity-20261012T161009Z-310d54b1.md) on 196 real drawings within 0.0005 mm, curves kept, mm and inch correct; Inkscape and LibreCAD open the exports; [LightBurn 2.1.01](../benchmarks/results/g6-lightburn-20261012T170036Z.md) imports all five at the exact placed sizes |
| M4 — Browser app and MCP | 20% | Complete: [Pages app](https://skulitom.github.io/Nestbolt/) with five examples and a live view; G5 [quality](../benchmarks/results/g5-browser-60s-s0-20261012T182218Z-032f0985.md) (WebAssembly vs native at 60 s on 65 jobs: median +0.02% Chrome 154, +0.07% Firefox 157, total +0.9%), [scale and responsiveness](../benchmarks/results/g5-scale-20261012T192645Z-39d0cca0.md) (2,000 parts imported, nested and exported, peak 1.05/1.16 GB, longest task 106 ms), hosting re-checked live; G7 real Claude Code run, CLI and UI end-to-end tests for every v1 item, MCPB and `mcp-publisher` validation in a [release dry run](https://github.com/skulitom/Nestbolt/actions/runs/38300373491) |
| M5 — Final gates | 20% | **Closed on Artem's acceptance (decision 5); G2 at 60 s not met as written.** [Final acceptance run](https://skulitom.github.io/Nestbolt/results/) (2026-10-13, seeds 1000-1004, held-out jobs, build `75cbb32`): G1 every layout valid (375/375 at 60 s, 60/60 at 300 s, 60/60 at 30 s, 65/65 strips); G2 at 300 s met (median 9.61%, 11/11, worst +0.84%); G2 at 60 s median 8.52% but 48/56 wins or ties (85.7%) and two jobs more than 1% worse (m-garment-bruce-1 −2.37%, b-jakobs1-strip-sheet −2.09%), all eight losses against Sparrow, seven on one-sheet jobs Nestbolt delegates to Sparrow; G3 median −0.002%, worst +0.72%; G4 10/11; G8 one command and the results page from those records. The first final run (`484ce8b`) crashed on one job (G1); [its page](https://skulitom.github.io/Nestbolt/results/final-484ce8b/) stays published |

| Evidence | Current result | Next step |
| --- | --- | --- |
| Published Sparrow reproduction | 39/39 layouts valid; 13/13 instance means pass; worst absolute difference 0.986671% | [Final proof](../benchmarks/results/m0-published-20261011T215820Z-10a30c6f.md) |
| Frozen datasets | 13 strip, 35 sheet, 40 maker jobs; 10 maker jobs held out | Use only development cases for tuning |
| LBF development matrix | 450/450 attempts; 283 valid, 5 invalid, 162 unsupported | Complete; [table](../benchmarks/results/comparison-session-20261011T221209Z-ce35672e.md) |
| SVGnest | All 450 development slots complete. At 60 s: sheets 103/105 identical and 85/105 expanded valid; makers 1/90 identical and 0/90 expanded. At 300 s: sheets 18/18 and 15/18; makers 3/12 and 0/12 | [Final expanded sheet table](../benchmarks/results/comparison-batches-20261012T021336Z-74941dfd.md), [final expanded maker table](../benchmarks/results/comparison-batches-20261012T023246Z-a5cc0290.md); no further development runs |
| Deepnest | All 450 development slots complete: 330 valid, 30 invalid, 88 no layout, two timeouts. At 300 s: both sheet settings 18/18 valid; makers identical 4/12, clearance-safe 9/12 | [Final maker identical](../benchmarks/results/comparison-batches-20261012T032935Z-846373a4.md), [clearance-safe](../benchmarks/results/comparison-batches-20261012T033500Z-e03868ab.md) |
| Current Sparrow | All 528 development slots accounted for: 127 valid, 43 invalid, 358 unsupported; both settings, both budgets, three seeds | [Complete coverage](../benchmarks/results/sparrow-development-20261012T0048.md); final-seed comparisons remain for M5 |
| Nestbolt search | All 65 development layouts valid. Repeated compression improves one sheet score (1.69%) and four maker scores (up to 0.30%) over v13, with zero regressions. Skipping unsuccessful repeats preserves every score | [35 sheets](../benchmarks/results/repack-sheet-20261012T035142Z-a7b22154.md), [30 makers](../benchmarks/results/repack-maker-20261012T035142Z-54130739.md); fixed-work diagnostics, no equal-time gate |
| Longer search | Up to 1,024 passes, preserving the first finished 64-pass block. A four-job 512-pass pilot improves Jakobs1 by 2.46% and Marques by 4.20%; the other two retain their 64-pass result | [All four cases](../benchmarks/results/progressive-pilot-20261012T0433.md); 80M query allowance and 60 s safety deadline, selected cases with extra work |
| Placement diversity | Combining original and varied placement strategies reduces Blaz1 from 12 sheets to 10 (16.28% less material), improves Bruce by 2.99%, and retains the preceding Jakobs1 and Marques scores. All four layouts independently valid | [Four-case evidence and rejected trial](../benchmarks/results/placement-diversity-20261012T045248Z.md); up to 1,024 passes, same 80M-query/60 s controls; broaden development coverage next |
| Repair collisions | The first broad run had two invalid late repairs (Shapes0/Shapes1, nearly coincident parts), caught by the independent checker before export. Repair now unions interior-pole and polygon collisions; both exact fixtures pass and replay identically | [Regression evidence](../benchmarks/results/repair-pole-collisions-20261012T052215Z.md); [original failures](../benchmarks/results/search-coverage-20261012T050634Z.md) retained |
| Native strip parity | 39/39 outputs valid at 60 s, seeds 0/1/2. Median regression −0.0390%; worst +1.6493%, against the better Sparrow setting per job. Development thresholds pass | [Audited comparison](../benchmarks/results/strip-development-20261012T040418Z-961c9a96.md), [adapter scope](STRIP_PARITY.md); final-seed G3 acceptance remains |
| Repeatability and rollback | Two compression replays have identical complete outputs. Tests preserve the full repacking history, other sheets and the valid incumbent when interrupted | [Compression replay](../benchmarks/results/compression-replay-20261012T0326.json); previous [blaz1 repair replay](../benchmarks/results/shallow-replay-20261012T0255.json) |
| Quality triage | Combined search on all 65 development jobs (seed 0, up to 1,024 passes / 80M queries / 60 s): 65/65 valid; vs 52 finite 60 s competitor medians 27 wins/ties, 15 more than 1% worse, median reduction 0.396716%. Thirteen jobs have no finite competitor | [Corrected coverage](../benchmarks/results/search-coverage-20261012T051749Z.md); the frozen G2 target is 10.77231474%, so sheet search needs a much stronger separator |
| Sheet separator | `nestbolt sheets`: warm start, then the last twelve sheets as one walled strip; the last sheet's free end is a pinned blocker (several sheets) or a shrinking container (one sheet). Three development seeds, 60 s, pinned CPUs: 195/195 valid; per-job median 48/52 wins/ties (92.3%); one job more than 1% worse (jakobs1 strip-sheet, -1.7%); median reduction **8.2619%** | [Seed 0](../benchmarks/results/sheets-eval-fixed-s0-20261012T125826Z-fd1af61e.md), [1](../benchmarks/results/sheets-eval-fixed-s1-20261012T130725Z-ece55c03.md), [2](../benchmarks/results/sheets-eval-fixed-s2-20261012T131624Z-24a17328.md); all earlier and interrupted batches in BENCHMARKS.md. All four losses are single-sheet jobs where Sparrow leads |
| Speed (G4-style) | 30 s runs vs the frozen 300 s competitor medians, three seeds, with the rectangle warm start: 195/195 valid; **8 of the 9** jobs with a finite 300 s median reached (88.9%); m-box-mini ties at 0.6660, jakobs2 strip-sheet misses by 2.7% | [Seed 0](../benchmarks/results/sheets-ab-rects-30s-s0-20261012T142836Z-c9d2a6d1.md), [1](../benchmarks/results/sheets-ab-rects-30s-s1-20261012T143305Z-524036e1.md), [2](../benchmarks/results/sheets-ab-rects-30s-s2-20261012T143733Z-7272c8c3.md); previous build 7/9 |
| Browser app | Same engine in WebAssembly Web Workers, several seeds in parallel; five bundled examples, live view of the best layout, offcut and bounding box per sheet; import, nest, export, defects, remnant outlines, several sheet sizes, fill modes, IndexedDB and ZIP projects | 22 Playwright tests (11 × Chromium and Firefox) in CI; [G5 quality](../benchmarks/results/g5-browser-60s-s0-20261012T182218Z-032f0985.md) and [scale](../benchmarks/results/g5-scale-20261012T192645Z-39d0cca0.md) pass; the four detailed-gear jobs remain 16-30% worse in one browser worker (half the native search rate) |
| MCP server and packaging | Five tools, workspace confinement, no overwrites, repeatable work budgets; end-to-end stdio test. JSON Schemas for library, request and report. MCPB bundle, native archives and release/registry workflows (dispatch or tag only) | 20 Node packaging tests pass, including a real bundle import-nest-validate smoke test; nothing released |
| Export fidelity (G6) | 196 drawings (fixtures, example parts, 192 boxes.py examples): imported, nested, exported to SVG and DXF and re-imported; 29,308 contours, none unmatched, largest distance 0.0005 mm (SVG) and 0.0000045 mm (DXF) | [Passing report](../benchmarks/results/g6-fidelity-20261012T161009Z-310d54b1.md); `python scripts/g6_fidelity.py`. It found and fixed self-touching boxes.py outlines, DXF chaining and single-precision collisions |
| Export opening (G6) | Fidelity fixtures (mm SVG with arcs, ellipses and Béziers; inch DXF with bulges, holes and arcs) nested and exported; Inkscape 1.4.4 (SVG and DXF) and LibreCAD 2.2.1.5 (DXF) report the placed drawing size within 0.04-0.27 mm | [Passing report](../benchmarks/results/g6-open-20261012T144206Z-4e0d95be.md); two earlier method failures retained; `python scripts/g6_open_check.py` |
| Real MCP client (G7) | Claude Code 2.1.280, `claude -p --mcp-config <file> --strict-mcp-config`, Nestbolt tools only: lists the tools, imports an SVG, nests with a 10 s budget, exports; the independent validator accepts the layout | [Passing report](../benchmarks/results/g7-claude-20261012T145002Z-3180a8d5.md); two earlier attempts retained; `python scripts/g7_claude.py` |
| Search limits | 1,000-part job returns a valid incumbent in 15.094 s under a 15 s cooperative deadline; two fixed-work replays produce identical results | [Stop and replay evidence](../benchmarks/results/search-control-20261012T0114.md); calibrate time-to-work mapping and wire browser/MCP cancellation |
| Compaction | All 65 layouts valid; seven sheet and ten maker improvements retained. Bounded relocation preserves every material score and reduces collision queries by 24% overall; original-geometry guard prevents material regression | [Sheet trial](../benchmarks/results/compact-b-20261012T013650Z-e3423fac.md), [maker trial](../benchmarks/results/compact-m-20261012T013654Z-fb5e8bfa.md); remains optional while stronger sheet repair is developed |
| Constructor speed diagnostic | Stable cost order cuts 1,000-part collision checks from 9.33M to 4.39M; last matched-CPU pair uses 61.8% less CPU time with identical output | [All ten timing attempts](../benchmarks/results/construct-profile-20261012T0042.md); four-circle experiment reverted; no G4 claim |
| Independent checker speed | Reusing clearance outlines cuts validation CPU by a further 17.0% on the gear job and 13.8% on the 1,000-part job. Full-search outputs and all 104 retained validation reports remain identical | [Reuse timings](../benchmarks/results/clearance-cache-20261012T0433.md), [preceding distance-pruning trial](../benchmarks/results/validator-speed-20261012T0420.md); no G4 claim |
| Repository and hosted checks | [Public repository](https://github.com/skulitom/Nestbolt) since 2026-10-12, Pages live | Release dry run passes; no release or registry listing published (Artem decides) |

The [complete baseline audit](../benchmarks/results/baseline-gap-20261012T033547Z-e9539412.md)
measures competitor reductions over LBF of **17.09% at 60 s** and **21.54% at 300 s**.
The target frozen from it (10.77231474%) was waived by Artem on 2026-10-12
([plan decision 4](PLAN.md)); the G2 median condition is the base 5%.
Missing finite comparisons remain explicit and never earn free wins.

Final acceptance (2026-10-13). The competitors ran first (Deepnest 870/870 slots,
SVGnest 870/870, Sparrow 1,000/1,000; one Deepnest harness fault before solving was
replaced and logged). Nestbolt's frozen `484ce8b` then crashed on b-albano-strip-sheet
(seed 1004, 60 s): a repacking trial its own check rejected was treated as fatal. The
fix (`75cbb32`, regression test) was frozen before any G2 number of the final run was
seen, and Nestbolt's final run was repeated in full against the same competitor
records. Both runs are published. G2 at 60 s is not met by either, with every loss
against Sparrow: on seven one-sheet jobs Nestbolt hands Sparrow's own problem to
Sparrow after its first layout, so Sparrow runs with slightly less time. Further
tuning against these results would use the held-out jobs, which the plan forbids. On
2026-10-13 Artem accepted the results as published (plan decision 5), which closes M5.
Next work is in [PLAN_V1_1.md](PLAN_V1_1.md); any new benchmark claim needs a new final
run with a fresh held-out set.

[Ties, failure coverage and the baseline-gap formula](../benchmarks/STATISTICS.md)
are now explicit. No competitor result means no free win. The [verified 10.6417% single-seed gap](../benchmarks/results/pilot-gap-feedback-20261011.md)
is superseded by the complete three-seed M1 audit. Both 60 s and 300 s G2
populations must pass separately.

The independent checker covers original geometry, spacing, quantities, units,
stock, margins, defects, rotations, mirroring and fill mode. The latest full local
checks passed 112 workspace tests, four stock-helper tests, both WASM builds,
source/schema/notices checks, 94 Python tests, 20 Node packaging tests and the
6 browser tests (3 each in Chromium and Firefox). Five Node tests cover CPU
selection and native process cleanup.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered. No release or registry listing has been published.
