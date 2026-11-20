# Common-line cutting with optional placement inside holes

The comparison used the original 13 development jobs, three seeds and 60 seconds per run. Ordinary nesting and both common-line arms used the same kerf spacing. The two common-line arms allowed inserts inside holes. Only straight outer edges were eligible for sharing. Common-line cutting still reserves holes by default.

| Kerf | Median cutting distance saved, bonus on | Worst material change vs ordinary nesting | Jobs within +1% material | Both limits met |
| --- | ---: | ---: | ---: | --- |
| 0.2 mm | 13.031% | +1.417% | 12/13 | No |
| 1.5 mm | 13.101% | +0.546% | 13/13 | Yes |

Each job uses the median of its three seeds. The material change compares the two material medians. The cut-length threshold is 10% at each kerf. The material ceiling applies to each job at each kerf.

The remaining failure was the mixed-bracket job at 0.2 mm kerf. The bonus arm saved 21.407% of cutting distance and used 1.417% more material than ordinary nesting. None of its parts sat inside a hole. All three bonus runs slightly reduced their starting material during edge alignment. Packing had already stopped after about 54 seconds, and the complete runs finished after 55.27–55.48 seconds. This leaves 4.5 seconds or more available for packing on these inputs.

## Mechanical jobs

| Job | Kerf | Extra material with holes reserved, October | Material change with opt-in, November | Inserts in holes, ordinary / bonus | Cutting distance saved with bonus |
| --- | ---: | ---: | ---: | ---: | ---: |
| large plates | 0.2 mm | +5.219% | +0.000% | 21 / 21 | 11.036% |
| large plates | 1.5 mm | +4.345% | -1.430% | 21 / 21 | 9.574% |
| panel hardware | 0.2 mm | +6.508% | +0.149% | 49 / 49 | 2.200% |
| panel hardware | 1.5 mm | +5.596% | -0.457% | 49 / 49 | 3.531% |

As a separate check against the October ordinary material medians, 26 of the 26 November bonus-arm job/kerf pairs stay within the original +1% allowance. The largest change is +0.782%. The gate table above uses the ordinary runs from the same build and session.

The two experiments used separate matched ordinary baselines. October used the default hole policy. The [original comparison and its failures](h5-cutting-development-20261015.md) remain available.

## Geometry and export checks

All 234 of 234 layouts passed a separate CLI validation. SHA-256 checks covered 234 archives and 3,132 recorded members. The source, binary, runner and frozen-input hashes matched at the beginning and end of the run.

Independent reconstruction of the 36 mechanical layouts checked 185,236 same-sheet part distances. Across the 48 mechanical sheets in common-line mode, each exported CUT vertex matched an original outer or hole vertex within 0.000000706 mm. Every SVG CUT and COMMON segment matched its DXF counterpart. Both owners of each of the 459 reported shared edges matched their independently computed straight exterior offsets within 0.009961 mm. The permitted offset tolerance is 0.01 mm. No emitted COMMON cut was repeated.

| Kerf | Closest pair of parts | Closest insert to host hole wall |
| --- | ---: | ---: |
| 0.2 mm | 0.200001 mm | 0.210650 mm |
| 1.5 mm | 1.500001 mm | 1.512812 mm |

The CLI, browser and MCP each placed two washers inside a frame on stock that had no space for them outside the frame. A separate Clipper2 test put two inserts next to a hole wall at both kerfs. Only the edge between the inserts produced a COMMON cut. Moving one insert half a kerf closer to the wall failed validation. With the bonus enabled, straight and arc leads also passed source validation on all six contours. [Combined lead checks and exports](h5-opt-in-hole-audit-20261120/combined-lead-exports.zip).

The opt-in replay of the two original LightBurn fixtures produced byte-identical SVGs. The AutoCAD 2007 DXFs retained the same units, layer colours and all nine cutting entities at identical coordinates. Both current DXFs passed ezdxf audit without repair. The native openings took place in October. [Current fixture replay](h5-opt-in-hole-audit-20261120/native-fixture-replay.json) and [native LightBurn saves](h5-commonline-checkpoint-20261014.md#native-lightburn-evidence).

## Informational comparison with Deepnest

The original native Deepnest comparison on these same jobs used zero spacing as its merge operation requires. Rechecking all 39 archived runs and 522 member hashes retained 35 valid layouts and four runs without a layout. A job needs three valid seeds for a three-seed median. These columns report millimetres of cutting distance.

| Job | Nestbolt opt-in saved, 0.2 mm | Nestbolt opt-in saved, 1.5 mm | Deepnest reported merged | Deepnest saved in exported SVG |
| --- | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 43,978.2 | 46,152.0 | 2/3 valid | 2/3 valid |
| m-box-desktop | 686.3 | 570.0 | 1,080.0 | 1,161.0 |
| m-box-long | 3,103.8 | 2,968.5 | 3,474.0 | 3,438.0 |
| m-box-mini | 120.0 | 342.0 | 384.0 | 429.0 |
| m-box-storage | 3,699.8 | 3,719.5 | 3,112.0 | 3,024.0 |
| m-box-tool | 1,343.0 | 1,464.0 | 1,168.0 | 1,184.0 |
| m-mechanical-large-plates | 12,268.2 | 10,642.7 | 36,124.2 | 17,856.2 |
| m-mechanical-panel-hardware | 3,868.3 | 6,206.5 | 0/3 valid | 0/3 valid |
| c-rect-equal | 2,582.4 | 3,262.0 | 2,940.0 | 3,130.0 |
| c-rect-mixed | 5,601.2 | 4,380.3 | 5,225.0 | 5,330.0 |
| c-bracket-l | 3,222.6 | 3,213.6 | 2,937.0 | 3,456.0 |
| c-bracket-u | 3,213.1 | 2,940.5 | 2,702.0 | 3,400.0 |
| c-bracket-mixed | 4,706.2 | 4,633.1 | 5,346.0 | 5,826.0 |

[All 26 job and kerf comparisons, including bonus off](h5-common-opt-in-holes-20261120T135332Z/README.md), [raw requests, layouts, exports and validations](h5-common-opt-in-holes-20261120T135332Z/results.json), [independent measurements and quartiles](h5-opt-in-hole-audit-20261120/results.json), and [Deepnest archive verification](h5-opt-in-hole-audit-20261120/deepnest-replay.json).
