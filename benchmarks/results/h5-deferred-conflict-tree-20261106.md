# Complete proof trees exclude four arrangements — 2026-11-06

Independent replay excludes **four more fixed29/cog arrangements**, leaving
**68 of the original 455** (387 excluded). The fifth tested arrangement
remains open. These are continuous zero-clearance exclusions conditional on
the fixed core and cog poses. All **440 whole-job allocations** remain, and
H2/H5 remain open at **60% completed milestone weight**.

The [previous insert-distribution proof](h5-frontier-insert-exclusions-20261106.md)
left five mandatory-bracket cases beyond its frozen enumeration limit.
This new method keeps their complete continuous necessary domains and
branches over candidates in a mandatory bracket group. It preserves every
remaining possibility without enumerating all optional insert-group subsets.
The previous bounded processes and placement calls remain closed.

## Independent tree replay

[The audit](h5-deferred-conflict-tree-20261106/tree-audit.json) reconstructs all root candidates from
the previously audited source covers. It verifies disjoint mandatory bracket
groups and self-conflicts, then replays every removal using exact integer
source-inner rectangle inequalities. A candidate is removed only when it
strictly overlaps every candidate in another mandatory group.

Every bracket branch contains each candidate exactly once. Insert branches
partition choosing a cell once versus omitting it, retaining all compatible
cells on inclusion. A closed count leaf would require a complete pairwise
conflict-clique cover below the required insert count. Every record must be
reachable exactly once; open leaves cannot support an exclusion.

| Omitted cog sites | Records checked | Open leaves | Result |
|---|---:|---:|---|
| [2,5,10] | 11 | 0 | Continuously excluded |
| [3,5,10] | 11 | 0 | Continuously excluded |
| [4,9,14] | 35 | 13 | Unresolved necessary-graph witness |
| [5,7,10] | 11 | 0 | Continuously excluded |
| [5,8,10] | 11 | 0 | Continuously excluded |

In each excluded case, all ten candidates of the selected mandatory bracket
group lead to an empty mandatory group. The exclusions therefore follow
from bracket contradictions alone. Across all five trees, replay checks
**79 records, 3,729 bracket removals, 183 insert removals and 17,340 distinct
ordered source-inner pair evaluations**.

The unresolved case produces eight bracket cells and eight insert cells
with no certified strict conflict between any selected pair. The
[saved witness](h5-deferred-conflict-tree-20261106/necessary-graph-witnesses.json) is a necessary
relaxation result: cells can contain incompatible actual positions, and the
inner rectangles do not represent every point of the original outlines.
It is **not a placement**. The process stops that case after this witness,
preserving its twelve other open leaves. No exclusion is inferred.

## Budget and remaining work

The frozen limits are six seconds and 25,000 expanded nodes per case,
35 seconds for preparation, and 45 seconds for the complete process.
[Complete preparation](h5-deferred-conflict-tree-20261106/process-ledger.json) takes **0.467354 s**;
the independent replay takes **0.289212 s**. There are no overruns,
placement solver calls or native calls.

[The remaining frontier](h5-deferred-conflict-tree-20261106/remaining-fixed29-choices.json) contains
67 arrangements with bracket-clique bounds above eight, plus [4,9,14].
The [next proof method](h5-deferred-conflict-tree-20261106/next-step.json) will assess a complete
optional-clique branch partition for those 67 bracket covers. Selecting
one cell or skipping an entire conflict clique can preserve all independent
eight-bracket choices while allowing updated clique bounds to close branches.
It requires its own frozen limits and independent replay. No such proof is
claimed here; it must not reopen the current five closed tree processes.

The prior main checkpoint 8a765828 still has its two native CI jobs running
at report preparation; four of six jobs have passed in
[CI 42300921299](https://github.com/skulitom/Nestbolt/actions/runs/42300921299).
The committed fifteen-exclusion checkpoint and this evidence wait for all
six jobs and the aggregate success before a normal push.

Production core code, README and release assets are unchanged. Full66
original-source validation must pass before native/material checks,
production integration and the full H5 matrix. H2 retains its original gate
and unopened reserved vectors.

[The manifest](h5-deferred-conflict-tree-20261106/raw-manifest.json) contains 20 new canonical
members and 35,960 compressed bytes. [External references](h5-deferred-conflict-tree-20261106/external-evidence.json)
and [source bindings](h5-deferred-conflict-tree-20261106/source-bindings.json) preserve the exact prior
inputs. Independent archive readback verifies all new and reused bytes and
local report links before commit.
