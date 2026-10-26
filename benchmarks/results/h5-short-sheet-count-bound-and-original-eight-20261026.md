# H5: an eight-part short-sheet bound and original construction — 2026-10-26

**For the checked 55-part first-sheet arrangement, at most eight of the eleven
remaining originals can go on the target short sheet. A new original-geometry
construction achieves eight on that sheet. Three cogs still need first-sheet
positions, so there is no complete 66-part witness and H2/H5 remain open at 60%.**

## Complete count coverage

The stem-ordered nine-or-more decision replaces the five old bracket bounding-box
orders with stem ordering; its audit checks all retained fields and 46,080
presence/rank cases. Its sole call is UNKNOWN.

The existing all-angle four-bracket/four-cog exclusion leaves exactly four
families with nine or more short-sheet parts among the six brackets, one insert
and four cogs still required: **(5,1,3), (6,0,3), (6,1,2), (6,1,3)**, in
bracket/insert/cog order. Enumerate all 70 family allocations to prove coverage;
no part-dropping or rounded-area monotonicity assumption is used.

Each exact-count model retains the full 122-variable stem model and adds 52
optional horizontal intervals, one global no-overlap and three count equalities.
Bracket intervals represent their full-height stems. Cog intervals have width
245.034 mm. These cog intervals are propagation devices, not asserted subsets
of the source. Their separation from every other interval follows from the
retained stem ordering, six cog gaps and 192 original-support direction bounds.
Independent reconstruction and actual solver import/export pass for all cases.

Three exact cases are INFEASIBLE; **(6,1,2)** remains UNKNOWN. Restoring every
universal-angle vertical cell and band to that last case gives 2,422 variables
and 3,415 constraints, but its sole call is also UNKNOWN. The inverse-index
audit verifies all 2,300 restored variables and 2,417 restored constraints,
including 54 profile groups and 63 capacity rows. These UNKNOWN results are
preserved and do not themselves exclude anything.

| Experiment | Variables / constraints | Result | Solver / shared seconds |
|---|---:|---|---:|
| h5-stem-ordered-nine-decision-20261026 | 122 / 942 | UNKNOWN | 20.026304 / 20.803981 |
| h5-core-count-partition-20261026/case-000 | 122 / 998 | INFEASIBLE | 3.158434 / 3.853256 |
| h5-core-count-partition-20261026/case-001 | 122 / 998 | INFEASIBLE | 4.236177 / 4.913938 |
| h5-core-count-partition-20261026/case-002 | 122 / 998 | UNKNOWN | 20.057031 / 20.728764 |
| h5-core-count-partition-20261026/case-003 | 122 / 998 | INFEASIBLE | 4.309419 / 4.992349 |
| h5-last-count-bands-20261026 | 2,422 / 3,415 | UNKNOWN | 20.034500 / 20.772403 |

All six calls are closed. Each had one declared 20-second solver / 30-second
shared limit, four workers and seed 0. All shared limits pass. Soft overruns
are recorded in [closed calls](h5-short-sheet-count-bound-and-original-eight-20261026/closed-calls.json); no retries occurred.

## Independent exact exclusion of the last family

Omit the insert and keep six brackets plus two cogs. Use each bracket's stem
start and each cog's center as its horizontal coordinate. All are strictly
ordered in any valid source layout, by the previously proved support and
spacing bounds.

For each of the 64 ordered bracket profile pairs, compare all inset rectangle
pairs plus the verified full-height stems. **768 rectangle pairs overlap in Y
throughout the full allowed anchor ranges.** Each therefore contributes an
open forbidden X interval. Convert those intervals to closed integer sets,
merge them independently, and find the smallest permitted stem distance
starting at the first stem's width. Touching endpoints remain permitted.
Add original-support bracket/cog gaps and the cog/cog gap, giving **81** exact
necessary distance bounds across nine profile types.

A complete finite dynamic program records the earliest feasible coordinate
for each count/last-profile state. Earlier coordinates dominate later ones:
all retained constraints are lower differences and fixed coordinate domains.
It checks **149 reachable states and 1,159 transitions**, with no terminal
state containing six brackets and two cogs. An independently implemented
backward latest-coordinate program also has **149 states and no terminal**.
All forward records, transitions and witness prefixes are independently checked.

The projection omits the insert and all nonadjacent exclusions, so it is weaker
than the original packing problem. Its negative result excludes the six-bracket,
two-cog subset for this stock target at every real cog angle and continuous
source anchor, with conservative integer rounding already covered by the
source proxy proofs. Combined with the three audited exact-case negatives,
this proves **at most eight short-sheet parts for the checked55 continuation**.
It does not prove the full job impossible or exclude other first-sheet arrangements.

## An actual eight-part short sheet

Construct three mirrored quarter-turn bracket pairs, followed by one original
cog and one original insert, using 0.225 mm construction separation. The short
sheet contains original brackets **21/22/25/26/28/29**, insert **37** and cog **53**.
The prior first-sheet 55 placements remain exactly unchanged. Cogs **63/64/65**
are explicit mandatory first-sheet additions; all 66 identities are accounted for.

The resulting **63-part partial** passes **1,513 original filled-outer pair
checks and 252 stock-edge checks**. Its **87 cutouts and 9,426 cutout vertices**
are preserved. Minimum pair distance is 0.212500 mm against the required native
guarded distance of 0.211708673 mm; minimum extra stock margin is 0.012500 mm.
A separate auditor directly transforms every original vertex, verifies allowed
rotations/mirrors, cutout coordinates and areas, and repeats all pairs/edges.
The achieved short-sheet count matches the proved upper bound for this branch.
This is a useful different allocation, not a claim of more placed parts than
every earlier partial or a valid full-job result.

Next investigate original cog placement space on the first sheet. If the fixed
55 cannot accept three cogs, release/rearrange first-sheet parts or evaluate
other eight-part allocations. Full66 native/material validation, production
integration within 60 seconds and the complete H5 matrix remain required.

## Repository and evidence

Source review at **2026-10-26T10:27:15.468912+00:00** finds local HEAD and main at **9842e4c1**,
with unchanged production/README digests and upstream stop-rule state. At the
preseal check, [CI40305808059](https://github.com/skulitom/Nestbolt/actions/runs/40305808059)
has **5/6 jobs passed**, overall **in_progress**. Queue this checkpoint
until all six checks pass before a normal push. H2 retains its original gate;
the 22 reserved vectors remain untouched. No new release is qualified.

All **16 audits pass**. [Checks](h5-short-sheet-count-bound-and-original-eight-20261026/checks.json),
[exact bound](h5-short-sheet-count-bound-and-original-eight-20261026/exact-count-bound-proof.json),
[original short sheet](h5-short-sheet-count-bound-and-original-eight-20261026/original-short-eight.json),
[partial63](h5-short-sheet-count-bound-and-original-eight-20261026/partial63-placements.json), [scope](h5-short-sheet-count-bound-and-original-eight-20261026/scope.json),
[next step](h5-short-sheet-count-bound-and-original-eight-20261026/next-step.json), [raw manifest](h5-short-sheet-count-bound-and-original-eight-20261026/raw-manifest.json).
The archive verifies 213 canonical files and
281 aliases by bytes, SHA-256 and CRC.
