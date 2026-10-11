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
