# H5: another short-sheet exclusion and original-source readback

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight. No new release qualifies.

The short-sheet allocation of **five brackets, five inserts and two cogs** is
excluded by an independently audited necessary model and its terminal
INFEASIBLE result. The [complete frontier](h5-short12-exclusion-and-seven-part-readback-20261029/updated-allocations.json)
now retains **440 candidates**, down from 441, with 32 Pareto maxima. All 4,576
original rows and previous exclusion labels remain preserved.

A separate test of five brackets and two cogs with no inserts finds a valid
placement for the necessary model's simplified geometry. Its original contours
fail spacing and stock checks, so this second result proves neither source
feasibility nor a further exclusion. The full 66-part job and H5 remain open.

## The 12-part exclusion

The [previous checkpoint](h5-short-source-reference-exclusion-20261029.md)
excluded 5/6/2 and its containing 5/7/2 and 5/8/2 counts. The new allocation
moves insert0 to the first sheet, requiring short12=5 brackets/5 inserts/2 cogs
and first54=18 frames/7 brackets/16 inserts/13 cogs. Every original remains
accounted for exactly once.

The [model audit](h5-short12-exclusion-and-seven-part-readback-20261029/short12-model-audit.json) compares the complete protobuf
against its audited parent. All 1,876 variables and 1,071 hints are unchanged.
Exactly one of the 1,913 constraints changes: insert0's short-sheet presence
becomes zero. Every other short owner remains mandatory and movable.

The [inactive-owner proof](h5-short12-exclusion-and-seven-part-readback-20261029/short12-inactive-owner-proof.json) checks all
133 variables associated with the inactive slot and classifies all 131 touching
constraints. All five uses of its optional intervals vanish from global
geometry/capacity constraints. Twelve cross-part mode tables, with 104 rows,
freely extend every legal active mode. Cross-part geometry and ordering
inequalities are guarded off. A verified local assignment satisfies the
remaining dummy constraints independently of active positions. Consequently,
retaining the bookkeeping slot does not restrict any source-feasible short12
layout.

The positive source-derived 11-part control fails only its missing mandatory
cog0 requirement. Disabling exactly that requirement makes every constraint
pass. The negative 12-part control fails 93 constraints. The insert capacity
peaks at two and five respectively.

The [response and source-scope audit](h5-short12-exclusion-and-seven-part-readback-20261029/short12-response-audit.json)
verifies 4,911 recursive input bindings, the exact searched model, parameters,
terminal response and the source-necessity chain. Its
[argument](h5-short12-exclusion-and-seven-part-readback-20261029/short12-necessity-proof.json) retains all original legal
bracket/insert modes and arbitrary independent real cog angles. The raw runner
keeps its conservative source-exclusion flag false; this separate audit
qualifies the count exclusion only after checking the complete mapping.

The [independent frontier comparison](h5-short12-exclusion-and-seven-part-readback-20261029/frontier-audit.json) verifies that
only 5/5/2 acquires a new exclusion label. The earlier containing counts already
have preserved evidence labels. The remaining 440 candidates and 32 maxima
are independently recomputed.

## Minimum seven-part test

To test whether all remaining five-bracket/two-cog allocations could be excluded
at once, a distinct necessary model removes every short-sheet insert. Its
[preflight](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-preflight.json) requires seven short originals and
59 first-sheet originals: 18 frames, 7 brackets, 21 inserts and 13 cogs. All 66
identities remain required globally.

The [full model audit](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-model-audit.json) verifies exactly six
changed presence requirements and six corresponding hint values. All 1,876
variables and the other 1,907 constraints are unchanged. The
[inactive-owner proof](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-inactive-owner-proof.json) classifies
753 inactive variables and 740 touching constraints, checks all five global
optional-interval uses, and verifies 42 cross-part tables containing 504 rows.
Every joint dummy constraint passes on a fixed control assignment. The positive
six-part source control fails only missing cog0; the negative seven-part control
fails 47 constraints. Both have zero insert capacity consumption.

