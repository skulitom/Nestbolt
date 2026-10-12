# Development comparison statistics

Policy recorded on 2026-10-11, before any Nestbolt search implementation or tuning
and before any held-out optimiser run. Earlier pilot tables retain their original
single-seed or valid-only scope; no old artifact is rewritten.

Every declared seed participates in a comparison. Sort independently valid scores
from best to worst (lower is better), followed by every invalid, no-layout,
unsupported, timed-out or failed attempt. Failed attempts receive no fabricated
numeric score. They act as failure-valued observations after all finite scores.
An unattempted or unaudited seed is missing: the group is incomplete and cannot
provide comparison statistics.

Use the inclusive percentile convention: rank `(n - 1) * p`, linearly interpolated
between adjacent observations. If an observation needed by that interpolation is
a failure, the percentile is a failure, represented explicitly with a null value.
No JSON Infinity, zero substitute or dropped seed is allowed.

For example, three outcomes with scores 1, 2 and a failure have comparison median
2, Q1 1.5 and a failed Q3. Their valid-only median is 1.5, which is a diagnostic and
must not be substituted into the comparison. One valid score and two failures
produce a failed median. Every table still reports the success/failure counts.

A comparison median is usable only when every declared attempt is audited, the
group contains at least three seeds, and its ranked median is finite. Tool and
configuration groups remain separate before selecting the better available
competitor. A failed or missing comparison cannot establish a percentage reduction
or be silently omitted from dataset coverage. Baseline-gap and final gate tables
must report that coverage explicitly.

This rule does not weaken G1: every Nestbolt output must still be valid across the
full required matrix. A finite Nestbolt median with a failed seed cannot pass G1.

## Gate definitions frozen before M2 implementation

For each job and budget, let C be the lowest finite comparison median among
Deepnest, SVGnest and applicable Sparrow, across their two declared settings.
LBF is the construction baseline, not a G2 competitor. Let L be LBF's lowest
finite comparison median across its settings, and N be Nestbolt's median.
All quantities use the original-job material score in SCORING.md.

- Material reduction is 100 * (1 - N/C). Positive means Nestbolt uses less.
- A tie means abs(N-C) <= 0.000001 * C (0.0001% relative). A win is N below
  that interval. The 1% maximum regression uses N/C <= 1.01 without rounding.
- Calculate headline medians and win/tie rates separately at 60 and 300 seconds;
  each eligible job has equal weight within its budget. Both budgets must pass.
  The long subset does not get extra weight in the 60-second headline.
- No finite competitor median means no numerical comparison, not a free win.
  Report such jobs separately with every tool's outcome and Nestbolt's success
  rate. Exclude them from both the reduction median and win/tie denominator,
  and publish that denominator next to each headline. G1 still covers them.
  Missing required attempts block the gate; they are not comparator failures.
- For M1, calculate gap_b = median(100 * (1 - C/L)) on development jobs with
  both finite C and L at budget b. Publish each population and all omitted
  outcomes. Freeze target = max(5, 0.5 * max(0, gap_60, gap_300)) percent after
  the complete M1 comparison. Use that same target for both G2 budgets. Never
  recompute the target from held-out or final Nestbolt results.
- The baseline gap is therefore the material saved by the best competitor
  relative to LBF, not LBF's excess divided by competitor material. To beat a
  competitor by target t, a job with gap g needs 100 * (1-(1-g/100)*(1-t/100))
  percent reduction relative to LBF. A 10.6% gap and a 5% target imply 15.07%.

These definitions were recorded after provisional competitor pilots but before
Nestbolt search or held-out optimisation. The suggested single-seed 10.6% gap is
indicative only; it cannot set the final M1 target.

Structural non-applicability may be established without running a solver only
from a documented capability limitation or a necessary mathematical bound
(for example, total net part area exceeds a single sheet for a strip-only tool).
A previous timeout or non-fitting result is not such a proof. Preserve already
completed evidence. A deterministic one-pass run may be reused in a future
budget table only with an explicit link and reuse label, never as a new run.

Harness faults may have explicitly selected replacement attempts. Retain and audit
the original record and every replacement outcome; never select by score. The
current report recognizes checker-build failures before launch, the historical
exact-coordinate import guards before SVGnest or Deepnest starts, Deepnest affinity setup
before solving, and Deepnest process cleanup after the budget. Native solver
crashes, invalid layouts, no-layout results and timeouts are not eligible. This
repairs development harness evidence; it does not waive frozen final-run controls.
