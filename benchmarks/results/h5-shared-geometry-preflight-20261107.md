# Shared geometry selector preflight — 2026-11-07

The separate selector reuses identical center geometry and raw intersection rows
inside **one unchanged invocation**. Complete outputs match the independently
audited references exactly. It has made **no optimizer call** and supplies no new
packing result. H2/H5 remain open at **60% completed milestone weight**; the last
construction still has 51 failing source pairs.

The cache key retains the exact family, nominal mode, angle and center float bit
patterns. Raw arrays are read-only. Each owner receives a copied row before its own
self-intersection column is zeroed; owner-dependent auxiliary calculations remain
unchanged. Deep-copied input/context snapshots and public result isolation remain.
There is no cache shared between invocations or changed runtime contexts.

[Complete equivalence](h5-shared-geometry-preflight-20261107/complete-tier-controls.json) covers all 5,911 primary
and 23,419 extended proposals in the original-source and earlier closed-runtime
contexts, plus all 5,911 primary proposals in the latest closed runtime. The latest
runtime's unmeasured full extension is not claimed independently audited here.
All 2,854 key minima, raw scores, 9,102 center trials, 111 physical mode choices,
aliases, ranks, exclusion fields and canonical sequence IDs match. Independent
score references cover **80,055 center/proposal scores** across the declared scopes.

[Constructor observation](h5-shared-geometry-preflight-20261107/geometry-reuse-controls.json) confirms the new
implementation builds exactly **2,342** distinct center geometries in the latest
runtime context, matching keys reconstructed from the 9,102 recorded trials.
The corresponding old calculation has 9,066 unique owner/mode centers. No constructor
instrumentation is used in timed calls. [Three changed-context controls](h5-shared-geometry-preflight-20261107/changed-context-controls.json)
vary coordinates/angle, weights and nominal mode in successive invocations; every
primary field still matches the original implementation.

[All twenty-one closures](h5-shared-geometry-preflight-20261107/twenty-one-key-control.json) remain excluded.
[Twenty-six synthetic and three real deadlines](h5-shared-geometry-preflight-20261107/deadline-controls.json) cover
cached/uncached primary and extension phases. An incomplete primary selects nothing;
an incomplete or ungrouped extension retains only the completed primary choice.
[Two different-best cases](h5-shared-geometry-preflight-20261107/different-best-fallback-controls.json) confirm
that a better partial-extension proposal cannot displace that primary choice.
[Snapshot and one-shot controls](h5-shared-geometry-preflight-20261107/snapshot-isolation-controls.json),
[six stale-cache rejections](h5-shared-geometry-preflight-20261107/stale-cache-controls.json) and
[membership/no-candidate policies](h5-shared-geometry-preflight-20261107/policy-controls.json) pass.

[Full selector plus grouping times](h5-shared-geometry-preflight-20261107/timings.json), in seconds:

| Context | Tier | Previous mean | Shared-row mean | Observed saving |
| --- | --- | ---: | ---: | ---: |
| source | primary | 8.750221 | 3.294461 | 5.455760 |
| source | extended | 8.640768 | 3.842568 | 4.798200 |
| runtime | primary | 6.586070 | 3.778391 | 2.807679 |
| runtime | extended | 8.120988 | 5.046955 | 3.074032 |
| latest_runtime | primary | 6.653476 | 3.738968 | 2.914508 |

Each row uses the fixed old/shared/shared/old order, with two samples per variant.
Input/context/public copies, cache creation, complete geometry/scoring and grouping
are timed. Output serialization and source/model verification remain outside these
measurements. The observations do not establish stable runtime or statistical
significance. The [bounded preflight](h5-shared-geometry-preflight-20261107/preflight-process.json) closes normally
in 255.340683 s, with peak committed memory
383,586,304 bytes under its 600 s / 2 GiB cap.

[Next](h5-shared-geometry-preflight-20261107/next-step.json), prepare and independently validate an original-source
initializer under all twenty-one closed keys, charging the retained 37.680691 s plus
every new preparation cost. Assess actual preparation/output/model/source costs
before freezing a fresh finite contract. No initializer, search contract, native
call or allocation exclusion is prepared here. Four arrangements and all 440
allocation candidates remain unresolved.

The two preceding tier checkpoints reached main **ddf2310d** after all six preceding
CI checks passed, preserving 52 protected files. [The receipt](h5-shared-geometry-preflight-20261107/prior-main-push-receipt.json)
and [current CI snapshot](h5-shared-geometry-preflight-20261107/main-ci-at-review.json) are retained
(0 passed, 6 live at review). Product code, README and releases remain
unchanged. This evidence checkpoint awaits the next ordinary push gate.

[Archive checks](h5-shared-geometry-preflight-20261107/archive-checks.json), [manifest](h5-shared-geometry-preflight-20261107/raw-manifest.json),
[source bindings](h5-shared-geometry-preflight-20261107/source-bindings.json), [historical references](h5-shared-geometry-preflight-20261107/external-evidence.json)
and [runtime pins](h5-shared-geometry-preflight-20261107/runtime-bindings.json) retain the evidence graph.
