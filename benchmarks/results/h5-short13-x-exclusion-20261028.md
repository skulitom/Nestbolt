# Source projection excludes the short-sheet 7/5/1 allocation — 2026-10-28

**Seven brackets, five inserts and one cog cannot fit the target short sheet.**
The new necessary model returns INFEASIBLE, and its geometry, complete serialized
model, solver response and source-to-model mapping pass independent audits.
Deleting extra parts preserves feasibility, so seven brackets, six inserts and
one cog is excluded too. The complete count frontier shrinks from **454 to 452**
remaining candidates. This does not exclude the full 66-part job or establish
that any surviving allocation is feasible.

## Exact horizontal spacing

Project the audited inner-octagon, actual-vertex edge and closed-corner regions
over every integer cog-minus-anchor Y in the complete outward stock domains.
Thirty-four interval-chain certificates cover all **983,930 integer Y values**.
The independent reader checks 13,825,864 integer facet inequalities and 780
outside-endpoint region checks. Every cog angle remains covered by the original
source theorems; no angle sampling is used to establish completeness.

Eight bracket–cog directions become stricter, by up to **23.375 mm**. Combining
them with the previous source-support directions preserves the stronger bound
on each side. All 6,985 mixed spacing checks across 635 valid source12 prefixes
pass. Recomputing the complete ordered core frontier advances 79 earliest
positions but, on its own, excludes no additional count allocation.

The next projection includes all five mandatory inserts. Its 11 profile types
and 121 directed pair distances pass an independent reader, including 49
complete-domain rectangle overlap cases. All 41,910 pair checks and 1,270
insert-triple checks across the valid prefixes pass. Three source-inner insert
heights exceed the relaxed sheet height by 17.021 mm, providing a further
necessary capacity condition.

## Complete source X-capacity model

The reduced model keeps all 13 original reference-X coordinates, every allowed
bracket/insert mode and all real cog angles. A free ordering literal for each
pair selects its audited directional spacing. Optional source-contained X
intervals consume their full Y heights against the relaxed 312.967 mm stock
height. These comprise the disjoint bracket rectangles, insert rectangles and
16 disjoint cog strips. Full stems used only in spacing proofs are never added
again to cumulative demand.

All **158 variables and 4,372 constraints** are independently verified, including
194 optional source rectangles, 78 original pairs and 2,010 selected-mode pairs.
Same-family X order only relabels identical copies. No Y position or cog angle
is fixed, and there are no objectives, hints or assumptions. Every valid
original-source placement would map to this relaxed model.

The sole call, using four workers with `fj` excluded, returns **INFEASIBLE** after
68,907 branches and 25,215 conflicts. Solver wall time is 2.036771 seconds;
returned solve time **2.037863 seconds**; shared process time 2.713545 seconds.
There is no overrun, retry or extension. The response reader confirms the exact
model bytes, parameters, counters and terminal status. As positive controls,
all 635 source-valid12 prefixes pass independent cumulative sweeps of 26,035
rectangles, with at least 2.979 mm spare height.

An initial preparation failed because the installed OR-Tools list overload of
`only_enforce_if` returned no fluent constraint object. Its scripts, diagnostic
and premature missing-model audit failure are retained. The fix stores the
constraint before applying enforcement; no solver call had opened. The repaired
model subsequently passed the full audit before its single call.

## Scope and next construction

Among all 4,576 original count allocations, only `[7,5,1]` and `[7,6,1]` are newly
excluded. The 452 survivors and all original complementary first-sheet counts
are preserved. The known valid `[7,4,1]` prefix and `[8,5,0]` short construction
remain allowed. There is no full66 exclusion, source66 witness or native pass.

Return to the best source64 layout and consider freeing its whole first-sheet
packet: 15 cogs, four brackets and five upper inserts, with the valid 42-part
core retained. This allows the two existing corner brackets and five inserts
to move, unlike the closed 17-mover phase7 construction. Any new source model
must pass preflight and retain all parts, guards and the original material
target. Native validation still requires a complete source-valid66.

Main `541d5bc9` contains both prior checkpoints. Its
[CI 40685021297](https://github.com/skulitom/Nestbolt/actions/runs/40685021297)
has five successful jobs and Windows checks still running at this checkpoint;
preserve that run before the next main push. Production, READMEs and upstream
heads/releases are unchanged. H2/H5 remain open at **60% completed milestone
weight**; all 22 reserved vectors remain unopened, and no release qualifies.

[Projection audit](h5-short13-x-exclusion-20261028/projection-checks.json),
[full model audit](h5-short13-x-exclusion-20261028/model-checks.json),
[closed response](h5-short13-x-exclusion-20261028/response-checks.json),
[source necessity proof](h5-short13-x-exclusion-20261028/necessity-proof.json),
[updated complete frontier](h5-short13-x-exclusion-20261028/updated-allocations.json),
[next step](h5-short13-x-exclusion-20261028/next-step.json),
[byte-verified archive](h5-short13-x-exclusion-20261028/raw-manifest.json).
The archive preserves 753 canonical files and
145 identical-byte aliases in 14,849,183
compressed bytes, including all source inputs, coverage certificates, models,
auditors, failed preparation, raw logs and the previous main-push receipt.
