# Continuous exclusions from mandatory cliques — 2026-11-04

Independent source-based proofs exclude **three more fixed29/cog arrangements**:
empty sites **[0,4,14]**, **[5,11,13]** and **[5,11,14]**. The proof covers
continuous anchors and remains valid at zero clearance. The fixed29 frontier
falls from **259 to 256** choices: **199 of the original 455** are now excluded.
No whole-job allocation is excluded; all **440** remain. H2/H5 stay open at
**60% completed milestone weight**.

This supersedes the unresolved status of these three arrangements in the
[source-polygon checkpoint](h5-source-polygons-and-joint-frontier-20261104.md).
Its closed grid calls remain preserved. Their responses are not used as
continuous infeasibility certificates.

## Complete continuous covers and mandatory bracket groups

The proof starts with the existing independently certified source-inner
rectangles and full-stock necessary anchor cover. Each eligible bracket box
is divided into closed Cartesian cells at most 50 mm wide and high.
Every legal original mode and continuous anchor remains covered.

[The bracket audit](h5-mandatory-clique-exclusions-20261104/bracket-clique-audit.json) verifies all **357**
cells and **4,721** strict source-inner overlap certificates. Each cell is
self-conflicting. All cells are partitioned into **eight conflict cliques per
arrangement**: every pair within a clique collides for every pair of anchors.
At most one original bracket can occupy each clique. Because eight brackets
are required, every clique must be occupied. This is an upper bound and a
necessary condition, not a packing witness.

## Preserved intermediate bounds

[Initial insert pruning](h5-mandatory-clique-exclusions-20261104/initial-insert-audit.json) removes
**87 / 189 / 127** cells that conflict with every bracket candidate in a
mandatory clique. Complete remaining insert covers are preserved.
[Exact swept-area replay](h5-mandatory-clique-exclusions-20261104/initial-area-audit.json) and
[mandatory bracket occupancy bounds](h5-mandatory-clique-exclusions-20261104/initial-occupancy-audit.json)
also pass, but neither excludes an arrangement. The latter checks **714**
exact component-outside areas and 24 clique minima.

[Bracket consistency replay](h5-mandatory-clique-exclusions-20261104/bracket-consistency-audit.json) then
verifies **232 ordered removals**, with **1,394** strict overlap certificates.
A removed node conflicts with every remaining node in another mandatory
bracket clique. Induction preserves every valid packing. The surviving
bracket-cell counts are **20 / 58 / 47**.

[Insert pruning with those survivors](h5-mandatory-clique-exclusions-20261104/consistent-insert-audit.json)
removes **178 / 202 / 203** of the complete **220 / 259 / 259** insert cells.
The remaining **42 / 57 / 56** cells have certified clique covers of
**9 / 10 / 12** groups. [Recomputed areas](h5-mandatory-clique-exclusions-20261104/consistent-area-audit.json)
and [mandatory occupancy](h5-mandatory-clique-exclusions-20261104/consistent-occupancy-audit.json) are retained
as intermediate necessary bounds. They do not establish the final exclusions.

## Exhaustive joint contradiction

Eight inserts must occupy eight distinct groups in their certified clique
cover. The [final independent replay](h5-mandatory-clique-exclusions-20261104/joint-distribution-audit.json)
enumerates every eight-group selection:

| Omitted cog sites | Insert groups | Complete selections | Contradictions |
|---|---:|---:|---:|
| [0,4,14] | 9 | 9 | 9 |
| [5,11,13] | 10 | 45 | 45 |
| [5,11,14] | 12 | 495 | 495 |

Each selection requires all eight bracket groups and its eight chosen insert
groups. The proof removes a candidate only after verifying that it conflicts
with every currently possible node in another mandatory group. All **549**
selections end with an empty mandatory group. Independent replay checks
**4,618 ordered removals** and **15,087 strict source-inner pair overlaps**.
Every continuous valid packing would survive those necessary eliminations,
so no such packing exists for any of these three fixed arrangements.

These are finite certificates for complete continuous necessary covers,
not a sampled-position or placement-grid exclusion. They assume the same
fixed29 originals and selected twelve reference cog poses. Changed core
placements, changed cog poses and different whole allocations remain open.

## Timing, evidence and next work

All nine complete preparation processes close within their declared caps;
their total is **3.274561 s**. Every intermediate audit, failed-to-exclude bound,
ordered trace and original input is preserved. There are **no placement solver
calls, full66 candidate readbacks or native calls** in this proof sequence.
Independent verification times are recorded separately in the audit files.

[The updated frontier](h5-mandatory-clique-exclusions-20261104/remaining-fixed29-choices.json) retains all
256 unexcluded choices. [The next step](h5-mandatory-clique-exclusions-20261104/next-step.json) extends the
cheap continuous bracket-clique bound to that complete frontier, with full
coverage and pair-certificate replay. Only independently proved bounds may
remove choices; an inconclusive result never establishes a valid packing.
All previous placement calls stay closed.

Full66 source/native/material validation, production integration and the H5
matrix remain required. H2 keeps its original gate and unopened reserved
vectors. Product source, README and release assets are unchanged.

At this checkpoint, [main CI 41928746100](https://github.com/skulitom/Nestbolt/actions/runs/41928746100)
has five successful jobs; Windows checks remain live. Reviewed local
checkpoints await all six jobs and the aggregate result before a normal push.
No live run was cancelled.

[The manifest](h5-mandatory-clique-exclusions-20261104/raw-manifest.json) contains 126 new canonical
members and 333,478 compressed bytes. [External references](h5-mandatory-clique-exclusions-20261104/external-evidence.json)
and [source bindings](h5-mandatory-clique-exclusions-20261104/source-bindings.json) preserve exact historical
dependencies. The independent archive reader verifies all new/reused members,
input hashes and local report links before commit.
