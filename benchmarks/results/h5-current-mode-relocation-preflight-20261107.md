# Current-mode relocation preflight — 2026-11-07

The broader source neighborhood now explicitly tests relocations in every
owner's current physical mode, including all fifteen cogs. Its selected
initializer combines an insert mode change with a cog relocation. Complete
independent source and ranking checks pass, but **no new optimizer has run and
no valid full66 packing is established**. H2/H5 remain open at **60% completed
milestone weight**.

## Complete source and key coverage

[Full score reconstruction](h5-current-mode-relocation-preflight-20261107/selection-replay.json) checks **9,102 nominal
centers** across **111 physical owner-mode choices**, plus **5,911 complete
current/single/joint proposals**: **15,013 full objective scores** in total.
This adds 33 current-mode options and 2,706 nominal centers to the old pool.
All 147 representative/alias bindings, 9,051 unique centers and 51 exact center
aliases are preserved. Grid scoring retains each incoming cog angle; the model
still has fifteen continuous angular coordinates.

The raw proposals map to **2,854 complete objective/physical-mode/weight keys**.
The unchanged physical vector has 562 placement variants, each of 78 single
physical changes has 33 variants, and 2,775 two-change vectors have one variant.
The independent reader verifies a deterministic minimum for every key before
global ranking. Maximum component score error is
**1.164e-10 mm²**; maximum scalar reduction
error is 1.746e-10 mm² and the alternate
exact-rational auxiliary reconstruction differs by at most
3.638e-12 mm². All
0 differently
ordered numerical ties within the predeclared 1e-6 mm² tolerance remain recorded.

All [fourteen closed keys](h5-current-mode-relocation-preflight-20261107/closed-problems.json) remain excluded.
Four appear in this source pool, excluding **565 raw proposals**, including
all 562 variants of the closed baseline. Different coordinates cannot reopen
that identity. Raw single/joint diagnostics and every member of each key group
remain in the complete archive; no proposal is discarded before scoring.

## Original geometry and selected model

[Source-domain reconstruction](h5-current-mode-relocation-preflight-20261107/source-grid-domains.json) rebuilds every
grid placement directly from original job rings, legal transforms and cutouts.
It checks 163,836 nominal moving/fixed pairs and
36,408 stock edges against 18
same-sheet fixed originals. There are 9,051 distinct
owner/mode/center placements, 162,918 distinct fixed-pair checks,
18,841 cutouts and 2,394,464
hole vertices. Every check passes. Minimum fixed gap is
0.230002000000 mm and minimum stock extra is
0.025002000000 mm. These are finite trial checks; the
previously certified hard domains remain the continuum evidence. Mutual moving
part clearance is still unresolved. [All 33 fixed originals](h5-current-mode-relocation-preflight-20261107/fixed-source-checks.json)
are independently checked as well.

The [selected raw proposal](h5-current-mode-relocation-preflight-20261107/initial-selection.json) moves owner 17 from
physical mode 0 to 2 and relocates cog owner 28 in its existing physical mode 0.
Two coordinate replacements therefore constitute **one physical mode change**.
It is reconstructed only from the original unoptimized A/W source state, with
unchanged weights, geometry and hard domains. Its augmented score is
**209855.390168 mm²** and original overlap is
**70686.649827 mm²**; this is an invalid initializer, not
a finished layout or a comparison with optimized historical winners.

[Model readback](h5-current-mode-relocation-preflight-20261107/selected-model-controls.json) preserves 81 coordinates,
33 movers, all 528 weighted original/clearance pairs and all 15 unweighted
coefficient-1 auxiliary terms. All 111 representative owner-mode models are
also read back. The selected model's 148
directed scalar gradient terms agree within
6.750e-14 mm under the existing explicit
source-boundary/nearest-feature conventions; no global smoothness claim follows.

## Stops, preparation and next work

[Eleven deadline controls](h5-current-mode-relocation-preflight-20261107/deadline-controls.json) cover six synthetic
neighborhood interruptions, one real 0.05 s interruption and four key-grouping
interruptions. Every partial result is retained and yields no selected proposal.
The real interruption overruns its cooperative boundary by
0.011213 s, recorded
explicitly. An in-progress geometry batch or grouping stage can overrun; the
verified Windows Job supplies the outer time and 2 GiB memory limit.
[Three policy controls](h5-current-mode-relocation-preflight-20261107/policy-stop-controls.json) reject an incomplete
pool and select nothing with all keys closed or zero strict improvement.
These controls are validation only and never seed search.

[Complete preparation](h5-current-mode-relocation-preflight-20261107/preparation-process.json) takes
**9.017476 s**, including imports and output. Retaining the
entire prior 18.187213 s source lineage gives **27.204689 s**
of preparation before any new search. [The independent audit](h5-current-mode-relocation-preflight-20261107/audit-process.json)
closes in 314.221394 s. Both process trees close, with no
optimizer calls. No time allowance has been reset.

[Next](h5-current-mode-relocation-preflight-20261107/next-step.json), freeze a finite search contract for this audited
source state and the larger runtime neighborhood. The extra selection cost
must fit inside the existing preparation-inclusive 60/90 s limits and source
reserve. No new search contract is prepared. All fourteen closed identities
and prior finite pipelines stay closed. Four earlier arrangements and all
440 allocation candidates remain; no native call, exclusion or H5 credit follows.

[Main CI at review](h5-current-mode-relocation-preflight-20261107/main-ci-at-review.json) has 5 passed jobs and
1 live jobs on a69021b6. This checkpoint and 85d36097 await the ordinary
push gate. Product code, README claims and releases remain unchanged.

[Archive verification](h5-current-mode-relocation-preflight-20261107/archive-checks.json), [manifest](h5-current-mode-relocation-preflight-20261107/raw-manifest.json),
[source bindings](h5-current-mode-relocation-preflight-20261107/source-bindings.json), [historical references](h5-current-mode-relocation-preflight-20261107/external-evidence.json)
and [runtime pins](h5-current-mode-relocation-preflight-20261107/runtime-bindings.json) retain the complete evidence.
