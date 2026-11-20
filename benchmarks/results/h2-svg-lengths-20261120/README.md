# SVG cutouts drawn with physical units

The [regression drawing](../../../crates/core/tests/fixtures/inch-hole.svg) is a 25.4 mm square with one 6.35 mm diameter hole. On `4307deb9`, the CLI imported one solid square and returned an empty warning list. The circle's coordinates and radius use inches. The importer read only bare numbers for those attributes.

On `907f9bb5`, the imported part contains a circular arc of radius 3.175 mm centered at (12.7, −12.7) mm in the Y-up coordinate system. The browser test measures the source circle with the browser's own SVG renderer, saves a Nestbolt project, and compares all four edges of its hole with the rendered bounds. Both Chromium and Firefox passed the 0.005 mm tolerance. [Browser regression](../../../web/tests/import-viewport.spec.ts)

The G6 fidelity check nested the part, exported both cutting formats, and matched the outer and inner contours in each. The maximum Hausdorff distance was below 0.000001 mm in both SVG and DXF. Reproduce it from the repository root with `cargo run --locked --release -p nestbolt-core --example fidelity -- crates/core/tests/fixtures/inch-hole.svg`. [Measured distances and contour counts](fidelity.json)

Separate release builds of the CLI imported all 257 training and 183 robustness SVG/DXF drawings with their recorded selection, scale, and gap options. The 282 successful imports produced identical saved libraries. The 158 rejected inputs produced identical exit codes and error text. The comparison checked each input hash against the frozen manifest and used only those two development splits. H2 remains open under decision 8. [Results by drawing and binary hashes](comparison.json)
