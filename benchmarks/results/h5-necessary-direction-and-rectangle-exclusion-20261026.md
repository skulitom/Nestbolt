# H5: necessary direction and inner-rectangle exclusion — 2026-10-26

**A small necessary model rules out the remaining declared eight-angle branch
for the nine-original short-sheet composition. The old two-angle branch was
closed separately. This does not exclude arbitrary cog angles, different sheet
compositions or continuous native geometry. H2/H5 remain open at 60%.**

## Results and scope

| Experiment | Variables / constraints | Result | Solver / shared seconds |
|---|---:|---|---:|
| h5-directional-cog-plane-probe-20261026 | 8,135 / 86,147 | UNKNOWN | 45.077206 / 46.237709 |
| h5-capacity-phase-mix-probe-20261026 | 233,773 / 253,597 | UNKNOWN | 45.149008 / 47.474273 |
| h5-necessary-direction-projection-20261026 | 2,732 / 3,582 | OPTIMAL | 3.650165 / 4.395420 |
| h5-rectangle-direction-projection-20261026 | 2,732 / 3,779 | INFEASIBLE | 3.748729 / 4.468353 |

All four sole calls are closed, with four workers and seed 0. The first two use
45 solver /60 shared seconds; the two necessary projections use 20/30. Soft
overruns of 0.077206 and
0.149008 seconds are preserved. Both shared budgets
pass. Neither UNKNOWN supports a count or geometric exclusion. No retry occurs.

The excluded fixed composition contains originals 21/22/25/26/37/53/63/64/65:
four brackets, one insert and four cogs. Every bracket independently chooses
all eight quarter-turn/mirror profiles; the insert has both orientations. Cog
phases are 56.25°,58.5°,60.75°,63°,65.25°,67.5°,69.75°,72°. The new model requires
at least one of the six newly added phases. The previously closed 9/11-only
branch is preserved in [the two-phase report](h5-two-phase-band-and-spacing-exclusions-20261026.md).
The conservative source guard and micrometre coordinate grid remain explicit.

## Earlier reductions remain inconclusive

The bidirectional compact construction covers 80 profile pairs across 15,680
directional 1 mm bins. It retains 15,736 sloping requirements and accounts for
406,340 source-face implications. Both left and right alternatives are present.
Removing 79,704 additional source plane flags yields 8,135 variables and 86,147
constraints. The independent audit proves a compact witness implies the full
source; reverse equivalence is not claimed. Its sole search returns UNKNOWN.

A separate full-source subfamily fixes only cog counts to three profile 9 and
one profile 15, selected by the earlier necessary area allocation. Every original
coordinate and complete vertical cell remains free. This unreduced 233,773-variable
model also returns UNKNOWN. No exclusion is copied from either attempt.

An exploratory compact-only order calculation is retained, but it is not the
basis for the final necessary model and has no independent-audit claim.

## Necessary horizontal bounds from original geometry

For each of 80 non-cog/cog profile cases, inspect the entire stock-allowed relative
Y interval and analytic source-boundary crossings. Prove a central rectangle
strictly inside the original guarded collision region, at every relative Y.
All integer deltaX values between the two retained endpoints are forbidden.
The resulting disjunction is therefore necessary: deltaX≤L or deltaX≥R.

For each non-cog profile, take the weakest L/R bounds across all eight cog choices
and independently check all 80 aggregate rectangles again. The minimum interior
margin exceeds 0.0009986 mm. Consecutive x-ordered cogs have source-proven minimum
spacing 256.820 mm. A right-then-left side assignment would contradict
R+spacing−L>0, whose minimum margin is 644.450 mm. Thus 15 monotone side clauses
are necessary, without fixing a nonidentical part's side.

The first projection has 18 original coordinates, 66 profile flags, 20 side flags
and 2,628 complete vertical-cell selectors: 2,732 variables and 3,582 constraints.
It includes 272 direction inequalities, 390 cog spacing bounds, 66 cell/profile
equalities and 63 exact area-band capacities. Independent reconstruction checks
every field, 165,564 cell-band coefficients and 2,614,368 covered integer Y values.
Sorting identical copies with their profiles covers 98,304 bracket choice/order
cases and 97,920 active cog choice/order cases. No balanced bracket count
restriction, compact sufficient guard, fixed pose or prior count cut is added.

The projection returns OPTIMAL quickly, but original geometry inspection finds
11 overlapping pairs. This is a necessary allocation only, never a valid layout.

## Inner rectangles close the branch

Each bracket is partitioned into three source-coordinate grid cells and each
insert into one. Inset each cell by 1 micrometre on every side. Independent checks
prove all 26 profile rectangles strictly inside their actual original filled
outers, with at least 0.00099999 mm boundary margin. The inset weakens the test;
no sufficient clearance or enlarged bounding box is introduced.

Retain the entire necessary parent model field-for-field. Its 98 physical/profile
rectangles get 196 optional intervals, each present exactly when its profile is
chosen, and one global 2D non-overlap constraint. Starts and ends are the original
anchor plus audited inner coordinates. No variables or fixed poses are added.
Every disjoint source placement must satisfy these inner-subset constraints.
The final 2,732-variable/3,779-constraint model returns INFEASIBLE in
3.748729 solver seconds. All 11 audits pass, including
actual import/export and independent readback of the sole response.

## Continuation and publication

Next derive an orientation-independent inner cog shape from the original
20-tooth boundary, then investigate necessary bounds for every allowed cog
rotation. Finite-angle stock boxes and band coefficients must not be reused
without proof. This remains a diagnostic branch; alternate sheet compositions
are open and any positive needs full original geometry checks.

All 66 original identities remain required: 55 checked first-sheet originals,
nine short-sheet originals and pending first-sheet brackets 28/29. Full native
material validation, production integration under 60 seconds and the full H5
matrix remain open. No new release or production-quality claim is qualified.

At 2026-10-26T09:12:51.451356+00:00, local HEAD is bc9edc2b and main is 7271cc8b. All six jobs in
[main CI 40290567078](https://github.com/skulitom/Nestbolt/actions/runs/40290567078)
pass. Queue this checkpoint with bc9edc2b for a normal push after verifying
staged evidence and ancestry. Product source, READMEs and upstream stop-rule
state are unchanged. H2 retains its original gate and all 22 reserved vectors
remain untouched.

[Checks](h5-necessary-direction-and-rectangle-exclusion-20261026/checks.json), [closed calls](h5-necessary-direction-and-rectangle-exclusion-20261026/closed-calls.json),
[scope](h5-necessary-direction-and-rectangle-exclusion-20261026/scope.json), [next step](h5-necessary-direction-and-rectangle-exclusion-20261026/next-step.json),
[raw manifest](h5-necessary-direction-and-rectangle-exclusion-20261026/raw-manifest.json). All 311
canonical files and 211 aliases are checked by byte
length, SHA-256 and CRC across 1 archive parts.
