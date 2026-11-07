# Selector computation equivalence — 2026-11-07

Two computation-only changes pass complete equivalence checks: gather pair losses
with precomputed NumPy indices, and calculate each complete problem digest once
per physical vector within a single invocation. Geometry, objectives, proposal
order, exclusions and deadline checkpoints are unchanged. **No new source state,
model or optimizer call is prepared.** H2/H5 remain open at **60% completed
milestone weight**; this is a selector implementation result, not a valid packing.

## Complete equivalence and bounded timing

[The frozen validation plan](h5-selector-equivalence-20261107/plan.json) checks the original unoptimized
source context and the already audited closed runtime context. Each uses the
fixed original/indexed/indexed/original order with full uncached geometry scoring.
All eight complete outputs are exactly equal to their independently audited
references: **9,102 centers, 23,419 proposals and 111 owner/mode selections** per
call, including every score component, key, exclusion, alias and raw coordinate.
The two references retain all **65,042 independently reconstructed scores** from
their earlier audits; equality here is checked against those exact records.

[Timing samples](h5-selector-equivalence-20261107/timings.json) measure only the complete uncached selector,
before serialization, key grouping, model readback and source checks. Both
implementations use the same CPU mask and one BLAS thread. There are only two
samples per implementation/context; no statistical significance or production
packing improvement is claimed.

| Context | Original selector (s) | Indexed selector (s) | Observed mean reduction |
| --- | ---: | ---: | ---: |
| source | 10.488474, 10.651646 | 7.541385, 7.671650 | 28.04% |
| runtime | 11.436044, 11.351386 | 10.051799, 9.310551 | 15.03% |

[A separate counted control](h5-selector-equivalence-20261107/cache-controls.json) verifies **2,854 digest
calls instead of 23,419**, while preserving every raw proposal. The cache is local
to each invocation's unchanged weights and objective identity. It does not cache
geometry and cannot carry results across calls. Pair-loss gathering retains the
exact existing 528-pair order and all sums/dot products.

[Changed-context controls](h5-selector-equivalence-20261107/key-context-controls.json) compare full original
and indexed output after changing all weights and, separately, adding an identity
discriminator. Every key changes and independently matches canonical JSON/SHA-256.
The mutated contexts are validation only. Across the four contexts, **93,676 raw
problem digests** are recomputed directly without either key helper. Repeated
calls, the original-source trial-cache path and all six stale trial-cache
rejections pass. No new optimizer identity is consumed by these controls.

[Fourteen deadline controls](h5-selector-equivalence-20261107/deadline-controls.json) cover six synthetic
checkpoints and a real 0.05 s deadline in each cached/full path. Every preserved
record is an exact prefix of the complete reference; interruption yields no
selected proposal. Real cooperative overruns are 0.001757
and 0.017452 s, retained explicitly. The unchanged key-grouping
implementation and its existing four deadline controls remain bound through
the preceding source preflight; this change does not modify grouping.

The separate [bounded validation process](h5-selector-equivalence-20261107/process.json) closes normally in
**184.945360 s**, below its 300 s/2 GiB limits, with peak
aggregate committed memory of 288,587,776 bytes.
All descendants close and optimizer calls remain zero.

## Next source preflight and unchanged acceptance

[Next](h5-selector-equivalence-20261107/next-step.json), reconstruct an initializer from the original A/W
source under all [eighteen closed identities](h5-selector-equivalence-20261107/closed-problems.json), preserving
the full **33.769462 s** preparation charge plus new work. Audit the selected model,
full score and scalar gradient before freezing any new finite search contract.
The current runtime and mutated validation contexts cannot seed that work.

The last construction still has **50 failed source pairs** and no valid full66
layout. Faster bookkeeping does not establish material savings, exclude an
allocation or reopen a problem. Four earlier arrangements and all 440 allocation
candidates remain unresolved. Full source/native/material validity, production
integration and the original H5 matrix remain required. README claims and releases
are unchanged.

The closed construction checkpoint is committed as **e90bc056**. Main remains
**8dc99684** at review, with 5 passed CI jobs and 1 live jobs in the
[retained snapshot](h5-selector-equivalence-20261107/main-ci-at-review.json). Both checkpoints await the
ordinary push gate; no CI run is cancelled.

[Archive verification](h5-selector-equivalence-20261107/archive-checks.json), [manifest](h5-selector-equivalence-20261107/raw-manifest.json),
[source bindings](h5-selector-equivalence-20261107/source-bindings.json), [historical references](h5-selector-equivalence-20261107/external-evidence.json)
and [runtime pins](h5-selector-equivalence-20261107/runtime-bindings.json) preserve the complete evidence.
