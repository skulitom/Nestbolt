# Insert distributions exclude fifteen arrangements — 2026-11-06

Independent continuous-source proofs exclude **15 more fixed29/cog
arrangements**, reducing the frontier from **87 to 72**. In total, **383 of
the original 455** choices are excluded. Five larger mandatory-clique cases
remain explicitly unresolved. All **440 whole-job allocations** remain;
H2/H5 stay open at **60%** completed milestone weight.

## Complete insert cover and pruning

The [preceding frontier proof](h5-full-frontier-proofs-20261106.md) leaves
20 arrangements with exactly eight mandatory bracket cliques. The new
[insert audit](h5-frontier-insert-exclusions-20261106/insert-audit.json) reconstructs every continuous
necessary insert anchor cell for all 20. It checks the mapping from each
follow-up case to the original frontier and consistency result.

Every removed cell strictly conflicts, for all anchors, with every surviving
bracket candidate in one mandatory clique. Independent replay verifies
**22,618** such pair certificates and **11,457** certificates for the retained
insert-clique covers. The resulting upper bounds range from eight to 23
inserts. This stage alone excludes no arrangement.

Complete preparation takes **0.915583 s**, with no overrun. Independent
coverage, source-overlap and index replay takes **0.348672 s**.

## Exhaustive bounded selection

Before processing, the next stage freezes a maximum of **20,000 eight-of-k
insert-group selections per arrangement**. Fifteen cases qualify, totalling
**21,738 selections**. Five cases with 21 or 23 insert cliques are recorded as
deferred; they are not excluded or partially counted as complete.

[Independent joint replay](h5-frontier-insert-exclusions-20261106/joint-audit.json) checks every selection
for all fifteen cases. Every valid packing must occupy all eight bracket
cliques and eight distinct insert cliques. A candidate is removed only if it
strictly overlaps every active candidate in another mandatory group. Each
selection ends with an empty mandatory group.

The audit verifies **375,801 ordered removals** and **1,717,058 strict
source-inner pair checks**. These finite certificates cover the complete
continuous necessary domains, including all legal source modes. They
therefore exclude the fifteen fixed arrangements even at zero clearance.
They do not exclude changed fixed-core placements, changed cog poses or
different whole-job allocations.

Complete preparation takes **5.521543 s**, within the frozen 25/35-second
internal/process caps. Independent replay takes **3.876276 s**. There are no
placement solver calls, native calls or time overruns.

## Remaining work and publication

[The retained frontier](h5-frontier-insert-exclusions-20261106/remaining-fixed29-choices.json) has **72**
choices: 67 with larger bracket-clique bounds, plus
[five deferred mandatory-clique cases](h5-frontier-insert-exclusions-20261106/deferred-large-distributions.json):
[2,5,10], [3,5,10], [4,9,14], [5,7,10] and [5,8,10].

[The next proof hypothesis](h5-frontier-insert-exclusions-20261106/next-step.json) branches on mandatory
bracket candidate domains and bounds the compatible insert count at each
node. A complete source-certified clique cover below eight supplies a
contradiction; each branching step must cover every remaining bracket option.
Independent tree replay is required before any exclusion. A truncated tree
or unresolved graph selection remains open. This avoids eagerly expanding
every optional insert-group combination; no such tree proof is claimed here.

The previously reviewed checkpoints and all 52 newer remote files were
[pushed normally](h5-frontier-insert-exclusions-20261106/main-sync-receipt.json) to main and the working
branch as **8a765828** after
[all six prior main checks](https://github.com/skulitom/Nestbolt/actions/runs/42094099320)
passed. [New CI](https://github.com/skulitom/Nestbolt/actions/runs/42300921299)
is running; no live run was cancelled. This evidence waits for that run before
the next push.

Production core code, README and release assets are unchanged by these
proofs. H2 retains its original gate and unopened reserved vectors.
Full66 original-source/native/material validation, production integration
and the H5 matrix remain required. No previous placement call is reopened.

[The manifest](h5-frontier-insert-exclusions-20261106/raw-manifest.json) contains 67 new canonical
members and 1,357,673 compressed bytes. [External references](h5-frontier-insert-exclusions-20261106/external-evidence.json)
and [source bindings](h5-frontier-insert-exclusions-20261106/source-bindings.json) preserve exact historical
dependencies. Independent archive readback checks every new/reused member and
local report link before commit.
