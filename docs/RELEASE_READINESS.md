# Next preview release

Artem authorized the next GitHub release when ready on 2026-10-16. The current
candidate `aba989e` is version `0.2.0-alpha.1`; it passes local integration,
its isolated browser pilot, current package verification and all six hosted
checks. Full quality, scale and exported-curve fidelity remain required. Milestone
completion remains 45%; a preview does not close the remaining v1.1 gates.

The README describes LightBurn projects, leads, common-line limits, automatic
workers and native downloads. Its benchmark headline remains explicitly tied
to frozen v1 build `75cbb32`, with no new competitor claim.

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
  The [recovery plan and preserved interruption](../benchmarks/results/h4-depth-reboot-recovery-20261016.md)
  retain all 402 completed current-build outcomes plus 195 frozen-v1 baselines,
  then run the missing 201 Firefox outcomes with the unchanged build, jobs,
  seeds, budgets and limits. Native and Chrome quality bounds pass; full H4
  acceptance still requires Firefox, scale and export review. The original
  session is never relabelled as complete or passing.
- [Current requirement preflight](../benchmarks/results/h4-depth-requirement-preflight-20261016.md)
  verifies the eleven subset cases, all 65 development jobs, original budgets,
  seeds and physical cores, and the exact current WASM's unshared memory.
  This confirms scope and the threading constraint, not quality or scale.
- Current-build scale and independent checks of every saved SVG/DXF curve for
  all 2,000 placements in both browsers remain required, followed by screenshot
  inspection and a complete H4 requirement review.
  The [recovery-aware continuation](../benchmarks/results/h4-depth-recovered-scale-plan-20261016.md)
  runs those fixed checks only after the recovered full comparison passes;
  it preserves the original interrupted sequence unchanged.
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
- [All six hosted checks pass for the tested implementation](../benchmarks/results/preview-depth-hosted-checks-20261016.md).
  Reviewed evidence is pushed to main as `21835ba`; all product, build and
  runner inputs match tested commit `23442be`. Its newer main CI run
  [38857882488](https://github.com/skulitom/Nestbolt/actions/runs/38857882488)
  also passes all six jobs. Full recovered quality/scale/export confirmation
  remains required before publishing.

The earlier `7eba929` [full matrix](../benchmarks/results/h4-preview-score-release-20261016.md)
failed Chrome at +1.032679%; `0a9fb44` [failed at +1.046217%](../benchmarks/results/h4-preview-development-20261016.md).
Both remain preserved. No unchanged-build repeat or gate change replaces them.
Common-line exchange experiments remain isolated from production.

## Publication and disclosures

After all current-candidate checks pass, publish the verified `v0.2.0-alpha.1`
as a prerelease without replacing stable Latest. Verify actual published
downloads, checksums and source/tag provenance, including the Windows bundle.
Evidence-only commits must retain the tested product digest. No preview tag
or release has been created. Registry publication remains separate.

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
acceptance comparison remain separate actions. No preview tag or release exists yet.
