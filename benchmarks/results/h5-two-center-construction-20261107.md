# Two-center construction — 2026-11-07

The finite pipeline closes after **two calls**, with **33,907.097540 mm² original
overlap and 50 failing source pairs** in its best candidate. Fixed-part and stock
checks pass, but no valid full66 layout is established. H2/H5 remain open at
**60% completed milestone weight**. No native call or allocation exclusion follows.

## Closed finite search and independent replay

The [source preflight](h5-two-center-preflight-20261107.md) supplies the original
unoptimized initializer and retains **33.769462 s**
of complete preparation. The [frozen contract](h5-two-center-construction-20261107/search-plan.json) permits
at most two 4 s calls, with the second shortened at the 54 s source-check boundary.
Selection and key grouping stop at 52 s. Algorithm/shared limits remain 60/90 s
including preparation, inside the verified 2 GiB Windows Job.

| Epoch | Optimizer evaluations | Saved improvements | Original overlap (mm²) | Failed source pairs |
| --- | ---: | ---: | ---: | ---: |
| 0 | 59 | 51 | 34,763.826160 | 52 |
| 1 | 31 | 27 | 33,907.097540 | 50 |

[Independent response replay](h5-two-center-construction-20261107/response-audit.json) checks all
**92 evaluation records**, **78
saved points**, all **528 updated weights**, every dynamic model and all three
winner streams. The three streams coincide within each epoch; all six full66
outputs remain preserved. Each source check reconstructs 66 original parts,
1,380 same-sheet pairs, 264 stock edges, 90 cutouts and 10,026 hole vertices.
Maximum independent evaluation score error is 5.821e-11
mm²; maximum scalar winner-gradient error is
1.634e-13 mm under the recorded boundary conventions.

[Complete runtime reconstruction](h5-two-center-construction-20261107/runtime-selection-audit.json) verifies
all **9,102 center trials**, **23,419 raw proposals** and **2,854 complete key minima**:
32,521 full independently rebuilt scores. The runtime uses full recalculation,
with no original-source cache. The selected changes are **[[11, 1], [13, 1]]**.
All [eighteen problem keys](h5-two-center-construction-20261107/closed-problems.json) now stay closed; different
coordinates never authorize another call for an existing key.

The [closed result](h5-two-center-construction-20261107/closed-search-result.json) stops after its source checks.
Preparation-inclusive algorithm/shared totals are
**54.572660/54.684802 s**. Recorded slice
overruns are **0.050725** and
**0.105534 s**; neither overall limit is exceeded.
[All five processes close](h5-two-center-construction-20261107/closed-search-process.json), with peak aggregate
committed memory of 152,592,384 bytes.
The separate [complete response audit](h5-two-center-construction-20261107/response-audit-process.json) closes
in 656.462557 s. This finite pipeline cannot resume.

## Coverage, residual geometry and runtime cost

[Same-context coverage](h5-two-center-construction-20261107/runtime-coverage-and-time.json) filters the recorded
pool to its exact 5,911 first-center proposals, retaining identical runtime state,
weights and exclusions. Using independent full scores, second-center combinations
strictly improve **659 eligible key minima**.
The best eligible placement **does not change**; its independent objective decrease is
**0.000000 mm²**, and selected center ranks
are **[0, 0]**. These scores do not establish a packing benefit.

The measured weight-update/selection/output/model interval is
**12.272820 s**, leaving only
**2.563988 s** for the second call. That interval
includes serialization and model verification; it is not a pure scoring-kernel timing.
The best candidate still fails more pairs than the preceding current-mode run
(50 versus 47), but [historical comparisons](h5-two-center-construction-20261107/prior-comparisons.json) are not
controlled experiments and do not establish a causal performance difference.

[Residual diagnosis](h5-two-center-construction-20261107/outcome-diagnostic.json) records 50
positive original/clearance pair terms, 0
flat available pair gradients, 0 bracket/bracket
source failures and 3 cogs whose negative-gradient
descent is blocked at their lower-y bound. [Family failures](h5-two-center-construction-20261107/family-failures.json)
and the complete failed geometry are preserved. No diagnostic changes a candidate.

[Read-only profiling](h5-two-center-construction-20261107/selector-profile.json) runs the unchanged uncached
selector once in the already audited runtime context. Every returned proposal,
alias, center trial and selected center agrees exactly with the closed search.
Instrumented time is 14.745650 s; instrumentation adds
overhead, so this is function attribution, not a production speed claim.
[All profile functions](h5-two-center-construction-20261107/profile-functions.json) and raw profiler data are retained.

| Function | Calls | Self seconds | Cumulative seconds |
| --- | ---: | ---: | ---: |
| `h5_two_center_neighbors_20261107.py:39 neighbors` | 1 | 0.399120 | 14.743840 |
| `h5_two_center_neighbors_20261107.py:118 emit` | 23,419 | 0.980727 | 8.220857 |
| `decorators.py:73 wrapped` | 160,337 | 0.362723 | 5.845642 |
| `decorators.py:171 wrapper` | 129,608 | 0.093568 | 5.505257 |
| `set_operations.py:112 intersection` | 46,616 | 4.838179 | 4.838179 |
| `h5_bracket_augmented_objective_20261107.py:21 problem_key` | 23,419 | 0.023727 | 2.647380 |
| `h5_bracket_augmented_objective_20261107.py:10 canonical_digest` | 23,421 | 0.039224 | 2.623721 |
| `__init__.py:183 dumps` | 23,421 | 0.047718 | 2.459591 |
| `encoder.py:183 encode` | 23,421 | 0.043498 | 2.394469 |
| `encoder.py:205 iterencode` | 23,421 | 2.340164 | 2.340164 |
| `h5_two_center_neighbors_20261107.py:126 <listcomp>` | 23,419 | 2.065071 | 2.065071 |
| `~:0 <built-in method builtins.sum>` | 55,682 | 0.093566 | 1.342281 |

Cumulative times overlap and must not be summed. The bounded profile process
[closes normally](h5-two-center-construction-20261107/selector-profile-process.json), with zero optimizer calls.
Repeated problem-key calculation accounts for 2.647380 s cumulative; constructing
the 528-entry pair-loss list for each proposal accounts for 2.065071 s self time.
These measured operations motivate local per-context digest reuse and ordered
NumPy pair gathering as the next implementation candidates. No speedup is yet measured.

[Next](h5-two-center-construction-20261107/next-step.json), assess equivalent selector computation using this
profile. No replacement implementation, successor source state or new search is
prepared. Complete output/score/deadline equivalence must precede any fresh
original-source preparation. Retain the full preparation cost and all eighteen
closed keys. Four earlier arrangements and all 440 allocation candidates remain.

The preceding checkpoints reached main **8dc99684** through an ordinary atomic
push after all six prior checks passed, preserving all 52 protected files.
The [push receipt](h5-two-center-construction-20261107/prior-main-push-receipt.json) and [current main CI snapshot](h5-two-center-construction-20261107/main-ci-at-review.json)
are retained (4 passed jobs, 2 live jobs at review). This checkpoint
awaits the ordinary push gate. Product code, README claims and releases are unchanged.

[Archive verification](h5-two-center-construction-20261107/archive-checks.json), [manifest](h5-two-center-construction-20261107/raw-manifest.json),
[source bindings](h5-two-center-construction-20261107/source-bindings.json), [historical references](h5-two-center-construction-20261107/external-evidence.json)
and [runtime pins](h5-two-center-construction-20261107/runtime-bindings.json) retain the evidence graph.
