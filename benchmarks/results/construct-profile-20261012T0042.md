# Constructor CPU diagnostic

Single-CPU development diagnostic on m-mechanical-batch-1000, seed 0, one construction. No equal-budget G4 claim. All preliminary trials retained; four-circle experiment reverted.

Stable best-first placement keeps the same layout hash across all ten constructions. The last matched-CPU comparison used 5.000/5.1875 CPU seconds versus 14.234375/12.40625 for the saved baseline: 61.76% less mean CPU time. Collision checks fell from 9,328,950 to 4,387,224.

The earlier four-circle prescreen experiment increased fast rejections, but timing varied and the full-search timeout remained. It was reverted. Background comparator load varied throughout; these short diagnostics do not establish production speed or the G4 gate.

| Run group | CPU seconds | Elapsed seconds |
| --- | --- | --- |
| 20261012T002228Z-02add385 | 18.53125, 18.078125 | 23.234, 20.938 |
| 20261012T002340Z-841be579 | 14.0625, 12.046875 | 14.515, 12.094 |
| 20261012T002941Z-8512e98b | 16.203125, 12.34375 | 21.640, 12.516 |
| 20261012T003729Z-313063da | 5.0, 5.1875 | 5.016, 5.203 |
| 20261012T003739Z-6db5e2af | 14.234375, 12.40625 | 14.531, 12.437 |

[All profiles, binary hashes, CPU masks and layout hashes](construct-profile-20261012T0042.json).
