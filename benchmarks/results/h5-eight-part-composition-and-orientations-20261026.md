# H5: changed composition and all bracket orientations — 2026-10-26

**The eight-part short-sheet inventory passes a necessary capacity test, but
has no verified placement. One fixed orientation pattern is excluded; all
allowed bracket orientations remain unresolved after two equivalent bounded
searches. H2/H5 remain open at 60% completed milestone weight.**

## Original-part accounting

Keep the previously verified first-sheet exchange: insert36 occupies cog53's
old position. All55 first-sheet originals remain checked. The nine-part
second-sheet composition has originals21/22/25/26/37/53/63/64/65. Changing only
the insert count from two to one in the exact673-variable/66-constraint band
model returns **INFEASIBLE**, in0.136694 solver /0.851925 shared seconds.
Every coefficient and63 capacity rows remain unchanged and parent restoration
is independently verified. This is a scoped solver result; the earlier
ten-part continuous certificate is not transferred to these new counts.

Next require insert37 on the first sheet as well. The second-sheet originals
are **21/22/25/26/53/63/64/65**: four brackets and four cogs. The55 checked
first-sheet originals plus these eight and the pending first-sheet originals
**28/29/37** account for all66 identities exactly once. None is dropped and no
first-sheet position is asserted for the pending three.

Changing only the necessary model's insert count/bounds from one to zero
returns **OPTIMAL**, in0.060929 solver /0.747618 shared seconds. Independent
readback checks all673 values,66 constraints, family totals and63 band loads.
The selected bracket profiles are5/5/6/7, with four cogs at the recorded angle.
This allocation ignores horizontal collisions and is not a layout.

## Full coordinate checks

The selected profiles define one fresh eight-original model with all16
coordinates free throughout the guarded short stock. Band cells are not locks
or hints. All28 physical pairs are retained. Independent geometry checks
reconstruct four original profiles, eight collision cases from7,084 unmerged
triangle-pair hulls,162 guarded faces and6,960 outside planes. Complete model
and real import audits pass for6,296 variables /6,431 constraints. Its sole
call returns **INFEASIBLE**, in1.823040 solver /2.580368 shared seconds.

A preflight script mistakenly compared the45-second solver budget with the
28-pair count. That audit and its downstream preparation failures are retained;
**zero solver calls opened**. The corrected audit and model use separate paths.
Geometry, identities and the declared budget did not change. The source plan
also retains a superseded historical description; its explicit new inventory
and typed parameters define the eight-part experiment and are checked exactly.

The broader model permits **all eight bracket quarter-turn/mirror choices**
independently, retaining the current cog angle. All73 collision cases are
independently rebuilt from9,604 triangle-pair hulls, with472 guarded faces and
24,986 outside planes. Minimum source guard0.2126mm exceeds the required
native0.211709mm. The model includes all518 orientation modes across28 pairs.
Sorting identical bracket copies by profile and cog copies by x coordinate
preserves feasibility by relabelling the same original family geometry.

The entire95,748-variable/97,636-constraint model and actual import pass
independent reconstruction. Its45-second call returns **UNKNOWN**, taking
45.147155 solver /46.628652 shared seconds. The0.147155-second soft overrun is
recorded; the shared60-second budget passes. UNKNOWN excludes no placement.

## Equivalent reduction of repeated constraints

A distinct formulation shares identical physical pair-plane literals across
orientation modes. It removes **55,298 repeated flags**, reducing the model to
**40,450 variables /42,338 constraints**. It preserves all48 coordinate/profile
variables,74 count/stock/symmetry constraints and1,862 face disjunctions.

An independent audit checks every one of95,700 edge projections onto40,402
shared planes, exact inactive-mode escape literals, complete model fields and
actual import. Equivalence holds in both directions: old feasible coordinates
can set each shared flag to its plane truth; shared flags can be copied back
to every corresponding old edge flag without losing a required face clause.

Its separately bounded call also returns **UNKNOWN**, in45.114145 solver /
46.029010 shared seconds, retaining the0.114145-second soft overrun. This is a
smaller equivalent diagnostic model, with no demonstrated packing improvement.

## Remaining work and repository

All five calls are closed. Next examine permitted cog rotations and their
original geometric support widths before choosing a different placement
formulation. Current-angle exclusions do not transfer to another angle or to
the complete job. All66 originals, native/material validation, production-budget
integration and the full13-job/two-kerf/three-seed H5 matrix remain required.

At 2026-10-26T05:38:25.163217+00:00, main81cc4186 has **five passed checks and one still live**
in [CI40273506020](https://github.com/skulitom/Nestbolt/actions/runs/40273506020).
Preserve that run before the next normal push. Production source, accurate
READMEs, upstream heads/releases and all22 reserved H2 vectors remain unchanged.
No new release is qualified.

[Checks](h5-eight-part-composition-and-orientations-20261026/checks.json), [closed calls](h5-eight-part-composition-and-orientations-20261026/closed-calls.json),
[next step](h5-eight-part-composition-and-orientations-20261026/next-step.json), [raw manifest](h5-eight-part-composition-and-orientations-20261026/raw-manifest.json).
All 347 canonical files and 281
aliases are byte/SHA-256/CRC verified across 1 archive parts.
