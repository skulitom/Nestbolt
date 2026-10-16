# Isolated collision-tree depth pilot — 2026-10-16

**99/99 layouts valid. Both browser subsets pass.**

Eligible for integration checks and a fresh full matrix; no H4 completion or release readiness yet.

The [committed plan](h4-quadtree-depth-probe-20261016/plan.json) fixes all eleven
H4 development jobs, 60 seconds and seeds 0–2. The sole algorithm setting
change is separator-window base tree depth four to three; original geometry,
leaf threshold, aspect scaling, work coefficients and search budgets are unchanged.
Native and each browser run separately on physical CCD0 cores 0,2,…14, with
at most eight simultaneous searches. This session starts after both earlier
H4/H5 measurements finish and are sealed; no measured sessions overlap.
The session took 17.614 minutes. Guards remain unchanged.

## Material comparison

Per-job material is the median of all three fixed seeds. Positive differences
are worse. The original limits remain +1% subset median and +5% for every job.

| Browser | Median vs native | Worst job | Total material | Pass |
| --- | ---: | ---: | ---: | --- |
| chrome | +0.689439% | +2.350728% | +0.511754% | yes |
| firefox | +0.639475% | +3.385773% | +0.664581% | yes |

All attempts and failures remain in [results](h4-quadtree-depth-probe-20261016/results.json).
Every valid layout covers all requested parts and agrees exactly with independently
recomputed original-geometry metrics; example library/request checks also agree.
[Verification](h4-quadtree-depth-probe-20261016/verification.json) retains all six
browser batch exits and affinity observations. Reliable temperatures are unavailable.
Hazard traversal order can change, so no fixed-work identity or isolated speed claim is made.

The raw archive has 1,067 members, 15,259,453 bytes and
SHA-256 `1e90ee17217697d949527d6ec256fcf56a851fda4bfc4a8fa37101c98981e1a5`. CRC, every member size and hash pass.
Original layouts, diagnostics, inputs, runner and exact source/executable/site
snapshots remain preserved. Full quality/native matrices, current browser scale
and package checks remain separate requirements. Earlier failed comparisons
remain authoritative for their builds. H4 stays open; completion remains 45%.
