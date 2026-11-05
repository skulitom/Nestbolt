# Frozen generator runtime on a supported Linux runner — 2026-11-04

The manual [main check run 41478150369](https://github.com/skulitom/Nestbolt/actions/runs/41478150369)
failed before maker rebuild: `ubuntu-latest` selected Ubuntu 26.04, for which
`actions/setup-python` has no Python 3.11.5 package. The other five jobs passed.
The [earlier push run on the same commit](https://github.com/skulitom/Nestbolt/actions/runs/41326907703)
passed all six checks. The original failure is preserved in
[the job log](ci-python-runner-recovery-20261104/failed-job-log.txt) and
[job records](ci-python-runner-recovery-20261104/failed-run-jobs.json).

Pin only the Linux maker-rebuild job to `ubuntu-24.04`. Keep Python 3.11.5,
generator dependencies, exact rebuild assertions, Windows coverage and all
other CI jobs unchanged. The official actions/python-versions manifest
[snapshot](ci-python-runner-recovery-20261104/python-3.11.5-manifest.json)
contains the Linux 24.04 x64 package and no 26.04 package.
Hosted confirmation is required; the original failure is not reclassified.

Repository reconciliation fast-forwarded the working branch from `379761aa`
to `34e408df`, preserving all 45 files of the new ornament example and README
update. No application or solver source changed. H2 and H5 remain open at 60%.

**Hosted confirmation, 2026-11-04:** [all six jobs on the correction pass](https://github.com/skulitom/Nestbolt/actions/runs/41848153978),
including the exact maker rebuild on Ubuntu 24.04 and Windows. The complete
[job records](ci-python-runner-recovery-20261104/recovery-complete-jobs.json)
are retained alongside the original failed run. No tests or runtime pins were relaxed.
