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
