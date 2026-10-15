# H4 letters and gears scale fixture

The frozen drawing contains two letters and two gears from the existing browser
examples. Set each quantity to 500 for 2,000 parts. The manifest pins the drawing,
both source drawings and the generator. It is a development fixture, with no
held-out geometry.

Use 1250 × 2500 mm sheets, the app's 5 mm margins, 1.5 mm part and edge spacing,
quarter-turn rotations, no mirroring, seed 0 and a 60-second search. Keep the
app's default workers (four selected, capped at two for this quantity).

The letters retain their original quadratic curves. The source gears represent
their outlines as dense polylines; they are not newly approximated curves. The
four imported outer proxies have 527, 224, 792 and 792 vertices respectively,
plus holes. Exports must retain the original drawing segments.

Attribution and licence terms are in
[the shipped examples' licence record](../../../web/public/examples/LICENSES.txt).
The letters use the existing DejaVu/Bitstream Vera outlined geometry; the gears
derive from Steren's public-domain/CC0 Openclipart gear. No font file is included.

`scripts/h4_scale_fixture.py` creates the fixture once and refuses to replace an
existing directory. `python scripts/h4_scale.py` checks its hashes, drives the
actual app in Chrome and Firefox, and retains outcomes, process-tree memory,
responsiveness telemetry and downloaded files. A saved layout is independently
validated with the native CLI. Failed nesting is a failed scale case even when
import, memory or responsiveness pass.
