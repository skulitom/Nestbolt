# Current preview hosted checks and push — 2026-10-16

**All six hosted checks pass for the tested implementation.**
[Run 38854287845](https://github.com/skulitom/Nestbolt/actions/runs/38854287845) tests commit `23442be`:
Windows and Linux native checks, browser tests, both maker-corpus rebuilds,
and benchmark smoke all succeed. Windows completes at 05:49:21 UTC.

The ordinary push of reviewed evidence commit `21835ba` completes at
05:50:27 UTC, after that run finishes. Remote main is verified at that exact
commit. No force or retry was used. [Checks](preview-depth-hosted-checks-20261016/checks.json)
and the original workflow/push outputs retain the identities and results.

Every product, build, test-runner and packaging-module path listed in the check
is unchanged between the tested and pushed commits. The current product digest
remains `8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88`. The newer
[main run 38857882488](https://github.com/skulitom/Nestbolt/actions/runs/38857882488)
is still in progress at this checkpoint; it is not reported as already passed.

This completes hosted-check verification for the code under measurement.
The [full H4 comparison](h4-preview-depth-release-20261016/plan.json),
conditional browser scale workflows, all-placement exported-curve checks,
screenshots and final requirement review remain outstanding. No release,
registry publication or milestone closure follows from CI alone. Completion
remains 45%.
