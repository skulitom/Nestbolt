# Status — 2026-10-12

**Completion: 20%. M0 and M1 are complete; M2 is in progress.**
Percentages count completed milestones only. Development results do not establish the final acceptance gates. All failures and earlier trials remain in
[BENCHMARKS.md](../BENCHMARKS.md). Ten held-out maker jobs remain unused for tuning.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| M0 — Groundwork and reproduction | 5% | Complete: 39 valid runs; all 13 means within the frozen 1% threshold |
| M1 — Baseline | 15% | Complete: all 1,878 declared slots audited; [target frozen at 10.77231474%](M1_BASELINE.md) |
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
| Deepnest | All 450 development slots complete: 330 valid, 30 invalid, 88 no layout, two timeouts. At 300 s: both sheet settings 18/18 valid; makers identical 4/12, clearance-safe 9/12 | [Final maker identical](../benchmarks/results/comparison-batches-20261012T032935Z-846373a4.md), [clearance-safe](../benchmarks/results/comparison-batches-20261012T033500Z-e03868ab.md) |
| Current Sparrow | All 528 development slots accounted for: 127 valid, 43 invalid, 358 unsupported; both settings, both budgets, three seeds | [Complete coverage](../benchmarks/results/sparrow-development-20261012T0048.md); final-seed comparisons remain for M5 |
| Nestbolt search | All 65 development layouts valid. Repeated compression improves one sheet score (1.69%) and four maker scores (up to 0.30%) over v13, with zero regressions. Skipping unsuccessful repeats preserves every score | [35 sheets](../benchmarks/results/repack-sheet-20261012T035142Z-a7b22154.md), [30 makers](../benchmarks/results/repack-maker-20261012T035142Z-54130739.md); fixed-work diagnostics, no equal-time gate |
| Longer search | Up to 1,024 passes, preserving the first finished 64-pass block. A four-job 512-pass pilot improves Jakobs1 by 2.46% and Marques by 4.20%; the other two retain their 64-pass result | [All four cases](../benchmarks/results/progressive-pilot-20261012T0433.md); 80M query allowance and 60 s safety deadline, selected cases with extra work |
| Native strip parity | 39/39 outputs valid at 60 s, seeds 0/1/2. Median regression −0.0390%; worst +1.6493%, against the better Sparrow setting per job. Development thresholds pass | [Audited comparison](../benchmarks/results/strip-development-20261012T040418Z-961c9a96.md), [adapter scope](STRIP_PARITY.md); final-seed G3 acceptance remains |
| Repeatability and rollback | Two compression replays have identical complete outputs. Tests preserve the full repacking history, other sheets and the valid incumbent when interrupted | [Compression replay](../benchmarks/results/compression-replay-20261012T0326.json); previous [blaz1 repair replay](../benchmarks/results/shallow-replay-20261012T0255.json) |
| Quality triage | One-seed fixed-work results vs 60 s competitor medians: 19/52 wins or ties; 23/52 more than 1% worse; median reduction −0.0047%. Thirteen jobs have no finite competitor median | [Every job](../benchmarks/results/search-gap-diagnostic-20261012T0332.md); improve the worst cases before equal-budget acceptance runs |
| Search limits | 1,000-part job returns a valid incumbent in 15.094 s under a 15 s cooperative deadline; two fixed-work replays produce identical results | [Stop and replay evidence](../benchmarks/results/search-control-20261012T0114.md); calibrate time-to-work mapping and wire browser/MCP cancellation |
| Compaction | All 65 layouts valid; seven sheet and ten maker improvements retained. Bounded relocation preserves every material score and reduces collision queries by 24% overall; original-geometry guard prevents material regression | [Sheet trial](../benchmarks/results/compact-b-20261012T013650Z-e3423fac.md), [maker trial](../benchmarks/results/compact-m-20261012T013654Z-fb5e8bfa.md); remains optional while stronger sheet repair is developed |
| Constructor speed diagnostic | Stable cost order cuts 1,000-part collision checks from 9.33M to 4.39M; last matched-CPU pair uses 61.8% less CPU time with identical output | [All ten timing attempts](../benchmarks/results/construct-profile-20261012T0042.md); four-circle experiment reverted; no G4 claim |
| Independent checker speed | Reusing clearance outlines cuts validation CPU by a further 17.0% on the gear job and 13.8% on the 1,000-part job. Full-search outputs and all 104 retained validation reports remain identical | [Reuse timings](../benchmarks/results/clearance-cache-20261012T0433.md), [preceding distance-pruning trial](../benchmarks/results/validator-speed-20261012T0420.md); no G4 claim |
| Backup and hosted checks | [Private GitHub repository](https://github.com/skulitom/Nestbolt); commits pushed | All five hosted checks passed for `9185a00`; local clearance/search tests, lint and both WASM builds pass |

The [complete baseline audit](../benchmarks/results/baseline-gap-20261012T033547Z-e9539412.md)
measures competitor reductions over LBF of **17.09% at 60 s** and **21.54% at 300 s**.
The frozen G2 target is **10.77231474%**, applied separately to both budgets.
Missing finite comparisons remain explicit and never earn free wins.

Next: strengthen sheet removal and compression on the weakest development cases,
reduce large-job search cost, and prepare equal-budget acceptance. M2 requires the complete
G1/G3/G4 evidence. M3 will recover hole area with true part-in-part placement.

[Ties, failure coverage and the baseline-gap formula](../benchmarks/STATISTICS.md)
are now explicit. No competitor result means no free win. The [verified 10.6417% single-seed gap](../benchmarks/results/pilot-gap-feedback-20261011.md)
is superseded by the complete three-seed M1 audit. Both 60 s and 300 s G2
populations must pass separately.

The independent checker covers original geometry, spacing, quantities, units,
stock, margins, defects, rotations, mirroring and fill mode. The latest full local
checks passed 91 workspace tests, four stock-helper tests, both WASM builds,
source/schema/notices checks and 91 Python tests. Five Node tests cover CPU
selection and native process cleanup.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered. No release or registry listing has been published.
