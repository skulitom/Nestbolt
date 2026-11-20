# SVG cutouts defined by point lists

A 40 × 30 mm frame has a 20 × 10 mm rectangular window. Both versions below imported successfully with an empty warning list in the CLI used for the preceding SVG length fix (the code on `main` at `3f9927d3`).

| Drawing | Chromium and Firefox SVG points | Previous CLI | Fixed importer |
| --- | --- | --- | --- |
| [Compact negative coordinates](../../../crates/core/tests/fixtures/compact-points.svg) | Four corners | Solid frame, 1200 mm² | One hole, 1000 mm² |
| [Word between coordinates](../../../crates/core/tests/fixtures/malformed-points.svg) | Empty point list | One hole, 1000 mm² | Import error identifies the window and requests corrected pairs |

The compact pair `10-20` denotes (10, −20). The browser test reads the original polygon's corners through the SVG DOM, imports both versions of the drawing through Nestbolt and checks that a rejected replacement clears the prior part. Core tests also check closed polylines, exponents, malformed separators, incomplete pairs and layer selection. [SVG point-list grammar](https://www.w3.org/TR/SVG11/shapes.html#PointsBNF), [browser test](../../../web/tests/import-viewport.spec.ts), [core tests](../../../crates/core/tests/import_viewport.rs).

SVG and DXF cutting files both preserved the frame and its window after nesting. All four contour comparisons matched within 0.000001 mm. Reproduce with `cargo run --locked --release -p nestbolt-core --example fidelity -- crates/core/tests/fixtures/compact-points.svg`. [Measured distances](fidelity.json)

The release CLIs read the same 257 training and 183 robustness drawings with their recorded import options. The 282 saved libraries, 158 rejection messages and all exit codes matched. Each case and its outcome also matched the previous published comparison. Four property-test seeds passed 10,000 importer checks and 1,008 nesting checks. [Binary hashes and result counts](comparison.json), [per-drawing outcomes](../h2-svg-lengths-20261120/comparison.json), [property results](habit-fuzz.json).
