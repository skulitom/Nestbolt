# Common-line cutting with inserts carried by their frames

The opt-in search met the material and cut-length requirements at both kerfs. All 234 layouts passed validation. Each run used one physical core for 60 seconds. The three arms were ordinary nesting, common-line detection, and common-line search. They used identical stock, parts, spacing and seeds 0–2. Both common-line arms allowed parts inside holes. The default common-line policy reserves holes. [Raw runs and three-arm scores](h5-common-rigid-host-row-confirmation-20261120T165222Z/README.md).

| Kerf | Median cutting saved | Largest material increase vs ordinary | Within +1% |
| --- | ---: | ---: | ---: |
| 0.2 mm | 13.031% | +0.002% (m-box-desktop) | 13/13 |
| 1.5 mm | 13.101% | +0.013% (m-box-desktop) | 13/13 |

## Material and cutting distance

Material change is the ratio of the three-seed bonus median to the ordinary median, minus one. Cutting savings are the three-seed median of the fraction saved by replacing separate exterior cuts with compensated shared cuts. The 10% cutting threshold applies to the median across all 13 jobs at each kerf. The +1% material ceiling applies separately to every job.

| Job | Laser material | Laser cut saved, bonus off | Laser cut saved, bonus on | Plasma material | Plasma cut saved, bonus off | Plasma cut saved, bonus on |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| m-box-batch-500 | +0.000% | 13.120% | 13.120% | +0.000% | 13.768% | 13.768% |
| m-box-desktop | +0.002% | 1.082% | 5.727% | +0.013% | 0.000% | 4.167% |
| m-box-long | +0.000% | 12.858% | 12.958% | +0.000% | 12.318% | 12.394% |
| m-box-mini | -0.000% | 2.551% | 9.269% | -5.878% | 7.270% | 10.130% |
| m-box-storage | +0.000% | 13.031% | 13.031% | +0.000% | 13.101% | 13.101% |
| m-box-tool | +0.000% | 9.019% | 9.184% | +0.000% | 10.011% | 10.011% |
| m-mechanical-large-plates | -0.008% | 0.000% | 12.903% | -0.645% | 0.000% | 11.951% |
| m-mechanical-panel-hardware | -0.302% | 0.000% | 2.139% | -0.115% | 0.000% | 2.712% |
| c-rect-equal | -0.000% | 16.215% | 39.743% | -0.000% | 38.833% | 39.619% |
| c-rect-mixed | +0.000% | 40.588% | 40.588% | -4.071% | 36.217% | 39.569% |
| c-bracket-l | -0.700% | 4.932% | 25.576% | -0.055% | 5.054% | 25.379% |
| c-bracket-u | -0.007% | 2.302% | 25.680% | +0.000% | 2.385% | 19.978% |
| c-bracket-mixed | -4.955% | 3.833% | 28.661% | -3.073% | 2.768% | 26.888% |

## Geometry and application checks

The independent replay checked 3,132 archived files, 1,387,791 same-sheet part pairs and 13,009 shared edges against the original source. The maximum CUT vertex difference was 0.000000706 mm. The maximum half-kerf offset difference was 0.009979 mm against the 0.01 mm tolerance. [Independent geometry and matched-input checks](h5-rigid-host-rows-20261120/confirmation.json).

The solver accepted a row construction in 30 of the 78 bonus runs, including 5/6 large-plate and 1/6 panel-hardware runs. All mechanical runs retained 21 large-plate inserts or 49 panel-hardware inserts in holes. On the 66-part large-plate job, the CLI, MCP and Firefox completed the same work budget with identical placements. Chrome returned a valid earlier placement at the 30-second wall limit on both its first run and isolated replay. Given the completed placement, all four surfaces produced byte-identical SVG and DXF exports. [Pilot and controls](h5-rigid-host-pilot-20261120.md), [surface evidence](h5-rigid-host-rows-20261120/surfaces.json).

The laser SVG and plasma DXF were opened in native LightBurn 2.1.01 in October. The current export produced the same four files as the previous verified build. Its R2007 DXFs agree with the native-checked originals in units, layers and all nine cutting entities. The line and arc lead reservations also reproduced their previous validations. [Native measurements and screenshots](h5-commonline-checkpoint-20261014.md#native-lightburn-evidence).

The workspace passed 312 tests. Both release Sparrow tests passed, including one skipped in debug. The release CLI passed 28 end-to-end tests and the core passed all seven common-line geometry tests. The browser suite passed 88 tests with four optional checks skipped. [Test logs and combined-PR checks](h5-rigid-host-rows-20261120/functional.json).

## Deepnest comparison

Deepnest used its required zero spacing. Its native merged length and the saving measured from its SVG are reported separately in millimetres. The 39 runs yielded 35 layouts and four no-layout outcomes. Medians below require all three seeds. [Independent archive replay](h5-opt-in-hole-audit-20261120/deepnest-replay.json).

| Job | Nestbolt laser saved, mm | Nestbolt plasma saved, mm | Deepnest native merged, mm | Deepnest SVG saved, mm |
| --- | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 43,978.2 | 46,152.0 | 2/3 valid | 2/3 valid |
| m-box-desktop | 783.5 | 570.0 | 1,080.0 | 1,161.0 |
| m-box-long | 3,103.8 | 2,968.5 | 3,474.0 | 3,438.0 |
| m-box-mini | 436.0 | 476.5 | 384.0 | 429.0 |
| m-box-storage | 3,699.8 | 3,719.5 | 3,112.0 | 3,024.0 |
| m-box-tool | 1,343.0 | 1,464.0 | 1,168.0 | 1,184.0 |
| m-mechanical-large-plates | 14,343.5 | 13,286.2 | 36,124.2 | 17,856.2 |
| m-mechanical-panel-hardware | 3,760.3 | 4,767.0 | 0/3 valid | 0/3 valid |
| c-rect-equal | 3,338.4 | 3,328.0 | 2,940.0 | 3,130.0 |
| c-rect-mixed | 5,601.2 | 5,460.5 | 5,225.0 | 5,330.0 |
| c-bracket-l | 3,222.6 | 3,197.8 | 2,937.0 | 3,456.0 |
| c-bracket-u | 4,057.4 | 3,156.5 | 2,702.0 | 3,400.0 |
| c-bracket-mixed | 6,300.8 | 5,911.0 | 5,346.0 | 5,826.0 |