The solver returns **OPTIMAL** with one assignment. This is a satisfaction model
without an objective; the status certifies a satisfying necessary-model
assignment, not optimal source packing. The [response audit](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-response-audit.json)
re-evaluates every model constraint and all seven active/six inactive owners.
No further allocation is excluded.

The source candidate reader executes and rejects the
[saved placement](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-core-placement.json). The five original
brackets have four failing pair gaps and four failing stock guards. The full
seven-part baseline, using 7-degree cog phases, has five pair failures and
five stock failures. Because the fixed bracket anchors already fail, changing
only cog angles cannot repair this candidate; the declared phase loop is not
run. No anchor repair or solver retry occurs.

A separate [source audit](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-source-audit.json) reconstructs all
seven original transformations, checking bracket quarter turns/mirrors and
the rational cog center independently of the candidate decoder. It then
replays all original contours, 17 cutouts and 2,230 hole vertices and reproduces
the [failure details](h5-short12-exclusion-and-seven-part-readback-20261029/minimum7-source-failures.json) exactly. This
confirms rejection of this candidate, without claiming that other positions
or cog angles are impossible.

## Closed calls

| Quantity | Short12, 5/5/2 | Minimum7, 5/0/2 |
|---|---:|---:|
| Search begins | 0.63 s | 0.54 s |
| Allocated solve time | 56.334056900 s | 56.314653500 s |
| Returned solve time | 2.236875600 s | 1.784775500 s |
| Algorithm time | 2.908464400 s | 2.789167800 s |
| Shared time | 2.961609500 s | 2.858293300 s |
| Returned response branches | 58,689 | 54,503 |
| Returned response conflicts | 2,438 | 707 |
| Status | INFEASIBLE | OPTIMAL |
| Assignments / source checks | 0 / 0 | 1 / 1 |

Both distinct calls use four workers and seed zero, with the declared
three-second source-validation reserve. Both are closed within their 60-second
algorithm and 90-second shared budgets, without any allocated-solve or overall
overrun. Neither is retried, reseeded or extended. There are no native calls,
new source-valid seven/twelve-part placements or complete source66 layouts.
The established valid64 layout remains byte-identical.

## Next allocation and publication

The [next inventory](h5-short12-exclusion-and-seven-part-readback-20261029/next-short11-inventory.json) requires **short11=
5 brackets/4 inserts/2 cogs** and **first55=18 frames/7 brackets/17 inserts/
13 cogs**. Insert0 and insert2 move to the first sheet. The
[preflight](h5-short12-exclusion-and-seven-part-readback-20261029/next-short11-preflight.json) accounts for all 66 originals;
its positive ten-part source control lacks only cog0, and its negative
eleven-part control has 55 pair failures and no stock failure. No model or
search for this allocation has opened. The [next-step record](h5-short12-exclusion-and-seven-part-readback-20261029/next-step.json)
requires a fresh model audit and preserves every closed call.

Main remains **3e33dedb** at the captured publication review. All six jobs in
[CI 40800774981](https://github.com/skulitom/Nestbolt/actions/runs/40800774981)
now pass; the [job snapshot](h5-short12-exclusion-and-seven-part-readback-20261029/main-ci-snapshot.json) preserves the result.
The preceding f96cf8a2 checkpoint is committed locally. After this evidence
commit, both checkpoints can be pushed normally together, subject to a fresh
remote-head/live-run check. No running check is cancelled.

The [publication review](h5-short12-exclusion-and-seven-part-readback-20261029/publication-review.json) confirms unchanged
production source, all three READMEs, upstream heads/releases and Nestbolt
stable v0.1.0 / preview v0.2.0-alpha.1. H2 retains its original gate and all 22
reserved vectors remain unopened. Full original/native/material validation,
production integration and the complete H5 quality matrix remain required.

The [manifest](h5-short12-exclusion-and-seven-part-readback-20261029/raw-manifest.json) preserves **4282 canonical files**
and **862 identical aliases** in **31164290 archive bytes**, including
both raw models and responses, proof inputs, controls, rejected original-source
placement and independent audits. Independent archive verification checks ZIP
integrity, SHA-256 hashes, aliases, source bindings, JSON and report links; its
result is saved as `archive-checks.json` beside the manifest.
