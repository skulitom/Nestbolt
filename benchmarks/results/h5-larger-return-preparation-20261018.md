# Larger-return pair qualification — 2026-10-18

The corrected isolated candidate passes **113 optimized core tests**, strict
lint/build, ten public observer outcomes, four public CLI comparisons and five
adversarial pilot checks. Production is unchanged and H5 remains open.

The [first candidate failure and output comparison](h5-larger-return-review-20261018.md)
remain preserved. Removing the returned-area filter admits valid alternatives:
the authored larger-return witness exchanges 2,700 mm2 for 2,790 mm2 without
increasing material. The unchanged runtime first fails this regression.

## Why four tests changed

The original four route/placement assertions all fail in the first candidate,
despite valid layouts and material no greater than each input. The direct
original/broader comparison preserves those failures and every original test.

The additional gap trace reproduces its saved final layout and statistics
exactly. Eight intermediate/final layouts independently validate. The named
part moves to sheet 0 during gap filling and remains there in the first
accepted result (12,205.4484 mm2). Later compression moves it back to sheet 1
and accepts lower material (12,200.1168 mm2). This is still 0.0388 mm2 worse
than the old runtime's final result; it is not a quality improvement claim.

The corrected tests preserve the intended invariants:

- Single fallback uses a source with only one part, so no pair is available.
- The return-frame search allows its newly valid alternative, requiring an
  actual incoming transfer and strictly lower material. Existing direct
  three-piece frame, rotation and reflection checks remain exact.
- The actual runtime material comparison is extracted unchanged into a helper.
  A direct test rejects both the former +0.0007 mm2 increase and a one-ULP
  increase, even with fewer sheets, and rejects an extra sheet despite lower
  material. Equal or reduced material with no extra sheet remains allowed.
- The window test still requires exchange, post-exchange fill calls and moves,
  valid geometry and nonincreasing material, including disabled/expired paths.
  A direct exchange-then-fill test checks the named part on sheet 0 immediately
  after filling, before later optimization. Both saved layouts independently
  validate and preserve strict material nonincrease.

103 previous tests remain unchanged; four are refined as above. Six added
tests cover larger returns, disabled/expired calls, impossible return room,
frozen sheets, the strict material boundary and immediate gap filling. The six
larger-return outcomes pass twelve further frozen-CLI before/after checks.
Exact source reversal proves the runtime differences are the paired area
filter removal, its unused sum removal and the semantics-preserving guard
extraction. Ranking, caps, choices, repairs, geometry, neutral guard, fill and
all budgets are unchanged. Two preparation-script audit failures are retained;
neither started a build or search before its correction.

The passing concurrent core run interleaved test-status stdout into the direct
fill JSON on stderr. Its reader failure and merged log remain. Recovery runs
only that same authored fixed-work test with separately captured streams,
using the same compiled binary; its two saved layouts independently validate.
The full core suite and every other completed observation are not repeated.

Normal public outputs and common-mode deterministic replays are exact except
wall time. Pilot block, score, case and measurement functions remain
AST-identical to the previous pilot. The proposed comparison retains four
jobs, both kerfs, seeds 0–2, three rotating sequential arms, eight physical
CCD0 cores and 60-second searches. The +1% material requirement and complete
13-job H5 gate remain unchanged. No measured gain or integration is claimed.

[Checks](h5-larger-return-preparation-20261018/checks.json),
[trace](h5-larger-return-preparation-20261018/gap-trace-results.json),
[source/test audit](h5-larger-return-preparation-20261018/refined-checks.json)
and [verified archive](h5-larger-return-preparation-20261018/integrity.json).
