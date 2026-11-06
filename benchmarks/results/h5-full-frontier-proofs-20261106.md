# Complete fixed-core frontier proof — archived 2026-11-06

The saved pre-pause audits exclude **169 more continuous fixed29/cog
arrangements**, reducing the frontier from **256 to 87**. In total, **368 of
the original 455** choices are excluded. These proofs remain valid at zero
clearance. They do not exclude changed fixed-core geometry, changed cog poses
or any of the **440 whole-job allocations**. H2/H5 remain open at **60%**
completed milestone weight.

The calculations completed on 2026-11-04 and are archived on resumption.
No closed process or placement call was repeated.

## Complete bracket bound

[The full frontier audit](h5-full-frontier-proofs-20261106/full-frontier-audit.json) covers all 256
choices remaining after the [three mandatory-clique exclusions](h5-mandatory-clique-exclusions-20261104.md).
It independently verifies **43,535 continuous anchor cells** and **1,027,915**
strict source-inner pair-overlap certificates. Every legal bracket mode and
anchor belongs to a retained necessary box and a closed subcell. Each subcell
is self-conflicting; each certified clique can hold at most one original.

| Certified bracket upper bound | Choices |
|---|---:|
| 5 | 14 |
| 6 | 71 |
| 7 | 66 |
| 8 | 38 |
| 9 | 20 |
| 10 | 29 |
| 11 | 9 |
| 12 | 5 |
| 13 | 2 |
| 15 | 2 |

The **151** choices below the required eight brackets are continuously
impossible. Bounds of eight or more are not packing witnesses.
Complete preparation takes **22.574358 s**, within the frozen 35/45-second
internal/process caps. Independent certificate replay takes **3.973246 s**.

## Mandatory-clique consistency

The 38 choices with exactly eight bracket cliques must occupy every clique.
[Independent consistency replay](h5-full-frontier-proofs-20261106/consistency-audit.json) checks
**4,711 ordered candidate removals** and **60,792** strict source-inner overlap
certificates. A candidate is removed only when it conflicts with every
remaining candidate in another mandatory clique. Every valid packing
therefore survives each removal.

**Eighteen** choices end with an empty mandatory clique and are excluded.
The other **20** reach a verified consistency fixed point; this does not
establish a feasible packing. Together with the 67 choices having larger
bracket-clique bounds, **87** arrangements remain.

Complete consistency preparation takes **0.752594 s**; independent replay
takes **0.691081 s**. Both preparation processes close with zero overruns,
no placement solver calls and no native calls.

[The retained list](h5-full-frontier-proofs-20261106/remaining-fixed29-choices.json) preserves all
87 choices. [The 20 mandatory-clique survivors](h5-full-frontier-proofs-20261106/consistent-mandatory-choices.json)
map each follow-up index back to the original frontier proof.
[The next step](h5-full-frontier-proofs-20261106/next-step.json) applies the already certified insert
pruning and complete eight-of-k distribution proof to those survivors, with
bounded processing and unresolved cases retained.

## Repository reconciliation

Main advanced through three commits during the pause, ending at bb27a0fe:
agent setup documentation, the measured LightBurn/offcut comparison and common
site navigation. [The merge audit](h5-full-frontier-proofs-20261106/reconciliation.json) preserves all
**52 remote files** and every local evidence file exactly. The file sets do
not overlap, and the merge has no conflicts. The latest
[main Checks run](https://github.com/skulitom/Nestbolt/actions/runs/42094099320)
passes all six jobs; its
[Pages deployment](https://github.com/skulitom/Nestbolt/actions/runs/42238317515)
also passes. The earlier f8ba0d95 checks are complete and successful.

Product core code and release assets are unchanged by this work. The new
README and comparison content from main are preserved. This checkpoint does
not qualify a new release or close H5: full66 source/native/material validation,
production integration and the full matrix remain required. H2 retains its
original gate and unopened reserved vectors.

[The manifest](h5-full-frontier-proofs-20261106/raw-manifest.json) contains 329 new canonical
members and 5,016,296 compressed bytes. [Historical references](h5-full-frontier-proofs-20261106/external-evidence.json)
and [input bindings](h5-full-frontier-proofs-20261106/source-bindings.json) retain the complete proof
dependencies. Independent archive replay checks every new/reused member and
local report link before commit.
