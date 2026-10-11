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

- 2026-10-11T17:56:22.939760+00:00 | M0 `published-20261011/albano-0` | completed_integrity_checked | 1200s, 3 workers | length 9747.749 | [record](output/m0/published-20261011/albano-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:56:22.994007+00:00 | M0 `published-20261011/blaz1-0` | completed_integrity_checked | 1200s, 3 workers | length 25.646978 | [record](output/m0/published-20261011/blaz1-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:56:23.006882+00:00 | M0 `published-20261011/dagli-0` | completed_integrity_checked | 1200s, 3 workers | length 56.614902 | [record](output/m0/published-20261011/dagli-0/run.json). Geometry validation pending M1.

- 2026-10-11T17:56:56.186850+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-c283d33b0a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T17:56:56.245490+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-f2006f6768.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T17:56:56.303972+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-7432cb7dbf.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:14:05.388499+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-e1e6911515.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:14:05.541646+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-babae60f88.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:14:05.814839+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-6ce95cc0ab.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:16:23.373487+00:00 | M0 `published-20261011/jakobs2-0` | completed_integrity_checked | 1200s, 3 workers | length 23.00045 | [record](output/m0/published-20261011/jakobs2-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:16:23.515272+00:00 | M0 `published-20261011/fu-0` | completed_integrity_checked | 1200s, 3 workers | length 30.846651 | [record](output/m0/published-20261011/fu-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:16:23.542167+00:00 | M0 `published-20261011/jakobs1-0` | completed_integrity_checked | 1200s, 3 workers | length 11.00028 | [record](output/m0/published-20261011/jakobs1-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:18:10.854544+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-7dc7e746de.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:18:11.051490+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-9a7ec50bcb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:18:11.115631+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-90e3945878.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:18:11.333601+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-157bd41b35.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:18:11.460417+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-903ab177ec.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:18:11.528513+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-7e57a80cb5.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:23.884883+00:00 | M0 `published-20261011/mao-0` | completed_integrity_checked | 1200s, 3 workers | length 1715.2783 | [record](output/m0/published-20261011/mao-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:36:24.008049+00:00 | M0 `published-20261011/marques-0` | completed_integrity_checked | 1200s, 3 workers | length 76.00197 | [record](output/m0/published-20261011/marques-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:36:24.025256+00:00 | M0 `published-20261011/shapes0-0` | completed_integrity_checked | 1200s, 3 workers | length 58.522026 | [record](output/m0/published-20261011/shapes0-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:36:42.348243+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-ac5458356f.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:42.419803+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-1074caed39.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:42.509766+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-a6e13e875e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:42.602982+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-5bbc28ce77.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:42.899817+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-5417e1b21f.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:43.222427+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-015c962576.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:43.331381+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-58fb725524.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:43.673372+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-52bcbb6a47.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T18:36:43.947389+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-f2d09d7c55.json). Original polygons; Clipper2 path; this does not establish full M1/G1.
