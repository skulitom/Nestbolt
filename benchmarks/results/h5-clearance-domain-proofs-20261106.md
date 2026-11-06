# Source unions and required-clearance domains — 2026-11-06

The new proofs remove **50 more node occurrences** but exclude **no further
fixed29/cog arrangement**. There are still **28 unresolved arrangements**,
with 427 of the original 455 already excluded. All 440 whole-job allocations
remain, and H2/H5 stay open at **60% completed milestone weight**.

## Exact polygon unions

[Independent subdivision replay](h5-clearance-domain-proofs-20261106/union-subdivision-audit.json)
checks 4,721 closed-cell queries against the previously certified original cog
collision polygons. Exact splits cover both closed children, including their
shared boundary. A closed leaf must lie strictly inside one source polygon.
Only a fully closed root removes its original cell.

The audit checks 4,969 records, 124 splits, 36 closed polygon leaves and 1,152
strict halfplanes. Four whole-cell queries close, removing five node occurrences
in four arrangements. The 4,713 uncovered samples are witnesses against this
coverage proof, not valid source placements. Depth limits and unproved siblings
leave their whole cells retained.

## Clearance-aware source geometry

The original job requires **0.2 mm clearance**. New collision polygons add a
closed L1 diamond of radius **199 µm**, contained inside the Euclidean 199 µm
ball. The strict margin to 200 µm means membership proves separation below the
required gap. It does not imply zero-clearance overlap.

[The authoritative v2 audit](h5-clearance-domain-proofs-20261106/clearance-audit-v2.json) independently
checks 1,800 transformed source vertices, 378 exact convex collision polygons,
829,440 hull difference/halfplane checks and ten closed-cell certificates.
All 45 additional node removals are certified; every other parent cell remains.
Together with the five union removals, 27 of the 28 domains become strictly
smaller. The bound is safety evidence; exhaustive pruning is not claimed.

[The first audit](h5-clearance-domain-proofs-20261106/clearance-audit-v1.json) had correct numerical checks
and an explicit false zero-clearance flag, but its generic proof prose wrongly
said “interior overlap”. [The preserved correction](h5-clearance-domain-proofs-20261106/proof-scope-correction.json)
changes that prose to source separation below required clearance. No input,
numerical result or preparation process was changed or repeated.

## New necessary-model trees

[Independent tree replay](h5-clearance-domain-proofs-20261106/tree-audit.json) verifies 18,942 records,
2,648 branch cliques, 15,469 closed count leaves, 8,253 mandatory covers and
564,916 ordered removals. It checks 4,642,924 support pairs, 7,688,682 clique
pairs and 1,936,331 distinct ordered source-inner evaluations.

All 45 new clearance removals and five inherited union removals are retained.
The audit rechecks 12,452 prior union edges across 329,032 exact Cartesian
boundary classes. Optional include/skip branches exhaust the retained domain;
any open leaf prevents an exclusion.

The 27 new trees yield nine [necessary graph witnesses](h5-clearance-domain-proofs-20261106/joint-graph-witnesses.json)
and eighteen cutoff cases. No tree closes completely. The unchanged 28th
arrangement is carried forward without another search; it remains in the
[complete survivor list](h5-clearance-domain-proofs-20261106/remaining-fixed29-choices.json).
No graph witness is a source placement.

## Limits and next work

[Complete preparation processes](h5-clearance-domain-proofs-20261106/process-ledger.json) take
1.433914, 2.162237 and 18.790352 seconds. All process and complete-case caps
pass. The exact tree replay takes 12.827812 seconds. There are no placement
solver or native calls, and no full construction 60/90-second budget claim.
Every process is closed.

[The next method](h5-clearance-domain-proofs-20261106/next-step.json) assesses required-clearance pair
conflicts: expand source-inner component difference rectangles by a 140 µm
axis square, whose maximum Euclidean norm is strictly below 200 µm, then
independently certify coverage of each whole relative-anchor box. Only genuinely
new certified constraints can justify a new bounded tree.

The archive preserves both clearance-audit versions and their correction,
all bounded process records, source bindings, scripts and complete tree records.
Its 134 canonical members occupy **3,862,318 bytes**. Historical inputs
are referenced through hash-verified parent archives.
