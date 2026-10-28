# H5: short-sheet transfer and source-based row clearance

The two complete 43-block searches closed **UNKNOWN**, with no complete
candidate. A new 61-part control exposes 61 false rectangle-cover collisions
between cog rows. Replacing those row-to-row checks with independently proved
source clearance removes the false rejection while retaining all 66 mandatory
originals. H5 is still open; neither result proves the job infeasible.

## Allocation and first cover model

The previously verified short sheet keeps its exact 7 bracket, 4 insert and
1 cog poses. The first sheet requires 18 frames, 5 brackets, 17 inserts and
14 cogs. It has 43 independently movable blocks: 40 orthogonal parts and three
rigid cog rows containing 5, 5 and 4 originals. Frames and inserts have two
orientations, brackets retain all eight quarter-turn/mirror modes, and cog
rows retain phase 7 degrees and 258.9 mm internal pitch. Only the two identical
five-cog rows have a relative ordering constraint.

The [cover-model audit](h5-transfer-and-hybrid-row-clearance-20261028/cover43-model-audit.json) verifies all 242
variables and 2,075 constraints, including 113 mode choices and 38 symmetry
orders. The new four-cog cover contains 205 rectangles; each five-cog cover
contains 253. The geometry proof checks 702 independently expanded source
triangles and 52,796 same-owner rectangle pairs. Stock bounds preserve the
original geometry boundary plus a 13 µm model guard, and clearance covers may
extend into the separately proved cover envelope.

The original positive control contains 52 parts and is rejected by exactly
14 mandatory constraints in the full target. Changing only those presence
requirements in an audit copy makes it pass all 273,430 cover pair checks.
The overlapping 66-part negative control has 982 source collisions and fails
all three cover collision constraints. Wrong row cardinalities are rejected;
no original can disappear through a four-cog/five-cog mode mismatch.

## Source-valid compact control and replacement constraints

The [61-part control](h5-transfer-and-hybrid-row-clearance-20261028/compact-source61.json) retains the verified
18-frame/11-insert core, adds the remaining six inserts at the top, and uses
cog row anchors at X 97.925 / 177.925 / 97.925 mm and Y 2107.875 / 2354.875 /
2601.875 mm. It omits only the five first-sheet brackets. Its independent
[source audit](h5-transfer-and-hybrid-row-clearance-20261028/compact-source61-audit.json) checks 1,242 original pairs,
75 cutouts and 8,196 hole vertices, with zero collisions and zero stock
failures. The minimum source gap is 0.223920332411 mm and the minimum extra
stock clearance is 0.0126 mm. This is a diagnostic control, not an improvement
over the preserved 64-part result.

All 61 cover collisions occur between row blocks 40/41 or 41/42. The saved
[old-model readback](h5-transfer-and-hybrid-row-clearance-20261028/old-cover-control61-rejections.json) confirms that
the same source-valid poses fail the old rectangle-cover collision rule.

The replacement model has three rectangle groups, each containing one cog row
and every orthogonal part. These retain all row-to-part and part-to-part cover
checks. Three complete source displacement domains replace row-to-row cover
checks. Two geometric types (5/5 and 5/4) account for all 65 original cog pairs
across the three rows. No row pair is left unconstrained.

The [independent geometry audit](h5-transfer-and-hybrid-row-clearance-20261028/hybrid43-geometry-audit.json) starts
from 78 original cog triangles and 6,084 Minkowski hulls. It checks all 45
distinct typed source-pair offsets, including actual floating translations,
and proves that the stored obstacle contains the required-clearance obstacle.
The construction uses a mitre buffer at required gap / cos(π/64) + 1.1 nm;
the independent comparison uses the conservative round buffer at required
gap / cos(π/64) + 0.1 nm. Complete constrained triangulations yield 98 and
166 cells. Exact rational error bounds prove all 792 inward halfplanes safe
for the bounded integer coordinates. Both zero-displacement controls fail.

The [hybrid-model audit](h5-transfer-and-hybrid-row-clearance-20261028/hybrid43-model-audit.json) verifies every one
of 672 variables and 3,374 constraints, all 903 distinct block pairs and
622 soft hints. Old fields remain unchanged except the three collision
constraints and hints; every new field is separately accounted for. All
43 blocks remain mandatory. The 61-part control fails exactly the five
missing-bracket requirements. An audit copy changing only those requirements
passes all 111,336 rectangle-pair visits. The full negative control fails all
nine rectangle collision constraints and three row-cell choices. Original
source reconstruction and wrong-size row rejection pass fresh checks.

