# Native import explanations across public surfaces — 2026-10-16

**All 56 training native projects and the real CLI, MCP and both browser checks pass.**
The reviewed candidate is now integrated for the authorized `0.2.0-alpha.1`
preview. Full production regression checks and affected performance confirmation
are recorded separately; H2 remains open on its complete audit and reserved
evaluation. No held-out geometry was opened here.

The importer explains when it uses bounding rectangles, cached text outlines or
native endpoint fallback for absent Bézier controls. Implicit zero control
coordinates count as present; a one-control fallback is not called a straight
line. Attached engraving and fixed artwork receive no false rectangle warning.
Original XML and the geometry algorithm remain unchanged.

The [first public-surface attempt](release-surface-probe-20261016/checks.json)
passed its automated checks. Screenshot review then found duplicate message
strings in both actual project downloads: ten entries but seven distinct
messages. The [failed manual review](release-surface-probe-20261016/visual-review.json)
is preserved. Public import had concatenated reader messages with nesting
messages that already contained them. It now uses the complete nesting list once.
Tests require unique arrays in CLI, MCP and browser payloads and saved libraries.

The [revised surface checks](release-surface-probe-20261016-v2/checks.json) pass
the real CLI import, stdio MCP import, Chromium and Firefox imports/downloads,
strict native lint, release WASM/site build and browser type checks. Both project
downloads now contain exactly seven unique messages in the original distinct
order. [Direct comparison](release-surface-probe-20261016-v2/followup-review.json)
finds every non-warning library field identical, including the original XML.
Screenshots were reviewed; the integrated test also explicitly checks that each
message enters the viewport after scrolling.

The [third training audit](h2-native-warning-probe-20261016-v3/checks.json) uses
exactly the same complete core source as the revised surface checks. It passes
all 56 frozen training originals: 45 accepted libraries retain every non-warning
field exactly, while eleven original rejections retain identical errors and no
partial library. Every distinct prior message remains in order. All 45 warning
arrays are unique; 30 repeated old entries are removed. Rectangle coverage is
12/12, fixed-shape coverage 14/14, cached-text 1/1, control fallback 1/1 and
fixed uncached-text explanation 2/2. All 23 focused native tests pass.

The preceding [candidate audit](h2-native-diagnostics-candidate-20261016.md),
its first failed wording check and dependency-inventory preflight remain intact.
The v3 raw archive has 234 members, 3,181,542 bytes, SHA-256
`a57abb1ccb66d265f312724d5a709b0fa11a4dd063a1329f16f97a755fc31f22`.
CRC and every member hash were verified before consolidating loose case files.
The original 1,181-file corpus inventory, labels, scoring exception and split
remain unchanged. This is diagnostic verification, not new import acceptance.

Production integration also contains the independently reviewed
[flat hole-index repair and exact CI regression](ci-curve-optimized-profile-20261016.md).
The CLI, browser package and metadata version are `0.2.0-alpha.1`; no tag,
release or registry publication has been created at this checkpoint.
