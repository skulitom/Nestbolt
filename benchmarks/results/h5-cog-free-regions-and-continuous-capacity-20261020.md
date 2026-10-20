# H5: cog free regions and continuous capacity — 2026-10-20

**At most thirteen cogs can fit while the selected 51 non-cog parts stay fixed,
even with arbitrary cog angles and continuous positions.** The original job
requires fifteen. At least one frame, bracket or insert pose must therefore
change. This is a necessary upper bound, not a thirteen-cog layout, and it
does not exclude solutions after other parts move. H2/H5 remain open at 60%.

## New cog contacts and retained failures

The [prior joint construction](h5-frame-capacity-and-joint-small-parts-20261020.md)
supplies all 18 frames, 12 brackets, 21 inserts and nine cogs. Its 51 non-cog
poses stay fixed for this investigation. Original filled outer outlines,
stock, margins, 0.2 mm clearance and material target remain unchanged.

The first preparation stopped with a missing `Path` import before creating
a plan or doing geometry work. Its exact helper and traceback are preserved.
The repaired preparation uses a new directory and records that repair.

All 9299 original candidate entries remain unchanged. Original-geometry checks
retain 608 of the 3947 old cog poses. Eight conservative free translation
regions cover four declared phases (0°, 4.5°, 9°, 13.5°) on two sheets.
All 438 proposed boundary/representative samples are processed: 437 new poses
and one exact duplicate, leaving no pending queries. Generation takes
3.484624400 seconds within its declared 120-second/2000-new-pose bounds.

An independent audit reconstructs every region and sampling order, checks
159,831 original cog/fixed-part pairs and 18,306 new cog/fixed-part pairs,
and exhaustively examines all 357,456 same-sheet pairs in the 1045-cog pool.
The exact 194,803 conflicts are represented by 883 verified cliques.
All nine known seed cogs remain. This finite sampling is not an all-angle proof.

The fully reconstructed cog-only model has 1045 variables and 884 constraints.
Its single declared 20-second call returns `OPTIMAL` in 0.748112200 seconds,
with nine cogs and solver bound nine. Both returned selections pass original
geometry; the exact seed's frozen CLI result is reused by hash, and the new
final layout receives one fresh CLI call. Both fail only because six cogs
are missing. The new final uses three new contacts and has minimum clearance
0.200100 mm. Its material charge is 4,985,103.45 mm² and filled area is
4,181,364.4704 mm², unchanged from this seed. It is not native-margin qualified
or an improvement over the previously documented best partials.

A separate cover-certificate model starts from the weaker greedy bound 17.
Its one declared 10-second call finishes in 0.538477400 seconds; saved covers
have sizes 17, 16, 15 and 14. Independent graph checks prove each cover valid.
The final certificate allows at most 14 cogs in this finite pool. It does not
independently certify the solver's reported packing optimum nine.

## A bound for all angles and continuous positions

The next construction replaces finite sampling with necessary geometry:

1. Exact rational segment-distance checks prove that a disk of radius
   **109.1157 mm** fits inside the filled cog about its recorded local center.
   Every rotated cog contains that disk. A deliberately weaker **0.1999 mm**
   clearance yields necessary center separation **218.4313 mm**.
2. Seventy-five axis-aligned rectangles are verified strictly inside the
   original transformed non-cog polygons with exact rational predicates.
   Expanding these by integer rectangles contained in a disk gives conservative
   forbidden center regions. Stock center limits are rounded outward.
3. Independent exact rectangle sweeps reconstruct the entire possible-center
   superset: 139 cells on sheet zero and one on sheet one. Small-diameter
   rectangle covers first bound capacity at 15 + 3 = **18**; a finite band
   partition improves this to 13 + 3 = **16**. Both results are retained and
   are inconclusive by themselves.
4. An exact rational **140.0002 mm** circumradius contains every cog vertex
   and hence the filled cog at any angle. Expanding each possible-center cell
   by its radius square encloses all space any cog can occupy. Clip this to
   outward-rounded usable stock and subtract only the verified solid interior
   rectangles of fixed parts. The resulting area is an upper bound, including
   space an actual cog might never be able to use.
5. Disjoint cogs each consume their original filled area,
   **50,062.718937983 mm²**. A conservative 0.000001 mm² allowance weakens this
   lower bound. Three different exact integer area algorithms agree; a separate
   geometry check also matches the areas and retains all nine known seed cogs.

| Target sheet | Reachable area upper bound, mm² | Area-based cog bound | Band-cover cog bound | Combined bound |
| --- | ---: | ---: | ---: | ---: |
| First | 549,821.78082009 | 10 | 13 | 10 |
| Last | 250,038.34467349 | 4 | 3 | 3 |
| Total | — | 14 | 16 | **13** |

The separate audit rechecks the circumradius, rational polygon area, all
expanded/clipped rectangles, exact area totals and all four band covers.
Known cog centers lie in the certified center regions and their complete
filled polygons lie in the reachable-area superset. Strict conservative
offsets and closed cell coverage account for boundary positions.

This certificate is conditional on these 51 non-cog poses and the original
filled-outer policy. It establishes that changing cog positions or phases
alone cannot complete this arrangement. It does not relax any H5 acceptance
rule, prove that thirteen are attainable, or rule out a rearranged full job.

## Source, README and release

Core source retains digest `8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88`. The English README includes the
remote comparison-page addition and still accurately describes the published
v0.2.0-alpha.1 preview, stable v0.1.0 and 60% plan completion. All three README
hashes match the previous reviewed checkpoint; no further README edit is needed
for this diagnostic evidence. Published release assets remain unchanged.

The remote abeb2739 checks are still running in the saved snapshot; five jobs pass and the Windows check remains in progress. No complete CI success is inferred.

No native packing, quality run or reserved held-out evaluation occurs.
The two actual layouts remain quantity failures. No new release is qualified.

## Next work

Do not repeat cog-only searches around these51 fixed non-cog poses: a continuous all-angle upper bound13 excludes the required15. Next examine a finite census that removes each non-cog obstacle in turn, recomputing the same conservative center/area bounds while retaining the other50 poses. Removing a part is a necessary relaxation, not a completed layout. A remaining bound below15 rules out changing only that pose; a larger bound merely identifies a possible joint-move target. Independently audit the resulting certificates before constructing changed non-cog placements. Do not reuse the old conditional cog conflict graph after non-cog moves. All66 original copies, native margins and unchanged H5 material/cutting gates remain required. H2 stays open under Artem’s decision.

[Checks](h5-cog-free-regions-and-continuous-capacity-20261020/checks.json), [pool audit](h5-cog-free-regions-and-continuous-capacity-20261020/pool-audit.json),
[layout audit](h5-cog-free-regions-and-continuous-capacity-20261020/layout-audit.json), [finite certificate](h5-cog-free-regions-and-continuous-capacity-20261020/finite-cover-audit.json),
[center-region audit](h5-cog-free-regions-and-continuous-capacity-20261020/center-region-audit.json),
[band covers](h5-cog-free-regions-and-continuous-capacity-20261020/band-cover-audit.json),
[continuous certificate audit](h5-cog-free-regions-and-continuous-capacity-20261020/continuous-capacity-audit.json),
[source review](h5-cog-free-regions-and-continuous-capacity-20261020/source-review.json), [remote checks](h5-cog-free-regions-and-continuous-capacity-20261020/main-ci-abeb2739.json),
[raw evidence](h5-cog-free-regions-and-continuous-capacity-20261020/raw.zip) and [manifest](h5-cog-free-regions-and-continuous-capacity-20261020/raw-manifest.json).
All 122 archive members, CRCs and byte hashes verify.
