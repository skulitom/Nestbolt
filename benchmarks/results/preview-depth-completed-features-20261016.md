# Completed LightBurn and lead evidence: preview applicability — 2026-10-16

**The completed H3/H6 evidence remains applicable to the current preview's
preservation and lead behavior.** This review opens no reserved geometry and
performs no new import, search or native application session. It changes no
milestone weight. [Checks and source identities](preview-depth-completed-features-20261016/checks.json).

Since the completed H3 review at `5fb6b5a`, four import paths have changed:
cached-text, missing-control and bounding-rectangle explanations, plus removal
of duplicated warnings. The [reviewed diff](preview-depth-completed-features-20261016/h3-diagnostic-only.diff)
leaves geometry operations intact. The preserving XML writer and cutting-sidecar
implementation are byte-identical at the Git source level. The already retained
56-project training check has 45 accepted libraries with unchanged geometry/XML
and eleven unchanged clear rejections; the reserved projects are not reopened.

Lead construction, original-source validation, layout checks and SVG/DXF export
sources are unchanged from the H6 material comparison at `77dfa55`. The
[adapter diff](preview-depth-completed-features-20261016/h6-integration-adapters.diff)
adds quick-start propagation and the optional common-line search route, moves
mixed-group rejection into the shared nesting-unit check, and uses the shared
layer-cut classification. Current integration tests and the
[actual downloaded CLI/MCPB checks](preview-depth-features-20261016.md) cover
the adapters, preserved groups, separate cutting files, reservations, explicit
flags and byte-identical repeat exports.

The measured lead material costs of **+1.0696% laser / +6.0951% plasma** remain
historical results for `77dfa55`, with all 156 original layouts and the recorded
comparison correction preserved. This review does not claim those exact costs
for a fresh search with the current preview. H6 requires cost reporting, without
a maximum cost threshold. The source/version scope in its completed report stays
unchanged. H2, H4 and H5 remain open; this review does not publish a release.
