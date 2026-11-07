# Staged cog candidate and exact safe-region projections — 2026-11-07

The new staged construction returns one **necessary 66-part candidate**, whose
original-source check fails on **32 pairs**. It adds all 32 complete certified
interactions, then stops when the changed model returns UNKNOWN. The pipeline
is closed. A new exact projection preparation now proposes one safe convex
region for every cog interaction; its repair model has not been built or solved.
No source-valid full66 layout or exclusion follows. Four fixed arrangements
and all 440 allocations remain, with H2/H5 open at **60% completed milestone
weight**.

## Controlled staged construction

[Preflight controls](h5-staged-cog-candidate-and-projections-20261107/pipeline-controls.json) verify **1,220 routing cases**:
all 258 cog interactions in both original-identity orders, active and inactive;
all 120 orthogonal pairs; all 38 fixed/short originals; all 28 movable stock
identities; and mixed/valid cases. Three distinct changed-model controls pass
full independent readback. Five deliberately corrupted models are rejected.
No control calls a solver. The complete verification process takes 2.263694 s.

The frozen pipeline permits at most four strictly changing rounds under one
preparation-inclusive 60/90-second and 2 GiB budget. The first solve is capped
at 30 seconds and later solves at eight, each further limited by remaining time
and a four-second source-check reserve. Solver processes close before separate
source-check processes start. No unchanged model can be retried.

[Independent response and model readback](h5-staged-cog-candidate-and-projections-20261107/response-audit.json) verifies
the actual **two closed calls**. The 1,332-variable / 4,712-constraint initial
model returns OPTIMAL for its necessary constraints after **8.416443 seconds**,
with 67,526 branches and 13,485 conflicts. Its one incumbent and returned
assignment satisfy every model constraint; this alone does not validate the
original contours.

[Original-source replay](h5-staged-cog-candidate-and-projections-20261107/original-source-audit.json) reconstructs every
original identity and repeats all **1,632 same-sheet pairs, 264 stock edges,
90 holes and 10,026 hole vertices**. It confirms 31 positive-area overlaps and
one clearance-only failure, with zero stock failures. The [observed collision
graph](h5-staged-cog-candidate-and-projections-20261107/candidate-collision-graph.json) involves 24 movers in one connected
component. These facts describe only this candidate.

All 32 failures map to previously unconstrained cog interactions. The changed
model has **5,041 variables and 12,819 constraints**, including 3,671 pair-region
selectors, 7,769 guarded source planes, 272 exact mode-coordinate links and
34 class marginals. [Every changed-model field is independently checked](h5-staged-cog-candidate-and-projections-20261107/round-model-checks.json)
before its call. That call returns **UNKNOWN**, with no incumbent, after
**8.030114 seconds** against its eight-second slice. The **0.030114-second
overrun is preserved**. The pipeline stops immediately; rounds 2 and 3 do not run.

[The complete process](h5-staged-cog-candidate-and-projections-20261107/closed-pipeline-process.json) closes all nine
processes with zero active descendants. Peak aggregate committed memory is
**1,009,483,776 bytes**, below 2 GiB. Charged initial preparation is 5.105639 s;
algorithm/shared totals are **27.116847 / 27.155075 seconds** including it.
No candidate passes full source geometry, no native call runs, and no
continuous or whole-allocation exclusion is claimed.

## Fresh exact safe-region projections

The new repair hypothesis retains this candidate's **28 selected legal modes**
and allows all 56 translation coordinates to move. It is a different convex
construction from either closed staged model. [Preparation](h5-staged-cog-candidate-and-projections-20261107/projection-preparation.json)
clips all **303 certified source regions** against their complete relative
coordinate bounds using rational arithmetic; four resulting sets are empty.

[Independent projection readback](h5-staged-cog-candidate-and-projections-20261107/projection-audit.json) reconstructs
the regions by enumerating pairwise boundary-line intersections and verifies
all **1,055 exact vertices**. It rechecks **470 pocket-plane implications for
real coordinates** and **557 retained-halfplane original-source support proofs**.
This establishes that relaxing coordinate integrality does not discard the
source safety margins of the selected regions.

For every actual candidate pair difference, every nonempty region of its
selected mode class receives an exact closest point. The auditor verifies
**18,882 projection optimality certificates**: exact membership and squared
distance, plus the convex variational inequality against every region vertex.
Exact distance and deterministic kind/id ordering select one region per pair.
**226 cog pairs already lie in a certified region; 32 require relative motion.**
Every one of 268 orthogonal component pairs retains an already satisfied
source-safe axis separator, independently reconstructed from original mode
offsets. No new solver is invoked during this preparation.

[The complete projection process](h5-staged-cog-candidate-and-projections-20261107/projection-process.json) takes
**2.767059 seconds** to prepare; its separate complete audit takes 4.146106 s.
Both stages close normally. These projections propose compatible individual
pair requirements; they do not prove that all choices can be satisfied together.

## Next one-call convex repair

[The next-model specification](h5-staged-cog-candidate-and-projections-20261107/next-step.json) uses 56 original
translation variables plus 56 absolute-motion auxiliaries, minimizing total
translation change from the candidate. Keep every selected source mode's stock
bounds, all four relative-domain bounds and all retained planes for each chosen
cog region, all 268 orthogonal separators, and the cog X-order chain needed by
the nonnegative relative-X domains. Eliminate canonical coordinates exactly
through their signed-permutation matrices and shifts.

Every model row, numeric scaling and pinned solver control requires independent
checking before **one** newly frozen call. [The complete charge before its
model build](h5-staged-cog-candidate-and-projections-20261107/next-preparation-charges.json) is **29.922133 seconds**:
the entire consumed 27.155075-second candidate pipeline, including both rounds
and its original preparation, plus complete projection preparation. The original
preparation must not be counted twice, and the new complete build still counts.

No repair model, LP call or valid layout is prepared here. Any infeasibility
would apply only to these selected modes and convex-region choices, without
excluding other regions, the continuous source domain or any whole allocation.
A returned candidate still requires all66 original-source checks, native/material
validation, production integration and the unchanged full H5 matrix.

[The preceding checkpoint reached main 548f5b40 normally](h5-staged-cog-candidate-and-projections-20261107/main-push-receipt.json)
after all six prior CI checks passed, preserving all 52 remote files and updating
the working branch atomically. [Current main CI at review](h5-staged-cog-candidate-and-projections-20261107/main-ci-at-review.json)
is preserved; no live run is cancelled. H2 retains its original gate and unopened
reserved vectors. Production, READMEs and release assets are unchanged.

[The archive](h5-staged-cog-candidate-and-projections-20261107/raw-manifest.json) contains 103
canonical members and 2,100,529 ZIP bytes.
[Historical references](h5-staged-cog-candidate-and-projections-20261107/external-evidence.json) and
[source bindings](h5-staged-cog-candidate-and-projections-20261107/source-bindings.json) preserve all consumed evidence.
The prior hash-bound invalid sealer source remains raw historical evidence,
with its expected syntax failure checked; no frozen failure bytes are edited.
Independent archive verification is required before commit.
