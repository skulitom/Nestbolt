# Global-capacity search and smaller initial model — 2026-11-07

The complete global-capacity construction closes its sole call **UNKNOWN**,
with no placement. All model and response audits pass, and the overall time
and memory limits hold. A distinct staged approach now has a fully audited
**1,332-variable, 4,712-constraint initial model**, with all original movers
and modes retained. Its source-check/cut pipeline has not been prepared or run.
Four fixed arrangements and all 440 allocations remain; H2/H5 stay open at
**60% completed milestone weight**.

## Complete global model and closed response

[The exhaustive model audit](h5-cog-capacity-search-and-initial-model-v2-20261107/closed-model-audit.json) verifies
**28,254 variables and 60,632 constraints**. All 258 detailed cog interactions
and all 120 orthogonal-owner interactions remain. The new global system adds
2,460 optional affine intervals, two cumulative constraints and one NoOverlap2D
constraint. Every interval shares its original owner coordinates and mode
selector. Both axes and all 172 coarse rectangle alternatives are checked.
The partial twelve-cog control passes both capacity bounds and all 66 coarse
pair checks, while remaining sixteen parts are unplaced in that control.

[Complete preparation and model building](h5-cog-capacity-search-and-initial-model-v2-20261107/closed-model-preparation-charges.json)
take **6.938077 seconds**, including the 2.691284-second complete build process.
The separate complete model audit takes 8.251503 seconds.

[Independent response readback](h5-cog-capacity-search-and-initial-model-v2-20261107/response-audit.json) verifies one
four-worker, seed-zero call with **48.164376 seconds allocated** and
**48.274940 seconds returned**, preserving the **0.110564-second solve-slice
overrun**. It records 148,027 branches and 17,411 conflicts, with no incumbent
or assignment. Preparation-inclusive algorithm/shared totals are
**56.129667 / 56.232693 seconds**, below the original 60/90-second limits.

[The Windows Job closes normally](h5-cog-capacity-search-and-initial-model-v2-20261107/closed-search-process.json), with
all three processes closed and zero active descendants. Peak aggregate
committed memory is **1,981,014,016 bytes**, below 2,147,483,648. The returned
UNKNOWN response proves no continuous or whole-allocation exclusion. This call
is permanently closed and will not be repeated, reseeded or extended.

## Initial model for staged source constraints

The new approach first asks for a necessary assignment using full orthogonal
geometry and globally coupled source occupancy. Detailed cog-pair disjunctions
are introduced only after an actual original-source collision is observed.
This differs from reopening either closed full model: no previous model or
search artifact is consumed, and the new initial model has no detailed cog-pair
choices. A necessary assignment cannot qualify as a valid layout by itself.

[Initial-model readback](h5-cog-capacity-search-and-initial-model-v2-20261107/initial-model-audit.json) verifies every field
of **1,332 variables and 4,712 constraints**. It retains all 28 original movers,
108 mode options, 56 world coordinates, 24 rigid orthogonal components,
640 component links, 268 component-pair separations and 25 valid copy orders.
All 1,564 X-axis and 552 Y-axis source projection intervals, both cumulative
constraints and the 172 optional coarse rectangles remain. There are exactly
zero detailed cog-pair selectors, planes or canonical-coordinate links.

The 36-value partial cog hint satisfies all 47 fully hinted active linear
constraints. Its projection peaks are 75,936 / 88,561 and 98,896 / 148,696 grid
units, and all 66 coarse cog pairs pass. It remains a partial control.
Binary/text equality, actual solver import, every original source-mode domain
and all constraint fields pass independent checks.

[The complete initial build](h5-cog-capacity-search-and-initial-model-v2-20261107/initial-process.json) takes **0.858846
seconds**; its separate complete audit takes 3.043320 seconds. With all consumed
source preparation, [the next pipeline starts with a charge of 5.105639
seconds](h5-cog-capacity-search-and-initial-model-v2-20261107/initial-preparation-charges.json). Closed previous model builds
are not reused, and their outputs are absent from the new runtime input graph.

## Remaining staged-pipeline obligations

[The proposed bounded pipeline](h5-cog-capacity-search-and-initial-model-v2-20261107/next-step.json) allows at most four
strictly changing rounds within the original preparation-inclusive 60/90-second
and 2 GiB limits: first solve at most 30 seconds, later solves at most eight,
each also limited by remaining time with a four-second source-check reserve.
Every dynamic rebuild, in-process audit, source check and solve is charged.

Every returned candidate must reconstruct all 66 original identities and check
1,632 same-sheet pairs, 264 stock edges, 90 holes and 10,026 hole vertices.
Before a later round, every newly failing cog pair must be mapped to its
complete certified source interaction. Keep all previous cuts and independently
audit the entire changed model before its sole call. A stock, fixed-part,
orthogonal-only or already-constrained pair failure is an inconsistency and
stops the pipeline. UNKNOWN, INFEASIBLE, invalid model, no new cut or deadline
also stop it; an unchanged model can never be retried.

No pipeline runner or new solver call is prepared in this checkpoint. These
limits and source-cut obligations must be frozen in executable code before any
call. Source-valid full66, native/material validation, production integration
and the unchanged complete H5 matrix remain required. H2 retains its original
gate and unopened reserved vectors. No release is made.

## Repository evidence

[The preceding two checkpoints reached main 37ede828 normally](h5-cog-capacity-search-and-initial-model-v2-20261107/main-push-receipt.json)
after all six prior checks passed, preserving all 52 remote files. The working
branch was updated atomically. [New main CI at review](h5-cog-capacity-search-and-initial-model-v2-20261107/main-ci-at-review.json)
is preserved; no live run is cancelled. Production and READMEs are unchanged.

[The archive](h5-cog-capacity-search-and-initial-model-v2-20261107/raw-manifest.json) contains 89
canonical members and 3,150,615 ZIP bytes.
[Historical references](h5-cog-capacity-search-and-initial-model-v2-20261107/external-evidence.json) and
[source bindings](h5-cog-capacity-search-and-initial-model-v2-20261107/source-bindings.json) retain all consumed evidence.
The pre-execution sealer-generator quoting error is retained as raw evidence. A first packaging pass then stops while trying to parse that known-invalid source, before writing any archive or documentation. Version2 verifies its exact hash and expected syntax failure, retains it as data and otherwise keeps strict helper parsing. Both failures and corrections are archived; no model, search or frozen evidence is repeated or changed. Independent archive verification is required before commit.
