# Published preview v0.2.0-alpha.1

Artem authorized the next GitHub release when ready on 2026-10-16. The current
product candidate `aba989e` was released as `v0.2.0-alpha.1` at `c36baa8`;
the [published downloads and provenance](../benchmarks/results/preview-depth-published-20261016.md)
and [Windows feature workflows](../benchmarks/results/preview-depth-published-features-20261016.md)
pass. It also passes local integration,
its isolated browser pilot, current package verification and all six hosted
checks. [The full H4 requirement audit](../benchmarks/results/h4-depth-complete-20261016.md)
now passes quality, scale, saved-curve fidelity and visual review. Completed
milestone weight is 60%; H2/H5 remain open and are disclosed in the preview.

The README describes LightBurn projects, leads, common-line limits, automatic
workers and native downloads. Its benchmark headline remains explicitly tied
to frozen v1 build `75cbb32`, with no new competitor claim.


**Hosted checks, 2026-10-17:** [both follow-up main commits pass all six checks](../benchmarks/results/reconciliation-20261017.md),
including 86 browser tests with four opt-in skips each. The original c36baa8
Firefox failure remains preserved with unknown cause. New failure diagnostics
remain enabled. Main's new plugin and translated/agent READMEs are reconciled;
application source and gate thresholds are unchanged.


## Candidate checks

- [Local integration](../benchmarks/results/h4-depth-integration-20261016.md) passes
  302 workspace tests (one ignored), 75 optimized core tests, 27 CLI tests,
  86 browser tests (four opt-in skips), builds, strict lint, schema/notices,
  and 23 packaging tests (one skip). Actual Windows MCPB import/nest/validate
  and confinement pass. The first inventory overlapped evidence writes; the
  original failure and same-bundle controlled recheck are both retained.
- [The isolated pilot](../benchmarks/results/h4-quadtree-depth-probe-20261016.md)
  validates all 99 layouts. Chrome +0.689439% and Firefox +0.639475% meet +1%,
  with every job within +5%. No isolated speed claim follows.
- [The original full comparison](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
  was interrupted by a Windows servicing restart after 201 native and 201 Chrome
  valid outcomes. Firefox had started but saved no outcomes; scale never began.
  The [completed recovery](../benchmarks/results/h4-depth-reboot-recovery-20261016.md)
  retains all 402 completed current-build outcomes plus 195 frozen-v1 baselines,
  and adds the missing 201 valid Firefox outcomes under unchanged limits.
  All quality conditions pass: native +0.000614%; curve-subset medians Chrome
  +0.851159% / Firefox +0.828477%, worst jobs +2.455588% / +2.561291%; full
  development aggregate and every-seed G5 limits also pass. The original
  interrupted session remains preserved. The subsequent scale/export checks
  and complete H4 review also pass.
- [Current requirement preflight](../benchmarks/results/h4-depth-requirement-preflight-20261016.md)
  verifies the eleven subset cases, all 65 development jobs, original budgets,
  seeds and physical cores, and the exact current WASM's unshared memory.
  This confirms scope and the threading constraint, not quality or scale.
- [Current-build scale and exact exported curves pass](../benchmarks/results/h4-depth-complete-20261016.md):
  both 2,000-part workloads in Chrome and Firefox, maximum RSS 1.352409 GB,
  maximum heartbeat gap 199 ms, all layouts independently valid. Every curved
  workload SVG/DXF primitive/control point for all 2,000 placements per browser
  passes 0.01 mm fidelity; all four actual screenshots are reviewed. Archives,
  source/build guards and every H4 requirement are verified. The original
  interrupted sequence remains unchanged.
- [All three downloaded packages and the Windows MCPB pass](../benchmarks/results/preview-depth-release-dryrun-20261016.md)
  on `23442be`, which contains the same tested product. Architecture, contents,
  permissions, versions and metadata match; the actual downloaded Windows
  bundle passes import/nest/validation and confinement from an isolated copy.
  Dry-run publication was skipped. The earlier `7eba929` package proof remains
  tied to its older executable.
- [Downloaded Windows feature checks](../benchmarks/results/preview-depth-features-20261016.md)
  also pass through CLI and MCPB: explicit repair/rejection messages, preserved
  editable groups/settings/fixed shapes, separate lead cutting files, matching
  validation reports and byte-identical repeat exports on authored fixtures.
- [Completed-feature applicability](../benchmarks/results/preview-depth-completed-features-20261016.md)
  binds H3/H6 preservation and lead behavior to current source and package checks.
  It retains the earlier material-cost figures as results of their original
  build, without reopening reserved projects or claiming a new measurement.
- [All six hosted checks pass for the tested implementation](../benchmarks/results/preview-depth-hosted-checks-20261016.md).
  Reviewed evidence is pushed to main as `21835ba`; all product, build and
  runner inputs match tested commit `23442be`. Its newer main CI run
  [38857882488](https://github.com/skulitom/Nestbolt/actions/runs/38857882488)
  also passes all six jobs. The recovered quality/scale/export confirmation
  is now complete. The [tag preflight](../benchmarks/results/preview-depth-publication-audit-20261016/tag/preflight.json)
  verifies unchanged tested product inputs, and the actual published downloads
  have subsequently passed all checks.

The earlier `7eba929` [full matrix](../benchmarks/results/h4-preview-score-release-20261016.md)
failed Chrome at +1.032679%; `0a9fb44` [failed at +1.046217%](../benchmarks/results/h4-preview-development-20261016.md).
Both remain preserved. No unchanged-build repeat or gate change replaces them.
Common-line exchange experiments remain isolated from production.

## Publication and disclosures

[v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is published as a prerelease; stable Latest remains v0.1.0 with unchanged assets.
All five release jobs pass. Actual downloads match their checksums, package
contents and exact source/tag provenance; Windows CLI/MCPB import, nesting,
validation, confinement and authored LightBurn/lead workflows pass. The
[publication audit](../benchmarks/results/preview-depth-publication-audit-20261016/completion.json)
preserves the original launcher and shared-cache errors and their limited
verification recoveries. No release asset was replaced or redownloaded during
recovery. Registry publication remains separate and was not performed.

[Release notes](../mcpb/RELEASE_NOTES.md) disclose:

- LightBurn preservation and lead allowances have completed their planned
  checks. Older text without cached outlines needs a native save or conversion
  to paths; groups mixing active cuts with Tool/output-disabled shapes need
  regrouping in LightBurn.
- Import acceptance still needs the remaining reserved evaluation and the
  pending denominator clarification. The split and negative fixtures stay fixed.
- Common-line cutting remains optional and under development. Two mechanical
  jobs exceed the +1% material limit, up to +6.51% in the retained comparison.
  Cut-distance savings do not establish material savings. COMMON paths require
  the documented CAM preparation to avoid duplicate cuts.
- LEADIN paths are review guides. The cutting program generates actual leads,
  and flagged contours need attention. Lead-enabled LightBurn exports include
  separate SVG/DXF cutting files alongside the preserved editable project.

The hosted browser remains on the [last Pages deployment from v0.1.0](https://github.com/skulitom/Nestbolt/actions/runs/38572138348).
The README distinguishes that hosted version from development-browser features;
this native/MCP preview does not itself dispatch the manual Pages workflow.

The published v1 claims remain unchanged. Registry publication and a new final
acceptance comparison remain separate actions. H2/H5 remain open at 60% completed weight.
