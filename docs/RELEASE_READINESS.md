# Next preview release

Artem authorized the next GitHub release when ready on 2026-10-16. The release
will be a preview of the current shop-file work. The full v1.1 plan remains at
45% completed milestone weight; a release does not close its remaining gates.

The README now describes LightBurn projects, lead-in allowances, common-line
setup, automatic browser workers and native downloads. Its headline comparison
is explicitly the frozen v1 benchmark at `75cbb32`. It makes no new comparative
quality claim for this preview.

## Before publishing

- The [guarded 65-job comparison](../benchmarks/results/h4-full-development-20261016.md)
  is complete: 780/780 valid layouts; native and both browser limits pass. Raw
  records and exact engines are sealed. The integrated repair changes search
  cost, so its performance still needs confirmation on the release build.
- The [exact curve-search repair](../benchmarks/results/ci-curve-optimized-profile-20261016.md)
  and authored regression are integrated. Original CI/debug failures remain
  preserved. The isolated optimized candidate passed 128 generated curve cases.
- [Native import explanations and duplicate-message repair](../benchmarks/results/native-diagnostics-surfaces-20261016.md)
  are integrated. All 56 training records, 23 focused tests and actual CLI,
  stdio MCP, Chromium and Firefox checks pass in the isolated candidate, with
  unchanged geometry/XML and original rejection messages. [Full production checks](../benchmarks/results/preview-integration-20261016.md)
  now pass: 302 workspace, 27 optimized CLI and 86 enabled browser tests, strict
  lint/builds and 23 package tests including the actual Windows MCPB.
- Recheck affected geometry, native/CLI/MCP/browser behavior and performance
  after fixes. Require green CI on the release commit.
- All six hosted checks pass on `0a9fb44`
  ([run](https://github.com/skulitom/Nestbolt/actions/runs/38830004774)).
  The integrated-build native measurement is complete with 201 valid layouts;
  its 65-job median difference from frozen v1 is 0%. Browser quality and current
  scale checks remain in progress or pending, so the release gate stays open.
- The preview version is `0.2.0-alpha.1`. Finish checking release notes and ensure the workflow
  marks the release as a preview without replacing the current stable Latest.
  [Release notes](../mcpb/RELEASE_NOTES.md) now describe the features, preparation
  steps and outstanding import/common-line limits; review them against the final build.
  [Packaging now accepts SemVer prerelease versions](../benchmarks/results/preview-packaging-20261016.md)
  and explicitly keeps previews out of Latest. Its tests cover version propagation and channel selection;
  the [three-platform dry run](../benchmarks/results/preview-release-dryrun-20261016.md)
  now passes for `0a9fb44`, including the actual downloaded Windows package checks.
- Windows x64, Linux x64 and macOS arm64 packaging passes on `0a9fb44`.
  Downloaded archive contents, architectures, versions and Windows MCPB checksum
  agree. If the final release commit changes package contents, record its own
  dry run. Published provenance and the downloaded Windows bundle still need
  verification after publication.

## Disclosures in the release notes

- LightBurn preservation and lead allowances have completed their planned
  checks. Older text without cached outlines needs a reviewed native save or
  conversion to paths. Groups mixing active cuts with Tool/output-disabled
  shapes need regrouping in LightBurn.
- Import acceptance still needs the remaining reserved evaluation and the
  pending denominator clarification. The current split and original negative
  fixtures remain unchanged.
- Common-line cutting is optional and under development. Both mechanical jobs
  exceed the planned +1% material limit, up to +6.51% in the retained development
  comparison. Cutting distance savings do not establish material savings.
  COMMON paths need the documented CAM setup to avoid duplicate cuts.
- LEADIN paths are review guides; the cutting program generates the actual
  leads. Flagged contours still need attention. Lead-enabled LightBurn exports
  include separate SVG/DXF cutting files beside the preserved editable project.
- Keep the published v1 benchmark numbers and provenance unchanged. Registry
  publication and a new final acceptance comparison remain separate actions.

No version tag or release has been created for this preview yet.
