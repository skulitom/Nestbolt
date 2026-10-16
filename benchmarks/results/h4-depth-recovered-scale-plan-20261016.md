# Recovery-aware H4 scale continuation — 2026-10-16

The [committed sequence](h4-depth-recovered-scale-plan-20261016/plan.json)
waits for the missing Firefox phase, verifies and archives the recovered full
comparison, then reports its actual outcome. It retains 402 completed native
and Chrome outcomes, adds only the 201 missing Firefox outcomes, and retains
195 frozen-v1 outcomes. The original servicing interruption and its unused
scale sequence remain unchanged.

Only a passing full comparison proceeds to the existing curves and G5 scale
workflows, sequentially, with the unchanged build, fixtures, automatic worker
selection, 60-second budgets and original memory/responsiveness limits.
Curves use Quick initial layout; G5 does not. After both workflows pass,
the independent reader checks every saved SVG/DXF curve and control point
for all 2,000 placements in each browser against the original source geometry,
within 0.01 mm. It does not regenerate exports or repeat searches.

Helper sources and hashes are captured before starting. The recovered
comparison's report records the Firefox recovery duration separately and
does not claim a continuous completed original session. Screenshot inspection,
archive sealing and a complete H4 requirement audit remain separate steps.
No reserved inputs are read, no other measured work overlaps, no release is
created and no gate is closed. Completed milestone weight stays **45%**.
