# Individual-cog search and source support halfplanes — 2026-11-07

The complete individual-cog model passes its full audit, but its **sole search
stops at the 2 GiB memory limit without a solver response or placement**.
Every process closes. A distinct source-certified representation is now ready:
one support inequality per convex exterior choice cuts the proposed guarded
geometry planes from **97,284 to 53,070**. Its complete model is not built yet.
Four fixed arrangements and all 440 whole allocations remain; H2/H5 stay open
at **60% completed milestone weight**.

## Complete model and preserved bounded failure

[Full protobuf readback](h5-independent-cog-search-and-halfplanes-20261107/model-audit.json) verifies all **29,310 variables
and 102,383 constraints**, binary/text agreement and an actual OR-Tools import.
The model retains all 28 original movers, twelve individually positioned cogs,
108 source-mode selectors and 56 world coordinates. The 192 cog/orthogonal pairs
have 384 canonical coordinates, 2,304 exact conditional mode links and 288 class
marginals. All 258 cog interactions and all 120 orthogonal-owner interactions
are present; the latter use 24 rigid rectangles, 640 mode links and 268 component
pairs. There are 25 valid identical-copy X-order constraints.

The partial hint contains 6,702 values and satisfies all 380 fully hinted active
constraints. It places only the twelve cogs; it is not a complete layout.
[Complete preparation and model building](h5-independent-cog-search-and-halfplanes-20261107/closed-model-preparation-charges.json)
consume **6.701406 seconds**, including the 3.458427-second full build process.

[The failure audit](h5-independent-cog-search-and-halfplanes-20261107/memory-stop-audit.json) binds the one call's exact
model, parameters, log and Windows Job result. Four workers and seed zero receive
**48.349494 seconds** of solve time. The log reaches search after 9.17 seconds of
presolve, with 29,098 variables and 124,289 constraints in the presolved model.
The calibrated supervisor then reports memory reason 3 and exit 124.

The [closed process](h5-independent-cog-search-and-halfplanes-20261107/closed-search-process.json) records **32.031 seconds**
inside the job and **38.762725 seconds including charged preparation**. Its peak
aggregate committed memory is **2,151,796,736 bytes**, 4,313,088 bytes above the
2,147,483,648-byte monitored threshold. The overshoot remains recorded; this is
not a claim of an instantaneous hard cap. All descendants close with zero active
processes. No incumbent, assignment, source check, result JSON or response protobuf
exists. There is no returned solver status, branch count or solve-duration result
to report; **UNKNOWN and INFEASIBLE are not synthesized**. This call is closed
and will not be repeated, reseeded or extended.

## New original-source support inequalities

The next construction keeps the same source domains and mode-coupled coordinates,
but replaces clipped convex exterior polygons with direct inequalities
`n dot z >= lower`. Candidate integer normals come from exact rational source-hull
differences. For each normal, the lower bound uses the largest actual source
support difference across every applicable mode alias, plus 0.23 mm times an
integer upper bound on the normal's Euclidean length. No floating source symmetry
or clipped-domain boundary is needed to prove this separator safe.

[Independent support readback](h5-independent-cog-search-and-halfplanes-20261107/support-halfplane-audit.json) verifies
**174 candidate halfplanes and 576 exact original-source support proofs**.
Minimum certified Euclidean gap is **0.23000000000000054 mm**. Exact rectangle
intersection checks prove six halfplanes empty in their complete coordinate
domains. Thirteen more are contained in retained choices; every cover chain
terminates at a retained halfplane. No original placement is excluded by a
global infeasibility claim.

The new representation retains **155 halfplanes and 148 unchanged certified
concave pockets**, giving **26,538 expanded choices and 53,070 guarded planes**.
All 66 cog-control pairs still pass: 49 use halfplanes and 17 use pockets.
The complete halfplane preparation takes **0.688040 seconds**. With all prior
source preparation, [the next construction's charge before model building](h5-independent-cog-search-and-halfplanes-20261107/next-preparation-charges.json)
is **3.931019 seconds**. The future complete build must still be charged.

## Preserved audit correction and next model

The first halfplane audit passes all numeric/source/clip/control checks, then
fails an overly broad input-lineage assertion. Historical source provenance
contains 464 older model/search bindings. A [separate correction](h5-independent-cog-search-and-halfplanes-20261107/audit-correction.json)
preserves the original producer wording, failed auditor and process; version 2
records those historical bindings and verifies that the **current failed
individual-cog model and search are absent** from the new geometry's input graph.
All numerical assertions and source geometry bytes remain unchanged. Only the
corrected independent audit is rerun; source preparation and solver calls are not.

[The next full-model plan](h5-independent-cog-search-and-halfplanes-20261107/next-step.json) preserves all owners, modes,
canonical links, class coupling and rigid component checks. Halfplane choices use
lower bounds, while pocket choices retain their upper-bound planes. Every field,
the new partial-control mapping and complete costs must pass independent readback
before one newly frozen call under the same 2 GiB and 60/90-second limits.
No such model or call is opened here. Full66 source/native/material validation,
production integration and the complete unchanged H5 matrix remain required.

[The prior checkpoint reached main c339bc7a normally](h5-independent-cog-search-and-halfplanes-20261107/prior-push-receipt.json)
after all six previous checks passed, preserving all 52 remote files.
[Current CI at report review](h5-independent-cog-search-and-halfplanes-20261107/main-ci-at-review.json) is retained; no live
run is cancelled. Production, READMEs and release assets are unchanged.

[The archive](h5-independent-cog-search-and-halfplanes-20261107/raw-manifest.json) contains 86
canonical members and 3,557,612 ZIP bytes.
[Historical references](h5-independent-cog-search-and-halfplanes-20261107/external-evidence.json) and
[source bindings](h5-independent-cog-search-and-halfplanes-20261107/source-bindings.json) preserve all consumed evidence.
Independent archive verification is required before commit.
