# H5: inspect existing relocation before adding an exchange search

This read-only review covers all 36 retained schedule trials from
`h5-schedule-probe-20261015T152046Z`: two mechanical jobs, two kerfs, three seeds
and three warm-start fractions. The historical product is `2c530e7`, with holes
reserved and the optional common-line bonus disabled. These are diagnostic
results, not a new current-build measurement or H5 pass.

The report hash, all 36 archive hashes and each archived `nested/result.json`
hash were checked. Every saved counter/history agrees exactly with the original
report, and all retained layouts have valid results. The receiver-only
`relocate` implementation is byte-identical after line-ending normalization
between that revision and the current source.

| Warm fraction | Runs | Direct insertions | Separated insertions | Failed insertions | Runs with no separated-insertion outcome |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.10 | 12 | 2 | 12 | 180 | 2 |
| 0.50 | 12 | 4 | 7 | 155 | 2 |
| 0.85 | 12 | 4 | 0 | 127 | 2 |

The existing relocation search is active in most trials, including the default
schedule. It already tries to insert a final-sheet part into an earlier sheet
and repair that receiver with the separator. A new copy of that operation would
not introduce the missing exchange mechanism.

The initial window call uses short-circuit evaluation: a successful direct
insertion skips relocation at that point. Later relocation retries require
three stalled separation outcomes and available budget. Zero outcome counters
do not prove that the function was never entered. Global disruption already
swaps parts and is not represented by these insertion counters; zero legacy
ejection counters do not establish an absence of all swaps.

Together with the [final-sheet area review](h5-last-sheet-inspection-20261015.md),
this supports testing a bounded, directed exchange: insert a final-sheet part,
return a smaller blocking part to the final sheet and repair both affected
sheets. It remains an unmeasured hypothesis. Preserve quantities, reserved holes,
deadlines, independent validation and the best incumbent. Do not change the +1%
material condition or repeat the rejected warm-schedule trials unchanged.

[Checks and all counters](h5-relocation-inspection-20261016/checks.json) and
[inspection code](h5-relocation-inspection-20261016/inspect.py) are retained.
No new searches, product edits or held-out evaluation; H5 remains open.
