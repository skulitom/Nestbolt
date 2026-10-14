# H2 repeatable warm-start deadline repair

## Diagnosis

The original training Iris DXF timed out after 360 s in the
[full fidelity sweep](h2-fidelity-20261013T202338Z.md), and again after 90 s
with a 20 s cooperative limit in the [bounded profile](h2-dense-profile-20261014T011204Z.json).
New phase markers separate the cost:

- [Model marker](h2-dense-profile-20261014T011920Z.json): model complete at 0.54 s,
  but the process still exceeds 30 s.
- [Warm-start markers](h2-dense-profile-20261014T012115Z.json): model complete at
  0.46 s; warm-start preparation 0.42 s, initial construction 0.62 s and validation
  0.82 s after entering the warm start. The initial valid layout therefore exists
  at about 1.28 s. The process still exceeds 30 s afterward.

This contradicts the earlier tentative preparation bottleneck. Repeatable-mode
warm search supplied a collision quota without a real-deadline probe. Repeated
geometry checks could consume many seconds without exhausting that quota.
Its first-construction fallback also used an unlimited control and retried any
interruption rather than only exhaustion of the work quota.

## Change and focused evidence

Both paths now use the existing real-deadline probe. Only a work-quota interruption
can trigger the one-construction fallback, and that fallback remains subject to
the real deadline. Before an incumbent exists, expiry names the fix (allow more
time); after an incumbent exists, the checked layout is retained and the result
is marked non-repeatable. Work coefficients, quotas, geometry, search defaults,
exports and the published v1 results are unchanged. Phase timings are printed
only when the existing NESTBOLT_DEBUG diagnostic flag is enabled.

An already-expired work clock reproduces the defect deterministically: the old
code incorrectly completes a fresh construction. The new regression passes and
requires the actionable timeout error instead. Original failed results remain.

The [corrected 20-second profile](h2-dense-profile-20261014T012740Z.json) completes
nesting in **20.503 s**, with final validation allowed to finish at the cooperative
boundary, and the complete fidelity command in **22.178 s**. Its one part is
independently valid, all 24 SVG/DXF contour comparisons match, maximum distance
**0.000000595 mm**, and `repeatable` is correctly false. No contour is omitted or
silently simplified. The former 30/90/360-second failed records are preserved.

## Full verification

The [complete 257-file training vector sweep](h2-fidelity-20261014T012836Z.md)
finished with **246 passes, 11 clear rejections, zero timeouts and zero errors**.
All **5,138** SVG/DXF contour comparisons match, with no missing/extra contours.
Maximum distances are **0.003301680 mm SVG** and **0.000499980 mm DXF**, both
below 0.01 mm. Every returned layout passes the independent validator.
The original one-second work budget, 240-second cooperative limit and 360-second
external timeout were retained, with one case on each of four CCD0 physical cores.
Product/binary/runner guards passed. No held-out geometry or labels were read.

All four formerly timed-out Iris files now pass. Their total command times are
241.354–243.512 seconds; all correctly report `repeatable: false` after hitting
the cooperative deadline. The other 242 successful cases complete their work
budgets. The raw R43 count mismatch is retained and governed only by its earlier
approved scoring exception; frozen labels and the split are unchanged. The
original failed full sweep and failed bounded probes remain available.

The expired-clock regression, strict Clippy, all 200 workspace tests (one
existing ignored), 20 optimized CLI feature tests and 48 Chromium/Firefox tests
(four opt-in benchmark/scale cases skipped) pass. The optimized WASM and browser
build also pass. H2/H3 are not complete: warning coverage, the required habit
fuzzing, native-project cases and held-out acceptance remain separate work.
Completed milestone weight remains 15%. This is not H4 performance or quality
acceptance.
