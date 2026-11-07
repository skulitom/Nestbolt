# Runtime profile and direct four-row source — 2026-11-07

The complete time ledger now reconciles, and the current boundary kernel remains
the measured choice. A batched bulk variant is still slower. A new direct
four-row source construction has **39 failing pairs**, including **10 cog/cog
overlaps**, and worsens the original source objective. It supplies no valid
layout or optimizer opportunity. H2/H5 remain open at **60% completed weight**.

[The closed-run ledger](h5-runtime-profile-and-four-row-source-20261107/closed-time-ledger.json) partitions all eleven
recorded intervals with zero sum error. Source preparation is **40.438637 s**;
post-preparation algorithm work is **14.013596 s**, comprising **7.650560 s**
inside the two optimizer calls and **6.363036 s** elsewhere. The second epoch's
weight/selection/output/model interval is **4.493695 s**. The 54-second reserve
is not fresh optimizer budget. Some historical markers combine multiple tasks;
their untimed subcomponents are explicitly left unresolved.

[Complete saved-evaluation replay](h5-runtime-profile-and-four-row-source-20261107/runtime-profile.json) checks all
**120 records twice**, including **19,440 scalar gradient coordinates**, with
exact score/gradient equality. [Controls](h5-runtime-profile-and-four-row-source-20261107/replay-controls.json) and
[timings](h5-runtime-profile-and-four-row-source-20261107/replay-timings.json) retain both unprofiled and instrumented
passes. They are diagnostic replays, not resumed solver calls. Observed timing
variation is preserved; profiler timings do not replace the actual search time.

[Independent binary-profile readback](h5-runtime-profile-and-four-row-source-20261107/profile-and-ledger-controls.json)
verifies all 282 function records. Intersections account for
**71.61% /
73.22%**
of exclusive instrumented time in the two epochs. Nested cumulative times are
not added. [The full profiles](h5-runtime-profile-and-four-row-source-20261107/profiles.json) retain the attribution.

This evidence motivated batching component correspondence in the rejected bulk
pilot. The new version also falls back for multiple components on one source
edge, preserving the existing component order. [All 20 controls](h5-runtime-profile-and-four-row-source-20261107/batched-pilot-controls.json)
match gradients, counts and shared lengths exactly. Of 566 directed pairs,
338 take the bulk path and 228 fall back (62 shared, 166 ambiguous/split-edge).
[Complete-kernel timing](h5-runtime-profile-and-four-row-source-20261107/batched-pilot-timings.json) has old/pilot means
**0.107552 / 0.190514 s**:
the pilot takes **1.771 times** as long in these fixed
observations. [It is rejected](h5-runtime-profile-and-four-row-source-20261107/batched-pilot-decision.json), and no full
replacement objective is built. Finite exact agreement is not global equivalence.

[The new source construction](h5-runtime-profile-and-four-row-source-20261107/four-row-source-plan.json) directly derives
one 4/4/4/3 arrangement from original unoptimized A/W data. Horizontal pitch is
two sevenths of the source center-domain width; vertical pitch is one third of
its height. Rows alternate half-pitch offsets, omitting the upper-right slot.
[Exact rational centers](h5-runtime-profile-and-four-row-source-20261107/four-row-centers.json) undergo one final float
conversion. All non-cog coordinates, 15 source angles, modes, weights and fixed
33 rows remain unchanged. There is no coordinate or angle sweep.

[Independent source/model checks](h5-runtime-profile-and-four-row-source-20261107/four-row-source-controls.json) verify
all 15 rational centers, all 81 scalar gradients, 66 original identities, 1,380
same-sheet pairs and 264 stock edges. Maximum independent gradient error is
**5.684e-14**. [Full source checks](h5-runtime-profile-and-four-row-source-20261107/four-row-source-checks.json)
have no stock failures but **39 pair failures**. Even the fixed33-plus-cog15
[48-part partial](h5-runtime-profile-and-four-row-source-20261107/partial48-source-checks.json) is invalid: the ten
[diagonal cog contacts](h5-runtime-profile-and-four-row-source-20261107/cog-contact-failures.json) overlap by approximately
**6.527023 mm²** each.

The fresh objective is **334586.901596 mm²**, compared with
**244577.060782 mm²** for original A/W, so this is
not a strict source improvement. [Its source state](h5-runtime-profile-and-four-row-source-20261107/four-row-source-state.json)
also has an already-closed mathematical key. Changing centers does not permit
another call. The historical source-score cache explicitly rejects this changed
context; old neighbor scores cannot be reused.

The complete [source preparation process](h5-runtime-profile-and-four-row-source-20261107/four-row-source-preparation-process.json)
costs **0.495311 s**. If consumed, the retained source
lineage totals **40.933948 s** before
new work. [Profiling](h5-runtime-profile-and-four-row-source-20261107/screened-runtime-profile-process.json),
[pilot](h5-runtime-profile-and-four-row-source-20261107/batched-guarded-pilot-process.json) and
[independent audit](h5-runtime-profile-and-four-row-source-20261107/runtime-and-four-row-audit-process.json) all close under
the fixed CCD1/one-thread/2 GiB controls. [The audit](h5-runtime-profile-and-four-row-source-20261107/independent-audit.json)
records zero optimizer calls and preserves every failure.

[Next](h5-runtime-profile-and-four-row-source-20261107/next-step.json), inspect the actual diagonal support/contact
geometry before any source-phase construction. No search contract is prepared;
[all 25 keys](h5-runtime-profile-and-four-row-source-20261107/closed-problems.json) stay closed. Four fixed arrangements
and all 440 allocations remain. The original full66/native/material and H5 matrix
requirements remain unmet. Main b4e16c74 has 5 passed / 1 live jobs in
[the CI snapshot](h5-runtime-profile-and-four-row-source-20261107/main-ci-at-review.json); no live run is cancelled.

[Archive checks](h5-runtime-profile-and-four-row-source-20261107/archive-checks.json), [raw manifest](h5-runtime-profile-and-four-row-source-20261107/raw-manifest.json),
[source bindings](h5-runtime-profile-and-four-row-source-20261107/source-bindings.json), [historical references](h5-runtime-profile-and-four-row-source-20261107/external-evidence.json)
and [runtime pins](h5-runtime-profile-and-four-row-source-20261107/runtime-bindings.json) retain the consumed evidence.
