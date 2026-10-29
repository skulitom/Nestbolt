# Complete and reduced first-sheet construction searches

2026-10-29. H5 development evidence for `m-mechanical-large-plates`.

Two distinct, audited first-sheet constructions are now closed without an
assignment. The complete model consumes its solve slice in presolve. Removing
144,938 independently proved redundant constraints and disabling presolve/LP
linearization reaches 89,145 branches, but still produces no placement within
the declared budget. Neither outcome proves infeasibility or excludes an
allocation. The valid short11 and valid64 remain preserved; the matching first55,
complete source/native/material checks, integration and H5 matrix remain open.
H2/H5 remain open at **60%** completion.

## Original-source region preparation

The [tall-domain audit](h5-first55-complete-and-reduced-construction-searches-20261029/tall-region-audit.json) covers 325 original mover
pairs, 95 geometry-pair templates and 3,038 expanded geometry cases. Its 6,480
cached convex regions expand to 329,644 choices. All **297,068 exact rounded-region
source-support proofs** pass, with a minimum certified gap of 0.225460638934 mm.
The initial summary inherited a constant of 55 pairs; the actual pair data and
independent audit both contain 325. That raw summary and its explicit correction
are preserved.

The [compact preparation](h5-first55-complete-and-reduced-construction-searches-20261029/compact-region-preparation.json) replaces round
inflation with a 0.226 mm half-width square, covers convex-hull exteriors using
clipped halfplanes, and triangulates only the concave pockets. Same-family
relative X domains respect the already required identical-copy X ordering.
All 26 moving originals and all 93 source-mode options remain.

This reduces the construction to **1,369 cached regions and 88,690 expanded
choices**. The [independent compact-region audit](h5-first55-complete-and-reduced-construction-searches-20261029/compact-region-audit.json)
checks every rounded region against every applicable original convex piece pair.
All **88,953 exact support proofs** pass, certifying at least
**0.225999998162 mm** of source clearance. No global free-space coverage claim is
made: these are conservative construction regions, and positive assignments
still require full original-source readback.

## Preparation failures and corrections

[The correction record](h5-first55-complete-and-reduced-construction-searches-20261029/preparation-corrections.json) preserves each
failed preparation and the distinct correction that followed it:

- A floating union lost a 17,500 mm² triangular pocket at a boundary discrepancy
  of approximately 7×10⁻¹⁵ mm. The explicit pocket, its triangle and its merged
  polygon each retain that area. Raw overlay errors remain recorded. A separate
  snapped overlay diagnostic has a maximum error of 0.000001233 mm²; neither
  overlay diagnostic substitutes for the exact per-region source-support proof.
- One region collapses after nine-decimal rounding. The corrected integer
  preparation explicitly prevents its selection with a guarded false condition.
- OR-Tools encodes that false condition as an empty `bool_or` clause. The initial
  independent reader expected only linear constraints and stopped. The corrected
  reader verifies the equivalent encoding explicitly. The model itself did not
  change. An intervening guarded runner invocation refused before creating a
  search directory; it did not open a solver call.

The [integer geometry audit](h5-first55-complete-and-reduced-construction-searches-20261029/integer-geometry-audit.json) verifies all
4,965 integer plane implications, including the disabled degenerate region,
inward micrometre stock domains and rounding bounds over the 1,500×900 mm
relative domain. The minimum inset after all rounding exceeds 0.0000001 mm.

## Complete model and sole call

The [complete model audit](h5-first55-complete-and-reduced-construction-searches-20261029/complete-model-audit.json) independently checks
all **88,835 variables and 317,577 constraints**. It preserves 93 legal source-mode
selectors, 88,690 region selectors, 186 guarded stock domains, 2,025 both-owner
mode marginals and 23 identical-copy ordering constraints. Every protobuf field
and the binary/text model agreement is verified.

The [response audit](h5-first55-complete-and-reduced-construction-searches-20261029/complete-response-audit.json) verifies 5,336 recursive
input bindings and the only call's raw response, log, parameters and timings.
The call stops after presolve with `UNKNOWN`, zero branches, zero conflicts,
zero incumbents and no assignment. Presolve leaves 88,596 variables, 236,421
constraints and 998,256 terms. No source checker or native validator is called.

## Equivalent reduced model and sole call

