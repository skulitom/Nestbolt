# Exchange coverage of height-setting parts — 2026-10-18

**None of 25 attempts selects the insert family that sets the credited sheet height.**

Two serial panel-hardware diagnostics use both kerfs, seed zero, 60 seconds
and physical CCD0 CPU 8. The observer changes no decision, work charge or
budget. Logging can change wall trajectories; these are diagnostic results,
not a quality comparison with earlier runs.

Both final layouts and both saved baselines validate. The independent
filled-outer audit checks 31,740 same-sheet pairs at the unchanged
1e-7 mm clearance tolerance. All original quantities, metrics, archive
members/hashes, counters and source/binary/input guards verify. The separate
rectangular-stock height calculation reproduces both baseline material
values exactly. The session takes 2.032 minutes.

| Kerf mm | Attempts | Visited choice indices | First insert-pair index | Insert attempts | Credited sheet height mm |
| --- | ---: | --- | ---: | ---: | ---: |
| 0.2 | 12 | 0, 1, 12 | 6 | 0 | 1591.654116 |
| 1.5 | 13 | 0, 1, 12 | 6 | 0 | 1591.654329 |

Outcomes: one exact-state rejection, eleven material-profile rejections
and thirteen source-repair-or-expiry stops. Seventeen attempts are paired,
including five mixed-item attempts. No exchange is accepted. The combined
source outcome preserves the original short-circuit condition; it does not
separate repair infeasibility from a time limit.

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

Coverage is by original part family. Zero insert-family attempts excludes
the two height-setting insert copies; a positive family count would not
by itself prove that those particular copies were chosen.

[Committed plan](h5-frontier-observer-20261018/plan.json),
[archive verification](h5-frontier-observer-20261018/verification.json),
[independent layouts and coverage](h5-frontier-observer-20261018/layout-checks.json),
[all observed attempts](h5-frontier-observer-20261018/observed-exchanges.json),
[source review](h5-frontier-observer-20261018/source-review.json).

Production, frozen inputs, the published preview and README claims remain
unchanged. The failed 72-outcome pilot remains the quality evidence.
**H2/H5 remain open; completed milestone weight is 60%.**
