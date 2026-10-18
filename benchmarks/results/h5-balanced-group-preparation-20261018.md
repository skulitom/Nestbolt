# Balanced incoming-pair preparation — 2026-10-18

The isolated candidate passes 97 optimized core tests, including all 90 prior
tests, strict lint, ten authored observer outcomes, four public CLI comparisons
and five adversarial paired-harness checks. Normal output is exact apart from
elapsed wall time; common fixed-work replays agree. Production is unchanged.

The candidate tries two nearby copies of the same original part together.
It considers at most twelve anchors, two nearest neighbours per anchor and six
distinct pairs in stable order. Incoming members preserve relative transforms;
every mapped orientation must be permitted. Each proposal returns the complete
union of actual obstructions, at most three parts, whose original combined area
is no greater than that of the incoming pair. It never takes a partial union.

Pair attempts share at most half the existing exchange window. Single-incoming
choices follow in the remaining window. Existing pair-repair caps, whole-job
geometry/material checks, incumbent preservation and the outer shared ten-percent
budget/1.2-second cap stay. Pair attempts and acceptances have omitted-zero
counters. The failed source-reuse experiment is not included.

Seven new tests cover the previously independently validated two-to-three witness,
disabled/expired operation, frozen-sheet preservation, group orientation and
relative transforms, bounded unique identity-safe pair selection, valid single
fallback and failure with an unchanged incumbent. All old strict-material/defect/reflection tests
remain. The fixture files are exact copies of the saved authored witness.

The initial run passed 94 tests and failed two new test assumptions. The tests
had used public angles in the rotated internal frame and expected a valid
single exchange to fail. Original sources/logs remain. The latter layout passes
the public CLI validator at unchanged material. Corrected orientation checks
use the internal frame; the old rejection case remains as a positive fallback
test, alongside a new constrained source-return case. Runtime code is unchanged
by these repairs. A second retained run passed 96 tests and exposed a further
test assumption: the nearest-pose sampler may choose an unmirrored pose. The
final test supplies an explicit permitted public mirrored transform through
the existing Model conversion. The internal f32 consistency check does not change
the independent geometry or material thresholds.

The subsequent 72-outcome pilot retains four jobs, two kerfs, three seeds,
three rotating sequential arms, 60-second searches and eight physical CCD0
cores. Its block, scoring, case and measurement functions remain AST-identical
to the previous pilot. A functioning authored case does not demonstrate real
job improvement. The +1% material limit and full 13-job H5 requirement remain.
No held-out access or integration; H2/H5 remain open at 60%.
