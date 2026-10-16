# Current preview CPU diagnosis — 2026-10-16

**All three diagnostic layouts validate. Edge/quadtree traversal is the main sampled cost.**
These profiles investigate the failed preview; they are not a repeated quality
comparison or an H4 pass. No production code, settings or geometry changed.

## Method

Candidate `7eba929`, source digest `c571ee083d17419941bbd36440c7ff859b5aab72b1bc4139d11a8443bf2fe208`.
The [committed diagnostic plan](h4-current-profile-plan-20261016/plan.json) fixes
gear-1, sign-1 and example-gears, 60 seconds, seed 0, serial Chrome pages and
physical CCD0 CPU 8. CDP samples the same WASM entry point at 1 ms. Sampling and
main-page execution differ from the app-worker/G5 method; reported times are
diagnostic. Every original requested part and independent metric agrees,
including the public gears library/request. All guards pass with no affinity
deviation. The complete profiling process took 185.638 seconds.

## Sampled costs

All call nodes with the same function name are aggregated. Function shares refer
only to sampled time; complete profiles and all-function aggregation are retained.

| Job | Span / sampled s | Edge collection | Edge/quadrant test | Bounding-box generation |
| --- | ---: | ---: | ---: | ---: |
| m-public-gear-1 | 60.165392 / 60.165248 | 42.789% | 32.880% | 5.405% |
| m-sign-1 | 59.764119 / 59.763965 | 24.863% | 21.649% | 9.481% |
| example-gears | 59.973136 / 59.972987 | 37.273% | 37.957% | 7.446% |

The difference between profile span and sampled deltas is only 0.000144–0.000154 s
in these observations; the large missing-time interval in the earlier gear profile
is not present here. This does not establish a speed gain. Scoring still accounts
for 12.234% of sign-1 samples, but traversal is a larger target in all three jobs.

The next hypothesis is a shallower collision-index configuration in an isolated
copy, retaining the original outlines and independent validation. Test one change
at a time; fewer tree visits could instead increase leaf work. No setting change
or improvement is established by profiling alone. Do not repeat rejected generic
SIMD/allocator trials or treat this diagnostic as a replacement quality result.

[Verification](h4-browser-profile-20261016T040030Z/verification.json), [aggregation](h4-browser-profile-20261016T040030Z/aggregate.json),
[raw archive](h4-browser-profile-20261016T040030Z/raw.zip). The archive contains 46 members,
3,925,250 bytes, SHA-256 `883309e887103c53582c36487dd774e4b7fdf62580d1bffe7f87bef825853825`.
CRC, every member size and SHA-256 pass. Original source, bindings/WASM, validator,
input snapshots, profiles, layouts, validation output and runner remain retained.
H4 stays open; the preview remains unreleased and completion stays 45%.
