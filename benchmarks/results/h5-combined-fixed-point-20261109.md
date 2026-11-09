# Combined conditional fixed point — 2026-11-09

**The complete bracket and insert bounds reach a joint fixed point: no further cells are excluded.**
Both fixed29 choices `[0,5,10]` and `[5,10,11]` remain open with 8,551 cells.
H2/H5 remain open at **60% completed milestone weight**.

## Full scope and independent verification

The [preceding insert proof](h5-complete-insert-capacity-20261109.md) removed 18
cells after the bracket-only fixed point. This stage combines all 3,138 bracket
representative queries and 3,512 direct insert queries under the changed masks.
It preserves original graph array positions and the certified bracket mapping.
The [source audit](h5-combined-fixed-point-20261109/source-preflight-audit.json) verifies all 6,650 rows,
8,551 current targets, 8,721 source self witnesses, 1,848,482 directed clique
edges and 87,484 possible-node records. The two baseline families share the
same prior 8,569-cell masks.

[Width controls](h5-combined-fixed-point-20261109/combined-width-controls.json) compare 425,600 scalar
answers across 128 cases, both family boundaries, the maximum query index
3,833 and large integer carries. Each bracket reference leaves seven brackets
and eight inserts; each insert leaves eight brackets and seven inserts.
Their different area requirements are applied to every query.

The producer restricts each certified possible-node set to the current mask,
carrying a signature only when that intersection is exactly unchanged.
It tightens 104 insert-family signatures in case09 and applies 2,121 weighted
updates. The independent auditor uses allowed-node union projection and
recomputes all **19,950 area bounds from all 151,597 original physical records**,
instead of using the producer's incremental losses. Every query, mapped target
and simultaneous root-clique implication matches.

| Omitted sites | Complete queries | Remaining cells | New exclusions |
|---|---:|---:|---:|
| [0,5,10] | 2,816 | 3,793 | 0 |
| [5,10,11] | 3,834 | 4,758 | 0 |

[The complete audit](h5-combined-fixed-point-20261109/complete-audit.json) confirms both masks are unchanged.
The loop stops after its first audited round; none of the other seven permitted
rounds opens. The fixed point applies to these conditional and clique rules,
not to all possible proofs. The previous exact global envelope bounds remain
applicable because both masks are identical. The 453/455 prior whole-choice
exclusions stand, including 428 at zero clearance.

## Limits and next work

[All five new numerical processes](h5-combined-fixed-point-20261109/process-summary.json) pass and close
with zero descendants. The [591 inherited processes](h5-combined-fixed-point-20261109/inherited-process-summary.json)
are terminal, including four preserved failures. New workers retain CCD1
logical processors 16–31, one BLAS/OMP/MKL thread and a 2 GiB Windows Job cap.
The controls use 20 s, the two preflight stages 30 s each, and the producer
and complete auditor 60 s each. Consumed preparation is **1309.785273 s**;
the independent audits are external verification. No optimizer, timer reset
or timed H5 pass follows.

[Next](h5-combined-fixed-point-20261109/next-step.json), assess conservative two-reference capacities.
Two selected cells restrict the remaining geometry simultaneously; a failed
pair bound could add a certified incompatibility. Its controls and finite
query scope must be independently checked before use. No such stage is prepared.

Common-line occupied outer envelopes reserve holes; all 90 cutting holes
remain preserved. No ordinary part-in-hole or whole-allocation exclusion is
claimed. All 440 whole-job allocations, full66 source/native/material checks,
production integration and the H5 matrix remain open. Valid64 stays best.
The eight older first32 and 680 five-column cores remain closed.

Product, README and releases are unchanged. Earlier checkpoints `3642e620`
and `335be569` are committed. Main remains `2ae15d96`; [CI at review](h5-combined-fixed-point-20261109/main-ci-at-review.json)
has 6 passed / 0 live jobs. These checkpoints await the ordinary push gate.
[Archive checks](h5-combined-fixed-point-20261109/archive-checks.json), [manifest](h5-combined-fixed-point-20261109/raw-manifest.json),
[source bindings](h5-combined-fixed-point-20261109/source-bindings.json), [historical references](h5-combined-fixed-point-20261109/external-evidence.json)
and [runtime pins](h5-combined-fixed-point-20261109/runtime-bindings.json) preserve the complete chain.
