# H5: aligned-angle profile-family exclusions — 2026-10-26

**The fixed 56.25-degree cog branch is closed within its guarded source models
and micrometre coordinate grid. After full coordinate checks exclude the
remaining orientation families, the strengthened capacity model is INFEASIBLE.
This is a conditional diagnostic result, not a complete-layout result or an
unrestricted packing-impossibility claim. H2/H5 stay open at 60%.**

## Preserved composition and scope

Every case retains four brackets, one insert and four cogs on the short sheet:
original IDs **21/22/25/26/37/53/63/64/65**. The verified first-sheet exchange
retains 55 other originals; brackets **28/29** still require first-sheet positions.
All 66 identities and original cutouts remain required. No native validator is
called on a partial layout.

The parent capacity model has 675 cell variables and 66 constraints. Its exact
band bounds and original counts remain unchanged. No selected vertical cell
is locked in the coordinate models: all 18 coordinates range across the full
guarded short stock, with every one of the 36 physical pairs represented.

## Conditional exclusions and full coordinate checks

1. The previous fixed-profile rejection adds the exact count exclusion
   **p4=1, p5=2, p6=1, p10=1**, giving 679 variables / 75 constraints.
   A necessary allocation remains: **0/2/5/5/10/9/9/9/9**. Its independently
   checked 8,955-variable / 9,140-constraint coordinate model is INFEASIBLE.
2. Broaden that orientation family to all mirrors: one bracket from **0/4**,
   one from **2/6**, two from **3/5**, insert **10**, four cogs **9**.
   The shared-plane model has **13,267 variables / 13,605 constraints** and
   retains all **74** physical orientation modes. It is INFEASIBLE.
   Its aggregate exclusion yields a 683-variable / 84-constraint capacity
   model, which selects the balanced family with insert **8**.
3. Balanced brackets mean one each from **0/4, 2/6, 1/7, 3/5**. All mirror
   alternatives are available; distinct bracket slots are never ordered.
   Only identical cog copies are ordered by x. With insert **8**, the
   **12,367-variable / 12,674-constraint** coordinate model is INFEASIBLE.
   Five count reifications produce the 688-variable / 95-constraint master,
   which selects balanced brackets with insert **10** instead.
4. The separate horizontal-insert model has **13,242 variables / 13,578
   constraints** and is also INFEASIBLE. Together the two balanced models
   cover both allowed insert profiles. Four bracket-count reifications and
   their not-all clause exclude balanced counts independently of insert
   orientation. The final **692-variable / 104-constraint** capacity model
   returns **INFEASIBLE**.

Every extension restores its entire parent exactly, retaining earlier
coefficients, domains, family counts and exclusions. Actual solver imports
and returned models/parameters/responses are checked. Count equalities are
reified in both directions; truth-table audits include 40,000 cases for the
five-count exclusion and 10,000 for the final four-count exclusion.

The final two-case implication audit enumerates **768** bracket identity and
mirror assignments, checks all **148** modes / **72** physical pairs across
the two source models, and verifies from the parent cells that insert **8/10**
is exhaustive. Identical family copies can be relabelled into source slots;
the bracket slots have no extra ordering restriction. This conditional
argument applies only to these guarded source representations and grid.

Independent geometry reconstruction uses the original polygons and unmerged
triangle-pair hulls. The balanced vertical and horizontal cases each check
**42** collision cases from **9,184** hulls. They retain respectively **395 /
397** guarded faces and **17,914 / 17,926** exact outside planes. Both minimum
guards are **0.2126 mm**, above the required native **0.211709 mm**. No simplified
cog, missing cutout, fixed prior second-sheet pose or optional part supplies
the result. A shared-plane flag always implies its complete original plane;
each source face retains its OR and inactive-orientation literals.

## Closed calls

| Call | Result | Solver seconds | Shared seconds |
|---|---|---:|---:|
| exact_master | OPTIMAL | 0.337660 | 1.034408 |
| group_master | OPTIMAL | 0.233514 | 0.916136 |
| balanced_master | OPTIMAL | 0.290905 | 0.965625 |
| union_master | INFEASIBLE | 0.280903 | 0.953830 |
| alternate_coordinates | INFEASIBLE | 2.005099 | 2.701765 |
| group_coordinates | INFEASIBLE | 5.113386 | 5.852288 |
| balanced_coordinates | INFEASIBLE | 4.467519 | 5.198782 |
| horizontal_coordinates | INFEASIBLE | 10.487806 | 11.255589 |

All **eight** calls are closed, all have terminal responses, and all remain
inside their declared shared limits with **zero soft overruns**. Necessary
calls use at most 20 solver / 30 shared seconds; coordinate calls use at most
45 / 60. Every call uses four workers and seed zero. No retry is opened.
All **20** independent model, geometry and response audits pass.

## Remaining work and repository state

This branch now offers no surviving candidate under its tested restrictions.
It does not rule out independent cog rotations, a different composition,
continuous original layouts, or the complete target. Next screen neighboring
cogs at different angles using their full original geometry, then audit any
changed profiles and collision model. Current exclusions cannot be reused
for changed cog-angle choices. The two first-sheet brackets, full native and
material checks, production integration and full H5 matrix remain required.

At **2026-10-26T06:34:51.063611+00:00**, local HEAD and main are **88e1dc19**. The
[main CI run](https://github.com/skulitom/Nestbolt/actions/runs/40277918871)
has five passing jobs while Windows checks still run. Commit this evidence
and queue the normal push until the prior run succeeds; do not cancel it.
Upstream heads/releases, production code and the accurate READMEs are
unchanged. H2 keeps its original gate; the 22 reserved vectors stay untouched.
No new release is qualified.

[Checks](h5-aligned-profile-family-exclusions-20261026/checks.json), [closed calls](h5-aligned-profile-family-exclusions-20261026/closed-calls.json),
[scope](h5-aligned-profile-family-exclusions-20261026/scope.json), [next step](h5-aligned-profile-family-exclusions-20261026/next-step.json),
[raw manifest](h5-aligned-profile-family-exclusions-20261026/raw-manifest.json). The archive contains
489 canonical files and 463
aliases in 1 parts, all byte/SHA-256/CRC checked.
