# Row reductions and a three-cog allocation — 2026-11-04

**No full 66-part layout is established.** Two expanded-row reductions are
audited without another solver call. A distinct short-sheet allocation receives
one bounded call and closes UNKNOWN. An exact continuous proof then rules out
adding four inserts around the older *fixed* four-bracket/three-cog core.
All 440 whole-job allocations remain; H2/H5 remain open at **60%**.

## Expanded-row reductions

[Exact integer reduction](h5-row-reductions-and-three-cog-allocation-20261104/integer-reduction-audit.json) checks all
2,666 regions. It proves 40 contain no integer point by examining 10,218 integer
slices, verifies 2,626 nonempty witnesses and 138 domain-implied planes, and
preserves all three selected positive-control regions. The estimated expanded
model falls from 16,314 / 58,749 variables/constraints to 16,274 / 57,677:
only 0.245188% / 1.824712%. Complete reduction preparation takes 0.524202 s.
This does not warrant a new call.

The geometric merge reduces 2,676 raw regions to 2,435, with 241 merges.
[Source certification](h5-row-reductions-and-three-cog-allocation-20261104/merged-source-region-audit.json) verifies
51,242 mover-row and 89,200 row-pair exact support proofs, all 12 source modes,
13 cogs, 36 relative domains and the four original positive controls.
Minimum certified gap is 0.225999998297 mm. The floating intersection tolerance
used during merging is not the safety proof. [Complete preparation](h5-row-reductions-and-three-cog-allocation-20261104/merge-process.json)
takes 3.919402 s. This modest reduction also receives no model or solver call.
Neither reduction excludes continuous geometry.

## A distinct short-sheet inventory

The new [inventory](h5-row-reductions-and-three-cog-allocation-20261104/short-inventory.json) requires **4 brackets,
4 inserts and 3 cogs** on the short sheet and **18 frames, 8 brackets,
17 inserts and 12 cogs** on the first sheet. Every original appears exactly
once. It exchanges one bracket for one cog compared with the valid 5/4/2
short sheet, carrying 10,062.718938 mm² more source area on the short sheet.

The intrinsic geometry and integer planes are unchanged audited inputs.
Every owner-mode/template pairing is rebuilt for the new inventory.
[Original-source checks](h5-row-reductions-and-three-cog-allocation-20261104/short-source-mode-audit.json) cover all 51
instance-mode choices and 204 mode/stock corner controls, including original
holes. The [integer audit](h5-row-reductions-and-three-cog-allocation-20261104/short-integer-audit.json) independently
reproves all 666 convex hulls and 2,264 inward integer-plane implications.
The [model audit](h5-row-reductions-and-three-cog-allocation-20261104/short-model-audit.json) checks every field of
**7,071 variables and 23,988 constraints**, including 6,998 region selectors,
23,382 guarded planes, 430 mode marginals and all 55 original-owner pairs.
The 0.001 mm grid, fixed 7-degree cog phase and conservative regions limit
negative conclusions.

[Final preparation](h5-row-reductions-and-three-cog-allocation-20261104/short-preparation-charges.json) charges
**3.278376 s**, including reused intrinsic preparation and both complete new
inventory/model processes. The sole short-stage call uses a frozen
**25 s algorithm / 35 s shared** budget, reserving 3 s for source readback.
Any eventual first-sheet stage must charge this entire short construction
within the unchanged whole-job 60/90-second limits.

[Independent response verification](h5-row-reductions-and-three-cog-allocation-20261104/short-response-audit.json)
checks 5,277 recursive input bindings. The call closes **UNKNOWN**, with
188,791 branches, 19,405 conflicts and no incumbent or assignment.
Allocated/returned solver time is **18.038973 / 18.098255 s**, retaining the
**0.059281 s** solver-slice overrun. Preparation-inclusive algorithm/shared
totals are **22.074408 / 22.142098 s**; overall stage limits pass.
There is no source11/source66 result, native call or allocation exclusion.
The call will not be repeated, reseeded or extended.

The first model-audit helper had a [syntax error](h5-row-reductions-and-three-cog-allocation-20261104/model-audit-first-attempt.json)
before it could run. Its original bytes are retained. The corrected audit
passed before the solver opened; neither model nor budget changed.

## Exact capacity of the older fixed core

The older valid 4/2/3 short layout uses cogs at exactly
−2.2428996024478143 radians. Its four brackets and three cogs retain their
original transforms, with identical-family copy identities mapped to the new
inventory. Both existing inserts are released; all four inserts are required.
Original-source readback confirms the fixed seven-part core and old nine-part
control remain valid.

A preliminary floating free-space diagnostic is preserved, including NaN bounds
from an empty polygon. Its conservative 0.226 mm regions do not cover every
guard-valid placement and supply **no negative certificate**.

The authoritative [capacity audit](h5-row-reductions-and-three-cog-allocation-20261104/fixed-core-capacity-audit.json)
uses an exact rational necessary relaxation. [Source partition certificates](h5-row-reductions-and-three-cog-allocation-20261104/source-partition-certificates.json)
verify convexity, area and cancellation of all internal edges against the
original bracket and cog outlines. All **233 retained inner rectangles**
are exactly contained in the 71 affine source pieces.
[All four legal insert rotations](h5-row-reductions-and-three-cog-allocation-20261104/insert-inner-rectangle-certificates.json)
contain the declared axis-aligned rectangle shrunk by 0.000001 mm on every side.
Thus the relaxation admits more placements than the required source geometry.

At **zero clearance**, an independent integer event sweep replays **1,248
open X intervals and boundary X points**, preserving all allowed Y intervals
and isolated points. The six resulting free boxes are covered by two horizontal
anchor components and no vertical component. Each horizontal component is
narrower and shorter than one insert body, so it cannot hold two nonoverlapping
inserts. **The fixed core can hold at most two inserts, whereas four are needed.**
This is a continuous fixed-core exclusion, independent of solver status or grid.
It does not exclude a construction that moves the core or any whole allocation.
Proof preparation takes 8.304109 s internally; no complete layout timing is
claimed. A [first audit type error and its correction](h5-row-reductions-and-three-cog-allocation-20261104/capacity-audit-attempts.json)
are both preserved; the successful independent audit takes 0.594493 s.

## Remaining work and publication

[The next step](h5-row-reductions-and-three-cog-allocation-20261104/next-step.json) requires a genuinely different
coordinated construction that moves the core, or a different whole-job
allocation. A cog-phase or seed change alone is insufficient justification to
retry this closed model. Preserve both older valid short layouts. A first55
search for the new 4/4/3 allocation is not qualified without a valid short11.
All66 original-source checks, native/material checks, integration and the H5
matrix remain required. H2 retains its original gate and unopened reserved
vectors. No new release qualifies.

[All six jobs and aggregate CI](h5-row-reductions-and-three-cog-allocation-20261104/prior-main-ci.json) on prior main
e47197f1 pass before publication. The normal push still verifies current remote
refs, ancestry, allowed paths and absence of other live main runs.

[The raw manifest](h5-row-reductions-and-three-cog-allocation-20261104/raw-manifest.json) contains 295 new canonical
members and 3,333,794 compressed bytes. [External references](h5-row-reductions-and-three-cog-allocation-20261104/external-evidence.json)
and [source bindings](h5-row-reductions-and-three-cog-allocation-20261104/source-bindings.json) preserve historical inputs.
The independent archive verifier checks all new and reused bytes and bindings.
