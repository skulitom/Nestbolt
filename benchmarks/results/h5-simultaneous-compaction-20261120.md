# Moving all last-sheet parts together

Allowing simultaneous translations of the original parts reduced material use
on all four complete mechanical layouts. Every proposal passed the public
validator and a separate check against the filled outer polygons, including
the two cases where improved placement also saved more cutting length on the
panel hardware. All four layouts still exceed their original material targets.

| Job | Kerf (mm) | Parts | Material (mm²) | Reduction from starting layout (mm²) | Above target | Cut length saved, before → after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Large plates | 0.2 | 66 | 5,119,800 | 2,094 | 2.624% | 13.576% → 13.479% |
| Large plates | 1.5 | 66 | 5,176,500 | 2,476 | 2.457% | 15.526% → 15.688% |
| Panel hardware | 0.2 | 178 | 4,927,768 | 15,205 | 4.350% | 5.659% → 7.009% |
| Panel hardware | 1.5 | 178 | 4,985,909 | 11,153 | 3.822% | 5.597% → 6.906% |

The starting points are the [four complete layouts assembled from archived
sheets](h5-archived-sheet-combinations-20261120.md). Part orientations, sheet
assignments, stock and kerfs stay fixed. A linear program moves parts on the
last sheet to reduce its used height. Each nearby pair is separated by a
supporting line. Where whole convex hulls overlap, the program separates
convex pieces of the original filled outlines. A second solve chooses the
least total movement at the achieved height.

The four initial layouts and eleven proposals all validated. Independent
geometry checks covered 79,543 same-sheet distances across those layouts.
All original quantities and first-sheet placements were preserved. The four
selected outputs also exported through the public CLI. Each case completed
in under 4.4 seconds on one logical CPU. The inputs came from earlier archive
searches, so these runs do not replace the matched 60-second H5 comparison.
[Native measurements](h5-simultaneous-compaction-20261120/results.json),
[independent measurements](h5-simultaneous-compaction-20261120/geometry-audit.json)
and [layouts, exports and process receipts](h5-simultaneous-compaction-20261120/layouts-and-exports.zip).
