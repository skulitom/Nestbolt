# Source-component unions exclude thirteen arrangements — 2026-11-06

Independent continuous-source replay excludes **13 more fixed29/cog
arrangements**, leaving **39 of the original 455** (416 excluded).
All **440 whole-job allocations** remain; H2/H5 remain open at **60%**
completed milestone weight.

## Stronger exact source conflicts

The [previous joint model](h5-joint-optional-trees-20261106.md) could prove a
cell pair conflicting only when one pair of source-inner rectangles overlapped
for every anchor pair. The new predicate checks whether the **union** of all
component collision regions covers the entire closed relative-anchor box.
Different component pairs may protect different parts of that box.

Collision rectangles are open. Exact X boundary/open-interval classes and
strictly overlapping Y intervals prove union coverage. Independent replay
instead checks every Cartesian boundary/open-interval class with doubled
integer samples, including degenerate axes and touching open boundaries.

[The probe audit](h5-union-augmented-proofs-20261106/probe-audit.json) verifies **675 controls and all
3,840 pairs** in the prior 32 graph witnesses. It finds **44 new pair conflicts**,
invalidating 29 particular witness selections, without excluding their whole
arrangements. The first audit incorrectly expected 711 controls; it stopped
before checking witnesses. Its source and [failure record](h5-union-augmented-proofs-20261106/audit-failure.json)
are preserved. A separate version corrects only the expected count
(1 empty + 36 singles + 630 pairs + 8 hand cases = 675) and passes.
The unchanged preparation process was not rerun.

[The full-domain edge audit](h5-union-augmented-proofs-20261106/edge-audit.json) then verifies
**22,639 genuinely new bracket/bracket conflicts** across all 52 remaining
arrangements, using **610,579 exact Cartesian class checks**. Every original
bracket and insert cell remains in its complete source cover. Seven bounded
scans stop early; their verified edge prefixes are safe. The audit claims
every stored edge is correct, not that every possible new edge was found.
Missing edges only weaken this necessary model.

## Augmented joint proof trees

Every case has new source-certified constraints, justifying a distinct
bounded joint model. Integer vector operations rebuild the old single-pair
edges; the frozen verified union edges strengthen them. The model still
requires eight brackets and eight inserts, with complete family clique
bounds, mandatory support removals, and exhaustive include/skip branches.

[Independent source and tree replay](h5-union-augmented-proofs-20261106/tree-audit.json) verifies
all **22,639 new edges again**, plus:

- **20,162 records**, 3,046 branching cliques and 15,512 closed count leaves;
- **8,830 mandatory covers** and 551,955 ordered removals;
- **4,694,358 mandatory-support checks** and 7,653,327 clique-pair checks;
- **2,814,228 distinct ordered source-inner pair evaluations**.

The fully closed trees exclude omitted-site choices **[0,5,9], [0,5,14],
[0,10,12], [0,10,13], [0,10,14], [4,9,14], [4,10,12], [4,10,14],
[6,11,12], [7,12,13], [8,13,14], [9,11,12] and [10,12,14]**.
The earlier joint-witness case [4,9,14] closes at its root under the stronger
constraints; its historical witness and earlier process remain unchanged.

These are continuous zero-clearance exclusions conditional on the fixed29
core and current cog poses. They do not exclude other core placements,
changed cog poses or any whole-job allocation.

## Open cases and recorded limits

[The retained frontier](h5-union-augmented-proofs-20261106/remaining-fixed29-choices.json) contains
**27 necessary joint graph witnesses and 12 time/node-limited cases**.
The [witness cells](h5-union-augmented-proofs-20261106/joint-graph-witnesses.json) are not source-valid
placements. Every partial tree retains explicit open leaves and supplies
no exclusion. All earlier processes remain closed.

[Complete preparation times](h5-union-augmented-proofs-20261106/process-ledger.json) are
**0.259107 s** for the probe, **12.011483 s** for the added edges and
**18.865523 s** for the stronger trees. Successful independent audits take
0.589385, 3.024228 and 13.847036 s. The failed count audit is preserved separately.
All declared complete-case and process caps pass. Search/scan cutoffs remain
recorded separately from overruns. No placement solver or native call runs.

The [next geometric check](h5-union-augmented-proofs-20261106/next-step.json) will test whole candidate
cells against original-source convex cog pieces, rather than only their
inscribed rectangles. A strictly contained closed anchor cell in a convex
source collision polygon can be removed by an exact corner/halfplane proof.
This requires original-source piece and transform certification, correct
omitted-site filtering, and complete-domain accounting. No such new pruning
is claimed yet, and no unchanged closed graph will be rerun.

These diagnostics do not establish a complete construction within 60/90
seconds. All consumed preparation remains chargeable before a construction
claim. Full66 original-source validation is required before native/material
checks, production integration and the H5 matrix.

Main 8a765828 has five successful CI jobs while Windows native checks still
run in [CI 42300921299](https://github.com/skulitom/Nestbolt/actions/runs/42300921299)
at report preparation. Local proof checkpoints wait for all six jobs and
aggregate success before a normal push. No live run is cancelled.
Production code, README and release assets are unchanged; H2 retains its
original gate and unopened reserved vectors.

[The manifest](h5-union-augmented-proofs-20261106/raw-manifest.json) contains 180 new canonical
members and 3,265,013 compressed bytes. [External references](h5-union-augmented-proofs-20261106/external-evidence.json)
and [source bindings](h5-union-augmented-proofs-20261106/source-bindings.json) preserve exact inputs.
Independent archive readback verifies every new/reused member and local
report link before commit.
