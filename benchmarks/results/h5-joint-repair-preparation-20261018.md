# Joint repair and source lowering — qualification, 2026-10-18

The [preceding 72-run pilot](h5-assignment-bridge-pilot-20261018.md) fails all four
mechanical material limits. The [authored witness](h5-joint-repair-witness-20261018.md)
establishes a fixed-assignment source that cannot fit, but permits an actual valid
joint repair when an extra part migrates. This candidate makes that repair
available to directed exchange proposals. It is isolated; production is unchanged.

## Behavior and guards

The original short exchange phase runs first. The remaining original relocation
allowance uses a temporary strip containing only the selected receiver and source.
Other active sheets are absent and cannot move; the earlier frozen prefix remains
untouched. Original item geometry, rotations, reflection, stock walls/defects and
the current source crop carry into that strip. Both outputs are then rechecked in
their exact single-sheet containers. This also enforces a crop too thin to create
the normal stable boundary blocker.

After both outputs validate, the existing bounded free-pose routine lowers source
members into newly freed space, highest first. It keeps each current orientation
and reflection, uses the same collision guards and stays within the original
deadline. Both before and after this step, charged geometry work and expiry are
checked. Final whole-job validation and material comparison remain authoritative.
Material-flat steps need canonical source-area descent and stay provisional until
a strict whole-job gain. Failure, expiry or the shared four-step cap restores the
last committed layout, matching tracker and accepted counts, including the new
joint accepted counter. Attempt/repair diagnostics remain visible.

Pair-selection counters describe the initial proposal; joint repair can move
additional members. Completed pair repair does not by itself mean the whole job
was accepted, or that each intermediate step improved material.

## Evidence and retained failures

The old-behavior contract run passes three tests and fails the five intended
missing-capability checks. The thin-crop failure guards the new helper API; it
does not establish a production crop bug, since the existing path already used
a cropped source container. An earlier attempt did not compile because two newly
authored fixture references used descriptive names; no search ran. Its logs and
sources remain. The harness also copied the prior witness executable on that
failed build; its separate notice identifies that executable as stale, never as
the failed compilation's output. Later harness records require actual test startup.

The first joint implementation passes 163/165 tests. Its two failed-target layouts
are valid and preserve the prefix/intervening sheet, but save only 29.4281 mm²:
the returned part remains raised. Four public CLI validations and ten filled-outer
pair checks preserve that diagnosis. Source lowering fixes those targets without
weakening their assertions.

The next run passes 164/165 tests. The remaining failure is a new rollback fixture
whose previously flat first move now saves 99.9452 mm² because source lowering
works. Committing that gain is correct. Two independent CLI checks and twelve
filled-outer pairs confirm it. An attempted hand-positioned lower-boundary fixture fails the internal collision
check and is retained. The corrected fixture uses the exact saved, independently
validated compacted output as its starting layout; its provenance is hashed.
All assertions and runtime code remain unchanged. The focused rollback test
passes, followed by all **165 optimized native tests**. All **157 prior test
bodies** are unchanged. The original authored-witness audit error is also retained.

Sixteen saved new outcomes receive **32 independent public CLI validations** and
**93 filled-outer pair checks**. Coverage includes actual extra-member
migration, nonadjacent selected sheets with a fixed middle and prefix, failed
repairs, disabled/expired/tiny budgets, thin crop rejection, successful acceptance,
exact replay, provisional rollback and preservation of fast-phase gains. Every
previously checked native witness is present exactly before its earlier evidence
is reused. Source reconstruction verifies all 157 files, with 153 unrelated files
unchanged and one authored saved-layout fixture added. Strict lint and the isolated observer build pass.

Ten public fixed-work outcomes and four baseline CLI comparisons pass. Ordinary
mode is exact apart from elapsed wall time, and common candidate replay is exact.
Six common outputs with real source holes pass an independent filled-outer audit
of **1,284 pairs**, at the unchanged 1e-7 mm numerical tolerance. The
public workflow actually reaches joint repair; no hole interior is used.

Original sources, binaries, logs, failures, corrected fixture, snapshots and
auditors are archived with verified member hashes and ZIP CRCs. These checks
establish functionality and preservation, not better development-job quality.

## Next decision

Prepare and commit a matched development-pilot plan, verify the unchanged scoring
and execution harness, and retain every outcome. Use the original 60-second
budget, job inputs, seeds and material limit. Only a passing pilot can justify
opening the full original 13-job H5 comparison. No production integration, new
release, held-out access, threshold change or H5 completion follows this report.

[Native/build checks](h5-joint-repair-preparation-20261018/build.json),
[saved-layout checks](h5-joint-repair-preparation-20261018/joint-checks.json),
[source audit](h5-joint-repair-preparation-20261018/source-checks.json),
[public checks](h5-joint-repair-preparation-20261018/public-checks.json),
[filled-outer audit](h5-joint-repair-preparation-20261018/public-filled-outers.json),
[archive integrity](h5-joint-repair-preparation-20261018/integrity.json).

All six hosted checks on preceding main `abd3bae` pass, including Windows, Linux, browsers and both maker rebuilds. This confirms that exact pushed checkpoint. The newly qualified joint-repair candidate remains isolated and still requires a committed matched development pilot before any integration decision. Production code and published release assets remain unchanged; H2/H5 remain open at 60%. [Six completed checks](h5-joint-repair-preparation-20261018/main-ci-abd3bae.json).

The [complete candidate patch](h5-joint-repair-preparation-20261018/candidate-complete.patch) includes the added authored fixture; [its manifest](h5-joint-repair-preparation-20261018/complete-patch.json) binds both the changed and added files. The raw archive retains the complete exact source tree.
