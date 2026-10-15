# Lead allowances through UI, CLI and MCP — 2026-10-15

Starting from `a26aaf9`, the public request now prepares lead reservations,
searches their enlarged collision shapes, selects final starts for each placed
copy, validates the resulting footprints and exports matching SVG/DXF starts.
Settings and the manual LightBurn workflow are documented in
[LEAD_INS.md](../../docs/LEAD_INS.md). H6 remains open; completed milestone weight
remains **15%**.

## Material scoring and final geometry

Original part area is separate from collision area. Fill-area and fill-priority
search order and candidate ranking value the original material, while preserving
priority as the primary objective where requested. The browser portfolio now
uses those same mode-specific objectives; previously it chose fewer sheets and
less material for every mode, including fill modes.

Stock consumption and offcuts still include lead space. The independent lead
checker rebuilds one world-space original-part-plus-leads shape per placed copy,
then reuses independent stock accounting. It retains original placed area and
priority; otherwise a larger lead could look like more useful material or be
reported as reusable offcut. Millimetre/inch tests cover identical physical
material, used height and offcut accounting.

Final planning checks actual per-copy common-line intervals and excludes their
endpoints within the existing 0.01 mm common-line tolerance. New starts must
clear stock, other copies' original reservation envelopes and already selected
new leads. Retaining unused original reservations is conservative. Valid existing
layouts can receive new starts or explicit flags without requiring the discarded
initial candidate envelopes to fit. No placement is moved by final planning.

Every placed contour is represented once as a reservation or a flag. The final
planner checks this accounting, and the independent checker reconstructs and
checks all supplied analytic leads against other parts, other leads and stock.
These remain distinct assurances: the planner still performs owner checks on
tightly flattened source curves, while the final checker exempts the owner and
does not independently derive missing-contour coverage. The broader final
coverage/owner/source-attachment audit is still required.

Length trials now round down to 0.001 mm **before** creating the lead path.
This arose during visual review: reporting three decimal places from a more
precise reserved length could describe a different native path. A new line/arc
test verifies the reported length is the constructed path length. The smallest
trial remains 0.5 mm. Native arc length calibration and source contours are
unchanged.

## Public paths and checks

- Browser controls expose kerf, length, line/arc style and outer/hole angles.
  Common-line and lead kerfs stay synchronized. Results show per-copy shortened
  lengths and explicit manual-attention flags; preview/offcut bounds include
  reserved space. Warning reports scroll without collapsing the sheet preview.
- CLI request JSON and `nest --lead-in --kerf ...` share this path. The public
  `validate --library ... --request ... --layout ...` recomputes the same report.
  The existing `validate --job ...` remains a polygon-only check.
- MCP `nest`, `validate_layout` and `export_layout` report the same lead plan.
  Browser validation and all standalone exports recompute from source settings
  and placed geometry instead of trusting a saved lead report.
- SVG/DXF keep CUT, COMMON and review-only LEADIN separate. A combined common-line
  fixture verifies each copy's actual exported start equals its lead attachment
  and both review layers survive. CLI/MCP repeat exports are byte-identical.

The final authored public fixture has two copies, each with an outer contour,
a 2 × 2 mm hole and a 0.4 × 0.4 mm hole. Browser arc runs place **391.68 mm²** of
original material; all six contours are accounted for, four leads reserve space,
two tiny-hole contours are flagged, and both larger-hole leads shorten to
**1.162 mm**. CLI arc and MCP default-line flows check their respective reports,
validation and repeat exports. These are feature checks, not material-efficiency
benchmarks or evidence of native shortened-lead behavior.

[Final Chromium preview](h6-lead-surfaces-20261015/final-chromium-lead-preview.png)
and [Firefox preview](h6-lead-surfaces-20261015/final-firefox-lead-preview.png)
show the actual browser output. Earlier screenshots, including the collapsed
preview that prompted the panel fix, are retained.

## Verification and retained failures

[Logs, source hashes, browser projects and checks](h6-lead-surfaces-20261015/checks.json)
record:

- **260 workspace tests pass**, one existing ignored, before the final length
  precision refinement. After that refinement: all **15 lead unit/property
  tests**, two public core tests, the MCP lead integration, strict Clippy and
  formatting pass. The **22 optimized CLI feature tests** also run on the
  refined core and pass.
- **54 browser tests pass**, four opt-in deployed/scale cases skipped, before
  the final precision/panel refinements. Rebuilt WASM passes six focused checks
  after the precision change, then six lead/common-line/window-layout checks
  in Chromium and Firefox after the panel fix. No retries or flaky outcomes.
- Browser production build, validator WASM, generated schema agreement, and
  packaging regression tests pass (21 passed, one platform-specific skip).
- All **1,181 frozen hashes** remain unchanged, including the frozen manifest
  `02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`.
  No held-out geometry, label, split or acceptance result was inspected or changed.

Retained initial failures were a misspelled test enum (`Units::In`), a shared-edge
fixture whose spacing was below its kerf, and a TypeScript test import missing
its NodeNext file extension. They were test/harness faults, corrected before the
passing checks. The visual precision and preview-size issues were implementation
fixes and have targeted regressions. Logs distinguish pre-refinement full runs
from the final focused checks. Builds and native tests use CCD1; no new benchmark
or native LightBurn session ran in this checkpoint.

Baseline `a26aaf9` also completed all six CI jobs in
[run 38713247396](https://github.com/skulitom/Nestbolt/actions/runs/38713247396).
That CI result belongs to the baseline, not this new source state.

## Remaining H6 work

Multipart rigid units and editable LightBurn lead rewrites still reject explicitly.
The final independent coverage/owner/source-attachment audit, native verification
of separate outer/hole settings and shortened lengths, and material-cost runs on
the common-line development set remain pending. Existing three-coupon native
evidence is unchanged and does not establish those remaining cases. No release,
registry publication or new benchmark quality claim is made.
