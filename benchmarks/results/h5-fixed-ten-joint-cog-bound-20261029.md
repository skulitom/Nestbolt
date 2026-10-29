# H5: fixed-ten inventory and continuous two-part exclusion

Work: 2026-10-28 to 2026-10-29. Evidence and documentation only.
H2/H5 remain open at 60% completed milestone weight; no release qualifies.

## Outcome

The proposed 5-bracket/6-insert/2-cog short sheet cannot retain ten of the
twelve exact parent poses. All **51 distinct fixed-ten geometries and 66
identity variants** are excluded by independently audited necessary bounds.
At least three parent poses must change for this allocation. The allocation
itself, other parent layouts and the original 66-part job remain unexcluded.
The valid 64-part layout and 444 necessary allocation survivors are unchanged.

The [preceding checkpoint](h5-short-exchange-continuous-bound-20261028.md)
excluded six fixed-eleven layouts. Releasing one additional original from
each produces 66 ordered identity variants and 51 distinct geometries.
Every variant accounts for all 66 original identities exactly once: the
target short sheet has 13 parts and the mandatory first-sheet complement
has 18 frames, 7 brackets, 15 inserts and 13 cogs. The released second original
remains a required short-sheet mover.

## Fixed-ten inventory and finite construction

All 51 fixed-ten source layouts pass independent readback, including 2,295
pair checks. Exact continuous cog-core coverage excludes 44 geometries
(58 identity variants); seven geometries (eight variants) retain a necessary
core witness. The audit checks 677,760 no-fit vertex sums, 762 certificate
nodes, 396 covered leaves and 57,024 leaf-corner half-plane inequalities.
Every witness is outside all necessary obstacles; none is claimed as a
source-valid placement. See the [inventory audit](h5-fixed-ten-joint-cog-bound-20261029/inventory-audit.json).

Six remaining geometries release the existing cog as well as a bracket and
therefore need two moving cogs. The seventh releases neighboring brackets
10 and 11. Its two identity variants share the same geometry, so it receives
one finite construction, with cog 0, bracket 11 and insert 0 as movers.
The geometry-identical bracket-copy swap gets no second run.

The adjacent-bracket preparation reuses 262 byte-identical, independently
audited source-type obstacles and constructs 344 new obstacles from 92,864
convex Minkowski hulls. It recomputes all 46 fixed-ten free domains. All 36
cog modes, eight bracket modes and two insert modes have nonempty individual
regions; all 46 representative 11-part source controls pass. Preparation
takes 6.833450 s and its independent audit takes 4.997199 s.

The sole declared 60/90-second construction exhausts 335 finite cog anchors
in 0.358753 algorithm seconds and 0.658447 shared seconds. Every residual
bracket domain is empty, leaving zero joint anchors, insert candidates or
13-part checks. An independent replay confirms all 2,680 complete bracket
domain queries. There is no overrun, solver call, native call, retry or reuse
of unused time. See the [construction result](h5-fixed-ten-joint-cog-bound-20261029/construction-result.json)
and [response audit](h5-fixed-ten-joint-cog-bound-20261029/construction-audit.json).

Review found an identity-format defect in the unexercised final candidate
checker: JSON identity lists would be compared against tuple keys. The
response audit reproduces that mismatch and verifies the normalized positive
control. No candidate reached this code, and the independent empty-domain
replay confirms that it did not change this result. The frozen script is
preserved; a future distinct constructor must normalize those identities.
The [retained defect record](h5-fixed-ten-joint-cog-bound-20261029/unexercised-candidate-validator-defect.json)
prevents treating this run as broader source-search validation.

## Continuous joint bound

A separate bound removes the finite-anchor limitation. The original cog's
40-vertex convex hull contains a disk of radius **139.268 mm**, proved by
exact rational half-planes and squared edge distances. Because rectangular
stock must contain an object's convex hull, this disk supplies a necessary
cog-center stock bound at every real angle. It is used only for stock.
Collision predicates retain the smaller polygon proved inside the filled
original cog; no convex-hull fill is substituted for collision geometry.

The proof covers fourteen continuous four-variable domains: all eight legal
bracket modes for the adjacent-bracket case, plus a cog/cog domain for each
of the six other geometries. Fixed-core and relative moving-core no-fit
polygons are reconstructed from exact vertex differences. The new bracket
cores pass 96 exact source-edge checks and all eight rotation/mirror modes
are verified. Both cog rotations remain arbitrary real values.

Every certificate covers its entire root rectangle. An independent audit
checks all sixteen actual corners of every four-dimensional leaf, every
exact child partition and every node's reachability. Across the fourteen
cases it verifies 175,176 no-fit vertex sums, 860 nodes, 437 covered leaves
and 195,584 leaf-vertex half-plane inequalities. Construction takes 0.806222 s
and the independent audit 5.846797 s, within the frozen 120-second proof cap.
No node or depth limit is reached.

Positive source cog/cog and existing cog/bracket controls pass; coincident
cog centers are rejected. The [joint audit](h5-fixed-ten-joint-cog-bound-20261029/joint-bound-audit.json),
[case certificates summary](h5-fixed-ten-joint-cog-bound-20261029/joint-bound-cases.json) and
[necessity argument](h5-fixed-ten-joint-cog-bound-20261029/necessity-proof.json) explain why this closes the
seven remaining geometries, not the overall allocation or job. Together with
the single-cog proof, all 51 fixed-ten geometries and all 66 variants close.

## Publication and continuation

The previous two checkpoints reached main `6b0a1d0b` in a normal atomic
fast-forward after all six prior CI jobs passed. At this snapshot,
[CI 40789500705](https://github.com/skulitom/Nestbolt/actions/runs/40789500705)
has four successful jobs and both platform checks still running. This
checkpoint queues until the remaining jobs pass; no live run is cancelled.
Production, all three READMEs, upstream heads/releases and Nestbolt's
`v0.1.0` stable / `v0.2.0-alpha.1` preview releases are unchanged.
H2 retains its original gate and 22 unopened vector files.

Next, inventory a new construction that changes at least three parent
poses, retaining nine. Keep the original target stock, all 66 identities and
common-line PIH off. Apply the audited necessary core bounds before choosing
another bounded source construction. No fixed-nine geometry or construction
has started. Native validation still requires a complete source-valid 66.

The [raw manifest](h5-fixed-ten-joint-cog-bound-20261029/raw-manifest.json) retains 2063 canonical members,
1145 identical-content aliases and 7466673 compressed bytes, including
all recursive input bindings, source checks, closed-run logs, audit scripts,
the unused-checker defect, coverage certificates and prior push receipt.
