# Interlocking common-line rows in the 13-job development comparison

H5 remains open. The opt-in configuration missed one or more original limits. All 234 complete layouts passed the public validator. The comparison used ordinary nesting at matching spacing, the same 13 frozen development jobs, 60 seconds on one physical core per run, and seeds 0, 1 and 2. The two common-line arms allowed parts inside holes. Only the bonus arm searched for interlocking rows and shared edges.

| Kerf | Median cutting distance saved | Worst material change vs ordinary | Jobs within +1% material |
| --- | ---: | ---: | ---: |
| 0.2 mm | 13.031% | +0.011% (m-mechanical-large-plates) | 13/13 |
| 1.5 mm | 13.101% | +1.793% (c-rect-mixed) | 12/13 |

Each job uses three-seed medians. The material comparison divides the bonus median by the ordinary median. The cut-length gate requires the median across jobs to reach 10% separately at each kerf. The material ceiling applies to every job.

All 36 layouts passed the [two-job pilot](h5-common-native-row-pilot-20261120T154338Z/README.md) before the full comparison. The [source construction](h5-repeated-bands-20261120.md) groups up to four right-angled parts, then chooses rows that fit across the available stock. The product uses a portion of the existing common-line time allowance and checks each proposed layout against the source geometry, current material use and shared cutting length. The default common-line policy reserves holes.

## Per-job results

| Job | Laser cut saved | Laser material | Plasma cut saved | Plasma material |
| --- | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 13.120% | +0.000% | 13.768% | +0.000% |
| m-box-desktop | 5.305% | +0.000% | 4.167% | +0.025% |
| m-box-long | 12.958% | +0.000% | 12.394% | +0.000% |
| m-box-mini | 9.269% | -0.000% | 10.130% | -5.878% |
| m-box-storage | 13.031% | +0.000% | 13.101% | +0.000% |
| m-box-tool | 9.184% | +0.000% | 10.011% | +0.000% |
| m-mechanical-large-plates | 11.316% | +0.011% | 9.382% | -0.965% |
| m-mechanical-panel-hardware | 2.393% | -0.261% | 3.957% | +0.008% |
| c-rect-equal | 30.743% | +0.000% | 38.833% | +0.000% |
| c-rect-mixed | 40.588% | +0.000% | 36.754% | +1.793% |
| c-bracket-l | 25.576% | -0.000% | 25.505% | -0.021% |
| c-bracket-u | 25.680% | -0.021% | 20.178% | -0.005% |
| c-bracket-mixed | 28.661% | -3.820% | 26.888% | -2.467% |

The c-rect-mixed job at 1.5 mm exceeded the +1% ceiling. Its material change was +1.793%.

[All three arms, including the bonus-off results](h5-common-native-row-confirmation-20261120T154853Z/README.md). The [original hole-reserving comparison](h5-cutting-development-20261015.md), [first opt-in measurement](h5-opt-in-holes-20261120.md), and [experimental scheduler](h5-opt-in-material-budget-20261120.md) retain their original failures.

## Independent checks

SHA-256 verification covered 234 archives and 3,132 members. The 78 matched triples used identical source jobs and libraries. A second reading of the validated outputs reproduced the gate arithmetic. The checked product commit was `e0655297`. [Inputs and scores](h5-native-interlocking-rows-20261120/confirmation-replay.json).

Independent geometry reconstruction covered all 234 layouts, 1,389,166 part-pair distances, and 12,677 shared edges. The maximum original-to-exported CUT vertex error was 0.000000707 mm. The largest shared-edge offset difference was 0.009973 mm against 0.01 mm. Every tested SVG CUT and COMMON segment matched its DXF counterpart. [Mechanical geometry and arm distributions](h5-native-interlocking-rows-20261120/confirmation-audit.json).

The first box check flagged a 3 mm discrepancy. Its source contour divided a straight 160 mm side into three segments of 3, 154 and 3 mm. The exported offset coincides exactly with the full side. The box check now verifies continuous collinear source sections across the contour start. The 10 mm minimum overlap and 0.01 mm offset tolerance apply throughout. [Original rejection](h5-native-interlocking-rows-20261120/box-offset-first-rejection.json). [All 108 box layouts](h5-native-interlocking-rows-20261120/confirmation-boxes.json).

The CLI, stdio MCP, Chrome and Firefox produced the same 80-copy mixed-bracket layout. CLI and MCP also produced byte-identical SVGs and DXFs. Chrome’s first fixed-work run reached its 30-second wall limit and returned a valid earlier layout. Its isolated replay finished the work budget. Both browsers returned the reference layout in 15-second wall-timed runs. [Surface results](h5-native-interlocking-rows-20261120/surfaces.json). [Six fixed-work compatibility comparisons](h5-native-interlocking-rows-20261120/compatibility.json) cover ordinary nesting and the default hole policy.

The October laser SVG and plasma DXF were opened in LightBurn 2.1.01. Re-exporting both coupons with the current executable produced the same four SVG and R2007 DXF files as the earlier opt-in build. The current DXFs match the native-checked originals in units, layers and all nine cutting entities. [Current export hashes](h5-native-interlocking-rows-20261120/native-fixtures.json) and [native measurements and screenshots](h5-commonline-checkpoint-20261014.md#native-lightburn-evidence). The combined line and arc lead fixtures retain the same six validated reservations each. [Lead results](h5-native-interlocking-rows-20261120/combined-leads.json). [Build and test results](h5-native-interlocking-rows-20261120/functional-tests.json).

## Deepnest comparison

Deepnest used its required zero spacing. Its native merged-length report and measured SVG saving are separate quantities. The 39 historical runs yielded 35 layouts and four no-layout outcomes. Distances below are three-seed medians in millimetres. [Original archive verification](h5-opt-in-hole-audit-20261120/deepnest-replay.json).

| Job | Nestbolt laser saved | Nestbolt plasma saved | Deepnest native merged | Deepnest SVG saved |
| --- | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 43,978.2 | 46,152.0 | 2/3 valid | 2/3 valid |
| m-box-desktop | 725.7 | 570.0 | 1,080.0 | 1,161.0 |
| m-box-long | 3,103.8 | 2,968.5 | 3,474.0 | 3,438.0 |
| m-box-mini | 436.0 | 476.5 | 384.0 | 429.0 |
| m-box-storage | 3,699.8 | 3,719.5 | 3,112.0 | 3,024.0 |
| m-box-tool | 1,343.0 | 1,464.0 | 1,168.0 | 1,184.0 |
| m-mechanical-large-plates | 12,580.0 | 10,430.0 | 36,124.2 | 17,856.2 |
| m-mechanical-panel-hardware | 4,206.3 | 6,956.4 | 0/3 valid | 0/3 valid |
| c-rect-equal | 2,582.4 | 3,262.0 | 2,940.0 | 3,130.0 |
| c-rect-mixed | 5,601.2 | 5,072.0 | 5,225.0 | 5,330.0 |
| c-bracket-l | 3,222.6 | 3,213.6 | 2,937.0 | 3,456.0 |
| c-bracket-u | 4,057.4 | 3,188.2 | 2,702.0 | 3,400.0 |
| c-bracket-mixed | 6,300.8 | 5,911.0 | 5,346.0 | 5,826.0 |
