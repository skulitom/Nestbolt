# H5: one-cog release with all brackets and inserts — 2026-10-23

**Best checked result remains 64/66, missing two brackets.** A distinct
conditional repair model frees one cog together with every bracket and insert.
It returns `FEASIBLE` with its original 60-second allowance. It neither
improves the checked layout nor proves the finite pool optimal. The original
66-copy inventory and material target remain unchanged; H2/H5 stay open at
**60%** completed milestone weight.

## New repair model and independent checks

The preceding [coverage audit](h5-individual-frame-joint-20261023.md) supplies
30 cores from two checked layouts: each fixes 18 frames and 14 cogs. Every
core pair and all 989,670 candidate/core memberships were independently checked.
All coverage bytes match that committed manifest. The new model chooses
exactly one core and up to 12 brackets, 21 inserts and one additional cog.
A zero-cog choice remains permitted if it reaches the area floor. Original
reserved frame holes, transforms, stock limits and quantities are unchanged.

All **16,058** eligible variable poses are retained before fresh reduction.
The complete original graph is projected into this neighborhood, with every
projected row reconstructed back to original global indices. All
**17,012,982** conflicts agree. Projection, serialization and
independent row verification take 147.568384 seconds. All 30 original
64-part baselines preserve full-graph feasibility. The 572 variable count
combinations are a subset of the previously verified original-area ordering;
the variable floor is **865,862,719**, and full inventory requires
**945,862,719**.

Fresh same-family substitutions require an adjacent retained replacement,
inclusion of every original neighbor and a superset of compatible cores.
The pass completes in 8.598320 seconds and 16,033,165
comparisons within its 30-second / 50-million limits. It removes
9,417 choices and retains **6,641**.
Independent certificates enumerate 15,522,966
neighbor relationships and 172,703
core memberships. Every mapped baseline preserves quantities and score.

The reduced graph has **4,686,314** conflicts. First-fit compression
completes in 8.105149 seconds within its 20-second allowance,
yielding 12,464 cliques and **0** residual
edges. Every edge reconstructs independently. There is no extra greedy search;
all 30 mapped baselines are checked, and the first best baseline is the hint.

The final graph encoding, every binary model field and all solver parameters
are independently reconstructed. The model has **6,671** variables
(6,641 poses and 30 core choices), with
**19,041** constraints. Original family caps, conditional core
membership and the area floor are explicit. One seed-zero, eight-worker call
uses a 60-second allowance and disabled CP model presolve, following the
previous recorded diagnosis. It runs for **60.778150 wall seconds**;
the soft overrun is preserved. Search starts at 0.34 seconds, after recovering
the baseline at 0.268763 seconds. The complete worker log records active
search; zero aggregate counters do not mean search was absent.

There is one callback and a distinct final result, selecting core 7. Both
return variable area 865,862,719; the reported upper bound remains 945,862,719.
This is **not an optimality or impossibility certificate**. This completed
solve is not repeated or extended.

## Original geometry and gate status

All 3 layouts, including the starting hint,
pass independent original geometry, transform, stock and pair checks. Each
contains 18 frames, 15 cogs, 10 brackets and 21 inserts. Every layout checks
1,521 same-sheet pairs. The frozen CLI is run 2 times,
with 1 exact-layout reuse; each result fails only
the original two-bracket quantity requirement. Filled area is
4401740.784069743 mm², charged material is
4988890.203494999 mm², and minimum separation is
0.200100000000 mm. These gaps are not native-margin qualified.

No native packing, production-budget qualification, complete H5 quality matrix
or held-out evaluation occurs. The full original target, native guard,
production budget and all 13 jobs at both kerfs remain required. This evidence
does not add a completed milestone or qualify a new release. Source and all
three accurate READMEs remain unchanged; preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain current.

## Next action and repository state

Measure continuous cog placement regions for the new 32-part cores and compare them with the retained finite candidate coverage. Begin with the original wide seed's 15 cores, treating mirrored cog poses as forbidden and retaining all original rotation freedoms, stock bounds, filled frame holes and full 66-copy target. Use the checked original geometry and an explicit fresh bounded query plan, record unprocessed orientations or proposal lists, and identify genuinely new contact poses before proposing another selection model. Prioritize regions where a cog move changes available bracket space. Do not repeat or extend either completed solver call, reuse an old core's emptiness result for these new cores, claim impossibility from conservative padding, or count a partial layout as passing H5. Native margins and the original production budget/full matrix remain required after a full witness exists.

Main remains 752b1c60 after a fresh fetch with no incoming changes. Its six-job
run 39976658315 is saved as `in_progress` / `pending`.
The preceding d49d0ff6 evidence checkpoint is committed locally; pushing later
checkpoints waits for the remaining main check. No unobserved success is claimed.

Evidence: [projection](h5-one-cog-release-joint-20261023/graph.json), [reduction](h5-one-cog-release-joint-20261023/reduction.json),
[baselines](h5-one-cog-release-joint-20261023/hints.json), [encoding](h5-one-cog-release-joint-20261023/encoding.json),
[model](h5-one-cog-release-joint-20261023/model.json), [solver](h5-one-cog-release-joint-20261023/solver.json),
[original layouts](h5-one-cog-release-joint-20261023/layouts.json), [best checked layout](h5-one-cog-release-joint-20261023/best-layout.json),
[distinct final layout](h5-one-cog-release-joint-20261023/final-layout.json), [source review](h5-one-cog-release-joint-20261023/source-review.json),
raw evidence [part 1](h5-one-cog-release-joint-20261023/raw-001.zip), and [manifest](h5-one-cog-release-joint-20261023/raw-manifest.json).
All 73 canonical members and 36
aliases are byte-verified, with archive CRCs and SHA-256 hashes checked. Each
independent ZIP part is below 50 MiB, and every original path remains represented.
