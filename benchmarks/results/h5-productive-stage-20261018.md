# Productive-exchange choices and repair allocations — 2026-10-18

**All four diagnostic layouts validate.** The observer records which
original part types are available and move between sheets, requested repair
time, elapsed duration, rejection stages and immediate
material/last-sheet extent. These are new observations, not a reconstruction
of the failed 72-outcome pilot or a quality comparison.

[The committed plan](h5-productive-stage-20261018/plan.json) uses the two
mechanical development jobs, kerfs 0.2 and 1.5 mm, seed zero, 60 seconds
and serial physical CCD0 CPU 8. All original algorithm settings remain.
Instrumentation can perturb wall timing. Production stays unchanged.

| Job | Kerf mm | Attempts | Accepted pairs | Same-inventory accepted | Outcomes |
| --- | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | 1 | 0 | 0 | accepted: 1 |
| m-mechanical-large-plates | 1.5 | 9 | 0 | 0 | material_guard_failed: 1, source_repair_failed: 8 |
| m-mechanical-panel-hardware | 0.2 | 9 | 0 | 0 | neutral_inventory_rejected: 4, source_repair_failed: 5 |
| m-mechanical-panel-hardware | 1.5 | 9 | 0 | 0 | neutral_inventory_rejected: 3, expired_after_repairs: 1, source_repair_failed: 5 |

Of 1 accepted exchanges, 0 return the same original
part types and quantities as they take. This preserves inventory, not
necessarily positions or orientations. Immediate validated material
decreases in 0 accepted exchanges; last-sheet occupied
extent decreases in 0. These observations do not establish
a later benefit or harm from rearrangement.

There are 42 retained proposals across the observed calls;
12 preserve inventory. Retained proposals are not necessarily
attempted, and these counts are not all sampled configurations.

The session took 4.055 minutes. All archive CRCs/member hashes,
trace references, solver counters, original quantities, public exports and
independently recomputed metrics pass. Source, input and binary guards match.
[Every attempt](h5-productive-stage-20261018/observed-exchanges.json) and
[verification](h5-productive-stage-20261018/verification.json) are retained.

No original failed result, gate, production implementation or held-out file
is changed. **H2/H5 remain open; completed weight stays 60%.**

## Source choices and repair time

| Job | Kerf mm | Source inventory by original item ID | Pair choices by item ID | Neutral rejections | Source failures / repairs | Requested source time range, s | Total source time, s |
| --- | ---: | --- | --- | ---: | ---: | --- | ---: |
| m-mechanical-large-plates | 0.2 | [{1: 1, 0: 12, 3: 6}] | [[[0, 0], [3, 3], [0, 0], [3, 3], [0, 0], [3, 3]]] | 0 | 0 / 1 | [0.3989439000000008, 0.3989439000000008] | 0.006577 |
| m-mechanical-large-plates | 1.5 | [{1: 1, 0: 12, 3: 6}] | [[[0, 0], [3, 3], [0, 0], [3, 3], [0, 0], [3, 3]]] | 0 | 8 / 9 | [0.0017689000000009614, 0.39891830000000095] | 0.994084 |
| m-mechanical-panel-hardware | 0.2 | [{2: 2, 1: 42, 0: 17, 3: 41}] | [[[2, 2], [1, 1], [0, 0], [3, 3], [1, 1], [0, 0]]] | 4 | 5 / 9 | [-0.0029295500000001695, 0.2799763000000004] | 0.544403 |
| m-mechanical-panel-hardware | 1.5 | [{2: 2, 1: 42, 0: 17, 3: 41}] | [[[2, 2], [1, 1], [0, 0], [3, 3], [1, 1], [0, 0]]] | 3 | 5 / 9 | [-0.0036167000000002503, 0.3026080999999996] | 0.589676 |

Item IDs denote original model items; repeated IDs represent interchangeable
copies. Retained choices are not necessarily attempted. Requested remaining
time is logged immediately before each separator call and can be negative.
Elapsed time can slightly overrun a checked deadline. These observations
do not prove the minimum time needed or feasibility of failed assignments.


## Independent audit and next hypothesis

The filled-outer audit independently checks all 18,669
same-sheet pairs across four layouts. Minimum clearance slack is
9.99999701851e-07 mm at the unchanged 1e-7 mm tolerance.
Original hole interiors remain reserved. All archives, trace references, five
solver counters, quantities, metrics and source/binary/input guards verify.

All twenty single-part attempts return more recorded item area to the source
sheet than they remove. All eight paired attempts preserve the same original
inventory; seven are rejected as neutral and one expires after repair. In both
large-plate cases, the largest remaining item (ID 1) has only one copy, so the
same-original-item pair selector excludes it. Its six choices instead use
IDs 0 and 3. Panel cases consider four original item families, but their
attempted pairs still preserve inventory. This is a proposal/assignment gap
as well as an incomplete-repair observation.

The next isolated change should test bounded pairs of different original
items, with authored witnesses using different dimensions and allowed-pose
checks. Keep the existing whole-job time budget, complete obstruction sets,
pair returned-area bound, geometry/material guards and normal-mode behavior.
This is a new hypothesis, not a claim that mixed pairs will meet H5. The
earlier repair-feasibility timings are not minimum required times; simply
enlarging repair windows is not justified as the sole remedy by these traces.

The [source review](h5-productive-stage-20261018/source-review.json) retains the
exact selector, deadline fragments and hashes. No production change or
repeated quality run; H2/H5 remain open at 60%.
