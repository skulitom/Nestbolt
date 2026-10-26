# H5: complete composition selection and original support — 2026-10-26

**A complete necessary selector accounts for all eleven remaining originals
and finds two eight-part short-sheet allocations. Neither is proved optimal
or an original geometric layout. New all-angle support bounds strengthen cog
spacing and bracket separation. Nine-or-more decisions remain UNKNOWN;
no count exclusion follows. H2/H5 remain open at 60%.**

## Complete sheet obligations and first-sheet resource

The checked first-sheet partial has 55 originals. The remaining originals are
**21/22/25/26/28/29/37/53/63/64/65**: six brackets, one insert and four cogs.
Every selector flag means either a selected short-sheet part or a mandatory
first-sheet addition. No original disappears and absent proxy coordinates
do not assert a first-sheet pose.

Recompute each family filled-outer area exactly using both shoelace and anchored
triangle formulas. With part-in-part off, cutouts do not reduce occupied area.
The first-sheet area capacity uses its actual dimensions, margins and edge
clearance, relaxed outward by 0.020 mm. Total original area minus that capacity
requires at least **39,892,822 area units** on the short sheet (1,000 units/mm²).
Ceil each selected family coefficient and floor the lower bound, weakening the
integer constraint conservatively. This area condition cannot prove a fit.

The objective ranks selected short-sheet count before rounded original area.
A count weight of 1,000,000,000 exceeds the maximum secondary area term of
460,050,876. Both selections preserve the exact complement of all 66 identities.

## Models and closed calls

| Experiment | Variables / constraints | Result | Solver / shared seconds |
|---|---:|---|---:|
| h5-complete-composition-selector-20261026 | 2,416 / 3,275 | FEASIBLE | 20.024937 / 20.771821 |
| h5-support-composition-selector-20261026 | 2,416 / 3,275 | FEASIBLE | 20.023314 / 20.793714 |
| h5-nine-short-decision-20261026 | 2,416 / 3,276 | UNKNOWN | 20.036722 / 20.774148 |
| h5-geometric-nine-decision-20261026 | 116 / 859 | UNKNOWN | 20.062534 / 20.708892 |

All four sole calls use 20 solver / 30 shared seconds, four workers and seed 0.
The shared limits pass. Their soft overruns are preserved as
**0.024937 / 0.023314 /
0.036722 / 0.062534 seconds**.
Every call is closed; no restart, reseed or extension occurs.

The complete selector has 11 presence flags, 54 profile choices, 2,300 complete
vertical-cell flags, 63 fresh band bounds, 146 optional inner rectangles,
conditional original spacing rules and the previously proved composition cut.
Selected identical copies form a prefix and are ordered with their profiles;
every pair condition is inactive for absent parts. Independent reconstruction
checks every field, 144,900 cell-band coefficients, 46,080 bracket and 384 cog
presence/rank permutations, exact objective and actual solver import/export.

The first FEASIBLE selection has **three brackets, one insert and four cogs**,
leaving originals **26/28/29** mandatory on the first sheet. Its objective is
8,340,050,876, with upper bound 10,409,988,157. The strengthened FEASIBLE selection
has **four brackets, one insert and three cogs**, leaving **28/29/65** mandatory
on the first sheet. Its objective is 8,329,988,157 with the same upper bound.
Neither proves maximum selected count, original clearance or first-sheet fit.

## All-angle original-tip support

The original cog contains a centered disk of radius **109.115 mm**. Its convex
hull contains a centered disk of radius **139.270 mm**, while every original
vertex lies within radius **140.001 mm**. Thus in any direction some original
vertex has projection at least h=139.270 mm and norm at most R=140.001 mm.
At center distance d from another cog, that vertex's squared distance from the
other center is at most **d² - 2hd + R²**.

Exact integer arithmetic proves this is strictly less than r² throughout
**[2r, 247.444 mm]**: the quadratic is convex and both endpoint values are
negative. Smaller distances collide by the two original inner disks. Therefore
original cog centers need at least **247.444 mm** separation at every real
rotation. After a conservative 3-micrometre anchor-rounding loss and the full
relative-Y range, the necessary X gap increases from **215.446 to 245.034 mm**.

Every bracket has an inset full-height vertical stem. The transverse component
of the cog support vertex is at most 15 mm, and the whole allowed relative-Y
range places that vertex inside each stem's height. The stem width plus inner
disk radius exceeds the outer radius, so the disk/stem and support-tip/stem
forbidden X intervals overlap. Their union extends a necessary directional
endpoint for each of the eight bracket profiles. Account for relative anchor
rounding and merge only overlapping, already proved forbidden intervals.

The strengthened selector changes exactly **192 bracket/cog endpoints and six
cog gaps**. Independent restoration proves every other parent field and the
objective unchanged. These bounds apply to actual original geometry for every
angle and continuous anchor; earlier proxy-only solutions need not survive.

## Nine-or-more remains open

A distinct decision removes the objective and requires at least nine short-sheet
parts, retaining every other constraint and original obligation. Complete parent
restoration and import pass, but the sole call is UNKNOWN.

A separate necessary projection removes all 2,300 vertical-cell variables,
their 2,300 implications, 54 cell/profile sums and 63 band bounds. Every other
field is retained, including the first-sheet resource, nine-part requirement,
source support and optional rectangle constraints; interval references are
remapped and audited. This weaker **116-variable / 859-constraint** geometry
model also returns UNKNOWN. No nine/ten-part exclusion is inferred.

## Verified next formulation

All eight quantization-safe bracket stems span a common Y interval,
**69.448–256.478 mm**, at every allowed anchor. At the shared line **Y=160 mm**,
disjoint original brackets require disjoint stem X intervals. This suggests
ordering identical selected brackets by stem starts instead of bounding-box
anchors, making adjacent stem separation explicit.

The five old bracket anchor-order constraints are identified exactly and must
be removed before adding the new order. Retain presence-prefix symmetry, add
six stem-start variables, 48 conditional affine profile channels and 40
conditional adjacent width inequalities. The expected model has **122 variables
/ 942 constraints**. Imposing both orders would be unsound. The common-line
proof and source relabelling are audited; no new model or call is prepared yet.
Require complete field/reference and import audits before a bounded call.

Full original geometry on both sheets, all 66 native/material checks, production
integration within 60 seconds and the complete H5 matrix remain required.

## Repository and evidence

At **2026-10-26T10:11:13.496192+00:00**, local HEAD is **5025ace1**, queued above main **6246967c**.
All six jobs in [main CI40298314725](https://github.com/skulitom/Nestbolt/actions/runs/40298314725)
now pass. Normally push both queued checkpoints after staged-byte and ancestry
checks. Production, READMEs, upstream stop-rule state and all 22 reserved H2
vectors remain unchanged. H2 retains its original gate; no release is qualified.

All **eleven audits pass**. [Checks](h5-complete-composition-selection-and-support-20261026/checks.json),
[closed calls](h5-complete-composition-selection-and-support-20261026/closed-calls.json), [scope](h5-complete-composition-selection-and-support-20261026/scope.json),
[next step](h5-complete-composition-selection-and-support-20261026/next-step.json), [raw manifest](h5-complete-composition-selection-and-support-20261026/raw-manifest.json).
All 184 canonical files and 197
aliases are byte/SHA-256/CRC verified across 1 archive parts.
