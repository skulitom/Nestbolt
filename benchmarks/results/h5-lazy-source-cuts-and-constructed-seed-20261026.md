# H5: source-cut attempts and a constructive necessary-model witness — 2026-10-26

**A direct construction satisfies every constraint in the simpler model, but the
complete source layout still has 38 colliding pairs.** Its valid 54-original
portion includes every frame, bracket and insert plus the three short-sheet
cogs. Both distinct source-cut searches close UNKNOWN in their first round.
H2/H5 remain open at 60% by completed gate weights.

## Two closed attempts

The first pipeline starts with all 114 whole-stock coordinates, 65 source-contained
rectangles, NoOverlap2D, both cumulative strip constraints and 47 equivalent-copy
orders: 180 serialized constraints, no hints or objective. All 57 first-sheet
originals remain mandatory, alongside the fixed verified short nine. Its declared
algorithm allows at most six rounds within 60 search/90 shared seconds, with a
15-second first solve and eight-second later caps. Any later round must add every
newly failing source pair; UNKNOWN stops the pipeline immediately.

Only round zero runs. It returns UNKNOWN after 390,943 branches and 26,682 conflicts.
Solver time is 15.013275 seconds, returned solve 15.014221, algorithm 16.570634 and
shared process 16.716055. No assignment, source candidate or new pair cut exists.
The small soft overruns are recorded. The run is closed without retry or extension.

## What the direct construction proves

Without a solver call, the construction places 12 turned and six wide frames,
eight first-sheet brackets and 19 inserts. Each bracket receives one insert in
its exterior concave notch; this is not nesting inside a hole. The remaining
inserts occupy strips beside and above the frame/bracket rows. Twelve cog inner
squares occupy six columns by two rows within the full-source stock domains.
Equivalent copies are assigned in nondecreasing Y order.

An independent serialized-model reader verifies all 114 coordinates, every one
of the 180 constraints, 2,080 rectangle pairs, 111 cumulative events and all
47 copy orders. Thus the closed search's UNKNOWN result is not a proof that
these necessary conditions are impossible.

An independent original-ring reader checks all 66 originals, 90 cutouts and
10,026 hole vertices, all 1,632 same-sheet pairs and 264 stock edges. It finds
38 pair failures and zero stock failures. Removing only the 12 first-sheet cogs
from the partial-layout view leaves **54 source-valid originals**, checked through
1,026 pairs and 216 stock edges, with 78 cutouts/7,626 hole vertices. Minimum gap
is 0.224308672487 mm and minimum extra stock clearance is 0.012600000000 mm.
All 12 excluded cogs remain present in the complete failed candidate and
mandatory in further work. This does not improve the older preserved 64-part
partial count and is not a full job fit.

Original 31 moves vertically by 1,531.493812 mm relative to the earlier mixed
candidate, escaping its independently proved 180 mm obstruction. The construction
therefore supplies a different configuration while showing why the single
153 mm inner square is an inadequate representation of each complete cog.

## Source-informed initialization

The second pipeline starts with all **38 actual failing-pair disjunctions** and
90 coordinate hints for the 45 first-sheet non-cogs. No first-sheet position is
fixed; the 12 first-sheet cogs have full domains and no hints. The new model has
3,880 variables, 13,246 constraints and 13,028 integer halfplanes. Its independent
reader checks all constraints and every hint. It shares the same declared bounded
round policy, but is a different model from the closed empty-cut attempt.

Again only round zero runs: UNKNOWN, 20,144 branches and 6,155 conflicts. Solver
time is 15.043030 seconds, returned solve 15.056194, algorithm 18.150153 and shared
process 18.386994. The 38 initial cuts remain; **zero new cuts** and zero source
candidates are generated. Soft overruns are preserved. No later round, unchanged
retry, exclusion claim, native call or full quality run occurs.

Four independent audits pass. The next distinct hypothesis is to replace each
single cog square with several disjoint rectangles contained in its actual
source outline, independently checking their coverage and disjointness. This
changes the necessary geometry model. It does not reopen either closed search
or qualify a source/native/material witness.

## Repository and evidence

At 2026-10-26T20:04:46.739487+00:00, [main checks](https://github.com/skulitom/Nestbolt/actions/runs/40386947038):
5 of six checks pass. The remaining main checks are still running; no checkpoint push is attempted. The preceding f010d74c checkpoint remains queued locally. Production,
READMEs and upstream heads/releases are unchanged. The 22 reserved H2 vectors
remain unopened, and no new release is qualified.

[Checks](h5-lazy-source-cuts-and-constructed-seed-20261026/checks.json), [unseeded response](h5-lazy-source-cuts-and-constructed-seed-20261026/unseeded-response-checks.json),
[construction model](h5-lazy-source-cuts-and-constructed-seed-20261026/constructed-model-checks.json),
[construction source](h5-lazy-source-cuts-and-constructed-seed-20261026/constructed-source-checks.json),
[seeded response](h5-lazy-source-cuts-and-constructed-seed-20261026/seeded-response-checks.json), [scope](h5-lazy-source-cuts-and-constructed-seed-20261026/scope.json),
[next step](h5-lazy-source-cuts-and-constructed-seed-20261026/next-step.json) and [raw manifest](h5-lazy-source-cuts-and-constructed-seed-20261026/raw-manifest.json).
The archive verifies 73 canonical files and
50 identical-content aliases by bytes, SHA-256 and CRC.
