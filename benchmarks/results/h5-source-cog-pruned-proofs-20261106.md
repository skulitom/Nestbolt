# Original cog polygons exclude eleven arrangements — 2026-11-06

Independent source and tree replay excludes **11 more fixed29/cog
arrangements**, leaving **28 of the original 455** (427 excluded).
All **440 whole-job allocations** remain; H2/H5 remain open at **60%**
completed milestone weight.

## Exact original-source collision polygons

The [previous union-augmented model](h5-union-augmented-proofs-20261106.md)
left 39 arrangements. The new preparation uses the original cog's certified
21 convex pieces, rather than only rectangles inscribed inside them.
Source coordinates, binary64 cosine/sine and translations are represented
exactly as rationals and scaled to a common integer denominator.

For each moving source-inner rectangle and cog piece, their Minkowski
collision polygon contains the anchor positions where their interiors overlap.
[Independent geometry replay](h5-source-cog-pruned-proofs-20261106/polygon-audit.json) verifies **378
exact convex collision polygons**, **1,800 transformed source vertices**
and **172,800 hull halfplane checks**. Each hull has source-derived vertices,
is strictly convex, and contains every vertex difference.

Every removed closed anchor cell has all four corners strictly inside one
of these convex polygons for a cog site actually present in that arrangement.
The audit checks **173 certificates and 5,536 strict corner/halfplane tests**
over **3,848 distinct source cells**. It verifies the complete mapping to
all 39 original bracket/insert domains, including aliases, omitted-site bits,
closed boundaries and degenerate cells.

This removes **847 node occurrences**, making every arrangement's domain
strictly smaller. All unproved cells remain, so no claim of exhaustive
polygon pruning is needed. The retained original clique counts alone add
no whole-arrangement exclusion.

## Proof trees over the retained domains

A distinct bounded model retains all earlier single-component and union
conflicts while starting from these newly source-certified domains.
[Independent complete tree replay](h5-source-cog-pruned-proofs-20261106/tree-audit.json) checks every
root removal again, including **27,104 strict corner tests**, then verifies:

- **19,443 records**, 2,712 branching cliques and 15,913 closed count leaves;
- **8,362 mandatory covers** and 598,126 ordered removals;
- **5,166,413 mandatory-support checks** and 8,840,330 clique-pair checks;
- **2,414,108 distinct ordered source-inner pair evaluations**.

The fully closed trees exclude omitted-site choices **[0,4,5], [0,4,10],
[0,5,6], [1,5,10], [4,11,12], [4,12,13], [4,13,14], [5,6,10],
[5,12,13], [5,13,14] and [6,10,11]**.

These are continuous zero-clearance exclusions conditional on the fixed29
core and current cog poses. They do not exclude changing those placements
or any whole-job allocation.

## Open outcomes, limits and next method

[The retained frontier](h5-source-cog-pruned-proofs-20261106/remaining-fixed29-choices.json) has
**10 necessary joint graph witnesses and 18 time/node-limited cases**.
The [saved witness cells](h5-source-cog-pruned-proofs-20261106/joint-graph-witnesses.json) are not
source-valid placements. Every incomplete tree retains open leaves and
supplies no exclusion. All prior processes remain closed.

[Complete preparations](h5-source-cog-pruned-proofs-20261106/process-ledger.json) take **0.931841 s**
for source-polygon pruning and **20.396204 s** for the new trees.
Independent audits take **1.310035 and 9.474546 s**. The unchanged fresh
tree limits are 0.70 seconds of search within 0.75 seconds per complete case,
1,500 expanded nodes, and 50/55/65-second global search/preparation/process
caps. All declared complete-case and process caps pass. Search cutoffs are
preserved separately. There are no placement solver or native calls.

[The next geometric proof](h5-source-cog-pruned-proofs-20261106/next-step.json) will test whether several
original-source collision polygons jointly cover a retained anchor cell.
A bounded binary subdivision can certify this through closed child boxes,
each strictly inside a present-cog polygon. Its independent replay must prove
that children cover their parent exactly and every final leaf has a source
certificate. Open leaves, uncovered sample points and cutoffs preserve the
entire unproved parent cell. Only new certified removals would justify a
stronger bounded model; no existing process may be extended.

The preceding five proof checkpoints were [pushed normally](h5-source-cog-pruned-proofs-20261106/main-sync-receipt.json)
to main and the working branch as **f543f082**, after all six jobs and aggregate
success in [CI 42300921299](https://github.com/skulitom/Nestbolt/actions/runs/42300921299).
All 52 newer remote files remain preserved. [New CI 42306548173](https://github.com/skulitom/Nestbolt/actions/runs/42306548173)
has four successful jobs and two native checks running at report preparation.
This checkpoint waits for that run before another normal push.

These diagnostics do not establish a complete construction within 60/90
seconds. All consumed preparation remains chargeable. Full66 original-source
validation is required before native/material checks, production integration
and the H5 matrix. Production code, README and release assets are unchanged;
H2 retains its original gate and unopened reserved vectors.

[The manifest](h5-source-cog-pruned-proofs-20261106/raw-manifest.json) contains 116 new canonical
members and 3,682,336 compressed bytes. [External references](h5-source-cog-pruned-proofs-20261106/external-evidence.json)
and [source bindings](h5-source-cog-pruned-proofs-20261106/source-bindings.json) preserve exact inputs.
Independent archive readback verifies every new/reused member and local
report link before commit.
