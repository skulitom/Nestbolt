# H5: two-phase band and spacing exclusions — 2026-10-26

**The tested two-angle branch is exhausted within its conservative source
geometry and micrometre coordinate grid. Complete family models become
INFEASIBLE after independently verified area and spacing implications are
made explicit. Their conditional exclusions leave the final capacity master
INFEASIBLE. No unrestricted packing-impossibility or H5 acceptance claim follows;
H2/H5 remain open at 60% completed milestone weight.**

## Balanced bracket family: complete choices and band links

Use one bracket each from **0/4, 2/6, 1/7, 3/5**, either insert **8/10**, and
four cogs independently choosing **9/11** (56.25° / 65.25°), with at least one
profile-11 cog. All nine originals remain mandatory and all 18 coordinates
range across the full guarded short stock.

The source includes **64** ordered collision cases and **144** physical
orientation modes over **36** part pairs. Independent geometry reconstruction
checks **30,464** unmerged triangle-pair hulls, **945** guarded faces and
**39,535** planes. All four cog copies have the same allowed choices, so they
can be x-sorted together with their chosen phases; the audit checks **360**
phase/order cases. No separate phase order restricts their spatial sequence.

The **31,797-variable / 32,646-constraint** shared-plane model returns UNKNOWN.
Its exact result remains preserved; no exclusion is inferred from it.

Add **916** Boolean vertical-cell selectors. For every original/profile choice,
the complete disjoint cell cover spans its entire permitted integer Y domain.
Each selector implies its interval, and each of **18** cell sums equals the
existing profile flag. All **63** independently verified band-area bounds are
then linked to the actual selections. No capacity cell is fixed or preferred.
The audit checks **909,760** permitted part/profile Y values through exact
contiguous coverage and all **57,708** cell/band coefficients.

Every parent coordinate witness extends to its unique cells and respects the
necessary occupied-area limits; conversely the new model retains every parent
constraint. This preserves source-coordinate feasibility while exposing useful
implications. The **32,713-variable / 33,643-constraint** model is INFEASIBLE.

Its checked four-count exclusion removes balanced bracket counts from the
mixed-angle master. Independent relabelling checks cover 384 bracket cases,
360 cog phase/order cases and both insert choices—their **276,480** Cartesian
combinations. Exact parent restoration, 10,000 count/flag truth cases and real
solver import pass. The **718-variable / 87-constraint** master remains OPTIMAL,
selecting one bracket each from **0/4** and **2/6**, two from **3/5**, a horizontal
insert, three profile-9 cogs and one profile-11 cog.

## Repeated bracket family: all phases and provable spacing

Broaden that family immediately to both insert choices and all independent
cog 9/11 choices with at least one 11. Its **48** collision cases, **29,056**
triangle-pair hulls, **796** faces and **32,886** planes independently verify.
The two repeated bracket slots may be x-sorted with their profile choices;
other bracket types remain unordered. All 144 orientation modes are retained.

The **31,892-variable / 32,746-constraint** shared-plane base is audited but
never called. Add the complete area channeling first. Its sole
**32,808-variable / 33,743-constraint** call returns UNKNOWN, also preserved.

Next derive cog-spacing bounds from the full original collision envelopes.
For each ordered phase pair, certify a whole forbidden rectangle covering
**every** stock-permitted relative Y, with X from zero through one integer
unit below the proposed bound. Strict containment, with minimum boundary
margin **0.001153 mm**, proves the implication; sampled boundary minima alone
are not used as proof. Independent reconstruction checks **24,336** original
triangle-pair hulls and **704** boundary samples, then every complete rectangle.

| Cog profiles | Required minimum horizontal center separation |
|---|---:|
| 9 / 9 | 257.862 mm |
| 9 / 11 or 11 / 9 | 260.232 mm |
| 11 / 11 | 258.046 mm |

Global cog x ordering makes each difference nonnegative. Add **six** universal
pair bounds at the smallest threshold and **24** bounds conditional on the
actual phase-choice flags. All original variables, clauses, stock choices and
band links remain unchanged. The **32,808-variable / 33,773-constraint** model
is INFEASIBLE in about **19.1 solver seconds**.

