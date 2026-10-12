# Status — 2026-10-12

**Completion: 5%. M0 is complete; M1 and M2 are in progress.**
Percentages count completed milestones only. Constructor results show valid starting layouts; competitor pilots do not yet
establish the final comparison. All failures and earlier trials remain in
[BENCHMARKS.md](../BENCHMARKS.md). Ten held-out maker jobs remain unused for tuning.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| M0 — Groundwork and reproduction | 5% | Complete: 39 valid runs; all 13 means within the frozen 1% threshold |
| M1 — Baseline | 15% | Validator and datasets complete; finish competitor seeds/settings and gap table |
| M2 — Sheet optimiser | 25% | All 30 development maker jobs construct validly; first sheet-removal repair works; improve large-job speed and quality |
| M3 — Part-in-part and import/export | 15% | Pending; original curves already retained in maker sources |
| M4 — Browser app and MCP | 20% | Scaffolding; five tools and actual Claude Code connection still to build |
| M5 — Final gates | 20% | Pending; all G1–G8 requirements remain in scope |

| Evidence | Current result | Next step |
| --- | --- | --- |
| Published Sparrow reproduction | 39/39 layouts valid; 13/13 instance means pass; worst absolute difference 0.986671% | [Final proof](../benchmarks/results/m0-published-20261011T215820Z-10a30c6f.md) |
| Frozen datasets | 13 strip, 35 sheet, 40 maker jobs; 10 maker jobs held out | Use only development cases for tuning |
| LBF development matrix | 450/450 attempts; 283 valid, 5 invalid, 162 unsupported | Complete; [table](../benchmarks/results/comparison-session-20261011T221209Z-ce35672e.md) |
| SVGnest | All 390 development 60 s slots complete. Sheets: identical 103/105 valid, expanded 85/105. Makers: identical 1/90, expanded 0/90; no finite maker medians | [Maker identical](../benchmarks/results/comparison-batches-20261012T011701Z-1f75fdda.md), [maker expanded](../benchmarks/results/comparison-batches-20261012T011902Z-36acd6a5.md); 300 s comparisons underway |
| Deepnest | 60 s / identical: 105/105 sheet attempts valid; 35 finite job medians. One audited post-budget cleanup failure replaced, original retained | [Three-seed table](../benchmarks/results/comparison-batches-20261012T011909Z-96b6f188.md); expanded settings and maker seeds underway; long budgets pending |
| Current Sparrow | All 528 development slots accounted for: 127 valid, 43 invalid, 358 unsupported; both settings, both budgets, three seeds | [Complete coverage](../benchmarks/results/sparrow-development-20261012T0048.md); final-seed comparisons remain for M5 |
| Nestbolt constructor | 30/30 valid; v3 has exactly the v2 layouts; median 0.453 s, slowest 15.563 s | [Current proof](../benchmarks/results/construct-maker-20261011T230206Z-b7a21810.md); improve material use |
| Nestbolt refinement | Three-method comparison: 30/30 valid; 22 improve, eight unchanged vs constructor; slowest 56.718 s | [Trial](../benchmarks/results/repack-maker-20261011T233725Z-c0e36d78.md); improve large-job speed |
| Nestbolt repair | 35/35 sheet and 30/30 maker jobs valid. All 64 comparable layouts exactly preserved; previously timed-out 1,000-part job now finishes in 40.1 s | [Sheet trial](../benchmarks/results/repack-sheet-20261012T003957Z-29681a27.md), [maker trial](../benchmarks/results/repack-maker-20261012T003947Z-73f9cdbc.md); improve quality |
| Search limits | 1,000-part job returns a valid incumbent in 15.094 s under a 15 s cooperative deadline; two fixed-work replays produce identical results | [Stop and replay evidence](../benchmarks/results/search-control-20261012T0114.md); calibrate time-to-work mapping and wire browser/MCP cancellation |
| Compaction | All 65 saved layouts remain valid. Relocation improves seven sheet and ten maker jobs, with no observed regressions; largest maker reduction 2.65% | [Sheet trial](../benchmarks/results/compact-b-20261012T012839Z-c2a42aba.md), [maker trial](../benchmarks/results/compact-m-20261012T012843Z-dac4bd32.md); reduce its 33 s cost on the unchanged 1,000-part layout before automatic scheduling |
| Constructor speed diagnostic | Stable cost order cuts 1,000-part collision checks from 9.33M to 4.39M; last matched-CPU pair uses 61.8% less CPU time with identical output | [All ten timing attempts](../benchmarks/results/construct-profile-20261012T0042.md); four-circle experiment reverted; no G4 claim |
| Backup and hosted checks | [Private GitHub repository](https://github.com/skulitom/Nestbolt); commits pushed | Search-control CI passed four jobs; Windows exposed a temporary-path alias in the new test fixture, now fixed; rerun pending |

Next: reduce repeated-construction cost on large jobs and strengthen repair while completing
only the missing M1 comparisons. Conservative proxies may
miss feasible layouts; M3 will recover hole area with true part-in-part placement.
The first constructor does not establish M2, G2 quality or G4 speed.

[Ties, failure coverage and the baseline-gap formula](../benchmarks/STATISTICS.md)
are now explicit. No competitor result means no free win. The [verified 10.6417% single-seed gap](../benchmarks/results/pilot-gap-feedback-20261011.md)
is not the final three-seed M1 target. Both 60 s and 300 s G2
populations must pass separately.

The independent checker covers original geometry, spacing, quantities, units,
stock, margins, defects, rotations, mirroring and fill mode. The latest full local
check passed 71 workspace tests, four stock-helper tests, both WASM builds,
source/schema/notices checks and 81 Python tests. Five Node tests cover CPU
selection and native process cleanup.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered. No release or registry listing has been published.
