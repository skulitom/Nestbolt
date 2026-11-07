# Exact contact proof and guarded bulk pilot — 2026-11-07

The current per-edge clipping method agrees with two independent exact-coordinate
calculations. The whole-boundary shortcut introduces false shared segments in the
two saved near-touching cases. A guarded prototype matches all **20 tested
contexts**, but its complete kernel takes **2.453 times** the current kernel
in the fixed observations. It is rejected as a replacement. No new layout or
optimizer call follows; H2/H5 remain open at **60% completed milestone weight**.

[The contact diagnosis](h5-bulk-contact-proof-and-guarded-pilot-20261107/contact-diagnostic.json) retains both original
binary64 polygons, edge masks, full-precision WKT/WKB and exact rational segment
intervals: [augmented winner](h5-bulk-contact-proof-and-guarded-pilot-20261107/augmented-raw-and-rational.json),
[original-area winner](h5-bulk-contact-proof-and-guarded-pilot-20261107/original-raw-and-rational.json). All
[eight analytic fixtures](h5-bulk-contact-proof-and-guarded-pilot-20261107/rational-fixture-controls.json) pass. Each case
has one real filled interval and zero shared length. The strict box filter is not
the cause: its omitted edge is disjoint, while the problematic edge is retained.

[Independent strip proofs](h5-bulk-contact-proof-and-guarded-pilot-20261107/exact-strip-proofs.json) reduce each eight-edge
polygon over the owner's full x-range to its left, lower and sloping top edges.
They directly solve the sole filled interval and integrate it using squared
endpoint distances. The top drops exactly **1/2199023255552 mm** across 300 mm:
one binary64 y ULP. The disputed horizontal segment is outside except at the
common endpoint. [The proof audit](h5-bulk-contact-proof-and-guarded-pilot-20261107/independent-contact-proof.json) agrees
with the current gradients to **2.593e-11**. The false shared segments measure
**60.774488 / 63.522505 mm**; applying them would add erroneous y-gradient terms
of **30.387244 / 31.761253**, despite the tiny coordinate gap.

[Six fixed ULP controls](h5-bulk-contact-proof-and-guarded-pilot-20261107/one-ulp-controls.json) retain the failure at zero
shift and agreement at minus/plus one ULP. They are validation fixtures, not new
candidate states. Exact source-edge membership alone is insufficient: a valid
vertical intersection is slightly rounded while the false horizontal segment
lies exactly on an owner edge. Neither set-distance equality nor simple edge
membership establishes the intended integral.

[The guarded pilot contract](h5-bulk-contact-proof-and-guarded-pilot-20261107/guarded-pilot-plan.json) falls back to the
unchanged screened per-edge kernel whenever a pair has positive bulk shared
length or ambiguous/nontrivial component mapping. Other components map to a
unique original edge within the declared 1e-7 mm correspondence tolerance, then
use original edges, pivots and integration order. This is a validation prototype;
these controls do not prove correctness for all geometries.

[All pilot controls](h5-bulk-contact-proof-and-guarded-pilot-20261107/guarded-pilot-controls.json) cover the same three
saved states at both geometry levels, six ULP cases and eight synthetic cases.
There are 566 directed pairs in the six saved-state contexts: 504 take the bulk
path and 62 fall back because of shared length. All 20 gradients, clipped counts
and shared lengths match exactly; [recorded differences](h5-bulk-contact-proof-and-guarded-pilot-20261107/guarded-pilot-differences.json)
are empty. [The rollup](h5-bulk-contact-proof-and-guarded-pilot-20261107/guarded-pilot.json) remains explicit.

[Complete-kernel timings](h5-bulk-contact-proof-and-guarded-pilot-20261107/guarded-pilot-timings.json) use the fixed
old/pilot/pilot/old order and include boundary construction, clipping, component
mapping, fallback and integration. Aggregate observations are
**[0.16844019968993962, 0.15760220028460026] s** for the current kernel and **[0.40478199999779463, 0.3950247997418046] s** for the
pilot; means are **0.163021 / 0.399903 s**. The earlier clipping-only
speedup does not survive complete integration. [The decision](h5-bulk-contact-proof-and-guarded-pilot-20261107/pilot-decision.json)
rejects this implementation on measured cost without claiming stable performance
statistics or global equivalence. No complete replacement objective is prepared.

The diagnostic, independent proof and pilot processes close in
**0.412898 / 0.384328 /
2.235118 s**, respectively, under CCD1/one-thread
and 2 GiB controls: [diagnostic](h5-bulk-contact-proof-and-guarded-pilot-20261107/diagnostic-process.json),
[proof](h5-bulk-contact-proof-and-guarded-pilot-20261107/audit-process.json), [pilot](h5-bulk-contact-proof-and-guarded-pilot-20261107/pilot-process.json).
Peak committed memory is 32,768,000 bytes;
all descendants close. These are read-only diagnostics, not timed packing runs.

[Next](h5-bulk-contact-proof-and-guarded-pilot-20261107/next-step.json), retain the screened per-edge objective and review
the complete construction cost ledger before another implementation choice.
[All 25 problem keys](h5-bulk-contact-proof-and-guarded-pilot-20261107/closed-problems.json) remain closed. The latest source
attempt still has 53 failed pairs in its original-area winner and 52 in its other
winner. Four fixed arrangements and all 440 allocations remain unresolved;
retained source preparation is **40.43863689946011 s** before any new work.

Main b4e16c74 has 5 passed / 1 live jobs in the
[CI snapshot](h5-bulk-contact-proof-and-guarded-pilot-20261107/main-ci-at-review.json). The prior
[ordinary push receipt](h5-bulk-contact-proof-and-guarded-pilot-20261107/prior-main-push-receipt.json) preserves the six-job
gate and 52 remote files. This checkpoint changes evidence and status only.

[Archive checks](h5-bulk-contact-proof-and-guarded-pilot-20261107/archive-checks.json), [raw manifest](h5-bulk-contact-proof-and-guarded-pilot-20261107/raw-manifest.json),
[source bindings](h5-bulk-contact-proof-and-guarded-pilot-20261107/source-bindings.json), [historical evidence](h5-bulk-contact-proof-and-guarded-pilot-20261107/external-evidence.json)
and [runtime pins](h5-bulk-contact-proof-and-guarded-pilot-20261107/runtime-bindings.json) retain the consumed evidence.
