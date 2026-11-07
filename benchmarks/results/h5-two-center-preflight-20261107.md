# Two-center source preflight — 2026-11-07

The source neighborhood now retains two distinct centers for every physical
owner/orientation and scores all their single/joint combinations. Complete
independent checks pass for **23,419 raw proposals**, **2,854 problem-key minima**
and the selected source initializer. **No optimizer has run and no valid full66
packing is established.** H2/H5 remain open at **60% completed milestone weight**.

## Complete source and key coverage

[Score reconstruction](h5-two-center-preflight-20261107/selection-replay.json) independently rebuilds all
**9,102 nominal center scores** and **23,419 complete proposal scores**:
**32,521 full original/clearance/auxiliary scores**. Every one of 111 physical
owner-mode choices retains its first two distinct centers in the unchanged
score/XY/local-index order. All 147 representative/alias bindings, 9,051 unique
owner-mode centers and 51 exact coordinate aliases are retained. The same
9×9 grid plus clamped control, geometry, domains, original weights and
incoming cog angles are used; all fifteen angles remain continuous in the model.

Raw coverage is one baseline, 222 single replacements and 23,196 joint
replacements. Each joint replaces its mutual pair exactly once. Grouping by
the existing complete objective/physical-mode/weight identity yields 2,854 keys:
the baseline has 2,179 raw members, 78 single-physical-change keys have 130 each,
and 2,775 two-physical-change keys have four each. Independent readback checks
both center ranks, every raw combination and every key minimum. Maximum
component score error is 1.164e-10 mm²;
6 numerical ranking
differences within the frozen 1e-6 mm² tolerance remain explicit.

All [sixteen closed identities](h5-two-center-preflight-20261107/closed-problems.json) stay excluded.
Five occur in this source pool and exclude **2,321 raw proposals**. Multiple
coordinate choices do not authorize another call on a closed identity.

[Coverage comparison](h5-two-center-preflight-20261107/coverage-audit.json) reconciles every old one-center
proposal with its identical placement in the expanded pool, using independent
scores and the same sixteen exclusions. There are 17,508 additional raw
proposals. Key minima strictly improve in **481** cases,
including **481 eligible keys**; the maximum
independently verified decrease is 113513.913176 mm².
The best eligible starting placement is unchanged from the one-center pool when both use the same sixteen exclusions.
The accepted centers have zero-based individual ranks
**[0, 0]**. A broader pool alone is not a
packing improvement, and none is claimed here.

## Source cache, geometry and selected model

The original 9,102-trial table is reused only with exact source hashes and the
full **27.204689 s** of prior preparation retained. The cache context binds
the complete library, modes, coordinates, weights, objective identity and
auxiliary regions. [Cache controls](h5-two-center-preflight-20261107/cache-controls.json) reject changes
in all six categories. A complete uncached calculation reproduces the cached
construction exactly, including every center, raw proposal and selection;
this validation-only calculation takes 9.188667 s.
Runtime states with different coordinates or weights cannot reuse the source cache.

[Inherited original-source domain controls](h5-two-center-preflight-20261107/inherited-source-domains.json)
are bound to the identical table and original state. They retain all 163,836
nominal fixed-pair checks, 36,408 stock edges, 18,841 cutouts and 2,394,464 hole
vertices, plus all 33 fixed originals. The full source-domain certificate is
unchanged. New readback verifies **222 owner/mode/center models**, membership
of both selected centers in the original trial sets and the complete selected
model. These checks do not resolve mutual moving-part clearance.

The [accepted initializer](h5-two-center-preflight-20261107/initial-selection.json) changes insert owner 16
from physical mode 1 to 0 and relocates cog owner 28 in its existing mode 0.
It comes solely from original unoptimized A/W source coordinates and weights.
Its augmented score is **211043.537474 mm²**, with
**70330.412724 mm² original overlap**. The
[complete model](h5-two-center-preflight-20261107/selected-model-controls.json) preserves 81 coordinates,
33 movers, all 528 weighted original/clearance pairs and 15 coefficient-1
auxiliary terms. Its 148 directed scalar
gradient terms agree within 6.750e-14 mm
under the existing documented boundary conventions.

## Stops, preparation and next work

[Eighteen deadline controls](h5-two-center-preflight-20261107/deadline-controls.json) check six synthetic
and one real interruption in each cached/full path, plus four key-grouping
interruptions. Every partial result remains recorded and selects no proposal.
The real cached/full cooperative overruns are respectively
0.000860/
0.142447 s. One in-progress
batch can overrun; the verified Windows Job remains the outer time/memory bound.
[Three policy controls](h5-two-center-preflight-20261107/policy-stop-controls.json) reject incomplete pools
and select nothing when all keys are closed or strict improvement is absent.

[New source preparation](h5-two-center-preflight-20261107/preparation-process.json) takes **6.564773 s**,
including imports, cache validation and output. The retained total is now
**33.769462 s**. [Independent validation](h5-two-center-preflight-20261107/audit-process.json)
closes in 685.332146 s. All processes close with zero optimizer
calls. A [generator replacement-order failure](h5-two-center-preflight-20261107/generator-correction.json)
was preserved and corrected before any source preparation opened; it created
no prepared files and consumed no optimizer attempt.

[Next](h5-two-center-preflight-20261107/next-step.json), freeze a finite search contract using this source
state, the actual full-selector cost and the existing preparation-inclusive
60/90 s limits with a source reserve. The faster source cache does not estimate
the cost of changed runtime states. No search contract is prepared. All sixteen
identities and prior finite pipelines stay closed; no historical optimized
winner or validation state may seed a successor. Four earlier arrangements
and 440 allocations remain. No native call, exclusion or H5 credit follows.

[Main CI at review](h5-two-center-preflight-20261107/main-ci-at-review.json) on b8a14317 has 5 passed
jobs and 1 live jobs. This checkpoint and a5cba93c await the ordinary push
gate. Product code, README claims and releases remain unchanged.

[Archive verification](h5-two-center-preflight-20261107/archive-checks.json), [manifest](h5-two-center-preflight-20261107/raw-manifest.json),
[source bindings](h5-two-center-preflight-20261107/source-bindings.json), [historical references](h5-two-center-preflight-20261107/external-evidence.json)
and [runtime pins](h5-two-center-preflight-20261107/runtime-bindings.json) retain complete evidence.
