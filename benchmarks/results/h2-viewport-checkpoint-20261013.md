# SVG page sizing and DXF width warnings — 2026-10-13

**H2 remains incomplete; completed milestone progress is 15%.**

SVG imports now apply the page's `viewBox`, aspect-ratio setting, alignment and
root transform in the correct order. Height-only pages set the scale too.
Malformed or relative page sizes and unsupported nested viewports return a
repair instruction. Slice mappings warn when complete paths extend beyond the
page because viewport clipping does not trim cutting geometry. These rules
follow the [SVG viewport specification](https://www.w3.org/TR/SVG2/coords.html#ComputingAViewportsTransform).

DXF constant and variable polyline widths retain their original centrelines and
now warn explicitly. The warning names the fix when the wider outline is the
intended cut. All ten frozen training width fixtures import with matching part
and hole counts and the expected warning. Geometry, labels and split are unchanged.

[Training imports](h2-import-training-20261013T213953Z.json) retain all previous
results: 246 imports, 11 rejections, 245 raw count matches and 246 reviewed matches
with the approved R43 exception. Maximum time is 0.516 s.
[Robustness](h2-import-robustness-20261013T214000Z.json) retains 36 imports and
147 rejections, with no crash or timeout; maximum time is 0.794 s.

[All 21 training SVG files](h2-fidelity-20261013T214119Z.md) were rerun through
nesting, independent validation, SVG/DXF export and re-import: 17 pass and four
retain their clear rejections. The 1,094 contour comparisons have no unmatched
contours; maximum distance is 0.003301680 mm for SVG and 0.000497299 mm for DXF,
below the 0.01 mm requirement. This measures fidelity against imported curves;
it does not establish source-feature completeness or H2 acceptance.

Validation: 176 workspace tests pass, with one existing ignored test; six focused
import tests cover page mappings, curves, invalid pages and both width formats.
CLI and MCP check exact bounds and warnings. Eighteen unique browser checks pass
across Chromium and Firefox, including independent browser coordinates for the
authored SVG and visible import warnings. Strict Clippy, browser type checking,
schemas, native/WASM/web builds and all 1,181 frozen hashes pass.

The initial Chromium rendering-oracle check differed by 0.000788 mm because CSS
layout rounds page dimensions. Its browser-only tolerance was corrected from
0.0005 to 0.005 mm; native bounds retain 1e-9 mm checks. The initial 17-pass/1-fail
run and the two passing reruns are recorded in the
[machine-readable checkpoint](h2-viewport-checkpoint-20261013.json), together
with a Python-environment launch failure before any benchmark child started.

Benchmarks ran on CCD0 physical cores with unchanged source/binary hashes;
builds and tests ran on CCD1. No held-out geometry or labels were examined.
Four dense DXF fidelity timeouts, two thin-shape nesting errors, remaining warning
coverage, habit fuzzing, native-project support and the held-out scoring question
remain open. N2–N5 are also incomplete.
