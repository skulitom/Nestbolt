# Complete refined frontier — 2026-11-06

All **26 refined fixed29/current-cog arrangements remain unresolved**.
No new whole arrangement is excluded. The total remains 429 of 455 excluded
at required 0.2 mm clearance, including 427 excluded even at zero clearance.
All 440 whole-job allocations remain, and H2/H5 stay open at **60% completed
milestone weight**.

## Complete source covers

[The authoritative cover audit](h5-frontier-refined-proofs-20261106/cover-audit-v2.json) independently
verifies the other 25 survivors, omitting the previously refined [4,5,10] case.
Every one of **18,854 retained parent boxes** is covered by its closed
Cartesian children, including shared boundaries and all source aliases.
There are **75,416 children**.

Exact present-cog source collision polygons plus the certified 199 µm diamond
remove **2,794 children** at the original 200 µm clearance. The checker replays
134,112 strict corner halfplanes. All unproved children remain, leaving
38,298 bracket and 34,324 insert nodes across the 25 cases.

## Preserved index correction

The [original audit](h5-frontier-refined-proofs-20261106/cover-audit-v1.json) verified geometry correctly,
but its inner child loop reused the outer case-index variable. Emitted
refinement indices consequently contained child-node numbers.
Graph preparation failed during input hashing, before writing a plan or
constructing any graph.

[The correction record](h5-frontier-refined-proofs-20261106/index-correction.json) preserves that audit,
the failed process, its stderr and hashes. Audit-v2 uses a separate case index
and replays every geometry check. A distinct versioned graph preparation
consumes the corrected indices with unchanged limits. The original source
preparation was not repeated; the failed graph preflight remains closed.

## Every-pair graphs and bounded trees

[Independent graph reconstruction](h5-frontier-refined-proofs-20261106/graph-audit.json) checks all
**110,803,502 unordered child pairs**, 15,782,954 ordered parent pairs and
every graph bit. It preserves all parent source constraints and verifies
**6,172,577 genuinely new child conflicts**. It also replays 30,434 parent
union edges across 559,898 Cartesian classes and 5,742,953 pairs in each
complete initial/root clique cover. No root bound falls below the required
eight parts in either family.

Each new model receives one fresh tree with frozen limits: 1.6 s search,
2 s complete case, 1,500 expanded nodes, 45 s global search, 55 s preparation
and 65 s process. The earlier [4,5,10] tree is not repeated.

[Independent candidate-set replay](h5-frontier-refined-proofs-20261106/tree-audit.json) checks
**11,716 records**, 593 branch cliques, 9,670 closed count leaves, 1,802
mandatory covers and **666,103 ordered removals**. It verifies 25,127,284
support pairs, 83,049,995 clique pairs and 17,515,135 distinct graph pairs.
All trees stop with open leaves: **1,453 in total**, with no refined graph
witness and no whole-arrangement exclusion.

[The full frontier](h5-frontier-refined-proofs-20261106/remaining-fixed29-choices.json) therefore stays
at 26. [Classification](h5-frontier-refined-proofs-20261106/frontier-classification.json) preserves the
earlier single refined cutoff and all 25 new cutoffs. A partial tree is neither
an exclusion nor a source placement.

## Complete costs and publication

[The complete preparation ledger](h5-frontier-refined-proofs-20261106/process-ledger.json) includes
10.539071 s for covers, **0.316752 s for the preserved failed preflight**,
7.361615 s for corrected graphs and 44.052088 s for the fresh trees.
The authoritative cover, graph and tree audits take 1.103694, 34.856346 and
45.716787 s. Final complete-case/process caps pass. No placement solver/native
calls or full construction 60/90-second budget claims are made.

[The previous checkpoints reached main](h5-frontier-refined-proofs-20261106/main-sync-receipt.json)
at **3046006d** through a normal atomic fast-forward after all six checks on
e7585660 passed. The working branch also advanced and all 52 newer remote
README/comparison/navigation files remained intact. The receipt records the
new [main CI run](https://github.com/skulitom/Nestbolt/actions/runs/42314416896).

## Next certificate method

[The assessment](h5-frontier-refined-proofs-20261106/sat-method-assessment.json) proposes a distinct
Boolean certificate workflow over the complete necessary graphs: cell
selectors, certified pair incompatibilities and verified family cardinalities.
Any legal continuous packing must satisfy that formula.

The primary [PySAT API documentation](https://pysathq.github.io/docs/html/api/solvers.html)
documents proof extraction and limited solving.
[DRAT-trim](https://github.com/marijnheule/drat-trim) documents independent
checking of an unsatisfiability proof against its exact DIMACS formula.
Selected versions and solver licences still need pinning and controls.

[Before any call](h5-frontier-refined-proofs-20261106/next-step.json), independently verify every formula
clause, cardinality semantics, valid/tampered checker controls and frozen
resource limits. An UNSAT status alone is insufficient; a complete independently
accepted proof is required. SAT yields only a necessary graph witness.
UNKNOWN, invalid or truncated proofs remain unresolved. No such model or
SAT call has run, and no closed tree will be extended or repeated.

The archive contains 332 canonical members and **12,685,492 bytes**.
It preserves both audit versions, the failed preflight, all exact graphs and
tree records, and hash-bound historical source evidence.
