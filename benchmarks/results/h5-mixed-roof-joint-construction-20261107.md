# Mixed frame roof: joint cell choices — 2026-11-07

The expanded search closes after **three new physical vectors and 17,001
proposal scores**. Its best candidate, from call 1, remains invalid with
**49 failing original pairs** and **42,163.183280 mm²** total overlap. Every
fixed-part and stock check passes. The third candidate is worse and is preserved.
No native validation, allocation exclusion or H5 credit follows. H2/H5 remain
open at **60% completed milestone weight**.

## Expanded source neighborhood

The geometry, unoptimized initializer, 33 movers, 81 parameters and all fifteen
continuous cog angles come from the preceding independently checked
[continuous construction](h5-mixed-roof-continuous-construction-20261107.md).
This expansion adds joint bracket/insert and bracket/cog cell choices. It retains
both distinct cog regions and each cog's actual current continuous angle.

Every round considers **159 single-owner, 3,888 bracket/insert and 1,620
bracket/cog choices**, totaling 5,667 distinct physical vectors. Only changed
owners move to their nearest point within the new certified cells. Exact pair
corrections replace the old mutual interaction once, avoiding double counting.
The rule orders full scores rounded to 1e-6 mm², then owner/mode.

[Independent preflight](h5-mixed-roof-joint-construction-20261107/neighbor-audit.json) reconstructs every polygon
and sums all 1,056 original-plus-clearance pair terms for **5,668 full scores**.
It uses no cached interaction deltas. Every center, physical key, distinct choice
and rank is checked; maximum score difference is **6.1118044e-10 mm²**.
Complete neighbor preparation takes **0.801021 s**, bringing consumed source
and initializer preparation to **13.055456 s**. The 84.446407-second exhaustive
audit is validation only and does not initialize the search.

The lowest initial joint proposal matches a previously closed vector and is
excluded. All three vectors called by the preceding pipeline stay excluded;
no optimized predecessor coordinates are used. The new calls select changes
bracket 7 (mode 10) and insert 8 (mode 3); then insert 10 (mode 3); then insert 3 (mode 3). The first changes a bracket and insert together; the later two
change one insert each. No bracket/cog joint proposal is selected.

## Closed execution and independent replay

Each new call is limited to thirteen seconds, within preparation-inclusive
60/90-second algorithm/shared limits, and each physical vector is called once.
[Independent response readback](h5-mixed-roof-joint-construction-20261107/response-audit.json) replays all
**17,001 proposals and 379 retained points**, and reconciles the counters for
**448 recorded function evaluations**, including every selection,
closed-vector exclusion, bound, gradient and model. The full-objective oracle
does not reuse the fast delta calculation.

All three candidates reconstruct all 66 originals, 1,380 same-sheet pairs,
264 stock edges, 90 holes and 10,026 hole vertices. The successive candidates
fail 51, 49 and 49 pairs. [The best candidate's original failures](h5-mixed-roof-joint-construction-20261107/source-failures.json)
remain explicit. The last candidate has 42,340.612008 mm² overlap and does not
replace the better second candidate.

The declared three-call limit closes the pipeline. Algorithm/shared totals are
**55.057091/55.132215 s**, including all
preparation. All slice overruns are preserved in the response audit, with no
overall overrun. [All five search processes close](h5-mixed-roof-joint-construction-20261107/closed-process.json),
with peak aggregate committed memory **109,060,096 bytes**. None of the six
calls across the two fixed-roof pipelines may resume, repeat or receive a
reset clock. These heuristic failures do not prove a continuous layout impossible.

## Next geometry and repository

[The next source preflight](h5-mixed-roof-joint-construction-20261107/next-step.json) proposes freeing the two
roof frames while retaining the sixteen base frames and fifteen short-sheet
parts. This would give 35 movers, 85 continuous parameters and 595 moving pairs.
The original frame is a 450×350 mm rectangle with a hole, permits quarter turns,
and forbids mirroring. New frame/source domains, gradients, stock bounds,
inventory mapping and a complete model need independent verification first.
No new geometry or call is prepared; improvement remains unproven.

Four earlier fixed arrangements and 440 whole allocations remain unresolved.
Full66 source/native/material checks, production parity and the unchanged H5
matrix remain required. H2 retains its original gate and reserved vectors.
Production, README and releases are unchanged; no release qualifies.

[The two previous checkpoints reached main 61ae8141](h5-mixed-roof-joint-construction-20261107/prior-main-push-receipt.json)
after all six prior CI jobs and the aggregate run passed, using an ordinary
atomic fast-forward and preserving all 52 remote files. [Fresh main CI](h5-mixed-roof-joint-construction-20261107/main-ci-at-review.json)
is running. This new checkpoint awaits the ordinary push gate.
[Raw evidence](h5-mixed-roof-joint-construction-20261107/raw-manifest.json), [source bindings](h5-mixed-roof-joint-construction-20261107/source-bindings.json)
and [six pinned runtime files](h5-mixed-roof-joint-construction-20261107/runtime-bindings.json) preserve the complete
evidence chain without bundling installed vendor runtimes.
