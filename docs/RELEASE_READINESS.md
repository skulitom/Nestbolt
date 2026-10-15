# Next preview release

Artem authorized the next GitHub release when ready on 2026-10-16. The release
will be a preview of the current shop-file work. The full v1.1 plan remains at
45% completed milestone weight; a release does not close its remaining gates.

The README now describes LightBurn projects, lead-in allowances, common-line
setup, automatic browser workers and native downloads. Its headline comparison
is explicitly the frozen v1 benchmark at `75cbb32`. It makes no new comparative
quality claim for this preview.

## Before publishing

- Finish and review the guarded 65-job, three-seed native/browser comparison in
  `benchmarks/results/h4-full-development-20261015/`. Its original limits and
  failed results must be preserved.
- Fix the new curve-search failure from
  [Linux CI 38819422170](https://github.com/skulitom/Nestbolt/actions/runs/38819422170/job/116712070745),
  then keep its exact input as a regression. The local reproduction reaches the
  same jagua-rs quadrant assertion; see the
  [failure record](../benchmarks/results/release-readiness-20261016.md).
- Complete the missing LightBurn import explanations identified by the
  [native diagnostic review](../benchmarks/results/h2-native-warning-review-20261015.md),
  without changing artwork or preservation semantics. Product changes wait for
  the running performance comparison to finish.
- Recheck affected geometry, native/CLI/MCP/browser behavior and performance
  after fixes. Require green CI on the release commit.
- Set the release version, finish the release notes and ensure the workflow
  marks the release as a preview without replacing the current stable Latest.
  [Packaging now accepts SemVer prerelease versions](../benchmarks/results/preview-packaging-20261016.md)
  and explicitly keeps previews out of Latest. Its tests cover version propagation and channel selection;
  the native packaging dry run remains required before pushing a tag.
- Run the packaging dry run for Windows x64, Linux x64 and macOS arm64. Verify
  archives, Windows MCPB, version agreement, checksums and provenance. Verify
  the downloaded Windows bundle after publication.

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
