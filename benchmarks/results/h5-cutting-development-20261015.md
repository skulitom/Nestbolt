# H5 common-line development measurement — 2026-10-15

Nestbolt: **234/234 valid runs**. Deepnest: **35/39 valid runs**.
All runs use a 60-second solver budget and seeds 0–2 on the original frozen 13-job cutting set. This is development evidence, with no held-out geometry or final acceptance run.

**H5 remains open on the material condition.** The two mechanical jobs exceed +1% at both kerfs; every other job is within the guard. No gate is relaxed. Overall completed milestone weight stays 20% (H1 and H6).

## Savings and material gate

| Kerf | Median bonus savings | Median material cost | Worst job material cost | Jobs above +1% |
| --- | ---: | ---: | ---: | ---: |
| 0.2 mm | 13.0311% | +0.0000% | +6.5085% | 2 |
| 1.5 mm | 13.1005% | +0.0000% | +5.5959% | 2 |

The 10% savings condition applies to the set median. Material is checked against normal mode at the same kerf spacing; individual jobs above +1% remain explicit failures of the strict material guard. A passing median does not waive those outliers.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-l | 0.2 | 5.767% | 25.576% | +0.339% |
| c-bracket-l | 1.5 | 4.565% | 25.505% | +0.774% |
| c-bracket-mixed | 0.2 | 4.650% | 22.054% | -0.434% |
| c-bracket-mixed | 1.5 | 2.179% | 20.943% | -1.169% |
| c-bracket-u | 0.2 | 2.805% | 19.555% | +0.000% |
| c-bracket-u | 1.5 | 1.805% | 20.225% | +0.002% |
| c-rect-equal | 0.2 | 17.217% | 30.743% | +0.000% |
| c-rect-equal | 1.5 | 38.833% | 38.833% | +0.000% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 36.217% | 36.902% | +0.000% |
| m-box-batch-500 | 0.2 | 13.120% | 13.120% | +0.000% |
| m-box-batch-500 | 1.5 | 13.768% | 13.768% | +0.000% |
| m-box-desktop | 0.2 | 1.271% | 5.305% | +0.017% |
| m-box-desktop | 1.5 | 4.167% | 4.167% | +0.029% |
| m-box-long | 0.2 | 12.858% | 12.958% | +0.000% |
| m-box-long | 1.5 | 12.318% | 12.394% | +0.000% |
| m-box-mini | 0.2 | 2.551% | 2.551% | +0.000% |
| m-box-mini | 1.5 | 7.270% | 7.270% | +0.000% |
| m-box-storage | 0.2 | 13.031% | 13.031% | +0.000% |
| m-box-storage | 1.5 | 13.101% | 13.101% | +0.000% |
| m-box-tool | 0.2 | 9.019% | 9.184% | +0.000% |
| m-box-tool | 1.5 | 10.011% | 10.011% | +0.000% |
| m-mechanical-large-plates | 0.2 | 0.000% | 12.802% | +5.219% |
| m-mechanical-large-plates | 1.5 | 0.000% | 12.826% | +4.345% |
| m-mechanical-panel-hardware | 0.2 | 0.000% | 5.025% | +6.508% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 5.205% | +5.596% |

Each entry uses the median of three seeds. Material cost is the ratio of the two material medians, not the median of per-seed ratios. The machine-readable record includes inclusive quartiles and IQR for every complete arm.

## Native Deepnest SVG comparison

The pinned, unmodified Deepnest app uses `mergeLines=true`, zero spacing, one worker and SVG export. Its native reported merged length and the actual reduction in exported SVG cutting length are separate measurements. They can differ because the exporter can merge additional coincident lines. The independent SVG oracle reconstructs linework from the original inputs and saved placements, checks physical units, missing/extra cutting geometry and unmerged total length. Nestbolt's separate validator checks each native layout before it is scored.

| Job | Valid Deepnest seeds | Nestbolt saved, laser / plasma | Deepnest reported merged length | Deepnest SVG cut saved | Deepnest SVG savings |
| --- | ---: | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 2/3 (seed 1: no_layout) | 43978.198 / 46151.998 mm | incomplete | incomplete | incomplete |
| m-box-desktop | 3/3 | 725.690 / 570.000 mm | 1080.000 mm | 1161.000 mm | 8.487% |
| m-box-long | 3/3 | 3103.800 / 2968.500 mm | 3474.000 mm | 3438.000 mm | 14.354% |
| m-box-mini | 3/3 | 120.000 / 342.000 mm | 384.000 mm | 429.000 mm | 9.120% |
| m-box-storage | 3/3 | 3699.801 / 3719.503 mm | 3112.000 mm | 3024.000 mm | 10.651% |
| m-box-tool | 3/3 | 1343.000 / 1464.000 mm | 1168.000 mm | 1184.000 mm | 8.096% |
| m-mechanical-large-plates | 3/3 | 14232.046 / 14258.027 mm | 36124.156 mm | 17856.174 mm | 16.062% |
| m-mechanical-panel-hardware | 0/3 (seed 0: no_layout, seed 1: no_layout, seed 2: no_layout) | 8832.828 / 9149.812 mm | incomplete | incomplete | incomplete |
| c-rect-equal | 3/3 | 2582.396 / 3262.000 mm | 2940.000 mm | 3130.000 mm | 37.262% |
| c-rect-mixed | 3/3 | 5601.201 / 5092.500 mm | 5225.000 mm | 5330.000 mm | 38.623% |
| c-bracket-l | 3/3 | 3222.579 / 3213.568 mm | 2937.000 mm | 3456.000 mm | 27.429% |
| c-bracket-u | 3/3 | 3089.726 / 3195.598 mm | 2702.000 mm | 3400.000 mm | 21.519% |
| c-bracket-mixed | 3/3 | 4848.388 / 4604.183 mm | 5346.000 mm | 5826.000 mm | 26.501% |

