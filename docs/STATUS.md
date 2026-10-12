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
| SVGnest | 60 s / identical: all three seeds complete, 103/105 valid; 35 finite job medians | [Three-seed table](../benchmarks/results/comparison-batches-20261011T235825Z-a4355046.md); finish expanded settings and maker seeds |
| Deepnest | 60 s / identical: 35/35 sheet jobs valid at both seeds 0 and 1; complete maker pilot retained | Seed 2 underway; further settings/budgets pending |
| Current Sparrow | 78/78 valid strip layouts across both settings and three seeds; both B settings complete at 60 s | [Strip table](../benchmarks/results/comparison-batches-20261012T000738Z-c8a95335.md); finish maker settings and long-budget cases |
| Nestbolt constructor | 30/30 valid; v3 has exactly the v2 layouts; median 0.453 s, slowest 15.563 s | [Current proof](../benchmarks/results/construct-maker-20261011T230206Z-b7a21810.md); improve material use |
| Nestbolt refinement | Three-method comparison: 30/30 valid; 22 improve, eight unchanged vs constructor; slowest 56.718 s | [Trial](../benchmarks/results/repack-maker-20261011T233725Z-c0e36d78.md); improve large-job speed |
| Nestbolt repair | Sheet set: 35/35 valid; two improve, 33 unchanged vs prior search, one fewer-sheet job. Maker set: 29/30 finish; mixed-stock and remnant jobs lose a sheet; 1,000-part job times out | [Sheet trial](../benchmarks/results/repack-sheet-20261012T000748Z-0c7fac06.md), [maker trial](../benchmarks/results/repack-maker-20261012T000758Z-533d7bb1.md); accelerate repeated construction |
| Backup and hosted checks | [Private GitHub repository](https://github.com/skulitom/Nestbolt); commits pushed | [Repacking CI](https://github.com/skulitom/Nestbolt/actions/runs/38186324561): all five jobs passed |

Next: reduce repeated-construction cost on large jobs and strengthen repair while completing
only the missing M1 comparisons. Conservative proxies may
miss feasible layouts; M3 will recover hole area with true part-in-part placement.
The first constructor does not establish M2, G2 quality or G4 speed.

[Ties, failure coverage and the baseline-gap formula](../benchmarks/STATISTICS.md)
are now explicit. No competitor result means no free win. The [verified 10.6417% single-seed gap](../benchmarks/results/pilot-gap-feedback-20261011.md)
is not the final three-seed M1 target. Both 60 s and 300 s G2
populations must pass separately.

The independent checker covers original geometry, spacing, quantities, units,
stock, margins, defects, rotations, mirroring and fill mode. The latest full local check passed 61 workspace tests, four stock-helper tests,
both WASM builds, source/schema/notices checks and 76 Python tests. Two additional
CPU-selection tests pass in Node.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered. No release or registry listing has been published.
