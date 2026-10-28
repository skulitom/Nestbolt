# Source stem-gap width exclusion — 2026-10-28

**Eight brackets and six inserts cannot fit on the target short sheet.**
An independently checked source-geometry argument requires at least
**1,489.948 mm** of horizontal width. The outward-relaxed sheet offers
**1,487.040 mm**, a deficit of **2.908 mm**. Deleting extras also excludes
eight brackets/seven inserts. These two new exclusions reduce the complete
frontier from 448 to **446** necessary candidates. All 4,576 original rows,
including previous exclusions, remain recorded.

## Closed full-shape construction

Before deriving the structural bound, one conservative source construction
tries eight brackets and six inserts with complete integer-micrometre X/Y
domains and all allowed outer modes. Each original filled outer is expanded
by 112 µm and partitioned into disjoint rectangles; nonoverlap would guarantee
224 µm source clearance, above the unchanged 211.708673 µm requirement.
Original stock domains retain at least 13 µm extra clearance.

Independent original-polygon checks verify all ten outer classes, their exact
expanded unions and the known source-valid 13-part control. Its minimum source
gap is 0.225 mm, with 0.025 mm extra stock clearance; its expanded shapes retain
a 1 µm gap. The model reader verifies all 104 variables, 613 constraints, 140
optional components and 100 partial-hint values. No placement is fixed. The
sixth insert is unhinted, and all 14 originals are mandatory.

The sole 60-second, four-worker call returns **UNKNOWN** after 288,795 branches
and 79,656 conflicts: 60.104262 s returned / 60.912529 s shared. The 0.104262 s
soft return overrun is retained. There is no assignment, source14 witness or
native call, and the call is closed. Its unknown result contributes **nothing
to the exclusion proof** below.

## Source-to-gap argument

Inset each original orthogonal rectangle by 2 µm, then floor the source anchor
to integer micrometres. The inset covers the less-than-1 µm displacement, so
every resulting rectangle remains inside the original filled outer. Holes stay
reserved. A separate check covers every one of the job's 12 declared transform
combinations: eight bracket transforms and four insert rotations reduce to ten
occupied outer classes.

Each bracket has one full-height stem and one wing. A stem is at least
249,996 µm high, and any wing or insert is at least 74,996 µm high. Their sum,
324,992 µm, exceeds the relaxed stock height of 312,967 µm. Therefore a stem's
X interval cannot overlap another source rectangle's X interval. Eight stems
partition the stock width into nine gaps; every insert stays in one gap.

A wing is separated from its own inward stem by only 4 µm. Another stem is
at least 74,996 µm wide, so it cannot intervene there. Each wing therefore
belongs to the adjacent left or right gap. At most two wings border any gap.
All eight bracket modes map to one of four stem-type/direction choices.

Within a gap, discard fixed wing anchors and source Y positions, retaining
only interval widths and summed vertical capacity. This is a relaxation.
For each wing combination and each 0–6 insert orientation split, enumerate
every distinct task order and place each interval at its earliest feasible X.
The exactness argument is given in the [necessity proof](h5-short-stem-gap-exclusion-20261028/necessity-proof.json).
In brief, processing any feasible schedule in original start order and shifting
each next task to its earliest feasible start cannot delay it or any later task.
An earliest start is zero or a previous interval end. Consequently at least one
enumerated order attains a relaxed minimum no greater than any source schedule.

The independent reader checks **168 cases, all 12,925 distinct orders and
94,348 earliest-start steps**, including nonoptimal schedules. It then verifies
all 42 gap bounds, 169 chain states and 2,380 transitions. A separately written
backward recurrence agrees on all 63 terminal bracket/insert count cases.
The known valid eight-bracket/five-insert source layout maps into its actual
nine gaps and passes; its relaxed width lower bound is 1,424.948 mm.

For eight brackets/six inserts, the minimum sum of inward stem widths and
relaxed gap widths is **1,489.948 mm**. This exceeds even the larger relaxed
stock by 2.908 mm, so the actual smaller target cannot contain that subset.
Only **8/6/0 and 8/7/0** were previously surviving supersets. Known valid
8/5/0 and 7/4/1 remain allowed. This is not a full66 infeasibility argument.

## Next work and publication

Both eight-bracket branches are now closed. Next predeclare the finite larger
gap cases needed for the remaining seven-bracket allocations, reusing the
verified 0–6-insert tables exactly. Independently check the extended enumeration
and recurrence before excluding anything. Use the remaining counts to choose a
different complete source construction; the valid64 still lacks two brackets.
No source search is restarted and no material, PIH or clearance rule changes.

The previous main checkpoint `f61f25d6` passes all six jobs in
[CI 40704324149](https://github.com/skulitom/Nestbolt/actions/runs/40704324149).
Production, READMEs and upstream heads/releases are unchanged. H2 and H5 remain
open at **60% completed milestone weight**; all 22 reserved H2 vectors remain
unopened and no new release qualifies.

[Closed source response](h5-short-stem-gap-exclusion-20261028/source-response-checks.json),
[independent width audit](h5-short-stem-gap-exclusion-20261028/gap-audit-checks.json),
[complete allocation list](h5-short-stem-gap-exclusion-20261028/updated-allocations.json),
[next step](h5-short-stem-gap-exclusion-20261028/next-step.json),
[byte-verified archive](h5-short-stem-gap-exclusion-20261028/raw-manifest.json).
The archive preserves 249 canonical files and
42 identical-byte aliases in 362,231
compressed bytes, including every task order, schedule, source model, input,
auditor, failed call and the preceding main-push receipt.
