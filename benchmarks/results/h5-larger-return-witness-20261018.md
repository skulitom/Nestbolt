# Pair exchange with larger returned area — 2026-10-18

Two incoming rectangles, 30x40 and 30x50 mm, can exchange with three 30x31 mm
rectangles while preserving all seven parts and exactly 19,700 mm2 charged
material. The returning group has **2,790 mm2**, exceeding the incoming
group's **2,700 mm2**. Both authored layouts pass the frozen public CLI and
independent filled-outer, spacing, edge and quantity checks. All metrics are
identical. No optimizer run occurs.

A 60x94 mm filler stays on each 100x100 mm sheet. With the one-millimetre edge
inset, at most 38 mm combined side width and 4 mm combined top/bottom height
remain around a filler. These 30 mm wide small parts therefore need one side
lane no higher than 98 mm, even if the filler moves. Either incoming part
moving alone, with any zero-to-three return count, makes a height sum exceed
98 mm on at least one sheet. All eight conservative bounds are recorded.
Moving both incoming parts needs 90.2 mm; the returns need 93.4 mm, including
the required 0.2 mm spacing. The authored coordinates satisfy both. Leaving
one return with the incoming pair would need at least 121 mm before spacing.

The current paired proposal rule rejects a complete return set when its area
exceeds incoming area. This witness shows that rule can exclude a valid
exchange with unchanged material. It does not show that allowing the exchange
improves a mechanical workload. An actual original-runtime regression and
complete candidate/quality checks remain necessary before any integration.
Whole-job geometry, quantity, pose and strict material guards must remain.

[Checks and conservative bounds](h5-larger-return-witness-20261018/checks.json),
[before](h5-larger-return-witness-20261018/before.json),
[after](h5-larger-return-witness-20261018/larger-return-after.json) and
[integrity](h5-larger-return-witness-20261018/integrity.json) retain all evidence.
This scoped witness makes no global infeasibility or H5 claim. Production and
reserved inputs are unchanged; completed milestone weight remains 60%.
