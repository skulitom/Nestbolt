# Fixed shelf and edge-layout capacity proofs — 2026-11-04

The six-insert top shelf passes original-source validation but **cannot be
completed** with six more brackets. Independently audited continuous bounds
exclude all 13 cog selections for that fixed shelf. Removing the shelf leaves
**one necessary edge-layout choice**, with cog sites **4, 5 and 10 empty**.
This is not a complete placement. H2/H5 remain open at **60% completed
milestone weight**.

## Valid shelf, insufficient bracket room

The [source audit](h5-shelf-and-edge-capacity-proofs-20261104/shelf-source-audit.json) verifies fixed33 plus six
horizontal inserts and all 13 remaining reference cogs: **52 source originals,
1,326 same-sheet pairs, 208 stock edges, 56 cutouts and 5,722 hole vertices**.
The reference contains one more cog than the required final twelve. The six
insert anchors are derived directly from the saved-world left bracket cover,
the full-stock upper Y anchor and a 180.23 mm pitch. All 66 required identities
remain partitioned between fixed39, six brackets, twelve cogs and the short9.

[Fresh exact source containment](h5-shelf-and-edge-capacity-proofs-20261104/shelf-inner-body-audit.json) verifies
41 inner rectangles and 164 exact corners for fixed39. Original certified cog
inner bodies and all eight legal bracket modes are unchanged; old fixed-core
anchor regions are not reused. The new
[continuous mask audit](h5-shelf-and-edge-capacity-proofs-20261104/shelf-mask-audit.json) independently replays
**22,314,444 point/open-interval classes** and verifies all **79** retained
closed cover boxes.

[Exact capacity replay](h5-shelf-and-edge-capacity-proofs-20261104/shelf-capacity-audit.json) checks every one of
the 13 additional cog omissions. The maximum bracket capacity is **four**,
below the required six; seven choices have no possible bracket anchor at all.
The proof covers the entire physical stock, every legal bracket mode and
continuous positions, even at zero clearance. It excludes only this fixed
shelf and these fixed cog poses.

The first component preparation encountered an empty eligible-shape list and
failed in the geometry library. Its
[closed process record](h5-shelf-and-edge-capacity-proofs-20261104/failed-capacity-process.json), stderr and
partial output remain preserved in the archive. Its audit could not proceed
because the preparation produced no complete choice table. A new version adds
explicit empty-list handling; the independent integer reader verifies zero
capacity directly for those domains. No failed file was overwritten or used
as an exclusion certificate.

## Necessary bounds without the shelf

The [fixed33 source audit](h5-shelf-and-edge-capacity-proofs-20261104/edge-inner-body-audit.json) reconstructs
35 source-contained rectangles from the actual saved transforms. Six brackets
and six inserts remain free. The bracket-only relaxation ignores the inserts.
Its [independent mask replay](h5-shelf-and-edge-capacity-proofs-20261104/edge-mask-audit.json) verifies
**22,050,936 continuous classes** and **155** cover boxes.

[Exact bracket capacities](h5-shelf-and-edge-capacity-proofs-20261104/edge-capacity-audit.json) exclude **12 of
13 choices**. Only additional empty site **5** survives. Its two groups have
capacities **five and one**, so any completion must assign five brackets to
the larger region and one to the other. These bounds do not establish that
either capacity is attainable.

A separate [source composition audit](h5-shelf-and-edge-capacity-proofs-20261104/combined-source-audit.json)
binds all twelve unchanged bracket/insert modes. The new
[insert-domain audit](h5-shelf-and-edge-capacity-proofs-20261104/insert-mask-audit.json) verifies another
**2,141,926 classes** and **212** cover boxes.
[Joint area/count replay](h5-shelf-and-edge-capacity-proofs-20261104/joint-capacity-audit.json) checks **19 exact
group areas**, **643 anchor-box assignments** and all bounded bracket/insert
count distributions across all 13 choices. It independently excludes eight
choices but leaves additional site 5 open. For that choice, its combined
reachable area is 367,322.331230 mm² versus a necessary six-bracket/six-insert
inner-body area of 358,788.720072 mm². That surplus is not a packing witness.

The strongest intersection of these proofs therefore remains the single
choice **[4,5,10]**; the joint bound adds no exclusion to the bracket-only
result. The [next-step record](h5-shelf-and-edge-capacity-proofs-20261104/next-step.json) preserves that scope and
the required next construction.

## Processes and remaining work

All successful preparations finished within their declared caps:

| Preparation | Complete process seconds |
| --- | ---: |
| Direct six-insert shelf | 0.300089 |
| Fresh shelf source bodies | 0.137830 |
| Shelf continuous cover | 1.774636 |
| Failed empty-list component pass | 0.329391 |
| Corrected shelf component pass | 0.570134 |
| Fresh fixed33 source bodies | 0.139111 |
| Fixed33 bracket cover | 1.746970 |
| Fixed33 bracket capacities | 0.628652 |
| Combined source composition | 0.129205 |
| New insert cover | 0.391872 |
| Joint bracket/insert capacities | 1.182815 |

These are proof-stage timings, not a complete construction budget. Any future
model must charge every preparation it consumes, including inherited source
work and failures where applicable, before its frozen 60/90-second call.
**No new placement solver or native call was opened.** All earlier calls
remain closed; the twelve-mover UNKNOWN is not reused as a negative proof.

Next, assess a genuinely new construction using the remaining cog selection,
the certified continuous anchor cover and the mandatory five/one bracket
distribution. It needs fresh source-covering positive geometry, an independently
audited model and a complete charged budget. It must not simply restart the
closed twelve-part companion.

These exclusions are conditional on fixed39 or fixed33. They do not reduce
the broader fixed29 frontier of 259 choices or the 440 whole-job allocation
candidates. Full66 original-source/native/material checks, production
integration and the full H5 matrix remain required. H2 retains its original
gate and unopened reserved vectors. Production code, README and release claims
are unchanged.

[The manifest](h5-shelf-and-edge-capacity-proofs-20261104/raw-manifest.json) contains 246 new canonical
members and 1,021,835 compressed bytes.
[External references](h5-shelf-and-edge-capacity-proofs-20261104/external-evidence.json) and
[source bindings](h5-shelf-and-edge-capacity-proofs-20261104/source-bindings.json) preserve exact historical
dependencies. The independent archive reader verifies all new and reused
members and local report links before commit.
