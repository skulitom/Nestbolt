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

- 2026-10-11T18:42:22.705382+00:00 | `20261011T184222Z-b-fu-nest-mb-given-identical-s0-1fdf5e06` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 5s limit, one pass/one worker, identical | valid; independent material 4.476310142857143 | [record](output/lbf/20261011T184222Z-b-fu-nest-mb-given-identical-s0-1fdf5e06/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:42:38.578619+00:00 | `20261011T184238Z-b-shapes0-nest-mb-free-upstream-default-s0-010ca6d8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 5s limit, one pass/one worker, upstream-default | valid; independent material 7.903032 | [record](output/lbf/20261011T184238Z-b-shapes0-nest-mb-free-upstream-default-s0-010ca6d8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:43:34.677390+00:00 | `20261011T184334Z-generated-lbf-constraints-identical-s0-343e5a63` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 5s limit, one pass/one worker, identical | failed; independent material none | [record](output/lbf/20261011T184334Z-generated-lbf-constraints-identical-s0-343e5a63/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:43:55.943225+00:00 | `20261011T184355Z-generated-lbf-constraints-identical-s0-a342e2d1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 5s limit, one pass/one worker, identical | valid; independent material 1.1246717541666666 | [record](output/lbf/20261011T184355Z-generated-lbf-constraints-identical-s0-a342e2d1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:16.305258+00:00 | `20261011T184516Z-b-albano-strip-sheet-identical-s0-4ae8ff92` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.9971891020408163 | [record](output/lbf/20261011T184516Z-b-albano-strip-sheet-identical-s0-4ae8ff92/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:16.699629+00:00 | `20261011T184516Z-b-albano-strip-sheet-upstream-default-s0-b8d40ead` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9971891020408163 | [record](output/lbf/20261011T184516Z-b-albano-strip-sheet-upstream-default-s0-b8d40ead/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:16.954206+00:00 | `20261011T184516Z-b-albano-nest-mb-given-identical-s0-8fc7451c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9426522302790596 | [record](output/lbf/20261011T184516Z-b-albano-nest-mb-given-identical-s0-8fc7451c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:17.235296+00:00 | `20261011T184517Z-b-albano-nest-mb-given-upstream-default-s0-af0cb757` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9426522302790596 | [record](output/lbf/20261011T184517Z-b-albano-nest-mb-given-upstream-default-s0-af0cb757/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:17.506394+00:00 | `20261011T184517Z-b-albano-nest-mb-free-identical-s0-2bb4415b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T184517Z-b-albano-nest-mb-free-identical-s0-2bb4415b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:17.793390+00:00 | `20261011T184517Z-b-albano-nest-mb-free-upstream-default-s0-85d1296f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T184517Z-b-albano-nest-mb-free-upstream-default-s0-85d1296f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:18.070906+00:00 | `20261011T184518Z-b-blaz1-strip-sheet-identical-s0-63cf06f3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.8002277333333336 | [record](output/lbf/20261011T184518Z-b-blaz1-strip-sheet-identical-s0-63cf06f3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:18.354576+00:00 | `20261011T184518Z-b-blaz1-strip-sheet-upstream-default-s0-918d931e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.8002277333333336 | [record](output/lbf/20261011T184518Z-b-blaz1-strip-sheet-upstream-default-s0-918d931e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:18.627823+00:00 | `20261011T184518Z-b-blaz1-nest-mb-given-identical-s0-52d3b7c0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 11.666872133333333 | [record](output/lbf/20261011T184518Z-b-blaz1-nest-mb-given-identical-s0-52d3b7c0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:18.965355+00:00 | `20261011T184518Z-b-blaz1-nest-mb-given-upstream-default-s0-daaca921` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 11.666872133333333 | [record](output/lbf/20261011T184518Z-b-blaz1-nest-mb-given-upstream-default-s0-daaca921/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:19.278491+00:00 | `20261011T184519Z-b-blaz1-nest-mb-free-identical-s0-627db35b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 13.5671944 | [record](output/lbf/20261011T184519Z-b-blaz1-nest-mb-free-identical-s0-627db35b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:19.655370+00:00 | `20261011T184519Z-b-blaz1-nest-mb-free-upstream-default-s0-cd186ea9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 13.5671944 | [record](output/lbf/20261011T184519Z-b-blaz1-nest-mb-free-upstream-default-s0-cd186ea9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:19.985712+00:00 | `20261011T184519Z-b-dagli-strip-sheet-identical-s0-77158b4d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.1669585333333332 | [record](output/lbf/20261011T184519Z-b-dagli-strip-sheet-identical-s0-77158b4d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:20.259517+00:00 | `20261011T184520Z-b-dagli-strip-sheet-upstream-default-s0-6092bbfb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.1669585333333332 | [record](output/lbf/20261011T184520Z-b-dagli-strip-sheet-upstream-default-s0-6092bbfb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:20.543614+00:00 | `20261011T184520Z-b-fu-strip-sheet-identical-s0-4ab1ae61` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.895080263157895 | [record](output/lbf/20261011T184520Z-b-fu-strip-sheet-identical-s0-4ab1ae61/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:20.831250+00:00 | `20261011T184520Z-b-fu-strip-sheet-upstream-default-s0-ca2de472` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.895080263157895 | [record](output/lbf/20261011T184520Z-b-fu-strip-sheet-upstream-default-s0-ca2de472/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:21.166444+00:00 | `20261011T184521Z-b-fu-nest-mb-given-identical-s0-5de2b343` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.476310142857143 | [record](output/lbf/20261011T184521Z-b-fu-nest-mb-given-identical-s0-5de2b343/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:21.426470+00:00 | `20261011T184521Z-b-fu-nest-mb-given-upstream-default-s0-e3f4f3c0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.476310142857143 | [record](output/lbf/20261011T184521Z-b-fu-nest-mb-given-upstream-default-s0-e3f4f3c0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:21.697193+00:00 | `20261011T184521Z-b-fu-nest-mb-free-identical-s0-d1c269b0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.671739952380952 | [record](output/lbf/20261011T184521Z-b-fu-nest-mb-free-identical-s0-d1c269b0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:21.969017+00:00 | `20261011T184521Z-b-fu-nest-mb-free-upstream-default-s0-bf3a07f9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.671739952380952 | [record](output/lbf/20261011T184521Z-b-fu-nest-mb-free-upstream-default-s0-bf3a07f9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:22.222484+00:00 | `20261011T184522Z-b-jakobs1-strip-sheet-identical-s0-550f1325` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.97662345 | [record](output/lbf/20261011T184522Z-b-jakobs1-strip-sheet-identical-s0-550f1325/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:22.531833+00:00 | `20261011T184522Z-b-jakobs1-strip-sheet-upstream-default-s0-6cd7d791` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.97662345 | [record](output/lbf/20261011T184522Z-b-jakobs1-strip-sheet-upstream-default-s0-6cd7d791/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:22.837710+00:00 | `20261011T184522Z-b-jakobs1-nest-mb-given-identical-s0-0640e80d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.834574583333334 | [record](output/lbf/20261011T184522Z-b-jakobs1-nest-mb-given-identical-s0-0640e80d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:23.157989+00:00 | `20261011T184523Z-b-jakobs1-nest-mb-given-upstream-default-s0-a8afe705` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.834574583333334 | [record](output/lbf/20261011T184523Z-b-jakobs1-nest-mb-given-upstream-default-s0-a8afe705/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:23.477989+00:00 | `20261011T184523Z-b-jakobs1-nest-mb-free-identical-s0-19f253aa` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.928895416666666 | [record](output/lbf/20261011T184523Z-b-jakobs1-nest-mb-free-identical-s0-19f253aa/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:23.825307+00:00 | `20261011T184523Z-b-jakobs1-nest-mb-free-upstream-default-s0-fa86c3b2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.928895416666666 | [record](output/lbf/20261011T184523Z-b-jakobs1-nest-mb-free-upstream-default-s0-fa86c3b2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:24.153606+00:00 | `20261011T184524Z-b-jakobs2-strip-sheet-identical-s0-7d7e6fde` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.987095 | [record](output/lbf/20261011T184524Z-b-jakobs2-strip-sheet-identical-s0-7d7e6fde/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:24.444771+00:00 | `20261011T184524Z-b-jakobs2-strip-sheet-upstream-default-s0-f645226a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.987095 | [record](output/lbf/20261011T184524Z-b-jakobs2-strip-sheet-upstream-default-s0-f645226a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:24.746927+00:00 | `20261011T184524Z-b-jakobs2-nest-mb-given-identical-s0-42ee555f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.916763708333333 | [record](output/lbf/20261011T184524Z-b-jakobs2-nest-mb-given-identical-s0-42ee555f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:25.073890+00:00 | `20261011T184525Z-b-jakobs2-nest-mb-given-upstream-default-s0-88bdf090` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.916763708333333 | [record](output/lbf/20261011T184525Z-b-jakobs2-nest-mb-given-upstream-default-s0-88bdf090/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:25.385219+00:00 | `20261011T184525Z-b-jakobs2-nest-mb-free-identical-s0-cb3a101b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.255797875 | [record](output/lbf/20261011T184525Z-b-jakobs2-nest-mb-free-identical-s0-cb3a101b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:25.724839+00:00 | `20261011T184525Z-b-jakobs2-nest-mb-free-upstream-default-s0-f5fbfc8c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.255797875 | [record](output/lbf/20261011T184525Z-b-jakobs2-nest-mb-free-upstream-default-s0-f5fbfc8c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:26.038267+00:00 | `20261011T184526Z-b-mao-strip-sheet-identical-s0-7eef78ae` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.9999798823529412 | [record](output/lbf/20261011T184526Z-b-mao-strip-sheet-identical-s0-7eef78ae/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:26.309078+00:00 | `20261011T184526Z-b-mao-strip-sheet-upstream-default-s0-58dd2969` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9999798823529412 | [record](output/lbf/20261011T184526Z-b-mao-strip-sheet-upstream-default-s0-58dd2969/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:26.573890+00:00 | `20261011T184526Z-b-mao-nest-mb-given-identical-s0-f83f5391` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.5218588878760255 | [record](output/lbf/20261011T184526Z-b-mao-nest-mb-given-identical-s0-f83f5391/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:26.855465+00:00 | `20261011T184526Z-b-mao-nest-mb-given-upstream-default-s0-adc7d05a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.5218588878760255 | [record](output/lbf/20261011T184526Z-b-mao-nest-mb-given-upstream-default-s0-adc7d05a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:27.130177+00:00 | `20261011T184527Z-b-mao-nest-mb-free-identical-s0-d7f01d59` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9936534986326344 | [record](output/lbf/20261011T184527Z-b-mao-nest-mb-free-identical-s0-d7f01d59/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:27.404677+00:00 | `20261011T184527Z-b-mao-nest-mb-free-upstream-default-s0-fb23394b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9936534986326344 | [record](output/lbf/20261011T184527Z-b-mao-nest-mb-free-upstream-default-s0-fb23394b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:27.678399+00:00 | `20261011T184527Z-b-marques-strip-sheet-identical-s0-7311756d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.6928079807692307 | [record](output/lbf/20261011T184527Z-b-marques-strip-sheet-identical-s0-7311756d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:27.958537+00:00 | `20261011T184527Z-b-marques-strip-sheet-upstream-default-s0-381062ae` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.6928079807692307 | [record](output/lbf/20261011T184527Z-b-marques-strip-sheet-upstream-default-s0-381062ae/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:28.218522+00:00 | `20261011T184528Z-b-shapes0-strip-sheet-identical-s0-c312b1df` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.95071125 | [record](output/lbf/20261011T184528Z-b-shapes0-strip-sheet-identical-s0-c312b1df/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:28.520768+00:00 | `20261011T184528Z-b-shapes0-strip-sheet-upstream-default-s0-977a932d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.95071125 | [record](output/lbf/20261011T184528Z-b-shapes0-strip-sheet-upstream-default-s0-977a932d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:28.821102+00:00 | `20261011T184528Z-b-shapes0-nest-mb-given-identical-s0-c15d6162` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.952538238095238 | [record](output/lbf/20261011T184528Z-b-shapes0-nest-mb-given-identical-s0-c15d6162/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:29.181241+00:00 | `20261011T184529Z-b-shapes0-nest-mb-given-upstream-default-s0-2d7ad6a6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.952538238095238 | [record](output/lbf/20261011T184529Z-b-shapes0-nest-mb-given-upstream-default-s0-2d7ad6a6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:29.529534+00:00 | `20261011T184529Z-b-shapes0-nest-mb-free-identical-s0-f4793304` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.903032 | [record](output/lbf/20261011T184529Z-b-shapes0-nest-mb-free-identical-s0-f4793304/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:29.895842+00:00 | `20261011T184529Z-b-shapes0-nest-mb-free-upstream-default-s0-199dd2bc` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.903032 | [record](output/lbf/20261011T184529Z-b-shapes0-nest-mb-free-upstream-default-s0-199dd2bc/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:30.277348+00:00 | `20261011T184530Z-b-shapes1-strip-sheet-identical-s0-97be0107` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9772045 | [record](output/lbf/20261011T184530Z-b-shapes1-strip-sheet-identical-s0-97be0107/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:30.601249+00:00 | `20261011T184530Z-b-shapes1-strip-sheet-upstream-default-s0-c73509cb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9772045 | [record](output/lbf/20261011T184530Z-b-shapes1-strip-sheet-upstream-default-s0-c73509cb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:30.911865+00:00 | `20261011T184530Z-b-shapes1-nest-mb-given-identical-s0-e5a9a668` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 8.286119333333334 | [record](output/lbf/20261011T184530Z-b-shapes1-nest-mb-given-identical-s0-e5a9a668/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:31.274249+00:00 | `20261011T184531Z-b-shapes1-nest-mb-given-upstream-default-s0-d03a6035` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.286119333333334 | [record](output/lbf/20261011T184531Z-b-shapes1-nest-mb-given-upstream-default-s0-d03a6035/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:31.634171+00:00 | `20261011T184531Z-b-shapes1-nest-mb-free-identical-s0-c617d8a9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.903032 | [record](output/lbf/20261011T184531Z-b-shapes1-nest-mb-free-identical-s0-c617d8a9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:32.019855+00:00 | `20261011T184532Z-b-shapes1-nest-mb-free-upstream-default-s0-09cd5fec` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.903032 | [record](output/lbf/20261011T184532Z-b-shapes1-nest-mb-free-upstream-default-s0-09cd5fec/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:32.385861+00:00 | `20261011T184532Z-b-shirts-strip-sheet-identical-s0-bf215c30` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9999089500000005 | [record](output/lbf/20261011T184532Z-b-shirts-strip-sheet-identical-s0-bf215c30/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:32.759099+00:00 | `20261011T184532Z-b-shirts-strip-sheet-upstream-default-s0-468c6ba8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9999089500000005 | [record](output/lbf/20261011T184532Z-b-shirts-strip-sheet-upstream-default-s0-468c6ba8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:33.131658+00:00 | `20261011T184533Z-b-shirts-nest-mb-given-identical-s0-c746befa` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 8.771087641025641 | [record](output/lbf/20261011T184533Z-b-shirts-nest-mb-given-identical-s0-c746befa/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:33.585046+00:00 | `20261011T184533Z-b-shirts-nest-mb-given-upstream-default-s0-299b6b85` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.771087641025641 | [record](output/lbf/20261011T184533Z-b-shirts-nest-mb-given-upstream-default-s0-299b6b85/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:34.042222+00:00 | `20261011T184534Z-b-shirts-nest-mb-free-identical-s0-f6b71b3d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.985671487179487 | [record](output/lbf/20261011T184534Z-b-shirts-nest-mb-free-identical-s0-f6b71b3d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:34.498564+00:00 | `20261011T184534Z-b-shirts-nest-mb-free-upstream-default-s0-64b29a28` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.985671487179487 | [record](output/lbf/20261011T184534Z-b-shirts-nest-mb-free-upstream-default-s0-64b29a28/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:34.941735+00:00 | `20261011T184534Z-b-swim-strip-sheet-identical-s0-57537e2d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.9999601877607789 | [record](output/lbf/20261011T184534Z-b-swim-strip-sheet-identical-s0-57537e2d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:35.269362+00:00 | `20261011T184535Z-b-swim-strip-sheet-upstream-default-s0-e2b77428` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9999494089012517 | [record](output/lbf/20261011T184535Z-b-swim-strip-sheet-upstream-default-s0-e2b77428/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:35.594511+00:00 | `20261011T184535Z-b-swim-nest-mb-given-identical-s0-5c400978` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 5.4671329918460385 | [record](output/lbf/20261011T184535Z-b-swim-nest-mb-given-identical-s0-5c400978/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:35.967754+00:00 | `20261011T184535Z-b-swim-nest-mb-given-upstream-default-s0-24448d34` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.31013764406947 | [record](output/lbf/20261011T184535Z-b-swim-nest-mb-given-upstream-default-s0-24448d34/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:36.333706+00:00 | `20261011T184536Z-b-swim-nest-mb-free-identical-s0-5ff6c066` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 5.9654123881329495 | [record](output/lbf/20261011T184536Z-b-swim-nest-mb-free-identical-s0-5ff6c066/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:36.696822+00:00 | `20261011T184536Z-b-swim-nest-mb-free-upstream-default-s0-6cf6cb4a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.641789552791679 | [record](output/lbf/20261011T184536Z-b-swim-nest-mb-free-upstream-default-s0-6cf6cb4a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:37.067459+00:00 | `20261011T184537Z-b-trousers-strip-sheet-identical-s0-1a48e40e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.983522405063291 | [record](output/lbf/20261011T184537Z-b-trousers-strip-sheet-identical-s0-1a48e40e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:37.399451+00:00 | `20261011T184537Z-b-trousers-strip-sheet-upstream-default-s0-f902d553` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.983522405063291 | [record](output/lbf/20261011T184537Z-b-trousers-strip-sheet-upstream-default-s0-f902d553/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:37.738585+00:00 | `20261011T184537Z-b-trousers-nest-mb-given-identical-s0-ec6de8dc` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.5117278418079096 | [record](output/lbf/20261011T184537Z-b-trousers-nest-mb-given-identical-s0-ec6de8dc/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:38.107996+00:00 | `20261011T184538Z-b-trousers-nest-mb-given-upstream-default-s0-08c260e0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.5117278418079096 | [record](output/lbf/20261011T184538Z-b-trousers-nest-mb-given-upstream-default-s0-08c260e0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:38.451253+00:00 | `20261011T184538Z-b-trousers-nest-mb-free-identical-s0-ec3a95b5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.716267604519774 | [record](output/lbf/20261011T184538Z-b-trousers-nest-mb-free-identical-s0-ec3a95b5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:45:38.794758+00:00 | `20261011T184538Z-b-trousers-nest-mb-free-upstream-default-s0-b181e6f9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.716267604519774 | [record](output/lbf/20261011T184538Z-b-trousers-nest-mb-free-upstream-default-s0-b181e6f9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:47:59.126199+00:00 | verified provisional LBF batch `20261011T184516Z-9dbe9b01` | 70/70 valid, seed 0, B only | [table](benchmarks/results/lbf-20261011T184759Z-924100e9.md). Full M1 and quality gates remain pending.

- 2026-10-11T18:49:13.150934+00:00 | `20261011T184913Z-generated-lbf-impossible-identical-s0-a9f86922` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 5s limit, one pass/one worker, identical | invalid; independent material none | [record](output/lbf/20261011T184913Z-generated-lbf-impossible-identical-s0-a9f86922/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:49:14.195222+00:00 | `20261011T184914Z-generated-lbf-timeout-identical-s0-7dc86e41` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `52eba70a201176d3b064ee8bf0eb849574f91468` (dirty=True) | seed 0, 1s limit, one pass/one worker, identical | timeout; independent material none | [record](output/lbf/20261011T184914Z-generated-lbf-timeout-identical-s0-7dc86e41/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T18:56:24.834747+00:00 | M0 `published-20261011/shapes1-0` | completed_integrity_checked | 1200s, 3 workers | length 52.521824 | [record](output/m0/published-20261011/shapes1-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:56:24.912044+00:00 | M0 `published-20261011/swim-0` | completed_integrity_checked | 1200s, 3 workers | length 5674.9463 | [record](output/m0/published-20261011/swim-0/run.json). Geometry validation pending M1.

- 2026-10-11T18:56:25.230575+00:00 | M0 `published-20261011/shirts-0` | completed_integrity_checked | 1200s, 3 workers | length 60.579433 | [record](output/m0/published-20261011/shirts-0/run.json). Geometry validation pending M1.

- 2026-10-11T19:02:01.868625+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-15bdf3e9f2.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:01.928777+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-1899ea309b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:01.978463+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-9b2d1db037.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.032668+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-b6651adf1e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.084488+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-a3cf635a4f.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.140500+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-e5e4bf7c0c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.209901+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-0262581ba3.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.269298+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-cb837c3a80.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.325713+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-203e7dafd4.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.379974+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-c1a9ba725b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.433865+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-317e5e15ec.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:02:02.490595+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-8826f83cf3.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:16:25.252258+00:00 | M0 `published-20261011/albano-1` | completed_integrity_checked | 1200s, 3 workers | length 9804.68 | [record](output/m0/published-20261011/albano-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:16:25.547759+00:00 | M0 `published-20261011/blaz1-1` | completed_integrity_checked | 1200s, 3 workers | length 25.67041 | [record](output/m0/published-20261011/blaz1-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:16:25.615680+00:00 | M0 `published-20261011/trousers-0` | completed_integrity_checked | 1200s, 3 workers | length 237.01588 | [record](output/m0/published-20261011/trousers-0/run.json). Geometry validation pending M1.

- 2026-10-11T19:18:55.600977+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-97fb23dcbc.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:55.745086+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-2e9a26029d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:55.896747+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-d416b21c8b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.159651+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-bf72bad6f9.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.302376+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-e760aa6552.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.381286+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-cdf620ed81.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.442618+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-10f2fe06ab.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.672895+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-b2a02f0564.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.788357+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-163af795e6.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:56.910816+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-34321f2f1b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:57.062598+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-427ec19b38.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:57.134040+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-4bf27ba844.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:57.207582+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-34a2c1d2ae.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:57.293106+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-d32d546d6b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:18:57.358047+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-31e77a18ee.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:19:54.227859+00:00 | M0 checkpoint: 15/39 full-budget runs, all independently valid; all thirteen instances have one seed and ALBANO/SHAPES2 have two. Three-seed quality gate remains incomplete. [Retained evidence](benchmarks/results/m0-first-fifteen-20261011.json).

- 2026-10-11T19:19:54.227859+00:00 | Maker source freeze: 40 jobs with 10 held-out reservations before optimiser tuning. All 40 source contracts and complete one-copy-per-sheet feasibility witnesses pass independently. Fresh isolated installation rebuilds jobs and retained curves byte for byte; four curve-bound/topology tests and three freeze/coverage tests pass. [Manifest](benchmarks/datasets/makers.json), [authoring evidence](benchmarks/datasets/maker-feasibility.json), [method and licences](benchmarks/makers/README.md). No nesting quality or milestone pass is claimed.

- 2026-10-11T19:31:06.941911+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T193059Z-e7f62151/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:31:15.192343+00:00 | SVGnest `svgnest-hole-margin-smoke` seed 0, 5s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T193107Z-84d7d464/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:33:28.994272+00:00 | SVGnest `svgnest-hole-margin-smoke` seed 0, 5s, identical, axis y | valid | material 0.135 | [record](output/playwright/svgnest/20261011T193321Z-1060b268/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:35:39.620163+00:00 | SVGnest `m-box-mini` seed 0, 5s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T193530Z-16bffdf0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:35:48.159071+00:00 | SVGnest `svgnest-hole-margin-smoke` seed 0, 5s, expanded, axis x | valid | material 0.19 | [record](output/playwright/svgnest/20261011T193539Z-700edbd3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:36:25.782975+00:00 | M0 `published-20261011/dagli-1` | completed_integrity_checked | 1200s, 3 workers | length 56.56602 | [record](output/m0/published-20261011/dagli-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:36:26.058822+00:00 | M0 `published-20261011/fu-1` | completed_integrity_checked | 1200s, 3 workers | length 30.846144 | [record](output/m0/published-20261011/fu-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:36:26.073354+00:00 | M0 `published-20261011/jakobs1-1` | completed_integrity_checked | 1200s, 3 workers | length 11.000162 | [record](output/m0/published-20261011/jakobs1-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:41:45.311707+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-6aa82810ba.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.360175+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-8fd280f6a2.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.409911+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-2c9d3e0387.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.458206+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-fb1045d01b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.508563+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-acc4b6cb8c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.556024+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-2106bac800.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.604100+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-b4c5470899.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.650943+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-9b8aa071d6.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.700290+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-f163205a15.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.748001+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-db26d80a3a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.800555+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-9d79dcb47b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.852498+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-36fb4d9397.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.908481+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-9de104be2c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:45.965990+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-26bf2acb52.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:46.036884+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-b5bf1fd39b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:46.088172+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-8bfb7b0716.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:46.142441+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-6c76938f17.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:41:46.192823+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-b0be7a8167.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T19:42:29.943056+00:00 | SVGnest `svgnest-independent-edge-gap` seed 0, 5s, identical, axis y | valid | material 0.195 | [record](output/playwright/svgnest/20261011T194221Z-d3b42bd5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:42:44.956648+00:00 | SVGnest `svgnest-stock-cap-failure` seed 0, 5s, identical, axis x | invalid | material None | [record](output/playwright/svgnest/20261011T194237Z-1fcb9046/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:43:05.389233+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T194257Z-998a7ee8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:44:11.283887+00:00 | SVGnest `m-box-mini` seed 0, 30s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T194407Z-b8b88baf/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:44:41.015297+00:00 | SVGnest `svgnest-independent-edge-gap` seed 0, 1s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T194437Z-9c7a0451/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:45:24.861160+00:00 | SVGnest `svgnest-independent-edge-gap` seed 0, 5s, identical, axis y | valid | material 0.195 | [record](output/playwright/svgnest/20261011T194515Z-8cf530ee/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:46:14.509938+00:00 | SVGnest `m-box-mini` seed 0, 30s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T194540Z-321e6a09/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:48:11.607934+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T194801Z-d25fa363/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:49:25.608461+00:00 | verified SVGnest batch `20261011T194801Z-823aff60` | 1 selected B outcomes retained | [table](benchmarks/results/svgnest-20261011T194925Z-bd80ec55.md). Provisional; full M1 and all quality gates pending.

- 2026-10-11T19:49:38.257125+00:00 | SVGnest `svgnest-stock-cap-failure` seed 0, 5s, identical, axis x | invalid | material None | [record](output/playwright/svgnest/20261011T194926Z-1fb80e38/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:51:25.468514+00:00 | retained 18/39 M0 runs and all 18 independent checks | [checkpoint](benchmarks/results/m0-first-eighteen-20261011.json). Incomplete; M0 gate remains pending.

- 2026-10-11T19:51:25.468514+00:00 | retained all 14 SVGnest preparation attempts, including no-layout/invalid/failed outcomes and superseded settings | [evidence](benchmarks/results/svgnest-preparation-20261011.json). Geometry/runner preparation only, not quality or performance claims.

- 2026-10-11T19:54:00.632328+00:00 | SVGnest `b-albano-nest-mb-free` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T195255Z-17bbcda0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:55:05.005496+00:00 | SVGnest `b-albano-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 2.902177556580971 | [record](output/playwright/svgnest/20261011T195400Z-c515cc6c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:56:10.311321+00:00 | SVGnest `b-albano-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.7802481265306123 | [record](output/playwright/svgnest/20261011T195505Z-c3c40163/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:56:42.315363+00:00 | M0 `published-20261011/marques-1` | completed_integrity_checked | 1200s, 3 workers | length 75.527275 | [record](output/m0/published-20261011/marques-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:56:42.387335+00:00 | M0 `published-20261011/jakobs2-1` | completed_integrity_checked | 1200s, 3 workers | length 22.669336 | [record](output/m0/published-20261011/jakobs2-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:56:42.519839+00:00 | M0 `published-20261011/mao-1` | completed_integrity_checked | 1200s, 3 workers | length 1714.6738 | [record](output/m0/published-20261011/mao-1/run.json). Geometry validation pending M1.

- 2026-10-11T19:57:15.951849+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T195610Z-7de05666/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:58:21.228593+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T195716Z-1368c5b1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T19:59:26.433548+00:00 | SVGnest `b-blaz1-strip-sheet` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T195821Z-54d68ddc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:00:32.328649+00:00 | SVGnest `b-dagli-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.1233333666666665 | [record](output/playwright/svgnest/20261011T195926Z-2385b1e6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:00:55.861160+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T200007Z-ebadbdec/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:00:57.441052+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-d264eda3cb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.505802+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-9931f0aa66.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.573996+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-07eceea25a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.632375+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-b46722c12b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.696501+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-21faae0581.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.759015+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-b18ab14741.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.822269+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-41e06ba1cf.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.888982+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-024f4a0dca.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:57.957476+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-52df94e7fc.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.024231+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-97541597b9.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.095964+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-3ba3d44bfd.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.174010+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-9eb63227b3.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.240603+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-35eabee710.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.330759+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-c108ccaa6d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.411313+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-16a2aafcb8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.485949+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-70b8785e42.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.557623+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-52992b8896.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.626433+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-a2fb3576ef.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.699955+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-891ba6a262.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.782846+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-8c97e64de6.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:00:58.867888+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-8223871974.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:01:41.393548+00:00 | SVGnest `b-fu-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T200032Z-4db9e465/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:02:16.232723+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T200119Z-aae49301/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:02:46.548665+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T200141Z-8fe77360/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:03:49.434185+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T200321Z-53450028/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:03:51.937163+00:00 | SVGnest `b-fu-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.4678362894736843 | [record](output/playwright/svgnest/20261011T200246Z-b1ce9018/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:05:00.489270+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 4.583333333333333 | [record](output/playwright/svgnest/20261011T200352Z-a02eb918/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:05:51.389680+00:00 | deepnest-next `svgnest-stock-cap-failure` seed 0, 5s, identical, axis x | timeout | material None | [record](output/playwright/deepnest/20261011T200412Z-78b17d5f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:06:08.399116+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 4.583333333333333 | [record](output/playwright/svgnest/20261011T200500Z-d821f87b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:07:08.184933+00:00 | deepnest-next `svgnest-stock-cap-failure` seed 0, 5s, identical, axis x | invalid | material None | [record](output/playwright/deepnest/20261011T200649Z-e600e833/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:07:14.297551+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.825 | [record](output/playwright/svgnest/20261011T200608Z-8b3eda3b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:08:20.939931+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.875 | [record](output/playwright/svgnest/20261011T200714Z-68166b0f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:08:57.907182+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, clearance-safe, axis y | failed | material None | [record](output/playwright/deepnest/20261011T200741Z-f3e0b6da/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:09:25.835949+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.875 | [record](output/playwright/svgnest/20261011T200821Z-1525e6d5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:10:30.169476+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.8833333142857143 | [record](output/playwright/svgnest/20261011T200925Z-0855f76a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:11:08.749430+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, clearance-safe, axis y | failed | material None | [record](output/playwright/deepnest/20261011T200949Z-24709b3f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:11:35.012085+00:00 | SVGnest `b-mao-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 1.8961903087207534 | [record](output/playwright/svgnest/20261011T201030Z-c9128f61/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:12:41.015441+00:00 | SVGnest `b-mao-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 2.5017777532664844 | [record](output/playwright/svgnest/20261011T201135Z-c37e274c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:13:05.814029+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, clearance-safe, axis y | failed | material None | [record](output/playwright/deepnest/20261011T201156Z-18afe663/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:13:48.070774+00:00 | SVGnest `b-mao-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.893629557647059 | [record](output/playwright/svgnest/20261011T201241Z-5d79b847/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:15:00.366574+00:00 | SVGnest `b-marques-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.1923076923076923 | [record](output/playwright/svgnest/20261011T201348Z-0f0a827e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:15:26.282141+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, clearance-safe, axis y | valid | material 0.195 | [record](output/playwright/deepnest/20261011T201505Z-756127a0/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:16:09.014366+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T201501Z-85934d02/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:16:42.921145+00:00 | M0 `published-20261011/shapes0-1` | completed_integrity_checked | 1200s, 3 workers | length 58.773052 | [record](output/m0/published-20261011/shapes0-1/run.json). Geometry validation pending M1.

- 2026-10-11T20:16:42.921145+00:00 | M0 `published-20261011/shapes1-1` | completed_integrity_checked | 1200s, 3 workers | length 53.037033 | [record](output/m0/published-20261011/shapes1-1/run.json). Geometry validation pending M1.

- 2026-10-11T20:16:43.529230+00:00 | M0 `published-20261011/shirts-1` | completed_integrity_checked | 1200s, 3 workers | length 60.105885 | [record](output/m0/published-20261011/shirts-1/run.json). Geometry validation pending M1.

- 2026-10-11T20:17:17.500278+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T201609Z-d2caf129/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:18:02.938912+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-8cd01d14bf.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.008478+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-6eada38810.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.088010+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-1e972b4369.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.161419+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-41f42ac5eb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.245156+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-a54a149d3e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.326057+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-495ba02f68.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.467064+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-2852537042.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.618760+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-6438add3ce.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.831019+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-4bded9e359.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:03.962906+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-4c395b7001.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.171075+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-bf4fb159aa.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.249021+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-5269da182e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.366486+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-ac92ab0398.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.517035+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-a681ceec29.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.676123+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-2b34093679.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.780171+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-bada454985.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:04.926299+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-07503cc01e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:05.086175+00:00 | independent geometry check `published-20261011/shapes0-1` | valid | [report](output/m0/published-20261011/shapes0-1/validation-52e15f7fe2.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:05.306247+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-33d2c66a3b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:05.467899+00:00 | independent geometry check `published-20261011/shapes1-1` | valid | [report](output/m0/published-20261011/shapes1-1/validation-831629162a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:05.787579+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-6277a8225d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:06.001099+00:00 | independent geometry check `published-20261011/shirts-1` | valid | [report](output/m0/published-20261011/shirts-1/validation-e1c12d8776.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:06.158701+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-78cdf5f68b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:06.260062+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-8d9195e508.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:18:23.544820+00:00 | SVGnest `b-shapes0-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261011T201717Z-047edce1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:19:28.220127+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T201823Z-516669f3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:20:50.875109+00:00 | deepnest-next `deepnest-mixed-stock-constraints` seed 0, 5s, clearance-safe, axis y | failed | material None | [record](output/playwright/deepnest/20261011T201935Z-0c0435ac/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:21:21.985182+00:00 | SVGnest output-decoder correction for all 38 selected records | [audit](benchmarks/results/svgnest-correction-20261011T202121Z-ad4dbe52.md). Native search unchanged, originals retained, full-precision SVG attributes revalidated. Provisional only.

- 2026-10-11T20:23:04.622016+00:00 | SVGnest output-decoder correction for all 24 selected records | [audit](benchmarks/results/svgnest-correction-20261011T202304Z-3f63b428.md). Native search unchanged, originals retained, full-precision SVG attributes revalidated. Provisional only.

- 2026-10-11T20:24:47.416516+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T202436Z-81a525a5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:24:52.044475+00:00 | deepnest-next `deepnest-mixed-stock-constraints` seed 0, 5s, clearance-safe, axis y | valid | material 1.0166666666666666 | [record](output/playwright/deepnest/20261011T202435Z-cd977646/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:27:40.533151+00:00 | retained all 11 deepnest-next preparation outcomes | [evidence](benchmarks/results/deepnest-preparation-20261011.json). Valid academic, conservative spacing and mixed-stock fixtures; initialization and constraint failures also retained. Full matrix remains pending.

- 2026-10-11T20:31:52.211045+00:00 | M0 checkpoint: 24/39 completed runs, all independently valid. [Immutable records and checks](benchmarks/results/m0-first-twenty-four-20261011.json). Three-seed quality comparison remains pending; no milestone pass.

- 2026-10-11T20:33:01.183548+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T203237Z-3e5e78e2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:33:37.447435+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T203228Z-74c3492a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:33:50.852555+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T203322Z-97e84a73/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:34:26.471230+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T203351Z-0da848ee/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:34:44.868254+00:00 | SVGnest `b-shapes1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.65 | [record](output/playwright/svgnest/20261011T203337Z-a8329990/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:35:53.641411+00:00 | SVGnest `b-shirts-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.615384615384615 | [record](output/playwright/svgnest/20261011T203445Z-aec3f5a7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:36:44.026752+00:00 | M0 `published-20261011/swim-1` | completed_integrity_checked | 1200s, 3 workers | length 5637.329 | [record](output/m0/published-20261011/swim-1/run.json). Geometry validation pending M1.

- 2026-10-11T20:36:44.402834+00:00 | M0 `published-20261011/albano-2` | completed_integrity_checked | 1200s, 3 workers | length 9770.604 | [record](output/m0/published-20261011/albano-2/run.json). Geometry validation pending M1.

- 2026-10-11T20:36:44.826463+00:00 | M0 `published-20261011/trousers-1` | completed_integrity_checked | 1200s, 3 workers | length 237.65578 | [record](output/m0/published-20261011/trousers-1/run.json). Geometry validation pending M1.

- 2026-10-11T20:36:59.732105+00:00 | SVGnest `b-shirts-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 8.940170923076924 | [record](output/playwright/svgnest/20261011T203553Z-db21abff/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:37:31.394698+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-b8ee67a1be.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:31.457255+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-96e400b163.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:31.577442+00:00 | independent geometry check `published-20261011/albano-2` | valid | [report](output/m0/published-20261011/albano-2/validation-7f4d2b6cee.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:31.800974+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-3f30c56a2b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:31.953633+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-1dea776c45.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.035660+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-bd576573c5.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.103824+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-91a561ef71.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.220889+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-d2999399eb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.301316+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-9fb681ec21.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.543218+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-fe6b579dad.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.691537+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-663dc88b86.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.781323+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-dda21d3874.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.858119+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-c165878516.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.916979+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-c11ff5a194.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:32.977326+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-48e13cf12c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.076388+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-38cff7a02e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.140641+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-4f083701c7.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.199427+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-8661a74ba1.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.255786+00:00 | independent geometry check `published-20261011/shapes0-1` | valid | [report](output/m0/published-20261011/shapes0-1/validation-f38e6b3664.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.312385+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-7e3b1e414d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.371157+00:00 | independent geometry check `published-20261011/shapes1-1` | valid | [report](output/m0/published-20261011/shapes1-1/validation-80ba3f218e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.487875+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-3253863269.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.654787+00:00 | independent geometry check `published-20261011/shirts-1` | valid | [report](output/m0/published-20261011/shirts-1/validation-5cca29508a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.788171+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-e53ff1da92.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.861833+00:00 | independent geometry check `published-20261011/swim-1` | valid | [report](output/m0/published-20261011/swim-1/validation-431fc28213.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:33.999089+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-cae3666ca0.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:37:34.077616+00:00 | independent geometry check `published-20261011/trousers-1` | valid | [report](output/m0/published-20261011/trousers-1/validation-cfe81e5d7f.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:38:05.125742+00:00 | SVGnest `b-shirts-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.7601461 | [record](output/playwright/svgnest/20261011T203659Z-cf0b31af/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:38:06.340694+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | timeout | material None | [record](output/playwright/deepnest/20261011T203427Z-54187460/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:39:15.343597+00:00 | SVGnest `b-swim-nest-mb-free` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T203805Z-f15456c5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:39:46.757781+00:00 | current Sparrow `s-fu-strip` seed 0, 5s, identical, axis x | valid | score 32.762651443481445 | [record](output/sparrow-benchmark/20261011T203938Z-ad2ef307/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:40:26.195411+00:00 | SVGnest `b-swim-nest-mb-given` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T203917Z-39000087/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:41:03.865223+00:00 | current Sparrow `b-fu-strip-sheet` seed 0, 5s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T204056Z-70fc2770/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:41:36.886817+00:00 | SVGnest `b-swim-strip-sheet` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T204026Z-5362091a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:41:37.320261+00:00 | current Sparrow `sparrow-independent-edge-gap` seed 0, 5s, identical, axis y | valid | score 0.3800540599999999 | [record](output/sparrow-benchmark/20261011T204135Z-3fc6fe3a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:42:32.816223+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T204223Z-1a0945fd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:42:41.853443+00:00 | SVGnest `b-trousers-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 2.7105826553672316 | [record](output/playwright/svgnest/20261011T204137Z-a04bf092/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:43:46.733523+00:00 | SVGnest `b-trousers-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.4180790960451977 | [record](output/playwright/svgnest/20261011T204241Z-6ce0aa31/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:44:17.643180+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T204411Z-f5e61880/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:44:51.015228+00:00 | SVGnest `b-trousers-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.329113924050633 | [record](output/playwright/svgnest/20261011T204346Z-8965ef37/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:45:02.988717+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T204451Z-5349c04d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:45:13.576475+00:00 | verified SVGnest batch `20261011T203228Z-43bd2875` | 11 selected B outcomes retained | [table](benchmarks/results/svgnest-20261011T204513Z-1f07ec81.md). Provisional; full M1 and all quality gates pending.

- 2026-10-11T20:46:09.881817+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T204557Z-599d5d0e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:46:22.628097+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T204610Z-adbc67d7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:46:35.065850+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T204622Z-2b92e355/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:48:16.267832+00:00 | Retained [all Deepnest startup trials](benchmarks/results/deepnest-startup-20261011.json), [three current Sparrow adapter trials](benchmarks/results/sparrow-preparation-20261011.json), and [27/39 M0 runs](benchmarks/results/m0-first-twenty-seven-20261011.json). First full three-seed ALBANO comparison passes; remaining instances pending. No completed milestone claimed.

- 2026-10-11T20:49:48.654243+00:00 | current Sparrow `s-albano-strip` seed 0, 60s, identical, axis x | valid | score 9943.8603515625 | [record](output/sparrow-benchmark/20261011T204844Z-6726fe59/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:50:50.463666+00:00 | current Sparrow `s-blaz1-strip` seed 0, 60s, identical, axis x | valid | score 26.276668548583984 | [record](output/sparrow-benchmark/20261011T204948Z-2285b9e6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:51:52.228670+00:00 | current Sparrow `s-dagli-strip` seed 0, 60s, identical, axis x | valid | score 58.866859436035156 | [record](output/sparrow-benchmark/20261011T205050Z-868d1838/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:52:06.585708+00:00 | deepnest-next `b-albano-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 2.799165018677214 | [record](output/playwright/deepnest/20261011T205057Z-0b6d9ee5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:52:54.053771+00:00 | current Sparrow `s-fu-strip` seed 0, 60s, identical, axis x | valid | score 32.16831970214844 | [record](output/sparrow-benchmark/20261011T205152Z-648fdc76/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:53:19.773059+00:00 | deepnest-next `b-albano-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 2.844649527576357 | [record](output/playwright/deepnest/20261011T205206Z-68684d77/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:53:56.275326+00:00 | current Sparrow `s-jakobs1-strip` seed 0, 60s, identical, axis x | valid | score 11.34487533569336 | [record](output/sparrow-benchmark/20261011T205254Z-ae1eb1c3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:54:27.202492+00:00 | deepnest-next `b-albano-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.7846551124489796 | [record](output/playwright/deepnest/20261011T205319Z-33e437a8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:54:58.084373+00:00 | current Sparrow `s-jakobs2-strip` seed 0, 60s, identical, axis x | valid | score 24.01105499267578 | [record](output/sparrow-benchmark/20261011T205356Z-d3896d8f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:55:10.144883+00:00 | verified deepnest batch `20261011T205057Z-85c116e8` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T205510Z-c961f172.md). Provisional; all failures retained.

- 2026-10-11T20:56:00.361247+00:00 | current Sparrow `s-mao-strip` seed 0, 60s, identical, axis x | valid | score 1778.25439453125 | [record](output/sparrow-benchmark/20261011T205458Z-5368e92b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:56:29.864755+00:00 | deepnest-next `b-blaz1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 9.666666666666666 | [record](output/playwright/deepnest/20261011T205517Z-2d547265/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:56:44.601896+00:00 | M0 `published-20261011/blaz1-2` | completed_integrity_checked | 1200s, 3 workers | length 25.53159 | [record](output/m0/published-20261011/blaz1-2/run.json). Geometry validation pending M1.

- 2026-10-11T20:56:45.048104+00:00 | M0 `published-20261011/fu-2` | completed_integrity_checked | 1200s, 3 workers | length 30.846409 | [record](output/m0/published-20261011/fu-2/run.json). Geometry validation pending M1.

- 2026-10-11T20:56:45.516580+00:00 | M0 `published-20261011/dagli-2` | completed_integrity_checked | 1200s, 3 workers | length 56.75514 | [record](output/m0/published-20261011/dagli-2/run.json). Geometry validation pending M1.

- 2026-10-11T20:56:48.670874+00:00 | SVGnest `b-albano-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 3.3564093236651282 | [record](output/playwright/svgnest/20261011T205540Z-0970bd5b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:57:02.423618+00:00 | current Sparrow `s-marques-strip` seed 0, 60s, identical, axis x | valid | score 77.65225982666016 | [record](output/sparrow-benchmark/20261011T205600Z-141682bd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:57:08.994131+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-a358e9862d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.070090+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-02ab38c3d9.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.144625+00:00 | independent geometry check `published-20261011/albano-2` | valid | [report](output/m0/published-20261011/albano-2/validation-c25a9c0f5d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.226306+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-c3f1c4f310.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.295789+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-3bd016f21c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.384390+00:00 | independent geometry check `published-20261011/blaz1-2` | valid | [report](output/m0/published-20261011/blaz1-2/validation-9b1e2d5b56.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.483088+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-ec41aa478c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.548010+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-32ecc776af.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.638246+00:00 | independent geometry check `published-20261011/dagli-2` | valid | [report](output/m0/published-20261011/dagli-2/validation-e31ff5686d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.702535+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-e1a0fe09ce.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.805065+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-0d4d2fe6a6.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.868675+00:00 | independent geometry check `published-20261011/fu-2` | valid | [report](output/m0/published-20261011/fu-2/validation-27b5d982a8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:09.997677+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-e49b8d6315.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.157592+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-1ff7454230.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.228041+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-cfb9e0b93b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.388539+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-e52fe32a33.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.468725+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-a4f2618554.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.530023+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-687544f941.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.601202+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-1a35d97ac2.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.665904+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-0077486642.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.735150+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-549e32004c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.795978+00:00 | independent geometry check `published-20261011/shapes0-1` | valid | [report](output/m0/published-20261011/shapes0-1/validation-a0d85f2fee.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.884689+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-6da9ab6792.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:10.975802+00:00 | independent geometry check `published-20261011/shapes1-1` | valid | [report](output/m0/published-20261011/shapes1-1/validation-333f56787a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:11.078543+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-11e494e7dc.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:11.153055+00:00 | independent geometry check `published-20261011/shirts-1` | valid | [report](output/m0/published-20261011/shirts-1/validation-31c4aa0bc8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:11.234386+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-d2dc04cced.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:11.307259+00:00 | independent geometry check `published-20261011/swim-1` | valid | [report](output/m0/published-20261011/swim-1/validation-49defd05cf.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:11.399371+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-7668968a21.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:11.464080+00:00 | independent geometry check `published-20261011/trousers-1` | valid | [report](output/m0/published-20261011/trousers-1/validation-dd0894edfc.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T20:57:38.326442+00:00 | deepnest-next `b-blaz1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 9.766666666666667 | [record](output/playwright/deepnest/20261011T205630Z-da8cc685/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:57:54.125874+00:00 | SVGnest `b-albano-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 4.161722698308064 | [record](output/playwright/svgnest/20261011T205648Z-48813117/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:58:04.754189+00:00 | current Sparrow `s-shapes0-strip` seed 0, 60s, identical, axis x | valid | score 61.06184768676758 | [record](output/sparrow-benchmark/20261011T205702Z-879dee50/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:58:49.296123+00:00 | deepnest-next `b-blaz1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 3.3333333333333335 | [record](output/playwright/deepnest/20261011T205738Z-9956b821/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T20:58:59.448355+00:00 | SVGnest `b-albano-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 3.150204081632653 | [record](output/playwright/svgnest/20261011T205754Z-50ae1013/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T20:59:07.151056+00:00 | current Sparrow `s-shapes1-strip` seed 0, 60s, identical, axis x | valid | score 54.495262145996094 | [record](output/sparrow-benchmark/20261011T205804Z-c223ac14/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T20:59:45.978562+00:00 | verified deepnest batch `20261011T205517Z-aced919d` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T205945Z-dfbb847c.md). Provisional; all failures retained.

- 2026-10-11T21:00:09.557780+00:00 | current Sparrow `s-shirts-strip` seed 0, 60s, identical, axis x | valid | score 61.87604904174805 | [record](output/sparrow-benchmark/20261011T205907Z-ed5d42d1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:00:18.661745+00:00 | verified SVGnest batch `20261011T205540Z-10313e98` | 3 selected B outcomes retained | [table](benchmarks/results/svgnest-20261011T210018Z-b7d68a2f.md). Provisional; full M1 and all quality gates pending.

- 2026-10-11T21:01:12.004309+00:00 | current Sparrow `s-swim-strip` seed 0, 60s, identical, axis x | valid | score 5954.77880859375 | [record](output/sparrow-benchmark/20261011T210009Z-c7d73d36/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:02:14.555650+00:00 | current Sparrow `s-trousers-strip` seed 0, 60s, identical, axis x | valid | score 241.4627685546875 | [record](output/sparrow-benchmark/20261011T210112Z-0124197c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:03:36.870549+00:00 | verified sparrow batch `20261011T204844Z-a05845ae` | 13/13 valid | [table](benchmarks/results/sparrow-20261011T210336Z-74491a27.md). Provisional; all failures retained.

- 2026-10-11T21:03:39.796276+00:00 | SVGnest `svgnest-independent-edge-gap` seed 0, 5s, identical, axis y | valid | material 0.255 | [record](output/playwright/svgnest/20261011T210326Z-0fa094f2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:08:19.577945+00:00 | SVGnest `b-swim-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 5.464502452627639 | [record](output/playwright/svgnest/20261011T210713Z-84636261/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:08:57.908487+00:00 | deepnest-next `b-dagli-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.9535405833333332 | [record](output/playwright/deepnest/20261011T210736Z-bdf892bc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:09:27.381334+00:00 | SVGnest `b-swim-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 4.936348159724673 | [record](output/playwright/svgnest/20261011T210820Z-85761439/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:10:12.384369+00:00 | deepnest-next `b-fu-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.761904761904762 | [record](output/playwright/deepnest/20261011T210859Z-0ac221cd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:10:38.045680+00:00 | SVGnest `b-swim-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.852801850139082 | [record](output/playwright/svgnest/20261011T210928Z-bf8adf1b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:10:52.657095+00:00 | verified SVGnest batch `20261011T210713Z-30fd7360` | 3 selected B outcomes retained | [table](benchmarks/results/svgnest-20261011T211052Z-d34e7f41.md). Provisional; full M1 and all quality gates pending.

- 2026-10-11T21:11:27.262790+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.761904761904762 | [record](output/playwright/deepnest/20261011T211012Z-0e9bc8cf/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:12:02.907075+00:00 | SVGnest `b-albano-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 2.5636123928806858 | [record](output/playwright/svgnest/20261011T211054Z-adf7b65c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:12:32.465101+00:00 | verified deepnest batch `20261011T210736Z-bec51038` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T211232Z-57323d69.md). Provisional; all failures retained.

- 2026-10-11T21:12:58.706464+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T211241Z-8805712b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:13:10.413908+00:00 | SVGnest `b-albano-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 2.902177554823116 | [record](output/playwright/svgnest/20261011T211203Z-8ae3c616/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:13:44.287765+00:00 | deepnest-next `deepnest-remnant-defect-smoke` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T211333Z-a98b74d3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:14:17.217098+00:00 | SVGnest `b-albano-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.8229719163265306 | [record](output/playwright/svgnest/20261011T211310Z-38c16878/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:14:37.128978+00:00 | deepnest-next `deepnest-remnant-defect-smoke` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T211426Z-6ea9ea16/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:15:29.053248+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T211417Z-5fdbcbe9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:15:49.373023+00:00 | deepnest-next `deepnest-remnant-defect-smoke` seed 0, 5s, identical, axis y | valid | material 0.7290322580645161 | [record](output/playwright/deepnest/20261011T211536Z-1bccfaee/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:16:34.816976+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T211529Z-814846be/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:16:40.800701+00:00 | deepnest-next `deepnest-stock-hole-smoke` seed 0, 5s, identical, axis x | valid | material 1.0 | [record](output/playwright/deepnest/20261011T211627Z-2bb143d6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:16:45.252474+00:00 | M0 `published-20261011/jakobs1-2` | completed_integrity_checked | 1200s, 3 workers | length 11.0004635 | [record](output/m0/published-20261011/jakobs1-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:16:45.663090+00:00 | M0 `published-20261011/jakobs2-2` | completed_integrity_checked | 1200s, 3 workers | length 23.000366 | [record](output/m0/published-20261011/jakobs2-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:16:45.939286+00:00 | M0 `published-20261011/mao-2` | completed_integrity_checked | 1200s, 3 workers | length 1713.4031 | [record](output/m0/published-20261011/mao-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:17:32.719335+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-c072aeafec.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:33.148584+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-19cf9a13db.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:33.481122+00:00 | independent geometry check `published-20261011/albano-2` | valid | [report](output/m0/published-20261011/albano-2/validation-26571a65a7.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:33.742187+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-c6147a845f.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:34.120986+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-bb3cd102b3.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:34.478362+00:00 | independent geometry check `published-20261011/blaz1-2` | valid | [report](output/m0/published-20261011/blaz1-2/validation-23722a7c45.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:34.894352+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-c7f44a599d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:35.245251+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-e4047796ef.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:35.645301+00:00 | independent geometry check `published-20261011/dagli-2` | valid | [report](output/m0/published-20261011/dagli-2/validation-dd4e89db9d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:36.103584+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-320fefc9bb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:36.465539+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-93258e7286.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:36.737246+00:00 | independent geometry check `published-20261011/fu-2` | valid | [report](output/m0/published-20261011/fu-2/validation-fb93428a49.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:36.950302+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-952deab364.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:37.386464+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-41bf26416b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:37.707385+00:00 | independent geometry check `published-20261011/jakobs1-2` | valid | [report](output/m0/published-20261011/jakobs1-2/validation-89ebf74f38.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:37.846415+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-107a5924de.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:38.130968+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-ec24a224be.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:38.453267+00:00 | deepnest-next `svgnest-independent-edge-gap` seed 0, 5s, clearance-safe, axis y | valid | material 0.195 | [record](output/playwright/deepnest/20261011T211723Z-9411acbc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:17:38.525959+00:00 | independent geometry check `published-20261011/jakobs2-2` | valid | [report](output/m0/published-20261011/jakobs2-2/validation-e125fbdc7d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:38.738836+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-335483e1c5.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:39.016024+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-a532d54e3b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:39.359099+00:00 | independent geometry check `published-20261011/mao-2` | valid | [report](output/m0/published-20261011/mao-2/validation-11fdf386b7.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:39.652192+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-5933c69545.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:39.954275+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-a0c3e07453.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:40.294742+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-21e5405027.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:40.600058+00:00 | SVGnest `b-blaz1-strip-sheet` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T211635Z-863ca8fc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:17:40.749025+00:00 | independent geometry check `published-20261011/shapes0-1` | valid | [report](output/m0/published-20261011/shapes0-1/validation-428f3293d6.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:41.178612+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-6f10af1d47.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:41.652533+00:00 | independent geometry check `published-20261011/shapes1-1` | valid | [report](output/m0/published-20261011/shapes1-1/validation-83648d5aaa.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:42.076432+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-18a2888df6.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:42.472388+00:00 | independent geometry check `published-20261011/shirts-1` | valid | [report](output/m0/published-20261011/shirts-1/validation-674da17dd3.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:42.892521+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-c295e0fbda.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:43.252359+00:00 | independent geometry check `published-20261011/swim-1` | valid | [report](output/m0/published-20261011/swim-1/validation-7f592a8da8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:43.616058+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-77609adf0e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:17:44.025289+00:00 | independent geometry check `published-20261011/trousers-1` | valid | [report](output/m0/published-20261011/trousers-1/validation-6bbf5b44e8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:18:47.831086+00:00 | SVGnest `b-dagli-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.12333335 | [record](output/playwright/svgnest/20261011T211741Z-da955e67/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:18:53.087737+00:00 | M0 checkpoint: 33/39 completed and independently valid, 7/13 complete three-seed comparisons within 1%; [retained evidence](benchmarks/results/m0-first-thirty-three-20261011.json). M0 incomplete, 0% gated completion.

- 2026-10-11T21:18:53.087737+00:00 | Deepnest stock/path preparation: all six attempts retained, final remnant, enclosed-defect and safe-hole smokes independently valid; [evidence](benchmarks/results/deepnest-stock-inputs-20261011.json). No milestone or quality-gate claim.

- 2026-10-11T21:19:27.815586+00:00 | deepnest-next `b-fu-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.3843985263157894 | [record](output/playwright/deepnest/20261011T211809Z-55b530c1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:19:57.723330+00:00 | SVGnest `b-fu-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T211848Z-e12f2632/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:20:36.231318+00:00 | deepnest-next `b-jakobs1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.9047620000000003 | [record](output/playwright/deepnest/20261011T211928Z-032738d1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:21:03.703714+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T211958Z-c665908e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:21:46.804904+00:00 | deepnest-next `b-jakobs1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.9047620000000003 | [record](output/playwright/deepnest/20261011T212037Z-a5ce1af2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:22:11.022296+00:00 | SVGnest `b-fu-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.4678362894736843 | [record](output/playwright/svgnest/20261011T212104Z-9515dd23/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:22:26.157927+00:00 | verified deepnest batch `20261011T211807Z-ef4481cd` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T212226Z-30644c2c.md). Provisional; all failures retained.

- 2026-10-11T21:23:19.039308+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 4.5 | [record](output/playwright/svgnest/20261011T212211Z-2b6c3521/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:24:25.752721+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 4.5 | [record](output/playwright/svgnest/20261011T212319Z-ea17b51f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:25:30.630984+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.825 | [record](output/playwright/svgnest/20261011T212425Z-9ce013d3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:25:46.407858+00:00 | `20261011T212546Z-m-box-batch-500-identical-s0-c6c42911` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212546Z-m-box-batch-500-identical-s0-c6c42911/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:46.822490+00:00 | `20261011T212546Z-m-box-batch-500-upstream-default-s0-75c9b62b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212546Z-m-box-batch-500-upstream-default-s0-75c9b62b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:47.121468+00:00 | `20261011T212547Z-m-box-desktop-identical-s0-da0018d7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212547Z-m-box-desktop-identical-s0-da0018d7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:47.399101+00:00 | `20261011T212547Z-m-box-desktop-upstream-default-s0-fff778a8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212547Z-m-box-desktop-upstream-default-s0-fff778a8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:47.681078+00:00 | `20261011T212547Z-m-box-long-identical-s0-eb030183` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212547Z-m-box-long-identical-s0-eb030183/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:47.983413+00:00 | `20261011T212547Z-m-box-long-upstream-default-s0-e1c109cc` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212547Z-m-box-long-upstream-default-s0-e1c109cc/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:48.295454+00:00 | `20261011T212548Z-m-box-mini-identical-s0-19df9ebd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212548Z-m-box-mini-identical-s0-19df9ebd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:48.602735+00:00 | `20261011T212548Z-m-box-mini-upstream-default-s0-c1379360` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212548Z-m-box-mini-upstream-default-s0-c1379360/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:48.859346+00:00 | `20261011T212548Z-m-box-storage-identical-s0-a9fc78ec` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212548Z-m-box-storage-identical-s0-a9fc78ec/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:49.146294+00:00 | `20261011T212549Z-m-box-storage-upstream-default-s0-79ebe008` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212549Z-m-box-storage-upstream-default-s0-79ebe008/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:49.448422+00:00 | `20261011T212549Z-m-box-tool-identical-s0-66a0d860` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212549Z-m-box-tool-identical-s0-66a0d860/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:49.742647+00:00 | `20261011T212549Z-m-box-tool-upstream-default-s0-9dd92761` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212549Z-m-box-tool-upstream-default-s0-9dd92761/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:50.151242+00:00 | `20261011T212550Z-m-garment-bruce-1-identical-s0-b5b5bf1a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.9677442279999999 | [record](output/lbf/20261011T212550Z-m-garment-bruce-1-identical-s0-b5b5bf1a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:51.070112+00:00 | `20261011T212551Z-m-garment-bruce-1-upstream-default-s0-d810d305` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9677442279999999 | [record](output/lbf/20261011T212551Z-m-garment-bruce-1-upstream-default-s0-d810d305/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:51.713852+00:00 | `20261011T212551Z-m-garment-bruce-2-identical-s0-2e1a1ef1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.99998865 | [record](output/lbf/20261011T212551Z-m-garment-bruce-2-identical-s0-2e1a1ef1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:52.976281+00:00 | `20261011T212552Z-m-garment-bruce-2-upstream-default-s0-88c591eb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9998925002500001 | [record](output/lbf/20261011T212552Z-m-garment-bruce-2-upstream-default-s0-88c591eb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:53.864876+00:00 | `20261011T212553Z-m-garment-bruce-3-identical-s0-7f156b29` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | invalid; independent material none | [record](output/lbf/20261011T212553Z-m-garment-bruce-3-identical-s0-7f156b29/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:56.192761+00:00 | `20261011T212556Z-m-garment-bruce-3-upstream-default-s0-9a5212dc` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.57284825 | [record](output/lbf/20261011T212556Z-m-garment-bruce-3-upstream-default-s0-9a5212dc/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:57.946066+00:00 | `20261011T212557Z-m-garment-teagan-1-identical-s0-41ff58e8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.9922504243333333 | [record](output/lbf/20261011T212557Z-m-garment-teagan-1-identical-s0-41ff58e8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:25:58.929246+00:00 | `20261011T212558Z-m-garment-teagan-1-upstream-default-s0-7d0417e4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9998894246666667 | [record](output/lbf/20261011T212558Z-m-garment-teagan-1-upstream-default-s0-7d0417e4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:00.478654+00:00 | deepnest-next `m-box-batch-500` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T212436Z-2f960507/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:25:59.747026+00:00 | `20261011T212559Z-m-garment-teagan-2-identical-s0-c24c2fb9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.9998064302500003 | [record](output/lbf/20261011T212559Z-m-garment-teagan-2-identical-s0-c24c2fb9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:01.358410+00:00 | `20261011T212601Z-m-garment-teagan-2-upstream-default-s0-e1dba29a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.99992575525 | [record](output/lbf/20261011T212601Z-m-garment-teagan-2-upstream-default-s0-e1dba29a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:02.579210+00:00 | `20261011T212602Z-m-garment-teagan-3-identical-s0-4d568750` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.982509403000001 | [record](output/lbf/20261011T212602Z-m-garment-teagan-3-identical-s0-4d568750/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:06.233894+00:00 | `20261011T212606Z-m-garment-teagan-3-upstream-default-s0-8d12acd9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.982122569666667 | [record](output/lbf/20261011T212606Z-m-garment-teagan-3-upstream-default-s0-8d12acd9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:08.674323+00:00 | `20261011T212608Z-m-mechanical-batch-1000-identical-s0-1288a5fe` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212608Z-m-mechanical-batch-1000-identical-s0-1288a5fe/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:09.010804+00:00 | `20261011T212609Z-m-mechanical-batch-1000-upstream-default-s0-7a9e1300` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212609Z-m-mechanical-batch-1000-upstream-default-s0-7a9e1300/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:09.241461+00:00 | `20261011T212609Z-m-mechanical-cog-washers-identical-s0-45d4acbe` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212609Z-m-mechanical-cog-washers-identical-s0-45d4acbe/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:09.553593+00:00 | `20261011T212609Z-m-mechanical-cog-washers-upstream-default-s0-29996dc8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212609Z-m-mechanical-cog-washers-upstream-default-s0-29996dc8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:09.857888+00:00 | `20261011T212609Z-m-mechanical-defective-stock-identical-s0-2cb1886c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212609Z-m-mechanical-defective-stock-identical-s0-2cb1886c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:10.164548+00:00 | `20261011T212610Z-m-mechanical-defective-stock-upstream-default-s0-a537e41c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212610Z-m-mechanical-defective-stock-upstream-default-s0-a537e41c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:10.430995+00:00 | `20261011T212610Z-m-mechanical-frame-inserts-identical-s0-68c65127` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212610Z-m-mechanical-frame-inserts-identical-s0-68c65127/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:10.688438+00:00 | `20261011T212610Z-m-mechanical-frame-inserts-upstream-default-s0-2efe63c1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212610Z-m-mechanical-frame-inserts-upstream-default-s0-2efe63c1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:11.019371+00:00 | `20261011T212611Z-m-mechanical-large-plates-identical-s0-dbd777b4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212611Z-m-mechanical-large-plates-identical-s0-dbd777b4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:11.317530+00:00 | `20261011T212611Z-m-mechanical-large-plates-upstream-default-s0-1a117450` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212611Z-m-mechanical-large-plates-upstream-default-s0-1a117450/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:11.639126+00:00 | `20261011T212611Z-m-mechanical-mixed-stock-identical-s0-66a3d1d7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212611Z-m-mechanical-mixed-stock-identical-s0-66a3d1d7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:11.910781+00:00 | `20261011T212611Z-m-mechanical-mixed-stock-upstream-default-s0-6071cc2b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212611Z-m-mechanical-mixed-stock-upstream-default-s0-6071cc2b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:12.202247+00:00 | `20261011T212612Z-m-mechanical-mounting-kit-identical-s0-4d8b781f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212612Z-m-mechanical-mounting-kit-identical-s0-4d8b781f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:12.493559+00:00 | `20261011T212612Z-m-mechanical-mounting-kit-upstream-default-s0-f9ed39eb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212612Z-m-mechanical-mounting-kit-upstream-default-s0-f9ed39eb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:12.849126+00:00 | `20261011T212612Z-m-mechanical-panel-hardware-identical-s0-f68b949e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212612Z-m-mechanical-panel-hardware-identical-s0-f68b949e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:13.188217+00:00 | `20261011T212613Z-m-mechanical-panel-hardware-upstream-default-s0-94769079` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212613Z-m-mechanical-panel-hardware-upstream-default-s0-94769079/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:13.451557+00:00 | `20261011T212613Z-m-mechanical-remnant-kit-identical-s0-ee0f3e4c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212613Z-m-mechanical-remnant-kit-identical-s0-ee0f3e4c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:13.775801+00:00 | `20261011T212613Z-m-mechanical-remnant-kit-upstream-default-s0-e3a447f6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212613Z-m-mechanical-remnant-kit-upstream-default-s0-e3a447f6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:14.033972+00:00 | `20261011T212614Z-m-mechanical-small-brackets-identical-s0-41987d99` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212614Z-m-mechanical-small-brackets-identical-s0-41987d99/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:14.329870+00:00 | `20261011T212614Z-m-mechanical-small-brackets-upstream-default-s0-bd50efbf` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212614Z-m-mechanical-small-brackets-upstream-default-s0-bd50efbf/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:14.568738+00:00 | `20261011T212614Z-m-public-gear-1-identical-s0-45e0a568` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212614Z-m-public-gear-1-identical-s0-45e0a568/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:14.858774+00:00 | `20261011T212614Z-m-public-gear-1-upstream-default-s0-92c3c743` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212614Z-m-public-gear-1-upstream-default-s0-92c3c743/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:15.214803+00:00 | `20261011T212615Z-m-public-gear-2-identical-s0-bf528beb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212615Z-m-public-gear-2-identical-s0-bf528beb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:15.557760+00:00 | `20261011T212615Z-m-public-gear-2-upstream-default-s0-dff83bea` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212615Z-m-public-gear-2-upstream-default-s0-dff83bea/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:15.901735+00:00 | `20261011T212615Z-m-public-gear-3-identical-s0-ca92989f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212615Z-m-public-gear-3-identical-s0-ca92989f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:16.259575+00:00 | `20261011T212616Z-m-public-gear-3-upstream-default-s0-6cbbbc44` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212616Z-m-public-gear-3-upstream-default-s0-6cbbbc44/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:16.645967+00:00 | `20261011T212616Z-m-public-gear-4-identical-s0-5ccaa9b5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212616Z-m-public-gear-4-identical-s0-5ccaa9b5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:17.004796+00:00 | `20261011T212617Z-m-public-gear-4-upstream-default-s0-46637038` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212617Z-m-public-gear-4-upstream-default-s0-46637038/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:17.354047+00:00 | `20261011T212617Z-m-sign-1-identical-s0-fbf8a0b7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212617Z-m-sign-1-identical-s0-fbf8a0b7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:17.668134+00:00 | `20261011T212617Z-m-sign-1-upstream-default-s0-bb8a6af7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212617Z-m-sign-1-upstream-default-s0-bb8a6af7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:18.008826+00:00 | `20261011T212618Z-m-sign-2-identical-s0-a1bec928` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212618Z-m-sign-2-identical-s0-a1bec928/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:18.400185+00:00 | `20261011T212618Z-m-sign-2-upstream-default-s0-df5746d9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212618Z-m-sign-2-upstream-default-s0-df5746d9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:18.719752+00:00 | `20261011T212618Z-m-sign-3-identical-s0-c8a0cb41` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212618Z-m-sign-3-identical-s0-c8a0cb41/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:19.097592+00:00 | `20261011T212619Z-m-sign-3-upstream-default-s0-f168a3aa` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212619Z-m-sign-3-upstream-default-s0-f168a3aa/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:19.441044+00:00 | `20261011T212619Z-m-sign-4-identical-s0-21e72b30` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T212619Z-m-sign-4-identical-s0-21e72b30/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:19.782255+00:00 | `20261011T212619Z-m-sign-4-upstream-default-s0-d8f8c71b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T212619Z-m-sign-4-upstream-default-s0-d8f8c71b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:26:36.781941+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.908333333333333 | [record](output/playwright/svgnest/20261011T212530Z-8df6b667/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:26:46.753944+00:00 | current Sparrow `m-box-batch-500` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T212644Z-691b2170/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:26:48.293816+00:00 | current Sparrow `m-box-desktop` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T212646Z-b3429a2c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:26:49.885589+00:00 | current Sparrow `m-box-long` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T212648Z-df668565/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:26:51.450586+00:00 | current Sparrow `m-box-mini` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T212649Z-fed277ed/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:26:52.986321+00:00 | current Sparrow `m-box-storage` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T212651Z-ac548476/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:26:54.623964+00:00 | current Sparrow `m-box-tool` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T212653Z-680536aa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:27:09.543770+00:00 | deepnest-next `m-box-desktop` seed 0, 60s, identical, axis y | valid | material 0.887 | [record](output/playwright/deepnest/20261011T212600Z-7cee41fd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:27:16.201426+00:00 | verified provisional LBF batch `20261011T212546Z-6e9ec88a` | 11/60 valid, seed 0, M only | [table](benchmarks/results/lbf-20261011T212716Z-c9c2fc4b.md). Full M1 and quality gates remain pending.

- 2026-10-11T21:27:42.620635+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.908333333333333 | [record](output/playwright/svgnest/20261011T212636Z-83af08e8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:27:58.132407+00:00 | current Sparrow `m-garment-bruce-1` seed 0, 60s, identical, axis y | valid | score 0.19318351233333328 | [record](output/sparrow-benchmark/20261011T212654Z-7526d902/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:28:19.156605+00:00 | deepnest-next `m-box-long` seed 0, 60s, identical, axis y | valid | material 0.3257377049180328 | [record](output/playwright/deepnest/20261011T212709Z-e0e49002/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:28:49.413980+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.8857142857142857 | [record](output/playwright/svgnest/20261011T212742Z-d98af425/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:29:01.008528+00:00 | verified deepnest batch `20261011T212436Z-18393dac` | 2/3 valid | [table](benchmarks/results/deepnest-20261011T212901Z-75266a12.md). Provisional; all failures retained.

- 2026-10-11T21:29:01.430913+00:00 | current Sparrow `m-garment-bruce-2` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T212758Z-81446f57/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:29:56.340997+00:00 | SVGnest `b-mao-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 1.8961902388331813 | [record](output/playwright/svgnest/20261011T212849Z-95569498/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:30:05.791917+00:00 | current Sparrow `m-garment-bruce-3` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T212901Z-e9271790/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:30:13.594475+00:00 | deepnest-next `m-box-mini` seed 0, 60s, identical, axis y | valid | material 0.716000005 | [record](output/playwright/deepnest/20261011T212902Z-60a8b56c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:31:03.866623+00:00 | SVGnest `b-mao-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 2.815955970829535 | [record](output/playwright/svgnest/20261011T212956Z-fb2f546f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:31:09.089438+00:00 | current Sparrow `m-garment-teagan-1` seed 0, 60s, identical, axis y | valid | score 0.7828706096666668 | [record](output/sparrow-benchmark/20261011T213005Z-6f599799/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:31:27.213342+00:00 | deepnest-next `m-box-storage` seed 0, 60s, identical, axis y | valid | material 0.5388524590163934 | [record](output/playwright/deepnest/20261011T213013Z-92ffd48c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:32:15.239097+00:00 | current Sparrow `m-garment-teagan-2` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T213109Z-42ffd8be/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:32:16.590528+00:00 | SVGnest `b-mao-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.9006386964705881 | [record](output/playwright/svgnest/20261011T213104Z-d907e4c4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:32:54.513149+00:00 | deepnest-next `m-box-tool` seed 0, 60s, identical, axis y | valid | material 1.5310000025000001 | [record](output/playwright/deepnest/20261011T213129Z-38b60fdf/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:33:22.264264+00:00 | current Sparrow `m-garment-teagan-3` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T213215Z-310f4922/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:24.715369+00:00 | current Sparrow `m-mechanical-batch-1000` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213322Z-4ec5dd84/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:27.402409+00:00 | current Sparrow `m-mechanical-cog-washers` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213324Z-dcd73687/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:29.317488+00:00 | SVGnest `b-marques-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.1923076923076923 | [record](output/playwright/svgnest/20261011T213217Z-3ab7bd08/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:33:30.092159+00:00 | current Sparrow `m-mechanical-defective-stock` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213327Z-86d4b92e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:32.595494+00:00 | current Sparrow `m-mechanical-frame-inserts` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213330Z-996b4373/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:35.337600+00:00 | current Sparrow `m-mechanical-large-plates` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213332Z-2393f195/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:37.990800+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213335Z-bf0b8eaf/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:40.364889+00:00 | current Sparrow `m-mechanical-mounting-kit` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213338Z-644f17ee/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:42.672385+00:00 | current Sparrow `m-mechanical-panel-hardware` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213340Z-4369fbba/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:44.690552+00:00 | current Sparrow `m-mechanical-remnant-kit` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213342Z-71c70440/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:46.706851+00:00 | current Sparrow `m-mechanical-small-brackets` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213344Z-7f314a37/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:48.642976+00:00 | current Sparrow `m-public-gear-1` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213346Z-9d6f37ad/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:50.361693+00:00 | current Sparrow `m-public-gear-2` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213348Z-b4ccdbfb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:52.758121+00:00 | current Sparrow `m-public-gear-3` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213350Z-7efe0dd9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:55.282100+00:00 | current Sparrow `m-public-gear-4` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213352Z-8d669493/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:33:58.054754+00:00 | current Sparrow `m-sign-1` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213355Z-a710dc41/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:34:00.983075+00:00 | current Sparrow `m-sign-2` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213358Z-61b4ad9d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:34:03.285139+00:00 | current Sparrow `m-sign-3` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213401Z-b30477b3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:34:04.999283+00:00 | current Sparrow `m-sign-4` seed 0, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T213403Z-b427656f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:34:40.076756+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 8.476190476190476 | [record](output/playwright/svgnest/20261011T213330Z-a6c005dd/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:35:12.075365+00:00 | `20261011T213512Z-b-albano-nest-mb-free-identical-s0-435cfbcd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T213512Z-b-albano-nest-mb-free-identical-s0-435cfbcd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:35:12.972972+00:00 | `20261011T213512Z-b-albano-nest-mb-free-upstream-default-s0-230e0b6c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T213512Z-b-albano-nest-mb-free-upstream-default-s0-230e0b6c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:35:49.648355+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T213440Z-9d7faa76/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:35:56.480853+00:00 | `20261011T213556Z-b-albano-nest-mb-free-identical-s1-ad5bd878` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `0960889994ccba23100dcb3c2a6a8e5c7ae9f50f` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.4921253612392884 | [record](output/lbf/20261011T213556Z-b-albano-nest-mb-free-identical-s1-ad5bd878/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T21:35:58.958611+00:00 | verified sparrow batch `20261011T212644Z-c47d25b5` | 2/30 valid | [table](benchmarks/results/sparrow-20261011T213558Z-4b7cdd15.md). Provisional; all failures retained.

- 2026-10-11T21:35:59.507125+00:00 | verified deepnest batch `20261011T212902Z-dd9a5bcc` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T213559Z-b00cc0a8.md). Provisional; all failures retained.

- 2026-10-11T21:36:46.008471+00:00 | M0 `published-20261011/marques-2` | completed_integrity_checked | 1200s, 3 workers | length 76.28874 | [record](output/m0/published-20261011/marques-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:36:46.663199+00:00 | M0 `published-20261011/shapes0-2` | completed_integrity_checked | 1200s, 3 workers | length 58.919643 | [record](output/m0/published-20261011/shapes0-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:36:46.877393+00:00 | M0 `published-20261011/shapes1-2` | completed_integrity_checked | 1200s, 3 workers | length 52.84154 | [record](output/m0/published-20261011/shapes1-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:36:56.368623+00:00 | SVGnest `b-shapes0-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261011T213549Z-5f9e87a5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:38:01.954923+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-05808c1613.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:02.249112+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-379344ad42.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:02.450282+00:00 | independent geometry check `published-20261011/albano-2` | valid | [report](output/m0/published-20261011/albano-2/validation-0dada97835.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:02.607581+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-18b3122eb1.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:02.755833+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-b132fea316.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:02.860589+00:00 | independent geometry check `published-20261011/blaz1-2` | valid | [report](output/m0/published-20261011/blaz1-2/validation-6551dc48c3.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:02.936760+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-25dc493a23.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.008776+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-e793f6ee2b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.134971+00:00 | independent geometry check `published-20261011/dagli-2` | valid | [report](output/m0/published-20261011/dagli-2/validation-394a5f0a48.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.256428+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-7e058a9235.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.332681+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-d58c545998.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.462196+00:00 | independent geometry check `published-20261011/fu-2` | valid | [report](output/m0/published-20261011/fu-2/validation-be053eec2c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.534280+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-bd470d5d97.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.631286+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-ea26216672.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.729300+00:00 | independent geometry check `published-20261011/jakobs1-2` | valid | [report](output/m0/published-20261011/jakobs1-2/validation-ee377d8184.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.807954+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-96a0d5c3eb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.890956+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-6063c6102d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:03.962983+00:00 | independent geometry check `published-20261011/jakobs2-2` | valid | [report](output/m0/published-20261011/jakobs2-2/validation-9154a3cc2f.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.110489+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-0d8d17506c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.237299+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-f04f6246ca.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.304317+00:00 | independent geometry check `published-20261011/mao-2` | valid | [report](output/m0/published-20261011/mao-2/validation-2c376dde84.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.378928+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-d6f80d77fb.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.493722+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-9f686f8944.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.611749+00:00 | independent geometry check `published-20261011/marques-2` | valid | [report](output/m0/published-20261011/marques-2/validation-d009d63a48.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.747713+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-d9f95ff131.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:04.900539+00:00 | independent geometry check `published-20261011/shapes0-1` | valid | [report](output/m0/published-20261011/shapes0-1/validation-dcfaef2465.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.056129+00:00 | independent geometry check `published-20261011/shapes0-2` | valid | [report](output/m0/published-20261011/shapes0-2/validation-e045ed2e64.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.155039+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-bc05e5fa17.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.334889+00:00 | independent geometry check `published-20261011/shapes1-1` | valid | [report](output/m0/published-20261011/shapes1-1/validation-9a03b3e891.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.584506+00:00 | independent geometry check `published-20261011/shapes1-2` | valid | [report](output/m0/published-20261011/shapes1-2/validation-7e2df19a4c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.686870+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-5ef869c087.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.805525+00:00 | independent geometry check `published-20261011/shirts-1` | valid | [report](output/m0/published-20261011/shirts-1/validation-3d27862a2c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:05.996840+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-7cde024c2c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:06.098023+00:00 | independent geometry check `published-20261011/swim-1` | valid | [report](output/m0/published-20261011/swim-1/validation-1dc525fcf0.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:06.222917+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-712339d0d9.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:06.362351+00:00 | independent geometry check `published-20261011/trousers-1` | valid | [report](output/m0/published-20261011/trousers-1/validation-88f5291e90.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:38:07.747162+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T213657Z-806ae462/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:38:14.653866+00:00 | deepnest-next `m-garment-bruce-1` seed 0, 60s, identical, axis y | valid | material 0.2211004806666666 | [record](output/playwright/deepnest/20261011T213610Z-f366e0d7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:39:21.372338+00:00 | verified SVGnest batch `20261011T211054Z-7faeffdd` | 24 selected B outcomes retained | [table](benchmarks/results/svgnest-20261011T213921Z-83f5b1f3.md). Provisional; full M1 and all quality gates pending.

- 2026-10-11T21:39:27.136987+00:00 | deepnest-next `m-garment-bruce-2` seed 0, 60s, identical, axis y | valid | material 0.4776541012500001 | [record](output/playwright/deepnest/20261011T213814Z-f97e3bf2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:40:32.386631+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T213923Z-6e654fc0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:41:14.534159+00:00 | deepnest-next `m-garment-bruce-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T213927Z-b1833c28/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:41:47.406043+00:00 | SVGnest `b-shapes1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.7 | [record](output/playwright/svgnest/20261011T214033Z-498c01b6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:42:58.437983+00:00 | SVGnest `b-shirts-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.615384615384615 | [record](output/playwright/svgnest/20261011T214147Z-5ab8eb3b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:44:05.697917+00:00 | SVGnest `b-shirts-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 8.940170923076924 | [record](output/playwright/svgnest/20261011T214258Z-e9d55fde/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:45:13.359040+00:00 | SVGnest `b-shirts-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.7601461 | [record](output/playwright/svgnest/20261011T214405Z-cbdbb233/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:46:03.932422+00:00 | verified deepnest batch `20261011T213609Z-9f54749b` | 2/3 valid | [table](benchmarks/results/deepnest-20261011T214603Z-a4686331.md). Provisional; all failures retained.

- 2026-10-11T21:46:19.890036+00:00 | SVGnest `b-swim-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 5.464502452627639 | [record](output/playwright/svgnest/20261011T214513Z-7482177c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:47:30.461597+00:00 | SVGnest `b-swim-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 4.936348159724673 | [record](output/playwright/svgnest/20261011T214620Z-0382e59d/run.json). Provisional settings, one worker and one CPU affinity.
