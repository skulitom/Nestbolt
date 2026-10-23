# H5: completing the selected cog group — 2026-10-23

**The best retained layout remains 64/66 parts.** Two new constructions around
the selected complete-cog arrangement reach 61/66, missing three brackets and
two inserts. Their smaller filled area does not improve the retained result.
The second model's upper bound excludes the full inventory in its finite pool,
but neither experiment proves continuous geometric impossibility. H2/H5 remain
open at **60%**.

## Eight missing parts around the checked 58-part subassembly

The [previous census](h5-dense-cog-limit-20261023.md) selected case 20, group 96
with member 3 omitted and the original last-sheet cog added. Exactly 18 frames,
15 cogs, nine brackets and 16 inserts stay fixed. Original stock and filled-area
arithmetic leave 644,250.519695 mm² free for the missing 219,000 mm². This necessary
area check passes; it does not establish that the gaps can hold those shapes.

Twenty newly declared translation-region queries cover all eight allowed bracket
orientations/reflections and both equivalent insert size classes on both sheets.
All finish within the 120-second generation allowance. All 16 bracket construction
regions are empty. The two first-sheet insert queries supply 56 new poses; all
last-sheet construction regions are empty. These are conservative, positively
padded regions, so their emptiness alone is not a continuous impossibility proof.
All 43 compatible prior poses are inserts, giving 99 total candidates. All 57
proposal events, including one duplicate, are preserved; nothing remains pending.

Independent checks cover 437,704 prior/fixed pairs, 2,622 proposal/fixed pairs,
the exact fixed subassembly and original stock. All 4,851 candidate pairs are
accounted for; 2,814 exact distances establish 2,814 conflicts, covered by 27
verified cliques. There are no rejected geometric proposals, residual edges or
compression expiry. Area arithmetic and the complete protobuf model are checked
independently. The empty bracket-family constraint is recorded as identically true.

One 30-second-limit, eight-worker, seed-zero solve finishes in 0.010675100 seconds
with a finite-pool optimum of three additional inserts. The hint and returned
layout receive fresh frozen-CLI calls; each fails only for the corresponding
missing quantities. The returned 61-part layout contains nine brackets, 19 inserts,
all 18 frames and all 15 cogs. Its 4,322,140.784070 mm² filled area is below the
saved 64-part layout's 4,381,615.346194 mm². Charged material remains
4,988,890.203495 mm², under the original target. No native margin is qualified.

## Move every bracket and insert together

A separately declared construction fixes only the 33 frame/cog poses, allowing
all 12 brackets and 21 inserts to move. It retains the complete nine-bracket,
19-insert seed and returns to the full prior source pool before small-part
filtering. Thus candidates previously blocked by the fixed small parts are
available again; no previous failed solve is retried.

All 20 new queries finish. The pool contains 1,694 compatible prior poses plus
180 new bracket and 171 new insert poses: 2,045 choices. All 496 proposal events
are retained, including 145 duplicates. Generation takes 9.742350500 seconds;
neither candidate cap nor time cap is reached, and no proposal is pending.

The independent audit checks 295,381 prior/fixed and 11,842 proposal/fixed pairs.
Among 1,149,136 same-sheet candidate pairs, 381,104 exact distances establish
342,611 conflicts. All are covered by 2,100 verified cliques without residual
edges or compression expiry. The original 28-small-part seed and every stock
bound are verified. All protobuf fields and the weighted filled-area objective
are reconstructed before solving.

One 30-second-limit call takes 30.040612200 seconds; the soft overrun is retained.
It returns `FEASIBLE` with the same 61 parts. Score 736,200,000 and upper bound
763,200,000 remain apart, so an optimum is not claimed. The full-inventory score
is 895,800,000: the returned bound excludes a complete packing within this
particular finite pool. It makes no claim about ungenerated poses or other
cog arrangements. No limit extension or second call is made.

The exact starting layout reuses its byte-verified frozen-CLI result. The callback
and different final layout each receive a fresh original CLI check. All three
layouts pass original filled-outer geometry, 1,242 same-sheet pairs each, and
retain precisely the three-bracket/two-insert quantity shortfall. The final uses
four newly generated poses but does not improve filled area. Minimum clearance
is about 0.2011 mm; native margins remain unqualified.

## Next action and repository state

Do not repeat either solve, extend its time limit, or treat this 61-part result as an improvement over the saved 64-part partial. The chosen cog arrangement came from minimum disruption of the old small parts; that ranking does not establish best packability after all small parts move. Next declare a finite comparison across the other saved complete-cog cases from output/h5-dense-group-blockers-20261023/cases.json. Retain the same 18 frames, reconstruct every 15-cog case from its source group/drop/last-cog specification, and independently validate any new compatibility graph against original geometry. Reuse the full bracket/insert source pool before fixed-cog filtering, including current new contacts; add group-conditioned contacts only under newly declared caps. Compare compatible small-part placements and use any checked stronger arrangement as a seed for one newly declared group-selection model. Keep each original case, excluded pose, failed result, bound and pending suffix. This changes the cog arrangement and the discrete group decision; it is not a retry of the expired single-group or free-all-small models. Any 66-part witness still needs native margins, unchanged production repair limits/budget, and the complete H5 scope. H2 retains Artem's original gate decision.

The saved main `2333dd2c` snapshot is in_progress, with 5 successful checks; a complete pass is not inferred. The preceding `db703a0c` checkpoint is local and waiting for that run
to finish before the next normal push, avoiding cancellation of live checks.
Production source and all three README hashes remain unchanged. The published
preview is still accurate; diagnostic evidence alone does not qualify a new
application build. No production packing, quality matrix, new native LightBurn
check or reserved-input evaluation occurs. Original acceptance and repair limits
remain unchanged.

Evidence: [first plan](h5-complete-cog-small-relocation-20261023/eight-plan.json), [first generation](h5-complete-cog-small-relocation-20261023/eight-generation.json),
[first graph audit](h5-complete-cog-small-relocation-20261023/eight-graph.json), [first model](h5-complete-cog-small-relocation-20261023/eight-model.json),
[first result](h5-complete-cog-small-relocation-20261023/eight-solver.json), [first original layouts](h5-complete-cog-small-relocation-20261023/eight-layouts.json),
[joint plan](h5-complete-cog-small-relocation-20261023/joint-plan.json), [joint generation](h5-complete-cog-small-relocation-20261023/joint-generation.json),
[joint graph audit](h5-complete-cog-small-relocation-20261023/joint-graph.json), [joint model](h5-complete-cog-small-relocation-20261023/joint-model.json),
[joint result](h5-complete-cog-small-relocation-20261023/joint-solver.json), [joint original layouts](h5-complete-cog-small-relocation-20261023/joint-layouts.json),
[source review](h5-complete-cog-small-relocation-20261023/source-review.json), [raw evidence](h5-complete-cog-small-relocation-20261023/raw.zip), and
[manifest](h5-complete-cog-small-relocation-20261023/raw-manifest.json). All 157 archive members, CRCs and
byte hashes verify.
