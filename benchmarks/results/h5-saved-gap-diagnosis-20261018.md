# Saved-layout gap diagnosis — 2026-10-18

Four seed-0 mechanical outputs from the rejected [source-frontier pilot](h5-source-frontier-pilot-20261018.md)
were reused byte-for-byte for deterministic, post-hoc geometry construction on CCD1.
No solver, quality comparison or full gate was rerun. The original 72 results remain intact.

The first convex-hull pass and second pass preserving concave outer contours each
consider 216 source copies and 1,144 orientation attempts across 168 unique region
constructions. Neither constructs an earlier-sheet transfer with every neighbour fixed.
The second pass decomposes each original filled outer ring into convex pieces and
checks exact union coverage before using their Minkowski sums. Holes stay reserved.
Absence of a witness is limited by finite free angles and conservative clearance buffers.

A third pass tries moving source copies directly below their saved +1% material
target. It constructs one valid insert move, with no material gain. A fourth pass
allows smaller height reductions, considers high source copies first and stops at
four moves per case. Each move lowers its own outline top by at least 0.001 mm;
all other placements remain exact. The actual total improvements are:

| Saved case | Material saved (mm²) | Height saved (mm) | Fraction of still-needed saving |
| --- | ---: | ---: | ---: |
| large-plates-k0.2 | 381.007500 | 0.254005 | 0.1357% |
| large-plates-k1.5 | 537.546000 | 0.358364 | 0.2690% |
| panel-hardware-k0.2 | 1965.146250 | 1.572117 | 0.7374% |
| panel-hardware-k1.5 | 67.571250 | 0.054057 | 0.0348% |

All four remain above the original target. These local geometric opportunities
recover at most **0.7374% of the remaining material gap**, so they do not justify
another runtime candidate or quality pilot by themselves.

The frozen public CLI performs **33 checks across 21 unique layouts**, using each
original library and cutting request. A separate vertex-transform audit covers
**94,696 filled-outer pairs**, quantities, rotations,
mirrors, stock margins, unchanged neighbours and the original material calculation.
All checks pass at the unchanged 1e-7 mm clearance tolerance. The raw archive's
315 members, CRCs and byte hashes verify. No production code changed.

[Checks](h5-saved-gap-diagnosis-20261018/checks.json),
[original plans, attempted layouts, geometry regions and validator output](h5-saved-gap-diagnosis-20261018/raw.zip),
[archive manifest](h5-saved-gap-diagnosis-20261018/raw-manifest.json),
[limitations and next investigation](h5-saved-gap-diagnosis-20261018/interpretation.json).

Do not integrate a new gap-placement policy or repeat the rejected pilot on this evidence. The fixed earlier-sheet diagnoses yield no constructed transfer; the four-step source sequences recover only 0.0348–0.7374% of the remaining material gap. This supports small missed local opportunities, not a route to H5. Before another runtime candidate, inspect the original part geometry for generic multi-part arrangements that could reduce the larger assignment/packing loss, and construct an independently validated whole-job layout under the unchanged no-hole, kerf, orientation and stock constraints. An unbounded offline construction would show feasibility only; it would still require a bounded implementation, all prior qualifications and a new matched pilot. Do not increase the four-step cap or budgets, relax material limits, use reserved inputs, or claim infeasibility from these finite-angle greedy diagnostics.

H2/H5 remain open at **60%**. The published preview and all three READMEs remain
accurate; this diagnostic work does not create a new release candidate.
