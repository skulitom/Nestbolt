# Next preview release

Artem authorized the next GitHub release when ready on 2026-10-16. The current
candidate `aba989e` is version `0.2.0-alpha.1`; it passes local integration
and its isolated browser pilot. Full quality, scale, exported-curve fidelity,
hosted checks and current package verification are still required. Milestone
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
- [The full comparison plan](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
  fixes all 67 union jobs, seeds 0–2 and 60 seconds in native/Chrome/Firefox:
  603 new outcomes plus 195 verified frozen-v1 baselines. Its original bounds
  and every attempt must pass before scale measurements begin.
- Current-build scale and independent checks of every saved SVG/DXF curve for
  all 2,000 placements in both browsers remain required, followed by screenshot
  inspection and a complete H4 requirement review.
- Fresh hosted checks and three-platform package/download verification are
  required for this changed candidate. The earlier `7eba929` package dry run
  does not certify the new executable.

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
