# Movable roof-frame construction — 2026-11-07

The broader model frees the two roof-frame originals, but its complete bounded
search still produces no valid layout. Three distinct calls close with a best
candidate containing **52 failing original pairs** and **32,645.952364 mm²**
overlap. Every fixed-part and stock check passes. No native call or allocation
exclusion follows. H2/H5 remain open at **60% completed milestone weight**.

## Original geometry and expanded movement

Only sixteen base frames and fifteen short-sheet originals remain fixed.
The two roof frames join six brackets, twelve inserts and fifteen cogs: **35
moving originals, 85 continuous parameters and all 595 moving pairs**. Each
frame keeps its original 450×350 mm outer rectangle and hole. Its allowed
rotations are 0°, 90°, 180° and 270°, with no mirroring. Filled outer geometry
continues to enforce common-line mode's prohibition on part-in-hole placement.

[Independent source-domain checks](h5-movable-roof-construction-20261107/source-domain-audit.json) verify
the twelve bracket/insert arrangements, four frame orientations and all-angle
cog envelope against one outward-rounded box containing the sixteen base frames.
All **44 atomic cells, 27 exact support proofs, 125 owner bindings and 620
original-source corner controls** pass. Minimum certified axis gap is
0.230001 mm. Domains conservatively restrict source free space; they do not
claim complete coverage of every legal placement.

[Frame clearance checks](h5-movable-roof-construction-20261107/frame-clearance-controls.json) independently
verify the exact expanded rectangle and all sixteen edge supports, certifying
at least 0.114 mm local offset. The inherited bracket/insert/cog source contours
and evidence remain unchanged. Source projections of the two frames and fifteen
cogs are at most **2.828427 nanometres**. Their 48-part control stays valid but
still lacks the eighteen companions. Complete source preparation is 4.494252 s.

## Fresh complete initializer and model

One new initializer starts from the seventeen unoptimized source poses, then
greedily places the six brackets and twelve inserts on all legal compound
9×9 grids. It consumes no optimized ancestor and no previous companion
initializer. Canonical alias-bound cuts require at most another 1.414214 nm
seed projection; the resulting original 48-part control independently passes.

[Full model readback](h5-movable-roof-construction-20261107/model-audit.json) replays **8,262 candidate trials,
125 owner/mode full scores and 91 mode vectors**. There are 97 physical owner
options and 62 distinct single-owner neighbors after outline/domain equivalence.
All [114 equivalence comparisons](h5-movable-roof-construction-20261107/physical-mode-controls.json) preserve
different frame orientations and different effective domains. The new compiler
derives angle coordinates from owner identities and parameter counts; the
independent verifier checks every frame and cog binding.

Controls include 148 scalar boundary-gradient comparisons, **340 central
samples over 170 coordinates**, three descent steps and eleven deliberately
corrupted models. [Both derivative step sizes pass](h5-movable-roof-construction-20261107/derivative-controls.json).
The complete initializer starts with 37 failing pairs and 100,406.579957 mm²
original overlap; it is not a valid full66 layout. Complete consumed source
and initializer preparation, including both wrapper processes, is **7.951382 s**.

## Closed bounded search and independent replay

The finite pipeline permits at most three distinct physical vectors, with
16/14/14-second slices and preparation-inclusive 60/90-second algorithm/shared
limits. All centers remain free inside certified hard domains, and all fifteen
cog angles remain continuous. The two later mode choices affect inserts;
frame quarter-turn alternatives are considered but not selected.

[Independent response replay](h5-movable-roof-construction-20261107/response-audit.json) verifies **123 mode
trials and 380 retained points**, and reconciles the counters for **469 recorded
function evaluations**. Every candidate reconstructs all 66 original parts,
1,380 same-sheet pairs, 264 stock edges, 90 holes and 10,026 hole vertices.
The successive candidates fail 60, 61 and 52 pairs; the third is best by the
declared objective. [Its source failures](h5-movable-roof-construction-20261107/source-failures.json) comprise
50 positive intersections and two clearance failures, all between moving parts.

The declared call limit closes the pipeline. Algorithm/shared totals are
**54.899362/54.970363 s**. Slice overruns of 0.019038, 0.027600 and 0.086949 s
are retained within the overall limits. [All five search processes close](h5-movable-roof-construction-20261107/closed-process.json),
with peak aggregate committed memory 94,683,136 bytes. These calls cannot resume,
repeat or receive a reset clock; local failure proves no allocation impossible.

## Observed frame limits and next source scope

[A separate read-only diagnostic](h5-movable-roof-construction-20261107/frame-constraint-diagnostic.json)
reconstructs frame motion and active bounds at all three saved candidates.
In the best one, the frames move **0 and 0.004160 mm**, retain their original
orientation, and both sit at the lower y bound imposed by the fixed base.
Their local negative objective-gradient directions point below that bound.
Five failing pairs involve these frames, totaling **5,177.537220 mm²** overlap.
[The complete observations](h5-movable-roof-construction-20261107/frame-constraint-records.json) describe these
specific candidates; they are not a global stationarity or infeasibility proof.

[The next preflight](h5-movable-roof-construction-20261107/next-step.json) assesses freeing the upper four
base frames as well, making original frame copies12–17 movable. With twelve base
frames and fifteen short-sheet parts fixed, the proposed model would have
39 movers, 93 parameters and 741 moving pairs. The smaller fixed core requires
new source-safe domains, a fresh source-only initializer, complete accounting
and independent model/gradient verification. No successor geometry or call is
prepared. Every earlier closed pipeline remains closed.

Four earlier fixed arrangements and 440 whole allocations remain unresolved.
Full66 source/native/material checks, production parity and the unchanged H5
matrix remain required. H2 retains its original gate and reserved vectors.
[Main CI at review](h5-movable-roof-construction-20261107/main-ci-at-review.json) has five passed jobs and a live
Windows native job on main61ae8141. Checkpoint4b666d51 and this checkpoint await
the ordinary push gate. Production, README and releases are unchanged; no
release qualifies. [Raw evidence](h5-movable-roof-construction-20261107/raw-manifest.json) and
[source bindings](h5-movable-roof-construction-20261107/source-bindings.json) retain exact historical references;
six installed runtime files are [separately pinned](h5-movable-roof-construction-20261107/runtime-bindings.json).
