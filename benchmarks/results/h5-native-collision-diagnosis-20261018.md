# H5: native collision margins and adjusted partial inputs — 2026-10-18

The native collision discrepancy is explained and corrected in the saved partial
inputs. **All four adjusted partials have exactly zero native loss**, on each sheet
and in the joined strip. Restoring their missing parts still expires four bounded
repair attempts. No complete target layout is found, and H5 remains open.

A new test-only observer exports actual native inflated polygons, original item
templates, container bounds, transforms and tracker entries. It observes the four
saved complete controls, partials and deliberately overlapping proposals without
running separation. Independent Shapely checks reconstruct every transform and
examine **51,175 pairs**. Every reported pair collision has actual native polygon
overlap; every significant native overlap is reported. Every static loss matches
an actual native polygon extending beyond its container. No collision detection
disagreement is found at the recorded 1e-7 geometric comparison scale.

All originally legal pairs with positive native loss are explained by the native
inflation margins. Native pose round-trip error is at most **0.000128 mm**;
independent offset reconstruction differs by at most **0.001168 mm**, within the
unchanged conversion guard. These loss scores include shape penalties and are not
overlap areas. The actual partial pair overlaps total 186–268 mm² per job, despite
the much larger numerical loss scores.

The native model uses `(clearance + conversion_guard) / cos(0.05)` for separation.
The geometric constructor used only 0.0011 mm extra spacing and 0.0001 mm edge
insets. At 0.2 mm, the guard explains the new pair contacts; at 1.5 mm, the chord
compensation alone already exceeds most of that extra spacing. The saved complete
controls also become colliding native inputs: their physically legal gaps can be
as tight as kerf + 0.000001 mm. The guards and physical acceptance criteria stay
unchanged.

A local linear construction then minimizes the largest translation, preserving
every original size, rotation, reflection, copy and sheet assignment. It keeps
the original target containers and seeks an additional 0.001 mm native cushion.
The first linear solution breaks another physical contact; that failure and its
solution are retained. A continuation reuses that solution, backtracks against
all original outer contours, and adds newly active contact constraints. All four
stop at the predeclared 20-iteration limit with predicted native gaps of
0.000622–0.000906 mm. **Their extra-cushion criterion remains failed.**

Those saved outputs are independently evaluated by the unchanged native engine.
Actual native loss is zero in all twelve sheet/joined checks. The original public
library/request checks reject only the unchanged missing quantities. Another
**13,566** filled-outer pair checks confirm physical clearances and original stock
targets. All other control inputs reproduce their earlier observations exactly.

| Case | Initial native pair collisions | Initial boundary collisions | Largest coordinate move (mm) | Adjusted native losses: first / last / joined | Completion repair |
| --- | ---: | ---: | ---: | ---: | --- |
| large-plates-k0.2 | 92 | 20 | 0.151779 | 0 / 0 / 0 | expired |
| large-plates-k1.5 | 88 | 16 | 0.158302 | 0 / 0 / 0 | expired |
| panel-hardware-k0.2 | 260 | 30 | 0.178131 | 0 / 0 / 0 | expired |
| panel-hardware-k1.5 | 243 | 27 | 0.162584 | 0 / 0 / 0 | expired |

The same missing original copies are restored at their already-saved deliberate
poses; pose selection is not repeated. Each new complete proposal passes the
original quantity/bounds checks and is rejected for its retained overlaps.
The original repair binary then runs once per changed input on logical CPU 8,
with seed 0 and the unchanged 12-work-second allowance. All four expire at
12.036–12.091 charged seconds (13.385–17.295 real seconds), returning no layout.
These are mechanism tests, not quality runs or proof of infeasibility.

The first geometry audit added native f32 tracker entries using Python binary64
and failed its approximate total check on the last case. The recovery reproduces
the native f32 accumulation order and requires exact totals for every item and
sheet. It reuses the first three completed geometry audits byte-for-byte and
finishes only the missing fourth. No native observation or repair was repeated
to repair that audit. Original failures and extra-cushion shortfalls remain.

[Checks](h5-native-collision-diagnosis-20261018/checks.json),
[all raw geometry, attempts, outputs and source](h5-native-collision-diagnosis-20261018/raw.zip),
[manifest](h5-native-collision-diagnosis-20261018/raw-manifest.json),
[next investigation](h5-native-collision-diagnosis-20261018/source-review.json).
All 482 archive members, CRCs and byte hashes verify.

The saved adjusted partials now start at exactly zero native loss, so do not repeat spacing correction or treat its extra-cushion shortfall as a native collision failure. Restoring the same missing copies still expires all four unchanged repair calls. The helper discards its best snapshot on expiry, leaving the remaining bottleneck unobserved. Next add a test-only terminal-snapshot observer to a fresh isolated source and target, starting with the closest large-plates / 0.2 mm case (three missing cogs). Replay that fixed adjusted input once with the same seed 0 and 12-work-second allowance solely to capture the retained best snapshot, remaining losses, per-part collision partners and sheet assignments before the existing expiry return. Preserve expiry and every original failed outcome; do not accept an expired snapshot or increase any budget. Independently validate its physical geometry even if rejected, so the next constructor or repair proposal addresses the observed obstructions. This is observational diagnosis, not another quality attempt or evidence that the +1% material target is impossible.

Production source and all 172 prior test bodies remain unchanged. The added
observer passes on eight fixed inputs; this does not claim a new regression suite
or full H5 acceptance run. Published preview assets and all three accurate READMEs
remain unchanged; H2/H5 are still open at **60%**.
