# Coupled roof bounds and cog transfer — 2026-11-07

**All twelve remaining fixed 48-part layouts are excluded** by an independent
combined bracket/insert area proof. A stronger bound then excludes all sixteen
two-turned-frame first-sheet cores **for every bracket/insert split between
sheets**. These are exact fixed-core results; no whole orientation class or
whole-job allocation is excluded.

A changed source inventory moves one cog onto the short sheet and produces
**120 source-valid 44-part partial layouts**. Each still lacks six brackets and
sixteen inserts. No optimizer runs, no complete 66-part layout is established,
and the preserved valid 64-part result remains best. H2/H5 stay open at
**60% completed milestone weight**.

[The new insert covers](h5-coupled-roof-bound-and-cog-transfer-20261107/coupled-cover-plan.json) use all four legal
original orientations over the entire physical first stock. Source-contained
inner obstacles and open forbidden-center rectangles preserve every boundary
point and intervening interval. [Independent proof readback](h5-coupled-roof-bound-and-cog-transfer-20261107/coupled-cover-audit.json)
verifies **1,250 reused source rectangles and 4,115,344 continuous classes**,
using signed corner counts instead of producer slice assignment. Every retained
label and covering rectangle is checked. Exact union areas are independently
recomputed using a two-dimensional count grid.

Individually, each case's bracket bound admits at least six and its insert bound
at least twelve. Their combined occupied cover is nevertheless too small for
all eighteen originals. Conservative lower areas of 39,999 mm² per bracket and
19,799 mm² per insert require **477,582 mm²**. The largest combined upper bound
is **426,333.180631 mm²**, leaving at least **51,248.819369 mm²** missing.
[All twelve bounds](h5-coupled-roof-bound-and-cog-transfer-20261107/coupled-capacities.json) are preserved. Together with
the earlier five bracket exclusions and sixteen invalid three-turned cases,
all 33 declared patterns from the preceding checkpoint are closed.

[The broader inventory proof](h5-coupled-roof-bound-and-cog-transfer-20261107/inventory-independent-plan.json) releases
every bracket and insert on both sheets, retaining only the exact eighteen
frames and fifteen cogs on the first sheet. All twelve brackets and twenty-one
inserts require at least **895,767 mm²**. The full outward-relaxed short usable
rectangle contributes at most **465,326.048858 mm²**, regardless of its contents.
Adding the first-sheet occupied cover still leaves at least **4,107.770511 mm²**
missing in every one of the sixteen fixed cores.

[Independent readback](h5-coupled-roof-bound-and-cog-transfer-20261107/inventory-independent-audit.json) recomputes the
normal-seed target and exact rectangle unions. It binds the current material
implementation and ordering test: gross sheet areas are charged with only one
trailing offcut subtracted. Three sheets exceed the target. A fixed first-sheet
frame already exceeds the allowed short height, so any second sheet must be
the short one. One sheet also fails the first-sheet area bound. The
[sixteen results](h5-coupled-roof-bound-and-cog-transfer-20261107/all-inventory-capacities.json) therefore cover arbitrary
bracket/insert counts and placements on these fixed cores. Moving a frame or
cog, or transferring a cog to the short sheet, changes the problem and remains
outside this exclusion.

[The changed allocation](h5-coupled-roof-bound-and-cog-transfer-20261107/allocation-readback.json) is a survivor in the
audited 4,576-row / 440-survivor ledger: short counts **6 brackets, 5 inserts,
1 cog**; first-sheet counts **18 frames, 6 brackets, 16 inserts, 14 cogs**.
This is not a claim that the allocation was globally untested. The new
[source constructor](h5-coupled-roof-bound-and-cog-transfer-20261107/cog-transfer-plan.json) retains three source-sized
two-L-plus-insert modules. One cog and two stacked horizontal inserts replace
the six right-hand inserts. [The short twelve-part layout](h5-coupled-roof-bound-and-cog-transfer-20261107/short12-source.json)
passes [source checks](h5-coupled-roof-bound-and-cog-transfer-20261107/short12-checks.json), with minimum gap **0.230000 mm**.

The audited two-turned frame pattern and sixteen cog sites now supply every
fourteen-of-sixteen choice: **120 exact partial layouts**. [Independent
readback](h5-coupled-roof-bound-and-cog-transfer-20261107/source44-audit.json) verifies all 120, **67,440 same-sheet pairs**,
**6,720 original holes across cases**, and all identities. A separate direct
segment calculation checks all 66 short-sheet pairs and 48 stock edges.
Original cog 14 is on the short sheet; cogs 0–13 bind to occupied first-sheet
sites. [Six brackets and sixteen inserts](h5-coupled-roof-bound-and-cog-transfer-20261107/remaining-identities.json)
remain mandatory. The new partials are not packing-quality improvements.

| Complete stage | Preparation | Separate audit |
|---|---:|---:|
| Coupled insert/bracket covers | 0.629648 s | 4.309011 s |
| Inventory-independent fixed-core bound | 0.192242 s | 0.560377 s |
| One-cog transfer and 120 source partials | 4.098935 s | 4.862092 s |

With **12.186441 s** inherited preparation retained, the new source pipeline
carries **17.107266 s** before any future model or search. All six bounded
process stages close with zero active descendants under the 2 GiB cap and
unchanged CPU/thread controls. No old solver call is restarted or retimed.

[Next](h5-coupled-roof-bound-and-cog-transfer-20261107/next-step.json), extract complete necessary covers allowing two
empty cog sites from the already audited full mask matrices. The old retained
one-empty-site covers are insufficient. Independently verify the six-bracket /
sixteen-insert area screen before any complete companion model. Four earlier
arrangements and all 440 whole-job allocations remain unresolved. Full source,
native and material checks, product integration, surface parity and the original
H5 matrix are still required.

[Both preceding checkpoints reached main be9c79d6 normally](h5-coupled-roof-bound-and-cog-transfer-20261107/main-push-receipt.json)
after all six prior checks passed, with all 52 protected files intact. Its
[fresh CI snapshot](h5-coupled-roof-bound-and-cog-transfer-20261107/main-ci-at-review.json) has **4 passed / 2 live jobs**.
This evidence checkpoint awaits the next ordinary main push. Product code,
README and releases are unchanged.

[Archive checks](h5-coupled-roof-bound-and-cog-transfer-20261107/archive-checks.json), [manifest](h5-coupled-roof-bound-and-cog-transfer-20261107/raw-manifest.json),
[source bindings](h5-coupled-roof-bound-and-cog-transfer-20261107/source-bindings.json), [historical references](h5-coupled-roof-bound-and-cog-transfer-20261107/external-evidence.json)
and [runtime pins](h5-coupled-roof-bound-and-cog-transfer-20261107/runtime-bindings.json) preserve all inputs and results.