## Closed calls and limits

Each model received one fresh 60-second algorithm budget inside a 90-second
shared limit, using four workers, seed 0 and `fj` disabled. Process startup,
input verification, solving and any candidate source readback count toward
the algorithm budget. Neither call was restarted, reseeded or extended.

| Measurement | Cover model | Hybrid model |
|---|---:|---:|
| Search begins, solver log seconds | 1.87 | 1.05 |
| Allocated solve seconds | 59.197238300 | 59.238716300 |
| Returned solve seconds | 59.220974700 | 59.258527500 |
| Solve soft overrun seconds | 0.023736400 | 0.019811200 |
| Algorithm seconds | 60.028382400 | 60.025292200 |
| Algorithm soft overrun seconds | 0.028382400 | 0.025292200 |
| Shared seconds | 60.106266000 | 60.084532700 |
| Returned worker branches / conflicts | 25,133 / 19,157 | 111,101 / 3,540 |
| Status / incumbents | UNKNOWN / 0 | UNKNOWN / 0 |

Counters describe the returned worker, not a sum across all four workers.
The [cover response audit](h5-transfer-and-hybrid-row-clearance-20261028/cover43-response-audit.json) and
[hybrid response audit](h5-transfer-and-hybrid-row-clearance-20261028/hybrid43-response-audit.json) recheck parameters,
hashes, serialized models, logs, counters and timing. All overruns remain
recorded. No complete assignment, source-valid 66-part layout or native
validation result was produced. A complete hybrid assignment would have
119,631 rectangle-pair visits plus all three source row-pair constraints.

## Failed preparations retained

The archive also preserves three failed preparations and their scripts:

- Adding a rounded 1 nm buffer to a legacy cog obstacle caused costly convex
  merging and then rejected the compact control. Diagnostics locate the
  offending row displacement at (−80, 247) mm, 0.000389340099 mm inside the
  legacy forbidden region. The original-source control remains valid. The
  process completed naturally before a stop request; the process-identity
  guard prevented termination of any other process.
- A dependent direct-obstacle preparation was incorrectly started after that
  stop guard failed. It stopped before creating its plan because the expected
  termination receipt did not exist. The missing-input failure is preserved;
  no termination receipt was fabricated.
- Recomputing the required-clearance obstacle and replacing greedy merging
  with constrained triangles completed in 1.001093 seconds, but the exact
  containment audit found a boundary discrepancy with zero area. The saved
  obstacle equalled the expected mitre construction. A fresh 1 nm scalar
  radius guard resolved the discrepancy, with preparation taking 0.975638
  seconds and the independent geometry audit 1.305561 seconds. It adds no
  rounded micro-edges. All original source thresholds remain unchanged.

None of these geometry preparations called a packing solver. Failed artifacts
were retained; only the final independently accepted model was searched.

## Publication and next action

After all six jobs in CI 40764537562 passed, a normal atomic push advanced
both `main` and `codex/v1-1-shop-files` from 75ee537c to 608fecf1, publishing
the two queued checkpoints. The [push receipt](h5-transfer-and-hybrid-row-clearance-20261028/main-push-receipt.json)
records live-run and ancestry checks. CI 40771628220 has four successful jobs
and both platform checks running at this checkpoint. It was not cancelled;
another main push must wait for all six passes.

The publication review confirms unchanged production source, all three
READMEs, Sparrow/Studio heads and release state. No new release qualifies.
The original H2 gate remains open under Artem's explicit decision; the
22 reserved vectors stay unopened. H2 and H5 remain open and completed
milestone weight remains **60%**.

Next compare original-source bracket clearance with row-cover clearance
around the 61-part control for all eight legal bracket modes. This should
distinguish unusable free space from another conservative cover restriction
before proposing a new search. Keep the current searches closed, the 64-part
control intact and the original 66-part/material target unchanged.

The [raw manifest](h5-transfer-and-hybrid-row-clearance-20261028/raw-manifest.json) binds 608 canonical files,
504 identical aliases and 2601047 compressed bytes. Recursive input
hashes, imported local helpers, failed preparations, all controls and both
closed solver responses are included. The archive verifier checks every byte,
alias, binding, JSON document and local report link.