## Final conditional capacity result

Exclude exactly **(p0+p4, p2+p6, p3+p5) = (1,1,2)**, independently of insert
orientation or cog phase counts allowed by the master. The audit checks
**9,216** bracket identity/mirror/x-order cases, **360** cog cases and both
insert choices, covering **6,635,520** Cartesian combinations. It verifies
the complete area/spacing implications, actual negative response, unchanged
parent, exact three-count logic and real solver import.

The resulting **721-variable / 94-constraint** master is **INFEASIBLE**.
Together with the earlier separately closed all-profile-9 branch, this leaves
no candidate in the tested two-angle guarded-source/grid branch. Other angles,
compositions and continuous original layouts remain outside that conclusion.

## Preserved calls and preparation failure

| Call | Result | Solver seconds | Shared seconds | Soft overrun |
|---|---|---:|---:|---:|
| balanced_base | UNKNOWN | 45.113378 | 46.004121 | 0.113378 |
| balanced_link | INFEASIBLE | 16.568950 | 17.484831 | 0.000000 |
| repeated_link | UNKNOWN | 46.477276 | 47.383980 | 1.477276 |
| spacing_probe | INFEASIBLE | 19.098474 | 20.000688 | 0.000000 |
| balanced_search | OPTIMAL | 0.305337 | 0.988032 | 0.000000 |
| final_search | INFEASIBLE | 0.290438 | 0.974161 | 0.000000 |

All **six** calls are closed with terminal responses and all **16** audits pass.
The two UNKNOWN calls exceed their 45-second soft limits by **0.113378** and
**1.477276 seconds**, respectively; both remain inside the declared 60-second
shared budget. Necessary calls use 20 / 30 seconds. No watchdog termination,
restart, reseed or extension occurs. Unknown results support no exclusions.

One helper-generation attempt fails after generating the final model builder
and auditor, before creating its runner or opening any solver call. A suffix
test mistakenly routes the runner template through audit-specific replacement
logic. The original helper and failure are preserved; a separate recovery
creates only the two missing helpers. The already prepared model/audit remains
unchanged, and the final master is called exactly once.

## Next work and repository state

Next screen the full 18-degree tooth period at 2.25-degree samples, retaining
the exact existing profiles and adding the six missing original rotations.
Compare original-pair span, certified spacing and band capacity before choosing
a new source family. This finite screen is not a continuous-rotation theorem;
current conditional exclusions cannot transfer to newly added angles.

The full job still requires all **66** originals: **55** checked first-sheet
originals, nine short-sheet IDs **21/22/25/26/37/53/63/64/65**, and pending
first-sheet brackets **28/29**. Full native/material validation, production
integration under the original budget and the full H5 matrix remain required.

At **2026-10-26T07:34:48.699300+00:00**, main and local HEAD are **50cdc07e**. The
[main CI run](https://github.com/skulitom/Nestbolt/actions/runs/40284102018)
has five successful jobs while Windows checks run. Commit and queue this
checkpoint until that run succeeds, without cancelling it. Upstream releases,
production and the accurate READMEs are unchanged. H2 retains its original gate;
all 22 reserved vectors remain untouched. No new release is qualified.

[Checks](h5-two-phase-band-and-spacing-exclusions-20261026/checks.json), [closed calls](h5-two-phase-band-and-spacing-exclusions-20261026/closed-calls.json),
[scope](h5-two-phase-band-and-spacing-exclusions-20261026/scope.json), [next step](h5-two-phase-band-and-spacing-exclusions-20261026/next-step.json),
[preparation failure](h5-two-phase-band-and-spacing-exclusions-20261026/helper-generation-failure.json),
[raw manifest](h5-two-phase-band-and-spacing-exclusions-20261026/raw-manifest.json). All 455
canonical files and 397 aliases are byte/SHA-256/CRC
checked in 1 archive parts.
