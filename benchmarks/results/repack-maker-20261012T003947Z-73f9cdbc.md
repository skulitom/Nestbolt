# Stable placement order and early failed-trial exit

Nestbolt constructor/repacking diagnostic: all 30 development M jobs, seed 0, 64 random samples per orientation/region, refinement=False, contacts=False, repacking_passes=4, 60-second process cap. No held-out jobs or quality gate.

30/30 independently valid layouts. All 29/29 comparable successful layouts have exactly the same layout hash as the previous repair version. Failed trials stop after the first unplaced copy; they remain unscored.

| Job | Status | Sheets | Normalized material | Elapsed seconds |
| --- | --- | ---: | ---: | ---: |
| m-box-batch-500 | valid | 3 | 2.03754902704918 | 6.719 |
| m-box-desktop | valid | 1 | 0.8370697349999999 | 0.219 |
| m-box-long | valid | 1 | 0.3257779282786885 | 0.297 |
| m-box-mini | valid | 1 | 0.72006583 | 0.110 |
| m-box-storage | valid | 1 | 0.5388926319672132 | 0.313 |
| m-box-tool | valid | 2 | 1.5310279025000002 | 0.234 |
| m-garment-bruce-1 | valid | 1 | 0.22243121100000002 | 0.250 |
| m-garment-bruce-2 | valid | 1 | 0.46745410774999996 | 0.562 |
| m-garment-bruce-3 | valid | 2 | 1.1172418073333332 | 1.984 |
| m-garment-teagan-1 | valid | 1 | 0.8471061753333333 | 0.312 |
| m-garment-teagan-2 | valid | 2 | 1.9867280085 | 0.578 |
| m-garment-teagan-3 | valid | 5 | 4.671629570666667 | 1.453 |
| m-mechanical-batch-1000 | valid | 2 | 1.0516419284 | 40.109 |
| m-mechanical-cog-washers | valid | 3 | 2.1575161475 | 1.984 |
| m-mechanical-defective-stock | valid | 3 | 2.8343804204 | 6.203 |
| m-mechanical-frame-inserts | valid | 1 | 0.5985403594262295 | 1.797 |
| m-mechanical-large-plates | valid | 2 | 1.2042315063333333 | 1.000 |
| m-mechanical-mixed-stock | valid | 2 | 1.0018446031616 | 4.218 |
| m-mechanical-mounting-kit | valid | 3 | 2.8372276299999997 | 1.062 |
| m-mechanical-panel-hardware | valid | 2 | 1.6366617187999999 | 2.469 |
| m-mechanical-remnant-kit | valid | 2 | 0.7099093899422197 | 3.156 |
| m-mechanical-small-brackets | valid | 7 | 6.830062485 | 1.140 |
| m-public-gear-1 | valid | 2 | 1.50570481 | 5.375 |
| m-public-gear-2 | valid | 2 | 1.349775505 | 5.235 |
| m-public-gear-3 | valid | 1 | 0.7371593352459016 | 23.329 |
| m-public-gear-4 | valid | 1 | 0.7994709139999999 | 8.485 |
| m-sign-1 | valid | 1 | 0.8110055 | 1.500 |
| m-sign-2 | valid | 1 | 0.6511720175 | 2.266 |
| m-sign-3 | valid | 1 | 0.1614319213114754 | 3.047 |
| m-sign-4 | valid | 1 | 0.3782463655737705 | 2.344 |

[Current full records and hashes](repack-maker-20261012T003947Z-73f9cdbc.json); [previous trial](repack-maker-20261012T000758Z-533d7bb1.md). Concurrent benchmark load means elapsed times are diagnostic, not a G4 comparison.
