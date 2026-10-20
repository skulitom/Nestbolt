# H5: which single non-cog part could move? — 2026-10-20

**Moving one bracket or insert alone cannot complete this arrangement.**
All twelve bracket choices and all twenty-one insert choices are ruled out by
independently checked bounds allowing arbitrary cog angles and continuous
positions. Moving one of the eighteen frames remains inconclusive. This does
not prove a frame move can work or exclude changes to multiple non-cog parts.
H2/H5 remain open at 60%.

## A necessary relaxation for each part

The [preceding certificate](h5-cog-free-regions-and-continuous-capacity-20261020.md)
allows at most thirteen cogs with all 51 non-cog poses fixed. This census
removes each non-cog obstacle in turn while keeping the other fifty in place.
Omitting the removed part makes the problem more generous than relocating it:
if even that space cannot hold fifteen cogs, moving only that part cannot
solve the original job.

The census declares 51 cases in candidate-index order and a 90-second limit,
stopping only between cases. All 51 finish in **24.103865400 seconds**, with
no pending cases or limit extension. It makes no solver, native packing or
quality call and produces no new layout.

For each case, the conservative inscribed-disk center regions are recomputed
from the remaining original-geometry interior rectangles. Each region component
gets a reachable-area bound, a bounding-box diameter cover, and two finite band
covers. Whole-sheet area bounds remain available where tighter.

A separate audit verifies every obstacle removal, exact center-region
complement and reachable-area total, all **121 components** and **242 band
covers**. All original seed center regions remain included. Its independent
integer event sweep agrees with every area; the audit takes **7.276938200 seconds**.

## Tighten the one remaining insert case

The initial component bounds exclude 32 changes: all twelve brackets and
twenty inserts. Insert candidate **8529** initially remains inconclusive at
fifteen. Removing it creates two separate, small possible-center regions on
the first sheet; counting their capacities independently permits one cog in
each. Their centers cannot actually coexist: every corner pair of their
bounding boxes lies strictly closer than the necessary **218.4313 mm**
center separation.

A saved component-clique certificate covers those two regions together with
capacity one. Separate corner-pair checks verify this certificate and every
component partition across all 51 cases. Candidate 8529's bound drops from
15 to **14**, excluding it too. The original looser result is retained.

| Removed part family | Cases | Single change ruled out | Still inconclusive |
| --- | ---: | ---: | ---: |
| Frame | 18 | 0 | 18 |
| Bracket | 12 | 12 | 0 |
| Insert | 21 | 21 | 0 |

The eighteen frame releases have necessary upper bounds of **15–17 cogs**.
These are capacity bounds, not achievable counts or replacement frame
positions. Any candidate must restore the released frame, retain the other
parts and place all fifteen cogs before original validation can succeed.

## Source, checks and release

All six hosted checks on remote main **abeb2739** now pass, including Windows,
Linux, browsers, benchmark smoke and both maker rebuilds. This confirms that
exact remote checkpoint; it does not stand in for checks on the subsequent
local evidence commits.

Core source and all three README hashes remain unchanged. The README still
accurately describes v0.2.0-alpha.1, stable v0.1.0 and the open v1.1 work.
No release is qualified by these conditional bounds. No reserved held-out
file is evaluated, no acceptance rule changes and no additional CLI layout
validation is called because no new layout is produced.

## Next work

Do not test single bracket or insert changes around this arrangement: the all-angle relaxation excludes all33. The18 frame releases remain inconclusive, with upper bounds15–17 and no returned placement. Next examine original-outline free translation regions for a moved frame at its allowed quarter-turn rotations while keeping the other50 non-cog poses fixed. Preserve the original frame pose and explicitly audit any new contact choices before considering a changed joint frame/cog construction. A released frame must be restored and all15 cogs placed; deleting a part never qualifies the original job. Multiple non-cog moves remain possible. Do not reuse a conflict graph conditional on the former fixed group.

[Checks](h5-single-non-cog-release-census-20261020/checks.json), [original census](h5-single-non-cog-release-census-20261020/census-result.json),
[independent audit](h5-single-non-cog-release-census-20261020/census-audit.json),
[refined component certificates](h5-single-non-cog-release-census-20261020/component-cover-audit.json),
[successful remote checks](h5-single-non-cog-release-census-20261020/main-ci-abeb2739-success.json),
[source review](h5-single-non-cog-release-census-20261020/source-review.json), [all case certificates](h5-single-non-cog-release-census-20261020/raw.zip)
and [manifest](h5-single-non-cog-release-census-20261020/raw-manifest.json).
All 131 archive members, CRCs and byte hashes verify.
