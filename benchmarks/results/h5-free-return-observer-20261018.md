# Actual return seeds and exchange outcomes — 2026-10-18

**All four diagnostic outputs validate.** The added free-space seed stage
changes none of the 43 observed returned poses. This explains what happened
in these observations; it does not reconstruct the earlier pilot or measure
the seed stage's effect across all jobs and seeds.

The [committed plan](h5-free-return-observer-20261018/plan.json) fixes both
mechanical jobs, both kerfs, seed zero, 60 seconds and serial physical CCD0 CPU 8.
The failed candidate's search decisions, clock reads, work charges and guards
remain exact after removing the observation code. Logging may perturb wall
trajectories. The session takes 243.569 seconds.

| Job | Kerf mm | Attempts | Accepted | Positive source loss | Actual material increase |
| --- | ---: | ---: | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 1 | 1 | 0 | 0 |
| m-mechanical-large-plates | 1.5 | 1 | 1 | 0 | 0 |
| m-mechanical-panel-hardware | 0.2 | 12 | 0 | 9 | 3 |
| m-mechanical-panel-hardware | 1.5 | 10 | 0 | 8 | 2 |

The 24 attempts include twelve paired attempts; every attempt selects an actual
highest source copy, and twelve select all highest copies. All four final and
four baseline layouts pass original filled-outer checks over
37,119 same-sheet pairs. Original quantities, public exports,
metrics, CRCs and every archive member hash pass.

The seed stage incurs 159–486 charged evaluations per
attempt, so it was not wholly skipped. Every captured post-seed pose still
matches its contained fallback exactly. Counts are per attempt and do not
prove every individual member completed a full sampling loop. Original
rotations/reflection and unchanged source poses match their recorded baselines.

All seven material-bearing trial layouts independently validate and their
material values reconstruct exactly from original geometry. The two accepted
large-plate trials save 28.887 and 132.567 mm², respectively. Each reduces charged
height by less than 0.1 mm; a cog or another insert remains height-setting.
The five panel trials increase material by 0.0025–18.925 mm² and are correctly
rejected under the unchanged exact guard. None is classified merely as expiry.
All seventeen positive-loss source repairs retain independently observed
filled-outer violations. Their failed snapshots remain failures, not outputs
presented as valid. Snapshot inspection uses nominal stock bounds and original
filled contours; it does not reconstruct cropped proxy boundaries or loss weights.

The geometry audit initially retained the older two-case terminal assertion
after inspecting all four cases. Its failure and checker remain. Only the
expected count was corrected; all four captured CLI checks were reused without
repeating a search or validation, and geometry assertions stayed unchanged.

## Next constraint

The bounded free-space seed stage changed none of the 43 observed return poses despite charged evaluations. These four diagnostic trajectories therefore supply no successful new seed witness, and do not justify expanding its sample count blindly. The two large-plate exchanges are independently valid but save less than 0.1 mm of charged height each; a cog or another insert remains height-setting. Source review shows that the directed step is invoked once per feasible window and returns immediately after its first accepted exchange. The next distinct hypothesis is bounded continuation after a strictly material-improving exchange, using the same original absolute exchange deadline and original total search budget, with a small explicit cap and stopping on no acceptance or no strict material gain. Keep the original per-exchange independent geometry/material guards, exact quantities, filled-hole reservation, and disabled/expired behavior. Qualify authored multi-success and rollback/deadline cases before a newly committed matched pilot. This targets the observed early return after tiny gains; it does not resolve the seventeen panel source-repair failures by itself, prove that another exchange fits, or establish H5 feasibility. All original H5 limits and the complete 13-job requirement remain. Do not repeat the unchanged failed quality pilot or access reserved geometry.

Production, release, reserved inputs and completed gate weights are unchanged.
**H2/H5 remain open; completed milestone weight is 60%.**

[Archive verification](h5-free-return-observer-20261018/verification.json),
[baseline/final geometry](h5-free-return-observer-20261018/layout-checks.json),
[actual seed and repair geometry](h5-free-return-observer-20261018/seed-detail-checks.json),
[source review and next hypothesis](h5-free-return-observer-20261018/source-review.json),
[preserved audit correction](h5-free-return-observer-20261018/layout-terminal-count-repair.json),
[full observations](h5-free-return-observer-20261018/results.json).
