# H5: fine-band capacities and spatial-bound diagnostics — 2026-10-29

The finer swept-support cover excludes **40 of 82 remaining count distributions**
and **seven of 25 fixed cog-site choices**. Its 26 exact area certificates pass an
independent source-containment and polygon-clipping audit. The retained construction
has **18 site choices and 42 count distributions**; all original source modes and
component assignments remain available for those choices.

These are necessary constraints on the saved construction, not a placement or a
global allocation exclusion. The 440 overall allocation candidates, complete
66-part source validation, native checks and H5 matrix remain open. Completion is
still **60%**. No placement solver or native validator was called in this checkpoint.

## A tighter conservative support cover

The previous cover used 10 mm square cells. This construction encloses every
rational swept-hull vertex with its four surrounding 0.1 mm lattice corners and
takes their integer convex hull. It then covers that polygon in 2 mm horizontal
bands, with each band's X extrema rounded outwards to 0.1 mm. The resulting union
contains every original allowed placement of the filled source material.

For each subset of original family components, the union's area is an upper bound
on the material those components can hold. The source material lower bounds are
the previously verified contained rectangles. A count distribution is excluded
only when its exact required area exceeds the exact conservative union area.

The [construction](h5-fine-band-capacities-and-spatial-diagnostics-20261029/fine-band-preparation.json) takes 1.9511964 s and examines
455 subset areas. The [independent audit](h5-fine-band-capacities-and-spatial-diagnostics-20261029/fine-band-audit.json) takes
13.7682386 s and verifies all 2,232 source swept pieces, containment of 14,714
source vertices, 1,810 distinct integer hulls and 240,450 recorded band spans.
It uses 196,029 exact polygon-band clipping operations, including exact checks of
outward rounding. The 100 reconstructed group supports reduce the previous
individual area bounds by between 4,950.4 and 26,733 mm².

The seven excluded empty-site pairs are `[4,10]`, `[5,14]`, `[9,10]`, `[9,14]`,
`[11,12]`, `[11,13]` and `[12,13]`. Including earlier necessary certificates,
87 of the construction's 105 site choices are now excluded.
The [complete bound table](h5-fine-band-capacities-and-spatial-diagnostics-20261029/all25-fine-band-bounds.json) records each
certificate and every retained distribution.

The [filtered-input audit](h5-fine-band-capacities-and-spatial-diagnostics-20261029/filtered-count-audit.json) confirms that only
proved count exclusions were applied. It checks 4,501 mode attributions and
2,957 unique family/geometry/region assignments; every same-geometry mode alias
still agrees on its original component. Filtering takes 0.0314010 s. A future
model must charge the full required preparation chain, including the 1.9511964 s
fine-band construction; audit time is reported separately.

## Spatial diagnostics retained without exclusions

The complete diagonal-strip scan screens 3,990,000 inequalities across six
directions and retains all 25 prior site choices and 82 counts. Its
[diagnostic audit](h5-fine-band-capacities-and-spatial-diagnostics-20261029/diagonal-diagnostic-audit.json) reconstructs 37,794
source projections and checks 150 actual-source minima against an independent
clipping oracle. The mathematical preflight independently checks 120 synthetic
cases, including five interior stationary candidates. No prospective exclusion
required exact reconstruction during discovery.

Two rectangular-window scans each screen 1,881,000 inequalities on a 100 mm grid.
The first uses conservative per-hull box bounds; the second screens with upper
estimates at source-hull vertices and has an exact convex-hull minimum routine
for prospective exclusions. Both retain all prior counts. The
[window diagnostic audit](h5-fine-band-capacities-and-spatial-diagnostics-20261029/window-diagnostic-audit.json) independently checks
50 actual-source cases. Its separate mathematical preflight compares exact minima
on 120 synthetic convex domains against a subdivision-and-clipping oracle:
2,711 subcells, 53,920 area evaluations and nine interior edge stationary candidates.

After the fine-band exclusions, a complete axis-strip scan screens 3,537,000
inequalities over the 18 retained choices and finds no further exclusion. Its
[diagnostic reader](h5-fine-band-capacities-and-spatial-diagnostics-20261029/fine-strip-diagnostic-audit.json) verifies unchanged
source projections and count sets, and checks 72 sampled support areas with
38,860 independent polygon clippings.

The diagnostic readers verify the recorded scan shape and selected mathematical
values. They do **not** independently recompute every screened inequality, and
these negative scans do not prove that no stronger spatial bound exists.

## Evidence and next work

The [next step](h5-fine-band-capacities-and-spatial-diagnostics-20261029/next-step.json) is to investigate direct regeneration of
the fine-band count constraints, then audit a materially strengthened placement
model. Every previous solver call remains closed. Native validation still requires
a complete original-source-valid 66-part placement first.

The [raw manifest](h5-fine-band-capacities-and-spatial-diagnostics-20261029/raw-manifest.json) records 4839 canonical files and
872 byte-identical aliases in multipart archives totalling 58286857 bytes.
It includes the source bindings, construction and audit helpers, raw diagnostics,
complete certificate tables and publication snapshots.

The [publication review](h5-fine-band-capacities-and-spatial-diagnostics-20261029/publication-review.json) confirms unchanged
production and README digests, upstream heads and releases, stable v0.1.0 and
preview v0.2.0-alpha.1. All six jobs for main `b86ea9dc` passed in
[run 40841006837](https://github.com/skulitom/Nestbolt/actions/runs/40841006837).
No new release qualifies. H2 remains open under Artem's retained original gate;
no reserved import vectors were evaluated.
