# Mixed-row continuous construction — 2026-11-07

The historical mixed-row frame layout now has independently checked continuous
source domains and a complete original-geometry model. Its bounded search still
fails: the best candidate has **52 failing original pairs** and
**38,972.237088 mm² overlap**. Fixed-part and stock checks all pass. No native
call or allocation exclusion follows. H2/H5 remain open at **60%** completed
milestone weight.

## Historical recipe and new source control

The [October 26 construction](h5-mixed-rows-source-contacts-20261026.md) already
used twelve quarter-turned frames in four columns/three rows, followed by six
unturned frames in three columns/two rows. Its finite 4,200-pose source-contact
model returned UNKNOWN and stays closed. This checkpoint claims no new frame
topology. The current 0.23 mm spacing makes its top 2,057.445 mm, 0.020 mm higher
than the historical 0.225 mm recipe. All fifteen short-sheet originals remain.

[Independent recipe readback](h5-mixed-rows-continuous-construction-20261107/source-recipe-audit.json) checks every
frame rectangle, 153 nominal frame-pair separations and the fixed 33 originals.
One source-only grid holds exactly fifteen cogs in five columns/three rows,
at the previously certified 6.75-degree phase and 261.766 mm contact pitches.
All 105 cog pairs and 270 cog/frame pairs pass; minimum gaps are 0.301548 and
0.268863 mm. The original 48-part control passes 633 pairs, 192 stock edges,
60 holes and 6,366 hole vertices. Six brackets and twelve inserts are still
missing. Complete source recipe preparation costs 4.160113 s.

## Hard domains and complete original model

The twelve-frame base and six-frame roof have separate outward-rounded
containing rectangles. [Exact source-domain checks](h5-mixed-rows-continuous-construction-20261107/source-domain-audit.json)
verify 13 arrangements, 112 atomic cells, 54 whole-cell support proofs,
147 owner bindings and 708 source corner controls. The minimum certified axis
gap is 0.230001 mm. These are conservative safe domains, not complete coverage
of all legal source free space. Ten bracket cells, six insert cells and one
all-angle cog cell remain explicit. The fifteen source cog projections are at
most 1.414214 nm; the original 48-part control remains valid.

The complete model has **33 movers, 81 parameters and 528 moving pairs**.
All fifteen cog centers and angles remain free. One fresh initializer places
the source cogs first, then the eighteen companions on every declared 9×9 grid.
It consumes no optimized ancestor or historical finite contact pool.
[Independent model readback](h5-mixed-rows-continuous-construction-20261107/model-audit.json) replays all **10,692 trial
scores, 147 owner/mode full scores and 115 vectors**. Canonical alias bounds
require no additional seed projection. There are 111 physical owner options
and 78 distinct single-owner neighbors; [137 equivalence controls](h5-mixed-rows-continuous-construction-20261107/physical-mode-controls.json)
preserve both distinct vertical-insert regions.

Controls also verify 132 scalar gradient terms, **324 central samples over
162 coordinates**, three descent directions and eleven deliberately corrupted
models. [Both derivative step sizes pass](h5-mixed-rows-continuous-construction-20261107/derivative-controls.json).
The initializer starts with 33 failing pairs and 74,476.597369 mm² overlap;
it is not valid. Complete consumed source/domain/initializer preparation is
**9.012576 s**. Verification work is recorded separately.

## Closed search and independently replayed failures

Three distinct physical vectors use declared 16/14/14-second slices within
preparation-inclusive 60/90-second limits. All later selected mode changes
affect inserts. [Response replay](h5-mixed-rows-continuous-construction-20261107/response-audit.json) verifies **155
mode trials and 390 retained points**, reconciling 478 function-evaluation
counters. Each candidate reconstructs all 66 originals, 1,380 same-sheet pairs,
264 stock edges, 90 holes and 10,026 hole vertices. The candidates fail 48, 49
and 52 pairs; the third has the best declared objective. Fewer failing pairs
and lower total overlap are different measures and do not establish validity.

The best [source failures](h5-mixed-rows-continuous-construction-20261107/source-failures.json) comprise 49 positive
intersections and three clearance-only failures. Algorithm/shared totals are
**56.181211/56.284123 s**; the source-check time stop closes the pipeline after
the third call. Slice overruns of 0.091584, 0.044335 and 0.011268 s remain
preserved. [All five search processes close](h5-mixed-rows-continuous-construction-20261107/closed-process.json),
with 94,543,872 bytes peak aggregate committed memory. No call can resume.

[Read-only diagnostics](h5-mixed-rows-continuous-construction-20261107/failure-diagnostic.json) attribute the best
candidate's overlap to bracket/insert (11,332.616199 mm²), bracket/cog
(7,014.549071), insert/insert (1,537.978812), cog/insert (14,102.662083) and
cog/cog (4,984.430922). Cogs move at most 42.846175 mm and rotate at most
7.200218 degrees from their source poses. Five have active lower y bounds
with negative local descent blocked. [The complete observations](h5-mixed-rows-continuous-construction-20261107/failure-diagnostic-records.json)
describe these candidates only and prove no global exclusion.

## Next model preflight and repository state

[The next preflight](h5-mixed-rows-continuous-construction-20261107/next-step.json) assesses bounded positive pair
weights on the exact original/clearance objective while retaining all hard
fixed-part and stock bounds. Guided weights are already used in Nestbolt and
in an [earlier H5 construction](h5-retained64-allocation-source-search-20261026.md);
that different finite-angle, soft-stock model also failed and remains closed.
The [weight-ceiling history](separator-weight-cap-20261014.md) is retained.
A weighted original-geometry model needs independent coefficient, gradient,
state-transition and zero-overlap-equivalence checks before any finite search.
Only the unoptimized source initializer may be consumed, with complete charge;
no closed uniform-weight call may be rerun. No new weighted model exists yet.

Four earlier fixed arrangements and 440 allocations remain unresolved. Full66
source/native/material validity, production parity and the unchanged H5 matrix
remain required. H2 retains its original gate and reserved vectors.
[Main CI at review](h5-mixed-rows-continuous-construction-20261107/main-ci-at-review.json) has five passing jobs and
Windows native CI still running on bca9af73. Checkpoint 15f55b9a and this
checkpoint await the ordinary push gate. Production, README and releases are
unchanged. [Raw evidence](h5-mixed-rows-continuous-construction-20261107/raw-manifest.json),
[source bindings](h5-mixed-rows-continuous-construction-20261107/source-bindings.json) and
[pinned runtime files](h5-mixed-rows-continuous-construction-20261107/runtime-bindings.json) retain all inputs and outcomes.
