# H5: continuous occupied-area relaxation — 2026-10-25

**The area bounds exclude none of the seven fixed arrangements.** Each bound
exceeds the 895,800 mm² needed by all 12 brackets and 21 inserts. This is
inconclusive: the pointwise union ignores competition between small parts,
so the excess area is not evidence that the inventory packs. No new layout
or solver call is produced. H2/H5 remain open at **60%** completed weight.

## Continuous coverage and independent audit

Keep each saved 18-frame/15-cog arrangement fixed. Relax positive clearance
to zero and expand stock bounds by 0.001 mm. Exact convex-piece Minkowski
sums form the original-outline forbidden translations; shrinking that union
removes only forbidden material. For every intersecting 50 mm grid cell,
an outward-padded convex hull covers the entire clipped translation region.
Minkowski sums of those hulls and the moving part cover every occupied point.
Clip to expanded stock after excluding only a subset of fixed material,
then union orientations, families and sheets. Holes remain reserved.

All **168** queries (seven cores, twelve permitted rotation/reflection classes,
two sheets) finish in **7.873071 seconds**, within the declared
120 seconds. All four insert quarter turns are included. No query is pending.
The independent audit takes **12.513682 seconds** and checks:

- Eleven input files against the previous committed evidence manifest.
- All 48 cached forbidden polygons, using 1,280 convex-piece vertex sums.
- All translation domains, exclusions, 6,543 grid hulls and 8,683 swept sums.
- All seven complete family/combined aggregates.
- **99,983** compatible original-polygon memberships and the corresponding
  original translations, covering 17,481 saved variable poses.
- Both 64-part and both 63-part baselines, without changing their placements.

| Fixed core | Combined upper area (mm²) | Excess over full small inventory (mm²) |
| --- | ---: | ---: |
| 0 | 1,041,279.453 | 145,479.453 |
| 1 | 1,041,304.926 | 145,504.926 |
| 2 | 1,040,983.871 | 145,183.871 |
| 3 | 1,039,050.212 | 143,250.212 |
| 4 | 1,022,067.245 | 126,267.245 |
| 5 | 1,048,539.198 | 152,739.198 |
| 6 | 1,041,545.148 | 145,745.148 |

Both family-specific bounds also exceed their required areas. These results
do not prove that a fixed arrangement must move, that the target is impossible,
or that more finite pose sampling will succeed. No area-grid refinement or
completed solver retry is used to force a different conclusion.

## Preserved audit failure

The first audit directory contains its script and plan but no result; its
terminal output was unavailable after the interruption and no process remained.
A separately recorded diagnostic verification reproduces an assertion that
assumed a polygonal negative round offset always provides its full nominal
0.001 mm inward distance. The actual minimum is
**0.000992935159 mm**.

The verified checker instead proves the necessary subset condition and records
the measured inward distance. Removing a subset of forbidden material enlarges
this relaxation regardless of the exact shrink distance. The saved construction
is unchanged. The failed checker, reproduced traceback and repaired checker
are all retained; the original result's pending-audit flag is preserved, with
the completed audit stored separately. This correction supplies no acceptance
clearance and makes no negative feasibility claim.

## Select a useful direct-coordinate investigation

The original-source conversion guard is 0.011444091796875 mm; the compensated
sheet-search separation is 0.21170867250963943 mm. Measuring all fixed-core
original polygons identifies **core 0 alone** as passing the sufficient pair
and stock distance screen: its minimum pair gap is 0.2126 mm and additional
stock margin is 0.0126 mm. Core 5 meets the pair screen but has only 0.0001 mm
stock margin. The other cores miss at least the pair screen. This is a geometric
screen, not an actual native transformed-collision acceptance.

Build a fresh direct-coordinate feasibility model for every original small part against fixed core 0, the only saved core passing the source-derived conservative pair and stock distance screen. Keep the other cores and all four baselines preserved as evidence. Permit all original bracket rotations/reflections and all insert quarter turns, with equivalent normalized rectangle rotations explicitly accounted for. Require exactly 12 brackets and 21 inserts, together with the unchanged 18 frames and 15 cogs; no partial objective. Use a declared 0.01 mm coordinate grid, at least 0.22 mm new-part separation and 0.02 mm extra stock margin, and independently checked inward-rounded convex safe translation domains. Represent an L bracket by its two exact rectangular arms; apply directional nonoverlap only across different physical parts, never between its own arms. Inspect the earlier macro-rectangle and finite-pose exact-inventory models to preserve their failures and distinguish this model. Declare construction and one solver limit before execution; retain incomplete construction and UNKNOWN without extending or restarting completed searches. Any full witness still requires original geometry, public CLI, actual native transformed-collision checks, original production-budget qualification and the full 13-job/two-kerf matrix. This grid/subdomain model may miss placements and cannot establish unrestricted impossibility. Do not refine the completed area grid simply to seek a negative bound, resume old capped pose lists, weaken inventory or change H2.

## Repository and scope

Engine source and all three accurate READMEs are unchanged. The published
preview remains v0.2.0-alpha.1 and stable Latest remains v0.1.0; this audit
does not qualify another release. Main 55835d7c's hosted checks are captured
as `in_progress` / `pending`. No native packing,
production quality matrix, registry publication or held-out evaluation occurs.
The original 66-part count, material target, native guard, production budget
and full 13-job/two-kerf H5 requirement are retained. H2's October 20 decision
to keep its original gate open is unchanged.

Evidence: [plan](h5-occupied-area-relaxation-20261025/plan.json), [construction](h5-occupied-area-relaxation-20261025/result.json),
[independent audit](h5-occupied-area-relaxation-20261025/audit.json), [source provenance](h5-occupied-area-relaxation-20261025/provenance.json),
[failure recovery](h5-occupied-area-relaxation-20261025/audit-recovery.json), [fixed-core margins](h5-occupied-area-relaxation-20261025/core-margins.json),
[source review](h5-occupied-area-relaxation-20261025/source-review.json), [manifest](h5-occupied-area-relaxation-20261025/raw-manifest.json)
and [raw archive](h5-occupied-area-relaxation-20261025/raw-001.zip). All 283 canonical
members and 10 aliases retain their exact bytes,
with CRC and SHA-256 verification.
