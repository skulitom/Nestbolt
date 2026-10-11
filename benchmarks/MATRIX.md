# Frozen benchmark coverage

`matrix-plan.json` freezes the job, budget, seed and settings-role coverage before
Nestbolt search tuning. It does not claim that a runner or acceptance gate passes.
Run `python scripts/matrix_plan.py --check` to verify it against the original
dataset freezes; the check refuses changed inputs or a rewritten schedule.

Every one of the 13 S, 35 B and 40 M jobs receives a 60-second comparison. A fixed
12-job B/M subset also receives 300 seconds. Selection follows the reasons in the
manifest: academic free/discrete rotations and detailed contours, flat-pack panels,
garment grain, defects, mixed stock, a held-out 2,000-part job and held-out public
gear geometry. Initial competitor pilots preceded this selection; Nestbolt has no
search implementation yet. No held-out optimiser results informed it.

Development uses seeds 0, 1 and 2 and excludes all ten held-out maker jobs, including
the two reserved long-budget jobs. Final acceptance uses fresh seeds 1000–1004 and
includes every held-out job. Both the identical-constraint and best-native-setting
roles are represented. Exact settings are still provisional: their configuration
hashes and any job-specific rules must be sealed before final acceptance.

There are 528 development and 1,000 final job/budget/seed/settings slots for a tool
covering every set. The per-tool matrix will apply the plan's applicability rules:
Sparrow/Nestbolt for S; Deepnest, SVGnest, applicable single-sheet Sparrow, LBF and
Nestbolt for B/M. Unsupported cases and every failure must remain visible, never
silently vanish from a table. Invalid output has no material score. A missing
comparison is not a verified percentage reduction.

Sessions stay below four hours and eight simultaneous runs, each using one worker.
Desktop runner batches also respect Anode's shorter job lifetime. Nestbolt's
all-core measurement is separate. Final aggregation must retain medians/IQR and
per-tool numbers before applying the best-valid-competitor-per-job gates.

This is a coverage freeze, not the G8 one-command executor. That executor still
needs to rebuild data, seal tool settings, schedule/resume every required attempt,
and produce the complete results page and charts.

`python scripts/comparator_coverage.py` performs a separate static development
input check, without running any optimiser or touching the held-out jobs. The
[first coverage report](results/comparator-coverage-20261011T212118Z-ed8cf053.md)
prepares all 35 B inputs for each comparator. For the 30 development M jobs it
prepares 30 for Deepnest, 27 for SVGnest and six each for LBF and Sparrow. Every
unsupported reason is retained. Successful preparation does not prove native
parsing, feasibility or a valid timed result; those require the actual runners.

[Development sessions](SESSIONS.md) now provide an immutable, resumable work queue
with explicit settings, source/binary checks and per-attempt audits. Four lifecycle
tests and a real three-attempt native resumption trial pass. The full matrix,
final configuration freeze, aggregation and G8 publication remain pending.
