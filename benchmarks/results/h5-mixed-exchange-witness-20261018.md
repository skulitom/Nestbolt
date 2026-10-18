# Mixed-dimension exchange witness — 2026-10-18

Two distinct incoming rectangles, **30 × 40 mm and 30 × 50 mm**, can trade
places with three 30 × 30 mm squares. A 60 × 94 mm filler remains on each
100 × 100 mm sheet. Both authored layouts independently validate, contain
all seven parts, and use exactly 19,700 mm2 of charged material. The exchange
preserves 2,700 mm2 of incoming/returned area. It is a useful assignment change
without immediate material reduction, so the existing changed-inventory
nonincrease rule should continue to allow it.

The frozen public CLI checks both layouts. Shapely separately verifies every
filled outer ring, pair spacing, edge inset and quantity. Rotations are fixed
to zero and mirroring is disabled. No optimizer or performance run occurs.

With one filler on each sheet, the remaining combined side width is 38 mm,
less than the 60 mm needed for two lanes of these 30 mm wide parts. The total
space above and below the filler is only 4 mm, less than every small part's
height. Therefore the small parts must stack in one side lane, whose usable
height cannot exceed 98 mm, even if the filler moves. For either chosen
incoming rectangle and each possible return count from zero to three, at
least one sheet's height sum exceeds 98 mm, ignoring positive clearance
conservatively. All eight explicit bounds are in [checks](h5-mixed-exchange-witness-20261018/checks.json).

The paired height sums are 90.2 mm for the two rectangles and 90.4 mm for
the three squares, including 0.2 mm spacing; the authored coordinates fit.
The current same-original-item pair selector cannot select the two distinct
incoming parts together. A new mixed-pair candidate still needs an actual
regression against that runtime, allowed-pose/rollback checks, and the
unchanged paired quality comparison.

This restricted assignment witness does not rule out other selected parts
or global layouts, prove usefulness on the mechanical jobs, or meet H5.
Original failures and the full 13-job material/cutting requirements remain.
H2/H5 stay open at 60% completed weight.
