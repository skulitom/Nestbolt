# Exact circular clearance and factored graph models — 2026-11-07

New source proofs remove **three impossible cells** and add **15 pair conflicts**
across the four remaining fixed29/current-cog arrangements. Every resulting
graph is genuinely stronger than its previous closed model. A more compact
Boolean encoding preserves all original conflicts, but its four new bounded
calls still reach their proof-size limits. **No further arrangement is excluded.**
The frontier stays at **four**, with **451 of 455 excluded at original 0.2 mm
clearance** and 427 even at zero clearance. All 440 whole allocations and full66
validation remain open. H2/H5 stay open at **60% completed milestone weight**.

## Exact unions on complete refined cells

[Independent subdivision replay](h5-exact-circle-forest-20261107/union-audit.json) checks 10,900 distinct
queries and 10,914 tree records on the four current refined domains. Both closed
children exactly cover every split, including their shared boundary. Three
closed leaves have 288 exact corner halfplane checks. One whole source cell
is proved covered by the union of the sixteen-direction cog collision polygons;
it is removed from [0,5,10]. All other cells remain, including every source
alias and boundary. The scan has seven exact splits, maximum depth two and no
query overrun. Preparation/audit processes close in 1.571373/1.747699 seconds.
The other three unchanged cases receive no call at this stage.

## Exact Euclidean clearance

[The new circular-distance audit](h5-exact-circle-forest-20261107/circle-audit.json) uses unexpanded
original cog/source-inner collision hulls and source-inner rectangle differences.
For each removed cell corner it supplies an exact rational point inside a source
hull or on one of its edges at distance strictly below 200 µm. Convex combinations
of those points stay inside the same hull, and convex combinations of their
error vectors stay inside the clearance disk. This proves the whole closed cell
impossible. Eight exact corner certificates remove two further cells, one each
from [5,10,11] and [10,11,12].

For pair conflicts, independent pointwise clamping checks all four corners of
the complete relative-anchor box against one original source-inner difference
rectangle. All 60 exact squared-distance tests are below 40,000 µm², certifying
15 new incompatible pairs. The same convexity argument covers the full box.
This uses the original required clearance, with no increased gap, numerical
validator guard or double expansion. All inherited conflicts remain; all
33,803,472 retained unordered graph pairs and complete clique partitions pass.
Preparation/audit processes close in 3.559523/0.888288 seconds.

## A compact, equivalent conflict encoding

A complete binary interval tree represents contiguous sets of original cell
selectors. Each internal segment has two forward child-to-parent implications.
Selecting a leaf therefore forces every ancestor segment true. Each cell's
larger-index conflict neighbors are partitioned into disjoint complete segments;
a negative cell/segment clause forbids exactly those original conflicts.
No segment contains a non-neighbor, every conflict is covered exactly once and
every internal segment is verified as the union of its two children.

Conversely, assigning each segment the actual OR of its leaves extends every
original independent set to these auxiliary variables. The existential
projection onto the original selectors is therefore exactly the original pair
model. Complete source conflict-clique partitions and explicit group ORs still
require eight selected brackets and eight selected inserts; source cell capacity
remains one. No original geometric constraint is omitted.

[Exhaustive controls](h5-exact-circle-forest-20261107/encoding-controls.json) verify every one of the
1,024 simple five-node graphs, all 32,768 original selector assignments and all
524,288 auxiliary extensions. The full research model audits independently
verify **15,208,033 original graph conflicts** represented by **2,637,822 factored
clauses**, including all child implications. Total model clauses are
**2,658,385**, with 1,088 threshold gates and 16,267 source cell-capacity proofs.
Every graph pair, segment cover, clause and threshold truth table is checked.

## Four closed calls and no accepted certificate

[The four-case batch](h5-exact-circle-forest-20261107/batch-process.json) retains the frozen per-case
60-second search, one-million-conflict, 64 MiB binary-proof and 2 GiB aggregate
memory limits. Complete process/stage caps and Windows Job Object descendant
closure are enforced. All four calls stop at the proof-byte limit. The complete
batch closes in **125.312357 seconds**, with zero active descendants.
[Per-case results](h5-exact-circle-forest-20261107/case-results.json) preserve every limit and original
model hash. No SAT witness, usable UNSAT response, accepted proof or source-valid
placement is claimed. These calls will not be repeated, reseeded or extended.

First read-only inspections of the [previous four limited streams](h5-exact-circle-forest-20261107/previous-stream-inspection.json)
and [these four new streams](h5-exact-circle-forest-20261107/current-stream-inspection.json) find no complete
prefix ending in an added empty clause. Every stream ends in truncated data;
no proof-checker call or exclusion follows. All original bytes stay preserved.

The [remaining graphs](h5-exact-circle-forest-20261107/remaining-source-graphs.json) correspond to empty
cog sites **[0,5,10], [5,10,11], [10,11,12] and [11,12,13]**.
[Next](h5-exact-circle-forest-20261107/next-step.json), assess selective complete refinement of anchor
cells or exact geometric constraints involving more than two cells. Preserve
all closed boundaries and aliases, and require genuinely new source constraints
before any distinct bounded call. All consumed preparation remains recorded;
no full-job 60/90-second construction claim or native validation follows.

The preceding verified checkpoint reached **main 909db92e** by normal atomic
fast-forward after all six checks and aggregate CI42321641931 passed. The
[push receipt](h5-exact-circle-forest-20261107/main-sync-receipt.json) verifies all 52 reconciled remote
files, unchanged refs before push and ordinary ancestry. No live run was
cancelled. New CI42325413099 is tracked separately; no release or registry
version is added.

[The manifest](h5-exact-circle-forest-20261107/raw-manifest.json) contains 238
new canonical members in 2 ZIP parts, totaling
63,168,157 bytes. [Historical references](h5-exact-circle-forest-20261107/external-evidence.json)
and [source bindings](h5-exact-circle-forest-20261107/source-bindings.json) preserve original dependencies.
Independent archive verification is required before commit.
