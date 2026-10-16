# Integrated preview: Chrome subset misses H4 — 2026-10-16

**Release remains pending.** All 201 native and 201 Chrome layouts validate,
but Chrome's eleven-job median material difference is **+1.046217%** against the unchanged +1% limit.
Every subset job remains within +5%. The original Firefox arm is still running;
it will finish and be retained. No run is restarted and no bound is changed.

The complete native 65-job median difference from frozen v1 is 0%, passing
its +0.5% limit. Chrome passes full G5: median +0.242546%, total +0.571472%,
with all three individual seeds also inside the original G5 bounds. These
passes do not override the subset failure. H4 remains open at 45% completed
milestone weight. The failed preview candidate is 0a9fb44.

| Subset job | Native median | Chrome median | Chrome difference |
| --- | ---: | ---: | ---: |
| m-mechanical-cog-washers | 1.874102893 | 1.896529477 | +1.196657% |
| m-public-gear-1 | 0.940620330 | 0.970441205 | +3.170341% |
| m-public-gear-2 | 0.823359310 | 0.825356333 | +0.242546% |
| m-public-gear-3 | 0.510739771 | 0.515192034 | +0.871728% |
| m-public-gear-4 | 0.552761854 | 0.554107566 | +0.243452% |
| m-sign-1 | 0.715922770 | 0.721289845 | +0.749672% |
| m-sign-2 | 0.576832768 | 0.582867687 | +1.046217% |
| m-sign-3 | 0.138065191 | 0.139889029 | +1.320998% |
| m-sign-4 | 0.321897101 | 0.328319494 | +1.995170% |
| example-letters | 0.280123247 | 0.278433268 | -0.603299% |
| example-gears | 0.939389425 | 0.971891635 | +3.459929% |

All input/source/executable/site guards still match the committed plan.
This report records a completed arm, not a new measurement. The raw outcomes
remain in the active matrix and will be sealed when its original process ends.
It does not establish which change or source of timing variation caused the gap.
A subsequent candidate must have an actual implementation change, preserve
geometry and deadlines, and earn its own performance evidence. The existing
profile identifies collision scoring as a cost worth investigating; no new
optimization is accepted from this failure alone.

[Recorded calculations and records](h4-preview-chrome-failure-20261016/checks.json)