Partial successful seeds remain available as descriptive values in JSON and are not substituted for a complete three-seed median. All unsuccessful native cases remain archived and unscored. Deepnest's zero-spacing SVG is not kerf compensated: these savings are informational, not equivalent cutting instructions for either Nestbolt kerf.

## Method, provenance and limits

Product commit `c6d3955598a8e242a3eacb2e8104aed1e6b4c1ef`. Six Nestbolt lanes use physical CCD0 cores at logical CPUs 0, 2, 4, 6, 8 and 10; two Deepnest lanes use 12 and 14. No more than eight solvers run at once. Each native process tree is pinned after import and before its timed solve; setup uses CCD1. Input geometry, stock, quantities and rotation rules are unchanged. Deepnest alone uses its required zero spacing.

Normal Nestbolt mode may place small parts in holes; common-line mode disables this as required by the plan. The bonus reserves the last 10% of its search budget for local shared-edge placement and limits accepted material growth relative to that phase's starting layout. The external comparison here still measures the entire workflow against normal mode, so that local limit is not itself evidence of the H5 material condition.

Product SHA-256 `0ad15c12922fef7a55fca39b7683b485e1fb4b7f0e73846ab0d8884b9e4e167f`. Binary SHA-256 `4cec132d9540524a0007b2a0894d6682064d42709ee971b48860d4199712137a`. Cutting manifest SHA-256 `922d36732c6e7624b1c5501c8320effb12b33f37d7361cc5d5856b28d19ca814`. Product, binary, runner and input guards remained unchanged throughout each completed measurement. All 273 archives and 3654 recorded members pass their SHA-256 checks. No geometry was uploaded; the native controller blocks HTTP/HTTPS and uses no DXF conversion service.

The earlier pilot, initial line-element oracle failure and interrupted startup remain in the repository. They are separate from these full-budget results. Published v1 results and frozen splits are unchanged. No release or new acceptance claim follows from this measurement.

[Full aggregate, quartiles, failures and source hashes](h5-cutting-development-20261015.json).

Raw records:

- [h5-common-development-20261015T142414Z](h5-common-development-20261015T142414Z/results.json)
- [h5-deepnest-development-20261015T142425Z-cpu12](h5-deepnest-development-20261015T142425Z-cpu12/results.json)
- [h5-deepnest-development-20261015T142426Z-cpu14](h5-deepnest-development-20261015T142426Z-cpu14/results.json)
- [h5-deepnest-development-20261015T142806Z-cpu14](h5-deepnest-development-20261015T142806Z-cpu14/results.json)
- [h5-deepnest-development-20261015T143234Z-cpu12](h5-deepnest-development-20261015T143234Z-cpu12/results.json)
- [h5-deepnest-development-20261015T143235Z-cpu14](h5-deepnest-development-20261015T143235Z-cpu14/results.json)
- [h5-deepnest-development-20261015T143407Z-cpu14](h5-deepnest-development-20261015T143407Z-cpu14/results.json)
- [h5-deepnest-development-20261015T143608Z-cpu12](h5-deepnest-development-20261015T143608Z-cpu12/results.json)
- [h5-deepnest-development-20261015T143739Z-cpu14](h5-deepnest-development-20261015T143739Z-cpu14/results.json)
- [h5-deepnest-development-20261015T143940Z-cpu12](h5-deepnest-development-20261015T143940Z-cpu12/results.json)
- [h5-deepnest-development-20261015T144241Z-cpu14](h5-deepnest-development-20261015T144241Z-cpu14/results.json)
- [h5-deepnest-development-20261015T144312Z-cpu12](h5-deepnest-development-20261015T144312Z-cpu12/results.json)
- [h5-deepnest-development-20261015T144414Z-cpu14](h5-deepnest-development-20261015T144414Z-cpu14/results.json)
- [h5-deepnest-development-20261015T144746Z-cpu14](h5-deepnest-development-20261015T144746Z-cpu14/results.json)
- [h5-deepnest-development-20261015T145217Z-cpu14](h5-deepnest-development-20261015T145217Z-cpu14/results.json)
- [h5-deepnest-development-20261015T145248Z-cpu12](h5-deepnest-development-20261015T145248Z-cpu12/results.json)

## Verification follow-up

The maximum Nestbolt search/export process wall time was 60.6293 seconds, including work outside the 60-second solver budget. Fresh independent validation matched every saved report; the maximum numeric round-trip difference was 2.9103830456733704e-11, within the unchanged 1e-9 report tolerance.

The pushed checkpoint passed runtime checks on Linux before CI found a stale generated request schema. Regeneration adds only the optional `search_bonus` field with its default `false`; the schema consistency check passes. This does not change the benchmarked product source or binary. The original CI log and correction checks are retained in `h5-cutting-checks-20261015/`. Subsequent CI status is separate from these local checks.

Reproduce the archive verification and aggregate without overwriting evidence: `python scripts/h5_cutting_report.py --out output/h5-cutting-recheck.json`. The resulting JSON can be byte-compared with the recorded aggregate. No search or geometry import is performed.
