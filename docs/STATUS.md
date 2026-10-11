# Status — 2026-10-11

**Completion: 5%. M0 is complete; M1 and M2 are in progress.**
Percentages count completed milestones only. Pilot results below describe the
competitors, not Nestbolt quality; all failures and earlier trials remain in
[BENCHMARKS.md](../BENCHMARKS.md). Ten held-out maker jobs remain unused for tuning.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| M0 — Groundwork and reproduction | 5% | Complete: 39 valid runs; all 13 means within the frozen 1% threshold |
| M1 — Baseline | 15% | Validator and datasets complete; finish competitor seeds/settings and gap table |
| M2 — Sheet optimiser | 25% | First constructor passes all 30 development maker jobs; improvement search next |
| M3 — Part-in-part and import/export | 15% | Pending; original curves already retained in maker sources |
| M4 — Browser app and MCP | 20% | Scaffolding; five tools and actual Claude Code connection still to build |
| M5 — Final gates | 20% | Pending; all G1–G8 requirements remain in scope |

| Evidence | Current result | Next step |
| --- | --- | --- |
| Published Sparrow reproduction | 39/39 layouts valid; 13/13 instance means pass; worst absolute difference 0.986671% | [Final proof](../benchmarks/results/m0-published-20261011T215820Z-10a30c6f.md) |
| Frozen datasets | 13 strip, 35 sheet, 40 maker jobs; 10 maker jobs held out | Use only development cases for tuning |
| LBF development matrix | 450/450 attempts; 283 valid, 5 invalid, 162 unsupported | Complete; [table](../benchmarks/results/comparison-session-20261011T221209Z-ce35672e.md) |
| SVGnest | Fresh 60 s / seed 0 sheet pilot: 34/35 valid | 23 interrupted attempts are rerunning with a frozen checker; settings and remaining seeds pending |
| Deepnest | First 12 sheet jobs valid; complete maker pilot retained, including failures | Remaining 23 sheet jobs, settings and seeds |
| Current Sparrow | All 13 strip jobs valid at each of seeds 0, 1 and 2 | Aggregate seed statistics; sheet applicability proof |
| Nestbolt constructor | 30/30 development maker layouts valid; median 0.438 s, slowest 18.047 s | [First proof](../benchmarks/results/construct-maker-20261011T223817Z-32654739.md); improve material use |
| Backup and hosted checks | [Private GitHub repository](https://github.com/skulitom/Nestbolt); commits pushed | [First CI run](https://github.com/skulitom/Nestbolt/actions/runs/38180612330): all five jobs passed |

Next: add layout improvement and sheet
removal, and complete only the missing M1 comparisons. Conservative proxies may
miss feasible layouts; M3 will recover hole area with true part-in-part placement.
The first constructor does not establish M2, G2 quality or G4 speed.

[Ties, failure coverage and the baseline-gap formula](../benchmarks/STATISTICS.md)
are now explicit. No competitor result means no free win. The [verified 10.6417% single-seed gap](../benchmarks/results/pilot-gap-feedback-20261011.md)
is not the final three-seed M1 target. Both 60 s and 300 s G2
populations must pass separately.

The independent checker covers original geometry, spacing, quantities, units,
stock, margins, defects, rotations, mirroring and fill mode. The latest full local check passed 48 workspace tests, four stock-helper tests,
both WASM builds, source/schema/notices checks and 71 Python tests. Two additional
CPU-selection tests pass in Node.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered. No release or registry listing has been published.
