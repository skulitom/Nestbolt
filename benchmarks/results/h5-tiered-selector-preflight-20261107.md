# Complete tier selector preflight — 2026-11-07

The validation-only selector finishes a complete **5,911-proposal primary tier**
before optionally evaluating the remaining **17,508 proposals**. Both tiers cover
all **2,854 objective/physical-mode/weight keys**. The complete source and closed-runtime
outputs reproduce the previously independently checked references exactly.
This establishes selection behavior, not a valid packing. H2/H5 remain open at
**60% completed milestone weight**. The last search still has 55 source-pair failures.

[Complete membership and score controls](h5-tiered-selector-preflight-20261107/complete-tier-controls.json) bind
both contexts to prior independent evidence for 65,042 center/proposal scores.
Every primary and extended key minimum is reconstructed against the independent
proposal scores; numerical ties within 1e-6 mm² remain recorded. The primary tier
uses each owner's best source-grid center with canonical sequence gaps; the full
tier restores the original ordered pool. Source centers, objectives and exclusions
are unchanged. [All nineteen closed keys](h5-tiered-selector-preflight-20261107/nineteen-key-control.json) remain excluded.

[Deadline controls](h5-tiered-selector-preflight-20261107/deadline-controls.json) cover **26 synthetic boundaries**
across cached and uncached paths, **two real primary deadlines** and **one real
extension deadline**. An incomplete primary has no selected candidate. An incomplete
or ungrouped extension retains its evidence but returns only the fully grouped
primary result. [Different-best controls](h5-tiered-selector-preflight-20261107/different-best-fallback-controls.json)
restrict eligibility for validation so the complete extension selects proposal 22625
instead of primary proposal 22619. Even after the better proposal appears in the
partial extension, and at the final full-grouping checkpoint, fallback still selects
22619. These artificial eligibility restrictions never become search exclusions.

[Isolation controls](h5-tiered-selector-preflight-20261107/snapshot-isolation-controls.json) mutate caller inputs,
source-cache contents and public result views after primary completion; the private
extension still matches its original reference. An extension can be attempted only
once, including after interruption. [Six stale-cache cases](h5-tiered-selector-preflight-20261107/stale-cache-controls.json)
are rejected. [Policy controls](h5-tiered-selector-preflight-20261107/policy-controls.json) reject missing/reordered
members and a mixed-tier prefix, and select nothing for all-closed or zero-margin pools.

[Measured selector plus grouping times](h5-tiered-selector-preflight-20261107/timings.json), in seconds:

| Context | Previous full mean | Primary mean | Primary plus extension |
| --- | ---: | ---: | ---: |
| source | 11.261713 | 17.645907 | 10.463463 |
| runtime | 10.916747 | 7.196888 | 7.858627 |

The fixed order is old full, primary, extended, primary, old full for each context.
Each compared mean has only two samples; the extended result has one. All new input
and public snapshot copies are timed. Serialization, source validation and model
preparation are outside these measurements. Timing variability prevents a stable
budget or significance claim. The [bounded preflight process](h5-tiered-selector-preflight-20261107/preflight-process.json)
closes in 301.291082 s with peak committed memory
378,568,704 bytes under its 600 s / 2 GiB limits.

[Separate phase profiling](h5-tiered-selector-preflight-20261107/cost-profile.json) makes three validation-only
calls: uncached source, cached source and uncached closed-runtime. Every primary
record, minimum and choice still matches the independent preflight. The runtime
primary takes 6.567979 s
(6.406250 process CPU seconds): center geometry and ranking consume
5.456954 s,
proposal scoring 0.735820 s,
public snapshots 0.308626 s,
and grouping 0.014136 s.
Complete raw/minimum/group/center output serialization adds
0.652793 s, with separate JSON readback
0.243599 s. Cached original-source
selection takes 1.259215 s before
0.634785 s serialization. These single
observations identify the dominant measured cost; they do not explain earlier
outliers or establish stable runtime. Model preparation and original-source geometry
validation are not measured here. [The profiling process](h5-tiered-selector-preflight-20261107/cost-profile-process.json)
closes normally in 17.513088 s, peak committed memory
125,808,640 bytes.

[Next](h5-tiered-selector-preflight-20261107/next-step.json), prepare and independently validate an original-source
primary-tier initializer under all nineteen closed keys, then assess its actual
cost and model/source/output costs before freezing a search contract. The retained
original-source preparation charge remains
36.028144 s plus new work. No optimizer call, initializer, search contract, native
call or allocation exclusion follows this validation. Four arrangements and all
440 allocation candidates remain unresolved.

The preceding checkpoint reached main **831ad47e** through an ordinary atomic
push after all six prior checks passed, preserving 52 protected files.
[The receipt](h5-tiered-selector-preflight-20261107/prior-main-push-receipt.json) and [current CI snapshot](h5-tiered-selector-preflight-20261107/main-ci-at-review.json)
are retained (3 passed, 3 live at review). Product code, README claims
and releases remain unchanged. This checkpoint awaits the next ordinary push gate.

[Archive verification](h5-tiered-selector-preflight-20261107/archive-checks.json), [raw manifest](h5-tiered-selector-preflight-20261107/raw-manifest.json),
[source bindings](h5-tiered-selector-preflight-20261107/source-bindings.json), [historical evidence](h5-tiered-selector-preflight-20261107/external-evidence.json)
and [runtime pins](h5-tiered-selector-preflight-20261107/runtime-bindings.json) retain the complete evidence graph.
