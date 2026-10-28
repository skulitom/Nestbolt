# Feasible cog moves and contact diagnosis — 2026-10-28

Exact source checks keep every accepted packet valid, but the height gain is
only **0.002768 mm**, with a **0.002945 mm width increase**. This does not solve
the mechanical material requirement. The sole search is closed at its declared
minimum trust radius. H2/H5 remain open at **60% completed milestone weight**.

Unlike the preceding failed SLSQP call, this sequence accepts a move only when
its actual original polygons pass every pair, stock and top constraint. It uses
15 independent centers and angles plus top, in mm/degrees, and retains the
constructive 0°–18° angle window. Construction clearance remains 0.224 mm and
extra stock clearance 0.013 mm. Linear proposals reserve another 0.000020 mm;
exact acceptance requires a 0.000010 mm residual. These are stricter proposal
rules; the unchanged source acceptance thresholds still govern the audit.

The starting source control passes 105 pairs, 60 stock edges, 15 holes and
3,000 hole vertices. Independent scalar original-ring calculations verify all
8,280 initial derivative entries, the 180 constraints, objective, stock/top
derivatives, mixed units, 46 bounds and the feasible zero step. Finite
differences are approximations, so this model audit never substitutes for
actual source acceptance.

The frozen budget permits one deterministic sequence, at most 80 LP directions,
14 backtracking trials per direction, 10,000 geometry evaluations, 60 seconds
of search and 90 seconds shared time. The initial trust bounds are 2 mm of
translation/top and 0.25° of angle change. Repeatedly short accepted moves shrink
the radius; it cannot be reduced below 0.00005 of the initial radius. Every LP
uses one HiGHS thread and at most two seconds. SciPy's warning that the `threads`
option is passed through to HiGHS is preserved in the raw stderr.

The sequence closes after **25 LP directions, 145 backtracking trials and
2,471 geometry evaluations**, using **3.735082 s search / 4.707303 s shared**.
There are 25 accepted moves plus the original control. Final radius scale is
0.0000457763671875, below the declared floor; no restart or extension occurs.
Independent readback verifies all 26 accepted states and every one of the 145
trials against original rings, angles, holes and stock. It reconstructs all 25
LPs, their bounds and accepted/rejected decisions, including **207,000 derivative
entries**, with maximum discrepancy 4.55e-8. Eighty-two rejected trials meet the
looser physical source threshold but fail the predeclared stricter proposal
rules; they are not silently accepted after the run.

The best actual packet is accepted state **12**:

| Measure | Value |
| --- | ---: |
| Actual height | 772.199631116 mm |
| Actual width | 1,436.450344214 mm |
| Height gain from starting packet | 0.002768279 mm |
| Width cost | 0.002944820 mm |
| Minimum source gap | 0.224056239 mm |
| Minimum extra stock clearance | 0.013707291 mm |
| Cog angle range | 6.999641°–7.000338° |

Its top decreases by 0.002868652 mm, but part of that is translation. Later
states have lower top values yet a slightly greater actual height. Selection
therefore uses independently measured height rather than the top objective.
No local or global optimum is claimed.

## Why the steps shrink

A separate read-only diagnosis uses the saved first LP direction; it does not
start another optimizer. It checks **1,344,000 original vertex-to-edge distances**
over all 105 source pairs. Twenty pairs are within 1 mm. Fifty-six nearby edge
features reproduce 40 direct forward/backward source-distance checks to within
**1.85e-10 mm**, at 0.0001 of the saved direction.

The coordinate finite-difference matrix is too optimistic for some combined
moves as the closest edge feature changes. For cogs 0 and 2, it predicts a
distance slope of 1.841549 mm per full step; direct forward motion gives
0.906249 mm. The pair has two features within 1e-7 mm of its closest distance.
This identifies a limitation of a single derivative for the minimum-distance
function. The source acceptance checks correctly prevented invalid moves.

The first diagnostic incorrectly asserted that this effect must exceed 1 mm
per full step. It failed; that code and failure are preserved. A separate
corrected diagnostic removes the unsupported effect-size assumption and reports
the measured **0.935300 mm** difference. No optimizer or placement was rerun.

The next proposal model should keep the nearby vertex/edge constraints separate,
using an audited distance window derived from the allowed center and angle
motion. Its gradients must be checked against original edge motion and the
saved rejected direction before a new bounded call. Exact source checks remain
mandatory. This does not yet supply the other 51 originals or a complete layout;
all 66 original parts and source/native/material checks remain prerequisites
for integration and the full H5 matrix.

## Publication

Main remains **8713c6e1**, with four successful jobs in
[CI 40742366525](https://github.com/skulitom/Nestbolt/actions/runs/40742366525).
Linux and Windows checks are live. The verified a2c0ba46 checkpoint and this
evidence wait for all six jobs and fresh remote/ancestry/live-run guards before
a normal push. Production and READMEs are unchanged. Sparrow remains
6f7b9d35 / v0.3.0; Studio remains c0bb9e86 without a release. No stop rule fires.
The previous valid64, 444 necessary allocations, original H2 gate and all 22
unopened reserved vectors remain preserved. No release qualifies.

Evidence: [preflight](h5-feasible-cog-source-20261028/preflight-audit.json),
[all source/model audits](h5-feasible-cog-source-20261028/source-audit.json),
[accepted source states](h5-feasible-cog-source-20261028/source-accepted.json),
[contact diagnosis](h5-feasible-cog-source-20261028/contact-diagnosis.json),
[preserved diagnostic correction](h5-feasible-cog-source-20261028/diagnostic-erratum.json),
[next step](h5-feasible-cog-source-20261028/next-step.json),
[raw manifest](h5-feasible-cog-source-20261028/raw-manifest.json).
The verified archive contains 274 canonical files and
142 identical-byte aliases in 1,113,622
compressed bytes, including every LP, trial, original-source readback, input,
script, initial failed diagnostic and corrected contact calculation.
