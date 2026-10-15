# Frozen H4 browser examples

These two jobs complete the eleven-job development quality subset in
`docs/PLAN_V1_1.md`. The other nine jobs come unchanged from the frozen maker
manifest: four public gears, four signs and mechanical cog/washers.

`scripts/h4_quality_fixture.py` imports the shipped `letters.svg` and `gears.svg`
and applies the same quantities, rotation choices, sheet dimensions, margins and
clearances as `tryExample` in the app. The small `project_job` Rust example calls
the public `Request::job` conversion; every collision component and the library's
curve-clearance allowance are retained. Original libraries and requests remain
available for independent validation of the saved layouts.

Letters has 45 imported parts and 156 physical cutting pieces. Its 147 declared
glyph quantities include glyphs whose disconnected contours become separate
parts in the app. Gears has two parts and 40 copies. Neither input is simplified.
Both use the H4 measurement budget of 60 seconds and seeds 0–2, with Quick initial
layout off. Those measurement settings replace only the example button's usual
time limit; shape, stock and quantity settings are unchanged.

`manifest.json` records all input hashes, generator/executable provenance and the
original example settings. The initial preparation assertion rejected a JSON
round-trip difference of 5.684341886080802e-14 mm. That attempt is retained under its original
`benchmarks/results/h4-quality-fixture-initial-20261015` path in the raw archive
linked from `benchmarks/results/h4-quality-checkpoint-20261015.md`; the final comparison
uses the repository's existing 1e-9 absolute JSON numeric tolerance, with exact
structure, component counts and discrete values. No geometry tolerance changed.

Sources and notices: `web/public/examples/LICENSES.txt`. Letters consists of
DejaVu Sans Bold glyph outlines under the Bitstream Vera/DejaVu licence, used as
drawing geometry as prescribed by the plan. Gears is Steren's public-domain/CC0
Openclipart drawing. Neither fixture contains held-out geometry.

Do not regenerate these files after measurement. Run
`python scripts/h4_quality.py` to measure the complete subset. Shorter or partial
runs are explicitly classified as pilots and cannot pass the gate.
