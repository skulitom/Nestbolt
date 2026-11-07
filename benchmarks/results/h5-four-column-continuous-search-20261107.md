# Four-column continuous-angle search — 2026-11-07

The new 39-mover model completes its frozen **three calls and 149 orientation
trials** without a valid layout. Its best objective candidate still fails
**69 source pairs: 57 moving pairs and 12 against fixed parts**. All stock
checks pass. The actual summed overlap, including fixed parts, is
**56,517.717179 mm²**; the moving-only objective component is smaller and must
not be reported as the full source overlap. H2/H5 remain open at **60%
completed milestone weight**. No native call, allocation exclusion or release
follows. Four fixed arrangements and 440 allocations remain.

## Complete source initialization and model

The preceding source construction fixed 18 quarter-turned frames and nine
short-sheet parts. This model jointly moves the remaining eight brackets,
nineteen inserts and twelve freely rotating cogs, using all 741 moving pairs
and 90 continuous parameters. All legal bracket/insert modes remain available.

The deterministic initializer uses the charged source-derived 6.75° tooth
phase. [Exact rational checks](h5-four-column-continuous-search-20261107/exact-contact-pitches.json) reconstruct
both axis contact bounds from 441 convex-piece pairs each. Both upward-rounded
row pitches are 261.766 mm. Translating certified free-region vertex coordinates
by these pitches gives 114 cog candidate centers. Orthogonal parts use cell
vertices, centroids and a fixed 9×9 grid, with explicit deterministic ties.
Every one of the **18,762 trial scores and selections** independently replays.
The full seed fails 39 source pairs and no stock edges; it is not a packing
witness. Complete new preparation takes **7.647472 s**, including all trials,
initial scoring, source validation and serialization. With the previously
charged source construction, preparation totals **11.244113 s**.

The objective equally weights actual moving filled-outline intersection area
and certified clearance-contour intersection area. It also adds four times
the squared distance of each center outside its entire certified free region.
This domain penalty is a heuristic for fixed-part avoidance; a finite positive
value does not establish clearance. Hard source stock bounds remain enforced.
All original contours and holes are retained, and filled outers enforce noPIH.
Internal convex-cell seams are not treated as physical obstacles.

[The complete model audit](h5-four-column-continuous-search-20261107/model-audit.json) verifies 152 owner/mode
bindings, 114 dynamic mode vectors, 152 independent full objective scores,
861 whole-region distance controls and 508 distance derivatives. It also
compares 156 scalar/batched source gradients, checks [180 central-coordinate
derivatives](h5-four-column-continuous-search-20261107/derivative-controls.json), [three seed descent steps](h5-four-column-continuous-search-20261107/seed-descent-controls.json)
and [ten deliberate corruptions](h5-four-column-continuous-search-20261107/negative-controls.json). Shared-edge
and nonconvex nearest-point conventions remain explicit; no global convergence
claim is made. All model checks pass before optimization.

## Physical equivalence and one bounded pipeline

[An independent exact nominal-outline audit](h5-four-column-continuous-search-20261107/physical-mode-audit.json)
groups equivalent insert orientations. It verifies that the 152 source mode
options reduce to 114 physical owner options for filled-outline collision
purposes. Of 113 single-owner alternatives, nineteen reproduce the current
physical geometry, and the others form 75 distinct physical neighbors.
Actual output still retains its selected legal transform and all holes.
Equivalent modes cannot reopen an optimized physical mode vector.

The frozen pipeline permits one initial call of at most 16 seconds and at most
two changed-physical-mode calls of 12 seconds each. Each later call selects the
lowest full-objective unvisited neighbor of the best saved candidate. The
neighbor need not improve before optimization; every worse result is retained
and compared with the global best. This policy was fixed before execution.
There are no random restarts, repeated physical vectors, adaptive weights or
extensions. The 60-second algorithm, 90-second shared, 2 GiB and four-second
source-reserve limits include all consumed preparation and runtime.

All three calls stop on time and return no numerical convergence result.
[Independent replay](h5-four-column-continuous-search-20261107/response-audit.json) verifies **240 saved points,
271 evaluations, 149 distinct mode trials**, all skipped equivalent/visited
vectors and every selected clamp. The third mode proposal initially increases
the objective by 273.294814 mm², then reduces it during optimization; that
increase is preserved. The best combined objective falls from 243,180.485079
to 94,988.169864 mm², but the original-source results remain invalid:

| Call | Failed source pairs | Moving–moving | Fixed–moving | Total source overlap (mm²) |
| --- | ---: | ---: | ---: | ---: |
| 0 | 67 | 56 | 11 | 65012.637 |
| 1 | 68 | 58 | 10 | 60684.079 |
| 2 | 69 | 57 | 12 | 56517.717 |

Every candidate is reconstructed from all 66 originals: 1,632 same-sheet pairs,
264 stock edges, 90 holes and 10,026 hole vertices. [The final failures](h5-four-column-continuous-search-20261107/source-failures.json)
contain 61 positive-area intersections and eight clearance-only failures.
Nine centers lie outside their certified free regions. The fixed-part
collisions contribute 14,636.360306 mm² beyond the moving-only area of
41,881.356872 mm². Lower heuristic penalties do not imply source validity,
material savings or a better valid part count.

The three optimizer-slice overruns are **0.026402, 0.141130 and 0.152586 s**.
All are preserved within complete algorithm/shared totals of
**54.960524 /55.032120 s**. [All five processes close](h5-four-column-continuous-search-20261107/closed-search-process.json),
with 94,212,096 bytes peak committed memory. The separate [response audit](h5-four-column-continuous-search-20261107/response-audit-process.json)
takes 39.874351 s and also closes normally. The pipeline is closed by its
three-call limit; unused time does not authorize another call or a reset clock.

## Next scope and repository state

[Historical review](h5-four-column-continuous-search-20261107/historical-allocation-scope.json) confirms an older
eight-bracket/five-insert short sheet and a closed fixed29 search for its
remaining four brackets, five inserts and fifteen cogs. That search allowed
four finite cog angles and failed 40 pairs and five stock checks. Neither the
allocation nor its old initialization is claimed as new.

[Next reconcile the current allocation ledger](h5-four-column-continuous-search-20261107/next-step.json) and assess
whether a source-derived model with all fifteen continuous cog angles provides
a genuinely different scope, with all 24 movers and 63 continuous parameters.
It would retain 276 moving pairs. Its original geometry, complete provenance,
deterministic initialization and all controls must be established before a
new bounded search. No successor geometry, initializer, model or call is
prepared. The current candidate and all earlier calls remain closed.

All66 source validation, native acceptance, material, the unchanged H5 matrix
and production UI/CLI/MCP parity remain required. The H2 gate remains open
under the earlier user decision. [Prior checkpoints reached main 89afabf2](h5-four-column-continuous-search-20261107/prior-main-push-receipt.json)
after all six previous checks passed, preserving 52 remote files. [Five current
CI jobs pass](h5-four-column-continuous-search-20261107/main-ci-at-review.json); Windows native CI remains live at
review. This checkpoint awaits the ordinary push gate. Production, README and
releases are unchanged.

[Raw evidence](h5-four-column-continuous-search-20261107/raw-manifest.json) preserves 361
canonical members and 1,170,837 ZIP bytes. [Historical references](h5-four-column-continuous-search-20261107/external-evidence.json)
and [source bindings](h5-four-column-continuous-search-20261107/source-bindings.json) preserve the full consumed
lineage. Independent archive readback is required before commit.
