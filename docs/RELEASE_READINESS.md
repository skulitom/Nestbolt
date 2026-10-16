# Next preview release

Artem authorized the next GitHub release when ready on 2026-10-16. Candidate
`7eba929` is version `0.2.0-alpha.1`, but its completed Chrome quality check
fails and it is not ready for release. The v1.1 plan remains at 45% completed
milestone weight; publishing a preview does not close its remaining gates.

The README now covers LightBurn projects, lead allowances, common-line setup,
automatic browser workers and native downloads. Its comparison headline remains
explicitly the frozen v1 benchmark at `75cbb32`, with no new competitor claim.

## Candidate checks

- [Local integration checks](../benchmarks/results/h4-score-integration-20261016.md)
  pass: 302 workspace tests, 27 optimized CLI tests, 86 enabled browser tests,
  strict lint, native/WASM/site builds, schemas/notices and actual Windows MCPB
  verification. Existing ignored/skipped tests remain disclosed in that record.
- [All six hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38840747952)
  pass on `7eba929`; [the exact record](../benchmarks/results/preview-score-ci-20261016/checks.json)
  includes Windows/Linux, web, benchmark smoke and maker rebuilds.
- [The package dry run and downloaded artifacts](../benchmarks/results/preview-score-release-dryrun-20261016.md)
  pass for Windows x64, Linux x64 and macOS arm64. The downloaded Windows CLI,
  server and MCPB pass actual version/import/nest/validation checks. Archive
  contents, executable architectures, permissions and checksum/metadata agree.
- The [full current-build comparison](../benchmarks/results/h4-preview-score-release-20261016.md)
  completed with all 603 new and 195 reused layouts valid. Native median is
  +0.000681% versus frozen v1; both full G5 comparisons pass. Firefox's curve
  subset passes at +0.881781%, but Chrome fails at **+1.032679%**, against +1%.
  Every original outcome, metric, source guard and failure is retained.
- The [conditional scale sequence](../benchmarks/results/h4-preview-score-scale-plan-20261016/stopped.json)
  stopped after sealing/reporting the quality failure. No current-build scale
  measurements were started. The [requirement preflight](../benchmarks/results/h4-requirement-preflight-20261016.md)
  verifies scope and unshared WASM memory; it does not close H4.
- [Current-build profiling](../benchmarks/results/h4-browser-profile-20261016T040030Z.md)
  completes with three valid layouts. Edge/quadtree traversal is the main sampled
  cost. The [shallower-tree isolated pilot](../benchmarks/results/h4-quadtree-depth-probe-20261016.md)
  now passes both subsets with all 99 layouts valid: Chrome +0.689439%, Firefox
  +0.639475%, every job within +5%. This candidate is not yet integrated; fresh
  full comparisons, scale and package checks remain required.

The earlier `0a9fb44` candidate's [completed comparison](../benchmarks/results/h4-preview-development-20261016.md)
failed Chrome's subset at +1.046217%, against +1%; all results are preserved.
The new finer exact-score bound first [passed its isolated subset](../benchmarks/results/h4-score-chunks-probe-20261016.md)
with Chrome +0.378238% and Firefox +0.432882%, before integration. That small
probe alone does not substitute for the current full comparison or establish
a general speed gain. The common-line experiments remain unintegrated.

## Publication and disclosures

A subsequent candidate must pass the unchanged full quality comparison, current
scale checks and complete requirement review before publication. Keep `7eba929`
unreleased and retain its failed comparison. Publish the verified
`v0.2.0-alpha.1` candidate as a prerelease without replacing stable Latest. The workflow
already enforces that channel. Later evidence-only commits do not change the
candidate's packaged contents. The existing dry-run package proof remains tied
to `7eba929`; a changed candidate needs its own package checks. Verify published
downloads/checksums and provenance afterward, including the actual Windows bundle.

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
