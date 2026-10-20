# H5: continuous regions for a single frame move — 2026-10-20

**Ten of eighteen possible single-frame changes are now ruled out across all
allowed frame positions and rotations.** Together with the preceding bracket
and insert certificates, this excludes 43 of the 51 single non-cog changes
around this arrangement. Eight frames remain unresolved. No full layout,
material improvement or new release is established; H2/H5 remain open at 60%.

## Cover all possible positions of a released frame

The [single-part census](h5-single-non-cog-release-census-20261020.md) excludes
every individual bracket or insert move. For each remaining frame, the other
50 non-cog poses stay fixed. The original frame is a 450 × 350 mm rectangle
with four allowed quarter turns; its holes remain reserved under the unchanged
common-line filled-outer policy.

An axis rectangle inset **0.0002 mm per side** fits inside every rotated frame
about its transformed local center. Exact rational containment checks verify
this for all four allowed rotations. The two resulting axis-size classes
cover all four rotations. Certified interior rectangles of the fixed parts,
expanded by the frame half-extents and rectangles within a deliberately weaker
**0.1998 mm** clearance disk, define necessary forbidden center regions.
Stock center limits are rounded outward.

All **72 queries** (18 frames × 2 size classes × 2 sheets) complete in
**4.230176500 seconds**, within the declared 120-second bound. The last sheet
is too short for either frame size class. The first-sheet queries contain
**4625 free cells in 52 components**; all 18 original frame poses are retained
in their corresponding size classes.

The independent audit checks the four moving-frame containments, every
expanded rectangle and exact complementary area. It verifies all 72 queries
in **3.838829400 seconds**. These domains are supersets of valid positions,
so they support necessary bounds; they are not new accepted frame placements.

## Guaranteed occupied area across a whole region

For any center-region bounding box, intersect the frame's inner rectangle over
all center positions in that box. When nonempty, this common solid rectangle
is occupied by every possible frame pose in the region. Adding it to the
other 50 non-cog obstacles gives a necessary bound on cogs without selecting
a particular frame position.

Each region uses the previously audited cog inner disk and circumradius,
exact reachable-area bounds, small-diameter covers and verified cliques of
mutually incompatible center components. A single deterministic pass over
all 52 components takes **37.089722700 seconds**. Its independent audit checks
136 cog components and 272 band covers. **Sixteen whole regions are excluded;
36 remain inconclusive.** The coarse results are preserved.

## Bounded spatial refinement

The changed construction keeps those sixteen exclusions and divides the
36 unresolved center regions at integer midpoints along their longest dimension.
It clips the exact free cells into children and recomputes the guaranteed
frame core and cog bound. It declares **120 seconds**, at most **256 new nodes**
and depth at most **six**, with a breadth-first order and no retry.

The run stops at its time boundary after **120.343610200 seconds**:
**165 new nodes are evaluated and 49 remain pending**. The small overshoot
finishes the current indivisible case; no further case starts after the
between-case deadline. Of the evaluated nodes, 94 exclude their entire region.
No depth-six terminal case occurs. The exact pending queue is retained.

An independent audit verifies the complete tree and midpoint partitions,
every guaranteed frame core, **499 cog components** and **998 band covers**.
The unchanged last-sheet capacity-three certificate is reused byte-for-byte.
The audit takes **22.344450500 seconds**. Exclusion is propagated only through
fully covered trees; an unfinished branch never becomes an impossibility claim.

| Single-part change | Fully excluded | Still unresolved |
| --- | ---: | ---: |
| Bracket, from the previous census | 12 | 0 |
| Insert, from the previous census | 21 | 0 |
| Frame, after this audit | 10 | 8 |
| Total | **43** | **8** |

The unresolved frame candidates are **7835, 8895, 8896, 8897, 8898, 9057, 9178, 9233**.
Their 49 pending regions provide bounded locations for a different
construction. This evidence does not exclude multiple non-cog changes and
does not prove that any unresolved single-frame change is feasible.

## Source, README and checks

Core source retains its reviewed digest; all three README hashes are unchanged.
The README still accurately describes the published preview and open work.
No new layout or frozen CLI validation is produced, and no native packing,
quality run or reserved held-out evaluation occurs.

Checks on the pushed 7c47f498 checkpoint are still running in the saved snapshot. A complete pass is not inferred. The previous abeb2739 checkpoint's six successful checks remain
recorded separately. Published releases and original acceptance requirements
are unchanged.

## Next work

Do not resume or extend the expired120-second spatial tree unchanged. Its49 pending nodes retain exact center cells for eight unresolved frames. Use those cells as a finite construction source: propose original-geometry frame contacts within them, keep each original frame as a checked baseline, and discard any proposal violating the other50 non-cog poses or original stock/clearance. For each unresolved frame, new cog contacts may be generated around the other50 fixed non-cog parts before a changed joint choice of one frame and up to15 cogs. Every new candidate and all frame/cog and cog/cog conflicts need original-geometry audit; the old51-fixed graph cannot be assumed valid. A completed result requires restoring the frame and all66 original copies, independent geometry/CLI checks, native margins and unchanged H5 gates. The43 ruled-out single changes need no further single-part search around this arrangement. Multiple non-cog changes remain possible.

[Checks](h5-single-frame-continuous-regions-20261020/checks.json), [frame domains](h5-single-frame-continuous-regions-20261020/frame-region-audit.json),
[coarse bounds](h5-single-frame-continuous-regions-20261020/coarse-capacity-audit.json),
[refinement result](h5-single-frame-continuous-regions-20261020/refinement-result.json),
[independent tree audit](h5-single-frame-continuous-regions-20261020/refinement-audit.json),
[source review](h5-single-frame-continuous-regions-20261020/source-review.json), [pushed-checkpoint checks](h5-single-frame-continuous-regions-20261020/main-ci-7c47f498.json),
[all regions, nodes and pending work](h5-single-frame-continuous-regions-20261020/raw.zip)
and [manifest](h5-single-frame-continuous-regions-20261020/raw-manifest.json).
All 466 archive members, CRCs and byte hashes verify.
