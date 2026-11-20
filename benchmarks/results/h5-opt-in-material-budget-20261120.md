# Common-line cutting with a material-first time budget

**H5 remains open.** In the 234-run confirmation, the mixed-bracket job at 0.2 mm kerf saved 22.210% of cutting distance and used 1.074% more material than its matched ordinary baseline. That exceeds the +1% limit. The revised scheduler stays experimental. The opt-in hole setting on main still uses the first scheduler.

In the [first opt-in comparison](h5-opt-in-holes-20261120.md), the mixed-bracket laser job used 1.417% more material than ordinary nesting. Its three bonus runs finished in under 55.5 seconds. The revised search preserves the ordinary initial packing schedule and estimates how much of the remaining time edge alignment can use, up to 10% of the budget. The estimate uses copy counts and polygon vertices. The original default still reserves holes.

In the [36-run pilot](h5-common-material-budget-pilot-20261120T142949Z/README.md), all four material comparisons passed. Alignment of the mixed brackets began at about 58 seconds. The laser job saved 22.006% of cut length and used 0.457% less material. The following fresh confirmation uses all 13 jobs, with independently run ordinary controls.

The comparison used the original 13 development jobs, three seeds and 60 seconds per run. Ordinary nesting and both common-line arms used the same kerf spacing. The two common-line arms allowed inserts inside holes. Only straight outer edges were eligible for sharing. Common-line cutting still reserves holes by default.

| Kerf | Median cutting distance saved, bonus on | Worst material change vs ordinary nesting | Jobs within +1% material | Both limits met |
| --- | ---: | ---: | ---: | --- |
| 0.2 mm | 13.031% | +1.074% | 12/13 | No |
| 1.5 mm | 13.101% | +0.886% | 13/13 | Yes |

Each job uses the median of its three seeds. The material change compares the two material medians. The cut-length threshold is 10% at each kerf. The material ceiling applies to each job at each kerf.

The [request replay](h5-opt-in-material-budget-20261120/matched-inputs.json) checked the original job, stock, part quantities, rotations and spacing of all 168 matched triples across the two full measurements and the pilot. To reproduce the candidate, apply the [scheduler patch](h5-opt-in-material-budget-20261120/scheduler-patch.zip) to commit `105a1ad2`. [Functional test results](h5-opt-in-material-budget-20261120/functional-tests.json) and [test logs](h5-opt-in-material-budget-20261120/functional-test-logs.zip) cover the revised code.

On 18 saved mixed-bracket laser layouts across all three measurements, the native compact command rejected both its slide and relocate modes because the conservative part approximations could not represent the source arrangement. All 36 runs stopped before changing a placement. [Source layouts, requests and command output](h5-opt-in-material-budget-20261120/conservative-compaction.zip).

## Mechanical jobs

| Job | Kerf | Extra material with holes reserved, October | Material change with opt-in, November | Inserts in holes, ordinary / bonus | Cutting distance saved with bonus |
| --- | ---: | ---: | ---: | ---: | ---: |
| large plates | 0.2 mm | +5.219% | +0.006% | 21 / 21 | 10.631% |
| large plates | 1.5 mm | +4.345% | +0.886% | 21 / 21 | 7.720% |
| panel hardware | 0.2 mm | +6.508% | -0.015% | 49 / 49 | 2.406% |
| panel hardware | 1.5 mm | +5.596% | -0.322% | 49 / 49 | 4.898% |

As a separate check against the October ordinary material medians, 26 of the 26 November bonus-arm job/kerf pairs stay within the original +1% allowance. The largest change is +0.810%. The gate table above uses the ordinary runs from the same build and session.

The two experiments used separate matched ordinary baselines. October used the default hole policy. The [original comparison and its failures](h5-cutting-development-20261015.md) remain available.

## Geometry and export checks

All 234 of 234 layouts passed a separate CLI validation. SHA-256 checks covered 234 archives and 3,132 recorded members. The source, binary, runner and frozen-input hashes matched at the beginning and end of the run.

