# Joint-repair observation qualification — 2026-10-18

The [72-run joint-repair pilot](h5-joint-repair-pilot-20261018.md) fails five
material comparisons. This separate observer records individual repairs to
explain that failure. It changes no search decisions, RNG calls, work charges,
deadline, validation reserve, step cap or geometry policy. Production is unchanged.

Nested records link each provisional chain, policy call, proposed swap and pair
repair. They retain original part types and physical poses, proposed/repaired
membership, collision loss, terminal outcomes, actual whole-job trials and
metrics, accepted steps, commits and rollbacks. Direct elapsed timers surround
separation and source lowering. Serialization and logging can change wall-time
trajectories; this is diagnostic evidence, not a performance comparison. Net
part-type migration can miss same-family copy swaps that cancel in the multiset.

All **165 unchanged native tests** pass, and **86 earlier witness outputs** are
exact. All **157 source files** reconstruct after reversing the recorded inserts;
155 unrelated files are unchanged. The second changed file only corrects the
observer example's description. Strict lint and the release observer build pass.

The saved native log contains **48 linked trace records**. The reader checks
parent/child identity, stage coverage, terminal state, finite timings, exact
proposal membership and source poses, part conservation, unchanged nonselected
sheets, acceptance metrics, provisional steps and rollback counters. Nine
deliberately damaged records are rejected. Completed and failed repairs, expiry,
accepted steps and an actual provisional rollback are represented.

Independent public CLI validation passes for **23 unique saved layouts**; the
filled-outer check covers **53 pairs** at the unchanged 1e-7 mm tolerance.
Whole-job baselines/trials use the original job. Component checks use selected
pair quantities and original full stock geometry; they do not replace internal
crop validation or original whole-job stock-count checks. The prior thin-crop
tests and their exact witnesses remain preserved.

Four public fixed-work outcomes (ordinary/common mode, seeds zero and one) match
the unobserved candidate exactly except elapsed wall time, with four independent
CLI checks. Common-mode trace counts equal the actual search statistics. The
first checker used an incorrect parent folder name after saving one outcome;
its source and failure remain. Only the reference path was corrected, and that
completed outcome was reused without another search.

The separate proposed diagnostic uses large plates and panel hardware at both
kerfs, seed zero and the original 60-second search allowance, serially on CCD0
physical CPU 8. The existing per-case validation/export/archive method is reused.
Its plan must be committed before any development measurement. No pilot retry,
integration, new release, held-out access or H5 credit follows qualification.
The completed milestone weight remains 60%.

[Checks](h5-joint-observer-preparation-20261018/checks.json),
[trace reader](h5-joint-observer-preparation-20261018/reader-checks.json),
[independent geometry](h5-joint-observer-preparation-20261018/geometry-checks.json),
[exact source reconstruction](h5-joint-observer-preparation-20261018/reconstruction.json),
[archive integrity](h5-joint-observer-preparation-20261018/integrity.json).
