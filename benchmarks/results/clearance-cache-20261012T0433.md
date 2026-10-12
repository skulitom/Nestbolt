# Reuse of independent clearance outlines

The checker creates at most one clearance outline while comparing an original transformed part with its neighbours. It is allocated lazily and discarded after that part. No solver collision geometry is used.

| Job | Validation CPU seconds before / after | Reduction | Full-search CPU reduction |
| --- | ---: | ---: | ---: |
| m-public-gear-3 | 0.828125 / 0.687500 | 16.98% | 10.57% |
| m-mechanical-batch-1000 | 0.453125 / 0.390625 | 13.79% | 5.18% |

Each validation comparison uses before/after/after/before ordering on CPU 12. Full searches are one matched pair on CPUs 8 and 10; operating-system load varies. Both complete solver outputs and all 104 saved validation reports are unchanged. These results are development diagnostics, not G4.

[All timings and source hashes](clearance-cache-20261012T0433.json). [Exact replay](validator-replay-20261012T042700Z-96b5826b.json).
