# H5: expanded contact placements and exact-inventory selection — 2026-10-18

The new contact pool is independently verified, but **no complete target layout
is found**. The retained valid partial still has 63 of 66 original parts, missing
three cogs. The full-inventory CP-SAT attempt ends **UNKNOWN** at its time limit;
that is not an infeasibility result. H5 remains open.

The [previous saved-pose selection](h5-saved-placement-selection-20261018.md)
suggested generating contact locations beyond the beam's three lowest choices.
This construction keeps its 2,614 candidates, adds 2,584 distinct half-turns about
their original target-sheet centres, and generates **3,600 new original-outline
contacts**, 900 per family. It uses the 63 selected old poses and their half-turns
as 126 anchors, with all applicable quarter-turn/reflection templates and cog
phases 0°, 4.5°, 9° and 13.5°. Conservative Minkowski boundaries and stock-domain
intersections provide points spread around entire contact rings. Unrounded
coordinates are retained; every admitted contact is clear of its generating
anchor. The result has **8,798 candidates**, below its declared 8,828 cap.

Generation completes in **18.965 seconds**, without its 120-second contact-query
limit firing. Actual filled-outer geometry defines **2,517,051 conflicting pairs**.
Pairwise verified cliques compress these into **17,097** binary exclusions in
16.051 seconds, below the 30-second compression ceiling. Every original conflict
edge is covered and every clique member pair is an actual edge, making the binary
model exactly equivalent. The known partial remains a feasible model certificate.

Independent source reconstruction checks all 8,798 unrounded poses, original
stock targets, allowed rotations/reflections and all 3,600 anchor contacts. An
independent bounding-box enumeration visits **29,902,803** same-sheet candidate
pairs and evaluates **2,822,033** original-polygon distances. It reproduces the
entire 2,517,051-edge graph exactly, without the producer's spatial index, then
checks every clique and complete edge coverage. All **1,303** selected-part pairs
of the retained partial pass; the original public CLI rejects only cog quantity.

Three serial, separately recorded MILP mechanism attempts use the same model and
120-second allowance. The first has no starting incumbent; the second explicitly
supplies the independently valid full binary vector; the third changes only
presolve from its default to off. The bundled HiGHS 1.12.0 model arrays are checked
against the same matrix, objective, bounds and integrality before solving.

| Attempt | Actual seconds | Solver outcome | Returned inventory |
| --- | ---: | --- | --- |
| SciPy interface, no incumbent input | 120.181630 | time limit, no incumbent | unchanged partial fallback |
| Explicit verified incumbent | 120.096101 | time limit, feasible incumbent retained | 63/66, three cogs missing |
| Same incumbent, presolve off | 124.519761 | time limit, feasible incumbent retained | 63/66, three cogs missing |

The time-limit overrun is retained, not rounded down. In the warm-start attempt,
presolve finishes at about 79 seconds; the first search line appears at 81.7
seconds. It increases nonzeros from **681,124 to 1,627,667**, and the root
relaxation does not finish. With presolve off, the first relaxation completes at
2.2 seconds and the solver spends its remaining allowance on cuts and heuristics,
but finds no better selection. These are local diagnostic observations, not
production speed or H5 evidence. Both returned layouts are byte-identical to the
already audited partial; those geometry checks are reused by exact hashes rather
than rerun. The bounds do not establish global geometric feasibility or impossibility.

A distinct [CP-SAT feasibility model](https://developers.google.com/optimization/cp/cp_solver)
then requires **all 66 parts exactly**, with the same 17,097 conflict cliques and
no partial-coverage objective or rounded area coefficients. The 63 known positions
are nonbinding positive hints. A single attempt uses seed 0, eight offline CCD1
workers and a [120-second limit](https://developers.google.com/optimization/cp/cp_tasks).
Pinned [OR-Tools 9.15.6755](https://pypi.org/project/ortools/9.15.6755/) runs only in
isolated diagnostic environments; no production dependency is added.

The first environment, based on Anaconda Python 3.11.5, terminates before returning
a solver status. Its wrapper exit is 1; no packing result is invented. A separate
two-variable, one-worker probe records a native **0xc0000005 access violation** at
the solve call. The complete original model, empty solver log and failing probe
remain preserved. A fresh environment from installed standard CPython 3.13.9,
with **every package version unchanged**, passes the identical tiny probe. Both
official Windows wheel hashes are checked. This local recovery does not identify
which interpreter, ABI, wheel or environment difference caused the crash.

The recovered run must export the **exact same model bytes** before solving. It
starts search after 4.07 seconds, but ends **UNKNOWN** after 120.185060 real seconds,
returning no complete selection. The saved response reports 36,530 branches and
27 conflicts. An independent parser verifies all 8,798 Boolean domains, all
17,097 literal lists, all four exact original-quantity equalities, and precisely
63 nonbinding hints. It verifies that there is no hidden partial objective or
additional model constraint. Neither the crash nor UNKNOWN is a packing result
or a proof of infeasibility.

[Checks](h5-contact-selection-20261018/checks.json),
[all raw geometry, models, logs, failures, environments' metadata and audits](h5-contact-selection-20261018/raw.zip),
[manifest](h5-contact-selection-20261018/raw-manifest.json),
[next investigation](h5-contact-selection-20261018/source-review.json).
All 1234 archive members, CRCs and byte hashes verify. Installed runtime
binaries are not included in the evidence archive; pinned package versions,
download provenance and wheel hashes are retained.

The expanded finite pool and its entire physical conflict graph are now audited. The original partial remains the only returned layout: no native or offline full target witness is established. Do not repeat these unchanged models or extend their declared limits. CP-SAT now has a working isolated standard-CPython runtime, but its full-inventory status is UNKNOWN, not infeasible. Next construct coherent multi-cog components directly from the original filled outer geometry: use two-phase alternating lattices with pitches derived from actual horizontal/vertical Minkowski contacts, verify every pair and allowed rotation, and record finite phase/offset choices before running. Try fitting these coordinated groups with the retained frame allocations and original bracket/insert inventory, preserving stock and the original material target. Component checks remain component checks; only all 66 original copies passing both original CLI and filled-outer validation constitute a witness for this case. Do not infer that a cog bounding-box or area improvement proves the whole job fits. Use exact-count selection with the working runtime only after a materially different construction supplies useful coordinated candidates. Native margins, production-budget qualifications, the four-step repair cap and the full H5 matrix still apply before integration or gate credit.

All six hosted checks on main `5743a32` pass ([record](h5-contact-selection-20261018/main-ci-5743a32.json));
that is the preceding pushed revision. Production source, all gate limits,
preview assets and all three accurate READMEs remain unchanged. H2/H5 stay open
at **60%**. No new native packing or quality run, runtime integration, release
qualification or gate credit is claimed.
