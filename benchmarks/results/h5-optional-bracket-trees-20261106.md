# Optional bracket trees exclude five arrangements — 2026-11-06

Independent continuous-source replay excludes **five more fixed29/cog
arrangements**, leaving **63 of the original 455** (392 excluded).
All **440 whole-job allocations** remain. H2/H5 stay open at **60%**
completed milestone weight.

The [preceding mandatory-clique trees](h5-deferred-conflict-tree-20261106.md)
left 67 arrangements whose complete bracket covers had more than eight
conflict cliques, plus the unresolved joint case [4,9,14]. This new process
handles exactly those 67 broader bracket covers. It does not repeat a closed
placement call or extend the previous five-case process.

## Complete optional-clique partitions

Every valid eight-bracket placement selects eight different cells in the
complete continuous necessary cover. At each tree node, a certified
pairwise-conflicting clique admits at most one bracket. The tree branches
once on each member of that clique, retaining every compatible cell,
and once on skipping the whole clique. This partitions every possibility.

A leaf closes only when a complete conflict-clique cover has fewer cliques
than the remaining required bracket count. Eight compatible cells instead
produce an unresolved necessary-graph witness. The process stops that case
at its first witness and preserves all unvisited branches as open.

[Independent integer replay](h5-optional-bracket-trees-20261106/tree-audit.json) verifies all
**10,967 records, 2,380 branching cliques and 6,858 closed count leaves**.
It checks **3,086,774 closed-cover pairs**, **27,075 branching-clique pairs**
and **855,133 distinct ordered source-inner pair evaluations**.
Every record is reachable exactly once, every include/skip branch has the
correct full candidate set, and every selected cell self-conflicts.

The completely closed trees exclude omitted cog-site choices **[1,11,12],
[2,11,12], [3,11,12], [8,9,14] and [8,11,12]**, even at zero clearance.
These conclusions are conditional on the fixed29 core and current cog poses;
they do not exclude changing those placements or any whole-job allocation.

## Open cases and limits

There are **61 necessary bracket-graph witnesses**, preserved with their
[source cells](h5-optional-bracket-trees-20261106/necessary-graph-witnesses.json). They are not
source-valid placements and do not include the required eight inserts.

Case **[9,10,14]** reaches the frozen **5,000 expanded-node limit** and
retains **32 open leaves**, without a witness or an exclusion. Its process
is closed and will not be extended or reseeded.

The frozen limits also allow 0.45 seconds per case, a 35-second global
search cutoff, 40 seconds for preparation and 50 seconds for the process.
[Complete preparation](h5-optional-bracket-trees-20261106/process-ledger.json) takes **6.176453 s**,
and the independent audit takes **2.258178 s**. All per-case/process time
limits pass; the intentional node cutoff remains recorded.
There are no placement solver or native calls.

[The remaining frontier](h5-optional-bracket-trees-20261106/remaining-fixed29-choices.json) contains
these 62 open bracket cases plus the earlier joint case [4,9,14].
[The next model](h5-optional-bracket-trees-20261106/next-step.json) will add the complete continuous
insert domains and require eight brackets and eight inserts together.
Its two-family clique partitions and count bounds need fresh frozen limits
and independent replay. The stronger joint problem is distinct from these
closed bracket-only trees. No new model or exclusion is claimed here.

All consumed preparation must remain in any later construction ledger;
these diagnostic proofs do not establish a full construction within 60/90
seconds. Full66 original-source validation remains required before any
native/material check, production integration or H5 matrix result.

The prior main checkpoint 8a765828 still has four passing jobs and two
native jobs running in
[CI 42300921299](https://github.com/skulitom/Nestbolt/actions/runs/42300921299)
at report preparation. The local proof checkpoints wait for all six jobs
and aggregate success before a normal push. No live run is cancelled.
Production code, README and release assets are unchanged. H2 retains its
original gate and unopened reserved vectors.

[The manifest](h5-optional-bracket-trees-20261106/raw-manifest.json) contains 81 new canonical
members and 310,197 compressed bytes. [External references](h5-optional-bracket-trees-20261106/external-evidence.json)
and [source bindings](h5-optional-bracket-trees-20261106/source-bindings.json) preserve exact prior
inputs. The independent archive reader verifies every new/reused member
and local report link before commit.
