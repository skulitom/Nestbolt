# Complete bracket-reference subdivisions — 2026-11-09

**All five reference queries and all twenty closed child regions pass independent
verification, but none is excluded.** Four parent bounds tighten; the exact
fixed29 frontier stays at omitted cog sites **`[0,5,10]` and `[5,10,11]`**, with
8,903 current nodes. The existing 453/455 exclusions, including 428 at zero
clearance, are unchanged. H2/H5 remain open at **60% completed milestone weight**.

## Complete scope and geometric meaning

[The frozen selection](h5-reference-subdivision-20261109/subdivision-plan.json) contains every surviving
query from the preceding five-query whole-reference pilot. Each original
closed anchor box is split at both integer midpoints. Every certified reference
cover piece is intersected with every child, including points and lines.
The independent auditor verifies each intersection and their complete union;
no unproved region is omitted. All twenty children are nonempty.

For each child, occupied rectangles common to every reference position receive
141 µm square buffers, strictly inside the original 0.2 mm clearance. Their
open forbidden companion-anchor regions are subtracted from complete closed
source covers. The current global mask and actual conflict row determine the
allowed companions. Every alias component is swept over the surviving covers.
The seven other brackets and eight inserts require **438,385 mm²**.

These are **common-line occupied outer envelopes with holes reserved**. The
[source-policy audit](h5-fixed29-pointwise-capacity-20261108/occupancy-scope/checks.json)
retains all 90 cutting holes. No net-material or ordinary part-in-hole exclusion
is claimed. Full-reference occupancy is an alternative bound calculated before
common-moving subtraction; the two deductions are never added. Pose-specific
bounds never transfer through conflict-row dominance.

## Independent result

[Complete reconciliation](h5-reference-subdivision-20261109/reconciliation-checks.json) verifies
**100 exact area bounds**, **865 reference boundary/interior classes**,
**640 common-rectangle corner checks**, **51,628 companion covers** and
**1,119,932 companion boundary/interior classes**. A parent bound is the maximum
over every child, rather than the best selected child.

| Case / current reference | Prior parent upper (mm²) | New complete parent upper (mm²) | Smallest child upper (mm²) |
|---|---:|---:|---:|
| 01 / 1227 | 451,297.078074 | 451,297.070856 | 451,115.585452 |
| 01 / 366 | 446,037.555964 | 445,033.181104 | 443,639.805682 |
| 09 / 1854 | 438,946.664440 | 438,946.657222 | 438,765.171818 |
| 09 / 160 | 444,377.686708 | 444,371.211649 | 439,937.990014 |
| 09 / 413 | 442,443.704850 | 442,443.704850 | 442,425.964391 |

[Exact integer results](h5-reference-subdivision-20261109/query-summary.json) preserve source labels
separately from current graph positions. The closest complete parent bound,
case 09 / reference 1854, still exceeds the required area by **561.657222 mm²**.
Even its best child remains **380.171818 mm²** above the requirement. These
surpluses prove neither a feasible arrangement nor an impossibility result.
The full source cover remains unchanged.

## Preserved audit failure and checked replacement

The producer completes once in 37.161113 s under its 45 s cap. The first
independent horizontal interval-merge audit reaches its hard 60 s limit after
two child readbacks. Its process, partial output and original script remain
preserved; no final proof uses that partial result. The producer is not repeated.
[The correction record](h5-reference-subdivision-20261109/failed-audit-correction.json) records the change.

The replacement auditor uses a horizontal event sweep with an interval tree,
independent of the producer's vertical prefix arrays. Before use,
[exhaustive controls](h5-reference-subdivision-20261109/area-controls-checks.json) compare all 4,096 subsets
of twelve labelled overlapping, nested and touching rectangles with an exact
unit-cell oracle, then repeat all 4,096 after integer scaling and translation.
Duplicate multiplicities and empty categories pass. Nine previously certified
full-source area bounds also match. All five replacement audits pass separately
within their unchanged 60 s caps; all twenty children are replayed in full.

| Bounded process | Complete time (s) | Cap (s) | Result |
|---|---:|---:|---|
| fixed29-reference-subdivision-process | 37.161113 | 45 | Pass |
| fixed29-reference-subdivision-audit-00-process | 60.006921 | 60 | Preserved hard limit |
| horizontal-segment-area-controls-process | 2.503975 | 30 | Pass |
| fixed29-reference-subdivision-audit-v2-00-process | 10.001610 | 60 | Pass |
| fixed29-reference-subdivision-audit-v2-01-process | 6.104015 | 60 | Pass |
| fixed29-reference-subdivision-audit-v2-02-process | 11.541841 | 60 | Pass |
| fixed29-reference-subdivision-audit-v2-03-process | 7.161516 | 60 | Pass |
| fixed29-reference-subdivision-audit-v2-04-process | 6.458253 | 60 | Pass |
| fixed29-reference-subdivision-reconciliation-process | 0.896391 | 10 | Pass |

[All nine processes close](h5-reference-subdivision-20261109/process-summary.json) with no live descendants,
CCD1 logical processors 16–31, one BLAS/OMP/MKL thread and a 2 GiB Windows Job
memory cap. Consumed numeric preparation is **308.762676 s**, including the
complete failed audit and new helper controls. No optimizer, timer reset or
timed H5 pass is allowed from this lineage.

## Remaining work and repository state

[Next](h5-reference-subdivision-20261109/next-step.json), assess complete conditional coverage of the current
minimal reference rows, with bounded batches and explicit accounting. The
five-query pilot does not cover every row. Repeating this subdivision or an old
closed optimization would add no new method. No broader batch is prepared.

[The two exact fixed29 cases](h5-reference-subdivision-20261109/remaining-fixed29-cases.json), all 440
whole-job allocations, full 66-part source/native/material validation, production
integration and the full H5 matrix remain open. The valid 64-part layout stays
best. The separate eight older first32 and 680 five-column cores remain closed.
Product, README and release state are unchanged.

[The preceding checkpoint reached main 0efe5688](h5-reference-subdivision-20261109/prior-main-push-receipt.json)
after all six prior checks passed. [Its current CI](h5-reference-subdivision-20261109/main-ci-at-review.json)
has 4 passed / 2 live jobs at review. This evidence checkpoint may
be committed locally while that run finishes; a normal push must preserve it.
[Archive checks](h5-reference-subdivision-20261109/archive-checks.json), [manifest](h5-reference-subdivision-20261109/raw-manifest.json),
[source bindings](h5-reference-subdivision-20261109/source-bindings.json),
[historical references](h5-reference-subdivision-20261109/external-evidence.json) and
[runtime pins](h5-reference-subdivision-20261109/runtime-bindings.json) preserve the consumed evidence.
