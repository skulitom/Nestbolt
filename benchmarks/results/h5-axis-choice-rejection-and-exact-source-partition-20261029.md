# H5: rejected axis choices and an exact smaller source partition

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight. No new release qualifies.

The six-choice source translation model is exactly contradictory before any
solver call. Expanding to eleven choice groups removes those particular
contradictions, but the sole mixed-integer call still reports INFEASIBLE.
Neither result excludes an allocation: **all 440 candidates remain open**.
No valid eleven-part or complete 66-part layout is produced.

A separately audited exact decomposition reduces each 80-vertex cog from
80 triangles to **21 convex pieces**. The next eleven-part construction can
therefore use **56 pieces and 1,115 inter-original piece pairs**, instead of
174 pieces and 8,726 pairs. This is preparation, not a new placement or search.

## Six choices: an exact contradiction without a solver

The [previous checkpoint](h5-short11-source-readback-and-translation-cycle-20261029.md)
prepared 90 separating-axis variants for six frozen source-piece pairs.
The [full model audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/six-choice-model-audit.json) checks all 113 variables
and 8,860 rows, including 90 binary selectors, six one-of groups, 8,764 unchanged
parent rows and all 1,440 stock-domain corner checks for deactivation constants.
All 22 translations remain free; the original modes, 7-degree cog phases,
0.225 mm separation and 0.025 mm stock clearance are retained.

The [fixed-row audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/six-choice-cycle-audit.json) finds a remaining
three-edge contradiction: cog14's lower Y stock bound, bracket7's upper Y
stock bound, and retained source-pair plane 634. Exact rational left-hand
coefficients cancel, leaving a negative sum of approximately
**-11.771415650079087 mm**. The [certificate](h5-axis-choice-rejection-and-exact-source-partition-20261029/six-choice-cycle-certificate.json)
proves this restricted model infeasible regardless of its selectors.
**No solver call is made for this model.** Other orientations and separation
choices remain outside that certificate.

## Eleven choices: one closed negative call

An expansion [audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/choice-expansion-audit.json) reconstructs all 2,023
original axis-subsystem edges, verifies five exact cycles, and replaces the
implicated additional pair rows. The result has **eleven groups / 160 variants**.
An exact potential satisfies the 2,012 remaining axis-subsystem edges; this
does not establish feasibility of the full model, which also has oblique rows.

The expanded [model audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/expanded-model-audit.json) verifies all
**183 variables / 8,930 rows**, 160 binary selectors, 8,759 unchanged parent rows
and 2,560 deactivation corner checks. All eleven short-sheet and 55 first-sheet
identities are accounted for once. No first-sheet layout is constructed.

The sole declared SciPy/HiGHS call returns **INFEASIBLE in presolve**, with zero
search nodes, assignments or source-check calls. The declared node limit is 128.
The [response audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/response-audit.json) verifies 5,094 recursive input
bindings and the exact submitted model. Solving takes 0.029906800 seconds;
including 0.643073600 seconds of charged preparation, algorithm/shared totals
are **1.432447900 / 1.480626600 seconds**, with no overrun. This call is closed
and is neither retried nor extended.

HiGHS reports dropping **814 tiny coefficients**, ranging from approximately
6.09e-17 to 1.14e-15. The [warning audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/coefficient-warning.json)
preserves the warning and bounds their largest possible effect on any row
over the recorded domains at **7.776017290390362e-13 mm**. This remains a
solver-reported negative, not an exact certificate for the entire input model.

A separate [oblique-row diagnostic](h5-axis-choice-rejection-and-exact-source-partition-20261029/oblique-diagnostic.json) projects
8,715 fixed rows into 15,506 difference edges. Its cycle search finds no
negative cycle and produces no exact full-model contradiction. It takes
**70.961358700 seconds**, outside the closed solver call; it is not a successful
under-60-second algorithm result. Repeated loading of the NPZ matrix accounts
for avoidable diagnostic overhead. Its raw output and duration are preserved.

## Exact source partition for the next construction

An initial exploratory fan-merge preparation obtains 40 pieces per cog through
40 exact area-preserving merges. Its [preparation record](h5-axis-choice-rejection-and-exact-source-partition-20261029/fan-merge-preflight.json)
is preserved, with independent overlap/boundary verification still pending for
that exploratory partition. It opens no model or search.

A better [partition](h5-axis-choice-rejection-and-exact-source-partition-20261029/core-teeth-partition.json) uses the original 40 root
vertices as one convex core and the original vertices of each tooth as twenty
quadrilaterals. Every vertex is an unchanged original source vertex. The
[independent exact audit](h5-axis-choice-rejection-and-exact-source-partition-20261029/core-teeth-audit.json) verifies all 80 source
vertices, strict convexity of all 21 pieces, zero-area intersections for all
210 piece pairs, cancellation of exactly 20 internal edges, the complete
80-edge original outer boundary and exact total source area.

The full eleven-part decomposition now needs 56 convex pieces and 1,115
inter-original piece pairs. The [next-step record](h5-axis-choice-rejection-and-exact-source-partition-20261029/next-step.json)
calls for separation alternatives across every relevant pair, avoiding the
retained seed directions that restricted the failed models. The new model
must independently verify geometry coverage, clearances, domains, identities
and every constraint before one bounded call. No model or search using this
partition exists yet. A fixed-mode/phase negative cannot exclude the allocation.
Original holes remain checked in source readback; PIH stays off. First55,
complete source/native/material checks, production integration and the full
H5 matrix still remain.

## Publication and preserved evidence

[All six checks](h5-axis-choice-rejection-and-exact-source-partition-20261029/main-ci-snapshot.json) on main **9dab2f4e** have passed
in [run 40805531238](https://github.com/skulitom/Nestbolt/actions/runs/40805531238).
This clears the prior checkpoint's CI wait. Normal publication of both queued
checkpoints still requires a fresh unchanged-head and no-live-run check.

The [publication review](h5-axis-choice-rejection-and-exact-source-partition-20261029/publication-review.json) confirms unchanged
production source, all three READMEs, upstream heads/releases, stable v0.1.0
and preview v0.2.0-alpha.1. The valid 64-part layout and 440-candidate frontier
are byte-identical. H2 retains its original gate; all 22 reserved vectors remain
unopened. There are no native calls or complete source66 results.

The [manifest](h5-axis-choice-rejection-and-exact-source-partition-20261029/raw-manifest.json) preserves **4398 canonical files**
and **840 identical aliases** in **32395590 archive bytes**. Models, raw
solver logs and warnings, exact certificates, both partition preparations,
the independent 21-piece audit and recursive source inputs are retained.
Independent ZIP/hash/alias/source-binding/JSON/link verification is stored
in `archive-checks.json` alongside the manifest.
