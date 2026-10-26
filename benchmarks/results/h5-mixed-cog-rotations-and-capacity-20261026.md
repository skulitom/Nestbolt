# H5: mixed cog rotations and capacity — 2026-10-26

**Independent cog rotations restore necessary capacity, but the selected
two-and-two and three-and-one orientation families both fail complete
coordinate checks. These are scoped diagnostic negatives. No full 66-part
target layout or H5 completion is claimed; completed milestone weight is 60%.**

## Original geometry and angle screen

The original cog has **20 teeth**, with four vertices per tooth. Checking the
actual radii and angular repetition establishes an 18-degree pitch, so the
half-tooth phase shift is **9 degrees**. Append profile **11 at 65.25 degrees**
to the existing **profile 9 at 56.25 degrees**. All 11 parent profiles retain
their exact values. The new width and height are approximately **279.576947 mm**;
the original 80 outer vertices and 200-vertex hole are retained.

For all four ordered angle pairs, construct the original filled-outline
Minkowski collision region and its conservative 0.2126 mm clearance envelope.
Screen the rightmost forbidden x over stock-permitted relative y using all
boundary vertex heights and endpoints. Selected offsets are rounded to the
micrometre grid and checked against original outlines, cutouts and stock.

The independent audit reconstructs all **12 profiles**, **24,336** unmerged
triangle-pair hulls, all four guarded regions, **708** boundary samples and all
four two-original placements. The minimum original pair gap is **0.212800 mm**,
above the native requirement **0.211709 mm**. Maximum profile reconstruction
error is 8.04×10⁻¹⁴ mm.

The best checked same-phase pair spans **536.405800 mm**; the best mixed pair
spans **539.292373 mm**, about **2.886574 mm wider**. Thus alternating this
half-tooth phase does not improve the screened two-part span. This local
comparison does not exclude arrangements with brackets, inserts or other
angles. It supplies no full-layout acceptance evidence.

## New necessary capacity and full coordinate checks

Rebuild and independently recompute **44,667** exact band-area coefficients
over **709** vertical cells and **63** stock bands. The new capacity model
retains all eight bracket profiles, both insert profiles and both cog angles.
Four brackets, one insert and four cogs remain mandatory, with **at least one
cog at profile 11**. No previous fixed-angle exclusion is transferred.

The actual **709-variable / 67-constraint** model is independently reconstructed
and imported. Its first bounded call is OPTIMAL, selecting bracket profiles
**4/5/5/6**, insert **10**, two cogs **9** and two **11**. The original run
description accidentally says 66 constraints; the actual model and both
independent audits include the 67th new-phase count constraint. Original bytes
are retained with a [documentation erratum](h5-mixed-cog-rotations-and-capacity-20261026/run-description-erratum.json).

Broaden the selected bracket types to all mirrors: one each from **0/4** and
**2/6**, two from **3/5**, with horizontal insert **10**. Both cog phases have
two mandatory copies. All 18 coordinates range over the full guarded stock;
no selected capacity cell or prior position is fixed. Only identical bracket
slots are profile-ordered, and cog x ordering applies separately within each
same-phase pair.

Independent geometry checks cover **39** collision cases, **22,612** unmerged
triangle-pair hulls, **655** guarded faces and **27,254** outside planes. The
**14,433-variable / 14,812-constraint** shared-plane model retains all **74**
physical orientation modes over all **36** pairs. Its only call is INFEASIBLE.

An exact conditional count exclusion removes only
**(p0+p4, p2+p6, p3+p5, p10, p11) = (1,1,2,1,2)**. The audit checks **9,216**
joint bracket/cog identity permutations, all six assignments of two cog phases,
40,000 count/flag truth cases, exact parent restoration and actual solver import.
The resulting **714-variable / 78-constraint** master remains OPTIMAL and
selects balanced bracket types, vertical insert **8**, three cogs **9** and
one **11**.

The next coordinate model allows one bracket each from **0/4, 2/6, 1/7, 3/5**,
including every mirror choice. Distinct bracket slots are unordered. Only the
three identical profile-9 cogs are x-ordered. Independent reconstruction checks
**52** collision cases, **17,920** triangle-pair hulls, **733** guarded faces and
**30,814** planes. Its **12,721-variable / 13,047-constraint** model also retains
all 74 modes / 36 pairs and returns INFEASIBLE. Its exclusion has not yet been
added to the master; the result remains preserved in full.

## Closed calls and next step

| Call | Result | Solver seconds | Shared seconds |
|---|---|---:|---:|
| search | OPTIMAL | 0.189884 | 0.862671 |
| exclusion_search | OPTIMAL | 0.264774 | 0.934491 |
| group_probe | INFEASIBLE | 19.966488 | 20.714431 |
| three_probe | INFEASIBLE | 21.901258 | 22.675988 |

All **four** calls are closed with terminal responses. Necessary calls use
20 solver / 30 shared seconds; coordinate calls use 45 / 60, four workers and
seed zero. There are no overruns or retries. All **12** independent audits pass.

Next combine the remaining balanced families in one broader source model:
each cog independently chooses **9/11**, and the insert chooses **8/10**, with
at least one profile-11 cog. This covers **144** physical orientation modes
and **64** ordered collision cases. Global cog x ordering is then valid because
all four identical original copies have the same allowed choices; do not add
a separate phase ordering that would constrain their spatial sequence.
Audit every original region, stock bound, source clause, shared plane and
actual import before a newly declared bounded call. Existing fixed-phase
negatives do not by themselves exclude the broader family.

All identities remain explicit: **55** checked first-sheet originals, mandatory
second-sheet **21/22/25/26/37/53/63/64/65**, and pending first-sheet brackets
**28/29**. Full original/native/material checks, production integration under
the existing budget and the complete H5 matrix remain necessary.

At **2026-10-26T07:03:51.398095+00:00**, [main CI40277918871](https://github.com/skulitom/Nestbolt/actions/runs/40277918871)
for **88e1dc19** passes all six jobs. Queued **1299e16b** and this checkpoint can
be pushed normally after staging and ancestry verification. Production,
READMEs, upstream heads/releases and all 22 reserved H2 vectors remain unchanged.
H2 keeps its original gate. No new release is qualified.

[Checks](h5-mixed-cog-rotations-and-capacity-20261026/checks.json), [pair comparison](h5-mixed-cog-rotations-and-capacity-20261026/pair-comparison.json),
[closed calls](h5-mixed-cog-rotations-and-capacity-20261026/closed-calls.json), [next step](h5-mixed-cog-rotations-and-capacity-20261026/next-step.json),
[raw manifest](h5-mixed-cog-rotations-and-capacity-20261026/raw-manifest.json). All 360
canonical files and 291 aliases are byte/SHA-256/CRC
verified in 1 archive parts.
