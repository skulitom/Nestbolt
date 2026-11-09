# Complete possible-node closure — 2026-11-09

**One complete audited closure round excludes 13 additional bracket-position cells.**
Both fixed29 choices `[0,5,10]` and `[5,10,11]` remain unresolved, with
**8,569 current nodes**. The earlier 453/455 whole-choice exclusions stand,
including 428 at zero clearance. H2/H5 remain open at **60% completed milestone weight**.

## Complete conservative coverage

The [previous checkpoint](h5-complete-reference-capacity-20261109.md) independently
verified the complete physical area partition and removed 321 bracket cells.
This proof consumes those reduced masks and every source signature. It does not
rerun the geometric partition. [The complete plan](h5-possible-node-closure-20261109/complete-plan.json) and
[independent preflight](h5-possible-node-closure-20261109/plan-audit.json) account for all 151,597 original
physical records, 87,484 distinct family signatures and 3,138 representative rows.

For an uncovered-query mask U, a possible covering-node set P is the initial
family universe intersected with every forbidden-node row indexed by U.
Every actual covering node must belong to P. The producer constructs that
intersection; the independent auditor checks each node against its allowed-query
column. Reprojecting P reproduces each original signature exactly. Restricting
P by the reduced active mask gives a conservative upper cover of current source
geometry. P is not a placement, and these bounds are not exact geometric unions.

[Exhaustive controls](h5-possible-node-closure-20261109/closure-controls.json) compare 4,096 three-node,
three-query cases to the union of every set realizing each signature. They
check 32,768 active-mask restrictions and 8,192 signature replays, including
noncompact positions across machine words. [All 88 closure batches](h5-possible-node-closure-20261109/all88-closure-batches.json)
pass their independent audits: 223,780,973 node memberships,
174,968 original/restricted replays and every one of 87,484 signatures.
17,434 signatures tighten after the earlier 321 removals.

## Complete conditional results

[All 50 query batches](h5-possible-node-closure-20261109/all50-query-batches.json) verify 9,414 conservative
conditional area bounds. The producer sums positive covered areas; the auditor
subtracts uncovered losses from each original physical piece. Every new bound
is at most its corresponding prior bound. [The reconciliation](h5-possible-node-closure-20261109/reconciliation.json)
checks all 5,070 remaining bracket mapping targets against the raw graph rows.
Only graph-row subset implications transfer; no pose-specific geometry transfers.
[Every query result](h5-possible-node-closure-20261109/all3138-query-results.json) is preserved.

| Omitted sites | New bracket cells excluded | Remaining nodes | Brackets / inserts | Global joint upper (mm²) |
|---|---:|---:|---:|---:|
| [0, 5, 10] | 0 | 3801 | 2118 / 1683 | 497,091.028543 |
| [5, 10, 11] | 13 | 4768 | 2939 / 1829 | 484,740.614909 |

The [final independent audit](h5-possible-node-closure-20261109/checkpoint-audit.json) reconstructs the seed
removals and all six conservative global bounds from complementary losses over
the original physical pieces. Both joint bounds remain above 478,384 mm².
These masks include only the new audited deficit seeds; no additional clique
propagation or fixed point is claimed. The common-line outer envelopes reserve
holes, and all 90 original cutting holes remain. No ordinary part-in-hole or
whole-allocation exclusion follows.

## Closed work and next step

All [281 new numerical processes](h5-possible-node-closure-20261109/process-summary.json) and
[191 inherited processes](h5-possible-node-closure-20261109/inherited-process-summary.json) are terminal
with zero descendants. The three inherited failed producers remain preserved.
Workers use CCD1 logical processors 16–31, one BLAS/OMP/MKL thread and a 2 GiB
Windows Job cap. Every new worker has a 20 or 30 s hard limit. Consumed
preparation is **1215.373242 s**. No optimizer, timer reset or timed H5 pass follows.

[Next](h5-possible-node-closure-20261109/next-step.json), check clique implications and assess further
complete restrictions of the already certified possible-node sets. No next
round is prepared. All 440 whole-job allocations, full 66-part source/native/
material validation, production integration and the H5 matrix remain open.
The valid 64-part layout stays best; the separate eight older first32 and
680 five-column cores stay closed. Product, README and releases are unchanged.

The preceding checkpoint is committed as `4d73b18a`. Main remains at `d6a8cecf`;
[its CI at review](h5-possible-node-closure-20261109/main-ci-at-review.json) has 6 passed / 0 live jobs.
Both evidence commits await the ordinary push gate. [Archive checks](h5-possible-node-closure-20261109/archive-checks.json),
[manifest](h5-possible-node-closure-20261109/raw-manifest.json), [source bindings](h5-possible-node-closure-20261109/source-bindings.json),
[historical references](h5-possible-node-closure-20261109/external-evidence.json) and [runtime pins](h5-possible-node-closure-20261109/runtime-bindings.json)
preserve the full evidence chain.
