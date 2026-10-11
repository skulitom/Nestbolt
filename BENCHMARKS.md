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
