# H5: corrected-source geometry and all-angle flat-edge support — 2026-10-26

**All geometry has been rebuilt for the source-valid retained 49 originals.**
The two brackets and all 15 cogs remain mandatory, with free positions and sheets,
all eight bracket variants and every real cog rotation. Neither of the two
bounded necessary searches finds an assignment or excludes this fixed subset.
H2/H5 remain open at **60%**; no source/native fit or release is claimed.

## Geometry rebuilt from corrected source transforms

The independent reader verifies 69 source-contained fixed rectangles, 1,330
integer forbidden bracket-anchor boxes and the complete union of 77 remaining
anchor rectangles across 16 variant/sheet domains. Exact set complements preserve
every integer boundary. For cogs, 69 source-inner-octagon sums provide 12 facets
each; 26,496 exact point-sum checks verify them. Of 33,275 closed grid cells,
28,175 are strictly excluded. The 5,100 remaining table rows cover all potentially
legal centers. Nine universal short-sheet count rows remain compatible.
No position-dependent certificate from the old fixed-51 arrangement is reused.

The first builder fails before model serialization because an OR-Tools method
returns `None`; its original code and failure are preserved. The repaired model
has 15,797 variables and 17,412 constraints. Its reader verifies all domains,
linked choices, optional rectangle intervals, 135 fully reified sheet equalities,
105 cog-pair clauses and 720 mixed variant/component clauses. There are no hints
or objective. Its single call ends **UNKNOWN** after 905,867 branches:
60.0538294 solver seconds / 60.0633621 returned seconds / 61.6408652 shared seconds.

## A stronger necessary rule from actual source vertices

For every real rotation, an original cog vertex attains signed-axis support of
at least 139,270 micrometers. Exact source-radius and center-flooring bounds yield
support **139,268**, radius **140,003**, and transverse bound **14,328** micrometers.
For a source-contained rectangle `[x,y,xx,yy]`, the strict center strips
`[x-h,y+L,xx+h,yy-L]` and `[x+L,y-h,xx-L,yy+h]` force an actual source collision.
The central band uses a strictly smaller source-contained disk; the outer band
uses an actual support vertex and verified rectangle-width inequalities.
The convex hull certifies vertex support only; it is never filled collision
geometry, and the cog-pair virtual disk is never applied to mixed collisions.

The exact reader checks all 80 source vertices, 40 hull edges, 80 source boundary
edges and all 186 fixed/moving support strips. Every rectangle satisfies the
strict width requirements. The stronger mask removes another **552 whole cells**,
leaving **4,548** rows (4,336 first-sheet / 212 short-sheet); all boundary centers
and all 15 previously checked cog-center cells remain represented.

The strengthened model preserves the earlier variables and constraints byte for
byte, then adds 15 mask tables, 1,440 conditional support clauses and 5,760
halfplanes. All **21,557 variables / 24,627 constraints** pass independent reading.
Its one new call ends **UNKNOWN** after **1,345,918 branches / 197,331 conflicts**:
60.097942 solver seconds / 60.1094835 returned seconds / 61.3953801 shared seconds.
Both small soft-limit overruns are retained, both calls stay inside their 90-second
shared bounds, and both searches are closed without retry or extension.

## Next work and publication checks

These are necessary models, not complete source geometry. There is no assignment,
fixed-49 exclusion, chosen cog angle, full-66 witness or native validation.
Continue through exact geometric decomposition/capacity reasoning or a materially
different source construction; preserve all originals, guards and material limits.

Main `36f162d0` has five successful checks. Its browser-only second attempt also
times out before tests: checkout alone takes **18m07s**. Both failures remain
preserved; CI checkout overhead will be repaired and validated independently before
the next main push. Production, READMEs and upstream heads/releases are unchanged.
All 22 reserved H2 vectors remain unopened.

[Checks](h5-corrected49-flat-edge-20261026/checks.json), [geometry](h5-corrected49-flat-edge-20261026/geometry-checks.json),
[support proof](h5-corrected49-flat-edge-20261026/necessity-proof.json), [mask](h5-corrected49-flat-edge-20261026/support-mask-checks.json),
[strong model](h5-corrected49-flat-edge-20261026/strong-model-checks.json), [response](h5-corrected49-flat-edge-20261026/strong-response-checks.json),
[next step](h5-corrected49-flat-edge-20261026/next-step.json), [manifest](h5-corrected49-flat-edge-20261026/raw-manifest.json).
The archive verifies 90 canonical files and
64 identical-content aliases by bytes, SHA-256 and CRC.
