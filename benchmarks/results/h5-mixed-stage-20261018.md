# Mixed-pair sampling and repair observations — 2026-10-18

**All four diagnostic layouts validate.** The observer records which
original part types are available and move between sheets, requested repair
time, elapsed duration, rejection stages and immediate
material/last-sheet extent. These are new observations, not a reconstruction
of the failed 72-outcome pilot or a quality comparison.

[The committed plan](h5-mixed-stage-20261018/plan.json) uses the two
mechanical development jobs, kerfs 0.2 and 1.5 mm, seed zero, 60 seconds
and serial physical CCD0 CPU 8. All original algorithm settings remain.
Instrumentation can perturb wall timing. Production stays unchanged.

| Job | Kerf mm | Attempts | Accepted pairs | Same-inventory accepted | Outcomes |
| --- | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | 7 | 0 | 0 | source_repair_failed: 7 |
| m-mechanical-large-plates | 1.5 | 3 | 0 | 0 | material_guard_failed: 1, source_repair_failed: 1, accepted: 1 |
| m-mechanical-panel-hardware | 0.2 | 9 | 0 | 0 | neutral_inventory_rejected: 4, source_repair_failed: 5 |
| m-mechanical-panel-hardware | 1.5 | 9 | 0 | 0 | neutral_inventory_rejected: 3, source_repair_failed: 6 |

Of 1 accepted exchanges, 0 return the same original
part types and quantities as they take. This preserves inventory, not
necessarily positions or orientations. Immediate validated material
decreases in 1 accepted exchanges; last-sheet occupied
extent decreases in 1. These observations do not establish
a later benefit or harm from rearrangement.

There are 42 retained proposals across the observed calls;
12 preserve inventory. Retained proposals are not necessarily
attempted, and these counts are not all sampled configurations.

The session took 4.055 minutes. All archive CRCs/member hashes,
trace references, solver counters, original quantities, public exports and
independently recomputed metrics pass. Source, input and binary guards match.
[Every attempt](h5-mixed-stage-20261018/observed-exchanges.json) and
[verification](h5-mixed-stage-20261018/verification.json) are retained.

No original failed result, gate, production implementation or held-out file
is changed. **H2/H5 remain open; completed weight stays 60%.**

## Source choices and repair time

| Job | Kerf mm | Source inventory by original item ID | Pair choices by item ID | Neutral rejections | Source failures / repairs | Requested source time range, s | Total source time, s |
| --- | ---: | --- | --- | ---: | ---: | --- | ---: |
| m-mechanical-large-plates | 0.2 | [{1: 1, 0: 12, 3: 6}] | [[[0, 0], [1, 0], [3, 3], [1, 0], [0, 0], [1, 0], [3, 3], [0, 3], [0, 0], [0, 3], [3, 3], [0, 3]]] | 0 | 7 / 7 | [-0.002513675000000326, 0.3989469000000003] | 1.028506 |
| m-mechanical-large-plates | 1.5 | [{1: 1, 0: 12, 3: 6}] | [[[0, 0], [1, 0], [3, 3], [1, 0], [0, 0], [1, 0], [3, 3], [0, 3], [0, 0], [0, 3], [3, 3], [0, 3]]] | 0 | 1 / 3 | [0.15857075000000087, 0.39891780000000043] | 0.801496 |
| m-mechanical-panel-hardware | 0.2 | [{2: 2, 1: 42, 0: 17, 3: 41}] | [[[2, 2], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1], [3, 3], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1]]] | 4 | 5 / 9 | [-0.0029769999999995633, 0.26500135000000036] | 0.513276 |
| m-mechanical-panel-hardware | 1.5 | [{2: 2, 1: 42, 0: 17, 3: 41}] | [[[2, 2], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1], [3, 3], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1]]] | 3 | 6 / 9 | [-0.0034684499999997342, 0.30151909999999926] | 0.581999 |

Item IDs denote original model items; repeated IDs represent interchangeable
copies. Retained choices are not necessarily attempted. Requested remaining
time is logged immediately before each separator call and can be negative.
Elapsed time can slightly overrun a checked deadline. These observations
do not prove the minimum time needed or feasibility of failed assignments.

## Paired sample rejection partition

| Job | Kerf | Pair kind | Calls | Visited / total | Invalid pose | Boundary | Empty | Over 3 | Returned area | Eligible | Retained | Truncated calls |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | same | 6 | 1050 / 1050 | 0 | 116 | 0 | 358 | 576 | 0 | 0 | 0 |
| m-mechanical-large-plates | 0.2 | mixed | 6 | 1332 / 1332 | 286 | 235 | 0 | 523 | 288 | 0 | 0 | 0 |
| m-mechanical-large-plates | 1.5 | same | 6 | 1050 / 1050 | 0 | 116 | 0 | 364 | 570 | 0 | 0 | 0 |
| m-mechanical-large-plates | 1.5 | mixed | 6 | 1332 / 1332 | 286 | 234 | 0 | 525 | 287 | 0 | 0 | 0 |
| m-mechanical-panel-hardware | 0.2 | same | 1 | 204 / 204 | 0 | 21 | 0 | 141 | 9 | 33 | 6 | 0 |
| m-mechanical-panel-hardware | 0.2 | mixed | 0 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| m-mechanical-panel-hardware | 1.5 | same | 1 | 204 / 204 | 0 | 21 | 0 | 142 | 8 | 33 | 6 | 0 |
| m-mechanical-panel-hardware | 1.5 | mixed | 0 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Reasons partition visited samples in the displayed order. Boundary collisions
take precedence when an oversized set also occurs. An empty set needs no exchange
and is skipped by this proposal routine. Retained proposals may never be attempted
when the phase expires. Counts do not establish causality or global infeasibility.


## Independent audit and next hypothesis

All 18,626 same-sheet pairs in the four saved layouts
pass the independent filled-outer audit. Minimum clearance slack is
9.99999701878e-07 mm under the unchanged 1e-7 mm tolerance.
The one accepted single swap decreases immediate material by 18.669 mm2;
this small local change does not replace the failed pilot comparison.

Both large-plate traces reach all twelve planned pairs and every generated
sample. The paired returned-area filter alone discards 1,721 otherwise eligible
samples, including 575 mixed samples, after pose/boundary/obstruction-count checks.
This identifies a search filter, not the feasibility of those rejected layouts.
The independently checked larger-return witness demonstrates that this area
inequality is not necessary for a valid material-nonincreasing pair exchange.
The next isolated candidate should first reproduce a failing runtime regression
for that witness, then test removing this proposal-area filter while retaining
complete obstruction sets, pose rules, both repairs, strict whole-job geometry
and material guards, all existing budgets and normal-mode behavior.

Panel traces expose a separate scheduling limitation: only the first same-item
pair is generated, retaining six proposals per kerf; seven attempted paired
swaps are rejected as unchanged-inventory without material gain. No mixed pair
is generated there. The recorded repairs already have zero loss and each takes
less than 0.0001 seconds. The trace does not allocate the remaining time among
construction, conversion and independent validation, so it does not establish
which of those dominates. Do not infer that longer repair windows alone solve
either workload, or that lifting the area filter will meet the quality gate.

[The source review](h5-mixed-stage-20261018/source-review.json) preserves the
exact filter, schedule, neutral guard and source hash. The
[larger-return witness](h5-larger-return-witness-20261018.md) remains authored
geometry evidence only. Production, limits, reserved inputs and 60% completion
are unchanged.
