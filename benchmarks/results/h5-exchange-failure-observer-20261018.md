# Exchange failure reasons — 2026-10-18

**Observed failure causes: 4 material increased, 18 source loss positive.**

Two serial panel-hardware diagnostics retain both kerfs, seed zero,
60 seconds and physical CCD0 CPU 8. The observer only adds data after
the original rejection decisions; every condition, clock read, work
charge and original test remains. Logging can change wall trajectories,
so this is not a quality or speed comparison.

Both final layouts and 2 baselines independently validate.
All 4 captured material/deadline trials also validate,
reproduce their original metrics exactly, reserve all filled outer contours,
and reproduce material by a separate rectangular-stock height calculation.
The original/final audit checks 31,811 filled-outer pairs;
captured trial checks add 32,004 pairs.
Quantities, exact selected physical poses, original archives, all member
hashes and source/binary guards pass. The 72-run quality pilot remains
failed and is not replaced by these observations.

| Kerf mm | Choice | Failure reason | Before material mm² | Trial material mm² | Change mm² |
| --- | ---: | --- | ---: | ---: | ---: |
| 0.2 | 0 | material_increased | 5114567.645000 | 5114567.648750 | +0.003750 |
| 0.2 | 0 | material_increased | 5114567.645000 | 5114567.648750 | +0.003750 |
| 1.5 | 0 | material_increased | 5114567.911250 | 5114567.913750 | +0.002500 |
| 1.5 | 0 | material_increased | 5114567.911250 | 5114567.913750 | +0.002500 |

The 18 saved failed sources are diagnostic intermediate states.
Their original-part inventory is checked independently. Original filled
polygons are inspected before and after repair for overlaps, clearance
and nominal stock bounds. This does not reconstruct the cropped separator
boundary or its weighted proxy loss. Positive recorded loss proves that
the source repair condition failed; it neither proves global infeasibility
nor excludes a concurrent deadline expiry. Zero recorded loss would identify
the deadline side of that original short-circuit condition.

All eighteen recorded source failures retain positive separator loss and independently observed original filled-outer pair violations (two to nine per failed source). None is explained only by deadline expiry. The four valid material trials increase material by 0.0025000004 to 0.0037500001 mm2 and keep inserts at the height-defining edge; they do not establish useful compaction. The strict material guard stays unchanged. The next isolated hypothesis concerns return initialization: current return poses are mapped around the removed incoming anchor and can initially extend above the old occupied height. Qualify a bounded whole-group translation into the existing source-container bounding box when the group fits, retaining already contained or oversized groups exactly. Preserve member orientations, reflection and relative geometry; charge the extra transformed-geometry work, keep all current budgets/repair/acceptance checks, and prove the bounded/no-op behavior on authored cases before any new quality pilot. This is a hypothesis, not a packing-feasibility or expected-improvement claim. No unchanged quality rerun or integration follows from this diagnostic.

[Committed scope](h5-exchange-failure-observer-20261018/plan.json),
[archive verification](h5-exchange-failure-observer-20261018/verification.json),
[baseline and final audit](h5-exchange-failure-observer-20261018/layout-checks.json),
[independent failed-trial and source audit](h5-exchange-failure-observer-20261018/failure-detail-checks.json).

**H2/H5 remain open; completed milestone weight is 60%.** No production
integration, reserved-input access, changed threshold or release.

All six hosted checks on main `b9ccbd5` pass, including the completed Windows check, Linux and browsers. The subsequent isolated candidate remains subject to its own quality pilot and the unchanged H5 gate. [Six completed checks](h5-exchange-failure-observer-20261018/main-ci-b9ccbd5.json).
