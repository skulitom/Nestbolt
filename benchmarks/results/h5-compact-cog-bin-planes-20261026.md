# H5: compact cog bin planes — 2026-10-26

**A verified sufficient cog-pair representation removes 148,074 auxiliary
variables while preserving the implication to every original source collision
clause. Its sole bounded search remains UNKNOWN. No full-source exclusion or
H5 acceptance follows; H2/H5 remain open at 60% completed milestone weight.**

## Whole-bin source proof

The previous complete model contains 231,787 shared planes, of which 148,074
belong to cog/cog pairs. All four cogs share the same eight allowed angles and
can be x-sorted with their profile choices. Use their complete relative-Y
domain, partitioned into 35 disjoint 2 mm integer bins.

For each of the **2,191** nonempty ordered-profile/bin intersections, choose
an actual rounded outside-plane edge for every source convex-face clause.
Positive-X edges give an exact integer lower-X threshold. Other edges are
usable without restriction only if they hold on the full stock-difference
rectangle. Taking the largest per-face threshold gives a sufficient right
rectangle. The independent audit checks all **150,952** face proofs at
**603,808** exact corners, plus whole-rectangle separation from the original
guarded collision geometry. No flat-bound model or solver call is created.

Flattening every edge over its bin would waste room. Retain its sloping source
inequality instead. Exact normalized-line comparisons at both Y endpoints
prove dominance throughout the interval. Remove only lines dominated by
another retained line, preserving a named implication for every source face.
Independent rational arithmetic checks all records. **44,588** unique positive
source edges reduce to **2,407** sloping requirements, with at most three per
profile/bin. **106,089** face edges already hold throughout their full stock
rectangle. Every one of the 150,952 face implications is accounted for.

These constraints are sufficient for the original source clauses. The reverse
implication is not proved: choosing one edge across a whole bin may exclude
some original source points. Even an INFEASIBLE result could therefore exclude
only this compact construction, not the complete eight-angle source family.

## Complete compact model audit

Remove exactly **148,074** cog-only plane flags and their implications, and
**3,660** corresponding face OR clauses. Independently reconstruct the exact
removed constraints as multisets. Retain all other **85,489** parent variables
and **88,493** parent constraints with exact index remapping and field equality.
All original coordinates, angle choices, stock bounds, mandatory counts, cog
ordering, non-cog pair clauses, vertical cells, area limits and existing
spacing bounds remain.

Add **210** complete relative-bin selectors, six exact-one sums and **14,442**
conditional sloping constraints across the six physical cog pairs. The final
model has **85,699 variables / 103,151 constraints**, compared with the full
source's 233,563 / 240,227. All **744** source orientation modes remain covered:
360 by retained source clauses and 384 by proved compact cog implications.
No coordinate is fixed, original omitted, angle separately ordered or hint added.

The full model is independently reconstructed and checked through actual solver
import/export. Every compact witness can extend to the full original source
model by assigning removed plane flags from plane truth. A positive would still
require independent original geometry and full-job validation.

## Closed search and next reduction

The sole 45-second, four-worker, seed-0 call returns **UNKNOWN** after
**46.077775 solver seconds**, with **47.517578 shared seconds**.
The **1.077775-second soft overrun** is preserved;
the declared 60-second shared budget is honored. No watchdog termination,
restart, reseed, extension or profile-family exclusion occurs. All four audits
pass. Earlier full-source UNKNOWN calls also remain closed and inconclusive.

Read-only inspection identifies the remaining shared planes:

| Pair type | Shared planes | Physical modes |
|---|---:|---:|
| bracket / bracket | 2,198 | 24 |
| bracket / insert | 1,811 | 16 |
| bracket / cog | 59,376 | 256 |
| insert / cog | 20,328 | 64 |

Next investigate compact bracket/cog and insert/cog requirements with complete
relative-Y bins and **both left/right alternatives**. Those nonidentical parts
cannot be assigned a fixed x order. Derive actual source difference boxes,
prove every chosen directional edge over its full bin, retain sloping planes,
and prune only exactly dominated lines. Keep bracket/bracket and bracket/insert
clauses. No new solve is justified until full coverage and the original-source
implication independently pass. Negative scope remains conservative and narrow.

All **66** originals remain required: 55 checked first-sheet originals,
nine short-sheet IDs **21/22/25/26/37/53/63/64/65**, and pending first-sheet
brackets **28/29**. Full native/material validation, production integration
under 60 seconds and the complete H5 matrix remain open.

At **2026-10-26T08:29:31.736128+00:00**, main and local HEAD are **7271cc8b**. Its
[CI run](https://github.com/skulitom/Nestbolt/actions/runs/40290567078) has three
successful jobs and three still running. The prior two checkpoints were pushed
normally after all six checks on their previous main passed. Commit and queue
this checkpoint until the current live run succeeds, without cancelling it.
Production, READMEs and upstream stop-rule state remain unchanged. H2 retains
its original gate; all 22 reserved vectors remain untouched. No new release
is qualified.

[Checks](h5-compact-cog-bin-planes-20261026/checks.json), [closed call](h5-compact-cog-bin-planes-20261026/closed-call.json),
[scope](h5-compact-cog-bin-planes-20261026/scope.json), [next step](h5-compact-cog-bin-planes-20261026/next-step.json),
[raw manifest](h5-compact-cog-bin-planes-20261026/raw-manifest.json). All 169 canonical
files and 63 aliases are byte/SHA-256/CRC checked
across 1 archive parts.
