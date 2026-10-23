# H5: continuous cog contacts and clearance-outline repair — 2026-10-23

**4,000 new cog poses pass original geometry and independent membership checks
against all 30 repair cores.** Of these, 3,971 have centers more than 0.05 mm
from every old cog center on their sheet, and 2,075 make at least one old
bracket candidate available relative to the released cog. These are candidate
positions, not additional placed parts. No new layout selection occurs here;
the best checked layout remains **64/66**, missing two brackets. H2/H5 stay
open at **60%** completed milestone weight.

## Failed check and repaired clearance construction

The original attempt stopped at its first cached-obstacle equivalence check,
before any region query completed or placement was generated. Its source,
plan and traceback remain intact. The original fixed cog shape and its
translated copy are exactly equal. Their unbuffered Minkowski obstacles differ
by only 2.54e-13 mm, but mitred
clearance buffering amplifies the difference to
**0.030732836758 mm**, with symmetric-difference area
0.004813395644 mm². This failed the existing strict check.

A proposed round-buffer replacement also failed the same equivalence threshold:
0.000061861367 mm. Its stopped assertion
and the subsequent diagnostic that records all values are preserved. Neither
failure is omitted or counted as a completed placement search.

The repaired helper constructs an explicit circumscribed **128-gon** around
the required 0.2 mm clearance plus the existing 0.0001 mm construction margin.
Every chord is independently checked to lie at least 0.2001 mm from its center.
The resulting radius is 0.200160284535 mm.
The helper forms the Minkowski sum by uniting the original obstacle with each
boundary segment swept by this convex polygon; hole rings are included.
This identity is independently checked against sums over exact convex pieces
for concave and holed examples, with zero difference.

On the unchanged failed case, the globally constructed and translated repaired
obstacles agree within **2.54e-13 mm**
and 1.13e-10 mm². All eight actual
family/orientation cache cases also pass the original 1e-7 mm / 1e-4 mm²
equivalence limits. Original part vertices, clearance and acceptance tolerances
are unchanged. This is a development helper repair; production code is unchanged.

## Completed region and bounded proposal passes

The new directory uses the same **120-second region allowance**, **60-second
proposal allowance** and **4,000-new-pose cap**. It considers the original wide
seed's 15 cores, each fixing 18 frames and 14 cogs, on both sheets. Four sampled
angles use the original **-2.2428996024478143 radians (-128.508681091830°)**
plus 0°, 4.5°, 9° and 13.5°. Cogs are never mirrored. These are finite free-angle
samples, not an exhaustive rotation search.

All **120/120** regions complete in **6.073348 seconds**;
none is empty. Representatives, boundary vertices and edge midpoints are
preserved for every region. Proposal lists are processed round-robin with exact
transform deduplication. The pass reaches its 4,000-pose cap after
**37.156931 seconds** and 18,339 events:
4,000 additions and 14,339 exact duplicates. There are no original-geometry
rejections. **60 unfinished proposal lists remain recorded**, and are not
resumed or silently completed. Conservative regions cannot prove impossibility.

## Independent original-geometry audit

All **35,488 original pool records** remain exactly equal as parsed JSON,
with all original indexes and seeds intact. Independent original-vertex
reconstruction checks all 4,000 new poses, their transforms, allowed stock
domains, source query points, areas and generating-core distances. It verifies
all 95,326 original generation pairs.
Every one of the 18,339 queue events and every
pending-list cursor replays exactly; all 120 saved regions and proposal lists
verify.

Compatibility is then checked against **all 30 cores**, including the second
seed's frame positions. All **120,000**
memberships agree between individual fixed-part distances and distances to
the full filled core unions. This includes
140,040 distinct fixed-part pairs and
120,000 union distances. The future conditional pool therefore retains all
**16,058 old variable choices plus 4,000 new cogs: 20,058 choices**. All 30
mapped 64-part baselines remain present.

Bracket effects are independently recalculated with a sequential bounds scan
and **4,031,840** exact distances,
rather than the generator's spatial-tree lookup. Every gain/loss list matches.
The largest single gain is **290 bracket
candidate positions**. This is not a claim that 290 brackets, or even one
additional bracket, can be placed together with the required inventory.
Nearest original cog centers are independently reconstructed by affine
centroid transforms. The complete audit takes 18.223668 seconds.

## Next action and gate status

Build one fresh conditional model using all 20,058 audited variable poses across the same 30 fixed cores: retain every one of the 16,058 old choices and all 4,000 new cogs before reduction. Preserve the full original 66-part target and all 30 mapped 64-part baselines. The previous unreduced original graph may supply unchanged old-old edges only after exact mapping/hash verification; compute and independently check every new cog/bracket and cog/insert conflict. Because the unchanged conditional inventory permits at most one variable cog, an explicitly declared complete cog clique is a valid derived strengthening, including pairs that are not geometric conflicts. Verify that implication separately and distinguish derived edges from original geometric edges. Use fresh core-compatibility-preserving substitutions and exact constraint reconstruction; never reuse the earlier reduction. Predeclare a single bounded solve with the previous 60-second/eight-worker/seed-zero/presolve-disabled strategy. Audit every resulting original layout and frozen-CLI result. Do not resume the 60 capped proposal lists, repeat prior solvers, claim a full target witness from bracket-candidate counts, or infer native/production H5 qualification.

No solver, native packing, production-budget qualification, complete H5 matrix
or held-out evaluation occurs. All 66 original copies, the original material
target, native guard, original production budget and all 13 jobs at both kerfs
remain required. The original cores are not native-margin qualified; the new
contact construction does not change that. No milestone or new release is
qualified by this diagnostic.

All six hosted checks for 752b1c60 pass. The queued d49d0ff6 and facf0f38
checkpoints were then pushed normally to main, with no incoming changes.
The new facf0f38 run 39984899040 is saved as
`in_progress` / `pending`. Source and all
three accurate READMEs remain unchanged; preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain current.

Evidence: [original seed view](h5-one-cog-continuous-regions-20261023/original-seed.png),
[failed mitre check](h5-one-cog-continuous-regions-20261023/mitre-diagnosis.json), [failed round check](h5-one-cog-continuous-regions-20261023/round-diagnosis.json),
[polygon repair](h5-one-cog-continuous-regions-20261023/polygon-repair.json), [cache checks](h5-one-cog-continuous-regions-20261023/obstacle-cache-audit.json),
[generation](h5-one-cog-continuous-regions-20261023/generation.json), [independent audit](h5-one-cog-continuous-regions-20261023/audit.json),
[source review](h5-one-cog-continuous-regions-20261023/source-review.json), raw evidence [part 1](h5-one-cog-continuous-regions-20261023/raw-001.zip), and
[manifest](h5-one-cog-continuous-regions-20261023/raw-manifest.json). All 190 canonical
members and 24 aliases are byte-verified, with archive
CRCs and SHA-256 hashes checked. Each ZIP part is independently readable and
below 50 MiB; all original paths remain represented.
