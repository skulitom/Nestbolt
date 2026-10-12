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

- 2026-10-11T21:47:58.298359+00:00 | deepnest-next `m-garment-teagan-1` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T214605Z-b877a861/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:48:07.993431+00:00 | current Sparrow `b-albano-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T214705Z-04c26ac4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:48:39.092031+00:00 | SVGnest `b-swim-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.852801850139082 | [record](output/playwright/svgnest/20261011T214730Z-931665c2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:49:10.026533+00:00 | current Sparrow `b-albano-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T214808Z-9f6d49f2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:49:31.947625+00:00 | deepnest-next `m-garment-teagan-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T214758Z-87ae6f9e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:49:46.225166+00:00 | SVGnest `b-trousers-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 2.7105826553672316 | [record](output/playwright/svgnest/20261011T214839Z-714aaed0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:50:12.368950+00:00 | current Sparrow `b-albano-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T214910Z-7a73a3cf/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:50:44.092746+00:00 | verified sparrow batch `20261011T214704Z-ea8d0e92` | 0/3 valid | [table](benchmarks/results/sparrow-20261011T215044Z-de7f97d5.md). Provisional; all failures retained.

- 2026-10-11T21:50:52.231886+00:00 | SVGnest `b-trousers-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.4180790960451977 | [record](output/playwright/svgnest/20261011T214946Z-f428555e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:51:10.597058+00:00 | deepnest-next `m-garment-teagan-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T214932Z-44f29e7f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:51:36.496816+00:00 | verified deepnest batch `20261011T214605Z-ce5142ef` | 0/3 valid | [table](benchmarks/results/deepnest-20261011T215136Z-64a5bd6a.md). Provisional; all failures retained.

- 2026-10-11T21:51:59.315111+00:00 | SVGnest `b-trousers-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.329113924050633 | [record](output/playwright/svgnest/20261011T215052Z-9c99e16b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:52:24.367399+00:00 | verified svgnest batch `20261011T213923Z-f9aacfb5` | 11/11 valid | [table](benchmarks/results/svgnest-20261011T215224Z-9e1ba193.md). Provisional; all failures retained.

- 2026-10-11T21:52:37.584025+00:00 | SVGnest `m-box-mini` seed 0, 5s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215224Z-7da36da6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:54:37.814845+00:00 | SVGnest `m-box-batch-500` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215310Z-1bca4608/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:54:59.009626+00:00 | deepnest-next `m-mechanical-batch-1000` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T215324Z-baf4ba59/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:54:59.396104+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T215353Z-34da2c2e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:55:47.271643+00:00 | SVGnest `m-box-desktop` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215438Z-a7be7fa9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:56:02.085839+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T215459Z-862b8c80/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:56:10.201612+00:00 | deepnest-next `m-mechanical-cog-washers` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T215459Z-4015c4b2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:56:55.224400+00:00 | SVGnest `m-box-long` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215547Z-1775906f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:57:04.616738+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T215602Z-f4050329/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:57:28.248953+00:00 | deepnest-next `m-mechanical-defective-stock` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T215610Z-30e8e95a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T21:57:51.640439+00:00 | M0 `published-20261011/shirts-2` | completed_integrity_checked | 1200s, 3 workers | length 60.243362 | [record](output/m0/published-20261011/shirts-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:57:51.651453+00:00 | M0 `published-20261011/swim-2` | completed_integrity_checked | 1200s, 3 workers | length 5688.784 | [record](output/m0/published-20261011/swim-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:57:51.843337+00:00 | M0 `published-20261011/trousers-2` | completed_integrity_checked | 1200s, 3 workers | length 238.72917 | [record](output/m0/published-20261011/trousers-2/run.json). Geometry validation pending M1.

- 2026-10-11T21:57:52.934679+00:00 | verified deepnest batch `20261011T215321Z-ea19d3cb` | 0/3 valid | [table](benchmarks/results/deepnest-20261011T215752Z-30b81baa.md). Provisional; all failures retained.

- 2026-10-11T21:58:02.917873+00:00 | SVGnest `m-box-mini` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215655Z-1ccc5985/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:58:03.765432+00:00 | independent geometry check `published-20261011/albano-0` | valid | [report](output/m0/published-20261011/albano-0/validation-c4ee024d56.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:03.832635+00:00 | independent geometry check `published-20261011/albano-1` | valid | [report](output/m0/published-20261011/albano-1/validation-5edbc47d97.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:03.893922+00:00 | independent geometry check `published-20261011/albano-2` | valid | [report](output/m0/published-20261011/albano-2/validation-bedcc9ee4a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:03.957539+00:00 | independent geometry check `published-20261011/blaz1-0` | valid | [report](output/m0/published-20261011/blaz1-0/validation-0a4e9a4c59.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.021675+00:00 | independent geometry check `published-20261011/blaz1-1` | valid | [report](output/m0/published-20261011/blaz1-1/validation-d332867310.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.095119+00:00 | independent geometry check `published-20261011/blaz1-2` | valid | [report](output/m0/published-20261011/blaz1-2/validation-2173c4b009.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.167302+00:00 | independent geometry check `published-20261011/dagli-0` | valid | [report](output/m0/published-20261011/dagli-0/validation-1cdebe4928.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.254701+00:00 | independent geometry check `published-20261011/dagli-1` | valid | [report](output/m0/published-20261011/dagli-1/validation-6d8891139a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.347850+00:00 | independent geometry check `published-20261011/dagli-2` | valid | [report](output/m0/published-20261011/dagli-2/validation-5864cffcdf.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.436701+00:00 | independent geometry check `published-20261011/fu-0` | valid | [report](output/m0/published-20261011/fu-0/validation-7b9ff0ff88.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.500939+00:00 | independent geometry check `published-20261011/fu-1` | valid | [report](output/m0/published-20261011/fu-1/validation-f92b0df4ef.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.556452+00:00 | independent geometry check `published-20261011/fu-2` | valid | [report](output/m0/published-20261011/fu-2/validation-0d36088606.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.626351+00:00 | independent geometry check `published-20261011/jakobs1-0` | valid | [report](output/m0/published-20261011/jakobs1-0/validation-5afa9ed672.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.681010+00:00 | independent geometry check `published-20261011/jakobs1-1` | valid | [report](output/m0/published-20261011/jakobs1-1/validation-6143c177e5.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.781599+00:00 | independent geometry check `published-20261011/jakobs1-2` | valid | [report](output/m0/published-20261011/jakobs1-2/validation-cebe957ea5.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:04.967869+00:00 | independent geometry check `published-20261011/jakobs2-0` | valid | [report](output/m0/published-20261011/jakobs2-0/validation-aa347251d9.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.024189+00:00 | independent geometry check `published-20261011/jakobs2-1` | valid | [report](output/m0/published-20261011/jakobs2-1/validation-56a922369e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.083636+00:00 | independent geometry check `published-20261011/jakobs2-2` | valid | [report](output/m0/published-20261011/jakobs2-2/validation-aeaeb186d8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.155585+00:00 | independent geometry check `published-20261011/mao-0` | valid | [report](output/m0/published-20261011/mao-0/validation-e1dcd80992.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.218780+00:00 | independent geometry check `published-20261011/mao-1` | valid | [report](output/m0/published-20261011/mao-1/validation-474bfa948b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.277369+00:00 | independent geometry check `published-20261011/mao-2` | valid | [report](output/m0/published-20261011/mao-2/validation-05b2c56c9d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.498289+00:00 | independent geometry check `published-20261011/marques-0` | valid | [report](output/m0/published-20261011/marques-0/validation-087118611c.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:05.745710+00:00 | independent geometry check `published-20261011/marques-1` | valid | [report](output/m0/published-20261011/marques-1/validation-0715201e7b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.045590+00:00 | independent geometry check `published-20261011/marques-2` | valid | [report](output/m0/published-20261011/marques-2/validation-112f0f6870.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.160065+00:00 | independent geometry check `published-20261011/shapes0-0` | valid | [report](output/m0/published-20261011/shapes0-0/validation-b6bbcd875a.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.366984+00:00 | independent geometry check `published-20261011/shapes0-1` | valid | [report](output/m0/published-20261011/shapes0-1/validation-dc5cf5514e.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.512542+00:00 | independent geometry check `published-20261011/shapes0-2` | valid | [report](output/m0/published-20261011/shapes0-2/validation-7c06f96c1b.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.673519+00:00 | independent geometry check `published-20261011/shapes1-0` | valid | [report](output/m0/published-20261011/shapes1-0/validation-6267940e7d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.749991+00:00 | independent geometry check `published-20261011/shapes1-1` | valid | [report](output/m0/published-20261011/shapes1-1/validation-dcb42de37d.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:06.862065+00:00 | independent geometry check `published-20261011/shapes1-2` | valid | [report](output/m0/published-20261011/shapes1-2/validation-166ec2fada.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.159135+00:00 | independent geometry check `published-20261011/shirts-0` | valid | [report](output/m0/published-20261011/shirts-0/validation-c247857f70.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.163649+00:00 | current Sparrow `b-dagli-strip-sheet` seed 0, 60s, identical, axis y | valid | score 0.88532895 | [record](output/sparrow-benchmark/20261011T215704Z-4eccec5b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:58:07.226679+00:00 | independent geometry check `published-20261011/shirts-1` | valid | [report](output/m0/published-20261011/shirts-1/validation-1642332687.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.296404+00:00 | independent geometry check `published-20261011/shirts-2` | valid | [report](output/m0/published-20261011/shirts-2/validation-1af51b5b52.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.517978+00:00 | independent geometry check `published-20261011/swim-0` | valid | [report](output/m0/published-20261011/swim-0/validation-118889d5d5.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.599534+00:00 | independent geometry check `published-20261011/swim-1` | valid | [report](output/m0/published-20261011/swim-1/validation-62f64d5fca.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.664976+00:00 | independent geometry check `published-20261011/swim-2` | valid | [report](output/m0/published-20261011/swim-2/validation-6ce6642825.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.732531+00:00 | independent geometry check `published-20261011/trousers-0` | valid | [report](output/m0/published-20261011/trousers-0/validation-ddaf67e0dc.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.792664+00:00 | independent geometry check `published-20261011/trousers-1` | valid | [report](output/m0/published-20261011/trousers-1/validation-0375985764.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:07.854678+00:00 | independent geometry check `published-20261011/trousers-2` | valid | [report](output/m0/published-20261011/trousers-2/validation-d7cb248aa8.json). Original polygons; Clipper2 path; this does not establish full M1/G1.

- 2026-10-11T21:58:20.660555+00:00 | M0 published reproduction PASS: 39/39 independently valid runs, 13/13 complete means within 1%; [table](benchmarks/results/m0-published-20261011T215820Z-10a30c6f.md). Historical native quality reproduction only; M1-M5 and G1-G8 remain pending.

- 2026-10-11T21:59:08.669282+00:00 | SVGnest `m-box-storage` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215803Z-b7b2509e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T21:59:09.280824+00:00 | current Sparrow `b-fu-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T215807Z-dfcca8bf/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T21:59:09.461256+00:00 | deepnest-next `m-mechanical-frame-inserts` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T215757Z-9837d8eb/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:00:11.380663+00:00 | current Sparrow `b-fu-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T215909Z-31db2eb7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:00:14.229328+00:00 | SVGnest `m-box-tool` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T215908Z-fe5b73ee/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:00:18.669990+00:00 | SVGnest `m-garment-bruce-1` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220014Z-e65ccea2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:00:19.075590+00:00 | deepnest-next `m-mechanical-large-plates` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T215909Z-d01509a9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:00:22.978451+00:00 | SVGnest `m-garment-bruce-2` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220018Z-4af37bf9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:00:27.705800+00:00 | SVGnest `m-garment-bruce-3` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220023Z-7be1914f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:00:30.339616+00:00 | `20261011T220030Z-b-albano-nest-mb-free-identical-s0-b35a213d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T220030Z-b-albano-nest-mb-free-identical-s0-b35a213d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:30.945405+00:00 | `20261011T220030Z-b-albano-nest-mb-free-upstream-default-s0-9272d959` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T220030Z-b-albano-nest-mb-free-upstream-default-s0-9272d959/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:31.724514+00:00 | `20261011T220031Z-b-albano-nest-mb-free-identical-s1-4950276f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.4921253612392884 | [record](output/lbf/20261011T220031Z-b-albano-nest-mb-free-identical-s1-4950276f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:32.168832+00:00 | SVGnest `m-garment-teagan-1` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220028Z-4c1d3689/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:00:32.324076+00:00 | `20261011T220032Z-b-albano-nest-mb-free-upstream-default-s1-0152137c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.4921253612392884 | [record](output/lbf/20261011T220032Z-b-albano-nest-mb-free-upstream-default-s1-0152137c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:33.613658+00:00 | `20261011T220033Z-b-albano-nest-mb-free-identical-s2-266682cb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.9425693849703363 | [record](output/lbf/20261011T220033Z-b-albano-nest-mb-free-identical-s2-266682cb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:34.435366+00:00 | `20261011T220034Z-b-albano-nest-mb-free-upstream-default-s2-0e987cc2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9425693849703363 | [record](output/lbf/20261011T220034Z-b-albano-nest-mb-free-upstream-default-s2-0e987cc2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:34.982376+00:00 | `20261011T220034Z-b-albano-nest-mb-free-identical-s0-363b0d64` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T220034Z-b-albano-nest-mb-free-identical-s0-363b0d64/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:35.811811+00:00 | `20261011T220035Z-b-albano-nest-mb-free-upstream-default-s0-27bff585` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 3.515800699186992 | [record](output/lbf/20261011T220035Z-b-albano-nest-mb-free-upstream-default-s0-27bff585/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:36.749873+00:00 | `20261011T220036Z-b-albano-nest-mb-free-identical-s1-8567989b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 3.4921253612392884 | [record](output/lbf/20261011T220036Z-b-albano-nest-mb-free-identical-s1-8567989b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:37.289525+00:00 | `20261011T220037Z-b-albano-nest-mb-free-upstream-default-s1-a06a32e9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 3.4921253612392884 | [record](output/lbf/20261011T220037Z-b-albano-nest-mb-free-upstream-default-s1-a06a32e9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:37.877471+00:00 | SVGnest `m-garment-teagan-2` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220032Z-17c47583/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:00:37.873957+00:00 | `20261011T220037Z-b-albano-nest-mb-free-identical-s2-4f796eff` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 2.9425693849703363 | [record](output/lbf/20261011T220037Z-b-albano-nest-mb-free-identical-s2-4f796eff/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:39.083262+00:00 | `20261011T220039Z-b-albano-nest-mb-free-upstream-default-s2-364c7ce8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 2.9425693849703363 | [record](output/lbf/20261011T220039Z-b-albano-nest-mb-free-upstream-default-s2-364c7ce8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:40.206250+00:00 | `20261011T220040Z-b-albano-nest-mb-given-identical-s0-af2a855b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9426522302790596 | [record](output/lbf/20261011T220040Z-b-albano-nest-mb-given-identical-s0-af2a855b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:40.929100+00:00 | `20261011T220040Z-b-albano-nest-mb-given-upstream-default-s0-370386bb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9426522302790596 | [record](output/lbf/20261011T220040Z-b-albano-nest-mb-given-upstream-default-s0-370386bb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:41.746020+00:00 | `20261011T220041Z-b-albano-nest-mb-given-identical-s1-23333a41` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.9505346077785104 | [record](output/lbf/20261011T220041Z-b-albano-nest-mb-given-identical-s1-23333a41/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:00:46.370546+00:00 | SVGnest `m-garment-teagan-3` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220038Z-dde163c2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:01:13.576826+00:00 | current Sparrow `b-fu-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220011Z-61ecb319/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:01:35.384949+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T220019Z-13f9c8e8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:02:10.384724+00:00 | `20261011T220210Z-b-albano-nest-mb-given-upstream-default-s1-8591016a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9505346077785104 | [record](output/lbf/20261011T220210Z-b-albano-nest-mb-given-upstream-default-s1-8591016a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:11.170702+00:00 | `20261011T220211Z-b-albano-nest-mb-given-identical-s2-fe9f6657` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 3.370282710613052 | [record](output/lbf/20261011T220211Z-b-albano-nest-mb-given-identical-s2-fe9f6657/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:11.942884+00:00 | `20261011T220211Z-b-albano-nest-mb-given-upstream-default-s2-b7fecec8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.370282710613052 | [record](output/lbf/20261011T220211Z-b-albano-nest-mb-given-upstream-default-s2-b7fecec8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:12.415101+00:00 | `20261011T220212Z-b-albano-strip-sheet-identical-s0-ecfb4389` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.9971891020408163 | [record](output/lbf/20261011T220212Z-b-albano-strip-sheet-identical-s0-ecfb4389/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:12.837781+00:00 | `20261011T220212Z-b-albano-strip-sheet-upstream-default-s0-995587f0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9971891020408163 | [record](output/lbf/20261011T220212Z-b-albano-strip-sheet-upstream-default-s0-995587f0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:13.238058+00:00 | `20261011T220213Z-b-albano-strip-sheet-identical-s1-fb137773` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.9999417142857145 | [record](output/lbf/20261011T220213Z-b-albano-strip-sheet-identical-s1-fb137773/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:13.644060+00:00 | `20261011T220213Z-b-albano-strip-sheet-upstream-default-s1-bdab1a9d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9999417142857145 | [record](output/lbf/20261011T220213Z-b-albano-strip-sheet-upstream-default-s1-bdab1a9d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:14.214623+00:00 | `20261011T220214Z-b-albano-strip-sheet-identical-s2-68363da5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.339294530816326 | [record](output/lbf/20261011T220214Z-b-albano-strip-sheet-identical-s2-68363da5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:14.656473+00:00 | `20261011T220214Z-b-albano-strip-sheet-upstream-default-s2-8a078d10` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.339294530816326 | [record](output/lbf/20261011T220214Z-b-albano-strip-sheet-upstream-default-s2-8a078d10/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:15.042622+00:00 | `20261011T220215Z-b-blaz1-nest-mb-free-identical-s0-26905f0f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 13.5671944 | [record](output/lbf/20261011T220215Z-b-blaz1-nest-mb-free-identical-s0-26905f0f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:15.593084+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220113Z-3d0a2f3c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:02:15.458606+00:00 | `20261011T220215Z-b-blaz1-nest-mb-free-upstream-default-s0-4fdea2e1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 13.5671944 | [record](output/lbf/20261011T220215Z-b-blaz1-nest-mb-free-upstream-default-s0-4fdea2e1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:16.416135+00:00 | `20261011T220216Z-b-blaz1-nest-mb-free-identical-s1-e26bd751` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 12.6719132 | [record](output/lbf/20261011T220216Z-b-blaz1-nest-mb-free-identical-s1-e26bd751/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:16.844466+00:00 | `20261011T220216Z-b-blaz1-nest-mb-free-upstream-default-s1-a03df89a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 12.6719132 | [record](output/lbf/20261011T220216Z-b-blaz1-nest-mb-free-upstream-default-s1-a03df89a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:17.484433+00:00 | `20261011T220217Z-b-blaz1-nest-mb-free-identical-s2-d5e52be1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 14.561120266666666 | [record](output/lbf/20261011T220217Z-b-blaz1-nest-mb-free-identical-s2-d5e52be1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:18.032471+00:00 | `20261011T220218Z-b-blaz1-nest-mb-free-upstream-default-s2-3e52d123` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 14.561120266666666 | [record](output/lbf/20261011T220218Z-b-blaz1-nest-mb-free-upstream-default-s2-3e52d123/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:02:19.293759+00:00 | verified deepnest batch `20261011T215757Z-14547022` | 0/3 valid | [table](benchmarks/results/deepnest-20261011T220219Z-3edeb335.md). Provisional; all failures retained.

- 2026-10-11T22:03:17.821295+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220215Z-316b5cca/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:03:26.056654+00:00 | `20261011T220326Z-b-blaz1-nest-mb-given-identical-s0-c2dbb072` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 11.666872133333333 | [record](output/lbf/20261011T220326Z-b-blaz1-nest-mb-given-identical-s0-c2dbb072/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:26.722388+00:00 | `20261011T220326Z-b-blaz1-nest-mb-given-upstream-default-s0-53ed486b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 11.666872133333333 | [record](output/lbf/20261011T220326Z-b-blaz1-nest-mb-given-upstream-default-s0-53ed486b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:27.123893+00:00 | `20261011T220327Z-b-blaz1-nest-mb-given-identical-s1-6c70c87b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 12.666849733333333 | [record](output/lbf/20261011T220327Z-b-blaz1-nest-mb-given-identical-s1-6c70c87b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:27.547899+00:00 | `20261011T220327Z-b-blaz1-nest-mb-given-upstream-default-s1-c03e0335` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 12.666849733333333 | [record](output/lbf/20261011T220327Z-b-blaz1-nest-mb-given-upstream-default-s1-c03e0335/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:28.108592+00:00 | `20261011T220328Z-b-blaz1-nest-mb-given-identical-s2-7f37b377` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 12.666703466666666 | [record](output/lbf/20261011T220328Z-b-blaz1-nest-mb-given-identical-s2-7f37b377/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:28.638046+00:00 | `20261011T220328Z-b-blaz1-nest-mb-given-upstream-default-s2-ca4261cf` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 12.666703466666666 | [record](output/lbf/20261011T220328Z-b-blaz1-nest-mb-given-upstream-default-s2-ca4261cf/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:29.197798+00:00 | deepnest-next `m-mechanical-mounting-kit` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T220219Z-592d2991/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:03:29.175504+00:00 | `20261011T220329Z-b-blaz1-strip-sheet-identical-s0-b17c9e40` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.8002277333333336 | [record](output/lbf/20261011T220329Z-b-blaz1-strip-sheet-identical-s0-b17c9e40/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:30.133618+00:00 | `20261011T220330Z-b-blaz1-strip-sheet-upstream-default-s0-d51bfbbc` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.8002277333333336 | [record](output/lbf/20261011T220330Z-b-blaz1-strip-sheet-upstream-default-s0-d51bfbbc/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:30.650858+00:00 | `20261011T220330Z-b-blaz1-strip-sheet-identical-s1-a3d8e7af` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.800627733333333 | [record](output/lbf/20261011T220330Z-b-blaz1-strip-sheet-identical-s1-a3d8e7af/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:31.344430+00:00 | `20261011T220331Z-b-blaz1-strip-sheet-upstream-default-s1-fac6ffc3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.800627733333333 | [record](output/lbf/20261011T220331Z-b-blaz1-strip-sheet-upstream-default-s1-fac6ffc3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:32.273650+00:00 | `20261011T220332Z-b-blaz1-strip-sheet-identical-s2-345003a3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 3.867084933333333 | [record](output/lbf/20261011T220332Z-b-blaz1-strip-sheet-identical-s2-345003a3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:32.867691+00:00 | `20261011T220332Z-b-blaz1-strip-sheet-upstream-default-s2-e0e7a1a0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.867084933333333 | [record](output/lbf/20261011T220332Z-b-blaz1-strip-sheet-upstream-default-s2-e0e7a1a0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:33.672113+00:00 | `20261011T220333Z-b-dagli-strip-sheet-identical-s0-e61a0896` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.1669585333333332 | [record](output/lbf/20261011T220333Z-b-dagli-strip-sheet-identical-s0-e61a0896/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:34.387106+00:00 | `20261011T220334Z-b-dagli-strip-sheet-upstream-default-s0-3edd2706` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.1669585333333332 | [record](output/lbf/20261011T220334Z-b-dagli-strip-sheet-upstream-default-s0-3edd2706/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:34.880194+00:00 | `20261011T220334Z-b-dagli-strip-sheet-identical-s1-ec1d87f4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.56773255 | [record](output/lbf/20261011T220334Z-b-dagli-strip-sheet-identical-s1-ec1d87f4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:35.538999+00:00 | `20261011T220335Z-b-dagli-strip-sheet-upstream-default-s1-f4eeeef7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.56773255 | [record](output/lbf/20261011T220335Z-b-dagli-strip-sheet-upstream-default-s1-f4eeeef7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:36.224146+00:00 | `20261011T220336Z-b-dagli-strip-sheet-identical-s2-af23da5c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 1.0834041333333333 | [record](output/lbf/20261011T220336Z-b-dagli-strip-sheet-identical-s2-af23da5c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:36.781789+00:00 | `20261011T220336Z-b-dagli-strip-sheet-upstream-default-s2-1f4ef19c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.0834041333333333 | [record](output/lbf/20261011T220336Z-b-dagli-strip-sheet-upstream-default-s2-1f4ef19c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:37.304298+00:00 | `20261011T220337Z-b-fu-nest-mb-free-identical-s0-2ab8666e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.671739952380952 | [record](output/lbf/20261011T220337Z-b-fu-nest-mb-free-identical-s0-2ab8666e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:37.781101+00:00 | `20261011T220337Z-b-fu-nest-mb-free-upstream-default-s0-ec3fb898` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.671739952380952 | [record](output/lbf/20261011T220337Z-b-fu-nest-mb-free-upstream-default-s0-ec3fb898/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:38.224392+00:00 | `20261011T220338Z-b-fu-nest-mb-free-identical-s1-5ef894d9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 4.607684714285714 | [record](output/lbf/20261011T220338Z-b-fu-nest-mb-free-identical-s1-5ef894d9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:38.992046+00:00 | `20261011T220338Z-b-fu-nest-mb-free-upstream-default-s1-46b1b480` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.607684714285714 | [record](output/lbf/20261011T220338Z-b-fu-nest-mb-free-upstream-default-s1-46b1b480/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:39.560887+00:00 | `20261011T220339Z-b-fu-nest-mb-free-identical-s2-46174262` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 4.7995362380952376 | [record](output/lbf/20261011T220339Z-b-fu-nest-mb-free-identical-s2-46174262/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:41.835749+00:00 | `20261011T220341Z-b-fu-nest-mb-free-upstream-default-s2-dcd5de1d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.7995362380952376 | [record](output/lbf/20261011T220341Z-b-fu-nest-mb-free-upstream-default-s2-dcd5de1d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:42.351372+00:00 | `20261011T220342Z-b-fu-nest-mb-given-identical-s0-cc8a5fe6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.476310142857143 | [record](output/lbf/20261011T220342Z-b-fu-nest-mb-given-identical-s0-cc8a5fe6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:42.845351+00:00 | `20261011T220342Z-b-fu-nest-mb-given-upstream-default-s0-2ba03279` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.476310142857143 | [record](output/lbf/20261011T220342Z-b-fu-nest-mb-given-upstream-default-s0-2ba03279/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:43.508767+00:00 | `20261011T220343Z-b-fu-nest-mb-given-identical-s1-71ccedbf` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.952437095238095 | [record](output/lbf/20261011T220343Z-b-fu-nest-mb-given-identical-s1-71ccedbf/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:44.149967+00:00 | `20261011T220344Z-b-fu-nest-mb-given-upstream-default-s1-22e5adc1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.952437095238095 | [record](output/lbf/20261011T220344Z-b-fu-nest-mb-given-upstream-default-s1-22e5adc1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:44.620775+00:00 | `20261011T220344Z-b-fu-nest-mb-given-identical-s2-e8bdd196` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 3.9526284285714284 | [record](output/lbf/20261011T220344Z-b-fu-nest-mb-given-identical-s2-e8bdd196/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:45.221792+00:00 | `20261011T220345Z-b-fu-nest-mb-given-upstream-default-s2-8fffbad1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.9526284285714284 | [record](output/lbf/20261011T220345Z-b-fu-nest-mb-given-upstream-default-s2-8fffbad1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:45.798363+00:00 | `20261011T220345Z-b-fu-strip-sheet-identical-s0-d8a5fcfe` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.895080263157895 | [record](output/lbf/20261011T220345Z-b-fu-strip-sheet-identical-s0-d8a5fcfe/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:46.268757+00:00 | `20261011T220346Z-b-fu-strip-sheet-upstream-default-s0-7c577ff8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.895080263157895 | [record](output/lbf/20261011T220346Z-b-fu-strip-sheet-upstream-default-s0-7c577ff8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:46.744981+00:00 | `20261011T220346Z-b-fu-strip-sheet-identical-s1-a14005d8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.951093 | [record](output/lbf/20261011T220346Z-b-fu-strip-sheet-identical-s1-a14005d8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:47.248931+00:00 | `20261011T220347Z-b-fu-strip-sheet-upstream-default-s1-f777325c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.951093 | [record](output/lbf/20261011T220347Z-b-fu-strip-sheet-upstream-default-s1-f777325c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:47.995935+00:00 | `20261011T220347Z-b-fu-strip-sheet-identical-s2-e1cf7b21` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 1.9099341052631578 | [record](output/lbf/20261011T220347Z-b-fu-strip-sheet-identical-s2-e1cf7b21/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:48.598346+00:00 | `20261011T220348Z-b-fu-strip-sheet-upstream-default-s2-e3763cba` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9099341052631578 | [record](output/lbf/20261011T220348Z-b-fu-strip-sheet-upstream-default-s2-e3763cba/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:49.431440+00:00 | `20261011T220349Z-b-fu-strip-sheet-identical-s0-d2a71d42` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 1.895080263157895 | [record](output/lbf/20261011T220349Z-b-fu-strip-sheet-identical-s0-d2a71d42/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:49.869554+00:00 | `20261011T220349Z-b-fu-strip-sheet-upstream-default-s0-88c63ced` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 1.895080263157895 | [record](output/lbf/20261011T220349Z-b-fu-strip-sheet-upstream-default-s0-88c63ced/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:50.420054+00:00 | `20261011T220350Z-b-fu-strip-sheet-identical-s1-cfd6532d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 1.951093 | [record](output/lbf/20261011T220350Z-b-fu-strip-sheet-identical-s1-cfd6532d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:50.977498+00:00 | `20261011T220350Z-b-fu-strip-sheet-upstream-default-s1-2899a969` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 1.951093 | [record](output/lbf/20261011T220350Z-b-fu-strip-sheet-upstream-default-s1-2899a969/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:51.481975+00:00 | `20261011T220351Z-b-fu-strip-sheet-identical-s2-e987ff89` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 1.9099341052631578 | [record](output/lbf/20261011T220351Z-b-fu-strip-sheet-identical-s2-e987ff89/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:52.057856+00:00 | `20261011T220352Z-b-fu-strip-sheet-upstream-default-s2-3d5099d9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 1.9099341052631578 | [record](output/lbf/20261011T220352Z-b-fu-strip-sheet-upstream-default-s2-3d5099d9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:52.765356+00:00 | `20261011T220352Z-b-jakobs1-nest-mb-free-identical-s0-9cdaad08` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.928895416666666 | [record](output/lbf/20261011T220352Z-b-jakobs1-nest-mb-free-identical-s0-9cdaad08/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:55.496106+00:00 | `20261011T220355Z-b-jakobs1-nest-mb-free-upstream-default-s0-15fa6e54` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.928895416666666 | [record](output/lbf/20261011T220355Z-b-jakobs1-nest-mb-free-upstream-default-s0-15fa6e54/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:55.988706+00:00 | `20261011T220355Z-b-jakobs1-nest-mb-free-identical-s1-deafacd8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 4.591465333333334 | [record](output/lbf/20261011T220355Z-b-jakobs1-nest-mb-free-identical-s1-deafacd8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:56.499681+00:00 | `20261011T220356Z-b-jakobs1-nest-mb-free-upstream-default-s1-608536fb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.591465333333334 | [record](output/lbf/20261011T220356Z-b-jakobs1-nest-mb-free-upstream-default-s1-608536fb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:57.511264+00:00 | `20261011T220357Z-b-jakobs1-nest-mb-free-identical-s2-71785400` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 4.744554916666667 | [record](output/lbf/20261011T220357Z-b-jakobs1-nest-mb-free-identical-s2-71785400/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:58.313142+00:00 | `20261011T220358Z-b-jakobs1-nest-mb-free-upstream-default-s2-88c7230e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.744554916666667 | [record](output/lbf/20261011T220358Z-b-jakobs1-nest-mb-free-upstream-default-s2-88c7230e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:58.826760+00:00 | `20261011T220358Z-b-jakobs1-nest-mb-given-identical-s0-d857a039` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.834574583333334 | [record](output/lbf/20261011T220358Z-b-jakobs1-nest-mb-given-identical-s0-d857a039/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:59.336845+00:00 | `20261011T220359Z-b-jakobs1-nest-mb-given-upstream-default-s0-dbd48a3b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.834574583333334 | [record](output/lbf/20261011T220359Z-b-jakobs1-nest-mb-given-upstream-default-s0-dbd48a3b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:03:59.953855+00:00 | `20261011T220359Z-b-jakobs1-nest-mb-given-identical-s1-b38bd7dc` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 4.50033075 | [record](output/lbf/20261011T220359Z-b-jakobs1-nest-mb-given-identical-s1-b38bd7dc/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:01.000347+00:00 | `20261011T220401Z-b-jakobs1-nest-mb-given-upstream-default-s1-2bd5f67f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.50033075 | [record](output/lbf/20261011T220401Z-b-jakobs1-nest-mb-given-upstream-default-s1-2bd5f67f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:02.451437+00:00 | `20261011T220402Z-b-jakobs1-nest-mb-given-identical-s2-76825dae` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 4.333749999999999 | [record](output/lbf/20261011T220402Z-b-jakobs1-nest-mb-given-identical-s2-76825dae/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:04.740451+00:00 | `20261011T220404Z-b-jakobs1-nest-mb-given-upstream-default-s2-ef4cab13` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.333749999999999 | [record](output/lbf/20261011T220404Z-b-jakobs1-nest-mb-given-upstream-default-s2-ef4cab13/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:05.667378+00:00 | `20261011T220405Z-b-jakobs1-strip-sheet-identical-s0-45f8c23b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.97662345 | [record](output/lbf/20261011T220405Z-b-jakobs1-strip-sheet-identical-s0-45f8c23b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:06.353913+00:00 | `20261011T220406Z-b-jakobs1-strip-sheet-upstream-default-s0-bade87da` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.97662345 | [record](output/lbf/20261011T220406Z-b-jakobs1-strip-sheet-upstream-default-s0-bade87da/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:06.921916+00:00 | `20261011T220406Z-b-jakobs1-strip-sheet-identical-s1-6be81ace` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 0.9757681 | [record](output/lbf/20261011T220406Z-b-jakobs1-strip-sheet-identical-s1-6be81ace/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:07.633490+00:00 | `20261011T220407Z-b-jakobs1-strip-sheet-upstream-default-s1-bba1b944` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9757681 | [record](output/lbf/20261011T220407Z-b-jakobs1-strip-sheet-upstream-default-s1-bba1b944/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:08.233815+00:00 | `20261011T220408Z-b-jakobs1-strip-sheet-identical-s2-5bb2af4f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 0.9999637 | [record](output/lbf/20261011T220408Z-b-jakobs1-strip-sheet-identical-s2-5bb2af4f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:09.062579+00:00 | `20261011T220409Z-b-jakobs1-strip-sheet-upstream-default-s2-90cb546f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9999637 | [record](output/lbf/20261011T220409Z-b-jakobs1-strip-sheet-upstream-default-s2-90cb546f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:09.862741+00:00 | `20261011T220409Z-b-jakobs2-nest-mb-free-identical-s0-c9afcc21` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.255797875 | [record](output/lbf/20261011T220409Z-b-jakobs2-nest-mb-free-identical-s0-c9afcc21/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:10.512120+00:00 | `20261011T220410Z-b-jakobs2-nest-mb-free-upstream-default-s0-87658000` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.255797875 | [record](output/lbf/20261011T220410Z-b-jakobs2-nest-mb-free-upstream-default-s0-87658000/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:11.142505+00:00 | `20261011T220411Z-b-jakobs2-nest-mb-free-identical-s1-30193b58` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.9617473333333333 | [record](output/lbf/20261011T220411Z-b-jakobs2-nest-mb-free-identical-s1-30193b58/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:11.806581+00:00 | `20261011T220411Z-b-jakobs2-nest-mb-free-upstream-default-s1-18bea6b3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.9617473333333333 | [record](output/lbf/20261011T220411Z-b-jakobs2-nest-mb-free-upstream-default-s1-18bea6b3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:12.447328+00:00 | `20261011T220412Z-b-jakobs2-nest-mb-free-identical-s2-89086e5d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 4.2515517916666665 | [record](output/lbf/20261011T220412Z-b-jakobs2-nest-mb-free-identical-s2-89086e5d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:13.123146+00:00 | `20261011T220413Z-b-jakobs2-nest-mb-free-upstream-default-s2-32937e7b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.2515517916666665 | [record](output/lbf/20261011T220413Z-b-jakobs2-nest-mb-free-upstream-default-s2-32937e7b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:16.950476+00:00 | `20261011T220416Z-b-jakobs2-nest-mb-given-identical-s0-f401a5fd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.916763708333333 | [record](output/lbf/20261011T220416Z-b-jakobs2-nest-mb-given-identical-s0-f401a5fd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:17.545613+00:00 | `20261011T220417Z-b-jakobs2-nest-mb-given-upstream-default-s0-c7fcb912` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.916763708333333 | [record](output/lbf/20261011T220417Z-b-jakobs2-nest-mb-given-upstream-default-s0-c7fcb912/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:18.188523+00:00 | `20261011T220418Z-b-jakobs2-nest-mb-given-identical-s1-0d45a420` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 4.333975 | [record](output/lbf/20261011T220418Z-b-jakobs2-nest-mb-given-identical-s1-0d45a420/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:18.928060+00:00 | `20261011T220418Z-b-jakobs2-nest-mb-given-upstream-default-s1-c60cf3ea` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.333975 | [record](output/lbf/20261011T220418Z-b-jakobs2-nest-mb-given-upstream-default-s1-c60cf3ea/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:19.519193+00:00 | `20261011T220419Z-b-jakobs2-nest-mb-given-identical-s2-27ef9282` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 4.2501451249999995 | [record](output/lbf/20261011T220419Z-b-jakobs2-nest-mb-given-identical-s2-27ef9282/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:19.939503+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 0, 60s, identical, axis y | valid | score 0.7004179749999999 | [record](output/sparrow-benchmark/20261011T220317Z-92f623c8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:04:20.096711+00:00 | `20261011T220420Z-b-jakobs2-nest-mb-given-upstream-default-s2-b6fd6912` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.2501451249999995 | [record](output/lbf/20261011T220420Z-b-jakobs2-nest-mb-given-upstream-default-s2-b6fd6912/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:20.742661+00:00 | `20261011T220420Z-b-jakobs2-strip-sheet-identical-s0-a033eb8f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.987095 | [record](output/lbf/20261011T220420Z-b-jakobs2-strip-sheet-identical-s0-a033eb8f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:21.369914+00:00 | `20261011T220421Z-b-jakobs2-strip-sheet-upstream-default-s0-545fefe1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.987095 | [record](output/lbf/20261011T220421Z-b-jakobs2-strip-sheet-upstream-default-s0-545fefe1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:21.981464+00:00 | `20261011T220421Z-b-jakobs2-strip-sheet-identical-s1-f4b5d765` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 0.9999283428571429 | [record](output/lbf/20261011T220421Z-b-jakobs2-strip-sheet-identical-s1-f4b5d765/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:22.546277+00:00 | `20261011T220422Z-b-jakobs2-strip-sheet-upstream-default-s1-6eab4ce6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9999283428571429 | [record](output/lbf/20261011T220422Z-b-jakobs2-strip-sheet-upstream-default-s1-6eab4ce6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:23.150759+00:00 | `20261011T220423Z-b-jakobs2-strip-sheet-identical-s2-bb6e0d40` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 0.9736153714285715 | [record](output/lbf/20261011T220423Z-b-jakobs2-strip-sheet-identical-s2-bb6e0d40/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:23.878341+00:00 | `20261011T220423Z-b-jakobs2-strip-sheet-upstream-default-s2-a5d6bf9c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9736153714285715 | [record](output/lbf/20261011T220423Z-b-jakobs2-strip-sheet-upstream-default-s2-a5d6bf9c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:24.613261+00:00 | `20261011T220424Z-b-jakobs2-strip-sheet-identical-s0-93e481a3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 0.987095 | [record](output/lbf/20261011T220424Z-b-jakobs2-strip-sheet-identical-s0-93e481a3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:25.191882+00:00 | `20261011T220425Z-b-jakobs2-strip-sheet-upstream-default-s0-38a12b07` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 0.987095 | [record](output/lbf/20261011T220425Z-b-jakobs2-strip-sheet-upstream-default-s0-38a12b07/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:25.821991+00:00 | `20261011T220425Z-b-jakobs2-strip-sheet-identical-s1-25f51e1c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 0.9999283428571429 | [record](output/lbf/20261011T220425Z-b-jakobs2-strip-sheet-identical-s1-25f51e1c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:26.346804+00:00 | `20261011T220426Z-b-jakobs2-strip-sheet-upstream-default-s1-71ba69b9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 0.9999283428571429 | [record](output/lbf/20261011T220426Z-b-jakobs2-strip-sheet-upstream-default-s1-71ba69b9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:26.873843+00:00 | `20261011T220426Z-b-jakobs2-strip-sheet-identical-s2-619f9591` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 0.9736153714285715 | [record](output/lbf/20261011T220426Z-b-jakobs2-strip-sheet-identical-s2-619f9591/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:27.389223+00:00 | `20261011T220427Z-b-jakobs2-strip-sheet-upstream-default-s2-d8c339dd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 0.9736153714285715 | [record](output/lbf/20261011T220427Z-b-jakobs2-strip-sheet-upstream-default-s2-d8c339dd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:27.953339+00:00 | `20261011T220427Z-b-mao-nest-mb-free-identical-s0-0b7d7eb5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9936534986326344 | [record](output/lbf/20261011T220427Z-b-mao-nest-mb-free-identical-s0-0b7d7eb5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:28.510084+00:00 | `20261011T220428Z-b-mao-nest-mb-free-upstream-default-s0-87f95cdd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9936534986326344 | [record](output/lbf/20261011T220428Z-b-mao-nest-mb-free-upstream-default-s0-87f95cdd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:32.704397+00:00 | `20261011T220432Z-b-mao-nest-mb-free-identical-s1-00e59033` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.1935424071710727 | [record](output/lbf/20261011T220432Z-b-mao-nest-mb-free-identical-s1-00e59033/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:33.421221+00:00 | `20261011T220433Z-b-mao-nest-mb-free-upstream-default-s1-7e7e1818` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.1935424071710727 | [record](output/lbf/20261011T220433Z-b-mao-nest-mb-free-upstream-default-s1-7e7e1818/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:34.234561+00:00 | `20261011T220434Z-b-mao-nest-mb-free-identical-s2-8b57c2ca` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.2883472816773014 | [record](output/lbf/20261011T220434Z-b-mao-nest-mb-free-identical-s2-8b57c2ca/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:34.822984+00:00 | `20261011T220434Z-b-mao-nest-mb-free-upstream-default-s2-9f71becb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.2883472816773014 | [record](output/lbf/20261011T220434Z-b-mao-nest-mb-free-upstream-default-s2-9f71becb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:35.646846+00:00 | `20261011T220435Z-b-mao-nest-mb-given-identical-s0-7d26754c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.5218588878760255 | [record](output/lbf/20261011T220435Z-b-mao-nest-mb-given-identical-s0-7d26754c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:36.187148+00:00 | `20261011T220436Z-b-mao-nest-mb-given-upstream-default-s0-d57cbdb3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.5218588878760255 | [record](output/lbf/20261011T220436Z-b-mao-nest-mb-given-upstream-default-s0-d57cbdb3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:36.729938+00:00 | `20261011T220436Z-b-mao-nest-mb-given-identical-s1-f8fd262b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.5311798851412943 | [record](output/lbf/20261011T220436Z-b-mao-nest-mb-given-identical-s1-f8fd262b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:37.272671+00:00 | `20261011T220437Z-b-mao-nest-mb-given-upstream-default-s1-8cf5e8fd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.5311798851412943 | [record](output/lbf/20261011T220437Z-b-mao-nest-mb-given-upstream-default-s1-8cf5e8fd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:37.766787+00:00 | `20261011T220437Z-b-mao-nest-mb-given-identical-s2-3cd550d4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.517141702218171 | [record](output/lbf/20261011T220437Z-b-mao-nest-mb-given-identical-s2-3cd550d4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:38.290327+00:00 | `20261011T220438Z-b-mao-nest-mb-given-upstream-default-s2-9557adfb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.517141702218171 | [record](output/lbf/20261011T220438Z-b-mao-nest-mb-given-upstream-default-s2-9557adfb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:38.746007+00:00 | `20261011T220438Z-b-mao-strip-sheet-identical-s0-543844a2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.9999798823529412 | [record](output/lbf/20261011T220438Z-b-mao-strip-sheet-identical-s0-543844a2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:39.193227+00:00 | `20261011T220439Z-b-mao-strip-sheet-upstream-default-s0-70b5130d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9999798823529412 | [record](output/lbf/20261011T220439Z-b-mao-strip-sheet-upstream-default-s0-70b5130d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:39.726129+00:00 | `20261011T220439Z-b-mao-strip-sheet-identical-s1-e9f83712` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 0.9999998039215687 | [record](output/lbf/20261011T220439Z-b-mao-strip-sheet-identical-s1-e9f83712/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:40.216579+00:00 | `20261011T220440Z-b-mao-strip-sheet-upstream-default-s1-3d81dea5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9999998039215687 | [record](output/lbf/20261011T220440Z-b-mao-strip-sheet-upstream-default-s1-3d81dea5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:40.757498+00:00 | `20261011T220440Z-b-mao-strip-sheet-identical-s2-994a71b2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 0.9855050980392157 | [record](output/lbf/20261011T220440Z-b-mao-strip-sheet-identical-s2-994a71b2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:41.242390+00:00 | `20261011T220441Z-b-mao-strip-sheet-upstream-default-s2-323b27f6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9855050980392157 | [record](output/lbf/20261011T220441Z-b-mao-strip-sheet-upstream-default-s2-323b27f6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:41.811963+00:00 | `20261011T220441Z-b-marques-strip-sheet-identical-s0-1b4d80fb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.6928079807692307 | [record](output/lbf/20261011T220441Z-b-marques-strip-sheet-identical-s0-1b4d80fb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:42.385756+00:00 | `20261011T220442Z-b-marques-strip-sheet-upstream-default-s0-ad2f191f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.6928079807692307 | [record](output/lbf/20261011T220442Z-b-marques-strip-sheet-upstream-default-s0-ad2f191f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:42.926248+00:00 | `20261011T220442Z-b-marques-strip-sheet-identical-s1-67946687` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.5876034615384615 | [record](output/lbf/20261011T220442Z-b-marques-strip-sheet-identical-s1-67946687/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:43.584809+00:00 | `20261011T220443Z-b-marques-strip-sheet-upstream-default-s1-bc593988` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.5876034615384615 | [record](output/lbf/20261011T220443Z-b-marques-strip-sheet-upstream-default-s1-bc593988/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:44.160339+00:00 | `20261011T220444Z-b-marques-strip-sheet-identical-s2-796297f5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 1.5392267884615385 | [record](output/lbf/20261011T220444Z-b-marques-strip-sheet-identical-s2-796297f5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:44.737824+00:00 | `20261011T220444Z-b-marques-strip-sheet-upstream-default-s2-50183e30` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.5392267884615385 | [record](output/lbf/20261011T220444Z-b-marques-strip-sheet-upstream-default-s2-50183e30/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:45.342337+00:00 | deepnest-next `m-mechanical-panel-hardware` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T220329Z-6fe29a07/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:04:45.308042+00:00 | `20261011T220445Z-b-shapes0-nest-mb-free-identical-s0-6eabbc66` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.903032 | [record](output/lbf/20261011T220445Z-b-shapes0-nest-mb-free-identical-s0-6eabbc66/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:51.568800+00:00 | `20261011T220451Z-b-shapes0-nest-mb-free-upstream-default-s0-7c0a7667` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.903032 | [record](output/lbf/20261011T220451Z-b-shapes0-nest-mb-free-upstream-default-s0-7c0a7667/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:52.300526+00:00 | `20261011T220452Z-b-shapes0-nest-mb-free-identical-s1-10cf34f4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 7.810367761904762 | [record](output/lbf/20261011T220452Z-b-shapes0-nest-mb-free-identical-s1-10cf34f4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:53.059214+00:00 | `20261011T220453Z-b-shapes0-nest-mb-free-upstream-default-s1-43fe3c33` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.810367761904762 | [record](output/lbf/20261011T220453Z-b-shapes0-nest-mb-free-upstream-default-s1-43fe3c33/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:53.751152+00:00 | `20261011T220453Z-b-shapes0-nest-mb-free-identical-s2-4ee83da0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 7.843214095238094 | [record](output/lbf/20261011T220453Z-b-shapes0-nest-mb-free-identical-s2-4ee83da0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:54.468629+00:00 | `20261011T220454Z-b-shapes0-nest-mb-free-upstream-default-s2-ecfd75b1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.843214095238094 | [record](output/lbf/20261011T220454Z-b-shapes0-nest-mb-free-upstream-default-s2-ecfd75b1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:55.212926+00:00 | `20261011T220455Z-b-shapes0-nest-mb-free-identical-s0-88040ee9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 7.903032 | [record](output/lbf/20261011T220455Z-b-shapes0-nest-mb-free-identical-s0-88040ee9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:56.005672+00:00 | `20261011T220456Z-b-shapes0-nest-mb-free-upstream-default-s0-bcdd5721` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 7.903032 | [record](output/lbf/20261011T220456Z-b-shapes0-nest-mb-free-upstream-default-s0-bcdd5721/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:56.907901+00:00 | `20261011T220456Z-b-shapes0-nest-mb-free-identical-s1-92ceea6e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 7.810367761904762 | [record](output/lbf/20261011T220456Z-b-shapes0-nest-mb-free-identical-s1-92ceea6e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:57.757242+00:00 | `20261011T220457Z-b-shapes0-nest-mb-free-upstream-default-s1-9fe2ce70` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 7.810367761904762 | [record](output/lbf/20261011T220457Z-b-shapes0-nest-mb-free-upstream-default-s1-9fe2ce70/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:58.561564+00:00 | `20261011T220458Z-b-shapes0-nest-mb-free-identical-s2-f246de17` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 7.843214095238094 | [record](output/lbf/20261011T220458Z-b-shapes0-nest-mb-free-identical-s2-f246de17/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:59.250926+00:00 | `20261011T220459Z-b-shapes0-nest-mb-free-upstream-default-s2-10305ba8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 7.843214095238094 | [record](output/lbf/20261011T220459Z-b-shapes0-nest-mb-free-upstream-default-s2-10305ba8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:04:59.988186+00:00 | `20261011T220459Z-b-shapes0-nest-mb-given-identical-s0-283ba459` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.952538238095238 | [record](output/lbf/20261011T220459Z-b-shapes0-nest-mb-given-identical-s0-283ba459/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:00.672536+00:00 | `20261011T220500Z-b-shapes0-nest-mb-given-upstream-default-s0-ac652757` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.952538238095238 | [record](output/lbf/20261011T220500Z-b-shapes0-nest-mb-given-upstream-default-s0-ac652757/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:01.327893+00:00 | `20261011T220501Z-b-shapes0-nest-mb-given-identical-s1-9fe15c20` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 7.858230904761904 | [record](output/lbf/20261011T220501Z-b-shapes0-nest-mb-given-identical-s1-9fe15c20/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:02.021742+00:00 | `20261011T220502Z-b-shapes0-nest-mb-given-upstream-default-s1-71194ed9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.858230904761904 | [record](output/lbf/20261011T220502Z-b-shapes0-nest-mb-given-upstream-default-s1-71194ed9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:02.664026+00:00 | `20261011T220502Z-b-shapes0-nest-mb-given-identical-s2-44df5225` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 7.857871047619048 | [record](output/lbf/20261011T220502Z-b-shapes0-nest-mb-given-identical-s2-44df5225/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:03.344693+00:00 | `20261011T220503Z-b-shapes0-nest-mb-given-upstream-default-s2-56ddc692` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.857871047619048 | [record](output/lbf/20261011T220503Z-b-shapes0-nest-mb-given-upstream-default-s2-56ddc692/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:03.941724+00:00 | `20261011T220503Z-b-shapes0-strip-sheet-identical-s0-90b3458d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.95071125 | [record](output/lbf/20261011T220503Z-b-shapes0-strip-sheet-identical-s0-90b3458d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:04.497590+00:00 | `20261011T220504Z-b-shapes0-strip-sheet-upstream-default-s0-e1df91a0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.95071125 | [record](output/lbf/20261011T220504Z-b-shapes0-strip-sheet-upstream-default-s0-e1df91a0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:05.049212+00:00 | `20261011T220505Z-b-shapes0-strip-sheet-identical-s1-1f946d45` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.9510916750000002 | [record](output/lbf/20261011T220505Z-b-shapes0-strip-sheet-identical-s1-1f946d45/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:09.639932+00:00 | `20261011T220509Z-b-shapes0-strip-sheet-upstream-default-s1-a6167b09` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9510916750000002 | [record](output/lbf/20261011T220509Z-b-shapes0-strip-sheet-upstream-default-s1-a6167b09/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:10.070814+00:00 | `20261011T220510Z-b-shapes0-strip-sheet-identical-s2-70d303ff` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.9510819500000003 | [record](output/lbf/20261011T220510Z-b-shapes0-strip-sheet-identical-s2-70d303ff/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:10.513706+00:00 | `20261011T220510Z-b-shapes0-strip-sheet-upstream-default-s2-12a697af` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9510819500000003 | [record](output/lbf/20261011T220510Z-b-shapes0-strip-sheet-upstream-default-s2-12a697af/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:11.025215+00:00 | `20261011T220511Z-b-shapes1-nest-mb-free-identical-s0-d377e95c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.903032 | [record](output/lbf/20261011T220511Z-b-shapes1-nest-mb-free-identical-s0-d377e95c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:11.581559+00:00 | `20261011T220511Z-b-shapes1-nest-mb-free-upstream-default-s0-07a97c18` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.903032 | [record](output/lbf/20261011T220511Z-b-shapes1-nest-mb-free-upstream-default-s0-07a97c18/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:12.179602+00:00 | `20261011T220512Z-b-shapes1-nest-mb-free-identical-s1-5ccd1a20` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 7.810367761904762 | [record](output/lbf/20261011T220512Z-b-shapes1-nest-mb-free-identical-s1-5ccd1a20/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:12.836419+00:00 | `20261011T220512Z-b-shapes1-nest-mb-free-upstream-default-s1-c590347d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.810367761904762 | [record](output/lbf/20261011T220512Z-b-shapes1-nest-mb-free-upstream-default-s1-c590347d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:13.697395+00:00 | `20261011T220513Z-b-shapes1-nest-mb-free-identical-s2-0083a9d8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 7.843214095238094 | [record](output/lbf/20261011T220513Z-b-shapes1-nest-mb-free-identical-s2-0083a9d8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:14.429284+00:00 | `20261011T220514Z-b-shapes1-nest-mb-free-upstream-default-s2-a6e5ac4b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.843214095238094 | [record](output/lbf/20261011T220514Z-b-shapes1-nest-mb-free-upstream-default-s2-a6e5ac4b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:15.369193+00:00 | verified svgnest batch `20261011T215310Z-ad709e2b` | 0/12 valid | [table](benchmarks/results/svgnest-20261011T220515Z-53a4946e.md). Provisional; all failures retained.

- 2026-10-11T22:05:15.044733+00:00 | `20261011T220515Z-b-shapes1-nest-mb-given-identical-s0-830254dd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 8.286119333333334 | [record](output/lbf/20261011T220515Z-b-shapes1-nest-mb-given-identical-s0-830254dd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:15.582286+00:00 | `20261011T220515Z-b-shapes1-nest-mb-given-upstream-default-s0-12e74b6b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.286119333333334 | [record](output/lbf/20261011T220515Z-b-shapes1-nest-mb-given-upstream-default-s0-12e74b6b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:16.195367+00:00 | `20261011T220516Z-b-shapes1-nest-mb-given-identical-s1-6b6e663d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 8.286629952380952 | [record](output/lbf/20261011T220516Z-b-shapes1-nest-mb-given-identical-s1-6b6e663d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:16.782931+00:00 | `20261011T220516Z-b-shapes1-nest-mb-given-upstream-default-s1-edf3481f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.286629952380952 | [record](output/lbf/20261011T220516Z-b-shapes1-nest-mb-given-upstream-default-s1-edf3481f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:17.389416+00:00 | `20261011T220517Z-b-shapes1-nest-mb-given-identical-s2-a9cfa655` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 8.285849809523809 | [record](output/lbf/20261011T220517Z-b-shapes1-nest-mb-given-identical-s2-a9cfa655/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:17.928475+00:00 | `20261011T220517Z-b-shapes1-nest-mb-given-upstream-default-s2-f6b1253d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.285849809523809 | [record](output/lbf/20261011T220517Z-b-shapes1-nest-mb-given-upstream-default-s2-f6b1253d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:18.689923+00:00 | `20261011T220518Z-b-shapes1-strip-sheet-identical-s0-598ce86a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9772045 | [record](output/lbf/20261011T220518Z-b-shapes1-strip-sheet-identical-s0-598ce86a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:19.323954+00:00 | `20261011T220519Z-b-shapes1-strip-sheet-upstream-default-s0-a4917e6e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9772045 | [record](output/lbf/20261011T220519Z-b-shapes1-strip-sheet-upstream-default-s0-a4917e6e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:19.855143+00:00 | `20261011T220519Z-b-shapes1-strip-sheet-identical-s1-9e03d13e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.9760103250000003 | [record](output/lbf/20261011T220519Z-b-shapes1-strip-sheet-identical-s1-9e03d13e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:20.380757+00:00 | `20261011T220520Z-b-shapes1-strip-sheet-upstream-default-s1-e5ed77e6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9760103250000003 | [record](output/lbf/20261011T220520Z-b-shapes1-strip-sheet-upstream-default-s1-e5ed77e6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:20.864924+00:00 | `20261011T220520Z-b-shapes1-strip-sheet-identical-s2-727b4a3c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.9762408249999996 | [record](output/lbf/20261011T220520Z-b-shapes1-strip-sheet-identical-s2-727b4a3c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:21.311582+00:00 | `20261011T220521Z-b-shapes1-strip-sheet-upstream-default-s2-50414049` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9762408249999996 | [record](output/lbf/20261011T220521Z-b-shapes1-strip-sheet-upstream-default-s2-50414049/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:21.756187+00:00 | `20261011T220521Z-b-shirts-nest-mb-free-identical-s0-15cc4e33` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 7.985671487179487 | [record](output/lbf/20261011T220521Z-b-shirts-nest-mb-free-identical-s0-15cc4e33/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:22.265753+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220419Z-43f218ea/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:05:22.427164+00:00 | `20261011T220522Z-b-shirts-nest-mb-free-upstream-default-s0-031fb95e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.985671487179487 | [record](output/lbf/20261011T220522Z-b-shirts-nest-mb-free-upstream-default-s0-031fb95e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:28.421572+00:00 | `20261011T220528Z-b-shirts-nest-mb-free-identical-s1-bb98a785` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 7.9856031282051285 | [record](output/lbf/20261011T220528Z-b-shirts-nest-mb-free-identical-s1-bb98a785/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:29.174950+00:00 | `20261011T220529Z-b-shirts-nest-mb-free-upstream-default-s1-867ccfd4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 7.9856031282051285 | [record](output/lbf/20261011T220529Z-b-shirts-nest-mb-free-upstream-default-s1-867ccfd4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:29.866957+00:00 | `20261011T220529Z-b-shirts-nest-mb-free-identical-s2-20807b7b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 8.212887743589743 | [record](output/lbf/20261011T220529Z-b-shirts-nest-mb-free-identical-s2-20807b7b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:30.503738+00:00 | `20261011T220530Z-b-shirts-nest-mb-free-upstream-default-s2-795f0c57` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.212887743589743 | [record](output/lbf/20261011T220530Z-b-shirts-nest-mb-free-upstream-default-s2-795f0c57/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:31.347221+00:00 | `20261011T220531Z-b-shirts-nest-mb-given-identical-s0-436f0b59` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 8.771087641025641 | [record](output/lbf/20261011T220531Z-b-shirts-nest-mb-given-identical-s0-436f0b59/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:32.069990+00:00 | `20261011T220532Z-b-shirts-nest-mb-given-upstream-default-s0-3c8968d8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.771087641025641 | [record](output/lbf/20261011T220532Z-b-shirts-nest-mb-given-upstream-default-s0-3c8968d8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:32.823209+00:00 | `20261011T220532Z-b-shirts-nest-mb-given-identical-s1-3faefee3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 8.87303282051282 | [record](output/lbf/20261011T220532Z-b-shirts-nest-mb-given-identical-s1-3faefee3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:33.781696+00:00 | SVGnest `m-garment-bruce-1` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T220528Z-a6103dae/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:05:33.704123+00:00 | `20261011T220533Z-b-shirts-nest-mb-given-upstream-default-s1-434f9f40` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.87303282051282 | [record](output/lbf/20261011T220533Z-b-shirts-nest-mb-given-upstream-default-s1-434f9f40/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:34.535502+00:00 | `20261011T220534Z-b-shirts-nest-mb-given-identical-s2-e1b24e5a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 8.66722758974359 | [record](output/lbf/20261011T220534Z-b-shirts-nest-mb-given-identical-s2-e1b24e5a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:35.325065+00:00 | `20261011T220535Z-b-shirts-nest-mb-given-upstream-default-s2-0eaec478` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 8.66722758974359 | [record](output/lbf/20261011T220535Z-b-shirts-nest-mb-given-upstream-default-s2-0eaec478/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:36.097468+00:00 | `20261011T220536Z-b-shirts-strip-sheet-identical-s0-90167a0d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.9999089500000005 | [record](output/lbf/20261011T220536Z-b-shirts-strip-sheet-identical-s0-90167a0d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:36.905544+00:00 | `20261011T220536Z-b-shirts-strip-sheet-upstream-default-s0-14b999c7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9999089500000005 | [record](output/lbf/20261011T220536Z-b-shirts-strip-sheet-upstream-default-s0-14b999c7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:37.577226+00:00 | `20261011T220537Z-b-shirts-strip-sheet-identical-s1-14022952` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.9775571750000003 | [record](output/lbf/20261011T220537Z-b-shirts-strip-sheet-identical-s1-14022952/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:38.306991+00:00 | `20261011T220538Z-b-shirts-strip-sheet-upstream-default-s1-605c88e6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9775571750000003 | [record](output/lbf/20261011T220538Z-b-shirts-strip-sheet-upstream-default-s1-605c88e6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:39.138207+00:00 | `20261011T220539Z-b-shirts-strip-sheet-identical-s2-714f8de4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.99988175 | [record](output/lbf/20261011T220539Z-b-shirts-strip-sheet-identical-s2-714f8de4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:39.831275+00:00 | `20261011T220539Z-b-shirts-strip-sheet-upstream-default-s2-80ad4e04` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.99988175 | [record](output/lbf/20261011T220539Z-b-shirts-strip-sheet-upstream-default-s2-80ad4e04/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:40.482686+00:00 | `20261011T220540Z-b-swim-nest-mb-free-identical-s0-42abc03f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 5.9654123881329495 | [record](output/lbf/20261011T220540Z-b-swim-nest-mb-free-identical-s0-42abc03f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:41.227630+00:00 | `20261011T220541Z-b-swim-nest-mb-free-upstream-default-s0-297bf910` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.641789552791679 | [record](output/lbf/20261011T220541Z-b-swim-nest-mb-free-upstream-default-s0-297bf910/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:41.913186+00:00 | `20261011T220541Z-b-swim-nest-mb-free-identical-s1-b794da8d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 5.968781223215225 | [record](output/lbf/20261011T220541Z-b-swim-nest-mb-free-identical-s1-b794da8d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:42.599307+00:00 | `20261011T220542Z-b-swim-nest-mb-free-upstream-default-s1-5ae36683` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.959175211573801 | [record](output/lbf/20261011T220542Z-b-swim-nest-mb-free-upstream-default-s1-5ae36683/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:43.241145+00:00 | `20261011T220543Z-b-swim-nest-mb-free-identical-s2-97e38a79` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 5.907579722875648 | [record](output/lbf/20261011T220543Z-b-swim-nest-mb-free-identical-s2-97e38a79/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:43.906987+00:00 | `20261011T220543Z-b-swim-nest-mb-free-upstream-default-s2-acbdfe1b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.936747625916795 | [record](output/lbf/20261011T220543Z-b-swim-nest-mb-free-upstream-default-s2-acbdfe1b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:44.619717+00:00 | `20261011T220544Z-b-swim-nest-mb-given-identical-s0-09479614` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 5.4671329918460385 | [record](output/lbf/20261011T220544Z-b-swim-nest-mb-given-identical-s0-09479614/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:51.671985+00:00 | `20261011T220551Z-b-swim-nest-mb-given-upstream-default-s0-9c501bda` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.31013764406947 | [record](output/lbf/20261011T220551Z-b-swim-nest-mb-given-upstream-default-s0-9c501bda/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:52.525353+00:00 | `20261011T220552Z-b-swim-nest-mb-given-identical-s1-632da686` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 5.827799107456129 | [record](output/lbf/20261011T220552Z-b-swim-nest-mb-given-identical-s1-632da686/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:53.229152+00:00 | `20261011T220553Z-b-swim-nest-mb-given-upstream-default-s1-b6fed308` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.847768901298923 | [record](output/lbf/20261011T220553Z-b-swim-nest-mb-given-upstream-default-s1-b6fed308/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:53.945526+00:00 | `20261011T220553Z-b-swim-nest-mb-given-identical-s2-5f02612b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 5.667383271506984 | [record](output/lbf/20261011T220553Z-b-swim-nest-mb-given-identical-s2-5f02612b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:54.695191+00:00 | `20261011T220554Z-b-swim-nest-mb-given-upstream-default-s2-6d3c8b0a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 5.776599320344002 | [record](output/lbf/20261011T220554Z-b-swim-nest-mb-given-upstream-default-s2-6d3c8b0a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:55.472678+00:00 | `20261011T220555Z-b-swim-nest-mb-given-identical-s0-132fb3c0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 5.4671329918460385 | [record](output/lbf/20261011T220555Z-b-swim-nest-mb-given-identical-s0-132fb3c0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:56.193780+00:00 | `20261011T220556Z-b-swim-nest-mb-given-upstream-default-s0-eb681ad5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 5.31013764406947 | [record](output/lbf/20261011T220556Z-b-swim-nest-mb-given-upstream-default-s0-eb681ad5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:56.997504+00:00 | `20261011T220556Z-b-swim-nest-mb-given-identical-s1-64204f95` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 5.827799107456129 | [record](output/lbf/20261011T220556Z-b-swim-nest-mb-given-identical-s1-64204f95/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:57.879146+00:00 | `20261011T220557Z-b-swim-nest-mb-given-upstream-default-s1-dbc1a279` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 5.847768901298923 | [record](output/lbf/20261011T220557Z-b-swim-nest-mb-given-upstream-default-s1-dbc1a279/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:58.737430+00:00 | `20261011T220558Z-b-swim-nest-mb-given-identical-s2-c9903276` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 5.667383271506984 | [record](output/lbf/20261011T220558Z-b-swim-nest-mb-given-identical-s2-c9903276/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:05:59.421599+00:00 | `20261011T220559Z-b-swim-nest-mb-given-upstream-default-s2-a8b44d99` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 5.776599320344002 | [record](output/lbf/20261011T220559Z-b-swim-nest-mb-given-upstream-default-s2-a8b44d99/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:00.199754+00:00 | `20261011T220600Z-b-swim-strip-sheet-identical-s0-70f92a0e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.9999601877607789 | [record](output/lbf/20261011T220600Z-b-swim-strip-sheet-identical-s0-70f92a0e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:00.874960+00:00 | `20261011T220600Z-b-swim-strip-sheet-upstream-default-s0-4efa1108` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9999494089012517 | [record](output/lbf/20261011T220600Z-b-swim-strip-sheet-upstream-default-s0-4efa1108/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:01.525210+00:00 | `20261011T220601Z-b-swim-strip-sheet-identical-s1-7f0b4618` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.9933327538247565 | [record](output/lbf/20261011T220601Z-b-swim-strip-sheet-identical-s1-7f0b4618/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:02.125871+00:00 | `20261011T220602Z-b-swim-strip-sheet-upstream-default-s1-19e2491d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9933327538247565 | [record](output/lbf/20261011T220602Z-b-swim-strip-sheet-upstream-default-s1-19e2491d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:02.725102+00:00 | `20261011T220602Z-b-swim-strip-sheet-identical-s2-2e1835ee` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 1.9955324680111266 | [record](output/lbf/20261011T220602Z-b-swim-strip-sheet-identical-s2-2e1835ee/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:03.365967+00:00 | `20261011T220603Z-b-swim-strip-sheet-upstream-default-s2-38349cd4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9955324680111266 | [record](output/lbf/20261011T220603Z-b-swim-strip-sheet-upstream-default-s2-38349cd4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:04.071123+00:00 | `20261011T220604Z-b-trousers-nest-mb-free-identical-s0-d2faa43b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.716267604519774 | [record](output/lbf/20261011T220604Z-b-trousers-nest-mb-free-identical-s0-d2faa43b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:04.993063+00:00 | `20261011T220604Z-b-trousers-nest-mb-free-upstream-default-s0-f30c6f39` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.716267604519774 | [record](output/lbf/20261011T220604Z-b-trousers-nest-mb-free-upstream-default-s0-f30c6f39/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:13.990704+00:00 | `20261011T220613Z-b-trousers-nest-mb-free-identical-s1-ce7f2ae5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.739641525423729 | [record](output/lbf/20261011T220613Z-b-trousers-nest-mb-free-identical-s1-ce7f2ae5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:15.322368+00:00 | `20261011T220615Z-b-trousers-nest-mb-free-upstream-default-s1-20c48094` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.739641525423729 | [record](output/lbf/20261011T220615Z-b-trousers-nest-mb-free-upstream-default-s1-20c48094/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:17.136305+00:00 | `20261011T220617Z-b-trousers-nest-mb-free-identical-s2-d73809ae` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 3.512296429378531 | [record](output/lbf/20261011T220617Z-b-trousers-nest-mb-free-identical-s2-d73809ae/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:18.082318+00:00 | `20261011T220618Z-b-trousers-nest-mb-free-upstream-default-s2-193970c4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.512296429378531 | [record](output/lbf/20261011T220618Z-b-trousers-nest-mb-free-upstream-default-s2-193970c4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:18.778198+00:00 | `20261011T220618Z-b-trousers-nest-mb-given-identical-s0-832037df` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 3.5117278418079096 | [record](output/lbf/20261011T220618Z-b-trousers-nest-mb-given-identical-s0-832037df/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:19.664187+00:00 | `20261011T220619Z-b-trousers-nest-mb-given-upstream-default-s0-67314bb2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.5117278418079096 | [record](output/lbf/20261011T220619Z-b-trousers-nest-mb-given-upstream-default-s0-67314bb2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:20.580497+00:00 | `20261011T220620Z-b-trousers-nest-mb-given-identical-s1-6b67d979` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 3.5457630169491527 | [record](output/lbf/20261011T220620Z-b-trousers-nest-mb-given-identical-s1-6b67d979/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:21.869877+00:00 | `20261011T220621Z-b-trousers-nest-mb-given-upstream-default-s1-c29d3d0c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.5457630169491527 | [record](output/lbf/20261011T220621Z-b-trousers-nest-mb-given-upstream-default-s1-c29d3d0c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:22.896253+00:00 | `20261011T220622Z-b-trousers-nest-mb-given-identical-s2-53ef62a7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 3.3635456723163846 | [record](output/lbf/20261011T220622Z-b-trousers-nest-mb-given-identical-s2-53ef62a7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:23.569133+00:00 | `20261011T220623Z-b-trousers-nest-mb-given-upstream-default-s2-402d21a8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 3.3635456723163846 | [record](output/lbf/20261011T220623Z-b-trousers-nest-mb-given-upstream-default-s2-402d21a8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:24.520279+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220522Z-fb4e001f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:06:24.225413+00:00 | `20261011T220624Z-b-trousers-nest-mb-given-identical-s0-0c635349` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 3.5117278418079096 | [record](output/lbf/20261011T220624Z-b-trousers-nest-mb-given-identical-s0-0c635349/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:25.204150+00:00 | `20261011T220625Z-b-trousers-nest-mb-given-upstream-default-s0-e3275054` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 3.5117278418079096 | [record](output/lbf/20261011T220625Z-b-trousers-nest-mb-given-upstream-default-s0-e3275054/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:25.914654+00:00 | `20261011T220625Z-b-trousers-nest-mb-given-identical-s1-39fd32c6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 3.5457630169491527 | [record](output/lbf/20261011T220625Z-b-trousers-nest-mb-given-identical-s1-39fd32c6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:26.577369+00:00 | `20261011T220626Z-b-trousers-nest-mb-given-upstream-default-s1-72259bec` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 3.5457630169491527 | [record](output/lbf/20261011T220626Z-b-trousers-nest-mb-given-upstream-default-s1-72259bec/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:27.576688+00:00 | `20261011T220627Z-b-trousers-nest-mb-given-identical-s2-7a77cebb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 3.3635456723163846 | [record](output/lbf/20261011T220627Z-b-trousers-nest-mb-given-identical-s2-7a77cebb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:28.539880+00:00 | `20261011T220628Z-b-trousers-nest-mb-given-upstream-default-s2-b862ab30` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 3.3635456723163846 | [record](output/lbf/20261011T220628Z-b-trousers-nest-mb-given-upstream-default-s2-b862ab30/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:30.263920+00:00 | `20261011T220630Z-b-trousers-strip-sheet-identical-s0-b3a2b539` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 2.983522405063291 | [record](output/lbf/20261011T220630Z-b-trousers-strip-sheet-identical-s0-b3a2b539/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:31.643207+00:00 | `20261011T220631Z-b-trousers-strip-sheet-upstream-default-s0-2612b539` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.983522405063291 | [record](output/lbf/20261011T220631Z-b-trousers-strip-sheet-upstream-default-s0-2612b539/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:32.386554+00:00 | `20261011T220632Z-b-trousers-strip-sheet-identical-s1-f2ba3af8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 2.9969105189873417 | [record](output/lbf/20261011T220632Z-b-trousers-strip-sheet-identical-s1-f2ba3af8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:44.122798+00:00 | deepnest-next `m-mechanical-remnant-kit` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T220446Z-1123401a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:06:43.834116+00:00 | `20261011T220643Z-b-trousers-strip-sheet-upstream-default-s1-d7da0689` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9969105189873417 | [record](output/lbf/20261011T220643Z-b-trousers-strip-sheet-upstream-default-s1-d7da0689/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:44.373663+00:00 | SVGnest `m-garment-bruce-1` seed 0, 5s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T220628Z-eaccb40b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:06:44.459306+00:00 | `20261011T220644Z-b-trousers-strip-sheet-identical-s2-dda9abfb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 2.9967448101265823 | [record](output/lbf/20261011T220644Z-b-trousers-strip-sheet-identical-s2-dda9abfb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:45.264334+00:00 | `20261011T220645Z-b-trousers-strip-sheet-upstream-default-s2-738d1d43` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 2.9967448101265823 | [record](output/lbf/20261011T220645Z-b-trousers-strip-sheet-upstream-default-s2-738d1d43/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:45.829679+00:00 | `20261011T220645Z-m-box-batch-500-identical-s0-00c832c8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220645Z-m-box-batch-500-identical-s0-00c832c8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:46.365292+00:00 | `20261011T220646Z-m-box-batch-500-upstream-default-s0-66fd4dc7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220646Z-m-box-batch-500-upstream-default-s0-66fd4dc7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:47.422906+00:00 | `20261011T220647Z-m-box-batch-500-identical-s1-ec4f5500` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220647Z-m-box-batch-500-identical-s1-ec4f5500/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:47.981515+00:00 | `20261011T220647Z-m-box-batch-500-upstream-default-s1-30557e30` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220647Z-m-box-batch-500-upstream-default-s1-30557e30/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:48.338764+00:00 | `20261011T220648Z-m-box-batch-500-identical-s2-fdd62e1e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220648Z-m-box-batch-500-identical-s2-fdd62e1e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:48.754253+00:00 | `20261011T220648Z-m-box-batch-500-upstream-default-s2-8d8b120d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220648Z-m-box-batch-500-upstream-default-s2-8d8b120d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:49.220492+00:00 | `20261011T220649Z-m-box-desktop-identical-s0-a9727c9c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220649Z-m-box-desktop-identical-s0-a9727c9c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:49.863891+00:00 | `20261011T220649Z-m-box-desktop-upstream-default-s0-f3a5927a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220649Z-m-box-desktop-upstream-default-s0-f3a5927a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:50.650279+00:00 | `20261011T220650Z-m-box-desktop-identical-s1-77cefc55` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220650Z-m-box-desktop-identical-s1-77cefc55/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:50.986251+00:00 | `20261011T220650Z-m-box-desktop-upstream-default-s1-812ba9d5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220650Z-m-box-desktop-upstream-default-s1-812ba9d5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:51.506354+00:00 | `20261011T220651Z-m-box-desktop-identical-s2-43b29421` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220651Z-m-box-desktop-identical-s2-43b29421/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:52.239906+00:00 | `20261011T220652Z-m-box-desktop-upstream-default-s2-32c891bb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220652Z-m-box-desktop-upstream-default-s2-32c891bb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:52.544338+00:00 | `20261011T220652Z-m-box-long-identical-s0-0282961c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220652Z-m-box-long-identical-s0-0282961c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:53.439804+00:00 | `20261011T220653Z-m-box-long-upstream-default-s0-cc0de07b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220653Z-m-box-long-upstream-default-s0-cc0de07b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:53.754436+00:00 | `20261011T220653Z-m-box-long-identical-s1-169b563b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220653Z-m-box-long-identical-s1-169b563b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:54.082648+00:00 | `20261011T220654Z-m-box-long-upstream-default-s1-98248ec5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220654Z-m-box-long-upstream-default-s1-98248ec5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:54.466527+00:00 | `20261011T220654Z-m-box-long-identical-s2-7e7ead29` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220654Z-m-box-long-identical-s2-7e7ead29/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:54.844024+00:00 | `20261011T220654Z-m-box-long-upstream-default-s2-aaf9f5ba` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220654Z-m-box-long-upstream-default-s2-aaf9f5ba/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:06:55.478626+00:00 | `20261011T220655Z-m-box-mini-identical-s0-893925b2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220655Z-m-box-mini-identical-s0-893925b2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:03.163703+00:00 | `20261011T220703Z-m-box-mini-upstream-default-s0-b5b03bbe` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220703Z-m-box-mini-upstream-default-s0-b5b03bbe/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:03.856079+00:00 | `20261011T220703Z-m-box-mini-identical-s1-677aa9f3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220703Z-m-box-mini-identical-s1-677aa9f3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:04.243010+00:00 | `20261011T220704Z-m-box-mini-upstream-default-s1-d2606bd1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220704Z-m-box-mini-upstream-default-s1-d2606bd1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:04.846059+00:00 | `20261011T220704Z-m-box-mini-identical-s2-dec6c824` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220704Z-m-box-mini-identical-s2-dec6c824/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:05.944214+00:00 | `20261011T220705Z-m-box-mini-upstream-default-s2-5cf2e763` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220705Z-m-box-mini-upstream-default-s2-5cf2e763/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:06.352511+00:00 | `20261011T220706Z-m-box-mini-identical-s0-1ab344aa` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220706Z-m-box-mini-identical-s0-1ab344aa/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:06.721670+00:00 | `20261011T220706Z-m-box-mini-upstream-default-s0-bf7d1243` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220706Z-m-box-mini-upstream-default-s0-bf7d1243/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:07.098665+00:00 | `20261011T220707Z-m-box-mini-identical-s1-dd4445ff` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220707Z-m-box-mini-identical-s1-dd4445ff/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:07.544433+00:00 | `20261011T220707Z-m-box-mini-upstream-default-s1-8d42bbdb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220707Z-m-box-mini-upstream-default-s1-8d42bbdb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:08.255125+00:00 | `20261011T220708Z-m-box-mini-identical-s2-f951c635` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220708Z-m-box-mini-identical-s2-f951c635/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:08.637019+00:00 | `20261011T220708Z-m-box-mini-upstream-default-s2-73176e44` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220708Z-m-box-mini-upstream-default-s2-73176e44/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:09.065788+00:00 | `20261011T220709Z-m-box-storage-identical-s0-042a168f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220709Z-m-box-storage-identical-s0-042a168f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:09.804933+00:00 | `20261011T220709Z-m-box-storage-upstream-default-s0-9c276c8e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220709Z-m-box-storage-upstream-default-s0-9c276c8e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:10.275320+00:00 | `20261011T220710Z-m-box-storage-identical-s1-1e70d882` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220710Z-m-box-storage-identical-s1-1e70d882/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:11.032444+00:00 | `20261011T220711Z-m-box-storage-upstream-default-s1-cac56269` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220711Z-m-box-storage-upstream-default-s1-cac56269/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:11.559500+00:00 | `20261011T220711Z-m-box-storage-identical-s2-5afaf7ca` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220711Z-m-box-storage-identical-s2-5afaf7ca/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:12.128796+00:00 | `20261011T220712Z-m-box-storage-upstream-default-s2-ebe85d03` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220712Z-m-box-storage-upstream-default-s2-ebe85d03/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:12.653269+00:00 | `20261011T220712Z-m-box-tool-identical-s0-602002ae` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220712Z-m-box-tool-identical-s0-602002ae/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:13.120819+00:00 | `20261011T220713Z-m-box-tool-upstream-default-s0-075d7ae1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220713Z-m-box-tool-upstream-default-s0-075d7ae1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:22.520465+00:00 | `20261011T220722Z-m-box-tool-identical-s1-2ba0868c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220722Z-m-box-tool-identical-s1-2ba0868c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:23.267841+00:00 | `20261011T220723Z-m-box-tool-upstream-default-s1-c11b0d78` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220723Z-m-box-tool-upstream-default-s1-c11b0d78/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:24.358837+00:00 | `20261011T220724Z-m-box-tool-identical-s2-2f46deb2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220724Z-m-box-tool-identical-s2-2f46deb2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:25.675901+00:00 | `20261011T220725Z-m-box-tool-upstream-default-s2-96936830` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220725Z-m-box-tool-upstream-default-s2-96936830/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:27.202803+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 0, 60s, identical, axis y | valid | score 0.7452374 | [record](output/sparrow-benchmark/20261011T220624Z-ceca9f0b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:07:26.705087+00:00 | `20261011T220726Z-m-garment-bruce-1-identical-s0-858d093e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.9677442279999999 | [record](output/lbf/20261011T220726Z-m-garment-bruce-1-identical-s0-858d093e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:28.827310+00:00 | `20261011T220728Z-m-garment-bruce-1-upstream-default-s0-9fa59a6f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9677442279999999 | [record](output/lbf/20261011T220728Z-m-garment-bruce-1-upstream-default-s0-9fa59a6f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:30.377853+00:00 | verified deepnest batch `20261011T220219Z-4577dacc` | 0/3 valid | [table](benchmarks/results/deepnest-20261011T220730Z-5e7c70c2.md). Provisional; all failures retained.

- 2026-10-11T22:07:30.207509+00:00 | `20261011T220730Z-m-garment-bruce-1-identical-s1-c79dce3b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 0.9906476670000001 | [record](output/lbf/20261011T220730Z-m-garment-bruce-1-identical-s1-c79dce3b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:32.272645+00:00 | `20261011T220732Z-m-garment-bruce-1-upstream-default-s1-c356f691` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9906476670000001 | [record](output/lbf/20261011T220732Z-m-garment-bruce-1-upstream-default-s1-c356f691/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:34.064594+00:00 | `20261011T220734Z-m-garment-bruce-1-identical-s2-94d2d459` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 0.9674126000000001 | [record](output/lbf/20261011T220734Z-m-garment-bruce-1-identical-s2-94d2d459/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:36.059238+00:00 | `20261011T220736Z-m-garment-bruce-1-upstream-default-s2-48179135` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9674126000000001 | [record](output/lbf/20261011T220736Z-m-garment-bruce-1-upstream-default-s2-48179135/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:38.257486+00:00 | `20261011T220738Z-m-garment-bruce-2-identical-s0-c799e335` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.99998865 | [record](output/lbf/20261011T220738Z-m-garment-bruce-2-identical-s0-c799e335/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:40.916948+00:00 | `20261011T220740Z-m-garment-bruce-2-upstream-default-s0-f0318432` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9998925002500001 | [record](output/lbf/20261011T220740Z-m-garment-bruce-2-upstream-default-s0-f0318432/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:43.150890+00:00 | `20261011T220743Z-m-garment-bruce-2-identical-s1-0ae52d5f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | invalid; independent material none | [record](output/lbf/20261011T220743Z-m-garment-bruce-2-identical-s1-0ae52d5f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:45.642305+00:00 | `20261011T220745Z-m-garment-bruce-2-upstream-default-s1-93110971` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | invalid; independent material none | [record](output/lbf/20261011T220745Z-m-garment-bruce-2-upstream-default-s1-93110971/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:47.463730+00:00 | `20261011T220747Z-m-garment-bruce-2-identical-s2-6adb7e31` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | invalid; independent material none | [record](output/lbf/20261011T220747Z-m-garment-bruce-2-identical-s2-6adb7e31/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:49.394909+00:00 | `20261011T220749Z-m-garment-bruce-2-upstream-default-s2-6a69d158` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9974835907499999 | [record](output/lbf/20261011T220749Z-m-garment-bruce-2-upstream-default-s2-6a69d158/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:51.703642+00:00 | `20261011T220751Z-m-garment-bruce-3-identical-s0-bad7acca` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | invalid; independent material none | [record](output/lbf/20261011T220751Z-m-garment-bruce-3-identical-s0-bad7acca/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:54.703420+00:00 | `20261011T220754Z-m-garment-bruce-3-upstream-default-s0-74fc0d1b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.57284825 | [record](output/lbf/20261011T220754Z-m-garment-bruce-3-upstream-default-s0-74fc0d1b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:07:57.372265+00:00 | `20261011T220757Z-m-garment-bruce-3-identical-s1-f971bb1a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.5643151666666666 | [record](output/lbf/20261011T220757Z-m-garment-bruce-3-identical-s1-f971bb1a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:00.393559+00:00 | `20261011T220800Z-m-garment-bruce-3-upstream-default-s1-caa523f1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.5660163501666668 | [record](output/lbf/20261011T220800Z-m-garment-bruce-3-upstream-default-s1-caa523f1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:03.436184+00:00 | `20261011T220803Z-m-garment-bruce-3-identical-s2-c155f1af` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | invalid; independent material none | [record](output/lbf/20261011T220803Z-m-garment-bruce-3-identical-s2-c155f1af/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:06.652693+00:00 | `20261011T220806Z-m-garment-bruce-3-upstream-default-s2-c3f46bab` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.5638791668333332 | [record](output/lbf/20261011T220806Z-m-garment-bruce-3-upstream-default-s2-c3f46bab/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:16.217145+00:00 | `20261011T220816Z-m-garment-teagan-1-identical-s0-d8f48f68` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 0.9922504243333333 | [record](output/lbf/20261011T220816Z-m-garment-teagan-1-identical-s0-d8f48f68/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:17.633986+00:00 | `20261011T220817Z-m-garment-teagan-1-upstream-default-s0-e26583f5` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.9998894246666667 | [record](output/lbf/20261011T220817Z-m-garment-teagan-1-upstream-default-s0-e26583f5/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:19.556584+00:00 | `20261011T220819Z-m-garment-teagan-1-identical-s1-c09f7f9d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 0.9999410663333332 | [record](output/lbf/20261011T220819Z-m-garment-teagan-1-identical-s1-c09f7f9d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:21.517908+00:00 | `20261011T220821Z-m-garment-teagan-1-upstream-default-s1-7a84a088` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.999921033 | [record](output/lbf/20261011T220821Z-m-garment-teagan-1-upstream-default-s1-7a84a088/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:23.440221+00:00 | `20261011T220823Z-m-garment-teagan-1-identical-s2-8ad8be12` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 0.9998439246666667 | [record](output/lbf/20261011T220823Z-m-garment-teagan-1-identical-s2-8ad8be12/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:25.341981+00:00 | `20261011T220825Z-m-garment-teagan-1-upstream-default-s2-2a4bbca6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 0.999975091 | [record](output/lbf/20261011T220825Z-m-garment-teagan-1-upstream-default-s2-2a4bbca6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:28.096599+00:00 | SVGnest `m-garment-bruce-1` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T220721Z-fbcbf264/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:08:27.395248+00:00 | `20261011T220827Z-m-garment-teagan-2-identical-s0-dbb57138` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 1.9998064302500003 | [record](output/lbf/20261011T220827Z-m-garment-teagan-2-identical-s0-dbb57138/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:30.377050+00:00 | current Sparrow `b-mao-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220727Z-67cc3443/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:08:30.054854+00:00 | `20261011T220830Z-m-garment-teagan-2-upstream-default-s0-a1685fe9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.99992575525 | [record](output/lbf/20261011T220830Z-m-garment-teagan-2-upstream-default-s0-a1685fe9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:31.965883+00:00 | `20261011T220831Z-m-garment-teagan-2-identical-s1-2a53ddeb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 1.9935135805000002 | [record](output/lbf/20261011T220831Z-m-garment-teagan-2-identical-s1-2a53ddeb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:34.600856+00:00 | `20261011T220834Z-m-garment-teagan-2-upstream-default-s1-e254320e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9950648080000002 | [record](output/lbf/20261011T220834Z-m-garment-teagan-2-upstream-default-s1-e254320e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:36.501349+00:00 | current Sparrow `s-albano-strip` seed 1, 60s, identical, axis x | valid | score 9865.40625 | [record](output/sparrow-benchmark/20261011T220733Z-cbff645c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:08:37.213769+00:00 | `20261011T220837Z-m-garment-teagan-2-identical-s2-97f0370b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 1.9999535302499998 | [record](output/lbf/20261011T220837Z-m-garment-teagan-2-identical-s2-97f0370b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:39.842971+00:00 | `20261011T220839Z-m-garment-teagan-2-upstream-default-s2-5ef0c2f3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 1.9998926305 | [record](output/lbf/20261011T220839Z-m-garment-teagan-2-upstream-default-s2-5ef0c2f3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:43.939819+00:00 | deepnest-next `m-mechanical-small-brackets` seed 0, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261011T220732Z-2ddb572a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:08:42.184040+00:00 | `20261011T220842Z-m-garment-teagan-2-identical-s0-30d5be5c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | valid; independent material 1.9998064302500003 | [record](output/lbf/20261011T220842Z-m-garment-teagan-2-identical-s0-30d5be5c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:44.677623+00:00 | `20261011T220844Z-m-garment-teagan-2-upstream-default-s0-11b8df01` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | valid; independent material 1.99992575525 | [record](output/lbf/20261011T220844Z-m-garment-teagan-2-upstream-default-s0-11b8df01/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:47.094796+00:00 | `20261011T220847Z-m-garment-teagan-2-identical-s1-2ea7b78c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | valid; independent material 1.9935135805000002 | [record](output/lbf/20261011T220847Z-m-garment-teagan-2-identical-s1-2ea7b78c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:49.860494+00:00 | `20261011T220849Z-m-garment-teagan-2-upstream-default-s1-0fe76695` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | valid; independent material 1.9950648080000002 | [record](output/lbf/20261011T220849Z-m-garment-teagan-2-upstream-default-s1-0fe76695/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:52.307932+00:00 | deepnest-next `m-public-gear-1` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T220844Z-f0e038fa/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:08:51.347823+00:00 | `20261011T220851Z-m-garment-teagan-2-identical-s2-a90abd1b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | valid; independent material 1.9999535302499998 | [record](output/lbf/20261011T220851Z-m-garment-teagan-2-identical-s2-a90abd1b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:53.612109+00:00 | `20261011T220853Z-m-garment-teagan-2-upstream-default-s2-6cb4b540` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | valid; independent material 1.9998926305 | [record](output/lbf/20261011T220853Z-m-garment-teagan-2-upstream-default-s2-6cb4b540/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:55.815101+00:00 | `20261011T220855Z-m-garment-teagan-3-identical-s0-c4c0a5dd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | valid; independent material 4.982509403000001 | [record](output/lbf/20261011T220855Z-m-garment-teagan-3-identical-s0-c4c0a5dd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:08:59.758996+00:00 | deepnest-next `m-public-gear-2` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T220852Z-1e57677f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:09:07.064949+00:00 | `20261011T220907Z-m-garment-teagan-3-upstream-default-s0-e57cadd7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.982122569666667 | [record](output/lbf/20261011T220907Z-m-garment-teagan-3-upstream-default-s0-e57cadd7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:09.967178+00:00 | `20261011T220909Z-m-garment-teagan-3-identical-s1-ee295ff9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | valid; independent material 4.999813548666666 | [record](output/lbf/20261011T220909Z-m-garment-teagan-3-identical-s1-ee295ff9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:12.938959+00:00 | `20261011T220912Z-m-garment-teagan-3-upstream-default-s1-ed1cb0a2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.999861519666667 | [record](output/lbf/20261011T220912Z-m-garment-teagan-3-upstream-default-s1-ed1cb0a2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:15.465905+00:00 | `20261011T220915Z-m-garment-teagan-3-identical-s2-8a8659ac` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | valid; independent material 4.9995178319999996 | [record](output/lbf/20261011T220915Z-m-garment-teagan-3-identical-s2-8a8659ac/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:18.443381+00:00 | `20261011T220918Z-m-garment-teagan-3-upstream-default-s2-a42a1ec3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | valid; independent material 4.967495569666667 | [record](output/lbf/20261011T220918Z-m-garment-teagan-3-upstream-default-s2-a42a1ec3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:20.817263+00:00 | `20261011T220920Z-m-mechanical-batch-1000-identical-s0-abb99f07` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220920Z-m-mechanical-batch-1000-identical-s0-abb99f07/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:21.164920+00:00 | `20261011T220921Z-m-mechanical-batch-1000-upstream-default-s0-fffedb7d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220921Z-m-mechanical-batch-1000-upstream-default-s0-fffedb7d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:21.457970+00:00 | `20261011T220921Z-m-mechanical-batch-1000-identical-s1-3c5bd07c` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220921Z-m-mechanical-batch-1000-identical-s1-3c5bd07c/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:21.776153+00:00 | `20261011T220921Z-m-mechanical-batch-1000-upstream-default-s1-f9bcc7da` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220921Z-m-mechanical-batch-1000-upstream-default-s1-f9bcc7da/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:22.358589+00:00 | `20261011T220922Z-m-mechanical-batch-1000-identical-s2-fc2f5924` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220922Z-m-mechanical-batch-1000-identical-s2-fc2f5924/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:22.623292+00:00 | `20261011T220922Z-m-mechanical-batch-1000-upstream-default-s2-07023d51` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220922Z-m-mechanical-batch-1000-upstream-default-s2-07023d51/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:22.913330+00:00 | `20261011T220922Z-m-mechanical-cog-washers-identical-s0-2b4bcab7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220922Z-m-mechanical-cog-washers-identical-s0-2b4bcab7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:23.239321+00:00 | `20261011T220923Z-m-mechanical-cog-washers-upstream-default-s0-80c7c49d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220923Z-m-mechanical-cog-washers-upstream-default-s0-80c7c49d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:23.522491+00:00 | `20261011T220923Z-m-mechanical-cog-washers-identical-s1-e4cf8899` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220923Z-m-mechanical-cog-washers-identical-s1-e4cf8899/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:23.849682+00:00 | `20261011T220923Z-m-mechanical-cog-washers-upstream-default-s1-d9d85f32` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220923Z-m-mechanical-cog-washers-upstream-default-s1-d9d85f32/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:24.136641+00:00 | `20261011T220924Z-m-mechanical-cog-washers-identical-s2-d98c054a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220924Z-m-mechanical-cog-washers-identical-s2-d98c054a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:24.413066+00:00 | `20261011T220924Z-m-mechanical-cog-washers-upstream-default-s2-f65400e7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220924Z-m-mechanical-cog-washers-upstream-default-s2-f65400e7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:24.693093+00:00 | `20261011T220924Z-m-mechanical-defective-stock-identical-s0-3c9f1cef` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220924Z-m-mechanical-defective-stock-identical-s0-3c9f1cef/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:25.065181+00:00 | `20261011T220925Z-m-mechanical-defective-stock-upstream-default-s0-6841ba27` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220925Z-m-mechanical-defective-stock-upstream-default-s0-6841ba27/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:25.439653+00:00 | `20261011T220925Z-m-mechanical-defective-stock-identical-s1-96cdf4ce` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220925Z-m-mechanical-defective-stock-identical-s1-96cdf4ce/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:25.699304+00:00 | `20261011T220925Z-m-mechanical-defective-stock-upstream-default-s1-9ba0a6f0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220925Z-m-mechanical-defective-stock-upstream-default-s1-9ba0a6f0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:25.946630+00:00 | `20261011T220925Z-m-mechanical-defective-stock-identical-s2-1be35706` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220925Z-m-mechanical-defective-stock-identical-s2-1be35706/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:33.035684+00:00 | current Sparrow `b-mao-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T220830Z-bab3b1b6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:09:34.126890+00:00 | `20261011T220934Z-m-mechanical-defective-stock-upstream-default-s2-cd97fc3d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220934Z-m-mechanical-defective-stock-upstream-default-s2-cd97fc3d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:34.751986+00:00 | `20261011T220934Z-m-mechanical-defective-stock-identical-s0-5cb2aa70` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220934Z-m-mechanical-defective-stock-identical-s0-5cb2aa70/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:35.026077+00:00 | `20261011T220935Z-m-mechanical-defective-stock-upstream-default-s0-7926b10d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220935Z-m-mechanical-defective-stock-upstream-default-s0-7926b10d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:35.413179+00:00 | `20261011T220935Z-m-mechanical-defective-stock-identical-s1-d781f3af` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220935Z-m-mechanical-defective-stock-identical-s1-d781f3af/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:35.730618+00:00 | `20261011T220935Z-m-mechanical-defective-stock-upstream-default-s1-b5dd9e68` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220935Z-m-mechanical-defective-stock-upstream-default-s1-b5dd9e68/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:36.133204+00:00 | `20261011T220936Z-m-mechanical-defective-stock-identical-s2-71e71fa4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220936Z-m-mechanical-defective-stock-identical-s2-71e71fa4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:36.544093+00:00 | SVGnest `m-garment-bruce-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T220828Z-c82211bf/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:09:36.753793+00:00 | `20261011T220936Z-m-mechanical-defective-stock-upstream-default-s2-f5571334` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220936Z-m-mechanical-defective-stock-upstream-default-s2-f5571334/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:37.615511+00:00 | `20261011T220937Z-m-mechanical-frame-inserts-identical-s0-12ff9350` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220937Z-m-mechanical-frame-inserts-identical-s0-12ff9350/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:37.916020+00:00 | `20261011T220937Z-m-mechanical-frame-inserts-upstream-default-s0-ea90c55d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220937Z-m-mechanical-frame-inserts-upstream-default-s0-ea90c55d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:38.343771+00:00 | `20261011T220938Z-m-mechanical-frame-inserts-identical-s1-c67b310e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220938Z-m-mechanical-frame-inserts-identical-s1-c67b310e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:38.646871+00:00 | `20261011T220938Z-m-mechanical-frame-inserts-upstream-default-s1-f91b1fce` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220938Z-m-mechanical-frame-inserts-upstream-default-s1-f91b1fce/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:38.955671+00:00 | `20261011T220938Z-m-mechanical-frame-inserts-identical-s2-8bd88d52` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220938Z-m-mechanical-frame-inserts-identical-s2-8bd88d52/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:39.326668+00:00 | `20261011T220939Z-m-mechanical-frame-inserts-upstream-default-s2-c1a90acd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220939Z-m-mechanical-frame-inserts-upstream-default-s2-c1a90acd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:39.648894+00:00 | current Sparrow `s-blaz1-strip` seed 1, 60s, identical, axis x | valid | score 26.661903381347656 | [record](output/sparrow-benchmark/20261011T220836Z-22e32fd6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:09:39.705635+00:00 | `20261011T220939Z-m-mechanical-large-plates-identical-s0-55083c9b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220939Z-m-mechanical-large-plates-identical-s0-55083c9b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:40.054491+00:00 | `20261011T220940Z-m-mechanical-large-plates-upstream-default-s0-e4d4652a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220940Z-m-mechanical-large-plates-upstream-default-s0-e4d4652a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:40.372211+00:00 | `20261011T220940Z-m-mechanical-large-plates-identical-s1-175138db` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220940Z-m-mechanical-large-plates-identical-s1-175138db/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:41.160923+00:00 | `20261011T220941Z-m-mechanical-large-plates-upstream-default-s1-b3c704dd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220941Z-m-mechanical-large-plates-upstream-default-s1-b3c704dd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:41.574283+00:00 | `20261011T220941Z-m-mechanical-large-plates-identical-s2-4872d3b3` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220941Z-m-mechanical-large-plates-identical-s2-4872d3b3/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:42.091016+00:00 | `20261011T220942Z-m-mechanical-large-plates-upstream-default-s2-2132e9ae` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220942Z-m-mechanical-large-plates-upstream-default-s2-2132e9ae/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:50.570503+00:00 | `20261011T220950Z-m-mechanical-mixed-stock-identical-s0-3ee54462` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220950Z-m-mechanical-mixed-stock-identical-s0-3ee54462/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:51.066502+00:00 | `20261011T220951Z-m-mechanical-mixed-stock-upstream-default-s0-9ad57626` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220951Z-m-mechanical-mixed-stock-upstream-default-s0-9ad57626/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:52.071964+00:00 | `20261011T220952Z-m-mechanical-mixed-stock-identical-s1-fae29b82` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220952Z-m-mechanical-mixed-stock-identical-s1-fae29b82/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:52.632570+00:00 | `20261011T220952Z-m-mechanical-mixed-stock-upstream-default-s1-d95a37f2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220952Z-m-mechanical-mixed-stock-upstream-default-s1-d95a37f2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:53.829362+00:00 | `20261011T220953Z-m-mechanical-mixed-stock-identical-s2-5c998b57` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220953Z-m-mechanical-mixed-stock-identical-s2-5c998b57/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:54.779864+00:00 | `20261011T220954Z-m-mechanical-mixed-stock-upstream-default-s2-bcc77295` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220954Z-m-mechanical-mixed-stock-upstream-default-s2-bcc77295/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:55.669635+00:00 | `20261011T220955Z-m-mechanical-mixed-stock-identical-s0-f271e742` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220955Z-m-mechanical-mixed-stock-identical-s0-f271e742/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:56.760824+00:00 | `20261011T220956Z-m-mechanical-mixed-stock-upstream-default-s0-33c06049` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220956Z-m-mechanical-mixed-stock-upstream-default-s0-33c06049/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:57.500465+00:00 | `20261011T220957Z-m-mechanical-mixed-stock-identical-s1-11d7d40b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220957Z-m-mechanical-mixed-stock-identical-s1-11d7d40b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:58.545151+00:00 | current Sparrow `s-albano-strip` seed 2, 60s, identical, axis x | valid | score 9889.6826171875 | [record](output/sparrow-benchmark/20261011T220855Z-ba6fbf73/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:09:58.480385+00:00 | `20261011T220958Z-m-mechanical-mixed-stock-upstream-default-s1-e06312cb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220958Z-m-mechanical-mixed-stock-upstream-default-s1-e06312cb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:58.888703+00:00 | `20261011T220958Z-m-mechanical-mixed-stock-identical-s2-a1d4a4af` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T220958Z-m-mechanical-mixed-stock-identical-s2-a1d4a4af/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:09:59.421321+00:00 | `20261011T220959Z-m-mechanical-mixed-stock-upstream-default-s2-80e33126` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 300s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T220959Z-m-mechanical-mixed-stock-upstream-default-s2-80e33126/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:00.144071+00:00 | `20261011T221000Z-m-mechanical-mounting-kit-identical-s0-9ab19874` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221000Z-m-mechanical-mounting-kit-identical-s0-9ab19874/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:00.464498+00:00 | `20261011T221000Z-m-mechanical-mounting-kit-upstream-default-s0-2ca1cf44` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221000Z-m-mechanical-mounting-kit-upstream-default-s0-2ca1cf44/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:01.268743+00:00 | `20261011T221001Z-m-mechanical-mounting-kit-identical-s1-5152262a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221001Z-m-mechanical-mounting-kit-identical-s1-5152262a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:02.316171+00:00 | `20261011T221002Z-m-mechanical-mounting-kit-upstream-default-s1-f57b22bb` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221002Z-m-mechanical-mounting-kit-upstream-default-s1-f57b22bb/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:03.477099+00:00 | `20261011T221003Z-m-mechanical-mounting-kit-identical-s2-6af68d0b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221003Z-m-mechanical-mounting-kit-identical-s2-6af68d0b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:04.619026+00:00 | `20261011T221004Z-m-mechanical-mounting-kit-upstream-default-s2-7f9af948` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221004Z-m-mechanical-mounting-kit-upstream-default-s2-7f9af948/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:05.822236+00:00 | `20261011T221005Z-m-mechanical-panel-hardware-identical-s0-701d3848` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221005Z-m-mechanical-panel-hardware-identical-s0-701d3848/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:14.781561+00:00 | `20261011T221014Z-m-mechanical-panel-hardware-upstream-default-s0-a8ade90b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221014Z-m-mechanical-panel-hardware-upstream-default-s0-a8ade90b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:16.148679+00:00 | `20261011T221016Z-m-mechanical-panel-hardware-identical-s1-d4b37c9d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221016Z-m-mechanical-panel-hardware-identical-s1-d4b37c9d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:17.531348+00:00 | `20261011T221017Z-m-mechanical-panel-hardware-upstream-default-s1-abd96c2d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221017Z-m-mechanical-panel-hardware-upstream-default-s1-abd96c2d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:18.639556+00:00 | `20261011T221018Z-m-mechanical-panel-hardware-identical-s2-42bee2d6` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221018Z-m-mechanical-panel-hardware-identical-s2-42bee2d6/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:19.965647+00:00 | `20261011T221019Z-m-mechanical-panel-hardware-upstream-default-s2-d8e3f402` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221019Z-m-mechanical-panel-hardware-upstream-default-s2-d8e3f402/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:20.641818+00:00 | `20261011T221020Z-m-mechanical-remnant-kit-identical-s0-4a506d4a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221020Z-m-mechanical-remnant-kit-identical-s0-4a506d4a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:21.967119+00:00 | `20261011T221021Z-m-mechanical-remnant-kit-upstream-default-s0-8837243d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221021Z-m-mechanical-remnant-kit-upstream-default-s0-8837243d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:23.228102+00:00 | `20261011T221023Z-m-mechanical-remnant-kit-identical-s1-5a623181` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221023Z-m-mechanical-remnant-kit-identical-s1-5a623181/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:24.531405+00:00 | `20261011T221024Z-m-mechanical-remnant-kit-upstream-default-s1-93716307` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221024Z-m-mechanical-remnant-kit-upstream-default-s1-93716307/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:25.938457+00:00 | `20261011T221025Z-m-mechanical-remnant-kit-identical-s2-f07da358` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221025Z-m-mechanical-remnant-kit-identical-s2-f07da358/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:27.242670+00:00 | `20261011T221027Z-m-mechanical-remnant-kit-upstream-default-s2-05fb2044` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221027Z-m-mechanical-remnant-kit-upstream-default-s2-05fb2044/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:28.593119+00:00 | `20261011T221028Z-m-mechanical-small-brackets-identical-s0-ab79002f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221028Z-m-mechanical-small-brackets-identical-s0-ab79002f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:29.816062+00:00 | `20261011T221029Z-m-mechanical-small-brackets-upstream-default-s0-44bd17b9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221029Z-m-mechanical-small-brackets-upstream-default-s0-44bd17b9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:31.057805+00:00 | `20261011T221031Z-m-mechanical-small-brackets-identical-s1-d8382b98` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221031Z-m-mechanical-small-brackets-identical-s1-d8382b98/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:32.415509+00:00 | `20261011T221032Z-m-mechanical-small-brackets-upstream-default-s1-55c9a177` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221032Z-m-mechanical-small-brackets-upstream-default-s1-55c9a177/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:33.140568+00:00 | `20261011T221033Z-m-mechanical-small-brackets-identical-s2-24c0be0e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221033Z-m-mechanical-small-brackets-identical-s2-24c0be0e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:33.868389+00:00 | `20261011T221033Z-m-mechanical-small-brackets-upstream-default-s2-820cb194` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221033Z-m-mechanical-small-brackets-upstream-default-s2-820cb194/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:35.299022+00:00 | current Sparrow `b-mao-strip-sheet` seed 0, 60s, identical, axis y | valid | score 0.8074253215686273 | [record](output/sparrow-benchmark/20261011T220933Z-b0fcf2ca/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:10:35.355109+00:00 | `20261011T221035Z-m-public-gear-1-identical-s0-cb97d77d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221035Z-m-public-gear-1-identical-s0-cb97d77d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:36.822052+00:00 | `20261011T221036Z-m-public-gear-1-upstream-default-s0-31672228` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221036Z-m-public-gear-1-upstream-default-s0-31672228/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:38.019519+00:00 | `20261011T221038Z-m-public-gear-1-identical-s1-134cbb98` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221038Z-m-public-gear-1-identical-s1-134cbb98/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:39.297423+00:00 | `20261011T221039Z-m-public-gear-1-upstream-default-s1-a17a161d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221039Z-m-public-gear-1-upstream-default-s1-a17a161d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:40.788878+00:00 | `20261011T221040Z-m-public-gear-1-identical-s2-12249ea8` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221040Z-m-public-gear-1-identical-s2-12249ea8/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:41.756188+00:00 | current Sparrow `s-dagli-strip` seed 1, 60s, identical, axis x | valid | score 58.09028244018555 | [record](output/sparrow-benchmark/20261011T220939Z-2cec2fab/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:10:43.915993+00:00 | SVGnest `m-garment-bruce-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T220936Z-81ae93a2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:10:49.692783+00:00 | `20261011T221049Z-m-public-gear-1-upstream-default-s2-738bdee2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221049Z-m-public-gear-1-upstream-default-s2-738bdee2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:50.837344+00:00 | `20261011T221050Z-m-public-gear-2-identical-s0-53bcf68e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221050Z-m-public-gear-2-identical-s0-53bcf68e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:51.825635+00:00 | `20261011T221051Z-m-public-gear-2-upstream-default-s0-02b0c40a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221051Z-m-public-gear-2-upstream-default-s0-02b0c40a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:53.170105+00:00 | `20261011T221053Z-m-public-gear-2-identical-s1-9d6d4ca7` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221053Z-m-public-gear-2-identical-s1-9d6d4ca7/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:54.318514+00:00 | `20261011T221054Z-m-public-gear-2-upstream-default-s1-e330245b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221054Z-m-public-gear-2-upstream-default-s1-e330245b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:55.525038+00:00 | `20261011T221055Z-m-public-gear-2-identical-s2-cf5ed90e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221055Z-m-public-gear-2-identical-s2-cf5ed90e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:56.878399+00:00 | `20261011T221056Z-m-public-gear-2-upstream-default-s2-4e199a9b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221056Z-m-public-gear-2-upstream-default-s2-4e199a9b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:58.145102+00:00 | `20261011T221058Z-m-public-gear-3-identical-s0-152085f1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221058Z-m-public-gear-3-identical-s0-152085f1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:10:59.526384+00:00 | `20261011T221059Z-m-public-gear-3-upstream-default-s0-fe2a827f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221059Z-m-public-gear-3-upstream-default-s0-fe2a827f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:00.812139+00:00 | current Sparrow `s-blaz1-strip` seed 2, 60s, identical, axis x | valid | score 26.856674194335938 | [record](output/sparrow-benchmark/20261011T220958Z-2c83735c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:11:00.777736+00:00 | `20261011T221100Z-m-public-gear-3-identical-s1-3efad45e` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221100Z-m-public-gear-3-identical-s1-3efad45e/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:02.003434+00:00 | `20261011T221102Z-m-public-gear-3-upstream-default-s1-7e1e82a4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221102Z-m-public-gear-3-upstream-default-s1-7e1e82a4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:03.187835+00:00 | verified deepnest batch `20261011T220731Z-4c1f576b` | 0/3 valid | [table](benchmarks/results/deepnest-20261011T221103Z-e48b455f.md). Provisional; all failures retained.

- 2026-10-11T22:11:03.317574+00:00 | `20261011T221103Z-m-public-gear-3-identical-s2-285a924a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221103Z-m-public-gear-3-identical-s2-285a924a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:04.724261+00:00 | `20261011T221104Z-m-public-gear-3-upstream-default-s2-4ad761dd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221104Z-m-public-gear-3-upstream-default-s2-4ad761dd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:06.129716+00:00 | `20261011T221106Z-m-public-gear-4-identical-s0-f3ab7953` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221106Z-m-public-gear-4-identical-s0-f3ab7953/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:07.536118+00:00 | `20261011T221107Z-m-public-gear-4-upstream-default-s0-3288e7a4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221107Z-m-public-gear-4-upstream-default-s0-3288e7a4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:08.688731+00:00 | `20261011T221108Z-m-public-gear-4-identical-s1-c17f58f4` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221108Z-m-public-gear-4-identical-s1-c17f58f4/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:09.844372+00:00 | `20261011T221109Z-m-public-gear-4-upstream-default-s1-6d60e8ea` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221109Z-m-public-gear-4-upstream-default-s1-6d60e8ea/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:11.047198+00:00 | `20261011T221111Z-m-public-gear-4-identical-s2-b737a21d` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221111Z-m-public-gear-4-identical-s2-b737a21d/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:12.436031+00:00 | `20261011T221112Z-m-public-gear-4-upstream-default-s2-0dd31356` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221112Z-m-public-gear-4-upstream-default-s2-0dd31356/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:13.796401+00:00 | `20261011T221113Z-m-sign-1-identical-s0-bcf18a69` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221113Z-m-sign-1-identical-s0-bcf18a69/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:15.146266+00:00 | `20261011T221115Z-m-sign-1-upstream-default-s0-0ba585e0` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221115Z-m-sign-1-upstream-default-s0-0ba585e0/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:16.476793+00:00 | `20261011T221116Z-m-sign-1-identical-s1-1effa91a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221116Z-m-sign-1-identical-s1-1effa91a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:25.533605+00:00 | `20261011T221125Z-m-sign-1-upstream-default-s1-08413478` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221125Z-m-sign-1-upstream-default-s1-08413478/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:26.846153+00:00 | `20261011T221126Z-m-sign-1-identical-s2-e3651a88` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221126Z-m-sign-1-identical-s2-e3651a88/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:27.889841+00:00 | `20261011T221127Z-m-sign-1-upstream-default-s2-c6441d51` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221127Z-m-sign-1-upstream-default-s2-c6441d51/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:29.286302+00:00 | `20261011T221129Z-m-sign-2-identical-s0-29ed92f2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221129Z-m-sign-2-identical-s0-29ed92f2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:30.724857+00:00 | `20261011T221130Z-m-sign-2-upstream-default-s0-2cbecf2a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221130Z-m-sign-2-upstream-default-s0-2cbecf2a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:32.038869+00:00 | `20261011T221132Z-m-sign-2-identical-s1-64c9d6ee` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221132Z-m-sign-2-identical-s1-64c9d6ee/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:33.424503+00:00 | `20261011T221133Z-m-sign-2-upstream-default-s1-451f77ba` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221133Z-m-sign-2-upstream-default-s1-451f77ba/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:34.497507+00:00 | `20261011T221134Z-m-sign-2-identical-s2-d12fd32f` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221134Z-m-sign-2-identical-s2-d12fd32f/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:35.636358+00:00 | `20261011T221135Z-m-sign-2-upstream-default-s2-415d6f01` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221135Z-m-sign-2-upstream-default-s2-415d6f01/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:37.052794+00:00 | `20261011T221137Z-m-sign-3-identical-s0-1101c9a1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221137Z-m-sign-3-identical-s0-1101c9a1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:38.616332+00:00 | current Sparrow `b-marques-strip-sheet` seed 0, 60s, identical, axis y | valid | score 0.9995147403846154 | [record](output/sparrow-benchmark/20261011T221035Z-b869bf76/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:11:38.241970+00:00 | `20261011T221138Z-m-sign-3-upstream-default-s0-da92f0e9` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221138Z-m-sign-3-upstream-default-s0-da92f0e9/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:39.582907+00:00 | `20261011T221139Z-m-sign-3-identical-s1-8762ca59` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221139Z-m-sign-3-identical-s1-8762ca59/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:40.996324+00:00 | `20261011T221140Z-m-sign-3-upstream-default-s1-5903962a` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221140Z-m-sign-3-upstream-default-s1-5903962a/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:42.424871+00:00 | `20261011T221142Z-m-sign-3-identical-s2-ea09c944` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221142Z-m-sign-3-identical-s2-ea09c944/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:43.674912+00:00 | `20261011T221143Z-m-sign-3-upstream-default-s2-d4aa77fd` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221143Z-m-sign-3-upstream-default-s2-d4aa77fd/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:44.923975+00:00 | current Sparrow `s-fu-strip` seed 1, 60s, identical, axis x | valid | score 31.615476608276367 | [record](output/sparrow-benchmark/20261011T221041Z-1d9ee82e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:11:44.796350+00:00 | `20261011T221144Z-m-sign-4-identical-s0-726f0a33` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221144Z-m-sign-4-identical-s0-726f0a33/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:46.165383+00:00 | `20261011T221146Z-m-sign-4-upstream-default-s0-2a910433` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 0, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221146Z-m-sign-4-upstream-default-s0-2a910433/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:47.167278+00:00 | `20261011T221147Z-m-sign-4-identical-s1-bdafa100` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221147Z-m-sign-4-identical-s1-bdafa100/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:48.504873+00:00 | `20261011T221148Z-m-sign-4-upstream-default-s1-e610559b` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 1, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221148Z-m-sign-4-upstream-default-s1-e610559b/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:49.905326+00:00 | `20261011T221149Z-m-sign-4-identical-s2-c9b145c2` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, identical | unsupported; independent material none | [record](output/lbf/20261011T221149Z-m-sign-4-identical-s2-c9b145c2/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:11:51.486435+00:00 | SVGnest `m-garment-teagan-1` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T221044Z-71b031ee/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:11:50.958419+00:00 | `20261011T221150Z-m-sign-4-upstream-default-s2-7a49daf1` | LBF `9e00fd867be0fc493002aea68a1c6613d5b833d6` | Nestbolt `1846f866c34160c7de70bbec7472bc84dca25659` (dirty=True) | seed 2, 60s limit, one pass/one worker, upstream-default | unsupported; independent material none | [record](output/lbf/20261011T221150Z-m-sign-4-upstream-default-s2-7a49daf1/run.json). Provisional M1 baseline, no quality-gate claim.

- 2026-10-11T22:12:02.665463+00:00 | deepnest-next `m-public-gear-1` seed 0, 5s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261011T221155Z-7e3badab/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:12:03.720313+00:00 | current Sparrow `s-dagli-strip` seed 2, 60s, identical, axis x | valid | score 58.508819580078125 | [record](output/sparrow-benchmark/20261011T221100Z-ccb9fb2d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:12:42.320302+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221138Z-b1329049/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:12:47.954746+00:00 | current Sparrow `s-jakobs1-strip` seed 1, 60s, identical, axis x | valid | score 11.017838478088379 | [record](output/sparrow-benchmark/20261011T221144Z-53295ae8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:12:59.199169+00:00 | SVGnest `m-garment-teagan-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T221151Z-197fc9f4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:13:06.591454+00:00 | current Sparrow `s-fu-strip` seed 2, 60s, identical, axis x | valid | score 31.924409866333008 | [record](output/sparrow-benchmark/20261011T221203Z-334c4bad/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:13:45.336116+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221242Z-d05b0140/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:13:50.876647+00:00 | current Sparrow `s-jakobs2-strip` seed 1, 60s, identical, axis x | valid | score 24.005708694458008 | [record](output/sparrow-benchmark/20261011T221247Z-38221186/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:13:59.704836+00:00 | deepnest-next `m-public-gear-1` seed 0, 5s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T221327Z-af9fbe0d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:14:07.815159+00:00 | SVGnest `m-garment-teagan-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T221259Z-d3ae8c9d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:14:09.363137+00:00 | current Sparrow `s-jakobs1-strip` seed 2, 60s, identical, axis x | valid | score 11.348267555236816 | [record](output/sparrow-benchmark/20261011T221306Z-09a3f45a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:14:47.802964+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221345Z-ec072835/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:14:53.571173+00:00 | current Sparrow `s-mao-strip` seed 1, 60s, identical, axis x | valid | score 1780.17919921875 | [record](output/sparrow-benchmark/20261011T221350Z-1ba6681e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:15:10.789723+00:00 | full development LBF queue audited: 450/450 attempts; 283 valid, 5 invalid, 162 unsupported. [Table](benchmarks/results/comparison-session-20261011T221209Z-ce35672e.md). Both configurations, seeds 0/1/2, frozen 60/300 s coverage; no held-out runs. Competitor matrix and M1 gap remain pending.

- 2026-10-11T22:15:12.153515+00:00 | current Sparrow `s-jakobs2-strip` seed 2, 60s, identical, axis x | valid | score 24.00525665283203 | [record](output/sparrow-benchmark/20261011T221409Z-314be9de/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:15:40.075747+00:00 | verified svgnest batch `20261011T220721Z-787a8edf` | 0/6 valid | [table](benchmarks/results/svgnest-20261011T221540Z-937f797b.md). Provisional; all failures retained.

- 2026-10-11T22:15:50.968765+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221447Z-051075a3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:15:53.262717+00:00 | SVGnest `m-public-gear-1` seed 0, 5s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T221540Z-6134ce39/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:15:55.756079+00:00 | current Sparrow `s-marques-strip` seed 1, 60s, identical, axis x | valid | score 77.03972625732422 | [record](output/sparrow-benchmark/20261011T221453Z-4bec5fef/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:16:14.609683+00:00 | current Sparrow `s-mao-strip` seed 2, 60s, identical, axis x | valid | score 1767.8349609375 | [record](output/sparrow-benchmark/20261011T221512Z-6d080858/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:16:52.926295+00:00 | deepnest-next `m-public-gear-1` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T221509Z-58495d32/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:16:53.718060+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221550Z-e81939e7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:16:58.417511+00:00 | current Sparrow `s-shapes0-strip` seed 1, 60s, identical, axis x | valid | score 61.53407669067383 | [record](output/sparrow-benchmark/20261011T221555Z-7ff7e89c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:17:17.303264+00:00 | current Sparrow `s-marques-strip` seed 2, 60s, identical, axis x | valid | score 77.70464324951172 | [record](output/sparrow-benchmark/20261011T221614Z-363e3203/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:17:22.596792+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T221711Z-70c53dfb/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:17:56.417318+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221653Z-519e2feb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:18:01.451977+00:00 | current Sparrow `s-shapes1-strip` seed 1, 60s, identical, axis x | valid | score 56.005836486816406 | [record](output/sparrow-benchmark/20261011T221658Z-efbb9479/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:18:19.780081+00:00 | current Sparrow `s-shapes0-strip` seed 2, 60s, identical, axis x | valid | score 61.037818908691406 | [record](output/sparrow-benchmark/20261011T221717Z-fcaa587b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:18:28.677265+00:00 | deepnest-next `m-public-gear-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T221653Z-0b143231/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:18:59.631356+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T221756Z-70e83d99/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:19:04.078727+00:00 | current Sparrow `s-shirts-strip` seed 1, 60s, identical, axis x | valid | score 61.74829864501953 | [record](output/sparrow-benchmark/20261011T221801Z-17b1cb79/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:19:22.655226+00:00 | current Sparrow `s-shapes1-strip` seed 2, 60s, identical, axis x | valid | score 56.00271224975586 | [record](output/sparrow-benchmark/20261011T221819Z-6b01521e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:20:04.361549+00:00 | deepnest-next `m-public-gear-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T221829Z-d17fde96/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:20:06.611374+00:00 | current Sparrow `s-swim-strip` seed 1, 60s, identical, axis x | valid | score 6007.15966796875 | [record](output/sparrow-benchmark/20261011T221904Z-633f231b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:20:24.853529+00:00 | current Sparrow `s-shirts-strip` seed 2, 60s, identical, axis x | valid | score 61.787559509277344 | [record](output/sparrow-benchmark/20261011T221922Z-17f612d4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:21:09.402956+00:00 | current Sparrow `s-trousers-strip` seed 1, 60s, identical, axis x | valid | score 241.06053161621094 | [record](output/sparrow-benchmark/20261011T222006Z-5c536421/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:21:26.916219+00:00 | current Sparrow `s-swim-strip` seed 2, 60s, identical, axis x | valid | score 5960.81103515625 | [record](output/sparrow-benchmark/20261011T222024Z-a7b3d3dc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:21:48.056139+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T222138Z-3dc492de/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:22:01.132629+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 5s, identical, axis y | valid | material 3.7142857619047622 | [record](output/playwright/deepnest/20261011T222148Z-0a53e4bc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:22:23.106878+00:00 | verified deepnest batch `20261011T221509Z-7fea82e6` | 0/3 valid | [table](benchmarks/results/deepnest-20261011T222223Z-1d48b429.md). Provisional; all failures retained.

- 2026-10-11T22:22:23.829635+00:00 | verified sparrow batch `20261011T215353Z-818c5cfc` | 5/24 valid | [table](benchmarks/results/sparrow-20261011T222223Z-896e5940.md). Provisional; all failures retained.

- 2026-10-11T22:22:28.757208+00:00 | current Sparrow `s-trousers-strip` seed 2, 60s, identical, axis x | valid | score 240.72894287109375 | [record](output/sparrow-benchmark/20261011T222126Z-7699e63e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:24:32.062736+00:00 | SVGnest `m-mechanical-batch-1000` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T222319Z-4c9102a3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:24:35.068034+00:00 | SVGnest `b-albano-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 3.3564093236651282 | [record](output/playwright/svgnest/20261011T222330Z-0f324c6c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:24:44.522159+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T222342Z-ba950dbb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:25:09.679644+00:00 | deepnest-next `m-public-gear-4` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T222340Z-78a54553/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:25:19.063734+00:00 | deepnest-next `m-sign-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T222341Z-d2015338/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:25:38.046126+00:00 | SVGnest `m-mechanical-cog-washers` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T222432Z-171d6718/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:25:39.610168+00:00 | SVGnest `m-mechanical-defective-stock` seed 0, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261011T222538Z-9b76878d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:25:40.329635+00:00 | SVGnest `b-albano-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 4.107888376181059 | [record](output/playwright/svgnest/20261011T222435Z-64ab1322/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:25:46.551759+00:00 | current Sparrow `b-shirts-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T222444Z-08efcac0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:26:26.020482+00:00 | deepnest-next `m-sign-1` seed 0, 60s, identical, axis y | valid | material 0.8429885300000001 | [record](output/playwright/deepnest/20261011T222509Z-57ef4b99/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:26:45.535122+00:00 | SVGnest `b-albano-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 3.150204081632653 | [record](output/playwright/svgnest/20261011T222540Z-a358ca12/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:26:45.801413+00:00 | SVGnest `m-mechanical-frame-inserts` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T222539Z-4c73dde7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:26:48.723839+00:00 | current Sparrow `b-swim-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T222546Z-dffcbadf/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:27:22.995196+00:00 | deepnest-next `m-sign-4` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T222519Z-43c51e82/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:27:51.084679+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 18.533333333333335 | [record](output/playwright/svgnest/20261011T222645Z-9d135949/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:27:51.353744+00:00 | current Sparrow `b-swim-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T222648Z-19fcf898/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:27:51.901996+00:00 | SVGnest `m-mechanical-large-plates` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T222645Z-1b7c250f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:27:55.854856+00:00 | SVGnest `m-mechanical-mixed-stock` seed 0, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261011T222752Z-0e95d367/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:28:25.608159+00:00 | deepnest-next `m-sign-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261011T222626Z-03fb2561/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:28:55.942466+00:00 | current Sparrow `b-swim-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T222751Z-3853414d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:29:02.669668+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T222752Z-44e2333b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:29:09.764755+00:00 | SVGnest `m-mechanical-mounting-kit` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T222756Z-9a7e0ad5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:30:00.600428+00:00 | current Sparrow `b-trousers-nest-mb-free` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T222855Z-64651e59/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:30:03.852702+00:00 | verified deepnest batch `20261011T222339Z-775b99b8` | 1/3 valid | [table](benchmarks/results/deepnest-20261011T223003Z-90040a14.md). Provisional; all failures retained.

- 2026-10-11T22:30:04.564173+00:00 | verified deepnest batch `20261011T222340Z-440fa2a9` | 0/2 valid | [table](benchmarks/results/deepnest-20261011T223004Z-524a7709.md). Provisional; all failures retained.

- 2026-10-11T22:30:05.629833+00:00 | verified sparrow batch `20261011T220733Z-f086b2d2` | 13/13 valid | [table](benchmarks/results/sparrow-20261011T223005Z-53934dc4.md). Provisional; all failures retained.

- 2026-10-11T22:30:15.798177+00:00 | SVGnest `b-blaz1-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 3.6 | [record](output/playwright/svgnest/20261011T222903Z-920c07f1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:30:25.729392+00:00 | SVGnest `m-mechanical-panel-hardware` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T222911Z-8e77c117/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:30:30.725079+00:00 | verified sparrow batch `20261011T220855Z-47c37293` | 13/13 valid | [table](benchmarks/results/sparrow-20261011T223030Z-c7340997.md). Provisional; all failures retained.

- 2026-10-11T22:30:31.218293+00:00 | SVGnest `m-mechanical-remnant-kit` seed 0, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261011T223027Z-d3cd3438/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:31:05.603639+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T223000Z-6528e37e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:31:30.020880+00:00 | SVGnest `b-dagli-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.9833333333333333 | [record](output/playwright/svgnest/20261011T223017Z-d6ee1b27/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:31:41.124040+00:00 | SVGnest `m-mechanical-small-brackets` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T223032Z-6e270e88/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:07.514980+00:00 | current Sparrow `b-trousers-strip-sheet` seed 0, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261011T223105Z-2500fc7c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T22:32:34.583262+00:00 | SVGnest `b-fu-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 4.772303952380953 | [record](output/playwright/svgnest/20261011T223130Z-c4517d18/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:36.287457+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223234Z-fd9758a3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:37.948748+00:00 | SVGnest `b-fu-strip-sheet` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223236Z-5f4fd0f8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:40.005076+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223238Z-c55739d2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:42.055784+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223240Z-f3177f9a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:44.187615+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223242Z-be59d08b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:46.187650+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223244Z-c5959754/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:47.796703+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223246Z-ae780fc0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:47.943540+00:00 | SVGnest `m-public-gear-1` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T223141Z-2068eab4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:49.448906+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223247Z-e29d5a54/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:49.774311+00:00 | SVGnest `m-public-gear-2` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223248Z-b83af8fa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:51.171218+00:00 | SVGnest `b-mao-nest-mb-free` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223249Z-3a2ebadc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:51.919255+00:00 | SVGnest `m-public-gear-3` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223249Z-d51e3cd3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:52.752700+00:00 | SVGnest `b-mao-nest-mb-given` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223251Z-88663e55/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:53.822315+00:00 | SVGnest `m-public-gear-4` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223252Z-bd54b98b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:54.327867+00:00 | SVGnest `b-mao-strip-sheet` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223252Z-1be88579/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:55.523472+00:00 | SVGnest `m-sign-1` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223253Z-72852cf8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:55.942299+00:00 | SVGnest `b-marques-strip-sheet` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223254Z-a91ff4a2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:57.245831+00:00 | SVGnest `m-sign-2` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223255Z-b7cc0fc2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:57.619359+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223256Z-dd682e01/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:58.981801+00:00 | SVGnest `m-sign-3` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223257Z-7704f47a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:32:59.249935+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223257Z-f24c1628/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:33:00.722651+00:00 | SVGnest `m-sign-4` seed 0, 60s, identical, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223259Z-074342c4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:33:00.860345+00:00 | SVGnest `b-shapes0-strip-sheet` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223259Z-3b86ff4f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:33:02.538503+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/svgnest/20261011T223300Z-2cc925b4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:36:41.376835+00:00 | verified sparrow batch `20261011T222342Z-fb2950f8` | 0/8 valid | [table](benchmarks/results/sparrow-20261011T223641Z-17f5e9d7.md). Provisional; all failures retained.

- 2026-10-11T22:39:00.113818+00:00 | verified svgnest batch `20261011T222319Z-de2c2e3e` | 0/18 valid | [table](benchmarks/results/svgnest-20261011T223900Z-7cd19c3c.md). Provisional; all failures retained.

- 2026-10-11T22:39:01.093477+00:00 | verified svgnest batch `20261011T222330Z-0ea3e785` | 8/24 valid | [table](benchmarks/results/svgnest-20261011T223901Z-b53f39ec.md). Provisional; all failures retained.

- 2026-10-11T22:42:00Z | First Nestbolt constructor: 30/30 development maker layouts independently valid, seed 0, deterministic 64-sample quota. Median 0.4375 s, maximum 18.047 s; diagnostic timings, not G4. [Proof](benchmarks/results/construct-maker-20261011T223817Z-32654739.md).

- SVGnest batches 20261011T222319Z-de2c2e3e and 20261011T222330Z-0ea3e785 retained 7 and 16 harness build failures respectively after the product dependency manifest changed before its lock was updated. Those attempts never reached the competitor and must not count as competitor failures. The affected slots are rerunning after the batch was changed to retain one immutable checker executable and its source hashes.

- 2026-10-11T22:42:31.897795+00:00 | SVGnest `b-fu-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T224119Z-540402ed/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:42:38.730758+00:00 | SVGnest `m-public-gear-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224117Z-f072cc9a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:43:38.700131+00:00 | SVGnest `b-fu-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.4473684210526316 | [record](output/playwright/svgnest/20261011T224232Z-832f0e41/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:43:52.981640+00:00 | SVGnest `m-public-gear-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224238Z-5525f7d5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:44:45.585512+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 5.360843916666667 | [record](output/playwright/svgnest/20261011T224338Z-b4047f7e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:45:05.973528+00:00 | SVGnest `m-public-gear-4` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224353Z-f9f5b659/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:45:54.053809+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 0, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T224446Z-1bfa608c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:46:16.512572+00:00 | SVGnest `m-sign-1` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224506Z-bcbdbabc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:47:02.040352+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.8479166749999999 | [record](output/playwright/svgnest/20261011T224554Z-516030b0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:47:26.420768+00:00 | SVGnest `m-sign-2` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224616Z-4e99f7d6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:48:09.676599+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 4.588006625 | [record](output/playwright/svgnest/20261011T224702Z-aec1d9b3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:48:34.743142+00:00 | SVGnest `m-sign-3` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224727Z-8c520fbc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:49:16.183485+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.9166666666666665 | [record](output/playwright/svgnest/20261011T224810Z-11dac240/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:49:42.011342+00:00 | SVGnest `m-sign-4` seed 0, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261011T224834Z-96bc3f05/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:50:07.285264+00:00 | Nestbolt constructor v2: 30/30 development maker layouts independently valid; all use less material than v1, median reduction 20.061918%. Diagnostic median time 0.555 s, max 42.937 s; speed remains work. [Proof](benchmarks/results/construct-maker-20261011T224552Z-f0cf58b4.md). Full local check passed 49 workspace tests, 4 stock-helper tests, 72 Python tests, both WASM builds and all schema/source/notices checks.

- 2026-10-11T22:50:20.858347+00:00 | verified svgnest batch `20261011T224116Z-f791d9a1` | 0/7 valid | [table](benchmarks/results/svgnest-20261011T225020Z-9a82f951.md). Provisional; all failures retained.

- 2026-10-11T22:50:23.822640+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.1428571428571428 | [record](output/playwright/svgnest/20261011T224917Z-10d2fdfd/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:51:31.621076+00:00 | SVGnest `b-mao-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 2.4289495381343054 | [record](output/playwright/svgnest/20261011T225024Z-eeea1a59/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:52:37.504897+00:00 | SVGnest `b-mao-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 2.3426354974171986 | [record](output/playwright/svgnest/20261011T225131Z-04cc77a7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:53:43.329948+00:00 | SVGnest `b-mao-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.8936295964705883 | [record](output/playwright/svgnest/20261011T225237Z-59dc64d9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:53:59.883796+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.8535714285714285 | [record](output/playwright/deepnest/20261011T225242Z-64e8fe8a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:54:00.226459+00:00 | deepnest-next `b-jakobs1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.8 | [record](output/playwright/deepnest/20261011T225242Z-3f3ca58d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:54:49.914161+00:00 | SVGnest `b-marques-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.1923076923076923 | [record](output/playwright/svgnest/20261011T225343Z-31b8e26b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:55:11.035522+00:00 | deepnest-next `b-mao-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 1.9107763391066543 | [record](output/playwright/deepnest/20261011T225400Z-bf672e50/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:55:13.061327+00:00 | deepnest-next `b-jakobs2-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261011T225401Z-3d876f64/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:55:56.611744+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 8.730147952380952 | [record](output/playwright/svgnest/20261011T225450Z-dd33442b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:56:23.293661+00:00 | deepnest-next `b-mao-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 2.171376481312671 | [record](output/playwright/deepnest/20261011T225511Z-7e94638e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:56:25.413274+00:00 | deepnest-next `b-jakobs2-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261011T225513Z-a8b3613b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T22:57:02.525822+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 0, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T225556Z-51f28a6f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:58:09.069282+00:00 | SVGnest `b-shapes0-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261011T225703Z-5f1a25e1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:59:14.952310+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 8.764053428571428 | [record](output/playwright/svgnest/20261011T225809Z-e24329c4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T22:59:38.715830+00:00 | verified deepnest batch `20261011T225236Z-1db081c3` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T225938Z-475986a0.md). Provisional; all failures retained.

- 2026-10-11T22:59:39.184026+00:00 | verified deepnest batch `20261011T225236Z-a8ea8870` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T225939Z-960296a4.md). Provisional; all failures retained.

- 2026-10-11T23:00:10.500246+00:00 | verified svgnest batch `20261011T224118Z-d13a6ccb` | 14/16 valid | [table](benchmarks/results/svgnest-20261011T230010Z-45a8a99e.md). Provisional; all failures retained.

- 2026-10-11T23:01:04.333229+00:00 | deepnest-next `b-mao-strip-sheet` seed 0, 60s, identical, axis y | valid | material 0.8766455364705882 | [record](output/playwright/deepnest/20261011T225951Z-7f2bff2c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:01:06.579616+00:00 | deepnest-next `b-shapes0-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 7.523809523809524 | [record](output/playwright/deepnest/20261011T225951Z-c9d9ea49/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:01:21.112764+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 0, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T230013Z-59b5e210/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:01:32.165332+00:00 | SVGnest `b-albano-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 2.5943748626675456 | [record](output/playwright/svgnest/20261011T230024Z-6be931e0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:02:28.211525+00:00 | deepnest-next `b-marques-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.0961538461538463 | [record](output/playwright/deepnest/20261011T230105Z-6022b959/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:02:29.993718+00:00 | SVGnest `b-shapes1-strip-sheet` seed 0, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T230121Z-5f2da779/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:02:30.789220+00:00 | deepnest-next `b-shapes0-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.775 | [record](output/playwright/deepnest/20261011T230108Z-26217ae4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:02:41.734251+00:00 | SVGnest `b-albano-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 2.901999560536146 | [record](output/playwright/svgnest/20261011T230133Z-12e8eb02/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:03:37.594898+00:00 | SVGnest `b-shirts-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 9.385514923076924 | [record](output/playwright/svgnest/20261011T230230Z-559c4ca3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:03:41.090075+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.523809523809524 | [record](output/playwright/deepnest/20261011T230228Z-66bc20d4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:03:44.074091+00:00 | deepnest-next `b-shapes1-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.523809523809524 | [record](output/playwright/deepnest/20261011T230231Z-9eb3f056/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:03:48.885616+00:00 | SVGnest `b-albano-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.8465447136734694 | [record](output/playwright/svgnest/20261011T230242Z-0b2853ce/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:04:45.935526+00:00 | SVGnest `b-shirts-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 8.940170923076924 | [record](output/playwright/svgnest/20261011T230338Z-9861305a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:04:56.733482+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T230349Z-249c362b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:05:52.919573+00:00 | SVGnest `b-shirts-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.72440475 | [record](output/playwright/svgnest/20261011T230446Z-6ee03f79/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:06:03.357692+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T230457Z-84b0c859/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:06:47.709671+00:00 | verified deepnest batch `20261011T225942Z-9ffd5cd8` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T230647Z-fb263948.md). Provisional; all failures retained.

- 2026-10-11T23:06:48.955185+00:00 | verified deepnest batch `20261011T225943Z-ab3f2f8c` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T230648Z-93224fbd.md). Provisional; all failures retained.

- 2026-10-11T23:06:59.121194+00:00 | SVGnest `b-swim-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 5.817885831366608 | [record](output/playwright/svgnest/20261011T230553Z-0a28c69d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:07:09.807129+00:00 | SVGnest `b-blaz1-strip-sheet` seed 1, 60s, identical, axis y | valid | material 3.683333333333333 | [record](output/playwright/svgnest/20261011T230603Z-acb1c49d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11 | constructor v3 development maker diagnostic | 30/30 valid; exact v2 layouts with earlier collision rejection | [table](benchmarks/results/construct-maker-20261011T230206Z-b7a21810.md). No quality or speed gate.

- 2026-10-11 | first six-pass repacking smoke | three independently valid incumbents; failed capped trials retained | [table](benchmarks/results/repack-smoke-20261011T2307.md).

- 2026-10-11T23:08:01.428058+00:00 | deepnest-next `b-shapes1-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 7.761904761904762 | [record](output/playwright/deepnest/20261011T230648Z-06894d74/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:08:01.574888+00:00 | deepnest-next `b-shirts-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 8.205128205128204 | [record](output/playwright/deepnest/20261011T230649Z-8e373aba/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:08:05.959717+00:00 | SVGnest `b-swim-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 5.550648252555879 | [record](output/playwright/svgnest/20261011T230659Z-2e0892cc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:08:17.062441+00:00 | SVGnest `b-dagli-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.9770498166666667 | [record](output/playwright/svgnest/20261011T230710Z-89310efa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:09:12.211081+00:00 | deepnest-next `b-shapes1-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.5 | [record](output/playwright/deepnest/20261011T230802Z-4592cd14/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:09:12.339539+00:00 | deepnest-next `b-shirts-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.5630952750000002 | [record](output/playwright/deepnest/20261011T230802Z-2b6cfe0e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:09:13.392967+00:00 | SVGnest `b-swim-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.4221066662030597 | [record](output/playwright/svgnest/20261011T230806Z-453a129f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:09:23.318315+00:00 | SVGnest `b-fu-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T230817Z-638c9b16/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:10:20.131826+00:00 | SVGnest `b-trousers-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 3.7430356836158194 | [record](output/playwright/svgnest/20261011T230913Z-c3b065ca/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:10:22.115324+00:00 | deepnest-next `b-shirts-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 7.461538461538462 | [record](output/playwright/deepnest/20261011T230912Z-6c3738f8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:10:22.061351+00:00 | deepnest-next `b-swim-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 4.90342160597153 | [record](output/playwright/deepnest/20261011T230912Z-f2d0d543/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:10:31.777852+00:00 | SVGnest `b-fu-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/svgnest/20261011T230923Z-992bba09/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:11:27.852714+00:00 | SVGnest `b-trousers-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.4180790960451977 | [record](output/playwright/svgnest/20261011T231020Z-00082f5b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:11:38.578363+00:00 | SVGnest `b-fu-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.394736842105263 | [record](output/playwright/svgnest/20261011T231032Z-44e9d6c2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:11:48.079681+00:00 | verified deepnest batch `20261011T230645Z-5433a266` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T231148Z-0f5829be.md). Provisional; all failures retained.

- 2026-10-11T23:11:49.184924+00:00 | verified deepnest batch `20261011T230646Z-35bc2b5f` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T231149Z-008e242e.md). Provisional; all failures retained.

- 2026-10-11T23:12:33.998059+00:00 | SVGnest `b-trousers-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.329113924050633 | [record](output/playwright/svgnest/20261011T231128Z-c0e625db/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:12:45.028275+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 4.5 | [record](output/playwright/svgnest/20261011T231138Z-a951abca/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:13:01.560841+00:00 | deepnest-next `b-swim-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 4.815309339490865 | [record](output/playwright/deepnest/20261011T231150Z-63f83c15/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:13:01.948873+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 0, 60s, identical, axis y | valid | material 3.264281231638418 | [record](output/playwright/deepnest/20261011T231150Z-5bd0ac49/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:13:52.343004+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 4.5 | [record](output/playwright/svgnest/20261011T231245Z-600bfc02/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:14:11.922775+00:00 | verified svgnest batch `20261011T230012Z-9e7e14e5` | 9/11 valid | [table](benchmarks/results/svgnest-20261011T231411Z-61a4c43d.md). Provisional; all failures retained.

- 2026-10-11T23:14:13.279192+00:00 | deepnest-next `b-swim-strip-sheet` seed 0, 60s, identical, axis y | valid | material 1.7257255092141865 | [record](output/playwright/deepnest/20261011T231302Z-e3dd38ef/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:14:15.004922+00:00 | deepnest-next `b-trousers-strip-sheet` seed 0, 60s, identical, axis y | valid | material 2.2025316455696204 | [record](output/playwright/deepnest/20261011T231302Z-b9a0ad43/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:14:58.516265+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.83333335 | [record](output/playwright/svgnest/20261011T231352Z-cf12539e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:15:23.779495+00:00 | deepnest-next `b-trousers-nest-mb-free` seed 0, 60s, identical, axis y | valid | material 2.6666666666666665 | [record](output/playwright/deepnest/20261011T231414Z-a21c179e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:15:23.851246+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T231416Z-d40e699a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:16:04.429363+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 3.9166666666666665 | [record](output/playwright/svgnest/20261011T231458Z-dc0efd09/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:16:28.841370+00:00 | SVGnest `b-shapes1-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.65 | [record](output/playwright/svgnest/20261011T231524Z-3b4e1411/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:17:09.091132+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.9166666666666665 | [record](output/playwright/svgnest/20261011T231604Z-0f0850ae/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:17:11.232771+00:00 | verified deepnest batch `20261011T231145Z-fcbff56e` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T231711Z-82f402f9.md). Provisional; all failures retained.

- 2026-10-11T23:17:11.962190+00:00 | verified deepnest batch `20261011T231146Z-2b0af1a6` | 2/2 valid | [table](benchmarks/results/deepnest-20261011T231711Z-bbb992e6.md). Provisional; all failures retained.

- 2026-10-11T23:17:33.842288+00:00 | SVGnest `b-shirts-nest-mb-free` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T231628Z-4342084c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:17:43.113791+00:00 | current Sparrow `b-albano-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231741Z-a6bdcaca/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:44.589443+00:00 | current Sparrow `b-albano-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231743Z-03a7d9fa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:46.053567+00:00 | current Sparrow `b-albano-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231744Z-535bc640/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:47.495365+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231746Z-1941de8d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:49.028584+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231747Z-2676f00c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:50.470155+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231749Z-e25e1478/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:53.615093+00:00 | current Sparrow `b-albano-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231751Z-e17eb077/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:55.115956+00:00 | current Sparrow `b-albano-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231753Z-58270867/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:56.564181+00:00 | current Sparrow `b-albano-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231755Z-fc1381c3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:58.077557+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231756Z-4dfce7ac/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:17:59.642881+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231758Z-a3277650/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:18:01.132459+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231759Z-4fec5fd7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:18:14.168248+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.8707417571428572 | [record](output/playwright/svgnest/20261011T231709Z-33a397ee/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:18:25.846833+00:00 | deepnest-next `b-blaz1-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 10.666666666666666 | [record](output/playwright/deepnest/20261011T231716Z-71719750/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:18:26.827700+00:00 | deepnest-next `b-albano-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 2.5943748626675456 | [record](output/playwright/deepnest/20261011T231716Z-12de5ce0/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:18:39.106040+00:00 | SVGnest `b-shirts-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 8.916239333333333 | [record](output/playwright/svgnest/20261011T231733Z-b330c99d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:18:52.982026+00:00 | current Sparrow `b-dagli-strip-sheet` seed 1, 60s, identical, axis y | valid | score 0.88377255 | [record](output/sparrow-benchmark/20261011T231750Z-300c58fb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:18:54.629283+00:00 | current Sparrow `b-fu-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231853Z-ea4c75ec/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:18:56.432562+00:00 | current Sparrow `b-fu-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231854Z-efc39e2a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:18:57.996768+00:00 | current Sparrow `b-fu-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231856Z-8ed925d1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:18:59.756319+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231858Z-3682de98/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:01.576997+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231859Z-b1ea4cbc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:03.129255+00:00 | current Sparrow `b-dagli-strip-sheet` seed 2, 60s, identical, axis y | valid | score 0.8835400499999999 | [record](output/sparrow-benchmark/20261011T231801Z-8a2c2a31/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:04.887607+00:00 | current Sparrow `b-fu-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231903Z-1728e20c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:06.605813+00:00 | current Sparrow `b-fu-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231904Z-a85b4400/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:08.178910+00:00 | current Sparrow `b-fu-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231906Z-9b99ba9f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:09.631854+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231908Z-416de7af/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:11.090614+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T231909Z-4d1718dd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:19:19.135326+00:00 | SVGnest `b-mao-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 1.9281879872379213 | [record](output/playwright/svgnest/20261011T231814Z-43852898/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:19:34.391770+00:00 | deepnest-next `b-blaz1-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 9.666666666666666 | [record](output/playwright/deepnest/20261011T231826Z-87138a79/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:19:36.882457+00:00 | deepnest-next `b-albano-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 2.844649527576357 | [record](output/playwright/deepnest/20261011T231827Z-c081807a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:19:44.731812+00:00 | SVGnest `b-shirts-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.73125 | [record](output/playwright/svgnest/20261011T231839Z-d6aa87ec/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:20:04.230182+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 1, 60s, identical, axis y | valid | score 0.701604625 | [record](output/sparrow-benchmark/20261011T231901Z-049c0019/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:20:06.259103+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232004Z-558a81e2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:20:07.851654+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232006Z-d9bfa594/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:20:13.365117+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 2, 60s, identical, axis y | valid | score 0.701202775 | [record](output/sparrow-benchmark/20261011T231911Z-67449b9a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:20:14.956824+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232013Z-b9206488/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:20:16.459090+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232014Z-e9f4bab8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:20:24.754851+00:00 | SVGnest `b-mao-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 2.422971741112124 | [record](output/playwright/svgnest/20261011T231919Z-f0acfc0d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:20:43.067120+00:00 | deepnest-next `b-blaz1-strip-sheet` seed 1, 60s, identical, axis y | valid | material 3.366666733333333 | [record](output/playwright/deepnest/20261011T231934Z-299116b6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:20:45.621498+00:00 | deepnest-next `b-albano-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.7848714557142857 | [record](output/playwright/deepnest/20261011T231937Z-c3b12409/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:20:50.219202+00:00 | SVGnest `b-swim-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 4.9602457530873005 | [record](output/playwright/svgnest/20261011T231944Z-92b695f1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:20:59.431134+00:00 | verified deepnest batch `20261011T231713Z-80fe227f` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T232059Z-08a8be88.md). Provisional; all failures retained.

- 2026-10-11T23:21:12.707482+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 1, 60s, identical, axis y | valid | score 0.7539087571428571 | [record](output/sparrow-benchmark/20261011T232007Z-8c45e160/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:21:14.184001+00:00 | current Sparrow `b-mao-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232112Z-b5d11ce9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:21:15.610672+00:00 | current Sparrow `b-mao-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232114Z-95c5b140/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:21:18.471783+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 2, 60s, identical, axis y | valid | score 0.7585047571428571 | [record](output/sparrow-benchmark/20261011T232016Z-036073a7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:21:19.958922+00:00 | current Sparrow `b-mao-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232118Z-45777e53/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:21:21.506448+00:00 | current Sparrow `b-mao-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232119Z-6a9446fc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:21:31.416052+00:00 | SVGnest `b-mao-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.8773284019607843 | [record](output/playwright/svgnest/20261011T232025Z-2fca2374/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:21:56.240117+00:00 | SVGnest `b-swim-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 5.341178197878091 | [record](output/playwright/svgnest/20261011T232050Z-da1113ec/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:22:10.920021+00:00 | deepnest-next `b-dagli-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.9504597666666667 | [record](output/playwright/deepnest/20261011T232100Z-867996a3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:22:17.705210+00:00 | current Sparrow `b-mao-strip-sheet` seed 1, 60s, identical, axis y | valid | score 0.8124014580392157 | [record](output/sparrow-benchmark/20261011T232115Z-053ccce1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:22:23.495424+00:00 | current Sparrow `b-mao-strip-sheet` seed 2, 60s, identical, axis y | valid | score 0.7946245980392156 | [record](output/sparrow-benchmark/20261011T232121Z-c9637d3c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11 | 30/30 valid refined maker constructions | [proof](benchmarks/results/construct-maker-20261011T231256Z-a812ca42.md). Development diagnostic only.

- 2026-10-11 | 35/35 valid 64-pass sheet repacks; six sheet-count improvements | [proof](benchmarks/results/repack-sheet-20261011T231949Z-43e06d0f.md). Development diagnostic only.

- 2026-10-11 | four valid refined-repacking smoke incumbents | [proof](benchmarks/results/repack-refined-smoke-20261011T2322.md). Development diagnostic only.

- 2026-10-11 | Sparrow applicability: 32 area-bound exclusions without new solver attempts | [proof](benchmarks/results/sparrow-applicability-20261011T2322.md). Development diagnostic only.

- 2026-10-11T23:22:35.533163+00:00 | verified deepnest batch `20261011T231712Z-f580d353` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T232235Z-95244f8f.md). Provisional; all failures retained.

- 2026-10-11T23:22:37.403935+00:00 | SVGnest `b-marques-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.2019230769230769 | [record](output/playwright/svgnest/20261011T232131Z-343908e4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:23:01.420855+00:00 | SVGnest `b-swim-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.7942708703059804 | [record](output/playwright/svgnest/20261011T232156Z-381da256/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:23:19.707375+00:00 | current Sparrow `b-marques-strip-sheet` seed 1, 60s, identical, axis y | valid | score 0.9808291634615384 | [record](output/sparrow-benchmark/20261011T232217Z-632dd1eb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:20.382246+00:00 | deepnest-next `b-fu-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261011T232211Z-c1aed495/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:23:21.136560+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232319Z-9c0e8c6c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:22.557008+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232321Z-c5365883/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:24.062918+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232322Z-f346187a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:25.403081+00:00 | current Sparrow `b-marques-strip-sheet` seed 2, 60s, identical, axis y | valid | score 0.9906952884615385 | [record](output/sparrow-benchmark/20261011T232223Z-5981f099/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:25.711720+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232324Z-5869413c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:26.829335+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232325Z-633932e6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:27.125737+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232325Z-b5a72c15/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:28.246404+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232326Z-1d1ad66c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:28.509910+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232327Z-9150a838/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:29.644000+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232328Z-f34ec6eb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:29.908340+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232328Z-fa60274d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:31.061160+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232329Z-3b2225e4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:31.274490+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232329Z-8d92f980/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:32.463546+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232331Z-322608dd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:32.650182+00:00 | current Sparrow `b-shirts-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232331Z-27aad9fc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:33.884338+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232332Z-038a8e49/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:34.038974+00:00 | current Sparrow `b-swim-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232332Z-09cbb272/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:35.328633+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232333Z-dfd321ba/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:36.742218+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232335Z-270fc6e9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:38.149218+00:00 | current Sparrow `b-shirts-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232336Z-37195fb3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:39.565218+00:00 | current Sparrow `b-swim-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232338Z-11479649/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:43.896928+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 8.857142857142858 | [record](output/playwright/svgnest/20261011T232237Z-402c0ad2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:23:49.071223+00:00 | deepnest-next `b-fu-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.368421052631579 | [record](output/playwright/deepnest/20261011T232237Z-41bc8c8e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:23:53.441258+00:00 | current Sparrow `b-swim-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232351Z-9f339eed/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:54.833871+00:00 | current Sparrow `b-swim-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232353Z-c22b4010/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:56.285583+00:00 | current Sparrow `b-trousers-nest-mb-free` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232354Z-10cb3ca9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:57.681782+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232356Z-c8535a86/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:23:59.143643+00:00 | current Sparrow `b-trousers-strip-sheet` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232357Z-3cea840e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:24:01.617155+00:00 | current Sparrow `b-swim-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232359Z-1e6e5014/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:24:03.322294+00:00 | current Sparrow `b-swim-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232401Z-f5781d4b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:24:04.815417+00:00 | current Sparrow `b-trousers-nest-mb-free` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232403Z-82a496db/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:24:05.892492+00:00 | SVGnest `b-trousers-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 2.689265536723164 | [record](output/playwright/svgnest/20261011T232301Z-9f84c4a1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:24:06.378059+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232404Z-d12b7b69/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:24:07.826178+00:00 | current Sparrow `b-trousers-strip-sheet` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T232406Z-3608eb8f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:24:29.415519+00:00 | deepnest-next `b-fu-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261011T232320Z-e31daf0b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:24:36.815852+00:00 | verified sparrow batch `20261011T231741Z-8cf6c1cc` | 5/30 valid | [table](benchmarks/results/sparrow-20261011T232436Z-f57cdfcb.md). Provisional; all failures retained.

- 2026-10-11T23:24:37.707339+00:00 | verified sparrow batch `20261011T231751Z-665eb178` | 5/30 valid | [table](benchmarks/results/sparrow-20261011T232437Z-00e407a2.md). Provisional; all failures retained.

- 2026-10-11T23:24:38.380258+00:00 | verified sparrow batch `20261011T232351Z-688651a5` | 0/5 valid | [table](benchmarks/results/sparrow-20261011T232438Z-ab27f067.md). Provisional; all failures retained.

- 2026-10-11T23:24:39.129025+00:00 | verified sparrow batch `20261011T232359Z-0f5cddfe` | 0/5 valid | [table](benchmarks/results/sparrow-20261011T232439Z-2e582843.md). Provisional; all failures retained.

- 2026-10-11T23:24:48.539125+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 8.857142857142858 | [record](output/playwright/svgnest/20261011T232344Z-698eed85/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:24:58.305077+00:00 | deepnest-next `b-jakobs1-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 3.75 | [record](output/playwright/deepnest/20261011T232349Z-160b597f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:25:10.767527+00:00 | SVGnest `b-trousers-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.23728813559322 | [record](output/playwright/svgnest/20261011T232406Z-172a440c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:25:18.167894+00:00 | verified deepnest batch `20261011T232059Z-c497f2a9` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T232518Z-01b3400b.md). Provisional; all failures retained.

- 2026-10-11T23:25:52.975467+00:00 | SVGnest `b-shapes0-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261011T232448Z-d558b6fa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:26:06.074693+00:00 | deepnest-next `b-jakobs1-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.75 | [record](output/playwright/deepnest/20261011T232458Z-e3309ca6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:26:15.887571+00:00 | SVGnest `b-trousers-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.2658227848101267 | [record](output/playwright/svgnest/20261011T232510Z-805f27a6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:26:30.773376+00:00 | deepnest-next `b-jakobs1-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.7750000499999999 | [record](output/playwright/deepnest/20261011T232519Z-99309af6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:26:57.718305+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 8.857142857142858 | [record](output/playwright/svgnest/20261011T232553Z-12b197a4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:27:41.601248+00:00 | deepnest-next `b-jakobs2-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 3.5833333333333335 | [record](output/playwright/deepnest/20261011T232631Z-b6effc06/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:28:51.654136+00:00 | deepnest-next `b-jakobs2-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.5833333333333335 | [record](output/playwright/deepnest/20261011T232741Z-6a51ae7c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:29:29.798901+00:00 | verified svgnest batch `20261011T230023Z-eb6d4768` | 24/24 valid | [table](benchmarks/results/svgnest-20261011T232929Z-304ec767.md). Provisional; all failures retained.

- 2026-10-11T23:29:30.826886+00:00 | verified svgnest batch `20261011T231415Z-3205693c` | 10/11 valid | [table](benchmarks/results/svgnest-20261011T232930Z-10c9e748.md). Provisional; all failures retained.

- 2026-10-11T23:29:31.794989+00:00 | verified deepnest batch `20261011T232236Z-eca3eb62` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T232931Z-54f98cd7.md). Provisional; all failures retained.

- 2026-10-11T23:30:41.680727+00:00 | SVGnest `b-albano-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 2.5584630371346955 | [record](output/playwright/svgnest/20261011T232936Z-ee4d4304/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:30:49.224106+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261011T232943Z-345e186f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:31:04.414175+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.8523809571428571 | [record](output/playwright/deepnest/20261011T232953Z-e3e1b6dd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:31:46.792719+00:00 | SVGnest `b-albano-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 2.8968908870577894 | [record](output/playwright/svgnest/20261011T233041Z-d6f1116b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:31:54.646542+00:00 | SVGnest `b-shapes1-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.65 | [record](output/playwright/svgnest/20261011T233049Z-e558ef3d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:32:12.722922+00:00 | deepnest-next `b-mao-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 1.9180627225767242 | [record](output/playwright/deepnest/20261011T233104Z-c4a5a3ee/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:32:17.671879+00:00 | verified deepnest batch `20261011T232518Z-9e064e7c` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T233217Z-d9bc3daf.md). Provisional; all failures retained.

- 2026-10-11T23:32:51.753494+00:00 | SVGnest `b-albano-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.8076942967346938 | [record](output/playwright/svgnest/20261011T233146Z-e38f4418/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:32:59.589532+00:00 | SVGnest `b-shirts-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 7.589743589743589 | [record](output/playwright/svgnest/20261011T233154Z-e63bc524/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:33:20.774231+00:00 | deepnest-next `b-mao-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 2.171376481312671 | [record](output/playwright/deepnest/20261011T233212Z-beff8690/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:33:31.018504+00:00 | deepnest-next `b-mao-strip-sheet` seed 1, 60s, identical, axis y | valid | material 0.8699480925490195 | [record](output/playwright/deepnest/20261011T233222Z-f47d26e7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:33:56.911069+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T233251Z-143edc9d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:34:04.468876+00:00 | current Sparrow `s-albano-strip` seed 0, 60s, upstream-default, axis x | valid | score 9902.3427734375 | [record](output/sparrow-benchmark/20261011T233302Z-1ed23e14/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:34:04.923461+00:00 | SVGnest `b-shirts-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 8.871794871794872 | [record](output/playwright/svgnest/20261011T233259Z-deb2d7e1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:34:14.789133+00:00 | current Sparrow `s-albano-strip` seed 1, 60s, upstream-default, axis x | valid | score 9898.357421875 | [record](output/sparrow-benchmark/20261011T233312Z-b87b451d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:34:40.682698+00:00 | deepnest-next `b-marques-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.1057692307692308 | [record](output/playwright/deepnest/20261011T233331Z-713de031/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:35:02.210484+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261011T233357Z-15f4ac10/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:35:06.238778+00:00 | current Sparrow `s-blaz1-strip` seed 0, 60s, upstream-default, axis x | valid | score 26.21071434020996 | [record](output/sparrow-benchmark/20261011T233404Z-16afd21c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:35:10.162263+00:00 | SVGnest `b-shirts-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.742410725 | [record](output/playwright/svgnest/20261011T233405Z-7bbdb645/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:35:16.462098+00:00 | current Sparrow `s-blaz1-strip` seed 1, 60s, upstream-default, axis x | valid | score 26.42534637451172 | [record](output/sparrow-benchmark/20261011T233414Z-497a653d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:35:49.013922+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 7.523809523809524 | [record](output/playwright/deepnest/20261011T233440Z-4d5eef8f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:36:07.556667+00:00 | SVGnest `b-blaz1-strip-sheet` seed 2, 60s, identical, axis y | valid | material 3.6 | [record](output/playwright/svgnest/20261011T233502Z-2ddc6e77/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:36:07.876645+00:00 | current Sparrow `s-dagli-strip` seed 0, 60s, upstream-default, axis x | valid | score 58.17390823364258 | [record](output/sparrow-benchmark/20261011T233506Z-55ba1510/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:36:15.468311+00:00 | SVGnest `b-swim-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 4.846951418442638 | [record](output/playwright/svgnest/20261011T233510Z-3d7400eb/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:36:18.465388+00:00 | current Sparrow `s-dagli-strip` seed 1, 60s, upstream-default, axis x | valid | score 58.925857543945305 | [record](output/sparrow-benchmark/20261011T233516Z-e0497c53/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:37:09.658307+00:00 | current Sparrow `s-fu-strip` seed 0, 60s, upstream-default, axis x | valid | score 31.68190574645996 | [record](output/sparrow-benchmark/20261011T233607Z-0478ac6d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:37:12.532641+00:00 | SVGnest `b-dagli-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.9781609333333333 | [record](output/playwright/svgnest/20261011T233607Z-e0ce775f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:37:19.973128+00:00 | verified deepnest batch `20261011T232953Z-fbc60183` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T233719Z-d52d7757.md). Provisional; all failures retained.

- 2026-10-11T23:37:20.673923+00:00 | current Sparrow `s-fu-strip` seed 1, 60s, upstream-default, axis x | valid | score 32.00153350830078 | [record](output/sparrow-benchmark/20261011T233618Z-6ecea7db/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:37:21.480019+00:00 | verified deepnest batch `20261011T233218Z-fa4c66d1` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T233721Z-0406604a.md). Provisional; all failures retained.

- 2026-10-11T23:37:21.522050+00:00 | SVGnest `b-swim-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 5.162206487869697 | [record](output/playwright/svgnest/20261011T233615Z-831eebc3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:38:12.620992+00:00 | current Sparrow `s-jakobs1-strip` seed 0, 60s, upstream-default, axis x | valid | score 11.026813507080078 | [record](output/sparrow-benchmark/20261011T233709Z-ba5ad02d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:38:21.731345+00:00 | SVGnest `b-fu-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 3.8095238095238093 | [record](output/playwright/svgnest/20261011T233713Z-693b5434/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:38:23.775426+00:00 | current Sparrow `s-jakobs1-strip` seed 1, 60s, upstream-default, axis x | valid | score 11.00328540802002 | [record](output/sparrow-benchmark/20261011T233720Z-b54c047d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:38:30.491648+00:00 | SVGnest `b-swim-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.7414362964186372 | [record](output/playwright/svgnest/20261011T233722Z-817ca590/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:38:42.859137+00:00 | deepnest-next `b-shapes0-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 7.523809523809524 | [record](output/playwright/deepnest/20261011T233728Z-31cb6c22/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:38:42.876530+00:00 | deepnest-next `b-shapes1-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 7.476190476190476 | [record](output/playwright/deepnest/20261011T233728Z-53f13faf/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:39:14.480157+00:00 | current Sparrow `s-jakobs2-strip` seed 0, 60s, upstream-default, axis x | valid | score 24.00970458984375 | [record](output/sparrow-benchmark/20261011T233812Z-e14b000a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:39:25.861064+00:00 | current Sparrow `s-jakobs2-strip` seed 1, 60s, upstream-default, axis x | valid | score 24.057613372802734 | [record](output/sparrow-benchmark/20261011T233823Z-64a97f27/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:39:27.604033+00:00 | SVGnest `b-fu-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.8095238095238093 | [record](output/playwright/svgnest/20261011T233821Z-37b90c7c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:39:36.580850+00:00 | SVGnest `b-trousers-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 2.7457627118644066 | [record](output/playwright/svgnest/20261011T233830Z-c9395af0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:39:52.881035+00:00 | deepnest-next `b-shapes1-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.5 | [record](output/playwright/deepnest/20261011T233843Z-4c29ad7d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:39:54.357625+00:00 | deepnest-next `b-shapes0-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.775 | [record](output/playwright/deepnest/20261011T233843Z-eeba912e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:40:16.540294+00:00 | current Sparrow `s-mao-strip` seed 0, 60s, upstream-default, axis x | valid | score 1782.2460327148438 | [record](output/sparrow-benchmark/20261011T233914Z-25f67c0b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:40:27.999796+00:00 | current Sparrow `s-mao-strip` seed 1, 60s, upstream-default, axis x | valid | score 1790.916748046875 | [record](output/sparrow-benchmark/20261011T233925Z-eb5c4dfa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:40:34.492348+00:00 | SVGnest `b-fu-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.415413552631579 | [record](output/playwright/svgnest/20261011T233927Z-f06979a3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:40:43.959387+00:00 | SVGnest `b-trousers-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.2937853107344632 | [record](output/playwright/svgnest/20261011T233937Z-41ee972c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:41:06.259513+00:00 | deepnest-next `b-shirts-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 7.461538461538462 | [record](output/playwright/deepnest/20261011T233953Z-2a3bb405/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:41:07.085212+00:00 | deepnest-next `b-shapes1-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 7.523809523809524 | [record](output/playwright/deepnest/20261011T233954Z-a153924c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:41:19.074474+00:00 | current Sparrow `s-marques-strip` seed 0, 60s, upstream-default, axis x | valid | score 76.81541442871094 | [record](output/sparrow-benchmark/20261011T234016Z-b650ba85/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:41:30.219083+00:00 | current Sparrow `s-marques-strip` seed 1, 60s, upstream-default, axis x | valid | score 77.3263931274414 | [record](output/sparrow-benchmark/20261011T234028Z-85bd0bd8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:41:41.127042+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 4.583333333333333 | [record](output/playwright/svgnest/20261011T234034Z-4fdd83be/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:41:50.682865+00:00 | SVGnest `b-trousers-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.3562386962025315 | [record](output/playwright/svgnest/20261011T234044Z-4d150e94/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:42:21.451554+00:00 | current Sparrow `s-shapes0-strip` seed 0, 60s, upstream-default, axis x | valid | score 61.046875 | [record](output/sparrow-benchmark/20261011T234119Z-aad02172/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:42:32.821827+00:00 | current Sparrow `s-shapes0-strip` seed 1, 60s, upstream-default, axis x | valid | score 61.51713562011719 | [record](output/sparrow-benchmark/20261011T234130Z-c6fd54d8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:42:48.088627+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 4.583333333333333 | [record](output/playwright/svgnest/20261011T234141Z-021d434a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:43:23.923781+00:00 | current Sparrow `s-shapes1-strip` seed 0, 60s, upstream-default, axis x | valid | score 54.56507110595703 | [record](output/sparrow-benchmark/20261011T234221Z-4f2be279/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:43:34.961347+00:00 | current Sparrow `s-shapes1-strip` seed 1, 60s, upstream-default, axis x | valid | score 56.01146697998047 | [record](output/sparrow-benchmark/20261011T234232Z-710d14d3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:43:54.121398+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.825 | [record](output/playwright/svgnest/20261011T234248Z-f135db7b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:44:26.226341+00:00 | current Sparrow `s-shirts-strip` seed 0, 60s, upstream-default, axis x | valid | score 61.579463958740234 | [record](output/sparrow-benchmark/20261011T234323Z-f45f34ab/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:44:37.050938+00:00 | current Sparrow `s-shirts-strip` seed 1, 60s, upstream-default, axis x | valid | score 62.796199798583984 | [record](output/sparrow-benchmark/20261011T234334Z-92c6e5e7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:45:00.495274+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 3.8125 | [record](output/playwright/svgnest/20261011T234354Z-88d72d91/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:45:28.162078+00:00 | current Sparrow `s-swim-strip` seed 0, 60s, upstream-default, axis x | valid | score 6024.28564453125 | [record](output/sparrow-benchmark/20261011T234426Z-230d2d56/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:45:38.924153+00:00 | current Sparrow `s-swim-strip` seed 1, 60s, upstream-default, axis x | valid | score 5910.28515625 | [record](output/sparrow-benchmark/20261011T234437Z-45ab12b4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:46:10.404625+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.8125 | [record](output/playwright/svgnest/20261011T234500Z-de9881aa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:46:26.354707+00:00 | verified svgnest batch `20261011T232943Z-338509f4` | 11/11 valid | [table](benchmarks/results/svgnest-20261011T234626Z-7436f9b9.md). Provisional; all failures retained.

- 2026-10-11T23:46:26.804755+00:00 | verified deepnest batch `20261011T233722Z-5d058b66` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T234626Z-87b2cfe3.md). Provisional; all failures retained.

- 2026-10-11T23:46:27.279232+00:00 | verified deepnest batch `20261011T233723Z-ef659f24` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T234627Z-85842355.md). Provisional; all failures retained.

- 2026-10-11T23:46:30.414690+00:00 | current Sparrow `s-trousers-strip` seed 0, 60s, upstream-default, axis x | valid | score 244.00906372070312 | [record](output/sparrow-benchmark/20261011T234528Z-102faa1b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:46:40.895661+00:00 | current Sparrow `s-trousers-strip` seed 1, 60s, upstream-default, axis x | valid | score 242.03526306152344 | [record](output/sparrow-benchmark/20261011T234538Z-e7a88648/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:47:22.369481+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.9136190571428571 | [record](output/playwright/svgnest/20261011T234610Z-889b5f28/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11 | Contact-only maker construction: 30/30 valid | [diagnostic](benchmarks/results/construct-maker-20261011T233229Z-abc5d7b1.md). All regressions retained; not a quality gate.

- 2026-10-11 | Contact-only sheet repacking: 35/35 valid | [diagnostic](benchmarks/results/repack-sheet-20261011T233219Z-3f26f543.md). All regressions retained; not a quality gate.

- 2026-10-11 | Three-method maker construction: 30/30 valid | [diagnostic](benchmarks/results/repack-maker-20261011T233725Z-c0e36d78.md). All regressions retained; not a quality gate.

- 2026-10-11 | Alternating-method sheet repacking: 35/35 valid | [diagnostic](benchmarks/results/repack-sheet-20261011T233736Z-d6963d0b.md). All regressions retained; not a quality gate.

- 2026-10-11T23:47:43.154807+00:00 | verified sparrow batch `20261011T233301Z-f20e6eef` | 13/13 valid | [table](benchmarks/results/sparrow-20261011T234743Z-f76b51b0.md). Provisional; all failures retained.

- 2026-10-11T23:47:44.448798+00:00 | verified sparrow batch `20261011T233311Z-8d956d8d` | 13/13 valid | [table](benchmarks/results/sparrow-20261011T234744Z-913bfcaa.md). Provisional; all failures retained.

- 2026-10-11T23:47:47.396109+00:00 | SVGnest `b-albano-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 3.322545162162162 | [record](output/playwright/svgnest/20261011T234636Z-f79d8d5b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:47:59.507552+00:00 | current Sparrow `b-albano-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234757Z-47ad0490/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:01.204778+00:00 | current Sparrow `b-albano-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234759Z-4c9f1e65/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:03.165351+00:00 | current Sparrow `b-albano-strip-sheet` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234801Z-f650bb6e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:04.864608+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234803Z-25b02fd2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:06.631790+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234804Z-f4b6138f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:08.342055+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234806Z-b2a76d87/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:19.185686+00:00 | deepnest-next `b-swim-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 4.624515100398043 | [record](output/playwright/deepnest/20261011T234644Z-1a319874/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:48:34.140087+00:00 | SVGnest `b-mao-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 2.5177757520510484 | [record](output/playwright/svgnest/20261011T234722Z-6a4666b0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:48:37.801110+00:00 | deepnest-next `b-shirts-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 8.205128205128204 | [record](output/playwright/deepnest/20261011T234642Z-a0b3be31/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:48:52.072049+00:00 | current Sparrow `s-albano-strip` seed 2, 60s, upstream-default, axis x | valid | score 9956.9619140625 | [record](output/sparrow-benchmark/20261011T234748Z-512a1c62/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:48:56.180095+00:00 | SVGnest `b-albano-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 4.161722698308064 | [record](output/playwright/svgnest/20261011T234747Z-84d8a4da/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:49:10.906263+00:00 | current Sparrow `b-dagli-strip-sheet` seed 0, 60s, upstream-default, axis x | valid | score 0.9999993 | [record](output/sparrow-benchmark/20261011T234808Z-939239b1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:12.646909+00:00 | current Sparrow `b-fu-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234910Z-9ce5e462/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:14.293223+00:00 | current Sparrow `b-fu-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234912Z-007b02e2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:15.971773+00:00 | current Sparrow `b-fu-strip-sheet` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234914Z-23645f23/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:17.600102+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234915Z-77c7ef04/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:19.259711+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T234917Z-13a71139/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:32.198725+00:00 | deepnest-next `b-swim-strip-sheet` seed 1, 60s, identical, axis y | valid | material 1.6935136150904033 | [record](output/playwright/deepnest/20261011T234819Z-529559f1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:49:42.098074+00:00 | SVGnest `b-mao-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 2.4655520455788515 | [record](output/playwright/svgnest/20261011T234834Z-fbace74a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:49:53.919527+00:00 | current Sparrow `s-blaz1-strip` seed 2, 60s, upstream-default, axis x | valid | score 26.843490600585938 | [record](output/sparrow-benchmark/20261011T234852Z-d241e3ef/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:49:55.030991+00:00 | deepnest-next `b-shirts-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.5651515249999997 | [record](output/playwright/deepnest/20261011T234838Z-f57f8518/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:50:03.498575+00:00 | SVGnest `b-albano-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 3.2220785540816324 | [record](output/playwright/svgnest/20261011T234856Z-d5b20031/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:50:21.093262+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 0, 60s, upstream-default, axis x | valid | score 0.9999965749999999 | [record](output/sparrow-benchmark/20261011T234919Z-29a16a3c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:50:22.861344+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235021Z-320823de/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:50:24.545805+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235022Z-8a82c330/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:50:44.137957+00:00 | deepnest-next `b-trousers-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 2.6666666666666665 | [record](output/playwright/deepnest/20261011T234932Z-a9fcf64e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:50:49.332069+00:00 | SVGnest `b-mao-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.942916300392157 | [record](output/playwright/svgnest/20261011T234942Z-249bde76/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:50:56.035632+00:00 | current Sparrow `s-dagli-strip` seed 2, 60s, upstream-default, axis x | valid | score 58.849693298339844 | [record](output/sparrow-benchmark/20261011T234953Z-b0f24390/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:51:07.496147+00:00 | deepnest-next `b-swim-nest-mb-free` seed 1, 60s, identical, axis y | valid | material 4.883006106894998 | [record](output/playwright/deepnest/20261011T234955Z-026cef8e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:51:10.550702+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 17.579967066666665 | [record](output/playwright/svgnest/20261011T235003Z-736868bf/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:51:26.996470+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 0, 60s, upstream-default, axis x | valid | score 0.9999439714285714 | [record](output/sparrow-benchmark/20261011T235024Z-639b9f70/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:51:28.829380+00:00 | current Sparrow `b-mao-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235127Z-b8743b1d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:51:30.470710+00:00 | current Sparrow `b-mao-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235128Z-1bd8d4ee/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:51:33.107168+00:00 | verified deepnest batch `20261011T234637Z-e713a7b4` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T235133Z-9374e80b.md). Provisional; all failures retained.

- 2026-10-11T23:51:33.530815+00:00 | verified deepnest batch `20261011T234634Z-719d2a45` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T235133Z-ef290674.md). Provisional; all failures retained.

- 2026-10-11T23:51:57.666694+00:00 | SVGnest `b-marques-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.1923076923076923 | [record](output/playwright/svgnest/20261011T235049Z-e3878a93/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:51:58.042399+00:00 | current Sparrow `s-fu-strip` seed 2, 60s, upstream-default, axis x | valid | score 32.55729103088379 | [record](output/sparrow-benchmark/20261011T235056Z-7e042940/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:52:17.335138+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 16.5 | [record](output/playwright/svgnest/20261011T235110Z-8f16d95f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:52:32.488573+00:00 | current Sparrow `b-mao-strip-sheet` seed 0, 60s, upstream-default, axis x | valid | score 0.9999901388235295 | [record](output/sparrow-benchmark/20261011T235130Z-a82efccb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:00.834946+00:00 | current Sparrow `s-jakobs1-strip` seed 2, 60s, upstream-default, axis x | valid | score 11.38460636138916 | [record](output/sparrow-benchmark/20261011T235158Z-9506d3eb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:04.726831+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 1, 60s, identical, axis y | valid | material 3.316166881355932 | [record](output/playwright/deepnest/20261011T235145Z-0616841f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:53:04.912992+00:00 | deepnest-next `b-albano-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 2.5943748626675456 | [record](output/playwright/deepnest/20261011T235145Z-297ec8fe/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:53:06.869417+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 8.666666666666666 | [record](output/playwright/svgnest/20261011T235157Z-78ea4ca3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:53:25.534037+00:00 | SVGnest `b-blaz1-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 3.8 | [record](output/playwright/svgnest/20261011T235217Z-f7841029/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:53:38.152747+00:00 | current Sparrow `b-marques-strip-sheet` seed 0, 60s, upstream-default, axis x | valid | score 0.9999628173076922 | [record](output/sparrow-benchmark/20261011T235232Z-81ef1aeb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:39.786006+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235338Z-1ab4e8d2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:41.534044+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235339Z-8e3aa25a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:43.134393+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235341Z-72055856/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:44.709102+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235343Z-b9a53b6d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:46.356500+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235344Z-4ccef597/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:47.920448+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235346Z-f82b02aa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:49.550376+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235347Z-1bd1dc6f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:51.192182+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235349Z-1f9edf55/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:52.806877+00:00 | current Sparrow `b-shirts-strip-sheet` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235351Z-8e798899/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:53:54.528199+00:00 | current Sparrow `b-swim-nest-mb-free` seed 0, 60s, upstream-default, axis x | unsupported | score None | [record](output/sparrow-benchmark/20261011T235352Z-f6fd21d2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:54:02.947660+00:00 | current Sparrow `s-jakobs2-strip` seed 2, 60s, upstream-default, axis x | valid | score 24.00564193725586 | [record](output/sparrow-benchmark/20261011T235300Z-936ec904/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:54:14.241716+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 8.571428571428571 | [record](output/playwright/svgnest/20261011T235307Z-682a4055/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:54:17.754692+00:00 | deepnest-next `b-albano-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 2.8395408538782685 | [record](output/playwright/deepnest/20261011T235305Z-df54a4a3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:54:19.894898+00:00 | verified sparrow batch `20261011T234756Z-716e99e7` | 5/30 valid | [table](benchmarks/results/sparrow-20261011T235419Z-cbe14750.md). Provisional; all failures retained.

- 2026-10-11 | Sparrow batch `20261011T234756Z-716e99e7` used axis x in error for B. Retained as an extra orientation diagnostic; it does not fill the frozen axis-y M1 slots. No outcomes are discarded or substituted.

- 2026-10-11T23:54:19.947993+00:00 | deepnest-next `b-trousers-strip-sheet` seed 1, 60s, identical, axis y | valid | material 2.2025316455696204 | [record](output/playwright/deepnest/20261011T235305Z-5e6d215d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:54:32.242969+00:00 | SVGnest `b-dagli-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 0.9770498166666667 | [record](output/playwright/svgnest/20261011T235325Z-c2f28755/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:54:54.725759+00:00 | current Sparrow `b-albano-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235452Z-aa4f0989/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:54:56.351167+00:00 | current Sparrow `b-albano-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235454Z-59b5166e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:54:58.037662+00:00 | current Sparrow `b-albano-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235456Z-e8b5451b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:54:59.680931+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235458Z-3eb1140f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:55:00.072074+00:00 | verified deepnest batch `20261011T235134Z-b6eb5bee` | 2/2 valid | [table](benchmarks/results/deepnest-20261011T235500Z-2804a8e5.md). Provisional; all failures retained.

- 2026-10-11T23:55:01.485561+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235459Z-da85083b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11 | interleaved-copy 64-pass trial: 35/35 valid; 9 improve, 20 unchanged, 6 worse vs prior search; one fewer-sheet job | [diagnostic](benchmarks/results/repack-sheet-20261011T235145Z-a809b3f1.md). No gate claim.

- 2026-10-11T23:55:03.208528+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235501Z-e4caecf6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:55:04.765624+00:00 | current Sparrow `s-mao-strip` seed 2, 60s, upstream-default, axis x | valid | score 1792.149169921875 | [record](output/sparrow-benchmark/20261011T235402Z-25ea924a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:55:21.765284+00:00 | SVGnest `b-shapes0-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261011T235414Z-b6e59add/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:55:30.022172+00:00 | deepnest-next `b-albano-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.810168298979592 | [record](output/playwright/deepnest/20261011T235418Z-00be1bff/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:55:38.107516+00:00 | SVGnest `b-fu-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 4.85447519047619 | [record](output/playwright/svgnest/20261011T235432Z-0b806817/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:55:58.195658+00:00 | verified deepnest batch `20261011T235137Z-1aa2ddbe` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T235558Z-7c5e10ea.md). Provisional; all failures retained.

- 2026-10-11T23:56:05.253781+00:00 | current Sparrow `b-albano-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235602Z-e30cb8ea/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:06.231336+00:00 | current Sparrow `b-dagli-strip-sheet` seed 0, 60s, upstream-default, axis y | valid | score 0.8834518666666666 | [record](output/sparrow-benchmark/20261011T235503Z-049240ac/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:07.326916+00:00 | current Sparrow `b-albano-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235605Z-1cbf6c74/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:07.659229+00:00 | current Sparrow `s-marques-strip` seed 2, 60s, upstream-default, axis x | valid | score 77.9709243774414 | [record](output/sparrow-benchmark/20261011T235504Z-2d4e37dd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:08.308613+00:00 | current Sparrow `b-fu-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235606Z-dc7bfeb8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:09.961881+00:00 | current Sparrow `b-albano-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235607Z-714fbae8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:10.520028+00:00 | current Sparrow `b-fu-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235608Z-581bd79b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:13.505715+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235609Z-a80a75aa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:13.537300+00:00 | current Sparrow `b-fu-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235610Z-dfe5bcb0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:16.735679+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235613Z-b1d39d1b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:16.750215+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235613Z-f78f3381/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:18.976996+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235616Z-619c7b7e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:19.026536+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235616Z-2e19afb2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:56:21.673205+00:00 | deepnest-next `b-blaz1-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 9.8 | [record](output/playwright/deepnest/20261011T235503Z-164f0c85/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:56:33.439885+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 8.666666666666666 | [record](output/playwright/svgnest/20261011T235521Z-ec5e350f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:56:44.294460+00:00 | SVGnest `b-fu-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 3.880952380952381 | [record](output/playwright/svgnest/20261011T235538Z-b574632c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:57:00.366026+00:00 | verified svgnest batch `20261011T232935Z-a2038664` | 24/24 valid | [table](benchmarks/results/svgnest-20261011T235700Z-7754d389.md). Provisional; all failures retained.

- 2026-10-11T23:57:10.434726+00:00 | current Sparrow `s-shapes0-strip` seed 2, 60s, upstream-default, axis x | valid | score 62.016361236572266 | [record](output/sparrow-benchmark/20261011T235607Z-1b82eab9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:21.694831+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 0, 60s, upstream-default, axis y | valid | score 0.7195452999999999 | [record](output/sparrow-benchmark/20261011T235619Z-2edf4e9c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:21.893072+00:00 | current Sparrow `b-dagli-strip-sheet` seed 1, 60s, upstream-default, axis y | valid | score 0.8900095666666666 | [record](output/sparrow-benchmark/20261011T235618Z-2ad11ecb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:23.432408+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235721Z-d3bc198f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:23.525720+00:00 | current Sparrow `b-fu-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235721Z-1f6b740a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:25.044591+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235723Z-93797228/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:25.106099+00:00 | current Sparrow `b-fu-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235723Z-05725a57/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:26.687484+00:00 | current Sparrow `b-fu-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235725Z-0477295d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:28.365386+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235726Z-6f51e86b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:30.081518+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235728Z-413e96f6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:57:36.600216+00:00 | deepnest-next `b-dagli-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.9386426999999999 | [record](output/playwright/deepnest/20261011T235602Z-9056d33f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:57:48.738760+00:00 | deepnest-next `b-blaz1-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 10.666666666666666 | [record](output/playwright/deepnest/20261011T235623Z-11f15d55/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:57:53.069971+00:00 | SVGnest `b-fu-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 1.394736842105263 | [record](output/playwright/svgnest/20261011T235645Z-3a432fb9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:58:12.452520+00:00 | current Sparrow `s-shapes1-strip` seed 2, 60s, upstream-default, axis x | valid | score 56.00193786621094 | [record](output/sparrow-benchmark/20261011T235710Z-69e5162d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:13.035282+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T235703Z-3c510954/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:58:25.401721+00:00 | svgnest B identical, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261011T235825Z-a4355046.md). No final gate.

- 2026-10-11T23:58:26.855319+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 0, 60s, upstream-default, axis y | valid | score 0.7568241142857143 | [record](output/sparrow-benchmark/20261011T235725Z-bf32be0c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:28.450285+00:00 | current Sparrow `b-mao-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235826Z-f52d5c7a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:30.034145+00:00 | current Sparrow `b-mao-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235828Z-3ff8f19b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:32.223968+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 1, 60s, upstream-default, axis y | valid | score 0.7013896749999999 | [record](output/sparrow-benchmark/20261011T235730Z-e978562f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:34.245411+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235832Z-aa6e3548/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:35.800662+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235834Z-c5ad2387/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:58:49.923009+00:00 | deepnest-next `b-fu-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261011T235737Z-1bfd2802/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:58:59.709468+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T235753Z-16f93690/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:59:00.878884+00:00 | deepnest-next `b-blaz1-strip-sheet` seed 2, 60s, identical, axis y | valid | material 3.3333333333333335 | [record](output/playwright/deepnest/20261011T235749Z-78fa0c11/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-11T23:59:13.417089+00:00 | verified deepnest batch `20261011T235501Z-2323f3cb` | 3/3 valid | [table](benchmarks/results/deepnest-20261011T235913Z-1ed79bc1.md). Provisional; all failures retained.

- 2026-10-11T23:59:14.399923+00:00 | current Sparrow `s-shirts-strip` seed 2, 60s, upstream-default, axis x | valid | score 61.45492935180664 | [record](output/sparrow-benchmark/20261011T235812Z-9aea23ce/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:59:19.777362+00:00 | SVGnest `b-shapes1-strip-sheet` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T235813Z-c6435bc9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-11T23:59:31.984429+00:00 | current Sparrow `b-mao-strip-sheet` seed 0, 60s, upstream-default, axis y | valid | score 0.7883978635294119 | [record](output/sparrow-benchmark/20261011T235830Z-8f4785d3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:59:37.573186+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 1, 60s, upstream-default, axis y | valid | score 0.7585018142857143 | [record](output/sparrow-benchmark/20261011T235835Z-82de8350/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:59:39.238748+00:00 | current Sparrow `b-mao-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235937Z-42294151/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-11T23:59:41.350931+00:00 | current Sparrow `b-mao-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261011T235939Z-0dae46c6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:03.487624+00:00 | deepnest-next `b-fu-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261011T235850Z-bf96cc21/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:00:07.517695+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261011T235900Z-4dd1d26a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:00:16.776234+00:00 | current Sparrow `s-swim-strip` seed 2, 60s, upstream-default, axis x | valid | score 5963.72021484375 | [record](output/sparrow-benchmark/20261011T235914Z-abcb63fa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:27.651055+00:00 | SVGnest `b-shirts-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 9.526993333333333 | [record](output/playwright/svgnest/20261011T235920Z-907c3be0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:00:29.728520+00:00 | deepnest-next `b-fu-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.3890977631578947 | [record](output/playwright/deepnest/20261011T235916Z-0bc7ccc5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:00:34.299954+00:00 | current Sparrow `b-marques-strip-sheet` seed 0, 60s, upstream-default, axis y | valid | score 0.99042775 | [record](output/sparrow-benchmark/20261011T235932Z-8add0979/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:35.909009+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000034Z-ef8d5c9e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:37.580163+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000035Z-a1bdd71f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:39.302217+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000037Z-1d07da5c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:41.007849+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000039Z-ea18f463/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:42.719765+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000041Z-53056cbc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:43.321810+00:00 | current Sparrow `b-mao-strip-sheet` seed 1, 60s, upstream-default, axis y | valid | score 0.8062506705882352 | [record](output/sparrow-benchmark/20261011T235941Z-8a222769/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:44.571577+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000042Z-9768d2ef/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:46.387319+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000044Z-adfcabc8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:48.216835+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000046Z-e1a8f333/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:49.741028+00:00 | current Sparrow `b-shirts-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000048Z-ae37a9b4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:00:51.422234+00:00 | current Sparrow `b-swim-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000049Z-33017b27/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:13.577949+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T000007Z-9becfcc7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:01:18.776791+00:00 | current Sparrow `s-trousers-strip` seed 2, 60s, upstream-default, axis x | valid | score 241.27084350585938 | [record](output/sparrow-benchmark/20261012T000016Z-5249e280/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:18.987508+00:00 | verified deepnest batch `20261011T235559Z-bd69894c` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T000118Z-fae7b336.md). Provisional; all failures retained.

- 2026-10-12T00:01:19.314549+00:00 | verified sparrow batch `20261011T235449Z-5d37fe32` | 5/30 valid | [table](benchmarks/results/sparrow-20261012T000119Z-6baecff3.md). Provisional; all failures retained.

- 2026-10-12T00:01:24.403232+00:00 | current Sparrow `b-albano-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000122Z-c3b53541/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:25.997065+00:00 | current Sparrow `b-albano-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000124Z-47c6f992/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:27.572004+00:00 | current Sparrow `b-albano-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000126Z-e5fca898/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:29.078628+00:00 | current Sparrow `b-blaz1-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000127Z-f33f7e5d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:31.380820+00:00 | current Sparrow `b-blaz1-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000129Z-c68c7112/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:33.651032+00:00 | current Sparrow `b-blaz1-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000131Z-d6f8164c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:34.495212+00:00 | SVGnest `b-shirts-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 8.846153846153847 | [record](output/playwright/svgnest/20261012T000027Z-fbeaa905/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:01:40.555925+00:00 | deepnest-next `b-jakobs1-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 3.9166666666666665 | [record](output/playwright/deepnest/20261012T000029Z-f6948132/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:01:45.604577+00:00 | current Sparrow `b-marques-strip-sheet` seed 1, 60s, upstream-default, axis y | valid | score 0.9889966634615385 | [record](output/sparrow-benchmark/20261012T000043Z-c1955084/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:47.115413+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000145Z-0d735d97/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:48.646189+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000147Z-b8db2c0f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:50.126084+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000148Z-fb9364c8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:51.609880+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000150Z-fcacf2b1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:53.169176+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000151Z-ebc42559/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:54.656226+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000153Z-c77c7efc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:56.191007+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000154Z-f1d0421b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:57.753112+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000156Z-fe3da3a9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:01:59.297883+00:00 | current Sparrow `b-shirts-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000157Z-a9479ddb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:00.828568+00:00 | current Sparrow `b-swim-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000159Z-15e0e9d1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:19.787557+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 4.673112124999999 | [record](output/playwright/svgnest/20261012T000113Z-d838a552/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:02:33.930148+00:00 | deepnest-next `b-jakobs1-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.775 | [record](output/playwright/deepnest/20261012T000121Z-f87036a5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:02:36.581322+00:00 | current Sparrow `b-dagli-strip-sheet` seed 2, 60s, upstream-default, axis y | valid | score 0.8905800666666667 | [record](output/sparrow-benchmark/20261012T000133Z-0a8550ae/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:38.164540+00:00 | current Sparrow `b-fu-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000236Z-25296470/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:39.583853+00:00 | current Sparrow `b-fu-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000238Z-67c7fa65/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:41.065415+00:00 | current Sparrow `b-fu-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000239Z-c0614a0c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:41.601206+00:00 | SVGnest `b-shirts-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.6881944750000004 | [record](output/playwright/svgnest/20261012T000135Z-0c656807/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:02:42.730973+00:00 | current Sparrow `b-jakobs1-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000241Z-570a2d16/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:44.213203+00:00 | current Sparrow `b-jakobs1-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000242Z-35798533/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:02:51.155764+00:00 | deepnest-next `b-jakobs1-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.9166666666666665 | [record](output/playwright/deepnest/20261012T000140Z-177647f2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:03:25.708548+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T000219Z-27946865/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:03:44.216326+00:00 | deepnest-next `b-jakobs2-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 3.5833333333333335 | [record](output/playwright/deepnest/20261012T000234Z-2d13bca8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:03:45.958624+00:00 | current Sparrow `b-jakobs1-strip-sheet` seed 2, 60s, upstream-default, axis y | valid | score 0.70069045 | [record](output/sparrow-benchmark/20261012T000244Z-427f0061/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:03:47.316154+00:00 | SVGnest `b-swim-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 5.559897677669457 | [record](output/playwright/svgnest/20261012T000241Z-44d882e6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:03:47.558038+00:00 | current Sparrow `b-jakobs2-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000345Z-bb334d74/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:03:49.194299+00:00 | current Sparrow `b-jakobs2-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000347Z-b2940907/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:04:31.157118+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T000325Z-970e39f5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:04:51.140331+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 2, 60s, upstream-default, axis y | valid | score 0.7611987 | [record](output/sparrow-benchmark/20261012T000349Z-a9923118/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:04:52.810451+00:00 | current Sparrow `b-mao-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000451Z-d66ea182/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:04:53.247949+00:00 | SVGnest `b-swim-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 5.411555827794429 | [record](output/playwright/svgnest/20261012T000347Z-1af74ac3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:04:54.408030+00:00 | current Sparrow `b-mao-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000452Z-39939acc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:04:55.116173+00:00 | deepnest-next `b-jakobs2-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.5833333333333335 | [record](output/playwright/deepnest/20261012T000344Z-56a389f7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:05:37.783253+00:00 | SVGnest `b-mao-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 2.5109634056517773 | [record](output/playwright/svgnest/20261012T000431Z-a1b96bd2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:05:56.269895+00:00 | current Sparrow `b-mao-strip-sheet` seed 2, 60s, upstream-default, axis y | valid | score 0.8019373756862745 | [record](output/sparrow-benchmark/20261012T000454Z-c4ffc77b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:05:59.686522+00:00 | verified deepnest batch `20261011T235914Z-748a8872` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T000559Z-093fa0f0.md). Provisional; all failures retained.

- 2026-10-12T00:06:00.028846+00:00 | verified deepnest batch `20261012T000120Z-faf50546` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T000600Z-ec855071.md). Provisional; all failures retained.

- 2026-10-12T00:06:00.430230+00:00 | SVGnest `b-swim-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.29195511891516 | [record](output/playwright/svgnest/20261012T000453Z-0bb1b798/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:06:01.053056+00:00 | verified sparrow batch `20261011T234747Z-cd587f00` | 13/13 valid | [table](benchmarks/results/sparrow-20261012T000601Z-d8be7ddf.md). Provisional; all failures retained.

- 2026-10-12T00:06:01.492609+00:00 | verified sparrow batch `20261011T235600Z-354856ab` | 5/30 valid | [table](benchmarks/results/sparrow-20261012T000601Z-cfe294c3.md). Provisional; all failures retained.

- 2026-10-12T00:06:44.351435+00:00 | SVGnest `b-mao-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 2.426962810088119 | [record](output/playwright/svgnest/20261012T000538Z-1ae98fe6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:06:48.456144+00:00 | current Sparrow `b-swim-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000646Z-50886ccb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:50.111737+00:00 | current Sparrow `b-swim-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000648Z-fc6c35c2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:51.802541+00:00 | current Sparrow `b-trousers-nest-mb-free` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000650Z-b269af48/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:53.369036+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000651Z-f736ea2b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:54.945752+00:00 | current Sparrow `b-trousers-strip-sheet` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000653Z-30f2045a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:58.138395+00:00 | current Sparrow `b-marques-strip-sheet` seed 2, 60s, upstream-default, axis y | valid | score 0.9944607692307693 | [record](output/sparrow-benchmark/20261012T000556Z-ab957185/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:58.248102+00:00 | current Sparrow `b-swim-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000656Z-ed240796/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:59.892331+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000658Z-2bf22714/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:06:59.911391+00:00 | current Sparrow `b-swim-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000658Z-807ade7c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:01.636059+00:00 | current Sparrow `b-trousers-nest-mb-free` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000659Z-0b38f024/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:01.662549+00:00 | current Sparrow `b-shapes0-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000659Z-ab38bf6e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:03.321152+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000701Z-6a5b8598/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:03.338687+00:00 | current Sparrow `b-shapes0-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000701Z-d4d38918/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:05.011199+00:00 | current Sparrow `b-shapes1-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000703Z-c2ddb922/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:05.037216+00:00 | current Sparrow `b-trousers-strip-sheet` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000703Z-5f127ba5/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:06.724789+00:00 | current Sparrow `b-shapes1-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000705Z-486eff40/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:08.289049+00:00 | SVGnest `b-trousers-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 3.8045889265536723 | [record](output/playwright/svgnest/20261012T000600Z-ed5e18a1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:07:08.426672+00:00 | current Sparrow `b-shapes1-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000706Z-162fd953/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:10.282666+00:00 | current Sparrow `b-shirts-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000708Z-e406122a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:11.917124+00:00 | current Sparrow `b-shirts-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000710Z-b9594a82/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:12.269061+00:00 | current Sparrow `b-swim-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000710Z-0917976e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:13.572909+00:00 | current Sparrow `b-shirts-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000711Z-e3453c23/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:13.977146+00:00 | current Sparrow `b-swim-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000712Z-00a88a15/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:15.196562+00:00 | current Sparrow `b-swim-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000713Z-769e2828/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:15.536384+00:00 | current Sparrow `b-trousers-nest-mb-free` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000713Z-2d630ab2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:17.231076+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000715Z-02a7480e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:18.939836+00:00 | current Sparrow `b-trousers-strip-sheet` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000717Z-85d7e86b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:07:27.545109+00:00 | deepnest-next `b-mao-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.8543540537254902 | [record](output/playwright/deepnest/20261012T000612Z-4a690a0d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:07:27.789727+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 2, 60s, identical, axis y | valid | material 0.8464285857142857 | [record](output/playwright/deepnest/20261012T000612Z-05974c41/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:07:34.846552+00:00 | sparrow S identical, 60 s: 39/39 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T000734Z-b8960d59.md). No final gate.

- 2026-10-12T00:07:38.139277+00:00 | sparrow S upstream-default, 60 s: 39/39 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T000738Z-c8a95335.md). No final gate.

- 2026-10-12T00:07:51.350655+00:00 | SVGnest `b-mao-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 0.8773284019607843 | [record](output/playwright/svgnest/20261012T000644Z-5d9a942c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:08:15.542783+00:00 | SVGnest `b-trousers-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 3.3111690621468925 | [record](output/playwright/svgnest/20261012T000708Z-f626ddd2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:08:34.586363+00:00 | current Sparrow `m-box-batch-500` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000831Z-ac5d0a7f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:36.732226+00:00 | current Sparrow `m-box-desktop` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000834Z-c5695de3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:38.422469+00:00 | current Sparrow `m-box-long` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000836Z-efb0777d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:40.045577+00:00 | current Sparrow `m-box-mini` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000838Z-1fd5c360/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:41.693667+00:00 | current Sparrow `m-box-storage` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000840Z-315bb013/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:41.896168+00:00 | current Sparrow `m-box-batch-500` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000840Z-d2a37b32/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:41.786419+00:00 | deepnest-next `b-marques-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.1442307692307692 | [record](output/playwright/deepnest/20261012T000727Z-732815ad/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:08:41.961662+00:00 | deepnest-next `b-mao-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 1.8298221956852023 | [record](output/playwright/deepnest/20261012T000728Z-199bb750/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:08:43.434466+00:00 | current Sparrow `m-box-tool` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000841Z-2a20cbe4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:43.530663+00:00 | current Sparrow `m-box-desktop` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000841Z-f92041b2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:45.120056+00:00 | current Sparrow `m-box-long` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000843Z-14e64179/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:46.801422+00:00 | current Sparrow `m-box-mini` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000845Z-870a0587/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:48.500134+00:00 | current Sparrow `m-box-storage` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000846Z-06799f37/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:49.756296+00:00 | verified sparrow batch `20261012T000121Z-70bfc9e4` | 5/30 valid | [table](benchmarks/results/sparrow-20261012T000849Z-88793b3d.md). Provisional; all failures retained.

- 2026-10-12T00:08:50.066390+00:00 | verified sparrow batch `20261012T000643Z-bed8122f` | 0/5 valid | [table](benchmarks/results/sparrow-20261012T000850Z-a6176822.md). Provisional; all failures retained.

- 2026-10-12T00:08:50.208619+00:00 | current Sparrow `m-box-tool` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T000848Z-8fc6e406/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:08:50.438723+00:00 | verified sparrow batch `20261012T000655Z-8d2ff019` | 0/5 valid | [table](benchmarks/results/sparrow-20261012T000850Z-5938cf88.md). Provisional; all failures retained.

- 2026-10-12T00:08:50.723454+00:00 | verified sparrow batch `20261012T000705Z-c5728660` | 0/5 valid | [table](benchmarks/results/sparrow-20261012T000850Z-99294abd.md). Provisional; all failures retained.

- 2026-10-12T00:08:52.047374+00:00 | sparrow B upstream-default, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T000852Z-599890ec.md). No final gate.

- 2026-10-12T00:08:57.832784+00:00 | SVGnest `b-marques-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 1.2019230769230769 | [record](output/playwright/svgnest/20261012T000751Z-7fa6ae50/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:09:21.841774+00:00 | SVGnest `b-trousers-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.2658227848101267 | [record](output/playwright/svgnest/20261012T000815Z-602ea830/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:09:46.466026+00:00 | current Sparrow `m-garment-bruce-1` seed 1, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T000843Z-00fc5498/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:09:53.205149+00:00 | current Sparrow `m-garment-bruce-1` seed 2, 60s, identical, axis y | valid | score 0.19621319600000006 | [record](output/sparrow-benchmark/20261012T000850Z-981c0a3f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:09:58.055755+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 7.476190476190476 | [record](output/playwright/deepnest/20261012T000842Z-f16ca037/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:09:59.295035+00:00 | deepnest-next `b-mao-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 2.171376481312671 | [record](output/playwright/deepnest/20261012T000842Z-3dff45e5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:10:04.128327+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T000858Z-62740f43/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:10:49.019826+00:00 | current Sparrow `m-garment-bruce-2` seed 1, 60s, identical, axis y | valid | score 0.42439584374999995 | [record](output/sparrow-benchmark/20261012T000946Z-f721713f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:10:56.675456+00:00 | current Sparrow `m-garment-bruce-2` seed 2, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T000953Z-ed2bb5b5/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:11:09.616822+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 8.80952380952381 | [record](output/playwright/svgnest/20261012T001004Z-fcaf8833/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:11:12.724870+00:00 | verified deepnest batch `20261012T000602Z-4c0794dd` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T001112Z-2bf8bddc.md). Provisional; all failures retained.

- 2026-10-12T00:11:13.131626+00:00 | verified deepnest batch `20261012T000603Z-f22ab30b` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T001113Z-668d11de.md). Provisional; all failures retained.

- 2026-10-12T00:11:55.576659+00:00 | current Sparrow `m-garment-bruce-3` seed 1, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001049Z-c95f67b8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:12:04.461590+00:00 | current Sparrow `m-garment-bruce-3` seed 2, 60s, identical, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001056Z-85682f7d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:12:16.826743+00:00 | SVGnest `b-shapes0-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261012T001109Z-0d4710a9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:12:35.236612+00:00 | verified svgnest batch `20261011T235702Z-96fa4c21` | 9/11 valid | [table](benchmarks/results/svgnest-20261012T001235Z-77a01b73.md). Provisional; all failures retained.

- 2026-10-12T00:12:37.742497+00:00 | deepnest-next `b-shapes1-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 7.571428571428571 | [record](output/playwright/deepnest/20261012T001117Z-c93826c9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:12:37.950654+00:00 | deepnest-next `b-shapes0-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 7.571428571428571 | [record](output/playwright/deepnest/20261012T001116Z-8a5c6078/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12 | Existing-sheet repair: sheet jobs: 35/35 valid | [diagnostic](benchmarks/results/repack-sheet-20261012T000748Z-0c7fac06.md). Full failures retained; no quality-gate claim.

- 2026-10-12 | Existing-sheet repair: maker jobs: 29/30 valid | [diagnostic](benchmarks/results/repack-maker-20261012T000758Z-533d7bb1.md). Full failures retained; no quality-gate claim.

- 2026-10-12T00:13:12.458955+00:00 | current Sparrow `m-garment-teagan-1` seed 1, 60s, identical, axis y | valid | score 0.762283004 | [record](output/sparrow-benchmark/20261012T001155Z-e493352f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:13.109848+00:00 | current Sparrow `m-garment-teagan-1` seed 2, 60s, identical, axis y | valid | score 0.7824918663333332 | [record](output/sparrow-benchmark/20261012T001204Z-f2071cf2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:14.363046+00:00 | current Sparrow `m-garment-teagan-2` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001312Z-80e6b4c0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:15.297042+00:00 | current Sparrow `m-garment-teagan-2` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001313Z-a2ca5262/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:16.208385+00:00 | current Sparrow `m-garment-teagan-3` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001314Z-429e8cf9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:17.059609+00:00 | current Sparrow `m-garment-teagan-3` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001315Z-f9a976e6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:17.948244+00:00 | current Sparrow `m-mechanical-batch-1000` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001316Z-4c711829/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:18.808985+00:00 | current Sparrow `m-mechanical-batch-1000` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001317Z-589f3158/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:19.605402+00:00 | current Sparrow `m-mechanical-cog-washers` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001317Z-cf21622a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:20.520920+00:00 | current Sparrow `m-mechanical-cog-washers` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001318Z-0325f995/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:21.225461+00:00 | current Sparrow `m-mechanical-defective-stock` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001319Z-a85a7f8d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:22.166591+00:00 | current Sparrow `m-mechanical-defective-stock` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001320Z-d1c179ca/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:22.941979+00:00 | current Sparrow `m-mechanical-frame-inserts` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001321Z-a1370c4d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:23.766828+00:00 | current Sparrow `m-mechanical-frame-inserts` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001322Z-7788f7cb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:24.646850+00:00 | current Sparrow `m-mechanical-large-plates` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001322Z-da57260f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:25.413370+00:00 | current Sparrow `m-mechanical-large-plates` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001323Z-097f3507/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:26.323232+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001324Z-71606829/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:27.048253+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001325Z-97889c36/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:27.051762+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 1, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T001217Z-e7c4b906/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:13:28.003005+00:00 | current Sparrow `m-mechanical-mounting-kit` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001326Z-a727e543/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:28.704906+00:00 | current Sparrow `m-mechanical-mounting-kit` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001327Z-839cb637/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:29.762986+00:00 | current Sparrow `m-mechanical-panel-hardware` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001328Z-96e4ff69/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:30.433450+00:00 | current Sparrow `m-mechanical-panel-hardware` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001328Z-0625e838/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:31.487671+00:00 | current Sparrow `m-mechanical-remnant-kit` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001329Z-2e05bea0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:32.105424+00:00 | current Sparrow `m-mechanical-remnant-kit` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001330Z-0d740ecb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:33.173136+00:00 | current Sparrow `m-mechanical-small-brackets` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001331Z-feacc0aa/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:33.835252+00:00 | current Sparrow `m-mechanical-small-brackets` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001332Z-4589515c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:34.822954+00:00 | current Sparrow `m-public-gear-1` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001333Z-db982602/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:35.578032+00:00 | current Sparrow `m-public-gear-1` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001333Z-4e1f165a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:36.645963+00:00 | current Sparrow `m-public-gear-2` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001334Z-a229a29e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:37.244986+00:00 | current Sparrow `m-public-gear-2` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001335Z-56268384/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:38.321609+00:00 | current Sparrow `m-public-gear-3` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001336Z-219042c0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:38.839494+00:00 | current Sparrow `m-public-gear-3` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001337Z-9cdd9450/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:39.916534+00:00 | current Sparrow `m-public-gear-4` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001338Z-43de4e6f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:40.495350+00:00 | current Sparrow `m-public-gear-4` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001338Z-d7a2216b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:41.563627+00:00 | current Sparrow `m-sign-1` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001339Z-26d4fc64/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:42.065831+00:00 | current Sparrow `m-sign-1` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001340Z-c5792424/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:43.239803+00:00 | current Sparrow `m-sign-2` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001341Z-95d6324a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:43.720140+00:00 | current Sparrow `m-sign-2` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001342Z-be061d78/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:45.210338+00:00 | current Sparrow `m-sign-3` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001343Z-53fe99fb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:45.543043+00:00 | current Sparrow `m-sign-3` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001343Z-fd6c390d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:47.238367+00:00 | current Sparrow `m-sign-4` seed 1, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001345Z-fac99456/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:48.113825+00:00 | current Sparrow `m-sign-4` seed 2, 60s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001345Z-192a78b4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:13:49.798443+00:00 | SVGnest `b-albano-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 3.603022044825313 | [record](output/playwright/svgnest/20261012T001238Z-b39ea88e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:14:02.089853+00:00 | verified svgnest batch `20261011T234635Z-0d229636` | 17/24 valid | [table](benchmarks/results/svgnest-20261012T001402Z-6a54b62e.md). Provisional; all failures retained.

- 2026-10-12T00:14:22.606396+00:00 | deepnest-next `b-shapes1-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.5 | [record](output/playwright/deepnest/20261012T001239Z-303d2367/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:14:27.173173+00:00 | deepnest-next `b-shapes0-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.775 | [record](output/playwright/deepnest/20261012T001239Z-1f326a59/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:14:43.169638+00:00 | verified sparrow batch `20261012T000829Z-6328f200` | 2/30 valid | [table](benchmarks/results/sparrow-20261012T001443Z-dbbc5bbd.md). Provisional; all failures retained.

- 2026-10-12T00:14:43.588179+00:00 | verified sparrow batch `20261012T000838Z-1b98feb8` | 2/30 valid | [table](benchmarks/results/sparrow-20261012T001443Z-83ef5775.md). Provisional; all failures retained.

- 2026-10-12T00:14:49.174247+00:00 | current Sparrow `m-box-batch-500` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001446Z-65ff3c8b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:14:50.953234+00:00 | current Sparrow `m-box-desktop` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001449Z-b5cb5973/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:14:52.723722+00:00 | current Sparrow `m-box-long` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001450Z-6e93138c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:14:54.480122+00:00 | current Sparrow `m-box-mini` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001452Z-9167a932/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:14:56.225554+00:00 | current Sparrow `m-box-storage` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001454Z-cb9dd6a8/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:14:57.903892+00:00 | current Sparrow `m-box-tool` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001456Z-41c17081/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:14:58.345116+00:00 | SVGnest `b-albano-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 4.161722698308064 | [record](output/playwright/svgnest/20261012T001350Z-21c5e259/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:14:58.485587+00:00 | current Sparrow `m-box-batch-500` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001456Z-2bfa1d54/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:00.186672+00:00 | current Sparrow `m-box-desktop` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001458Z-c0a8c9bb/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:01.966543+00:00 | current Sparrow `m-box-long` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001500Z-660f7524/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:03.797345+00:00 | current Sparrow `m-box-mini` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001501Z-84db3b77/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:05.606158+00:00 | current Sparrow `m-box-storage` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001503Z-7f365ca3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:07.380679+00:00 | current Sparrow `m-box-tool` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001505Z-01552cbd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:09.099218+00:00 | current Sparrow `m-box-batch-500` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001507Z-6af2a076/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:10.888846+00:00 | current Sparrow `m-box-desktop` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001509Z-d5de247a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:12.644209+00:00 | current Sparrow `m-box-long` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001510Z-2822907d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:13.220011+00:00 | SVGnest `b-shapes1-nest-mb-given` seed 2, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T001404Z-e27afdf2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:15:14.405730+00:00 | current Sparrow `m-box-mini` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001512Z-77e63bc2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:16.194327+00:00 | current Sparrow `m-box-storage` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001514Z-6272bc1f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:17.923949+00:00 | current Sparrow `m-box-tool` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T001516Z-31bdb134/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:15:37.247351+00:00 | deepnest-next `b-shirts-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 7.410256410256411 | [record](output/playwright/deepnest/20261012T001422Z-e253b923/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:15:41.028054+00:00 | deepnest-next `b-shapes1-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 7.571428571428571 | [record](output/playwright/deepnest/20261012T001427Z-dadf0a76/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:16:19.399584+00:00 | current Sparrow `m-garment-bruce-1` seed 0, 60s, upstream-default, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001457Z-e765f342/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:16:34.917374+00:00 | current Sparrow `m-garment-bruce-1` seed 2, 60s, upstream-default, axis y | valid | score 0.19623193366666666 | [record](output/sparrow-benchmark/20261012T001517Z-c8554e22/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:16:34.915374+00:00 | current Sparrow `m-garment-bruce-1` seed 1, 60s, upstream-default, axis y | valid | score 0.19581479666666665 | [record](output/sparrow-benchmark/20261012T001507Z-9eacc193/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:16:38.954120+00:00 | SVGnest `b-shapes1-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.625 | [record](output/playwright/svgnest/20261012T001513Z-f3f791a2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:16:39.884357+00:00 | verified deepnest batch `20261012T001114Z-83c301ff` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T001639Z-84b0a068.md). Provisional; all failures retained.

- 2026-10-12T00:16:54.335105+00:00 | verified deepnest batch `20261012T001115Z-2a0892e8` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T001654Z-6398a871.md). Provisional; all failures retained.

- 2026-10-12T00:17:51.428821+00:00 | SVGnest `b-albano-strip-sheet` seed 2, 60s, expanded, axis y | timeout | material None | [record](output/playwright/svgnest/20261012T001458Z-b53f6c7c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:18:44.438050+00:00 | current Sparrow `m-garment-bruce-2` seed 0, 60s, upstream-default, axis y | valid | score 0.42302783450000003 | [record](output/sparrow-benchmark/20261012T001620Z-da7f8f0a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:18:44.435538+00:00 | current Sparrow `m-garment-bruce-2` seed 2, 60s, upstream-default, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001634Z-bb42c5a5/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:18:51.634770+00:00 | current Sparrow `m-garment-bruce-2` seed 1, 60s, upstream-default, axis y | valid | score 0.42682101699999997 | [record](output/sparrow-benchmark/20261012T001635Z-1e40525c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12 | 1,000-part timing trace: 90-second watchdog before third construction pass completed; repair not reached | [trace](benchmarks/results/repair-timing-20261012T001132Z.md). Development diagnostic, no G4 claim.

- 2026-10-12T00:21:04.686930+00:00 | current Sparrow `m-garment-bruce-3` seed 2, 60s, upstream-default, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001844Z-4a5cf81a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:21:05.288493+00:00 | current Sparrow `m-garment-bruce-3` seed 0, 60s, upstream-default, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001844Z-58420bf7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:21:07.145121+00:00 | current Sparrow `m-garment-bruce-3` seed 1, 60s, upstream-default, axis y | invalid | score None | [record](output/sparrow-benchmark/20261012T001851Z-13d1b736/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:21:12.043795+00:00 | SVGnest `b-shirts-nest-mb-free` seed 2, 60s, expanded, axis y | timeout | material None | [record](output/playwright/svgnest/20261012T001704Z-8841cada/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:21:15.375441+00:00 | SVGnest `b-blaz1-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 18.579967066666665 | [record](output/playwright/svgnest/20261012T001853Z-fc6fa7bc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:21:29.368664+00:00 | deepnest-next `b-shirts-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 8.35897435897436 | [record](output/playwright/deepnest/20261012T001930Z-b91ff318/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:21:30.982062+00:00 | deepnest-next `b-swim-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 4.612620819358099 | [record](output/playwright/deepnest/20261012T002011Z-d2bc1b9f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:22:06.894022+00:00 | current Sparrow `m-garment-teagan-1` seed 2, 60s, upstream-default, axis y | valid | score 0.7629377483333334 | [record](output/sparrow-benchmark/20261012T002104Z-96902a51/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:07.546009+00:00 | current Sparrow `m-garment-teagan-1` seed 0, 60s, upstream-default, axis y | valid | score 0.7626814826666666 | [record](output/sparrow-benchmark/20261012T002105Z-e417d35c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:08.536131+00:00 | current Sparrow `m-garment-teagan-2` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002206Z-294b8a2c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:09.179966+00:00 | current Sparrow `m-garment-teagan-2` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002207Z-0c7274e4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:09.340096+00:00 | current Sparrow `m-garment-teagan-1` seed 1, 60s, upstream-default, axis y | valid | score 0.7625963179999999 | [record](output/sparrow-benchmark/20261012T002107Z-d757a8d9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:10.165755+00:00 | current Sparrow `m-garment-teagan-3` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002208Z-1af7fbd6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:10.867241+00:00 | current Sparrow `m-garment-teagan-3` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002209Z-f9af7841/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:10.979232+00:00 | current Sparrow `m-garment-teagan-2` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002209Z-a899aca1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:11.781945+00:00 | current Sparrow `m-mechanical-batch-1000` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002210Z-e8ab4857/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:12.489872+00:00 | current Sparrow `m-mechanical-batch-1000` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002210Z-8af987fc/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:12.584071+00:00 | current Sparrow `m-garment-teagan-3` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002210Z-f3ebbe55/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:13.313978+00:00 | current Sparrow `m-mechanical-cog-washers` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002211Z-3f2b89ff/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:14.073201+00:00 | current Sparrow `m-mechanical-cog-washers` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002212Z-cf10ca9b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:14.125163+00:00 | current Sparrow `m-mechanical-batch-1000` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002212Z-50462f60/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:14.805951+00:00 | current Sparrow `m-mechanical-defective-stock` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002213Z-a460072c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:15.710275+00:00 | current Sparrow `m-mechanical-defective-stock` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002214Z-1cd67dad/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:15.716275+00:00 | current Sparrow `m-mechanical-cog-washers` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002214Z-4315d078/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:16.310996+00:00 | current Sparrow `m-mechanical-frame-inserts` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002214Z-f78bbe27/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:17.321324+00:00 | current Sparrow `m-mechanical-frame-inserts` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002215Z-af5fd5c1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:17.361965+00:00 | current Sparrow `m-mechanical-defective-stock` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002215Z-7f19ee07/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:17.820140+00:00 | current Sparrow `m-mechanical-large-plates` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002216Z-74926403/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:18.928635+00:00 | current Sparrow `m-mechanical-frame-inserts` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002217Z-0f513250/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:18.939664+00:00 | current Sparrow `m-mechanical-large-plates` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002217Z-e20eb271/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:19.376595+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002217Z-6811cb72/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:19.287956+00:00 | SVGnest `b-shirts-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 8.871794871794872 | [record](output/playwright/svgnest/20261012T002112Z-034e59fe/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:22:20.543881+00:00 | current Sparrow `m-mechanical-large-plates` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002218Z-20040d52/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:20.553887+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002218Z-c52eef20/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:20.933656+00:00 | current Sparrow `m-mechanical-mounting-kit` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002219Z-44bbb203/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:22.147683+00:00 | current Sparrow `m-mechanical-mounting-kit` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002220Z-fe759826/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:22.191059+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002220Z-1df6e196/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:22.493808+00:00 | current Sparrow `m-mechanical-panel-hardware` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002220Z-0f6a7a50/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:22.849779+00:00 | SVGnest `b-blaz1-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 15.533333333333333 | [record](output/playwright/svgnest/20261012T002115Z-c6c9fffa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:22:23.763993+00:00 | current Sparrow `m-mechanical-panel-hardware` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002222Z-68c5cd8d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:23.776515+00:00 | current Sparrow `m-mechanical-mounting-kit` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002222Z-db372ee9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:24.039033+00:00 | current Sparrow `m-mechanical-remnant-kit` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002222Z-0005ab2a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:25.344821+00:00 | current Sparrow `m-mechanical-panel-hardware` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002223Z-263c4fdd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:25.393585+00:00 | current Sparrow `m-mechanical-remnant-kit` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002223Z-11fdffb3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:25.670943+00:00 | current Sparrow `m-mechanical-small-brackets` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002224Z-e4e98948/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:27.061787+00:00 | current Sparrow `m-mechanical-small-brackets` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002225Z-0468a130/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:27.078570+00:00 | current Sparrow `m-mechanical-remnant-kit` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002225Z-2a8581e3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:27.318645+00:00 | current Sparrow `m-public-gear-1` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002225Z-bf94fe74/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:28.752837+00:00 | current Sparrow `m-mechanical-small-brackets` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002227Z-04998ec3/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:28.759892+00:00 | current Sparrow `m-public-gear-1` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002227Z-b213b6c9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:28.910886+00:00 | current Sparrow `m-public-gear-2` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002227Z-a445b7cf/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:30.398678+00:00 | current Sparrow `m-public-gear-1` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002228Z-18272024/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:30.447245+00:00 | current Sparrow `m-public-gear-2` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002228Z-7f99c956/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:30.527193+00:00 | current Sparrow `m-public-gear-3` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002228Z-06df9c0c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:32.019434+00:00 | current Sparrow `m-public-gear-2` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002230Z-f67bdd0b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:32.086078+00:00 | current Sparrow `m-public-gear-3` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002230Z-dd3938ae/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:32.143658+00:00 | current Sparrow `m-public-gear-4` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002230Z-36aabc7c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:33.689514+00:00 | current Sparrow `m-public-gear-3` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002232Z-b4b0dc52/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:33.728989+00:00 | current Sparrow `m-public-gear-4` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002232Z-bb75028b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:33.747005+00:00 | current Sparrow `m-sign-1` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002232Z-c9be77bd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:35.440825+00:00 | current Sparrow `m-sign-1` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002233Z-72bdfdb0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:35.487814+00:00 | current Sparrow `m-sign-2` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002233Z-0b18fc31/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:35.494814+00:00 | current Sparrow `m-public-gear-4` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002233Z-1abb2aa4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:37.139984+00:00 | current Sparrow `m-sign-2` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002235Z-37c525c9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:37.151405+00:00 | current Sparrow `m-sign-1` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002235Z-5b3af055/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:37.192552+00:00 | current Sparrow `m-sign-3` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002235Z-ed0d8305/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:39.608151+00:00 | current Sparrow `m-sign-3` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002237Z-a876f3fd/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:39.614152+00:00 | current Sparrow `m-sign-2` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002237Z-e71aaa03/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:39.640698+00:00 | current Sparrow `m-sign-4` seed 2, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002237Z-44a4740b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:41.338577+00:00 | current Sparrow `m-sign-3` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002239Z-9b017f87/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:41.383563+00:00 | current Sparrow `m-sign-4` seed 0, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002239Z-ced0f122/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:43.049863+00:00 | current Sparrow `m-sign-4` seed 1, 60s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T002241Z-754fecc4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:22:43.671511+00:00 | deepnest-next `b-shirts-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.560416675 | [record](output/playwright/deepnest/20261012T002129Z-80fc161b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:22:43.890849+00:00 | deepnest-next `b-swim-strip-sheet` seed 2, 60s, identical, axis y | valid | material 1.7021978259735744 | [record](output/playwright/deepnest/20261012T002131Z-7bd8e587/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:23:25.563853+00:00 | SVGnest `b-shirts-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.7104762 | [record](output/playwright/svgnest/20261012T002219Z-f29966bc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:23:29.319683+00:00 | SVGnest `b-blaz1-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 3.6 | [record](output/playwright/svgnest/20261012T002223Z-c73c5103/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:23:54.501482+00:00 | deepnest-next `b-trousers-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 2.6666666666666665 | [record](output/playwright/deepnest/20261012T002244Z-e1b355b9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:23:56.157125+00:00 | deepnest-next `b-swim-nest-mb-free` seed 2, 60s, identical, axis y | failed | material None | [record](output/playwright/deepnest/20261012T002243Z-d2ab1569/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:24:31.728180+00:00 | SVGnest `b-swim-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 5.703071886129198 | [record](output/playwright/svgnest/20261012T002325Z-23078b28/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:24:35.023179+00:00 | SVGnest `b-dagli-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 0.9781609333333333 | [record](output/playwright/svgnest/20261012T002329Z-522e92fa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:25:36.304355+00:00 | SVGnest `b-swim-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 5.246107983485592 | [record](output/playwright/svgnest/20261012T002431Z-d3e0c95f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:25:39.475180+00:00 | SVGnest `b-fu-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 4.7309591428571425 | [record](output/playwright/svgnest/20261012T002435Z-db3955b3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:26:40.850599+00:00 | SVGnest `b-swim-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.316183825278164 | [record](output/playwright/svgnest/20261012T002536Z-f1341695/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:26:43.907998+00:00 | SVGnest `b-fu-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 3.8095238095238093 | [record](output/playwright/svgnest/20261012T002539Z-a17e0f9b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:27:45.653389+00:00 | SVGnest `b-trousers-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 3.6767019887005654 | [record](output/playwright/svgnest/20261012T002640Z-010fd595/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:27:48.428880+00:00 | SVGnest `b-fu-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 1.3711113947368423 | [record](output/playwright/svgnest/20261012T002644Z-20e70871/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:28:50.118163+00:00 | SVGnest `b-trousers-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 3.23728813559322 | [record](output/playwright/svgnest/20261012T002745Z-89f7f341/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:28:53.163039+00:00 | SVGnest `b-jakobs1-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 5.549986499999999 | [record](output/playwright/svgnest/20261012T002748Z-5a326c03/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:29:55.009270+00:00 | SVGnest `b-trousers-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.3164556962025316 | [record](output/playwright/svgnest/20261012T002850Z-c6bcbb89/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:29:57.926559+00:00 | SVGnest `b-jakobs1-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 4.833333333333333 | [record](output/playwright/svgnest/20261012T002853Z-4ab4d88f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:30:21.580710+00:00 | verified sparrow batch `20261012T001444Z-a0a1df4b` | 2/30 valid | [table](benchmarks/results/sparrow-20261012T003021Z-7b1c9087.md). Provisional; all failures retained.

- 2026-10-12T00:30:22.473117+00:00 | verified sparrow batch `20261012T001455Z-d9c3d70b` | 3/30 valid | [table](benchmarks/results/sparrow-20261012T003022Z-7f393fac.md). Provisional; all failures retained.

- 2026-10-12T00:30:23.389886+00:00 | verified sparrow batch `20261012T001505Z-e849c888` | 2/30 valid | [table](benchmarks/results/sparrow-20261012T003023Z-951c6eb0.md). Provisional; all failures retained.

- 2026-10-12T00:30:24.148709+00:00 | verified deepnest batch `20261012T001715Z-c78617cb` | 2/3 valid | [table](benchmarks/results/deepnest-20261012T003024Z-878cdf29.md). Provisional; all failures retained.

- 2026-10-12T00:30:24.898143+00:00 | verified deepnest batch `20261012T001803Z-30fa5823` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T003024Z-7e8f0cfb.md). Provisional; all failures retained.

- 2026-10-12T00:31:01.935744+00:00 | sparrow M upstream-default, 60 s: 90/90 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T003101Z-1ef96148.md). No final gate.

- 2026-10-12T00:31:04.429068+00:00 | sparrow M identical, 60 s: 90/90 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T003104Z-58217447.md). No final gate.

- 2026-10-12T00:31:04.889811+00:00 | SVGnest `b-jakobs1-strip-sheet` seed 2, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T002958Z-e15aaaa9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:31:10.173667+00:00 | sparrow B identical, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T003110Z-83b933da.md). No final gate.

- 2026-10-12T00:31:11.265362+00:00 | verified svgnest batch `20261012T001403Z-e5c41762` | 9/11 valid | [table](benchmarks/results/svgnest-20261012T003111Z-6efc065a.md). Provisional; all failures retained.

- 2026-10-12T00:31:34.297528+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 2, 60s, identical, axis y | valid | material 3.264281231638418 | [record](output/playwright/deepnest/20261012T003023Z-82874fed/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:32:12.344897+00:00 | SVGnest `b-jakobs2-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 4.822759083333334 | [record](output/playwright/svgnest/20261012T003105Z-67ec159c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:32:52.175233+00:00 | deepnest-next `b-trousers-strip-sheet` seed 2, 60s, identical, axis y | valid | material 2.2025316455696204 | [record](output/playwright/deepnest/20261012T003135Z-36205edc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:33:20.292773+00:00 | SVGnest `b-jakobs2-nest-mb-given` seed 2, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T003212Z-89a3e070/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:33:22.032038+00:00 | current Sparrow `b-albano-nest-mb-free` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003320Z-3a240451/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:33:23.466442+00:00 | current Sparrow `b-fu-strip-sheet` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003322Z-f3f77203/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:33:32.705910+00:00 | current Sparrow `b-albano-nest-mb-free` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003330Z-912e8c64/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:33:34.250149+00:00 | current Sparrow `b-fu-strip-sheet` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003332Z-8620bc08/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:33:44.205547+00:00 | current Sparrow `b-albano-nest-mb-free` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003342Z-24967763/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:33:45.872417+00:00 | current Sparrow `b-fu-strip-sheet` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003344Z-c6b31719/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:34:24.879993+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 2, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T003320Z-5715705c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:35:00.968556+00:00 | verified deepnest batch `20261012T003018Z-b31900c4` | 2/2 valid | [table](benchmarks/results/deepnest-20261012T003500Z-77e37855.md). Provisional; all failures retained.

- 2026-10-12T00:35:28.154207+00:00 | deepnest B identical, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T003528Z-1cfd337e.md). No final gate.

- 2026-10-12T00:35:31.744254+00:00 | SVGnest `b-mao-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 2.879296568216348 | [record](output/playwright/svgnest/20261012T003425Z-953b65dc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:36:15.320136+00:00 | deepnest-next `b-albano-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 2.999166395297737 | [record](output/playwright/deepnest/20261012T003502Z-02432225/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:36:16.671899+00:00 | deepnest-next `b-blaz1-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 11.666666666666666 | [record](output/playwright/deepnest/20261012T003502Z-3f954cc2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:36:36.899942+00:00 | SVGnest `b-mao-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 2.4655520455788515 | [record](output/playwright/svgnest/20261012T003531Z-fa132b04/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:37:22.813088+00:00 | deepnest-next `b-albano-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 2.901999560536146 | [record](output/playwright/deepnest/20261012T003615Z-72c5255d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:37:24.150110+00:00 | deepnest-next `b-blaz1-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 9.8 | [record](output/playwright/deepnest/20261012T003616Z-7b8b51c2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:37:41.478703+00:00 | SVGnest `b-mao-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 0.9423974729411765 | [record](output/playwright/svgnest/20261012T003637Z-c995027e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:38:25.586624+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 0, 300s, identical, axis y | valid | score 0.7472568571428572 | [record](output/sparrow-benchmark/20261012T003323Z-985d80db/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:27.039289+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003825Z-fd00bed7/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:28.473086+00:00 | current Sparrow `b-swim-nest-mb-given` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003827Z-8a5cd43b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:29.618457+00:00 | deepnest-next `b-albano-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.9626355618367348 | [record](output/playwright/deepnest/20261012T003722Z-02013d95/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:38:29.910028+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003828Z-9a710c5e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:31.103019+00:00 | deepnest-next `b-blaz1-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 3.6333333333333333 | [record](output/playwright/deepnest/20261012T003724Z-9e401117/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:38:33.572488+00:00 | current Sparrow `m-box-mini` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003832Z-6b35e76d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:35.039187+00:00 | current Sparrow `m-garment-teagan-2` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003833Z-90c2756a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:36.470019+00:00 | current Sparrow `m-mechanical-defective-stock` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003835Z-1a01654a/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:36.989531+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 1, 300s, identical, axis y | valid | score 0.7517478999999999 | [record](output/sparrow-benchmark/20261012T003334Z-4d060b0f/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:38.046346+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 0, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003836Z-4543acee/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:38.663091+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003837Z-8561ded6/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:40.257360+00:00 | current Sparrow `b-swim-nest-mb-given` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003838Z-b5b41c71/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:41.085891+00:00 | current Sparrow `b-albano-nest-mb-free` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003839Z-28bb05ec/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:41.779007+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003840Z-c4b168a9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:42.564989+00:00 | current Sparrow `b-fu-strip-sheet` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003841Z-ab5fc18d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:44.520694+00:00 | current Sparrow `m-box-mini` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003842Z-2928026b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:45.998351+00:00 | current Sparrow `m-garment-teagan-2` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003844Z-0087fd86/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:46.607108+00:00 | SVGnest `b-marques-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 1.1923076923076923 | [record](output/playwright/svgnest/20261012T003741Z-678defe6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:38:47.450542+00:00 | current Sparrow `m-mechanical-defective-stock` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003846Z-b379e2ce/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:48.234323+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 2, 300s, identical, axis y | valid | score 0.7295884857142857 | [record](output/sparrow-benchmark/20261012T003345Z-a1ca9218/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:49.032713+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 1, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003847Z-63626aa1/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:49.651615+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003848Z-0e9bca94/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:51.085933+00:00 | current Sparrow `b-swim-nest-mb-given` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003849Z-bbd80e88/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:52.509657+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003851Z-acace31d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:53.434330+00:00 | current Sparrow `b-albano-nest-mb-free` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003851Z-9018cc04/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:54.844942+00:00 | current Sparrow `b-fu-strip-sheet` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003853Z-3257b454/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:54.894547+00:00 | current Sparrow `m-box-mini` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003853Z-097e0a35/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:56.323313+00:00 | current Sparrow `m-garment-teagan-2` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003854Z-9551706b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:57.760020+00:00 | current Sparrow `m-mechanical-defective-stock` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003856Z-1f760547/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:38:59.185677+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 2, 300s, identical, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003857Z-024c02b5/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:39:01.595099+00:00 | current Sparrow `b-albano-nest-mb-free` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003900Z-25aadaee/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:39:03.034752+00:00 | current Sparrow `b-fu-strip-sheet` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T003901Z-c120010b/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12 | Four-circle prescreen experiment (reverted) | [all outcomes](benchmarks/results/repack-sheet-20261012T002931Z-ee3d3324.md). Development diagnostic; no gate.

- 2026-10-12 | Four-circle prescreen experiment (reverted) | [all outcomes](benchmarks/results/repack-maker-20261012T002920Z-53a2356b.md). Development diagnostic; no gate.

- 2026-10-12 | Stable best-first placement experiment | [all outcomes](benchmarks/results/repack-sheet-20261012T003546Z-05639134.md). Development diagnostic; no gate.

- 2026-10-12 | Stable best-first placement experiment | [all outcomes](benchmarks/results/repack-maker-20261012T003536Z-600978bc.md). Development diagnostic; no gate.

- 2026-10-12T00:39:51.046633+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 8.659419714285715 | [record](output/playwright/svgnest/20261012T003846Z-854200d7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:40:42.052299+00:00 | verified deepnest batch `20261012T003458Z-ded0f797` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T004042Z-5e9ede76.md). Provisional; all failures retained.

- 2026-10-12T00:40:43.339653+00:00 | verified deepnest batch `20261012T003459Z-a8cfa189` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T004043Z-3d77f051.md). Provisional; all failures retained.

- 2026-10-12T00:40:53.706390+00:00 | deepnest-next `b-dagli-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.99 | [record](output/playwright/deepnest/20261012T003945Z-434c0308/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:40:54.890044+00:00 | deepnest-next `b-fu-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.4210526315789473 | [record](output/playwright/deepnest/20261012T003947Z-986c17aa/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:40:55.685271+00:00 | SVGnest `b-shapes0-nest-mb-given` seed 2, 60s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T003951Z-8e0ddc08/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12 | constructor speed experiments, all ten layouts identical; stable cost ordering reduces collision checks by 53%, last matched CPU pair uses 61.76% less CPU time | [diagnostic](benchmarks/results/construct-profile-20261012T0042.md). No G4 claim.

- 2026-10-12T00:42:02.496554+00:00 | SVGnest `b-shapes0-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.825 | [record](output/playwright/svgnest/20261012T004055Z-6f9193eb/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:42:04.598167+00:00 | deepnest-next `b-fu-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 4.8535033809523815 | [record](output/playwright/deepnest/20261012T004054Z-979b0cb5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:42:04.867805+00:00 | deepnest-next `b-jakobs1-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 4.600854 | [record](output/playwright/deepnest/20261012T004055Z-61dace85/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12 | stable best-first placement plus early failed-trial exit | 30/30 valid, 29/29 comparable layouts exactly preserved | [diagnostic](benchmarks/results/repack-maker-20261012T003947Z-73f9cdbc.md). No quality/speed gate.

- 2026-10-12 | stable best-first placement plus early failed-trial exit | 35/35 valid, 35/35 comparable layouts exactly preserved | [diagnostic](benchmarks/results/repack-sheet-20261012T003957Z-29681a27.md). No quality/speed gate.

- 2026-10-12T00:43:08.183833+00:00 | SVGnest `b-shapes1-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 8.659419714285715 | [record](output/playwright/svgnest/20261012T004202Z-f2eb4ac0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:43:13.824633+00:00 | deepnest-next `b-fu-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261012T004204Z-3e4724fe/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:43:14.494431+00:00 | deepnest-next `b-jakobs1-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.9166666666666665 | [record](output/playwright/deepnest/20261012T004205Z-a19d22cf/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:43:27.631835+00:00 | SVGnest `m-box-batch-500` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004212Z-ec192bc8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:43:44.836007+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 0, 300s, upstream-default, axis y | valid | score 0.7443140285714286 | [record](output/sparrow-benchmark/20261012T003842Z-5d1eddf4/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:46.294008+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004344Z-6c9deed9/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:47.714143+00:00 | current Sparrow `b-swim-nest-mb-given` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004346Z-23f53448/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:49.147873+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004347Z-db7a21a2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:51.574718+00:00 | current Sparrow `m-box-mini` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004350Z-ca55498e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:52.965920+00:00 | current Sparrow `m-garment-teagan-2` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004351Z-17becc8d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:54.416024+00:00 | current Sparrow `m-mechanical-defective-stock` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004352Z-fcd8efb0/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:55.831328+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 0, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004354Z-016228c2/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:56.847128+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 1, 300s, upstream-default, axis y | valid | score 0.7414808714285714 | [record](output/sparrow-benchmark/20261012T003854Z-a0564a41/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:58.267463+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004356Z-778ca583/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:43:59.700481+00:00 | current Sparrow `b-swim-nest-mb-given` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004358Z-0e34435c/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:01.102210+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004359Z-4acc5420/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:03.498671+00:00 | current Sparrow `m-box-mini` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004402Z-6ebf56da/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:04.417124+00:00 | verified deepnest batch `20261012T003945Z-9d97571e` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T004404Z-42d802ad.md). Provisional; all failures retained.

- 2026-10-12T00:44:04.908275+00:00 | current Sparrow `m-garment-teagan-2` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004403Z-60141bea/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:05.131894+00:00 | verified deepnest batch `20261012T003946Z-73abd16b` | 3/3 valid | [table](benchmarks/results/deepnest-20261012T004405Z-2d618f63.md). Provisional; all failures retained.

- 2026-10-12T00:44:05.630246+00:00 | current Sparrow `b-jakobs2-strip-sheet` seed 2, 300s, upstream-default, axis y | valid | score 0.7394091 | [record](output/sparrow-benchmark/20261012T003903Z-6ddbfa22/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:06.362045+00:00 | current Sparrow `m-mechanical-defective-stock` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004404Z-124f009e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:07.072781+00:00 | verified svgnest batch `20261012T001237Z-d975d71f` | 19/24 valid | [table](benchmarks/results/svgnest-20261012T004407Z-4610bcb4.md). Provisional; all failures retained.

- 2026-10-12T00:44:07.079288+00:00 | current Sparrow `b-shapes0-nest-mb-free` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004405Z-9f9a3435/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:07.765701+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 1, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004406Z-270eb547/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:08.574238+00:00 | current Sparrow `b-swim-nest-mb-given` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004407Z-a88bc7db/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:09.976027+00:00 | current Sparrow `b-trousers-nest-mb-given` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004408Z-6728953e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:12.327228+00:00 | current Sparrow `m-box-mini` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004410Z-0c28f8ea/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:13.763788+00:00 | current Sparrow `m-garment-teagan-2` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004412Z-2305a96e/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:15.184845+00:00 | current Sparrow `m-mechanical-defective-stock` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004413Z-3b8d086d/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:16.575264+00:00 | current Sparrow `m-mechanical-mixed-stock` seed 2, 300s, upstream-default, axis y | unsupported | score None | [record](output/sparrow-benchmark/20261012T004415Z-2b7984ec/run.json). Provisional single-strip comparison; deadline includes construction.

- 2026-10-12T00:44:31.839718+00:00 | SVGnest `m-box-desktop` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004327Z-784eb22a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:44:55.805306+00:00 | sparrow B identical, 300 s: 18/18 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T004455Z-7ae22fb7.md). No final gate.

- 2026-10-12T00:44:55.869442+00:00 | sparrow M identical, 300 s: 12/12 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T004455Z-aef16b3a.md). No final gate.

- 2026-10-12T00:44:55.985138+00:00 | sparrow B upstream-default, 300 s: 18/18 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T004455Z-ec1e0666.md). No final gate.

- 2026-10-12T00:44:56.048721+00:00 | sparrow M upstream-default, 300 s: 12/12 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T004456Z-d7048476.md). No final gate.

- 2026-10-12T00:45:11.686846+00:00 | deepnest-next `b-jakobs1-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.825 | [record](output/playwright/deepnest/20261012T004403Z-1dfbc0ad/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:45:11.792427+00:00 | deepnest-next `b-jakobs2-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 3.939032708333334 | [record](output/playwright/deepnest/20261012T004404Z-b56b1de9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:45:36.087217+00:00 | SVGnest `m-box-long` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004431Z-22354e14/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:46:15.423414+00:00 | SVGnest `m-box-batch-500` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004457Z-205afacb/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:46:23.692627+00:00 | deepnest-next `b-jakobs2-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.7916666666666665 | [record](output/playwright/deepnest/20261012T004513Z-667928b3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:46:23.718808+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.9724702428571429 | [record](output/playwright/deepnest/20261012T004513Z-43adca7e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:46:40.964589+00:00 | SVGnest `m-box-mini` seed 1, 60s, identical, axis y | valid | material 0.82 | [record](output/playwright/svgnest/20261012T004536Z-8c657250/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:46:41.157142+00:00 | svgnest B expanded, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T004641Z-9dad00a0.md). No final gate.

- 2026-10-12T00:47:20.142493+00:00 | SVGnest `m-box-desktop` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004615Z-2aeb6b6a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:47:32.830240+00:00 | deepnest-next `b-mao-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 2.76853805834093 | [record](output/playwright/deepnest/20261012T004624Z-864703e5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:47:34.007289+00:00 | deepnest-next `b-mao-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 2.8004817429352777 | [record](output/playwright/deepnest/20261012T004624Z-78302977/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:47:45.577018+00:00 | SVGnest `m-box-storage` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004641Z-92d9fec9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:48:13.125139+00:00 | SVGnest `m-box-batch-500` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004701Z-294438e7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12 | all 528 Sparrow development slots accounted for, both budgets and settings, three seeds; {'valid': 127, 'invalid': 43, 'unsupported': 358} | [coverage](benchmarks/results/sparrow-development-20261012T0048.md). No M1 completion or final gate.

- 2026-10-12T00:48:24.294320+00:00 | SVGnest `m-box-batch-500` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004712Z-603612f7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:48:25.464107+00:00 | SVGnest `m-box-long` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004720Z-24f68bc4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:48:35.369778+00:00 | SVGnest `m-box-batch-500` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004722Z-6d2a79c8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:48:47.285084+00:00 | deepnest-next `b-mao-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 0.8897835101960785 | [record](output/playwright/deepnest/20261012T004734Z-0be346e3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:48:47.270228+00:00 | deepnest-next `b-marques-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.2719780192307693 | [record](output/playwright/deepnest/20261012T004735Z-2cf1f551/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:48:51.786915+00:00 | SVGnest `m-box-tool` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004745Z-d6f4568e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:48:57.442545+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 0, 60s, expanded, axis y | failed | material None | [record](output/playwright/deepnest/20261012T004848Z-82af07f1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:49:19.390616+00:00 | SVGnest `m-box-desktop` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004813Z-418b3eae/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:49:29.921805+00:00 | SVGnest `m-box-desktop` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004824Z-50355779/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:49:31.024246+00:00 | SVGnest `m-box-mini` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004825Z-d2fd7413/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:49:42.974276+00:00 | SVGnest `m-box-desktop` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004835Z-1aa08fe1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:49:58.423927+00:00 | SVGnest `m-garment-bruce-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004851Z-1bc588aa/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:49:59.857657+00:00 | deepnest-next `b-shapes0-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 7.809523809523809 | [record](output/playwright/deepnest/20261012T004848Z-76b9b92d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:50:10.947927+00:00 | deepnest-next `b-shapes0-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.9 | [record](output/playwright/deepnest/20261012T004858Z-b4b227ea/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:50:25.611307+00:00 | SVGnest `m-box-long` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004919Z-63a2dd5b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:50:37.822455+00:00 | SVGnest `m-box-long` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004930Z-be36b68f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:50:40.407131+00:00 | SVGnest `m-box-storage` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004931Z-66e562ec/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:50:51.047806+00:00 | SVGnest `m-box-long` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004943Z-fd65d863/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:51:08.197876+00:00 | SVGnest `m-garment-bruce-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T004958Z-5183e52a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:51:19.121120+00:00 | deepnest-next `b-shapes1-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 7.899973857142857 | [record](output/playwright/deepnest/20261012T005002Z-b4dd78fa/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:51:29.055248+00:00 | deepnest-next `b-shapes1-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 7.809523809523809 | [record](output/playwright/deepnest/20261012T005013Z-ccd724bd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:51:35.001759+00:00 | SVGnest `m-box-mini` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005026Z-a526acd8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:51:45.585307+00:00 | SVGnest `m-box-mini` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005038Z-9a750f52/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:51:51.001276+00:00 | SVGnest `m-box-tool` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005040Z-0fec0b04/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:52:00.029982+00:00 | SVGnest `m-box-mini` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005051Z-7e008008/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:52:17.117895+00:00 | SVGnest `m-garment-bruce-3` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005108Z-1150267e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:52:35.875369+00:00 | deepnest-next `b-shapes1-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.55 | [record](output/playwright/deepnest/20261012T005121Z-a15a10e9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:52:43.163061+00:00 | SVGnest `m-box-storage` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005135Z-6e0c7f2f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:52:45.571577+00:00 | deepnest-next `b-shirts-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 7.939641128205128 | [record](output/playwright/deepnest/20261012T005131Z-e41c6fc4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:52:54.872788+00:00 | SVGnest `m-box-storage` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005146Z-7abfc053/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:52:59.991661+00:00 | SVGnest `m-garment-bruce-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005151Z-98b5251f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:53:09.177587+00:00 | SVGnest `m-box-storage` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005200Z-61dec3e9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:53:26.212946+00:00 | SVGnest `m-garment-teagan-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005217Z-7e4de393/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:53:51.429451+00:00 | deepnest-next `b-shirts-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 8.76923076923077 | [record](output/playwright/deepnest/20261012T005238Z-d0619114/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:53:52.601094+00:00 | SVGnest `m-box-tool` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005243Z-ef3de272/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:54:03.560268+00:00 | SVGnest `m-box-tool` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005255Z-edc81efb/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:54:03.678051+00:00 | deepnest-next `b-shirts-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.616071425 | [record](output/playwright/deepnest/20261012T005248Z-6bf1b483/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:54:09.249072+00:00 | SVGnest `m-garment-bruce-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005300Z-1d3c88a3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:54:17.328117+00:00 | SVGnest `m-box-tool` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005309Z-0943d94d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:54:35.809911+00:00 | SVGnest `m-garment-teagan-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005326Z-dfa668c0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:55:01.319648+00:00 | SVGnest `m-garment-bruce-1` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005353Z-6ba3131b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:55:09.977336+00:00 | deepnest-next `b-swim-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 5.628967939249969 | [record](output/playwright/deepnest/20261012T005353Z-ee79dc2f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:55:10.997334+00:00 | SVGnest `m-garment-bruce-1` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005403Z-7438c422/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:55:18.938847+00:00 | SVGnest `m-garment-bruce-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005409Z-63641f0d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:55:24.812693+00:00 | SVGnest `m-garment-bruce-1` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005417Z-dcd247b3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:55:45.271117+00:00 | SVGnest `m-garment-teagan-3` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005435Z-3e379543/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:56:08.023207+00:00 | SVGnest `m-garment-bruce-2` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005501Z-bae896fc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:56:17.115482+00:00 | SVGnest `m-garment-bruce-2` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005511Z-2c528ce4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:56:25.463864+00:00 | SVGnest `m-garment-teagan-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005519Z-ab11bbdb/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:56:27.799583+00:00 | deepnest-next `b-swim-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 1.8012685742350487 | [record](output/playwright/deepnest/20261012T005517Z-86218f0e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:56:31.383435+00:00 | SVGnest `m-garment-bruce-2` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005524Z-d690f15e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:57:01.544322+00:00 | SVGnest `m-mechanical-batch-1000` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005545Z-af28c0fd/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:57:17.058371+00:00 | SVGnest `m-garment-bruce-3` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005608Z-1ac91307/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:57:25.446122+00:00 | SVGnest `m-garment-bruce-3` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005617Z-f7eb147a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:57:33.317007+00:00 | SVGnest `m-garment-teagan-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005625Z-c7be9888/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:57:40.249330+00:00 | SVGnest `m-garment-bruce-3` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005631Z-f8a515b3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:57:45.921808+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 3.361581920903955 | [record](output/playwright/deepnest/20261012T005632Z-fc8ca33e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T00:58:09.779813+00:00 | SVGnest `m-mechanical-cog-washers` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005701Z-3ef62b35/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:58:11.638405+00:00 | SVGnest `m-mechanical-defective-stock` seed 1, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T005809Z-3452bf9b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:58:24.206447+00:00 | SVGnest `m-garment-teagan-1` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005717Z-c64fb987/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:58:31.536967+00:00 | SVGnest `m-garment-teagan-1` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005725Z-0bf559b0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:58:42.046466+00:00 | SVGnest `m-garment-teagan-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005733Z-0c445554/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:58:46.830310+00:00 | SVGnest `m-garment-teagan-1` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005740Z-527d1099/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:59:19.734881+00:00 | SVGnest `m-mechanical-frame-inserts` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005811Z-8caec0b0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:59:32.050098+00:00 | SVGnest `m-garment-teagan-2` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005824Z-030cc0a4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:59:38.340110+00:00 | SVGnest `m-garment-teagan-2` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005831Z-31c2f20b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:59:55.630964+00:00 | SVGnest `m-garment-teagan-2` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005847Z-1a9a4e77/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T00:59:57.615309+00:00 | SVGnest `m-mechanical-batch-1000` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005842Z-ec7908d9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:00:27.989179+00:00 | SVGnest `m-mechanical-large-plates` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005920Z-3784d590/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:00:30.335954+00:00 | SVGnest `m-mechanical-mixed-stock` seed 1, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010028Z-e6fcceb0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:00:41.468710+00:00 | SVGnest `m-garment-teagan-3` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005932Z-291b1e68/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:00:47.156183+00:00 | SVGnest `m-garment-teagan-3` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005938Z-ef51482f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:01:04.271266+00:00 | SVGnest `m-garment-teagan-3` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005955Z-1bd30ba0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:01:05.154371+00:00 | SVGnest `m-mechanical-cog-washers` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T005958Z-b6524393/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:01:07.232241+00:00 | SVGnest `m-mechanical-defective-stock` seed 2, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010105Z-b13363ba/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:01:38.588573+00:00 | SVGnest `m-mechanical-mounting-kit` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010030Z-8d534e09/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:02:00.862401+00:00 | SVGnest `m-mechanical-batch-1000` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010041Z-d5fe6417/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:02:03.725090+00:00 | SVGnest `m-mechanical-batch-1000` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010047Z-f1108714/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:02:15.097824+00:00 | SVGnest `m-mechanical-frame-inserts` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010107Z-58731e0d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:02:19.577477+00:00 | SVGnest `m-mechanical-batch-1000` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010104Z-d99da5a2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:02:47.663601+00:00 | SVGnest `m-mechanical-panel-hardware` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010138Z-7dcf46e7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:02:49.421052+00:00 | SVGnest `m-mechanical-remnant-kit` seed 1, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010247Z-885724cd/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:07.076721+00:00 | SVGnest `m-mechanical-cog-washers` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010201Z-49877725/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:08.737466+00:00 | SVGnest `m-mechanical-defective-stock` seed 0, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010307Z-b43d2294/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:09.665168+00:00 | SVGnest `m-mechanical-cog-washers` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010203Z-fd581bc2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:11.244910+00:00 | SVGnest `m-mechanical-defective-stock` seed 1, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010309Z-6a7ae0da/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:21.100059+00:00 | SVGnest `m-mechanical-large-plates` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010215Z-5cef904e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:22.861513+00:00 | SVGnest `m-mechanical-mixed-stock` seed 2, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010321Z-e68b7243/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:26.205526+00:00 | SVGnest `m-mechanical-cog-washers` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010219Z-a9907a5c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:27.811257+00:00 | SVGnest `m-mechanical-defective-stock` seed 2, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010326Z-5b7ef4e8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:03:31.665102+00:00 | deepnest-next `b-swim-nest-mb-given` seed 0, 60s, expanded, axis y | valid | material 4.890746984951449 | [record](output/playwright/deepnest/20261012T010222Z-ba690049/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:03:35.721700+00:00 | deepnest-next `b-albano-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 3.718118574379257 | [record](output/playwright/deepnest/20261012T010223Z-d5236c7f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:03:56.466196+00:00 | SVGnest `m-mechanical-small-brackets` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010249Z-1cad7ea2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:04:15.089680+00:00 | SVGnest `m-mechanical-frame-inserts` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010308Z-cb1d4d7a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:04:17.253907+00:00 | SVGnest `m-mechanical-frame-inserts` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010311Z-563b142d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:04:28.752047+00:00 | SVGnest `m-mechanical-mounting-kit` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010322Z-b645c449/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:04:34.452901+00:00 | SVGnest `m-mechanical-frame-inserts` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010327Z-6b83411c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:04:44.974032+00:00 | deepnest-next `b-trousers-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 3.718582790960452 | [record](output/playwright/deepnest/20261012T010332Z-01d6f7c3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:04:45.671530+00:00 | deepnest-next `b-albano-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 2.9044536824873655 | [record](output/playwright/deepnest/20261012T010336Z-d656dc0f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:05:05.494503+00:00 | SVGnest `m-public-gear-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010356Z-18e2c5ee/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:21.036461+00:00 | SVGnest `m-mechanical-large-plates` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010415Z-4f70abb6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:22.772451+00:00 | SVGnest `m-mechanical-mixed-stock` seed 0, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010521Z-10d4838c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:23.716869+00:00 | SVGnest `m-mechanical-large-plates` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010417Z-00c58866/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:25.320165+00:00 | SVGnest `m-mechanical-mixed-stock` seed 1, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010523Z-a63bf52a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:36.773657+00:00 | SVGnest `m-mechanical-panel-hardware` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010428Z-49d0d805/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:38.526010+00:00 | SVGnest `m-mechanical-remnant-kit` seed 2, 60s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010536Z-a2a2ac63/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:41.068120+00:00 | SVGnest `m-mechanical-large-plates` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010434Z-b4f05b3d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:42.737092+00:00 | SVGnest `m-mechanical-mixed-stock` seed 2, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010541Z-b65c955e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:05:59.414198+00:00 | deepnest-next `b-trousers-strip-sheet` seed 0, 60s, expanded, axis y | valid | material 2.3485881265822783 | [record](output/playwright/deepnest/20261012T010446Z-d86055d2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:05:59.847459+00:00 | deepnest-next `b-albano-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 1.9000344304081633 | [record](output/playwright/deepnest/20261012T010446Z-5072d8b3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:06:14.898279+00:00 | SVGnest `m-public-gear-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010505Z-4debf1ec/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:06:28.711240+00:00 | SVGnest `m-mechanical-mounting-kit` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010522Z-9d995f2f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:06:30.915638+00:00 | SVGnest `m-mechanical-mounting-kit` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010525Z-143508d5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:06:44.565073+00:00 | SVGnest `m-mechanical-small-brackets` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010538Z-64e107d1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:06:48.579626+00:00 | SVGnest `m-mechanical-mounting-kit` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010542Z-842811ec/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:10.164902+00:00 | deepnest-next `b-blaz1-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 10.894280666666667 | [record](output/playwright/deepnest/20261012T010601Z-a90aca8c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:07:27.077681+00:00 | SVGnest `m-public-gear-3` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010615Z-a0ca0503/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:35.552401+00:00 | SVGnest `m-mechanical-panel-hardware` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010628Z-444b08af/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:37.228915+00:00 | SVGnest `m-mechanical-remnant-kit` seed 0, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010735Z-dbdf4e4e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:37.548918+00:00 | SVGnest `m-mechanical-panel-hardware` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010631Z-b6add4f6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:39.252829+00:00 | SVGnest `m-mechanical-remnant-kit` seed 1, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010737Z-15f3d28c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:52.036292+00:00 | SVGnest `m-public-gear-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010644Z-ac85b899/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:55.492339+00:00 | SVGnest `m-mechanical-panel-hardware` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010648Z-6b9f4d30/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:07:57.040292+00:00 | SVGnest `m-mechanical-remnant-kit` seed 2, 60s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T010755Z-d0c40c83/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:08:24.071729+00:00 | deepnest-next `b-blaz1-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 9.8 | [record](output/playwright/deepnest/20261012T010711Z-290e73d5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:08:35.999438+00:00 | SVGnest `m-public-gear-4` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010727Z-a123dfc0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:08:43.143671+00:00 | SVGnest `m-mechanical-small-brackets` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010737Z-d0ddab3f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:08:44.818781+00:00 | SVGnest `m-mechanical-small-brackets` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010739Z-10545787/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:08:58.819254+00:00 | SVGnest `m-public-gear-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010752Z-6afaf173/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:09:02.303139+00:00 | SVGnest `m-mechanical-small-brackets` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010757Z-f2b7f98e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:09:36.530972+00:00 | deepnest-next `b-blaz1-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 3.6 | [record](output/playwright/deepnest/20261012T010825Z-3aaafba6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:09:42.478892+00:00 | SVGnest `m-sign-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010836Z-825d8b2f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:09:49.755281+00:00 | SVGnest `m-public-gear-1` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010843Z-e103df05/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:09:51.190776+00:00 | SVGnest `m-public-gear-1` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010844Z-d93b6411/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:10:08.091269+00:00 | SVGnest `m-public-gear-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010858Z-4645ed47/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:10:08.705139+00:00 | SVGnest `m-public-gear-1` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010902Z-c5c72998/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:10:49.575761+00:00 | SVGnest `m-sign-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010942Z-b06f3c77/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:10:50.162179+00:00 | deepnest-next `b-dagli-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 0.9614942666666667 | [record](output/playwright/deepnest/20261012T010937Z-1edf992b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:10:56.598629+00:00 | SVGnest `m-public-gear-2` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010949Z-fc1e06b9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:10:58.010265+00:00 | SVGnest `m-public-gear-2` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T010951Z-54f7eece/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:11:14.745967+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 0.8907143 | [record](output/playwright/deepnest/20261012T011005Z-31d1d112/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:11:16.532600+00:00 | SVGnest `m-public-gear-4` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011008Z-6ab83186/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:11:16.586121+00:00 | SVGnest `m-public-gear-2` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011008Z-ed269514/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:11:37.884450+00:00 | Cooperative 15 s deadline and two deterministic work-limit replays on the 1,000-part development job; all valid, identical layouts | [evidence](benchmarks/results/search-control-20261012T0114.md). No G4 claim.

- 2026-10-12T01:11:56.529971+00:00 | SVGnest `m-sign-3` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011049Z-5bb91f87/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:12:02.219709+00:00 | deepnest-next `b-fu-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 5.6520022857142855 | [record](output/playwright/deepnest/20261012T011051Z-4530a078/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:12:06.750096+00:00 | SVGnest `m-public-gear-3` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011056Z-feb2499e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:12:07.709020+00:00 | SVGnest `m-public-gear-3` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011058Z-d48b3cba/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:12:22.192728+00:00 | SVGnest `m-sign-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011116Z-ccf85473/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:12:22.667597+00:00 | deepnest-next `b-mao-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 2.3788598845335764 | [record](output/playwright/deepnest/20261012T011115Z-ca3b0edb/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:12:25.962864+00:00 | SVGnest `m-public-gear-3` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011116Z-b205e2d9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:13:03.096452+00:00 | SVGnest `m-sign-4` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011156Z-3d0a5ad4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:13:10.150782+00:00 | deepnest-next `b-fu-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 3.761904761904762 | [record](output/playwright/deepnest/20261012T011203Z-5ee191cc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:13:14.135807+00:00 | SVGnest `m-public-gear-4` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011206Z-971a4c71/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:13:15.182425+00:00 | SVGnest `m-public-gear-4` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011207Z-921d66b2/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:13:27.841522+00:00 | SVGnest `m-sign-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011222Z-bd5ea9ff/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:13:33.096769+00:00 | deepnest-next `b-mao-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 2.8014882023701 | [record](output/playwright/deepnest/20261012T011223Z-134a177c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:13:33.131090+00:00 | SVGnest `m-public-gear-4` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011226Z-af41c82c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:14:01.903352+00:00 | Before rerunning: declare exactly two Deepnest harness replacements, B swim-free / identical / seed 2 and B shapes0-free / expanded / seed 0, both 60 s. All original records and every replacement outcome retained. [Declaration](benchmarks/results/deepnest-infrastructure-reruns-20261012T0119.json).

- 2026-10-12T01:14:06.648624+00:00 | deepnest-next `b-albano-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 3.480520447593936 | [record](output/playwright/deepnest/20261012T011258Z-3fcddd7c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:14:19.894906+00:00 | SVGnest `m-sign-1` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011314Z-f8c412e0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:14:20.565707+00:00 | SVGnest `m-sign-1` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011315Z-07fe489c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:14:21.128527+00:00 | deepnest-next `b-fu-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 1.8157894736842106 | [record](output/playwright/deepnest/20261012T011311Z-0c7d9275/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:14:33.895562+00:00 | SVGnest `m-sign-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011327Z-5a9c4c67/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:14:38.503874+00:00 | SVGnest `m-sign-1` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011333Z-e4c51a2e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:14:40.541318+00:00 | deepnest-next `b-mao-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 0.8952775584313726 | [record](output/playwright/deepnest/20261012T011334Z-64f05a69/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:15:20.105693+00:00 | deepnest-next `b-albano-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 2.901999560536146 | [record](output/playwright/deepnest/20261012T011407Z-0fa50d6f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:15:25.772498+00:00 | SVGnest `m-sign-2` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011420Z-626bfe3b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:15:26.360081+00:00 | SVGnest `m-sign-2` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011420Z-b6e54a00/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:15:28.724031+00:00 | deepnest-next `b-jakobs1-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 4.666666666666667 | [record](output/playwright/deepnest/20261012T011422Z-45f300da/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:15:40.028816+00:00 | SVGnest `m-sign-4` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011434Z-663003f6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:15:44.245772+00:00 | SVGnest `m-sign-2` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011438Z-f8db7a26/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:15:48.812642+00:00 | deepnest-next `b-marques-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 1.3076923076923077 | [record](output/playwright/deepnest/20261012T011441Z-b8a50752/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:15:50.919918+00:00 | deepnest-next `b-swim-nest-mb-free` seed 2, 60s, identical, axis y | valid | material 4.801038395908773 | [record](output/playwright/deepnest/20261012T011443Z-6e00e129/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:16:31.861429+00:00 | SVGnest `m-sign-3` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011525Z-f2221dc6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:16:32.071043+00:00 | deepnest-next `b-albano-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 1.8906664304081633 | [record](output/playwright/deepnest/20261012T011521Z-43f3b277/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:16:32.366792+00:00 | SVGnest `m-sign-3` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011526Z-68ba4ff8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:16:36.782731+00:00 | deepnest-next `b-jakobs1-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 3.75 | [record](output/playwright/deepnest/20261012T011529Z-c177e5d3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:16:50.087558+00:00 | SVGnest `m-sign-3` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011544Z-1764ca1c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:17:00.134355+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 7.852014523809524 | [record](output/playwright/deepnest/20261012T011549Z-f714cf80/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:17:01.018824+00:00 | svgnest M identical, 60 s: 90/90 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T011701Z-1f75fdda.md). No final gate.

- 2026-10-12T01:17:02.457752+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 0, 60s, expanded, axis y | valid | material 7.899973857142857 | [record](output/playwright/deepnest/20261012T011551Z-114b3846/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:17:37.825648+00:00 | SVGnest `m-sign-4` seed 0, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011631Z-c981c296/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:17:38.178052+00:00 | SVGnest `m-sign-4` seed 1, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011632Z-e58660c7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:17:42.584811+00:00 | deepnest-next `b-blaz1-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 10.666666666666666 | [record](output/playwright/deepnest/20261012T011633Z-9baf348b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:17:47.605484+00:00 | deepnest-next `b-jakobs1-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 0.875 | [record](output/playwright/deepnest/20261012T011637Z-fa5f6895/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:17:55.815166+00:00 | SVGnest `m-sign-4` seed 2, 60s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T011650Z-274125ef/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:18:08.431311+00:00 | deepnest-next `b-shapes0-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 7.809523809523809 | [record](output/playwright/deepnest/20261012T011701Z-def3579f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:18:10.740429+00:00 | deepnest-next `b-swim-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 4.961063007379444 | [record](output/playwright/deepnest/20261012T011703Z-f24fb839/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:18:49.316601+00:00 | deepnest-next `b-blaz1-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 9.8 | [record](output/playwright/deepnest/20261012T011743Z-142163b5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:18:54.861939+00:00 | deepnest-next `b-jakobs2-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 3.9474971666666665 | [record](output/playwright/deepnest/20261012T011748Z-a358c855/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:19:02.338235+00:00 | svgnest M expanded, 60 s: 90/90 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T011902Z-36acd6a5.md). No final gate.

- 2026-10-12T01:19:09.530624+00:00 | deepnest B identical, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T011909Z-96b6f188.md). No final gate.

- 2026-10-12T01:19:17.432248+00:00 | deepnest-next `b-swim-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 1.6917136220445061 | [record](output/playwright/deepnest/20261012T011811Z-d56f76d6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:19:17.894947+00:00 | deepnest-next `b-shapes0-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.9 | [record](output/playwright/deepnest/20261012T011809Z-ec214fe9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:19:56.482540+00:00 | deepnest-next `b-blaz1-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 3.433333333333333 | [record](output/playwright/deepnest/20261012T011850Z-f8610c1f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:20:05.224944+00:00 | deepnest-next `b-jakobs2-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 3.8333333333333335 | [record](output/playwright/deepnest/20261012T011855Z-c132a07a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:20:15.380930+00:00 | deepnest-next `m-box-batch-500` seed 1, 60s, identical, axis y | valid | material 2.3863934426229507 | [record](output/playwright/deepnest/20261012T011849Z-166478a8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:20:24.596731+00:00 | deepnest-next `b-trousers-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 3.820179186440678 | [record](output/playwright/deepnest/20261012T011918Z-9d7d5b3a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:20:27.939705+00:00 | deepnest-next `b-shapes1-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 7.852014523809524 | [record](output/playwright/deepnest/20261012T011918Z-d612f58a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:21:03.834365+00:00 | deepnest-next `b-dagli-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 0.95 | [record](output/playwright/deepnest/20261012T011957Z-96ce4fd6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:21:22.605514+00:00 | deepnest-next `m-box-desktop` seed 1, 60s, identical, axis y | valid | material 0.885 | [record](output/playwright/deepnest/20261012T012016Z-0271f7d8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:21:31.409563+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 3.3111690621468925 | [record](output/playwright/deepnest/20261012T012025Z-d12c8515/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:21:35.237241+00:00 | deepnest-next `b-shapes1-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 7.809523809523809 | [record](output/playwright/deepnest/20261012T012028Z-e05843ec/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:21:38.618719+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 0.9690476285714285 | [record](output/playwright/deepnest/20261012T012032Z-574e0c28/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:22:14.042737+00:00 | deepnest-next `b-fu-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 5.656538571428572 | [record](output/playwright/deepnest/20261012T012104Z-bc6f22ae/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:22:25.971521+00:00 | SVGnest `b-albano-nest-mb-free` seed 0, 300s, identical, axis y | valid | material 2.5062623599208966 | [record](output/playwright/svgnest/20261012T011719Z-4d4cedd3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:22:30.034953+00:00 | deepnest-next `m-box-long` seed 1, 60s, identical, axis y | valid | material 0.3257377049180328 | [record](output/playwright/deepnest/20261012T012123Z-df652291/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:22:42.068047+00:00 | deepnest-next `b-shapes1-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.45 | [record](output/playwright/deepnest/20261012T012136Z-4dd72db1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:22:45.417244+00:00 | deepnest-next `b-mao-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 2.7350966703129744 | [record](output/playwright/deepnest/20261012T012139Z-30ea8986/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:23:23.592508+00:00 | deepnest-next `b-fu-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261012T012214Z-ce6d0c33/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:23:33.594813+00:00 | SVGnest `b-albano-nest-mb-free` seed 1, 300s, identical, axis y | valid | material 2.774408033399253 | [record](output/playwright/svgnest/20261012T011828Z-a0e31f0f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:23:37.078505+00:00 | deepnest-next `m-box-mini` seed 1, 60s, identical, axis y | valid | material 0.716000005 | [record](output/playwright/deepnest/20261012T012230Z-6c3bbd71/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:23:44.278010+00:00 | SVGnest `b-albano-nest-mb-free` seed 2, 300s, identical, axis y | valid | material 2.6038985948143263 | [record](output/playwright/svgnest/20261012T011839Z-c83bbc43/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:23:51.925654+00:00 | deepnest-next `b-shirts-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 8.474624615384615 | [record](output/playwright/deepnest/20261012T012242Z-6e4e0546/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:23:55.085391+00:00 | deepnest-next `b-mao-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 2.7886232318444244 | [record](output/playwright/deepnest/20261012T012246Z-4eabcb0a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:24:33.414376+00:00 | deepnest-next `b-fu-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 1.5365881842105265 | [record](output/playwright/deepnest/20261012T012324Z-d24bf108/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:24:44.676060+00:00 | deepnest-next `m-box-storage` seed 1, 60s, identical, axis y | valid | material 0.5388524590163934 | [record](output/playwright/deepnest/20261012T012338Z-476b434b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:25:01.643691+00:00 | deepnest-next `b-shirts-nest-mb-given` seed 1, 60s, expanded, axis y | valid | material 8.871794871794872 | [record](output/playwright/deepnest/20261012T012352Z-d4988962/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:25:02.109359+00:00 | deepnest-next `b-mao-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 0.9026602309803923 | [record](output/playwright/deepnest/20261012T012356Z-0f4525c6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:25:40.874720+00:00 | deepnest-next `b-jakobs1-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 4.535815916666667 | [record](output/playwright/deepnest/20261012T012434Z-eb00f257/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:25:52.073199+00:00 | deepnest-next `m-box-tool` seed 1, 60s, identical, axis y | valid | material 1.4790000025 | [record](output/playwright/deepnest/20261012T012445Z-e0c2733b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:26:08.895094+00:00 | deepnest-next `b-shirts-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.59375 | [record](output/playwright/deepnest/20261012T012502Z-34dfe779/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:26:12.224826+00:00 | deepnest-next `b-marques-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 1.1826923076923077 | [record](output/playwright/deepnest/20261012T012502Z-c444c111/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:26:25.529216+00:00 | Two-sweep compaction of 35 B development layouts; every attempt retained | [evidence](benchmarks/results/compact-b-20261012T012622Z-10241405.md).

- 2026-10-12T01:26:48.085084+00:00 | deepnest-next `b-jakobs1-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 3.8333333333333335 | [record](output/playwright/deepnest/20261012T012541Z-9a0d9b3a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:26:55.040308+00:00 | Two-sweep compaction of 30 M development layouts; every attempt retained | [evidence](benchmarks/results/compact-m-20261012T012625Z-c3cdcbe3.md).

- 2026-10-12T01:26:59.888921+00:00 | deepnest-next `m-garment-bruce-1` seed 1, 60s, identical, axis y | valid | material 0.21860406799999996 | [record](output/playwright/deepnest/20261012T012553Z-6dd555c4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:27:16.467234+00:00 | deepnest-next `b-swim-nest-mb-free` seed 1, 60s, expanded, axis y | valid | material 5.611848604231749 | [record](output/playwright/deepnest/20261012T012609Z-f34219dc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:27:19.515898+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 7.618578666666667 | [record](output/playwright/deepnest/20261012T012613Z-4547bf85/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:27:31.808304+00:00 | SVGnest `b-fu-strip-sheet` seed 0, 300s, identical, axis y | valid | material 1.3976608157894737 | [record](output/playwright/svgnest/20261012T012226Z-f40d366f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:27:55.701908+00:00 | deepnest-next `b-jakobs1-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 0.8125 | [record](output/playwright/deepnest/20261012T012649Z-0a1844af/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:28:09.174182+00:00 | deepnest-next `m-garment-bruce-2` seed 1, 60s, identical, axis y | valid | material 0.48162238775 | [record](output/playwright/deepnest/20261012T012700Z-8c117aa9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:28:26.300283+00:00 | deepnest-next `b-shapes0-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 7.809523809523809 | [record](output/playwright/deepnest/20261012T012720Z-4d292d41/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:28:42.249648+00:00 | SVGnest `b-fu-strip-sheet` seed 1, 300s, identical, axis y | valid | material 1.394736842105263 | [record](output/playwright/svgnest/20261012T012337Z-fd024d19/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:28:43.712326+00:00 | Two-sweep compaction of 35 B development layouts; every attempt retained | [evidence](benchmarks/results/compact-b-20261012T012839Z-c2a42aba.md).

- 2026-10-12T01:28:50.342086+00:00 | SVGnest `b-fu-strip-sheet` seed 2, 300s, identical, axis y | valid | material 1.394736842105263 | [record](output/playwright/svgnest/20261012T012345Z-7d0fbfb1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:29:05.745583+00:00 | deepnest-next `b-jakobs2-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 3.935232625 | [record](output/playwright/deepnest/20261012T012756Z-ec654f80/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:29:34.074569+00:00 | deepnest-next `b-shapes0-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.9 | [record](output/playwright/deepnest/20261012T012827Z-ffb183b1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:29:36.004824+00:00 | deepnest-next `m-garment-bruce-3` seed 1, 60s, identical, axis y | valid | material 1.1054080543333333 | [record](output/playwright/deepnest/20261012T012810Z-cc53fd30/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:30:01.274410+00:00 | deepnest-next `b-trousers-strip-sheet` seed 1, 60s, expanded, axis y | valid | material 2.2025316455696204 | [record](output/playwright/deepnest/20261012T012850Z-a25c4140/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:30:05.505628+00:00 | Two-sweep compaction of 30 M development layouts; every attempt retained | [evidence](benchmarks/results/compact-m-20261012T012843Z-dac4bd32.md).

- 2026-10-12T01:30:13.297918+00:00 | deepnest-next `b-jakobs2-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 3.6666666666666665 | [record](output/playwright/deepnest/20261012T012906Z-d6001f7d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:30:41.278327+00:00 | deepnest-next `b-shapes1-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 7.618578666666667 | [record](output/playwright/deepnest/20261012T012935Z-75560157/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:31:08.553172+00:00 | deepnest-next `b-swim-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 4.8097503701417565 | [record](output/playwright/deepnest/20261012T013002Z-27dd6c76/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:31:13.138521+00:00 | deepnest-next `m-garment-teagan-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T012937Z-38454fce/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:31:48.376538+00:00 | deepnest-next `b-shapes1-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 7.809523809523809 | [record](output/playwright/deepnest/20261012T013042Z-dca288b7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:32:15.597500+00:00 | deepnest-next `b-swim-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 1.6942486256954103 | [record](output/playwright/deepnest/20261012T013109Z-f74cd28b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:32:40.462069+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 0, 300s, identical, axis y | valid | material 0.8595238142857142 | [record](output/playwright/svgnest/20261012T012735Z-64c8f0d0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:32:55.251448+00:00 | deepnest-next `b-shapes1-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.45 | [record](output/playwright/deepnest/20261012T013149Z-da80032b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:33:02.760069+00:00 | deepnest-next `m-garment-teagan-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T013114Z-a91b0f39/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:33:34.938039+00:00 | deepnest-next `b-trousers-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 3.7233521016949154 | [record](output/playwright/deepnest/20261012T013220Z-1583cd51/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:33:50.919396+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 1, 300s, identical, axis y | valid | material 0.8610389714285714 | [record](output/playwright/svgnest/20261012T012845Z-6a515603/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:33:57.179440+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 2, 300s, identical, axis y | valid | material 0.8552381 | [record](output/playwright/svgnest/20261012T012851Z-6d7bb48a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:34:03.575628+00:00 | deepnest-next `b-shirts-nest-mb-free` seed 2, 60s, expanded, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T013256Z-926d4c8b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:34:45.597061+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 3.3111690621468925 | [record](output/playwright/deepnest/20261012T013335Z-9e64a3a8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:34:47.498204+00:00 | deepnest-next `m-garment-teagan-3` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T013303Z-c31b7334/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:35:24.438496+00:00 | deepnest-next `b-shirts-nest-mb-given` seed 2, 60s, expanded, axis y | valid | material 8.871794871794872 | [record](output/playwright/deepnest/20261012T013405Z-0adfd295/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:35:42.864618+00:00 | SVGnest `b-albano-nest-mb-free` seed 0, 300s, expanded, axis y | valid | material 3.613992398593716 | [record](output/playwright/svgnest/20261012T013037Z-2670c63c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:35:55.202142+00:00 | deepnest-next `b-trousers-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.3485881265822783 | [record](output/playwright/deepnest/20261012T013446Z-283f9fed/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:36:33.492801+00:00 | deepnest-next `b-shirts-strip-sheet` seed 2, 60s, expanded, axis y | valid | material 2.56875 | [record](output/playwright/deepnest/20261012T013525Z-44a8757e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:36:51.375788+00:00 | deepnest-next `m-mechanical-batch-1000` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T013448Z-2eb342d1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:36:54.619918+00:00 | Two-sweep compaction of 35 B development layouts; every attempt retained | [evidence](benchmarks/results/compact-b-20261012T013650Z-e3423fac.md).

- 2026-10-12T01:37:46.426239+00:00 | deepnest-next `b-swim-nest-mb-free` seed 2, 60s, expanded, axis y | valid | material 5.724314465693773 | [record](output/playwright/deepnest/20261012T013634Z-5dbebf89/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:37:46.887749+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 0, 300s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261012T013241Z-19a7a142/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:38:04.803575+00:00 | deepnest-next `m-mechanical-cog-washers` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T013652Z-23f23daf/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:38:13.075504+00:00 | Two-sweep compaction of 30 M development layouts; every attempt retained | [evidence](benchmarks/results/compact-m-20261012T013654Z-fb5e8bfa.md).

- 2026-10-12T01:38:55.483565+00:00 | SVGnest `b-albano-nest-mb-free` seed 1, 300s, expanded, axis y | valid | material 3.849349406943529 | [record](output/playwright/svgnest/20261012T013349Z-8d71b240/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:38:57.798405+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 1, 300s, identical, axis y | valid | material 7.809523809523809 | [record](output/playwright/svgnest/20261012T013351Z-a83779ea/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:39:06.431567+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 2, 300s, identical, axis y | valid | material 7.857142857142857 | [record](output/playwright/svgnest/20261012T013358Z-c040c0f3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:39:37.037411+00:00 | deepnest-next `m-mechanical-defective-stock` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T013805Z-7bd8f09f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:40:10.959345+00:00 | deepnest B expanded, 60 s: 105/105 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T014010Z-9b8afe5e.md). No final gate.

- 2026-10-12T01:40:49.759592+00:00 | SVGnest `b-fu-strip-sheet` seed 0, 300s, expanded, axis y | valid | material 1.368421052631579 | [record](output/playwright/svgnest/20261012T013544Z-cb5b9884/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:42:24.971953+00:00 | deepnest-next `m-box-batch-500` seed 2, 60s, identical, axis y | valid | material 2.455081967213115 | [record](output/playwright/deepnest/20261012T014042Z-315e2384/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:42:34.505234+00:00 | deepnest-next `m-mechanical-frame-inserts` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T014119Z-493c3263/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:42:58.338413+00:00 | SVGnest `b-swim-nest-mb-given` seed 0, 300s, identical, axis y | valid | material 4.850556276076423 | [record](output/playwright/svgnest/20261012T013752Z-46d90ad0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:43:35.355541+00:00 | deepnest-next `m-box-desktop` seed 2, 60s, identical, axis y | valid | material 0.942 | [record](output/playwright/deepnest/20261012T014226Z-52876a19/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:43:44.389474+00:00 | deepnest-next `m-mechanical-large-plates` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T014235Z-492ef957/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:44:02.890191+00:00 | SVGnest `b-fu-strip-sheet` seed 1, 300s, expanded, axis y | valid | material 1.394736842105263 | [record](output/playwright/svgnest/20261012T013856Z-bc1074a5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:44:05.082471+00:00 | SVGnest `b-swim-nest-mb-given` seed 1, 300s, identical, axis y | valid | material 4.981320154812013 | [record](output/playwright/svgnest/20261012T013859Z-f74438bc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:44:15.167113+00:00 | SVGnest `b-swim-nest-mb-given` seed 2, 300s, identical, axis y | valid | material 4.946872094586707 | [record](output/playwright/svgnest/20261012T013907Z-fa7213e1/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:44:44.427823+00:00 | deepnest-next `m-box-long` seed 2, 60s, identical, axis y | valid | material 0.3257377049180328 | [record](output/playwright/deepnest/20261012T014336Z-ef6c1b52/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:45:03.499228+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T014345Z-70007222/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:45:19.020990+00:00 | SVGnest `b-albano-nest-mb-free` seed 2, 300s, expanded, axis y | valid | material 3.38897024170512 | [record](output/playwright/svgnest/20261012T014012Z-0c11ca37/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:45:53.814485+00:00 | deepnest-next `m-box-mini` seed 2, 60s, identical, axis y | valid | material 0.666000005 | [record](output/playwright/deepnest/20261012T014445Z-d4071c64/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:45:56.830948+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 0, 300s, expanded, axis y | valid | material 1.1428571428571428 | [record](output/playwright/svgnest/20261012T014051Z-6ea5571d/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:46:12.760155+00:00 | deepnest-next `m-mechanical-mounting-kit` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T014504Z-92a80170/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:47:07.519751+00:00 | deepnest-next `m-box-storage` seed 2, 60s, identical, axis y | valid | material 0.5388524590163934 | [record](output/playwright/deepnest/20261012T014555Z-ab0c47c7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:47:25.025937+00:00 | deepnest-next `m-mechanical-panel-hardware` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T014613Z-2f126f2d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:48:08.269958+00:00 | SVGnest `b-trousers-nest-mb-given` seed 0, 300s, identical, axis y | valid | material 3.3111690621468925 | [record](output/playwright/svgnest/20261012T014301Z-d917be59/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:48:19.424060+00:00 | deepnest-next `m-box-tool` seed 2, 60s, identical, axis y | valid | material 1.4790000025 | [record](output/playwright/deepnest/20261012T014708Z-74ccd8a7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:49:11.556147+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 1, 300s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T014404Z-a646b1b8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:49:12.644397+00:00 | SVGnest `b-trousers-nest-mb-given` seed 1, 300s, identical, axis y | valid | material 3.169491525423729 | [record](output/playwright/svgnest/20261012T014406Z-818e6841/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:49:22.323064+00:00 | deepnest-next `m-mechanical-remnant-kit` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T014726Z-2d4e36a2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:49:22.452427+00:00 | SVGnest `b-trousers-nest-mb-given` seed 2, 300s, identical, axis y | valid | material 3.23728813559322 | [record](output/playwright/svgnest/20261012T014416Z-243d009f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:49:28.655870+00:00 | deepnest-next `m-garment-bruce-1` seed 2, 60s, identical, axis y | valid | material 0.21853775400000003 | [record](output/playwright/deepnest/20261012T014820Z-24aae9c6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:50:26.210134+00:00 | SVGnest `b-fu-strip-sheet` seed 2, 300s, expanded, axis y | valid | material 1.3711113947368423 | [record](output/playwright/svgnest/20261012T014520Z-f6a13d05/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:50:33.414875+00:00 | deepnest-next `m-mechanical-small-brackets` seed 1, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T014923Z-08f47489/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:50:47.009386+00:00 | deepnest-next `m-garment-bruce-2` seed 2, 60s, identical, axis y | valid | material 0.47674022025 | [record](output/playwright/deepnest/20261012T014929Z-559351e8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:51:04.679957+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 0, 300s, expanded, axis y | valid | material 8.761801285714286 | [record](output/playwright/svgnest/20261012T014558Z-02ac5627/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:52:38.220263+00:00 | deepnest-next `m-garment-bruce-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015048Z-b40a53d9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:52:51.264766+00:00 | deepnest-next `m-public-gear-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015034Z-fca8f1a2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:53:15.924922+00:00 | SVGnest `m-box-mini` seed 0, 300s, identical, axis y | valid | material 0.816000005 | [record](output/playwright/svgnest/20261012T014809Z-65e4dd47/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:54:19.891404+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 1, 300s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T014912Z-338631f0/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:54:21.335274+00:00 | SVGnest `m-box-mini` seed 1, 300s, identical, axis y | valid | material 0.77 | [record](output/playwright/svgnest/20261012T014914Z-23f6903c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:54:30.984101+00:00 | deepnest-next `m-public-gear-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015252Z-2007341b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:54:31.356678+00:00 | SVGnest `m-box-mini` seed 2, 300s, identical, axis y | valid | material 0.805 | [record](output/playwright/svgnest/20261012T014924Z-11831618/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:54:38.656575+00:00 | deepnest-next `m-garment-teagan-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015239Z-c1523130/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:55:40.022318+00:00 | SVGnest `b-jakobs2-strip-sheet` seed 2, 300s, expanded, axis y | invalid | material None | [record](output/playwright/svgnest/20261012T015032Z-ef1d625c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:56:12.664774+00:00 | SVGnest `b-swim-nest-mb-given` seed 0, 300s, expanded, axis y | valid | material 4.933811423230414 | [record](output/playwright/svgnest/20261012T015106Z-097e4be8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:56:51.085892+00:00 | deepnest-next `m-garment-teagan-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015439Z-462bf7b9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:58:27.452199+00:00 | SVGnest `m-garment-teagan-2` seed 0, 300s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T015319Z-5a05a1d4/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:58:31.225061+00:00 | SVGnest `m-mechanical-defective-stock` seed 0, 300s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T015829Z-5e8f9dcc/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:58:34.881557+00:00 | SVGnest `m-mechanical-mixed-stock` seed 0, 300s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T015832Z-56216a84/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:58:36.558047+00:00 | deepnest-next `m-garment-teagan-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015652Z-b2c2176c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:59:06.212456+00:00 | deepnest-next `m-public-gear-3` seed 1, 60s, identical, axis y | timeout | material None | [record](output/playwright/deepnest/20261012T015432Z-178626f2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T01:59:27.445660+00:00 | SVGnest `b-swim-nest-mb-given` seed 1, 300s, expanded, axis y | valid | material 5.25473007323688 | [record](output/playwright/svgnest/20261012T015421Z-72f46e4c/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:59:29.698043+00:00 | SVGnest `m-garment-teagan-2` seed 1, 300s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T015422Z-52b5f0c7/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:59:33.563553+00:00 | SVGnest `m-mechanical-defective-stock` seed 1, 300s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T015931Z-f5743c47/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:59:37.814447+00:00 | SVGnest `m-mechanical-mixed-stock` seed 1, 300s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T015935Z-be46f698/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:59:40.464872+00:00 | SVGnest `m-garment-teagan-2` seed 2, 300s, identical, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T015432Z-59cbb412/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:59:44.008155+00:00 | SVGnest `m-mechanical-defective-stock` seed 2, 300s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T015942Z-71de7eb6/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T01:59:47.674374+00:00 | SVGnest `m-mechanical-mixed-stock` seed 2, 300s, identical, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T015945Z-e742c784/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:00:07.558104+00:00 | deepnest-next `m-mechanical-batch-1000` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015837Z-bfdb885f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:00:40.264013+00:00 | deepnest-next `m-public-gear-4` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T015907Z-ee25cae0/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:00:48.181312+00:00 | SVGnest `b-shapes0-nest-mb-free` seed 2, 300s, expanded, axis y | valid | material 8.792837380952381 | [record](output/playwright/svgnest/20261012T015541Z-91125209/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:01:22.143729+00:00 | SVGnest `b-trousers-nest-mb-given` seed 0, 300s, expanded, axis y | valid | material 3.3111690621468925 | [record](output/playwright/svgnest/20261012T015614Z-ff9f10e3/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:02:09.060887+00:00 | svgnest B identical, 300 s: 18/18 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T020209Z-e12e4595.md). No final gate.

- 2026-10-12T02:02:09.528299+00:00 | svgnest M identical, 300 s: 12/12 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T020209Z-0ffdd0af.md). No final gate.

- 2026-10-12T02:02:21.412795+00:00 | deepnest-next `m-box-batch-500` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020108Z-ec0fad81/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:03:33.300865+00:00 | deepnest-next `m-box-desktop` seed 0, 60s, clearance-safe, axis y | valid | material 0.945 | [record](output/playwright/deepnest/20261012T020223Z-17e9c606/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:04:12.980767+00:00 | deepnest-next `m-mechanical-cog-washers` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T020300Z-8368b5b7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:04:24.224532+00:00 | deepnest-next `m-sign-1` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020301Z-c2c084d6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:04:36.321892+00:00 | SVGnest `b-trousers-nest-mb-given` seed 1, 300s, expanded, axis y | valid | material 3.169491525423729 | [record](output/playwright/svgnest/20261012T015928Z-68768678/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:04:44.308230+00:00 | deepnest-next `m-box-long` seed 0, 60s, clearance-safe, axis y | valid | material 0.32704918032786884 | [record](output/playwright/deepnest/20261012T020334Z-c9812b43/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:04:52.461245+00:00 | collision-guided repair B: 35/35 valid, 1 improved and 1 regressed vs previous fixed-pass algorithm | [all outcomes](benchmarks/results/repack-sheet-20261012T020010Z-102281dd.md). No final quality or speed gate.

- 2026-10-12T02:04:52.504137+00:00 | collision-guided repair M: 30/30 valid, 1 improved and 0 regressed vs previous fixed-pass algorithm | [all outcomes](benchmarks/results/repack-maker-20261012T020020Z-f56fc431.md). No final quality or speed gate.

- 2026-10-12T02:05:24.068028+00:00 | deepnest-next `m-box-batch-500` seed 2, 60s, clearance-safe, axis y | valid | material 2.4921311475409835 | [record](output/playwright/deepnest/20261012T020351Z-e9723784/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:05:32.330367+00:00 | deepnest-next `m-box-batch-500` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020349Z-de1b55a9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:05:41.915587+00:00 | deepnest-next `m-mechanical-defective-stock` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020414Z-f3079bc0/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:05:57.973882+00:00 | SVGnest `b-swim-nest-mb-given` seed 2, 300s, expanded, axis y | valid | material 5.162206487869697 | [record](output/playwright/svgnest/20261012T020049Z-411261a8/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:06:02.003038+00:00 | deepnest-next `m-box-mini` seed 0, 60s, clearance-safe, axis y | valid | material 0.787 | [record](output/playwright/deepnest/20261012T020445Z-8eaaf183/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:06:31.530610+00:00 | SVGnest `m-box-mini` seed 0, 300s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T020123Z-aba8f542/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:06:36.585451+00:00 | deepnest-next `m-box-desktop` seed 2, 60s, clearance-safe, axis y | valid | material 0.945 | [record](output/playwright/deepnest/20261012T020525Z-80e98965/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:06:46.123129+00:00 | deepnest-next `m-box-desktop` seed 1, 60s, clearance-safe, axis y | valid | material 0.945 | [record](output/playwright/deepnest/20261012T020533Z-ae0f8c2f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:07:01.664137+00:00 | deepnest-next `m-mechanical-frame-inserts` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T020543Z-69fe22ba/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:07:19.973948+00:00 | deepnest-next `m-box-storage` seed 0, 60s, clearance-safe, axis y | valid | material 0.5401639344262295 | [record](output/playwright/deepnest/20261012T020603Z-09b05838/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:07:21.276029+00:00 | deepnest-next `m-sign-2` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020425Z-f8b0a451/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:07:48.441921+00:00 | deepnest-next `m-box-long` seed 2, 60s, clearance-safe, axis y | valid | material 0.32704918032786884 | [record](output/playwright/deepnest/20261012T020637Z-f534b4b9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:07:57.375428+00:00 | deepnest-next `m-box-long` seed 1, 60s, clearance-safe, axis y | valid | material 0.32704918032786884 | [record](output/playwright/deepnest/20261012T020647Z-0aa8b846/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:08:20.534859+00:00 | deepnest-next `m-mechanical-large-plates` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T020703Z-af6de048/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:08:34.302772+00:00 | deepnest-next `m-box-tool` seed 0, 60s, clearance-safe, axis y | valid | material 1.4790000025 | [record](output/playwright/deepnest/20261012T020722Z-b2034d25/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:09:01.037294+00:00 | deepnest-next `m-box-mini` seed 2, 60s, clearance-safe, axis y | valid | material 0.752 | [record](output/playwright/deepnest/20261012T020750Z-0bbfdd80/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:09:02.979936+00:00 | deepnest-next `m-sign-3` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020723Z-0b36e14b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:09:09.442153+00:00 | deepnest-next `m-box-mini` seed 1, 60s, clearance-safe, axis y | valid | material 0.774000005 | [record](output/playwright/deepnest/20261012T020758Z-6687c481/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:09:45.465718+00:00 | SVGnest `m-box-mini` seed 1, 300s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T020437Z-6e71a622/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:09:48.878818+00:00 | deepnest-next `m-garment-bruce-1` seed 0, 60s, clearance-safe, axis y | valid | material 0.22518335233333334 | [record](output/playwright/deepnest/20261012T020835Z-a5f94a0a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:09:52.239938+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T020821Z-61bcbe35/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:10:15.104116+00:00 | deepnest-next `m-box-storage` seed 2, 60s, clearance-safe, axis y | valid | material 0.5401639344262295 | [record](output/playwright/deepnest/20261012T020902Z-ada31f9a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:10:24.005445+00:00 | deepnest-next `m-box-storage` seed 1, 60s, clearance-safe, axis y | valid | material 0.5401639344262295 | [record](output/playwright/deepnest/20261012T020911Z-9c108990/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:10:41.903550+00:00 | deepnest-next `m-sign-4` seed 1, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T020904Z-1c3c654e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:11:07.403826+00:00 | deepnest-next `m-garment-bruce-2` seed 0, 60s, clearance-safe, axis y | valid | material 0.4877499222500001 | [record](output/playwright/deepnest/20261012T020950Z-135f7596/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:11:08.164891+00:00 | SVGnest `b-trousers-nest-mb-given` seed 2, 300s, expanded, axis y | valid | material 3.23728813559322 | [record](output/playwright/svgnest/20261012T020600Z-2928ef37/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:11:09.136786+00:00 | deepnest-next `m-mechanical-mounting-kit` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T020954Z-26e276c8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:11:26.658237+00:00 | deepnest-next `m-box-tool` seed 2, 60s, clearance-safe, axis y | valid | material 1.4330000025 | [record](output/playwright/deepnest/20261012T021016Z-f30d5360/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:11:35.372526+00:00 | deepnest-next `m-box-tool` seed 1, 60s, clearance-safe, axis y | valid | material 1.4790000025 | [record](output/playwright/deepnest/20261012T021025Z-52acecad/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:11:40.694117+00:00 | SVGnest `m-garment-teagan-2` seed 0, 300s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T020633Z-ed2218ce/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:11:44.133167+00:00 | SVGnest `m-mechanical-defective-stock` seed 0, 300s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T021142Z-341f6b6b/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:11:47.719011+00:00 | SVGnest `m-mechanical-mixed-stock` seed 0, 300s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T021145Z-642de624/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:12:31.497449+00:00 | deepnest-next `m-mechanical-panel-hardware` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T021110Z-35e14d44/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:12:40.017627+00:00 | deepnest-next `m-garment-bruce-1` seed 2, 60s, clearance-safe, axis y | valid | material 0.224454846 | [record](output/playwright/deepnest/20261012T021128Z-64bfb39c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:12:47.462468+00:00 | deepnest-next `m-mechanical-frame-inserts` seed 0, 60s, clearance-safe, axis y | valid | material 0.6166470090163935 | [record](output/playwright/deepnest/20261012T021127Z-4218c6a3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:12:48.488389+00:00 | deepnest-next `m-garment-bruce-3` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021109Z-0894548a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:12:50.899098+00:00 | deepnest-next `m-garment-bruce-1` seed 1, 60s, clearance-safe, axis y | valid | material 0.22868668933333333 | [record](output/playwright/deepnest/20261012T021136Z-c7cc23d4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:13:36.706305+00:00 | svgnest B expanded, 300 s: 18/18 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T021336Z-74941dfd.md). No final gate.

- 2026-10-12T02:13:57.384565+00:00 | deepnest-next `m-garment-bruce-2` seed 2, 60s, clearance-safe, axis y | valid | material 0.4798551255 | [record](output/playwright/deepnest/20261012T021246Z-21b4df35/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:13:58.841410+00:00 | deepnest-next `m-mechanical-large-plates` seed 0, 60s, clearance-safe, axis y | valid | material 1.2436131259999998 | [record](output/playwright/deepnest/20261012T021248Z-d4eb636d/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:14:03.954031+00:00 | deepnest-next `m-garment-bruce-2` seed 1, 60s, clearance-safe, axis y | valid | material 0.5020563222500001 | [record](output/playwright/deepnest/20261012T021252Z-bd9175ed/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:14:32.805177+00:00 | deepnest-next `m-mechanical-remnant-kit` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021233Z-5bb1550a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:14:48.517234+00:00 | deepnest-next `m-garment-teagan-1` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021249Z-2c09b715/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:14:56.392723+00:00 | SVGnest `m-garment-teagan-2` seed 1, 300s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T020947Z-e1c6483e/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:15:03.508224+00:00 | SVGnest `m-mechanical-defective-stock` seed 1, 300s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T021501Z-a4b4fbf5/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:15:06.498204+00:00 | SVGnest `m-mechanical-mixed-stock` seed 1, 300s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T021504Z-f28f648f/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:15:30.907125+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 0, 60s, clearance-safe, axis y | valid | material 1.037753514144 | [record](output/playwright/deepnest/20261012T021400Z-13cbc43a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:15:31.265299+00:00 | deepnest-next `m-garment-bruce-3` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021358Z-5072f603/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:15:36.393024+00:00 | deepnest-next `m-garment-bruce-3` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021405Z-6c8599da/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:15:45.146674+00:00 | deepnest-next `m-mechanical-small-brackets` seed 2, 60s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T021434Z-34d9c563/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:16:17.125296+00:00 | SVGnest `m-box-mini` seed 2, 300s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T021109Z-b3d72093/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:16:36.819275+00:00 | deepnest-next `m-garment-teagan-2` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021449Z-cca2bb23/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:16:40.092453+00:00 | deepnest-next `m-mechanical-mounting-kit` seed 0, 60s, clearance-safe, axis y | valid | material 2.7940625925 | [record](output/playwright/deepnest/20261012T021532Z-8d7028b1/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:17:21.371382+00:00 | deepnest-next `m-garment-teagan-1` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021537Z-f37bb80b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:17:25.067847+00:00 | deepnest-next `m-garment-teagan-1` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021532Z-d027abad/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:17:43.928902+00:00 | deepnest-next `m-mechanical-frame-inserts` seed 1, 60s, clearance-safe, axis y | valid | material 0.6225393286885246 | [record](output/playwright/deepnest/20261012T021635Z-932d12be/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:17:55.249794+00:00 | deepnest-next `m-mechanical-panel-hardware` seed 0, 60s, clearance-safe, axis y | valid | material 1.7303596172 | [record](output/playwright/deepnest/20261012T021641Z-805fc12f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:18:39.476716+00:00 | deepnest-next `m-public-gear-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021546Z-35b4ba4e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:18:46.349406+00:00 | deepnest-next `m-garment-teagan-3` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021637Z-d38360e6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:18:57.675209+00:00 | tested and reverted surrogate early screening for multi-item repair: four valid, identical-layout runs; no consistent timing benefit | [all evidence](benchmarks/results/displace-profile-20261012T0219.md). No speed-gate claim.

- 2026-10-12T02:18:59.143059+00:00 | deepnest-next `m-mechanical-large-plates` seed 1, 60s, clearance-safe, axis y | valid | material 1.2146666666666666 | [record](output/playwright/deepnest/20261012T021745Z-8c3d9244/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:19:13.859013+00:00 | deepnest-next `m-garment-teagan-2` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021722Z-a3ef5e38/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:19:22.747880+00:00 | deepnest-next `m-mechanical-remnant-kit` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021757Z-6b652499/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:19:38.969853+00:00 | deepnest-next `m-garment-teagan-2` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021726Z-084c45a5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:20:09.376098+00:00 | deepnest-next `m-mechanical-batch-1000` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021848Z-bc487ed5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:20:16.790383+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 1, 60s, clearance-safe, axis y | valid | material 1.0284506139840002 | [record](output/playwright/deepnest/20261012T021900Z-b7f9c2b2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:20:31.028859+00:00 | deepnest-next `m-public-gear-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021842Z-7f30eb84/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:20:33.528505+00:00 | deepnest-next `m-mechanical-small-brackets` seed 0, 60s, clearance-safe, axis y | valid | material 6.67 | [record](output/playwright/deepnest/20261012T021923Z-efefd9f4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:20:49.782613+00:00 | deepnest-next `m-garment-teagan-3` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021915Z-75337509/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:21:24.020689+00:00 | deepnest-next `m-mechanical-cog-washers` seed 0, 60s, clearance-safe, axis y | valid | material 2.1825 | [record](output/playwright/deepnest/20261012T022010Z-af20c737/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:21:24.424495+00:00 | SVGnest `m-garment-teagan-2` seed 2, 300s, expanded, axis y | no_layout | material None | [record](output/playwright/svgnest/20261012T021618Z-62cc803a/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:21:28.547971+00:00 | deepnest-next `m-mechanical-mounting-kit` seed 1, 60s, clearance-safe, axis y | valid | material 2.74143522 | [record](output/playwright/deepnest/20261012T022018Z-fa4985dc/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:21:31.529599+00:00 | SVGnest `m-mechanical-defective-stock` seed 2, 300s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T022129Z-1c4e7ba9/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:21:34.855291+00:00 | SVGnest `m-mechanical-mixed-stock` seed 2, 300s, expanded, axis y | unsupported | material None | [record](output/playwright/svgnest/20261012T022133Z-9e9ac014/run.json). Provisional settings, one worker and one CPU affinity.

- 2026-10-12T02:22:18.216892+00:00 | deepnest-next `m-public-gear-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022032Z-268b0f59/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:22:20.296903+00:00 | deepnest-next `m-public-gear-1` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022034Z-c8fe2299/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:22:36.904948+00:00 | deepnest-next `m-mechanical-batch-1000` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022050Z-bfff322c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:22:41.848629+00:00 | deepnest-next `m-mechanical-panel-hardware` seed 1, 60s, clearance-safe, axis y | valid | material 1.7728125512000001 | [record](output/playwright/deepnest/20261012T022129Z-97426b40/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:23:39.040641+00:00 | deepnest-next `m-public-gear-4` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022219Z-4f74b65a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:23:47.130877+00:00 | deepnest-next `m-mechanical-cog-washers` seed 1, 60s, clearance-safe, axis y | valid | material 2.1825 | [record](output/playwright/deepnest/20261012T022238Z-5a1782b7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:23:52.790707+00:00 | deepnest-next `m-garment-teagan-3` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T021940Z-f146e25e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:24:26.984059+00:00 | deepnest-next `m-public-gear-2` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022221Z-2ec062dd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:24:37.663324+00:00 | deepnest-next `m-mechanical-remnant-kit` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022242Z-467f7d9b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:25:16.489010+00:00 | deepnest-next `b-albano-nest-mb-free` seed 0, 300s, identical, axis y | valid | material 2.5943748626675456 | [record](output/playwright/deepnest/20261012T022005Z-33a84558/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:25:49.529281+00:00 | deepnest-next `m-public-gear-3` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022428Z-a3c0f2f2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:25:50.811436+00:00 | deepnest-next `m-mechanical-small-brackets` seed 1, 60s, clearance-safe, axis y | valid | material 6.63 | [record](output/playwright/deepnest/20261012T022438Z-2c5ea74f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:27:19.948760+00:00 | deepnest-next `m-public-gear-1` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022555Z-ad6e2195/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:27:30.104833+00:00 | deepnest-next `m-public-gear-4` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022554Z-32872e8f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:28:47.298693+00:00 | deepnest-next `m-sign-1` seed 0, 60s, clearance-safe, axis y | valid | material 0.9447733 | [record](output/playwright/deepnest/20261012T022731Z-ba2e412c/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:29:06.926625+00:00 | deepnest-next `m-public-gear-2` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022721Z-7fb9a494/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:30:24.078880+00:00 | deepnest-next `m-sign-2` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022848Z-6fe6ed61/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:30:37.468729+00:00 | deepnest-next `m-public-gear-3` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T022908Z-1846a37b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:30:51.921816+00:00 | deepnest-next `b-fu-strip-sheet` seed 0, 300s, identical, axis y | valid | material 1.368421052631579 | [record](output/playwright/deepnest/20261012T022521Z-2646c905/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:32:46.737118+00:00 | svgnest M expanded, 300 s: 12/12 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T023246Z-a5cc0290.md). No final gate.

- 2026-10-12T02:33:18.073125+00:00 | deepnest-next `m-sign-3` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023025Z-f6666850/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:33:57.044011+00:00 | deepnest-next `m-public-gear-4` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023038Z-c004d7f8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:35:36.614224+00:00 | deepnest-next `m-mechanical-defective-stock` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023233Z-ae17e157/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:35:41.220289+00:00 | deepnest-next `m-mechanical-batch-1000` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023230Z-e4d5f0a2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:36:01.934821+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 0, 300s, identical, axis y | valid | material 0.8411458428571429 | [record](output/playwright/deepnest/20261012T023052Z-a7c0bfb2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:36:29.847158+00:00 | deepnest-next `m-sign-1` seed 1, 60s, clearance-safe, axis y | valid | material 0.94796155 | [record](output/playwright/deepnest/20261012T023421Z-c30c8d77/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:36:50.999457+00:00 | deepnest-next `m-mechanical-cog-washers` seed 2, 60s, clearance-safe, axis y | valid | material 2.1825 | [record](output/playwright/deepnest/20261012T023542Z-186a2270/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:36:58.240301+00:00 | deepnest-next `m-mechanical-defective-stock` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023537Z-072cec43/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:37:10.382927+00:00 | deepnest-next `m-sign-4` seed 0, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023427Z-16ee36e8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:38:11.289903+00:00 | deepnest-next `m-mechanical-defective-stock` seed 2, 60s, clearance-safe, axis y | valid | material 3.3214 | [record](output/playwright/deepnest/20261012T023652Z-6a6be6dd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:38:24.253442+00:00 | deepnest-next `m-sign-1` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023659Z-e18588ad/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:38:36.978418+00:00 | deepnest-next `b-albano-nest-mb-free` seed 1, 300s, identical, axis y | valid | material 2.5943748626675456 | [record](output/playwright/deepnest/20261012T023237Z-07dbddd8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:39:24.016560+00:00 | deepnest-next `m-mechanical-frame-inserts` seed 2, 60s, clearance-safe, axis y | valid | material 0.6237919545081968 | [record](output/playwright/deepnest/20261012T023812Z-d5991444/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:39:46.176341+00:00 | deepnest-next `m-sign-2` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023825Z-b397ced9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:40:24.092192+00:00 | bounded group-separation development trial, sheet: all outcomes retained; no material gain on completed jobs | [report](benchmarks/results/repack-sheet-20261012T023153Z-f9cc4dca.md).

- 2026-10-12T02:40:24.116232+00:00 | bounded group-separation development trial, maker: all outcomes retained; no material gain on completed jobs | [report](benchmarks/results/repack-maker-20261012T023204Z-cf2e3cd9.md).

- 2026-10-12T02:40:31.478194+00:00 | deepnest-next `m-mechanical-large-plates` seed 2, 60s, clearance-safe, axis y | valid | material 1.2396666666666667 | [record](output/playwright/deepnest/20261012T023925Z-4d9a98ac/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:41:21.304431+00:00 | deepnest-next `m-sign-3` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023947Z-762e2248/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:41:50.330999+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 2, 60s, clearance-safe, axis y | valid | material 1.0218500911232 | [record](output/playwright/deepnest/20261012T024032Z-214e7ac4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:41:57.614674+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 0, 300s, identical, axis y | valid | material 6.809523809523809 | [record](output/playwright/deepnest/20261012T023650Z-70faf3fd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:41:58.772116+00:00 | deepnest-next `b-albano-nest-mb-free` seed 0, 300s, expanded, axis y | valid | material 3.8726159228740933 | [record](output/playwright/deepnest/20261012T023651Z-aa27fac2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:42:05.789540+00:00 | deepnest-next `m-sign-2` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T023927Z-0e98b80b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:42:20.945503+00:00 | deepnest-next `b-albano-nest-mb-free` seed 2, 300s, identical, axis y | valid | material 2.635464733025709 | [record](output/playwright/deepnest/20261012T023711Z-14ebcaec/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:42:56.087489+00:00 | indexed blocker-search diagnostic: four exact-output replays, two CPU10 pairs; retain speed change, no G4 claim | [all profiles](benchmarks/results/relax-profile-20261012T0242.md).

- 2026-10-12T02:42:57.289939+00:00 | deepnest-next `m-mechanical-mounting-kit` seed 2, 60s, clearance-safe, axis y | valid | material 2.7920882775 | [record](output/playwright/deepnest/20261012T024151Z-3845c307/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:43:27.220332+00:00 | deepnest-next `m-sign-4` seed 2, 60s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T024122Z-f88ca780/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:43:44.438976+00:00 | deepnest-next `b-fu-strip-sheet` seed 1, 300s, identical, axis y | valid | material 1.368421052631579 | [record](output/playwright/deepnest/20261012T023838Z-119043dd/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:44:00.955176+00:00 | deepnest M identical, 60 s: 90/90 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T024400Z-b9c3dab2.md). No final gate.

- 2026-10-12T02:44:06.242095+00:00 | deepnest-next `m-mechanical-panel-hardware` seed 2, 60s, clearance-safe, axis y | valid | material 1.7398561948000002 | [record](output/playwright/deepnest/20261012T024258Z-dc14d7b5/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:44:55.937266+00:00 | deepnest-next `m-sign-3` seed 1, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T024206Z-49ac4517/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:45:44.837220+00:00 | deepnest-next `m-mechanical-remnant-kit` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T024407Z-c7a6a4da/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:46:52.127497+00:00 | deepnest-next `m-mechanical-small-brackets` seed 2, 60s, clearance-safe, axis y | valid | material 6.78 | [record](output/playwright/deepnest/20261012T024545Z-508eb9a8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:47:04.256109+00:00 | deepnest-next `b-swim-nest-mb-given` seed 0, 300s, identical, axis y | valid | material 4.699584844202751 | [record](output/playwright/deepnest/20261012T024158Z-bd62deb4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:47:05.379176+00:00 | deepnest-next `b-fu-strip-sheet` seed 0, 300s, expanded, axis y | valid | material 1.4210526315789473 | [record](output/playwright/deepnest/20261012T024159Z-cea34eac/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:47:27.668022+00:00 | deepnest-next `b-fu-strip-sheet` seed 2, 300s, identical, axis y | valid | material 1.368421052631579 | [record](output/playwright/deepnest/20261012T024221Z-efbca856/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:48:02.098814+00:00 | deepnest-next `b-albano-nest-mb-free` seed 1, 300s, expanded, axis y | valid | material 3.891092154032081 | [record](output/playwright/deepnest/20261012T024255Z-9eea3ec4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:48:22.162545+00:00 | deepnest-next `m-public-gear-1` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T024653Z-cf437d42/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:48:51.920459+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 1, 300s, identical, axis y | valid | material 0.8386904857142857 | [record](output/playwright/deepnest/20261012T024345Z-516d295f/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:49:06.055401+00:00 | deepnest-next `b-albano-nest-mb-free` seed 2, 300s, expanded, axis y | valid | material 3.480520447593936 | [record](output/playwright/deepnest/20261012T024355Z-94d9c5e3/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:49:30.133421+00:00 | deepnest-next `m-sign-4` seed 1, 60s, clearance-safe, axis y | timeout | material None | [record](output/playwright/deepnest/20261012T024457Z-b1bea5d2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:50:21.459491+00:00 | deepnest-next `m-public-gear-2` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T024823Z-866e7ce2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:52:11.082259+00:00 | deepnest-next `m-public-gear-3` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T025022Z-b8fcd29e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:52:13.711956+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 0, 300s, identical, axis y | valid | material 3.264281231638418 | [record](output/playwright/deepnest/20261012T024705Z-593ec22b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:52:14.886430+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 0, 300s, expanded, axis y | valid | material 0.9724702428571429 | [record](output/playwright/deepnest/20261012T024706Z-2ca75e95/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:52:39.969291+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 2, 300s, identical, axis y | valid | material 0.8357142857142857 | [record](output/playwright/deepnest/20261012T024728Z-2c6bd7ad/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:53:13.846469+00:00 | deepnest-next `b-fu-strip-sheet` seed 1, 300s, expanded, axis y | valid | material 1.368421052631579 | [record](output/playwright/deepnest/20261012T024803Z-7469472b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:54:12.906191+00:00 | deepnest-next `b-fu-strip-sheet` seed 2, 300s, expanded, axis y | valid | material 1.368421052631579 | [record](output/playwright/deepnest/20261012T024906Z-4325d9f6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:54:37.074132+00:00 | deepnest-next `m-box-mini` seed 0, 300s, identical, axis y | valid | material 0.666000005 | [record](output/playwright/deepnest/20261012T024931Z-2414ba5b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:54:50.222479+00:00 | deepnest-next `m-public-gear-4` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T025314Z-b9a3fe91/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:56:01.813488+00:00 | deepnest-next `m-sign-1` seed 2, 60s, clearance-safe, axis y | valid | material 0.90956862 | [record](output/playwright/deepnest/20261012T025451Z-c8cee8b4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:56:07.410505+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 1, 300s, identical, axis y | valid | material 7.285714285714286 | [record](output/playwright/deepnest/20261012T025101Z-5958a78a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:57:35.732999+00:00 | deepnest-next `m-sign-2` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T025602Z-642be2bb/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:58:20.389734+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 1, 300s, expanded, axis y | valid | material 0.8227891285714286 | [record](output/playwright/deepnest/20261012T025314Z-0aa1074b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:59:07.803746+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 2, 300s, identical, axis y | valid | material 7.285714285714286 | [record](output/playwright/deepnest/20261012T025359Z-d497c2a8/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:59:09.215555+00:00 | deepnest-next `m-sign-3` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T025736Z-397234a0/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:59:19.407877+00:00 | deepnest-next `b-jakobs2-strip-sheet` seed 2, 300s, expanded, axis y | valid | material 0.86875 | [record](output/playwright/deepnest/20261012T025413Z-e1e7cd21/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T02:59:58.822332+00:00 | deepnest-next `m-garment-teagan-2` seed 0, 300s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T025438Z-1eb6e071/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:00:34.855391+00:00 | deepnest-next `m-sign-4` seed 2, 60s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T025910Z-e757ac7e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:00:39.014685+00:00 | shallow-overlap repair, sheet: 35 valid; 1 improved; all outcomes retained | [report](benchmarks/results/repack-sheet-20261012T025253Z-db613259.md). No final gate.

- 2026-10-12T03:00:39.043257+00:00 | shallow-overlap repair, maker: 30 valid; 0 improved; all outcomes retained | [report](benchmarks/results/repack-maker-20261012T025303Z-d1b807bb.md). No final gate.

- Shallow-overlap repair replay: two identical full outputs for blaz1 free; 11 to 10 sheets, first accepted improvement at pass 3; [raw proof](benchmarks/results/shallow-replay-20261012T0255.json).

- 2026-10-12T03:00:43.890989+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 0, 300s, expanded, axis y | valid | material 6.908609523809524 | [record](output/playwright/deepnest/20261012T025533Z-2ce95378/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:01:14.719291+00:00 | deepnest-next `b-swim-nest-mb-given` seed 1, 300s, identical, axis y | valid | material 4.635537696571581 | [record](output/playwright/deepnest/20261012T025608Z-5297ad14/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:01:21.991942+00:00 | deepnest M clearance-safe, 60 s: 90/90 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T030121Z-9132c7c2.md). No final gate.

- 2026-10-12T03:02:21.222563+00:00 | deepnest-next `m-box-mini` seed 1, 300s, identical, axis y | valid | material 0.716000005 | [record](output/playwright/deepnest/20261012T025714Z-3a122271/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:04:17.959911+00:00 | deepnest-next `b-swim-nest-mb-given` seed 2, 300s, identical, axis y | valid | material 4.490559616591205 | [record](output/playwright/deepnest/20261012T025908Z-6446e40e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:05:42.210265+00:00 | deepnest-next `m-box-mini` seed 0, 300s, clearance-safe, axis y | valid | material 0.724000005 | [record](output/playwright/deepnest/20261012T030035Z-5f192411/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:05:51.204778+00:00 | deepnest-next `b-swim-nest-mb-given` seed 0, 300s, expanded, axis y | valid | material 4.9488791489752835 | [record](output/playwright/deepnest/20261012T030044Z-f9646d50/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:06:23.635563+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 2, 300s, expanded, axis y | valid | material 7.778558285714285 | [record](output/playwright/deepnest/20261012T030113Z-474bbfc2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:06:23.705157+00:00 | deepnest-next `b-shapes0-nest-mb-free` seed 1, 300s, expanded, axis y | valid | material 6.855455761904762 | [record](output/playwright/deepnest/20261012T030113Z-a229ebc2/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:06:23.805844+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 1, 300s, identical, axis y | valid | material 2.8866193446327686 | [record](output/playwright/deepnest/20261012T030115Z-fb0eda9a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:07:09.954410+00:00 | deepnest-next `m-box-mini` seed 2, 300s, identical, axis y | valid | material 0.666000005 | [record](output/playwright/deepnest/20261012T030202Z-cf9a1f52/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:07:58.416089+00:00 | deepnest-next `m-garment-teagan-2` seed 1, 300s, identical, axis y | valid | material 2.185148404 | [record](output/playwright/deepnest/20261012T030222Z-bf7dcfed/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:09:28.876271+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 2, 300s, identical, axis y | valid | material 3.264281231638418 | [record](output/playwright/deepnest/20261012T030419Z-8e4a1a55/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:10:58.590826+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 0, 300s, expanded, axis y | valid | material 3.4919600338983052 | [record](output/playwright/deepnest/20261012T030552Z-8dbaacf6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:11:20.881286+00:00 | deepnest-next `m-garment-teagan-2` seed 0, 300s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T030543Z-cfc3ec87/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:11:31.172446+00:00 | deepnest-next `b-swim-nest-mb-given` seed 1, 300s, expanded, axis y | valid | material 4.874427976043186 | [record](output/playwright/deepnest/20261012T030624Z-bab4bc87/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:11:31.248616+00:00 | deepnest-next `b-swim-nest-mb-given` seed 2, 300s, expanded, axis y | valid | material 4.8097503701417565 | [record](output/playwright/deepnest/20261012T030624Z-35802495/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:12:56.238906+00:00 | deepnest-next `m-garment-teagan-2` seed 2, 300s, identical, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T030710Z-556afbf6/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:12:58.741441+00:00 | deepnest-next `m-box-mini` seed 1, 300s, clearance-safe, axis y | valid | material 0.724000005 | [record](output/playwright/deepnest/20261012T030750Z-4f169369/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:13:17.059177+00:00 | deepnest-next `m-mechanical-defective-stock` seed 1, 300s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T030759Z-db5cc037/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:14:14.740741+00:00 | deepnest B identical, 300 s: 18/18 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T031414Z-7121a8ab.md). No final gate.

- 2026-10-12T03:16:29.627066+00:00 | deepnest-next `m-mechanical-defective-stock` seed 0, 300s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T031114Z-73c13894/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:16:39.587949+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 1, 300s, expanded, axis y | valid | material 3.3111690621468925 | [record](output/playwright/deepnest/20261012T031132Z-51ebebb7/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:16:42.437646+00:00 | deepnest-next `b-trousers-nest-mb-given` seed 2, 300s, expanded, axis y | valid | material 3.3111690621468925 | [record](output/playwright/deepnest/20261012T031132Z-ca0a297e/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:18:04.448584+00:00 | deepnest-next `m-box-mini` seed 2, 300s, clearance-safe, axis y | valid | material 0.724000005 | [record](output/playwright/deepnest/20261012T031256Z-b3a886da/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:18:20.138353+00:00 | deepnest-next `m-mechanical-defective-stock` seed 2, 300s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T031257Z-017ecf15/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:18:30.579467+00:00 | deepnest-next `m-garment-teagan-2` seed 1, 300s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T031259Z-a6bf8ae4/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:21:42.488159+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 0, 300s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T031630Z-abd713c9/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:23:43.121772+00:00 | deepnest-next `m-garment-teagan-2` seed 2, 300s, clearance-safe, axis y | no_layout | material None | [record](output/playwright/deepnest/20261012T031805Z-41bba72a/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:23:46.791666+00:00 | deepnest-next `m-mechanical-defective-stock` seed 0, 300s, clearance-safe, axis y | valid | material 3.3214 | [record](output/playwright/deepnest/20261012T031833Z-9ee22e68/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:23:48.743750+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 1, 300s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T031834Z-76de4247/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:23:52.548974+00:00 | deepnest-next `m-mechanical-defective-stock` seed 1, 300s, clearance-safe, axis y | valid | material 2.9922153160000002 | [record](output/playwright/deepnest/20261012T031831Z-6d0e138b/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:24:36.703124+00:00 | deepnest B expanded, 300 s: 18/18 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T032436Z-b7be7a88.md). No final gate.

- 2026-10-12T03:28:57.684370+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 0, 300s, clearance-safe, axis y | valid | material 1.0263109647104 | [record](output/playwright/deepnest/20261012T032347Z-71b6c697/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:29:01.055817+00:00 | deepnest-next `m-mechanical-defective-stock` seed 2, 300s, clearance-safe, axis y | valid | material 3.3406 | [record](output/playwright/deepnest/20261012T032344Z-bcccc0c0/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:29:09.119952+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 2, 300s, identical, axis y | invalid | material None | [record](output/playwright/deepnest/20261012T032354Z-95865478/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:29:35.461586+00:00 | deepnest M identical, 300 s: 12/12 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T032935Z-846373a4.md). No final gate.

- 2026-10-12T03:30:44.754540+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 1, 300s, clearance-safe, axis y | valid | material 1.0206608351232 | [record](output/playwright/deepnest/20261012T032525Z-156a1337/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:31Z | Last-sheet compression after full repacking: [35 sheets](benchmarks/results/repack-sheet-20261012T032354Z-429e1837.md), all valid, 3 better/32 equal/0 worse vs v11; [30 makers](benchmarks/results/repack-maker-20261012T032404Z-eba64968.md), all valid, 8 better/22 equal/0 worse at a different work allowance. [Rejected replacement schedule](benchmarks/results/repack-sheet-20261012T031256Z-f5c905dc.md) retains five regressions. [Two exact compression replays](benchmarks/results/compression-replay-20261012T0326.json). Development diagnostics only.

- 2026-10-12T03:32Z | [Search quality triage](benchmarks/results/search-gap-diagnostic-20261012T0332.md): one fixed-work Nestbolt seed vs audited 60 s competitor medians, 52 comparisons, 19 wins/ties, 23 more than 1% worse, median reduction -0.00466317%. Thirteen jobs have no finite competitor median. Unequal work; not an acceptance result.

- 2026-10-12T03:34:50.375113+00:00 | deepnest-next `m-mechanical-mixed-stock` seed 2, 300s, clearance-safe, axis y | valid | material 1.0207213549312 | [record](output/playwright/deepnest/20261012T032934Z-9dcd74ca/run.json). Provisional native settings; independent score only for valid output.

- 2026-10-12T03:35:00.035337+00:00 | deepnest M clearance-safe, 300 s: 12/12 audited development attempts | [three-seed table](benchmarks/results/comparison-batches-20261012T033500Z-e03868ab.md). No final gate.

- 2026-10-12T03:35:47Z | M1 complete: [full audited baseline](benchmarks/results/baseline-gap-20261012T033547Z-e9539412.md), 27 tables / 1,878 declared slots, zero missing. Gap60=17.09055735915256%, gap300=21.54462947027872%; [G2 target frozen](benchmarks/baseline-target.json) at10.77231473513936% under the predeclared formula. No held-out or Nestbolt scores enter the target. Completed milestones M0+M1=20%; full goal remains active.

- 2026-10-12T04:04Z | Conditional repeated compression v15: [35 sheet jobs](benchmarks/results/repack-sheet-20261012T035142Z-a7b22154.md) and [30 maker jobs](benchmarks/results/repack-maker-20261012T035142Z-54130739.md), all valid. Repetition improves one B score by 1.69467427% and four M scores by up to 0.29843428% over v13; no score regresses. Conditional stopping preserves all v14 scores and reduces collision queries. Different work budgets and concurrent loads; no equal-time quality or speed gate.

- 2026-10-12T04:04:18Z | Native strip adapter: [complete three-seed development comparison](benchmarks/results/strip-development-20261012T040418Z-961c9a96.md), all 39 outputs independently valid. Median regression -0.039034271339577487%, maximum +1.6493127928228324%, against the better Sparrow settings median per instance at 60 s. Development parity thresholds pass; final-seed G3 remains open. [Portable source provenance](benchmarks/results/strip-source-provenance-20261012T0408.json).

- 2026-10-12T04:20Z | [Independent checker speed diagnostic](benchmarks/results/validator-speed-20261012T0420.md): distance pruning preserves all 104 saved validation reports and both complete profiled solver outputs. Interleaved validation CPU reductions: gear 32.7044%, 1,000-part batch 9.375%. One matched full-search pair: gear 44.046875 to 36.671875 CPU s; batch essentially unchanged. Rejected edge-sort trial and all six search timings retained. New exhaustive-reference distance tests and full local checks pass. Development diagnostics only; G4 remains open.

- 2026-10-12T04:33Z | [Clearance-outline reuse](benchmarks/results/clearance-cache-20261012T0433.md): all 104 saved validation reports and both complete profiled search outputs unchanged. Interleaved validation CPU reduction: gear 16.9811%, 1,000-part batch 13.7931%, beyond the preceding distance-pruning version. One full-search pair per job: 10.5667% and 5.1835% less CPU. Development diagnostics, no G4 claim.

- 2026-10-12T04:33Z | [Progressive search pilot](benchmarks/results/progressive-pilot-20261012T0433.md): four selected difficult development jobs, seed 0, up to 512 passes, 80M queries and 60 s safety deadline. All valid; Jakobs1 improves 2.4565%, Marques 4.2017%, Blaz1 and Bruce match their finished 64-pass baseline. First 64 histories and finishing trials identical in all four cases. Blaz1 stops at the work limit after 424 completed passes. Extra work and selected cases; no population or equal-budget claim.

- 2026-10-12T04:52:48Z | [Placement diversity](benchmarks/results/placement-diversity-20261012T045248Z.md): original and diversified strategies share successive seeds after the preserved first64 block. Four selected development jobs, up to1,024 passes/80M queries/60s: Blaz1 12→10 sheets and16.2846% less material; Bruce2.9893% less; Jakobs1/Marques unchanged vs preceding512-pass best. All independently valid. Three entire reports replay exactly; Bruce layout identical across deadline-limited and complete runs. All13 new attempts retained, including the rejected diversity-only strategy with two regressions. No equal-work, population, G2 or G4 claim.

- 2026-10-12T05:06:34Z | [Combined placement search, first broad development run](benchmarks/results/search-coverage-20261012T050634Z.md): all 65 development B/M jobs, seed 0, up to 1,024 passes/80M queries/60 s safety deadline; four earlier pilot runs reused, 61 new. 63 valid; **two failed**: late sheet-removal repairs on b-shapes0-strip-sheet and b-shapes1-strip-sheet admitted nearly coincident parts (independent overlap ratio about 0.99994) and the native command exited without exporting a layout. Against the preceding fixed-work layouts 43 better, 18 tied, 2 worse. Retained as failures; [raw batch](benchmarks/results/search-development-20261012T045942Z-d0c3d8fe.json). No gate claim.

- 2026-10-12T05:22:15Z | [Repair collision regression](benchmarks/results/repair-pole-collisions-20261012T052215Z.md): repair and translation separation now take the union of interior-pole (surrogate) and polygon collisions (`nestbolt-repair-v6`, `nestbolt-repack-v18`). Exact pre-failure incumbents recovered as fixtures; the old code fails and the fix passes both, replaying identically. [Corrected full rerun](benchmarks/results/search-coverage-20261012T051749Z.md): **65/65 valid**; vs preceding fixed-work layouts 45 better, 18 tied, 2 worse (remnant kit, gear2: both stop before the next compression block). Quality triage vs 52 finite three-seed 60 s competitor medians: 27 wins/ties, 15 more than 1% worse, median reduction 0.396716%; 13 jobs without a finite competitor earn no wins. Five of nine available finite 300 s targets reached within 30 s. [Raw batch](benchmarks/results/search-development-20261012T051100Z-476a0e2b.json). Development triage only; no G1/G2/G4 claim, held-out jobs unused.
- 2026-10-12T09:54:20Z | New `nestbolt sheets` command, [first fixed-sheet separator development batch](benchmarks/results/sheets-development-20261012T094605Z-f6cbed76.md) (binary `c1d8f2b0`): repacking warm start (10%), then per-sheet Sparrow separation to empty the least-filled sheet and Sparrow exploration/compression of the last sheet, 60 s wall clock, seed 0, one pinned CPU per job, all 65 development jobs. 62/65 valid; the three failures are the unsupported mixed-stock, remnant and defect jobs (no fallback yet in that binary). Against the frozen three-seed 60 s competitor medians: 34/51 wins/ties, 11 more than 1% worse, median reduction 1.1536%. Development triage only.

- 2026-10-12T10:22:40Z | [Second separator batch](benchmarks/results/sheets-development-20261012T101332Z-a64299a0.md) (binary `18dff7f0`): adds ejection chains, gradual squeeze insertion, unsimplified collision proxies and a general-search fallback for unsupported stock. 61/65 valid; **four native crashes** (Shapes0 free/given, Shapes1 free, Shirts free: `key is not valid anymore` after a separated insertion into the victim re-keyed its parts). 30/48 wins/ties, 14 more than 1% worse, median 1.0264%. Retained as failures; that elimination path was removed rather than patched.

- 2026-10-12T10:35:17Z | [Virtual-strip separator batch](benchmarks/results/sheets-development-20261012T102518Z-09573066.md) (binary `a9b6d191`): the last six sheets are laid end to end as one strip with walls (container holes); a port of Sparrow's separator to general jagua layouts shrinks the last sheet (exploration, then compression), parts move between sheets by sampling and an emptied sheet is removed. **65/65 valid**. Against the frozen competitor medians: **49/52 wins/ties (94.2%), one result more than 1% worse (jakobs1 strip-sheet, -2.091%), median reduction 6.1687%**; 13 jobs have no finite competitor. The three losses are Sparrow-best single-sheet jobs. One seed, development triage; the frozen G2 target is 10.77231474% and no gate is claimed. The record's source hashes were taken at report time, after test-only and formatting edits; the binary hash identifies the executable.
- 2026-10-12T10:41Z | Separator tuning, eight development jobs with more than six sheets, seed 0: [window of 12 sheets](benchmarks/results/sheets-window12-20261012T104100Z-d3048cfb.md) (binary `8a66e21e`) is neutral against the six-sheet window within single-seed noise. All 8 valid.

- 2026-10-12T10:43Z | [Gap filling](benchmarks/results/sheets-gapfill-20261012T104327Z-d376d1dd.md) (binary `5c7245a3`, direct left-bottom moves from the last sheet into earlier window sheets every 5 s): all 65 valid; 48/52 wins/ties, 2 more than 1% worse, median 5.8759% (v4 6.1687%); 29 jobs better and 31 worse than v4, within noise. [Gap filling with a 12-sheet window](benchmarks/results/sheets-gapfill-window12-20261012T105248Z-37fa93f1.md) on the same eight jobs: 8/8 valid, no extra sheet removed.

- 2026-10-12T10:55Z | Relocation trials on eight multi-sheet jobs, seed 0, all valid: [whole-window separation](benchmarks/results/sheets-relocate-20261012T105450Z-41158206.md) (binary `e0775228`) and [three receivers per part](benchmarks/results/sheets-relocate2-20261012T105634Z-e5414043.md) (binary `24e016a0`) still leave Shapes0 on seven sheets; tracing showed separated parts returning to the last sheet.

- 2026-10-12T11:00Z | [One-sheet relocation every 5 s](benchmarks/results/sheets-relocate-sheet-20261012T110004Z-67de9da4.md) (binary `e8c04155`): receivers are separated alone, as in the first per-sheet search. 65/65 valid; Shapes0/Shapes1 nest-mb reach six sheets (+9.9%/+9.7% vs v4), but 46 jobs are worse than v4 and the median drops to 4.1632% (46/52 wins/ties, 3 more than 1% worse). Rejected as a schedule; relocation is now limited to window starts and stalls.

- 2026-10-12T11:38Z | v4 rebuilt from commit c06294c (binary `1833afe2`), three development seeds for the A/B baseline: [seed 0](benchmarks/results/sheets-ab-v4-s0-20261012T111047Z-15a12954.md) 65/65 valid, 50/52 wins/ties, median 5.8967%; [seed 1](benchmarks/results/sheets-ab-v4-s1-20261012T111946Z-4e57aca8.md) 65/65, 48/52, median 6.4055%; [seed 2](benchmarks/results/sheets-ab-v4-s2-20261012T112845Z-6285c7e6.md) 65/65, 47/52, median 5.8958%. Single-seed triage per run; three-seed competitor medians.
