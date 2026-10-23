# H5: fixed-part cog limit and coordinated relocation — 2026-10-23

**The best retained layout remains 64 of 66 parts, missing two cogs.** A new
cog-only model proves an optimum of 13 cogs within its finite pool when all
51 non-cogs stay fixed. This is not a continuous impossibility result. A separate
audit identifies a checked complete-cog subassembly for coordinated small-part
relocation. H2/H5 remain open at **60%**.

## New cog-only pool

The [improved 64-part layout](h5-dense-wide-progress-20261023.md) supplies the exact
18 frame, 12 bracket and 21 insert poses. Its necessary continuous cog bound of
19 is inconclusive for 15. The changed construction preserves the whole prior
pool and maps every seed placement exactly, appending only the newly added fixed
insert. All 1,346 compatible old cog poses remain, including applicable denser
groups and the complete 13-cog seed.

Sixteen conservative translation-region queries use the exact current cog angles
plus four sampled phases on both target sheets. All queries complete. Round-robin
proposal processing adds 1,500 cog poses in 8.351362300 seconds. The fresh pose cap
leaves eight recorded lists pending; they are not resumed. The candidate total is
2,846. The eight last-sheet construction regions are empty under the positive
padding; original valid last-sheet seed positions remain available.

Independent checks cover 242,894 old/fixed pairs, 61,360 proposal/fixed pairs,
every actual proposal, its origin and original stock bounds. No proposal is
geometrically rejected. Among 3,944,502 same-sheet candidate pairs, 1,432,196 exact
distances establish 1,169,914 conflicts. All are covered by 3,621 verified cliques,
with no residual edge or compression expiry. The full seed is preserved.

## Finite optimum and original validation

Every protobuf model field is independently reconstructed before one eight-worker,
seed-zero call with a 30-second limit. It finishes in 3.845595200 seconds with
`OPTIMAL`: the objective and bound both equal 13 cogs. The current fixed-part pool
therefore cannot supply the two missing cogs. No additional solver call is made.

The starting hint, one callback and a different final layout all pass original
geometry checks. The hint exactly matches the retained 64-part layout, so its
frozen-CLI result is reused with verified source bytes. Two fresh frozen-CLI calls
for the different outputs fail only for two missing cogs. Their 4,381,615.346194 mm²
filled area and 4,988,890.203495 mm² charged material do not improve. Minimum
clearance remains about 0.2011 mm; native construction margins are unqualified.
The finite phase/pose cap and conservative regions do not justify a claim about
all continuous positions or rotations.

## Which existing parts block complete cog groups?

A separately declared 165-case census considers every saved first-sheet group
of 15 cogs, each possible one-cog omission paired with the original last-sheet
cog, and every saved 14-cog group paired with that last cog. All cases contain
exactly 15 original cogs and retain the 18 frame poses.

The independent reconstruction checks all 15,155 cog pairs, 41,760 cog/frame
pairs and 52,745 cog/small-part pairs. Every case completes within the declared
30-second allowance. At least eight of the current small-part poses must move
for each of these particular cog arrangements. This is a conditional statement
about the 165 cases, not a global lower bound on moves.

Ranking by removed filled area, count and case index selects case 20: group 96,
member 3 omitted, plus the original last-sheet cog. It leaves three brackets and
five inserts to relocate, total 219,000 mm². The exact checked subassembly contains
18 frames, 15 cogs, nine brackets and 16 inserts: 58 parts. All 1,101 pairs and
original stock bounds pass; a fresh frozen-CLI result reports precisely the three
missing brackets and five missing inserts. Its 4,262,740.784070 mm² filled area is
below the retained 64-part result. It is a construction hypothesis, not a new best
layout or a qualified production repair.

Do not repeat this fixed-non-cog model or resume the eight capped lists. The existing 64-part layout remains the best retained partial. For a changed coordinated construction, use output/h5-dense-group-blockers-20261023/best-subassembly.json: case 20, saved group 96 with member 3 omitted plus the original last-sheet cog. All 18 frames and all 15 cogs coexist with nine brackets and 16 inserts. Exactly three original brackets and five inserts remain to place. First check the original remaining-area/stock constraints, then declare a finite completion of those two families against the exact 58 retained poses. Reuse only compatible old poses, generate new actual-outline contacts for every allowed bracket orientation/reflection and both insert size classes, independently check the complete conflict model, and keep all attempts and limits. The 165-case blocker minimum is conditional on those arrangements, not a global move bound. This construction is not yet a production repair mechanism; the unchanged repair limits, native margins, original 66-copy validity, production budget and complete H5 gates remain requirements before integration. H2 retains Artem’s unchanged gate.

## Repository and release status

The preceding checkpoints were pushed normally to main as `2333dd2c` after all
six checks on `37edb1d2` passed. The saved main `2333dd2c` snapshot is in_progress, with 4 successful checks; no complete pass is inferred. Core source and all three README hashes
are unchanged. The existing preview remains accurately described; no new build
qualifies for release. No native packing, quality matrix or reserved-input
evaluation occurs. Original gates, release authorization and H2's reviewed
denominator decision remain unchanged.

Evidence: [generation](h5-dense-cog-limit-20261023/generation.json), [graph audit](h5-dense-cog-limit-20261023/graph-audit.json),
[model audit](h5-dense-cog-limit-20261023/model-audit.json), [solver result](h5-dense-cog-limit-20261023/solver-result.json),
[layout audit](h5-dense-cog-limit-20261023/layout-audit.json), [blocker census](h5-dense-cog-limit-20261023/blocker-census.json),
[independent reconstruction](h5-dense-cog-limit-20261023/blocker-audit.json), [exact subassembly](h5-dense-cog-limit-20261023/subassembly.json),
[original CLI failure](h5-dense-cog-limit-20261023/subassembly-public.json), [source review](h5-dense-cog-limit-20261023/source-review.json),
[raw evidence](h5-dense-cog-limit-20261023/raw.zip), and [manifest](h5-dense-cog-limit-20261023/raw-manifest.json).
All 102 archive members, CRCs and byte hashes verify.
