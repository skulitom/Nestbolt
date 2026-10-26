# H5: rejected outer-cover candidate and complete source-clause search — 2026-10-26

**The relaxed candidate is invalid; the complete source-clause model ends
UNKNOWN.** Neither result establishes a valid 66-original target layout or
packing impossibility. All original counts, material limits and clearance
guards remain unchanged. H2/H5 remain open at **60%** completed milestone weight.

## Complete replacement and relaxed candidate

The preceding checkpoint's necessary outer cover is installed in the audited
table-free model. Remove all **21,819** old safe-cell variables and **116,237**
cell constraints, including **54 empty-cell sums** which otherwise would still
forbid their pair modes. Preserve exactly **10,255 original variables / 57,577
constraints**, all nine movable originals, 57 fixed originals, domains, counts,
areas, coordinates, capacities and proved exclusions. Add all 394 explicit
query-difference bounds and **60,671** outer-box flags. The result has
**70,926 variables / 180,101 constraints**, with 79 advisory hints.

The independent **14.469089s** audit reconstructs every removed old
cell equation from its source, inverse-verifies the retained parent fields,
checks every added box and activation, restores the exact complete parent
protobuf, and verifies the actual solver import/export. Every integer
displacement satisfying the original guarded source clauses remains available.
The relaxation is deliberately not a safety certificate.

One eight-worker, seed-zero call, capped at 45 seconds with a ten-second
shutdown reserve inside a shared 60-second budget, returns a candidate in
**16.162402s**, shared **18.195138s**.
No cap overrun occurs. All calls terminate and remain closed.

Readback verifies all nine selected identities and inward domains, copy
ordering, all 394 pair activations and 16 chosen boxes. It checks **633 full
original guarded clauses / 27,362 inequalities**. Six clauses fail for six
different original pairs. Box membership is not accepted as safe geometry.

A separate reconstruction retains all **66 original copies**, checks
**1,540 same-sheet pairs / 264 stock edges**, and reconstructs all **90 original
cutouts / 10,026 cutout vertices** under the original transforms. Maximum
profile disagreement is **5.09e-13 mm**. Both original area constraints pass;
charges are 4,051,952,616 and 429,788,154 lower-area units. Fixed-original
clearances and all stock margins pass. Six moving-original pairs fail:

| Original items | Failure |
|---|---|
| Brackets 28 / 29 | 39,799.450801 mm² filled-outline overlap |
| Bracket 28 / cog 65 | 20,458.099742 mm² filled-outline overlap |
| Bracket 29 / cog 65 | 20,324.858527 mm² filled-outline overlap |
| Insert 50 / cog 57 | 12.686744 mm² filled-outline overlap |
| Cogs 57 / 62 | 0.188978 mm gap; required guard is 0.211709 mm |
| Cogs 64 / 65 | 0.209214 mm gap; required guard is 0.211709 mm |

Filled outer polygons are intentional because part-in-hole remains off. All
internal cutouts are retained in the original library and their transformed
geometry is separately checked. The first new audit incorrectly asserted that
the original shapes had no holes and stopped immediately. Its source, plan and
failure remain preserved; the separate repaired readback removes that false
assumption and verifies the actual cutouts. No source shape, placement, model
or gate is changed by that repair. No invalid candidate is sent to the native
validator.

## Complete source-clause formulation

Replace every outer box and appended pair-cover constraint with the complete
original guarded separation clauses. Preserve the same original variable and
constraint prefix and **72 non-box hints**. For each of the 164 query cases,
derive the full signed displacement rectangle directly from original domain
bounds and evaluate every source halfplane at its four integer corners:

- A face is always satisfied only if one outside edge holds over the whole rectangle.
- An edge is removed only when it cannot hold anywhere in that rectangle.
- A face with no possible edge forbids its active pair; one live edge is imposed directly.
- Otherwise all live edges remain in its conditional OR. Identical directions are shared only within the same physical pair and query mode.

This is exactly equivalent to all original guarded source clauses inside the
recorded source domains. It adds no padding or clearance relaxation. The model
retains all **394 physical pair/mode uses**, covering **8,238 source faces**:
3,818 are proved whole-rectangle tautologies, 2 impossible faces forbid their
pair modes, 5 require one direction, and 4,413 retain full disjunctions.
The result has **167,044 variables / 376,363 constraints**, including 156,789
shared directional flags. No faster runtime is presumed from this formulation.

Preparation takes **8.681279s**. Independent audit takes
**33.171390s**, checking **103 committed source files**,
**218,048 exact corner evaluations**, every retained prefix field, every added
variable/constraint/mapping entry and all hints. Restoring verified additions
to the parent reproduces its full protobuf exactly. Actual solver parsing,
validation and export also agree. Offline preparation/auditing is explicitly
not production-budget qualification.

This differs from the previously closed 181,160-variable full-source call:
it incorporates the subsequently proved domain and regional capacity
exclusions, original copy ordering, explicit difference bounds, exact
whole-rectangle simplification and the independently verified six-cog hints.
It neither restarts nor extends that earlier call.

The new single eight-worker, seed-zero call is capped at 45 seconds, with a
ten-second shutdown reserve in a fresh shared 60-second loading, verification
and search budget. Actual model loading takes **2.070101s**,
equality/parameter verification **0.704983s**. The call
ends **UNKNOWN in 45.471545s**; shared elapsed time is
**48.583887s**. The solver exceeds its soft cap by
**0.471545s**, preserved explicitly;
the shared budget is honored. There is no incumbent, retry, continuation,
native validation or H5 quality run. UNKNOWN is not an impossibility result.

## Next investigation and repository state

Check whether the verified six-cog witness admits continuous completion by the
missing original brackets and insert across all recorded original domains.
The earlier finite pose census cannot prove that it does not. Use exact rational
clipping or independently replayable interval/branch certificates; retain
lower-dimensional cases, residual domains and caps. Any conclusion is conditional
on those six positions, source angles, fixed 57 and source integer domains, and
must never exclude a domain in a model where the cogs can move. Use that evidence
to choose which source positions or orientations to change before another full
search. Both new calls stay closed.

All H5 requirements remain: 66 original shapes, unchanged material/native
guards, a native-valid layout, production-budget integration and the complete
13-job/two-kerf matrix. H2's original gate and 22 reserved vectors remain intact.

Main 728b2db2 remains preserved. Its own
[CI 40246226212](https://github.com/skulitom/Nestbolt/actions/runs/40246226212) is **in_progress**, with **5/6** successful
jobs at this snapshot. The two preceding local checkpoints and this checkpoint
await its terminal outcome before a normal push, reconciling newer remote work
first. Production source, all three accurate READMEs, preview v0.2.0-alpha.1 and
stable Latest v0.1.0 are unchanged. No new release is qualified.

Evidence: [outer transformation](h5-bounded-source-search-20261026/outer-model-audit.json),
[candidate rejection](h5-bounded-source-search-20261026/outer-original-geometry-audit.json),
[full source-model audit](h5-bounded-source-search-20261026/source-model-audit.json),
[closed call readback](h5-bounded-source-search-20261026/source-search-audit.json),
[archive](h5-bounded-source-search-20261026/raw-001.zip) and [manifest](h5-bounded-source-search-20261026/raw-manifest.json).
All **534 canonical files / 247
exact-content aliases** have size, SHA-256 and CRC verification, retaining both
models, source files, parameters, logs, candidates, all failures and audits.
