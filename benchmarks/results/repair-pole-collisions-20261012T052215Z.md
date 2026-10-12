# Repair collision regression

**Both failing development jobs are fixed; all 65 development layouts pass independent validation.**

The first broad run retained 63 valid outcomes and two failed runs. Late sheet-removal trials on Shapes0 and Shapes1 admitted nearly coincident parts. The independent checker rejected overlap ratios of about 0.99994, and the native commands exited without exporting a layout. These are retained failures, not successful results.

Repair and translation separation now collect the union of certified interior-pole collisions and polygon collisions. Both traversals share the same collector and stop callback, counting each hazard once. Static hazards remain immovable. The original-geometry checker, geometry, clearance guards and acceptance tolerances are unchanged.

Valid incumbents were recovered immediately before each failed repair using deterministic query limits. The regression fixtures call the same donor, seed and ejection allowance directly. The old code fails the regression test; the corrected code passes both fixtures and repeats their complete results exactly. The full native rerun covers all 65 development jobs.

| Job | Original outcome | Corrected material | Completed passes |
| --- | --- | ---: | ---: |
| b-shapes1-strip-sheet | Failed independent validation | 2.450030525 | 652 |
| b-shapes0-strip-sheet | Failed independent validation | 2.700237850 | 1024 |

Against the older 64-pass sheet / 6-pass maker baseline, the corrected longer search improves 45 jobs, ties 18 and regresses two. The remnant job hits its query allowance after 60 passes; gear2 reaches its deadline after 52. Both stop before the next scheduled compression block. They remain visible in the results; shorter-budget finishing needs attention.

Quality triage against the 52 finite competitor medians gives 27 wins/ties, 15 results more than 1% worse, and a median material reduction of 0.396716%. Thirteen jobs have no finite competitor and do not earn wins. Five of nine available finite 300-second targets are reached within 30 seconds; 55 jobs lack a 300-second reference. This does not establish the full speed gate.

Local checks pass: 94 workspace Rust tests, four stock-helper tests, 95 Python tests, both WASM builds, lint and source/schema/notices/freeze checks. The ten held-out maker jobs remain unused.

[Original broad-run outcomes](search-coverage-20261012T050634Z.md) · [Corrected coverage and timing](search-coverage-20261012T051749Z.md)
[Regression evidence, exact fixtures, retained errors, logs and portable source hashes](repair-pole-collisions-20261012T052215Z.json)
