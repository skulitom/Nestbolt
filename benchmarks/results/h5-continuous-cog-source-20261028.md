# Continuous cog rotations: rejected local result — 2026-10-28

Allowing independent cog rotations produced **no better source-valid packet**.
The sole SLSQP call is closed. Its returned candidate fails 11 of the 105
source-pair checks and one stock boundary; it is preserved as rejected evidence.
The starting packet remains valid at **772.202399 mm high × 1,436.447399 mm wide**.
H2/H5 remain open at **60% completed milestone weight**.

This experiment gives every one of the 15 cogs an independent center and angle,
plus a common top objective: 46 continuous variables. Angles range from 0° to
18°, a constructive subset of the job's free rotations, with no exact source
symmetry claim. Every evaluation rebuilds the filled polygon from all original
80 vertices. No fixed-angle obstacle or capacity rectangle is reused.

Positions and top use metres; angles use radians. The 180 inequality residuals
are in metres: 105 source-pair constraints and 75 stock/top constraints. The
construction clearance is 0.224 mm and stock extra 0.013 mm, compared with the
original acceptance thresholds of 0.211708673 mm and 0.011444092 mm. Overlap
uses negative square root of intersection area as an optimization proxy; source
acceptance always requires actual disjoint polygons and original distances.

Before solving, independent scalar construction checked all 180 constraints
in five cases, including varied angles and deliberately invalid coincident,
stock and top controls. All 900 comparisons passed, as did 46 finite-difference
probes. The complete positive control passes 105 original pairs, 60 stock edges,
15 holes and 3,000 hole vertices.

The predeclared budget permits one call, 200 iterations, 6,000 geometry
evaluations, 60 seconds of search and 90 seconds shared time. There are no
restarts. The call returned after **48 iterations / 2,486 geometry evaluations**,
using **8.321686 seconds** of search and **9.325484 seconds** shared time; neither
budget was exceeded. The raw status is 4, “Inequality constraints incompatible”.
This is a local numerical failure, **not an infeasibility certificate**: the
independently verified starting packet satisfies the declared constraints.

The first proposed step lowers the top by 96.679438 mm, but its most violated
source residual is −95.187405 mm. Every one of the 48 saved callbacks is
source-invalid. The raw final packet is 777.142862 mm high, has 11 failed pairs,
and extends 0.262361 mm beyond the usable stock boundary. No failed candidate
replaces the starting packet. Independent source readback and the frozen-input,
bound and budget audit pass for the retained evidence. The height gain is zero.

The next formulation must keep accepted iterates feasible: small proposed
center/angle changes, independently checked derivatives, and exact source
clearance checks before accepting any move. It needs a new audited control and
one frozen finite budget. This closed SLSQP call will not be restarted or
extended. The other 51 original parts still need placement; any cog packet
requires all 66 original parts and source/native/material validation before
integration or the full H5 matrix. The previous valid64 and 444 necessary
allocation counts are preserved.

The preceding commits 05a7232c and 8713c6e1 were pushed normally and atomically
to main and the working branch after all six jobs on 2adfa569 passed.
[CI 40742366525](https://github.com/skulitom/Nestbolt/actions/runs/40742366525)
is running on main 8713c6e1. This checkpoint waits for its six jobs before
another normal push. Production and all READMEs are unchanged. Upstream Sparrow
remains 6f7b9d35 / v0.3.0; Studio remains c0bb9e86 without a release. No stop rule
fires. H2's original gate and 22 unopened reserved vectors remain unchanged.
No new release qualifies.

Evidence: [preflight](h5-continuous-cog-source-20261028/preflight-audit.json),
[independent source readback](h5-continuous-cog-source-20261028/source-audit.json),
[rejected source checks](h5-continuous-cog-source-20261028/rejected-source-readback.json),
[budget and diagnosis](h5-continuous-cog-source-20261028/contract-audit.json),
[retained packet](h5-continuous-cog-source-20261028/retained-source15.json),
[next step](h5-continuous-cog-source-20261028/next-step.json),
[raw manifest](h5-continuous-cog-source-20261028/raw-manifest.json).
The byte-verified archive contains 47 canonical files
and 39 identical-byte aliases in 79,646
compressed bytes, including the frozen inputs, scripts, raw response, all callback
diagnostics, rejected readback, positive control and publication receipt.
