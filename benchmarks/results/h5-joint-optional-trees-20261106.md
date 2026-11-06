# Joint bracket/insert proofs exclude eleven arrangements — 2026-11-06

Independent replay excludes **11 more fixed29/cog arrangements**, leaving
**52 of the original 455** (403 excluded). All **440 whole-job allocations**
remain; H2/H5 remain open at **60% completed milestone weight**.

## Complete insert domains

The [previous bracket-only proof](h5-optional-bracket-trees-20261106.md)
left 63 fixed arrangements. A fresh [insert-cover audit](h5-joint-optional-trees-20261106/insert-audit.json)
reconstructs every eligible continuous anchor cell for both insert geometries,
retaining all legal source aliases and closed boundary classes. It verifies
**21,067 cells and 218,597 pairwise conflict certificates**. No cell is
filtered out, and these insert bounds alone exclude no case.

Complete preparation takes **13.917995 s**; independent replay takes
**1.309437 s**. The 25/35-second preparation/process limits pass.

## Stronger two-family proof

The new model adds the complete insert domains to the **62 open
bracket-only cases**, requiring eight brackets and eight inserts together.
The existing joint graph witness [4,9,14] is carried forward and independently
rechecked against the complete new covers, without another search.

At each tree node, a complete pairwise-conflicting clique partition bounds
the remaining count for each family. If its count equals that family's
required count, every clique is mandatory. A candidate can then be removed
only if it strictly conflicts with every active candidate in one distinct,
nonempty mandatory group.

Each optional branch chooses every candidate of a complete conflict clique
once, plus a branch skipping the whole clique. Inclusion retains exactly all
compatible candidates of both families. A closed leaf has a complete clique
bound below the remaining bracket or insert count. Every partial or
post-witness branch remains open.

[Independent integer replay](h5-joint-optional-trees-20261106/joint-audit.json) verifies:

- **19,134 records**, 2,977 branching cliques and 14,475 closed count leaves;
- **9,590 mandatory covers** and 444,620 ordered removals;
- **2,839,121 mandatory-support pair checks** and 4,464,849 clique-pair checks;
- **2,477,150 distinct ordered source-inner pair evaluations**.

Every record is reached exactly once, all include/skip child domains are
reconstructed, and every exclusion has an entirely closed tree.
The excluded omitted-site choices are **[1,10,11], [2,10,11], [3,10,11],
[4,10,13], [5,6,11], [7,10,11], [7,11,12], [8,10,11], [8,12,13],
[9,10,14] and [9,12,13]**. The earlier node-limited bracket-only case
[9,10,14] closes under the new joint constraints; its old process remains
unchanged and closed.

These are continuous zero-clearance proofs conditional on the fixed29 core
and current cog poses. They do not exclude changing those placements or
any whole-job allocation.

## Open results and next geometry

There are **31 new joint graph witnesses**, plus the one carried forward,
all preserved with their [source cells](h5-joint-optional-trees-20261106/joint-graph-witnesses.json).
These 32 selections contain eight cells of each family with no certified
pair conflict; they are **not source-valid placements**.

Another **20 cases hit the frozen search cutoff**, including three whose
compatibility graphs are incomplete. Their complete partial records and open
leaves are preserved. They supply no exclusion and will not be extended,
reseeded or rerun under the same model.

The frozen search cutoff is **0.70 seconds per case**, within a **0.75-second
complete-case cap**, with 1,500 expanded nodes maximum. Global search,
preparation and process caps are 50/55/65 seconds. The complete joint process
takes **34.529171 s** and independent replay **8.286970 s**.
Every complete-case and process cap passes. Search cutoffs are recorded
separately from overruns. [The process ledger](h5-joint-optional-trees-20261106/process-ledger.json)
preserves both new preparations; there are no placement solver/native calls.

[The retained frontier](h5-joint-optional-trees-20261106/remaining-fixed29-choices.json) has 52 cases.
[The next geometric proof](h5-joint-optional-trees-20261106/next-step.json) will assess whether the
union of several source-inner component collision rectangles covers an
entire relative anchor box. Current pair certificates require one component
pair to cover that box by itself. Exact union coverage can certify additional
conflicts without removing continuous anchor possibilities. New edges must
pass an independent boundary-aware check before a stronger model is allowed.
If no new edges result, do not repeat the current search.

These diagnostic proofs do not establish a full construction within 60/90
seconds. Any later construction must charge all consumed preparation.
Full66 original-source validation remains required before native/material
checks, production integration and the H5 matrix.

Main 8a765828 has five passing CI jobs and the Windows native job still
running in [CI 42300921299](https://github.com/skulitom/Nestbolt/actions/runs/42300921299)
at report preparation. All local proof checkpoints await the six jobs and
aggregate success before a normal push. No live run is cancelled.
Production code, README and release assets are unchanged. H2 retains its
original gate and unopened reserved vectors.

[The manifest](h5-joint-optional-trees-20261106/raw-manifest.json) contains 152 new canonical
members and 3,691,574 compressed bytes. [External references](h5-joint-optional-trees-20261106/external-evidence.json)
and [source bindings](h5-joint-optional-trees-20261106/source-bindings.json) preserve exact inputs.
Independent archive readback verifies every new and reused member and all
local report links before commit.
