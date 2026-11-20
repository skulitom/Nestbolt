# Moving inserts with their frames in common-line search

The opt-in search placed all 21 large-plate inserts and all 49 panel-hardware inserts in holes. It can now move a frame with its inserts when building rows across a sheet. It ranks the resulting placement using the original parts and their cutting paths. This four-job pilot used 60 seconds on one physical core per run, three seeds, two kerfs, and three arms. All 72 layouts validated and all eight material comparisons stayed below the +1% ceiling. [Requests and per-run exports](h5-common-rigid-host-row-pilot-20261120T164303Z/README.md).

| Job | Laser material vs ordinary | Laser cut saved | Plasma material vs ordinary | Plasma cut saved |
| --- | ---: | ---: | ---: | ---: |
| Mixed rectangles | 0.000% | 40.588% | −2.754% | 39.569% |
| Mixed brackets | −2.338% | 28.661% | −0.391% | 26.888% |
| Mechanical large plates | −0.007% | 14.436% | −1.416% | 11.954% |
| Mechanical panel hardware | +0.055% | 5.577% | −0.133% | 4.932% |

Material compares the three-seed median of the bonus arm to the ordinary arm at the same spacing. Cutting savings compare shared and separate paths for each placement. Independent reconstruction checked all 264,994 same-sheet part pairs and 3,440 shared edges. The largest difference between a COMMON segment and its source half-kerf offset was 0.009961 mm, within the 0.01 mm tolerance. [Scores, source offsets and per-sheet geometry](h5-rigid-host-rows-20261120/pilot.json).

On the 66-part laser job, the CLI, stdio MCP and Firefox completed the 30-second work budget with identical placements. Chrome reached the wall-time limit with a valid earlier placement and reported that its work budget was incomplete. Both browsers revalidated the completed native placement and produced the same four SVG/DXF files as the CLI and MCP. Six fixed-work controls covering ordinary and hole-reserving modes reproduced the archived layouts and exports. [Surface results](h5-rigid-host-rows-20261120/surfaces.json), [browser export hashes](h5-rigid-host-rows-20261120/exports.json), [compatibility controls](h5-rigid-host-rows-20261120/compatibility.json).

The previous rectangle-only pilot exceeded the laser large-plate material limit at +1.375%. The four-job result qualifies this revision for a separate 234-run confirmation on all 13 development jobs. H5 remains open at this checkpoint. [Previous pilot](h5-rectangular-rows-20261120.md) and [confirmation criteria](h5-rigid-host-rows-20261120/plan.json).
