# Free-space return initialization — preparation, 2026-10-18

The [contained-return pilot](h5-contained-return-pilot-20261018.md) fails five
material pairs. Box containment alone does not look for a lower collision-free
position. This candidate adds a bounded translation search for each returned
part against the source layout, including returns already placed in this attempt.

At most 256 translations use a 12×12 grid and four bounding-box edge anchors for
each of the first 28 source members in existing order. Exact collision checks
reserve filled holes. Each original orientation and reflection stays unchanged.
Clear seeds are ordered by occupied height and then horizontal position; the old
contained seed remains if no clear placement exists. The original seed and every
transformed candidate are charged. Shared deadline checks bound the search, and
every return is still registered even when that deadline has elapsed. The original
repair allocation, proposal choices and strict whole-job material/geometry
acceptance remain. A finite grid is a heuristic, not a feasibility proof.

All 137 optimized tests pass: 130 prior tests are unchanged, three prior fixture
expectations are revised, and four regressions are new. Those four first fail
against the previous behavior; their original source, binary and log remain.
The first implementation passes 134 tests but improves three formerly neutral
fixtures, breaking their no-move expectation. Six frozen-CLI validations prove
the preserved failed outputs valid, reducing authored material from 19,700 to
19,600.0558 mm². Only those three expectations change: an accepted move now must
strictly reduce material against the internal incumbent, while a rejected,
disabled or expired operation must preserve it exactly. Standalone exact-state
and material-profile predicate tests and all runtime acceptance code remain
unchanged. Exact-state rejection is no longer required to occur in this fixture;
its unchanged predicate tests and reconstructed runtime support that guard.
The first revised oracle used a direct model conversion and failed two exact
no-op checks because it omitted the existing strip split/rejoin. Its binary,
source and log remain. The corrected oracle uses the actual disabled operation;
no numerical tolerance or runtime change is introduced.
New checks cover sequential clear returns,
exact inventory, replay/work counts, permitted mixed rotations and mirrors,
expired and mid-search deadlines, and unplaceable returns with reserved holes.
Two saved authored output layouts and their inputs pass four frozen-CLI checks
and independent original filled-outer clearance checks; no test was rerun to
obtain those saved witnesses. Twelve active/disabled/expired outcomes pass 24 frozen
CLI validations: four active cases strictly improve, and all eight disabled or
expired cases preserve their exact internal incumbents. One profile-witness JSON
line was interleaved in the parallel full-test log. That original log and failed
reader remain; only the authored profile test was repeated using the same binary
with separate output streams. No quality run was repeated.
Ten public outcomes and four CLI comparisons preserve normal
results exactly except wall time and reproduce common-mode results deterministically.

Strict lint and the experimental executable build pass. All 156 formatted source
files reconstruct exactly; 155 files and all other runtime blocks are unchanged.
Five adversarial pilot-harness tests pass. Measurement, scoring, ordering and the
previously qualified process-identity guard are AST-identical to the prior pilot.

The next pilot must commit its plan before measuring the same four development
jobs, both kerfs and three seeds at matched 60-second budgets on eight physical
CCD0 cores. No quality measurement has begun. Success would still require the
full original 13-job H5 gate. Production, reserved inputs, release and README
claims are unchanged. **H2/H5 remain open; completed milestone weight is 60%.**

[Checks](h5-free-return-preparation-20261018/checks.json),
[original failures](h5-free-return-preparation-20261018/expected-failure.json),
[reviewed fixture expectations](h5-free-return-preparation-20261018/revised-expectations.json),
[independent authored outputs](h5-free-return-preparation-20261018/seed-checks.json),
[exact source reconstruction](h5-free-return-preparation-20261018/reconstruction.json),
[raw evidence](h5-free-return-preparation-20261018/raw.zip),
[member hashes and archive integrity](h5-free-return-preparation-20261018/integrity.json).
