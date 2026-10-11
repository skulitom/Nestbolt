# Benchmark log

Append-only run summaries. Raw runs live in `output/runs/` (ignored by Git) and
must be archived with any published result. The runner records commit/dirty state,
source hash, tool commit, lockfile, binary and input checksums, seed and elapsed time.

No acceptance benchmark has passed. Generated smoke instances only check that the
pinned executable runs and writes readable output. They are not sets S, B or M,
and do not reproduce the published experiments or independently validate geometry.


- 2026-10-11T17:11:09.385567+00:00 | `20261011T171109Z-generated-rectangles-s0-ff927bfa` | Sparrow `4629b22795ae6b25b3b460ccde6fb36a71292b6d` | Nestbolt `uncommitted scaffold` (dirty=True) | seed 0, 5s, 1 worker | completed_unvalidated | [record](output/runs/20261011T171109Z-generated-rectangles-s0-ff927bfa/run.json). No independent validity/quality claim.

- 2026-10-11T17:11:14.712896+00:00 | `20261011T171114Z-generated-concave-s0-22529b39` | Sparrow `4629b22795ae6b25b3b460ccde6fb36a71292b6d` | Nestbolt `uncommitted scaffold` (dirty=True) | seed 0, 5s, 1 worker | completed_unvalidated | [record](output/runs/20261011T171114Z-generated-concave-s0-22529b39/run.json). No independent validity/quality claim.

- 2026-10-11T17:14:08.032218+00:00 | `20261011T171408Z-generated-rectangles-s0-0c891e67` | Sparrow `4629b22795ae6b25b3b460ccde6fb36a71292b6d` | Nestbolt `uncommitted scaffold` (dirty=True) | seed 0, 5s, 1 worker | completed_unvalidated | [record](output/runs/20261011T171408Z-generated-rectangles-s0-0c891e67/run.json). No independent validity/quality claim.

- 2026-10-11T17:14:13.308724+00:00 | `20261011T171413Z-generated-concave-s0-6193c2d8` | Sparrow `4629b22795ae6b25b3b460ccde6fb36a71292b6d` | Nestbolt `uncommitted scaffold` (dirty=True) | seed 0, 5s, 1 worker | completed_unvalidated | [record](output/runs/20261011T171413Z-generated-concave-s0-6193c2d8/run.json). No independent validity/quality claim.

- 2026-10-11T17:33:21.851539+00:00 | M0 experiment `adapter-smoke-20261011` opened | [metadata](output/m0/adapter-smoke-20261011/experiment.json) | 5s smoke only. No pass claimed.

- 2026-10-11T17:33:27.050745+00:00 | M0 `adapter-smoke-20261011/blaz1-0` | completed_integrity_checked | 5s, 3 workers | length 26.793299 | [record](output/m0/adapter-smoke-20261011/blaz1-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:33:27.235953+00:00 | M0 `adapter-smoke-20261011/albano-0` | completed_integrity_checked | 5s, 3 workers | length 9941.22 | [record](output/m0/adapter-smoke-20261011/albano-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:35:11.638777+00:00 | M0 experiment `adapter-smoke-verified-20261011` opened | [metadata](output/m0/adapter-smoke-verified-20261011/experiment.json) | 5s smoke only. No pass claimed.

- 2026-10-11T17:35:16.984944+00:00 | M0 `adapter-smoke-verified-20261011/blaz1-0` | completed_integrity_checked | 5s, 3 workers | length 26.900911 | [record](output/m0/adapter-smoke-verified-20261011/blaz1-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:35:17.184348+00:00 | M0 `adapter-smoke-verified-20261011/albano-0` | completed_integrity_checked | 5s, 3 workers | length 9941.264 | [record](output/m0/adapter-smoke-verified-20261011/albano-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:36:22.495157+00:00 | M0 experiment `published-20261011` opened | [metadata](output/m0/published-20261011/experiment.json) | frozen 39-run quality reproduction; 1200s, 3 workers each. No pass claimed.

- 2026-10-11T17:51:03.718465+00:00 | independent geometry check `adapter-smoke-verified-20261011/albano-0` | valid | [report](output/m0/adapter-smoke-verified-20261011/albano-0/validation-a83f3e7b54.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T17:51:04.112631+00:00 | independent geometry check `adapter-smoke-verified-20261011/blaz1-0` | valid | [report](output/m0/adapter-smoke-verified-20261011/blaz1-0/validation-d0a8289eae.json). Original polygons; Clipper2 path; this does not establish full M1/G1.
