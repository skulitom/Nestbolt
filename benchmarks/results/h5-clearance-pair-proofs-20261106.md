# Required-clearance pair exclusions — 2026-11-06

Complete independently replayed trees exclude fixed29/cog arrangements
**[0,5,13] and [5,9,10] at the original required 0.2 mm clearance**.
The frontier falls from 28 to **26**, with **429 of 455** excluded at required
clearance. The earlier 427 exclusions remain valid even at zero clearance;
the two new proofs make no such claim. All 440 whole-job allocations remain.
H2/H5 stay open at **60% completed milestone weight**.

## Source-distance pair certificates

For each pair of retained anchor cells, derive the complete closed box of
relative anchor positions. A component collision rectangle is the exact
difference of the two certified source-inner rectangles.

Expand that rectangle by an axis square of radius **140 µm**. Its maximum
squared Euclidean norm is **2 × 140² = 39,200 < 40,000 = 200²**.
Thus every point of the expansion has source distance strictly below the
original 200 µm requirement. Coverage by a union of open expanded rectangles
proves that every anchor pair violates required clearance, even if the same
pair has no zero-clearance overlap certificate.

[Independent edge replay](h5-clearance-pair-proofs-20261106/edge-audit.json) checks **22,610 genuinely
new conflicts** using 306,186 exact Cartesian boundary/open-interval classes:
11,490 bracket/bracket, 10,272 bracket/insert and 848 insert/insert pairs.
Every endpoint remains in its complete certified parent domain, and every new
edge is absent from both prior single-component and saved union conflicts.

All 28 cases become stronger. Thirteen scans report complete; fifteen stop at
their frozen limits and retain only verified prefixes. The audit proves edge
safety, not augmentation completeness. Missing edges weaken the necessary
model and never justify deleting a source placement.

## Independent complete-tree replay

[The tree audit](h5-clearance-pair-proofs-20261106/tree-audit.json) checks **15,668 records**, including
2,106 branching cliques, 12,874 closed count leaves and 6,772 mandatory covers.
It verifies 559,564 ordered removals, 5,029,133 mandatory support pair checks,
8,893,595 clique pairs and 2,180,969 distinct ordered source-inner evaluations.

The replay independently reconstructs every include/skip branch and propagates
only conflicts with all members of a nonempty mandatory group. It rechecks
the 22,610 new edges, 13,054 prior union edges, all 45 clearance root removals
and five inherited source-union removals. The combined edge replay checks
652,832 Cartesian classes.

Only the two completely closed trees exclude their arrangements. Five
[necessary graph witnesses](h5-clearance-pair-proofs-20261106/joint-graph-witnesses.json) and twenty-one
cutoff cases remain in the [26-case frontier](h5-clearance-pair-proofs-20261106/remaining-fixed29-choices.json).
Neither a graph witness nor a partial tree is a source placement or an exclusion.
The fixed core and current cog poses define this proof's scope; other whole-job
allocations and changed placements remain open.

## Timing, publication and next work

[Complete preparation](h5-clearance-pair-proofs-20261106/process-ledger.json) takes **10.627570 s**
for edge generation and **22.117861 s** for the distinct 28-case trees.
Independent audits take 1.509956 and 9.587673 s. Complete-case and process
overruns are zero. Every process is closed; none is extended or repeated.
There are no placement solver/native calls or full construction budget claims.

[The previous two checkpoints reached main](h5-clearance-pair-proofs-20261106/main-sync-receipt.json)
at e7585660 after all six checks on f543f082 passed. The normal atomic
fast-forward also updated the working branch and preserved all 52 newer remote
README/comparison/navigation files. The new
[main CI run](https://github.com/skulitom/Nestbolt/actions/runs/42310587794)
was queued when the receipt was written.

[The next method](h5-clearance-pair-proofs-20261106/next-step.json) assesses required-clearance root
pruning against all 29 fixed original core rectangles. Every proposed removal
will need a complete exact source-distance union certificate; unproved cells
and every source alias must remain. A new bounded tree requires genuinely
smaller independently audited domains.

The archive has 91 canonical members and **3,137,800 bytes**. It
preserves every new script, process and proof, with hash-verified parent archive
references for reused source evidence.
