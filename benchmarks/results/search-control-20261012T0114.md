# Cooperative stop and deterministic replay

One development job: `m-mechanical-batch-1000`, seed 0, up to 64 passes, CPU 14.
All three runs return the same independently valid 1,000-part layout on two sheets.
Normalized material is 1.0516419284. This is an interruption diagnostic, not a G4 claim.

| Control | Wall seconds | CPU seconds | Collision queries | Completed passes | Stop |
| --- | ---: | ---: | ---: | ---: | --- |
| 15,000 ms deadline | 15.094 | 14.9375 | 13,006,336 | 2 | deadline |
| 13,006,336 queries, replay 1 | 15.046 | 14.90625 | 13,006,336 | 2 | work limit |
| 13,006,336 queries, replay 2 | 15.859 | 15.65625 | 13,006,336 | 2 | work limit |

The first complete layout arrived at 5.562 seconds in the deadline run; its refined
replacement arrived at 13.484 seconds. Stopping during the next pass preserves that
replacement. Both fixed-work replays produce byte-identical full JSON results.
The replay allowance comes from the deadline run; it is a reproducibility test.

The limit is cooperative: an individual geometry operation or independent
validation finishes before yielding. Interruption before the first construction
finishes returns an error and writes no layout. Core tests cover cancellation
before and after the first pass and work-limit interruption during sheet repair.

[Full profiles, hashes, validation and progress](search-control-20261012T0114.json).
