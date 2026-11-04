# Direct count proofs and relative-hull capacities — 2026-11-04

Independent continuous-source proofs reduce the restricted fixed-cog construction
from **9 site choices / 13 count distributions to 2 choices / 3 distributions**.
The remaining choices are [5,10] and [10,11]. All 440 whole-job allocations,
the full 66-part layout and H5 matrix remain open. These are exclusions within
the specified conservative source domains, not whole-job infeasibility claims.

## Preserved partial pass and timing limitations

A larger triple pass reconstructs 497 source options over nine bracket domains.
[Its audit](h5-direct-counts-and-relative-hull-capacities-20261104/partial-triple-audit.json) verifies 16,998 pair exclusions and
177,020 complete disjunction trees, while preserving 193,588 necessary triples.
All 46,982 unprocessed triples are explicitly retained. This pass yields no
capacity bound. [Its timing record](h5-direct-counts-and-relative-hull-capacities-20261104/partial-triple-timing-limitation.json)
states that the reported 58.690668 seconds precedes evidence serialization;
complete process time was not captured. It is not performance-gate evidence.

## Direct count proofs and measured timing

A distinct direct method searches only prefixes needed for each demanded
multiplicity, scales rational bounds exactly, and reuses certified prefix
failures across source domains. [Independent full Floyd closure](h5-direct-counts-and-relative-hull-capacities-20261104/direct-count-audit.json)
verifies 311,071 complete prefix trees and all 325,081 prefixes needed to cover
six complete count exclusions. [The full process](h5-direct-counts-and-relative-hull-capacities-20261104/direct-process.json)
takes 63.843848 seconds: its **3.843848-second preparation-target overrun is
preserved**, while the 90-second process cap passes.

A revised algorithm checks every proper submultiset before solving a prefix,
so an impossible smaller combination rejects a larger one. It rebuilds directly
from original source inputs and imports no earlier search certificates.
[Its independent audit](h5-direct-counts-and-relative-hull-capacities-20261104/subsumed-count-audit.json) verifies 211,129 trees,
859,992 proof nodes and the same six complete capacity bounds. [Full process
time](h5-direct-counts-and-relative-hull-capacities-20261104/subsumed-process.json), including evidence serialization, is
50.408002 seconds. Both methods stop before completing every larger domain;
neither discards unprocessed possibilities or claims a placement.

[Applying the six proved bounds](h5-direct-counts-and-relative-hull-capacities-20261104/direct-filter-audit.json) removes nine
count distributions and choices [0,5], [0,10], [5,11], [10,12], [10,13] and
[12,14], leaving three choices and four distributions. Every surviving source
field is unchanged. Proof validity and the recorded timing failure remain
separate facts; the failed timing is not relabelled as a pass.

## Stronger pair constraints from original source hulls

For choice [13,14], 134 bracket options must hold six copies. A new necessary
pair method preserves X/Y coupling: every relative translation lies in the
convex hull of differences between original source-hull vertices. It excludes
a pair only when that complete hull is covered by strictly inset forbidden
rectangles from the contained original-source components.

The [pair audit](h5-direct-counts-and-relative-hull-capacities-20261104/relative-pair-audit.json) verifies all 9,045 option pairs,
4,597 axis exclusions, and **656 additional relative-hull exclusions**, using
12,196 exact source vertex differences and 1,927 independent rational polygon
clippings. The remaining necessary pair set has 3,792 entries. [The full
preparation process](h5-direct-counts-and-relative-hull-capacities-20261104/relative-pair-process.json) takes 0.666982 seconds.

A new direct count proof uses those audited pair constraints and charges that
complete preparation time. [Independent readback](h5-direct-counts-and-relative-hull-capacities-20261104/relative-count-audit.json)
verifies 78,129 complete trees, 338,457 proof nodes and all 103,919 count prefixes,
proving a maximum of five brackets in the six-bracket domain. [The measured
process](h5-direct-counts-and-relative-hull-capacities-20261104/relative-count-process.json), including pair preparation and
evidence serialization, takes 18.168017 seconds with no overrun.

The [final filter audit](h5-direct-counts-and-relative-hull-capacities-20261104/final-filter-audit.json) removes [13,14] and
verifies all 761 retained source-mode attributions. [The authoritative table](h5-direct-counts-and-relative-hull-capacities-20261104/all2-filtered-bounds.json)
contains [5,10] with bracket/insert component counts [6,1,6] or [7,0,6], and
[10,11] with [6,1,6]. All four earlier fixed two-insert companion choices are
now excluded within their specified domains; their valid partial layouts and
all closed model calls remain preserved.

These timings measure standalone proof processes, not a complete H5 construction
pipeline. Any later construction must measure and charge all prerequisites it
actually uses. No new placement solver, source66 checker or native validator was
called. [Next work](h5-direct-counts-and-relative-hull-capacities-20261104/next-step.json) requires all thirteen moving originals
for the surviving choices, or a distinct placement method with explicit scope.

The archive contains 112 new canonical members and
11,316,959 compressed bytes. [The manifest](h5-direct-counts-and-relative-hull-capacities-20261104/raw-manifest.json),
[external evidence map](h5-direct-counts-and-relative-hull-capacities-20261104/external-evidence.json), and [source bindings](h5-direct-counts-and-relative-hull-capacities-20261104/source-bindings.json)
preserve the complete new evidence and resolve reused bytes against two previous
committed manifests. Independent verification reads and hashes every referenced
member. H2/H5 remain open at **60%**; the original gates, held-out isolation,
production code and release status are unchanged.
