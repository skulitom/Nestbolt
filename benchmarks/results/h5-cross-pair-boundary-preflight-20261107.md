# Cross-pair boundary preflight — 2026-11-07

Batching exact boundary integration across active part pairs passes the frozen
numerical controls. On four fixed validation cases the research evaluator is
**1.4252–1.5082× faster** by median time. No placement search runs, no source
candidate changes, and no closed call resumes. This is a kernel measurement,
not a packing-quality result. H2/H5 remain open at **60% completed milestone weight**.

## Same geometry with explicit interaction mappings

The previous evaluator vectorizes edges within each directed pair. The new
research module concatenates edges across all active directed pairs at each
original/clearance geometry level. Each clipped leaf retains its explicit
source edge, interaction group, owner, pivot and pair coefficient. It retains
the exact straight-segment integral, zero contribution from points and
degenerate edges, and the shared-boundary half convention. That convention
does not turn a contact into a unique smooth derivative.

[The numerical audit](h5-cross-pair-boundary-preflight-20261107/numerical-audit.json) compares **842 directed
interactions** against both the scalar integral and the preceding vector
implementation. Independent source-ring transforms and weighted accumulation
check **405 owner coordinates** across five frozen cases, including all
coefficients set to 64. Scores, pair losses and detail fields agree. Maximum
scalar discrepancies are **1.274e-11** per directed integral and **1.819e-12**
in the assembled weighted gradient.

[Nine polygon controls](h5-cross-pair-boundary-preflight-20261107/synthetic-controls.json) cover disjoint and
point contacts, shared sides, identical outlines, both containment directions,
partial and multipart clipping, variable vertex counts and a repeated vertex.
Three additional controls cover empty and mixed-empty batches.
[Eight explicit edge origins](h5-cross-pair-boundary-preflight-20261107/collection-controls.json) exercise
empty, point, line, multiline and nested collection leaves with nonconsecutive
groups, an empty group, distinct pivots, a degenerate edge and two input orders.

[Central differences](h5-cross-pair-boundary-preflight-20261107/central-summary.json) check **810 samples**:
all 81 coordinates, at two frozen steps, for each of five deterministic
interior validation points. The prior tolerance remains
`0.02 + 3e-6 × |analytic derivative|`. The largest absolute discrepancy is
0.005094 in the all64 coefficient control. No point or tolerance is changed
after observing a result. These points are verification-only.

## Frozen paired timings

[The protocol](h5-cross-pair-boundary-preflight-20261107/frozen-plan.json) fixes cases, tolerances, two warmups
per implementation, ten samples per implementation and alternating order
before execution. Both implementations use the same models and coordinates
under CCD1 (logical CPUs 16–31), with BLAS/OMP/MKL threads fixed to one.
Every measured result is checked for numerical agreement and input immutability.

| Frozen validation case | Previous median | Batched median | Ratio |
|---|---:|---:|---:|
| Unoptimized weighted initializer | 43.578 ms | 28.893 ms | 1.5082× |
| Epoch1 weighted winner | 80.594 ms | 56.548 ms | 1.4252× |
| Epoch3 weighted winner | 85.897 ms | 60.168 ms | 1.4276× |
| Epoch3 unweighted winner | 85.456 ms | 59.852 ms | 1.4278× |

[All medians and ranges](h5-cross-pair-boundary-preflight-20261107/timing-summary.json) are reconstructed from
the 80 raw timing records preserved in the archive. The maximum-weight case
is a numerical control only. No optimizer throughput or end-to-end production
speedup is inferred from these four research measurements.

## Preserved affinity-check failure

The [first audit process](h5-cross-pair-boundary-preflight-20261107/preserved-failed-process.json) stops before
geometry or timing because an untyped ctypes call truncates the Windows
pseudo process handle. [A separate diagnostic](h5-cross-pair-boundary-preflight-20261107/affinity-abi-diagnostic.json)
reproduces error 6 and verifies that explicit HANDLE/pointer signatures read
the expected CCD1 affinity. Versioned audit and timing files change only
that observation and output destinations; original files, frozen cases,
kernels, tolerances and failed output remain preserved.

The failed wrapper takes 0.267324s; the [passing two-stage wrapper](h5-cross-pair-boundary-preflight-20261107/passing-process.json)
takes 34.325079s, including 27.632215s for the audit and 6.685359s for timing.
All three stage jobs close, with no active processes, deadline overrun or
memory-limit breach. These are validation-only times, not a new placement
preparation. [Checkpoint readback](h5-cross-pair-boundary-preflight-20261107/checkpoint-audit.json) independently
reconciles corrections, controls, medians, immutable sources and closure.
[Runtime bindings](h5-cross-pair-boundary-preflight-20261107/runtime-bindings.json) pin 12 files; the
[runtime note](h5-cross-pair-boundary-preflight-20261107/runtime-note.json) explicitly distinguishes seven
preflight pins from five supplementary DLL hashes recorded afterward.

## Next selection preflight and repository state

[The next proposal](h5-cross-pair-boundary-preflight-20261107/next-step.json) assesses simultaneous two-owner
physical-mode changes under the exact weights. The closed weighted pipeline
scored single-owner changes. Before any new search, independently enumerate
and score joint alternatives from the unoptimized source initializer, preserve
every closed coefficient/mode problem and require an improvement over the
best admissible single move. A later pipeline would need its own finite
contract and complete preparation accounting. No selector or successor call
exists here; a faster evaluator alone cannot reopen any closed call.

The preceding weighted result remains invalid: 49 original pair failures and
28,207.754973 mm² overlap. Four earlier fixed arrangements and 440 allocations
remain unresolved. No native call, allocation exclusion or release follows.
Main remains d8aa6a90; [four CI jobs pass and two native jobs run at review](h5-cross-pair-boundary-preflight-20261107/main-ci-at-review.json).
The preceding 0af0c522 checkpoint and this checkpoint await the ordinary push
gate. Product code and README claims are unchanged.

[Archive verification](h5-cross-pair-boundary-preflight-20261107/archive-checks.json),
[manifest](h5-cross-pair-boundary-preflight-20261107/raw-manifest.json),
[historical evidence references](h5-cross-pair-boundary-preflight-20261107/external-evidence.json) and
[source bindings](h5-cross-pair-boundary-preflight-20261107/source-bindings.json) preserve the complete record.

The original archive checker stopped at the link to its own not-yet-written result.
[The versioned correction](h5-cross-pair-boundary-preflight-20261107/archive-verifier-correction.json)
checks that one link after writing and reading back the result; every other
link remains checked beforehand. The original checker stays in the archive,
and [the corrected checker](h5-cross-pair-boundary-preflight-20261107/verify-archive-v2.py) is preserved alongside it.
No numerical audit or timing is repeated.
