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
| SVGnest | All 450 development slots complete. At 60 s: sheets 103/105 identical and 85/105 expanded valid; makers 1/90 identical and 0/90 expanded. At 300 s: sheets 18/18 and 15/18; makers 3/12 and 0/12 | [Final expanded sheet table](../benchmarks/results/comparison-batches-20261012T021336Z-74941dfd.md), [final expanded maker table](../benchmarks/results/comparison-batches-20261012T023246Z-a5cc0290.md); no further development runs |
| Deepnest | All 390 development 60 s slots complete. Sheets: identical 105/105 and expanded 104/105 valid. Makers: identical 25/90 valid, eight finite medians; clearance-safe 47/90 valid, 15 finite medians | [Maker identical](../benchmarks/results/comparison-batches-20261012T024400Z-b9c3dab2.md), [maker clearance-safe](../benchmarks/results/comparison-batches-20261012T030121Z-9132c7c2.md); finish the 300 s matrix |
| Current Sparrow | All 528 development slots accounted for: 127 valid, 43 invalid, 358 unsupported; both settings, both budgets, three seeds | [Complete coverage](../benchmarks/results/sparrow-development-20261012T0048.md); final-seed comparisons remain for M5 |
| Nestbolt search | Latest trial: all 65 development layouts valid. Shallow-overlap ranking removes a sheet on blaz1 free (11 → 10; 5.77% less material); other scores are unchanged. The 1,000-part job completes in 31.2 s | [35 sheet outcomes](../benchmarks/results/repack-sheet-20261012T025253Z-db613259.md), [30 maker outcomes](../benchmarks/results/repack-maker-20261012T025303Z-d1b807bb.md); fixed-pass diagnostics, not equal-time gates |
| Repair repeatability | Two repeated 64-pass blaz1 runs have identical full outputs and valid layouts; the improvement arrives in pass 3 | [Replay evidence](../benchmarks/results/shallow-replay-20261012T0255.json); a regression test protects the ten-sheet result |
| Search limits | 1,000-part job returns a valid incumbent in 15.094 s under a 15 s cooperative deadline; two fixed-work replays produce identical results | [Stop and replay evidence](../benchmarks/results/search-control-20261012T0114.md); calibrate time-to-work mapping and wire browser/MCP cancellation |
| Compaction | All 65 layouts valid; seven sheet and ten maker improvements retained. Bounded relocation preserves every material score and reduces collision queries by 24% overall; original-geometry guard prevents material regression | [Sheet trial](../benchmarks/results/compact-b-20261012T013650Z-e3423fac.md), [maker trial](../benchmarks/results/compact-m-20261012T013654Z-fb5e8bfa.md); remains optional while stronger sheet repair is developed |
| Constructor speed diagnostic | Stable cost order cuts 1,000-part collision checks from 9.33M to 4.39M; last matched-CPU pair uses 61.8% less CPU time with identical output | [All ten timing attempts](../benchmarks/results/construct-profile-20261012T0042.md); four-circle experiment reverted; no G4 claim |
| Backup and hosted checks | [Private GitHub repository](https://github.com/skulitom/Nestbolt); commits pushed | All five hosted checks passed for commit `ce69b09`; local tests, lint and both WASM builds pass for shallow-overlap ranking |

The [current baseline audit](../benchmarks/results/baseline-gap-20261012T030330Z-035c0ad1.md) covers every 60 s slot. The median competitor improvement over LBF is **17.09055736%** across 38 paired jobs. Thirteen jobs lack a finite competitor median and fourteen lack a finite LBF median; they remain separate. The 300 s matrix must finish before the M1 target is frozen.

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
check passed 77 workspace tests plus the new blaz1 regression test, four stock-helper tests, both WASM builds,
source/schema/notices checks and 89 Python tests. Five Node tests cover CPU
selection and native process cleanup.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered. No release or registry listing has been published.
