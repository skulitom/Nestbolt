# Smaller first55 model: closed UNKNOWN — 2026-11-04

The [continuous source exclusions](h5-continuous-small-block-exclusions-20261104.md)
reduce the canonical first55 model to 14 site choices and 24 count distributions.
All 6,498 variables and 32,697 constraints pass [independent readback](h5-block-pruned-global-call-20261104/model-audit.json),
including source-mode coupling, all 183 different-owner rectangle pairs,
182 canonical component equalities and 227 valid within-component orderings.
The [count-input audit](h5-block-pruned-global-call-20261104/count-input-audit.json) checks all 3,676 retained
source-mode attributions and preserves the proved count-table bytes.

The sole declared call returned **UNKNOWN**, with 53,720 branches, 4,508 conflicts
and no assignment. [The response audit](h5-block-pruned-global-call-20261104/response-audit.json) records
42.969984 s charged preparation, 12.282428 s allocated solve time and 12.348058 s
returned solve time. The **0.065630 s solve-slice overrun is preserved**.
Algorithm time 56.080238 s and shared time 56.175358 s remain within 60/90 s.
There is no new infeasibility or placement claim, and the call remains closed.
[All preparation charges](h5-block-pruned-global-call-20261104/preparation-charges.json) include the original
short-sheet construction, source capacities, original count filter, new direct
proofs and new model build. The longer strip derivation is not a required input
to this direct algorithm.

The first builder stopped on a stale forbidden-pair count before producing a
model or calling a solver. Its files and failure record remain preserved; v2
uses the correct 91 forbidden pairs. The successful model and result were not
modified after their audits.

The new archive contains 43 canonical files and
1,498,902 compressed bytes. [Its manifest](h5-block-pruned-global-call-20261104/raw-manifest.json)
and [exact external evidence map](h5-block-pruned-global-call-20261104/external-evidence.json) form a complete
bundle with the preceding committed evidence archive; every reused member is
bound by manifest hash, member path, byte count and SHA-256. This avoids another
copy of the same historical source data. [Source bindings](h5-block-pruned-global-call-20261104/source-bindings.json)
resolve across both bundles and are independently checked before commit.

The 14/24 restricted domain and 440 whole-job allocation candidates remain open.
No source66 check, native validation or release follows. H2/H5 remain open at
**60%**; product source, original gates and all 22 reserved H2 vectors are
unchanged. [Next work](h5-block-pruned-global-call-20261104/next-step.json) examines the remaining independent
two-insert blocks and their companions; this global call must not be repeated.
