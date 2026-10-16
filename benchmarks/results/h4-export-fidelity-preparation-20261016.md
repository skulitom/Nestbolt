# Saved cutting-file fidelity checker preparation — 2026-10-16

**The independent checker is ready; current candidate scale exports are still pending.**
It reads saved files and runs no searches or export regeneration. Preparation
uses two previously saved Chrome sheets from the sealed October 15 scale run;
this is not a full old-project or current-build acceptance result.

The checker parses SVG with svgpathtools 1.8.0 and DXF with ezdxf 1.4.4. Every
exported line, quadratic and cubic must match the original library primitive
under the saved placement. DXF degree, clamped knots and absence of rational
weights are checked. All entity counts, path IDs and source contours must agree.
Because Bezier basis weights are nonnegative and sum to one, the maximum control
point difference bounds the entire corresponding curve. The existing 0.01 mm
fidelity limit is unchanged.

The two old sheets cover 1,097 placements and 495,424 primitives in each format,
including all three primitive types. Maximum control error is below 0.000000707 mm.
Eight sensitivity tests pass, including deliberately moved controls, missing and
extra geometry, and an unsupported rational spline. [Exact checks](h4-export-fidelity-preparation-20261016/checks.json)
record the source archive, project and checker hashes.

Two preparation failures are preserved. The first read stock height from the
wrong saved field. The second exposed the installed single-pass DXF iterator
omitting the last entity; raw counts and the ordinary reader confirm it exists.
The final checker uses the seekable iterator and independently counts all raw
entities, so no final cut is silently skipped. No exported file was repaired.

After the current scale workflows finish, check every curve-sheet export in
both browsers, with no sheet selection. Retain that result separately from this
preparation record and from performance telemetry. H4 remains open; completion
stays 45%. No reserved geometry was opened, and no release is created here.