Independent reconstruction of the 36 mechanical layouts checked 185,183 same-sheet part distances. Across the 48 mechanical sheets in common-line mode, each exported CUT vertex matched an original outer or hole vertex with a maximum error of approximately 0.000000707 mm. Every SVG CUT and COMMON segment matched its DXF counterpart. Both owners of each of the 456 reported shared edges matched their independently computed straight exterior offsets within 0.009961 mm. The permitted offset tolerance is 0.01 mm. No emitted COMMON cut was repeated.

| Kerf | Closest pair of parts | Closest insert to host hole wall |
| --- | ---: | ---: |
| 0.2 mm | 0.200001 mm | 0.210650 mm |
| 1.5 mm | 1.500001 mm | 1.512812 mm |

The CLI, browser and MCP each placed two washers inside a frame on stock that had no space for them outside the frame. A separate Clipper2 test put two inserts next to a hole wall at both kerfs. Only the edge between the inserts produced a COMMON cut. Moving one insert half a kerf closer to the wall failed validation. With the bonus enabled, straight and arc leads also passed source validation on all six contours. [Combined lead checks and exports](h5-opt-in-hole-audit-20261120/combined-lead-exports.zip).

The opt-in replay of the two original LightBurn fixtures produced byte-identical SVGs. The AutoCAD 2007 DXFs retained the same units, layer colours and all nine cutting entities at identical coordinates. Both current DXFs passed ezdxf audit without repair. The native openings took place in October. All four SVG/DXF fixture exports were byte-identical between the first opt-in build and the revised scheduler. [Current fixture hashes](h5-opt-in-material-budget-20261120/native-fixtures.json). [Current fixture replay](h5-opt-in-hole-audit-20261120/native-fixture-replay.json) and [native LightBurn saves](h5-commonline-checkpoint-20261014.md#native-lightburn-evidence).

## Informational comparison with Deepnest

The original native Deepnest comparison on these same jobs used zero spacing as its merge operation requires. Rechecking all 39 archived runs and 522 member hashes retained 35 valid layouts and four runs without a layout. A job needs three valid seeds for a three-seed median. These columns report millimetres of cutting distance.

| Job | Nestbolt opt-in saved, 0.2 mm | Nestbolt opt-in saved, 1.5 mm | Deepnest reported merged | Deepnest saved in exported SVG |
| --- | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 43,978.2 | 46,152.0 | 2/3 valid | 2/3 valid |
| m-box-desktop | 725.7 | 548.0 | 1,080.0 | 1,161.0 |
| m-box-long | 3,103.8 | 2,968.5 | 3,474.0 | 3,438.0 |
| m-box-mini | 120.0 | 342.0 | 384.0 | 429.0 |
| m-box-storage | 3,699.8 | 3,719.5 | 3,112.0 | 3,024.0 |
| m-box-tool | 1,343.0 | 1,464.0 | 1,168.0 | 1,184.0 |
| m-mechanical-large-plates | 11,818.4 | 8,582.0 | 36,124.2 | 17,856.2 |
| m-mechanical-panel-hardware | 4,230.0 | 8,609.8 | 0/3 valid | 0/3 valid |
| c-rect-equal | 2,582.4 | 3,262.0 | 2,940.0 | 3,130.0 |
| c-rect-mixed | 5,601.2 | 4,346.6 | 5,225.0 | 5,330.0 |
| c-bracket-l | 3,222.6 | 2,841.6 | 2,937.0 | 3,456.0 |
| c-bracket-u | 3,126.4 | 3,059.1 | 2,702.0 | 3,400.0 |
| c-bracket-mixed | 4,882.7 | 4,720.2 | 5,346.0 | 5,826.0 |

[All 26 job and kerf comparisons, including bonus off](h5-common-material-budget-confirmation-20261120T143452Z/README.md), [raw requests, layouts, exports and validations](h5-common-material-budget-confirmation-20261120T143452Z/results.json), [independent measurements and quartiles](h5-opt-in-material-budget-20261120/confirmation-audit.json), and [Deepnest archive verification](h5-opt-in-hole-audit-20261120/deepnest-replay.json).