The [independent redundancy audit](h5-first55-complete-and-reduced-construction-searches-20261029/redundancy-implication-audit.json)
checks exact integer corner bounds for every cached plane, every source-mode
alias and 114 same-family transitive ordering paths. Selected region selectors
already imply their owners' mode-dependent stock bounds through the audited
mode marginals. These bounds imply **144,938** of the guarded region planes.

The [reduced model audit](h5-first55-complete-and-reduced-construction-searches-20261029/reduced-model-audit.json) proves that all 88,835
variables and all remaining **172,639 constraints** are unchanged. It verifies
every remapped index and every other protobuf field. The removed constraints
have independently verified implication proofs, so the reduced model is
equivalent to the audited complete construction; no part, mode or region choice
is pruned.

The reduced model's only call explicitly disables presolve and LP linearization.
It uses four workers and seed zero, as did the complete model. It reaches
**89,145 branches and 45 conflicts**, then returns `UNKNOWN` with no incumbent or
assignment. The [response audit](h5-first55-complete-and-reduced-construction-searches-20261029/reduced-response-audit.json) verifies
5,371 recursive bindings, its parameters and its absent source readback. This
call is closed; neither closed call is extended or reseeded.

| Timing, seconds | Complete model | Reduced model |
|---|---:|---:|
| Charged preparation | 36.342435 | 42.794513 |
| Allocated solve slice | 17.925214 | 11.806165 |
| Returned solve time | 18.144726 | 11.941126 |
| Preserved solve-slice overrun | 0.219511 | 0.134961 |
| Preparation-inclusive algorithm time | 56.254583 | 56.175153 |
| Preparation-inclusive shared time | 56.383286 | 56.295412 |

Both charges include the prior valid short11's **22.247810-second shared time**.
The reduced construction also charges the complete model preparation and its
own conversion. Both overall algorithm/shared totals satisfy 60/90 seconds;
the two solve-slice overruns remain explicit.

## Next construction: simultaneous cog-site selection

The [next plan](h5-first55-complete-and-reduced-construction-searches-20261029/next-step.json),
[preparation checks](h5-first55-complete-and-reduced-construction-searches-20261029/site-selection-preflight.json),
[identity inventory](h5-first55-complete-and-reduced-construction-searches-20261029/site-selection-inventory.json) and
[all 105 subsets](h5-first55-complete-and-reduced-construction-searches-20261029/all105-site-subsets.json) define a smaller construction:
choose exactly 13 of the 15 valid cog positions from the preserved valid64 first
sheet, then place all seven brackets and six inserts with their **80 legal
orthogonal source-mode options**. Every possible pair of empty cog sites remains
available simultaneously; no sequence of per-subset solver retries is planned.

The pool's 15 original cog poses and the fixed29 pass an original-source control.
Each selected cog receives one of the required identities 1–13 in deterministic
site order. All 105 subsets preserve the disjoint full66 identity partition.
One [53-part partial control](h5-first55-complete-and-reduced-construction-searches-20261029/partial53-source-checks.json), including the
valid short11, passes **916 pairs, 212 stock edges, 63 holes and 6,732 hole
vertices**. The seven brackets and six inserts are still absent from that control.
It does not replace valid64 or establish first55 feasibility.

The site-selection preflight still requires its independent audit, followed by
source-safe occupancy-guarded geometry and a complete model audit before one
bounded call. No site-selection model or search is opened. Fixed cog sites
restrict this construction; a negative result would not prove global infeasibility.

## Preservation and publication

No allocation is excluded; the authoritative frontier remains 440 candidates.
The original valid64 and the independently valid short11 retain their recorded
hashes. There are no production edits or native validator calls in this checkpoint.

[Publication review](h5-first55-complete-and-reduced-construction-searches-20261029/publication-review.json) confirms unchanged production,
READMEs, upstream heads and releases. Stable remains v0.1.0; preview remains
v0.2.0-alpha.1. At the saved snapshot, four checks on main `f81a9ccd` have passed
and both platform checks are still running in
[run 40819131061](https://github.com/skulitom/Nestbolt/actions/runs/40819131061).
A subsequent normal push requires a fresh all-six-pass result and unchanged
remote heads; no CI run is cancelled. H2 retains its original gate and all 22
reserved vectors remain unopened. No new release qualifies.

The archive contains **4667 canonical members**, **938 verified identical
aliases** and **58619773 ZIP bytes**, preserving the raw models, calls, logs,
failures, corrections, exact certificates, source controls, helpers, recursive
input bindings and previous normal-push receipt. Its verifier checks ZIP integrity,
every member and alias hash, every bound input, JSON parsing and local report links.
