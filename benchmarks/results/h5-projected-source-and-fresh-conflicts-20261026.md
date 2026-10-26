# H5: projected source models and fresh conflicts — 2026-10-26

**Two independently audited equivalent formulations finish their bounded calls
without a complete layout. Fresh collision tables for the expanded domains
are now independently verified.** H2/H5 remain open at **60%**.

## Exact signed projections

The complete 12-mover/54-fixed model keeps every original source constraint,
all 66 required originals, 24 anchor coordinates, 538 same-sheet pair modes,
two necessary area inequalities, the fresh second-sheet cog capacity of two
and 54 advisory hints. No coordinate lock or copy-order exclusion is introduced.

For each ordered physical pair, opposite primitive normals share one signed
integer projection `z = A*(xb-xa) + B*(yb-ya)`. The **201,575** old direction
definitions become unary lower/upper thresholds over **8,185** exact projections.
This reduces their coordinate terms, including new defining equalities, from
**777,018 to 242,236**: **534,782 fewer terms**. The complete model has
**223,086 variables / 289,916 constraints**. The projection bounds are verified
independently at all **130,960** coordinate-box corners. Eliminating the new
variables restores the complete parent proto exactly; actual import/export passes.

The single new call returns **UNKNOWN** after **45.869232 solver seconds** and
**48.289739 shared seconds**. Search starts at 9.85 solver seconds; the earlier
unfactored run started at 16.54 seconds and was killed at its outer deadline.
These are individual diagnostic observations, not a performance benchmark.
No candidate is saved. The **0.869232-second solver soft-limit overshoot** is
preserved; the shared 60-second budget is honored.

## Exact unary truth channels

A second formulation retains that complete projected model and appends
**201,575** complementary unary constraints. Each auxiliary flag now equals
its threshold's truth. An independent occurrence audit verifies that every old
flag appeared only in its own positive enforcement and positive source-face
disjunctions: **304,048** such disjunctive uses. Setting flags to actual threshold
truth can only turn false flags true, so no old source disjunction becomes false.
Dropping the complements restores the entire parent; both directions preserve
physical placement feasibility. Auxiliary assignments themselves need not match.

This model has **223,086 variables / 491,491 constraints** and the same 54 hints.
Its separate call returns **UNKNOWN** after **45.687183 solver seconds** and
**48.865027 shared seconds**, with a **0.687183-second solver soft-limit overshoot**.
Search starts at 12.82 solver seconds. Its solver response reports 246,297
Booleans, versus 443,411 in the one-sided projected call. These observations
do not establish a quality or speed advantage. No full layout is found.

Both readback audits verify the actual model, complete parameter bytes, returned
response/status and timing. Each call is closed: no restart, extension or reseed.
No native validation or production qualification occurs. Offline preparation
remains outside these diagnostic search budgets and cannot count toward H5.

## Fresh expanded-domain conflict census

Rebuild every conflict bit from the **54-fixed** domains; no old fixed57 table
is reused. The complete inventory contains **164 unique query pairs**,
**9,437,545 domain pairs**, and **538 physical query-mode uses over 66 pairs**.
For each domain pair, compute the entire signed anchor-difference rectangle,
pad it outward by one micrometre and require strict containment inside an
explicitly inset raw original collision obstacle. This proves incompatibility
for all anchors in the two domains, rather than sampling a few points.

Construction checks the complete census in 9.265043 seconds and certifies
**3,948,295 conflicts**, with no pending cases. The independent audit rebuilds
all 82 raw obstacles from **9,824 unmerged triangle-pair hulls**, checks every
packed bit, domain order and trailing padding, and proves each excluded rectangle
lies inside the independently reconstructed original obstacle. Its maximum
raw-boundary discrepancy is **1.654789e-11 mm**, and every inset core retains
at least **0.0000999999865 mm** of independently checked interior margin.
All **102** source query/mutual files match committed evidence. This audit takes
13.531452 seconds.

Identical B-conflict rows compress losslessly into **1,152 unique groups**,
including zero rows. An independent integer-bit replay verifies every row
partition and Boolean implication. Across physical pairs, the nonzero groups
represent **25,189,075** conflict uses with **4,010** group auxiliaries,
**4,687** nonzero group constraints and **1,099,261** mutual-exclusion literals.
A group flag equals a sum of already mutually exclusive A-domain selectors;
its exclusion with marked B selectors expresses exactly the recorded conflicts.
An unmarked bit is not proof that the two domains admit feasible anchors.

These groups are prepared and audited but **not yet added to a search model**.
Next append them to an intact projected source model, verify all group/domain
mappings and constraints, and audit actual import before a distinct bounded
call. Every original geometry guard, mandatory part and source clause remains.
Any positive still requires all 66 original outlines/cutouts, pair/stock/material
checks and native validation, followed by production integration and the full
13-job/two-kerf matrix.

## Repository and release state

The prior checkpoint b3c2f2e0 is queued locally above main d85f2b2a. At 02:49 UTC,
[main CI 40258687459](https://github.com/skulitom/Nestbolt/actions/runs/40258687459)
has five jobs passed and Windows checks still running. Preserve that run before
a normal push. Upstream heads/releases, product source and READMEs are unchanged.
No new release is qualified. H2 retains the original gate and all 22 reserved
vectors remain untouched.

Evidence: [projection audit](h5-projected-source-and-fresh-conflicts-20261026/projected-model-audit.json),
[truth-channel audit](h5-projected-source-and-fresh-conflicts-20261026/truth-model-audit.json),
[search observations](h5-projected-source-and-fresh-conflicts-20261026/search-observations.json),
[fresh conflict audit](h5-projected-source-and-fresh-conflicts-20261026/fresh-conflict-audit.json),
[group audit](h5-projected-source-and-fresh-conflicts-20261026/conflict-groups-audit.json),
[checks](h5-projected-source-and-fresh-conflicts-20261026/checks.json) and [raw manifest](h5-projected-source-and-fresh-conflicts-20261026/raw-manifest.json).
**895** canonical files and **737**
exact-content aliases are size/SHA-256/CRC verified in **2**
independently readable archive part(s).
