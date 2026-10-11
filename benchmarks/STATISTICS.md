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
