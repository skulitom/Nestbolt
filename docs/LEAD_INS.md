# Lead-in allowances

Enable **Lead-in allowances** in the browser settings, add `lead_in` to the
CLI/MCP request, or pass `nest --lead-in --kerf 0.2`. Leads reserve space and set
contour starts; the exported red **LEADIN** paths are for review. The cutting
program generates the actual leads.

```json
"lead_in": {
  "kerf_mm": 0.2,
  "length_mm": 3.0,
  "style": "arc",
  "outer_angle_degrees": 45.0,
  "hole_angle_degrees": 90.0
}
```

Only `kerf_mm` is required. Defaults are length 3 mm, style `line`, outer angle
45° and hole angle 90°. Kerf must be positive (maximum 1000 mm); length must be
0.5–50 mm; angle magnitudes must be 0–90°. Arc length follows LightBurn:
`radius = length / abs(angle in radians)`, with a straight limit at zero angle.
This replaces the original fixed-radius assumption under
[plan decision 3](PLAN_V1_1.md#10-reviewed-decisions).

The CLI overrides are `--lead-length`, `--lead-style line|arc`,
`--lead-outer-angle` and `--lead-hole-angle`. Supply them with `--lead-in` and
`--kerf`. `--common-line` can be enabled together with leads; both features must
use the same physical kerf. The browser keeps their kerf controls synchronized.

## Placement and reports

The search reserves both possible cutting directions, including the half-kerf
stroke and a pierce disc whose diameter is twice the kerf. It uses enlarged
collision geometry but scores original part area. Lead waste never counts as
useful part area in either fill mode. The final report recomputes stock use and
the trailing offcut from original parts plus the actual final lead footprints.

Starts prefer outer convex corners, then long straight edges, then curves.
Hole starts favour a long straight edge or a point toward the interior of a
smooth hole. Leads shorten in trials down to 0.5 mm. Each trial rounds its length
down to 0.001 mm before constructing the path, so the reported three-decimal
setting describes the actual reserved lead. Each placed contour has
one reservation or an explicit flag; a flag means the tested candidates did
not fit, not a proof that every conceivable start is impossible.

After placement, each copy is checked against stock, other copies and leads.
Starts on that copy's actual common-line segments are excluded and tried again.
Unused initial reservations remain conservative obstacles when choosing new
starts; this can flag a contour whose space could be recovered by moving parts.
Existing valid layouts can also acquire leads by reselecting starts, shortening,
or reporting flags. Standalone export recomputes this plan from the source
request and layout, rather than trusting saved report JSON.

`report.json` and MCP/browser results include `lead_in` with options, expected,
reserved and flagged contour counts, and one record per placed copy. Each record
lists source contour indices, exact start parameters, actual lengths, shortened
status, analytic paths for both directions, flags and world-space bounds. Indices
are zero based in JSON; the browser displays copy and contour numbers starting
at one. Browser previews draw one lead direction in red and include all reserved
space in the offcut extent.

Validate a public request including its leads with:

```sh
nestbolt validate --library library.json --request run/request.json --layout run/layout.json
```

`validate --job ... --layout ...` remains the polygon-job checker; it has no
lead settings. MCP `validate_layout` and browser validation use the request,
return the final lead report and include reserved space in material metrics.

## LightBurn setup

1. Keep **Choose best starting point** off. Both cutting directions have reserved
   space, so the checked coupons allowed **Choose best direction**.
2. Disable output for **LEADIN / C02**. It shows the allowance; it is not another
   cut to run. Disable the sheet-outline layer too. SVG/DXF sheet colours can map
   to C05 in LightBurn; colour alone does not guarantee a Tool layer.
3. Configure native leads with the reported style and length. Outer angle signs
   are positive and hole angle signs negative. The angle fields above are
   magnitudes. Keep lead-out and overcut off; those paths are not reserved.
4. Assign separate cut settings to contours with different angles or lengths.
   In particular, the defaults use different outer and hole angles. Apply every
   shortened length from the report. For flagged contours, disable that native
   lead or adjust its start manually and inspect the result.
5. Review the native preview before cutting. Automatic start changes, new lead
   settings, added overcut or moved geometry invalidate the checked allowance.

The [three searched native coupons](../benchmarks/results/h6-lead-planner-checkpoint-20261015.md)
verified line/arc previews and 24 contour starts in LightBurn Pro 2.1.01. Each
coupon used one angle for outer and hole contours. The separate-layer workflow
for different defaults and shortened lengths still needs its native check.

## Current scope

SVG/DXF cutting parts with one outer contour and optional holes are supported.
Editable LightBurn projects and rigid units with several disconnected components
are explicitly rejected by the lead planner; normal preserving project exports
remain available without lead overrides. Multi-component planning, the broader
independent final coverage/owner audit and material-cost measurements on the
common-line development set remain unfinished. These public controls and tests
are a development checkpoint, not completion of H6 or a new quality claim.
