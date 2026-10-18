# Larger-return candidate — failed tests and output review, 2026-10-18

**The candidate is not qualified. No quality pilot has started.** Removing
the paired proposal area filter makes the new valid larger-return case pass,
but the full optimized core suite reports 107 passes and four failures.
All four new tests pass. Original tests, failed binaries, sources and logs
are retained; no assertion has been changed or removed.

## Original regression and candidate failure

The unchanged runtime first fails the larger-return positive case while
impossible-return and disabled/expired checks pass. The candidate changes
only the pair proposal area rejection and unused area sum. Six actual
positive/frozen/negative outcomes pass twelve frozen-CLI before/after checks.

The four older failures concern the selected route or final placement:
- A fixture expected no paired attempt before a successful single swap.
- A roundoff fixture expected rejection of its known single swap.
- A rotated-return fixture expected all three return pieces to move.
- A gap-filling fixture expected a particular small part on the first sheet.

Their geometry/material checks passed before those assertions. This fact
alone does not justify relaxing tests or claim a quality improvement.

## Direct output comparison

Both runtimes are reproduced with logging added only after searches end.
All original assertions remain. The original runtime passes the four cases;
the broader runtime reproduces all four failures. Ten actual observations
(including the original disabled/expired window variants) pass twenty
frozen-CLI validations. Every after-layout has valid geometry/quantities
and material no greater than its own before-layout. These authored fixed-work
checks are not development quality or performance measurements.

| Case | Original final material, mm2 | Broader final material, mm2 | Difference, mm2 |
| --- | ---: | ---: | ---: |
| balanced_pair_falls_back_to_a_valid_single_exchange | 19699.999400000 | 19699.999400000 | +0.000000000 |
| return_frame_keeps_incumbent_when_roundoff_increases_charged_material | 19500.000100000 | 19433.947200000 | -66.052900000 |
| directed_exchange_uses_the_rotated_return_gap | 19699.999400000 | 19433.947200000 | -266.052200000 |
| accepted_exchange_still_fills_a_known_gap | 12200.078000000 | 12200.116800000 | +0.038800000 |

## Preserved harness failures

The first logging preparation stopped because a source fragment appeared
twice. It started no build or search. The corrected preparation scopes the
insertion to the intended test and preserves the original partial folder.
The first shared-target comparison then reused the original executable for
the broader arm; its unexpected passing test immediately stopped the run.
The two hashes were identical. That outcome was not scored. Recovery builds
only the broader arm in a fresh target, verifies a distinct executable, and
preserves the six completed original observations and twelve validations.
All source/runtime hashes, old outputs and both failures remain in the archive.

[Comparison](h5-larger-return-review-20261018/output-comparison.json),
[checks](h5-larger-return-review-20261018/checks.json) and
[exact archive integrity](h5-larger-return-review-20261018/integrity.json).
The original +1% material and full 13-job H5 requirements remain. Production
and reserved inputs are unchanged; H2/H5 remain open at 60%.

## Next investigation

The broader search produces an equally charged valid result for the old
single-fallback fixture and lower charged material for the two return-frame
fixtures. Those outcomes show that the older chosen-route assertions are not
equivalent to the whole-job geometry/material invariants. They do not by
themselves justify changing any assertion or qualify the candidate.

The gap-filling fixture is different: the broader result uses 0.0388 mm2 more
material than the original result and leaves the named small part on sheet 1.
It remains valid and below its own before-layout material. Counters record one
successful post-exchange fill, but do not identify the part that moved or prove
that this intermediate placement survives later exploration/compression.

Next, observe the actual layouts immediately before/after exchange and gap
filling, plus the final accepted snapshot, for this authored fixed-work case.
Require its final result to reproduce the saved outcome before attributing
the missing placement to filling, a different chosen swap, or later snapshot
selection. Then choose a correction and preserve targeted strict-material,
rotated-return and single-fallback coverage. Do not merely loosen four assertions
to obtain a passing suite. The quality pilot remains unopened.

[Source review](h5-larger-return-review-20261018/source-review.json) preserves
the exact fill/snapshot call site and hash. No test assertion is changed.
