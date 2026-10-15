# Native lead-length calibration — 2026-10-15

LightBurn Pro 2.1.01 treats an arc lead's **length as distance along the arc**.
On an outer straight edge, a positive angle gives an exterior arc tangent to the
cut, with sweep equal to that angle and radius `length / angle_in_radians`.
This conflicts with the original plan's `radius = length / 2` rule. Artem
explicitly approved matching LightBurn and updating the plan on 2026-10-15
([decision 3](../../docs/PLAN_V1_1.md#10-reviewed-decisions)).

## Native observations

The [authored SVG](h6-lead-native-calibration-20261014T041122Z/coupon.svg) is a
20 × 10 mm rectangle whose first vertex is halfway along its upper edge.
LightBurn imports it at that exact size. Choose Best Starting Point and Choose
Best Direction are both off for these measurements; lead-out and overcut are off.
Every case is saved as a native project with the actual lead settings and source
vertex order, plus unchanged settings and preview screenshots.

| Native setting | Measurement from preview | Arc-length model |
| --- | ---: | ---: |
| Line, length 3 mm, 45° | 3.032 mm line | 3 mm line |
| Arc, length 3 mm, 45° | radius 3.818 mm | radius 3.819719 mm |
| Arc, length 3 mm, 90° | radius 1.926 mm | radius 1.909859 mm |

The original plan predicted radius 1.5 mm in both arc cases. The observations
reject that interpretation: its radius differs by 2.318 mm and 0.426 mm.
The arc-length model's maximum radial raster residual is 0.024837 mm at 45°
and 0.037652 mm at 90°. These are **raster measurements with a 0.05 mm tolerance**,
not proof of the 0.01 mm vector-fidelity gate or of the final collision envelope.
The rectangle supplies a scale of 34.05 pixels/mm in all three previews.

[Line preview](h6-lead-native-calibration-20261014T041122Z/line45-preview-20261015.png),
[45° arc preview](h6-lead-native-calibration-20261014T041122Z/arc45-preview-20261015.png),
[90° arc preview](h6-lead-native-calibration-20261014T041122Z/arc90-preview-20261015.png).
The [JSON audit](h6-lead-native-calibration-20261014T041122Z/calibration.json)
records native settings, measured bounds, residuals, restored optimization flags
and SHA-256 hashes. Reproduce it with
`python scripts/h6_lead_calibration_audit.py <folder> --out <new-result.json>`.
The audit pins itself to CPU 0 and reads only this authored coupon's files.

## Retained interruptions and failed assumptions

- The folder was created on 2026-10-14. That attempt stopped before a verified
  preview. UI Automation toggled Add Lead-In without enabling its dependent
  fields; three field edits were rejected. Physical off/on clicks enabled them.
  An observation response then lacked the expected structured result. None of
  that attempt is counted as a native geometry measurement.
- On 2026-10-15 Anode initially reported a stale host-not-answering error.
  Reacquiring the lease restored inspection and capture without signing out the
  desktop or closing other applications. No previous LightBurn process remained.
- The new owned LightBurn process showed a low-resolution warning and offered
  an application update. Ignore and No preserved its existing configuration and
  version; only the temporary hidden display was enlarged to 1920 × 1080.
- Opening Preview through UI Automation timed out despite opening the window;
  observing its accessibility tree also timed out. Screenshots confirmed the
  result. Subsequent preview openings used the freshly observed button position.
  No uncertain action was replayed.
- The first exploratory pixel crop included the preview legend, yielding absurd
  fitted radii of 24–33 mm. The final audit explicitly restricts its crop to the
  visible lead, excludes red traversal moves, and checks the rectangle scale.
  It is specific to these screenshots and is not a general image recognizer.

All original optimization flags were restored and compared automatically.
The owned LightBurn process was closed, the original 1280 × 720 display restored,
and the lease released. The source coupon remains unchanged. `coupon.lbrn2` is
the final working save with the restored direction preference; the three
`*-native.lbrn2` measurement copies retain direction optimization off.

## Remaining H6 work

This establishes the straight-edge length interpretation only. Hole leads,
corners, reversed traversal, the zero-angle limit, own-material fit, shortening,
shared-edge exclusion, contour coverage and searched exports still need checks.
The lead planner, search integration and UI/CLI/MCP controls are not implemented.
The three screenshots above are calibration cases, **not** the three nested
exports required by H6. No milestone is complete; weighted progress stays 15%.
