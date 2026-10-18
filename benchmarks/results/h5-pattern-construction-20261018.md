# Mixed-part construction diagnosis — 2026-10-18

The [saved-gap diagnosis](h5-saved-gap-diagnosis-20261018.md) found only small local gains.
This follow-up uses the same four saved seed-0 mechanical jobs to construct groups
of several parts. It runs offline geometry and integer optimization on CCD1;
**no Nestbolt search, timing comparison, original pilot or gate is rerun**.

The simple catalog combines corner/rectangle pairs, corner pairs and staggered
round-part grids. All four inventories exceed their usable target rectangle area,
so no placement is attempted. The retained mixed catalog adds groups of two to
four parts and contact points where enclosing-box extrema change owner. This
matters: checking only forbidden-region vertices missed compact arrangements.
Two brackets and one insert fill **97.31%** of their 310.4022 × 330.4022 mm box in
the large-plate 0.2 mm case. These are component geometry results only.

An integer coverage model chooses the smallest padded rectangle total within each
finite catalog. It preserves all original quantities. Only the large-plate 1.5 mm
case initially passes that necessary area check; 300 attempted column-based
placements leave parts unplaced. A separate 15-degree free-angle check reduces
round-pair boxes by **0.7075–1.9875%**. Adding those verified pairs admits both
large-plate inventories to the area check. The following additional placement
attempts include both fixed large-rectangle columns and unpinned rectangles:

| Saved case | Selected padded area (mm²) | Available padded area (mm²) | Area check | Additional attempts |
| --- | ---: | ---: | :---: | ---: |
| large-plates-k0.2 | 4,898,551.544 | 4,908,251.189 | yes | 324 |
| large-plates-k1.5 | 4,954,744.257 | 4,986,399.424 | yes | 324 |
| panel-hardware-k0.2 | 4,757,147.502 | 4,657,894.713 | no | 0 |
| panel-hardware-k1.5 | 4,847,288.701 | 4,754,670.518 | no | 0 |

**No complete target layout is found.** Every one of the **948** attempted partial
layouts retains an explicit missing-parts list. The best final large-plate attempts
still leave 217,800.000 mm² / 446,862.719 mm² of filled part area unplaced. The panel
jobs fail even the finite catalog area check. These are restrictions of this
construction, not global infeasibility proofs.

The frozen public CLI validates **446 distinct component layouts**. Their component
quantities contain only pattern members, and the component stock is enlarged when
needed to test a large pattern. Those checks must not be cited as full-job or
original-stock validation. A separate vertex-transform audit checks **3,668**
component pairs and **526,094** pairs across all 948 partial placements. Quantities
including missing copies, allowed rotations/mirrors, original margins, target sheet
height and reserved holes all verify at the unchanged 1e-7 mm clearance tolerance.
All 2391 raw members, CRCs and byte hashes verify; the original pilot and
production digest are unchanged.

[Checks](h5-pattern-construction-20261018/checks.json),
[raw plans, catalogs, partial layouts, failures and CLI checks](h5-pattern-construction-20261018/raw.zip),
[manifest](h5-pattern-construction-20261018/raw-manifest.json),
[interpretation](h5-pattern-construction-20261018/interpretation.json).

The mixed-cluster contact construction supplies valid compact components, including two brackets and one insert, but no complete target layout is constructed. Do not integrate a runtime candidate or repeat a matched pilot on component results. The finite catalog minimum rules out only those conservative rectangle allocations for the panel jobs; it does not prove the original polygon problem infeasible. Next test whole-outline placement of the verified components, with joint sheet assignment and interleaving of their free exterior space, while preserving the original stock, quantities, rotations, kerf and reserved holes. Keep the quarter-turn failures, free-angle refinement and all incomplete layouts. A complete independently validated whole-job witness is required before bounded runtime work; then unchanged budgets, four-step repair cap, prior qualifications and a new matched pilot still apply.

H2/H5 remain open at **60%**. This does not create a new qualified release.
The published preview and all three README descriptions remain unchanged and accurate.
