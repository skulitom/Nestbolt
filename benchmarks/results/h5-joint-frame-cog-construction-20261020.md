# H5: joint frame and cog constructions — 2026-10-20

**All eight changed joint models still place nine cogs, six short of the
original requirement.** They finish below their declared limits and report
optimality for their finite candidate sets. All sixteen returned layouts
pass original geometry and fail the frozen CLI only for the cog quantity.
No improved partial, full witness or new release is established.
H2/H5 remain open at 60%.

## New constructions from unresolved frame regions

The [continuous-region audit](h5-single-frame-continuous-regions-20261020.md)
leaves eight single-frame choices unresolved. Each case holds the other fifty
non-cog poses fixed and allows a frame and all cogs to be selected together.
The original frame plus nine cogs remains a complete feasible starting point.
Every compatible old frame/cog candidate is retained, including old positions
outside the pending regions as additional valid finite choices.

The source pool's 9736 entries remain unchanged. New frame proposals come from
the remaining center cells, unioned by axis-size class and eroded by 0.001 mm
for positive construction margin. The canonical 0°/90° frame transforms cover
the two rectangular size classes; retained original poses keep their actual
rotations. New cog translation contacts use phases 0°, 4.5°, 9° and 13.5°
around the fifty fixed parts on both sheets.

Each case declares 120 seconds for generation, at most 600 new frame poses and
1000 new cog poses. Every polygon representative point, boundary vertex and
edge midpoint is processed in a recorded round-robin order. All **80 queries**
and **6,335 proposals** complete without a generation limit or
pending query. Across the eight conditional sets, **853 frame
and 641 cog poses** are added. These are case totals, not a
deduplicated count across cases. All **1,440 rejected proposals**
remain recorded under the original geometry rules.

The independent audit checks **2,181,328 old-candidate/fixed-part pairs**
and **267,796 proposal/fixed-part pairs**. It
reconstructs the frame regions and every sampling order, checks every accepted
and rejected proposal, and retains all eight original feasible seeds.

## Recompute every relevant conflict

No graph conditional on the old 51 fixed parts is reused. Original geometry
independently checks all **5,131,041 eligible same-sheet
frame/cog and cog/cog pairs**, reproducing **2,751,883 conflicts**.
The **38,315 verified cliques** cover every conflict;
no residual pair or compression limit remains.

Frame/frame geometry edges are intentionally omitted because every later model
requires exactly one frame. Those omitted pairs are never treated as geometric
clique evidence. All other pair conflicts are retained.

## Joint models and returned layouts

Each model fixes the fifty retained non-cog poses, requires exactly one frame,
and maximizes cogs from the known feasible nine through the original fifteen.
Every protobuf field, quantity constraint, objective and complete hint is
independently reconstructed before solving. Each case gets one 20-second
maximum, eight workers and seed zero, with no retry.

| Released frame | Frame choices | Cog choices | Seconds | Reported cog optimum |
| --- | ---: | ---: | ---: | ---: |
| 7835 | 224 | 1229 | 1.442912700 | 9 |
| 8895 | 107 | 1127 | 0.795694800 | 9 |
| 8896 | 105 | 1128 | 0.802788300 | 9 |
| 8897 | 105 | 1090 | 0.779464100 | 9 |
| 8898 | 229 | 1091 | 1.158131700 | 9 |
| 9057 | 260 | 1309 | 1.412562000 | 9 |
| 9178 | 210 | 1134 | 0.985501600 | 9 |
| 9233 | 231 | 1224 | 0.998900600 | 9 |

All eight runs return `OPTIMAL`, each with one callback and a distinct final
selection. The final count remains nine in every case. This is solver-reported
finite-pool optimality; it does not certify arbitrary continuous layouts or
prove that multiple non-cog moves are necessary.

All **16 layouts** receive independent original-outline, rotation, stock,
clearance and quantity checks. Twelve frozen CLI calls are fresh; four reuse
the exact original layout and hash-recorded result. Every CLI result fails
only with `part cog: expected 15, found 9`.

Every layout retains all 18 frames, 12 brackets and 21 inserts. Material charge
remains **4,985,103.45 mm²**, but the missing cogs invalidate the original job.
Filled area remains **4,181,364.4704 mm²**, with no improvement over this seed
or the previously documented better partials. Minimum clearances include
0.200100 mm; no native-margin qualification is claimed. The returned optima
use retained source poses rather than the new contacts.

## Source and next work

Core source and all three README hashes remain unchanged. The README accurately
describes the published preview and remaining work; no new release is qualified.
No native packing, quality run or reserved held-out evaluation occurs.

All six checks on remote 7c47f498 pass in the saved snapshot.

Do not rerun these eight joint single-frame models unchanged or resume the expired spatial tree. Their complete finite-pool optima remain nine cogs, and none of the new contact poses improves the returned count. Next investigate a coordinated whole-group construction: review the already audited complete frame groups, then allow bracket, insert and cog positions to be selected together instead of keeping either the51 non-cog set or one of the four old cog arrangements fixed. Choose a changed group or candidate construction from the original geometry after checking prior group results, declare its finite generation/solve limits, retain a valid partial baseline where available and independently recompute all relevant conflicts. An original66-copy witness, native margins and unchanged H5 material/cutting gates remain required; no single-part finite optimum proves unrestricted impossibility.

[Checks](h5-joint-frame-cog-construction-20261020/checks.json), [generation](h5-joint-frame-cog-construction-20261020/generation-results.json),
[independent candidates and graphs](h5-joint-frame-cog-construction-20261020/candidate-and-graph-audit.json),
[model audits](h5-joint-frame-cog-construction-20261020/model-audits.json), [solver results](h5-joint-frame-cog-construction-20261020/solver-results.json),
[all layout checks](h5-joint-frame-cog-construction-20261020/layout-audit.json), [source review](h5-joint-frame-cog-construction-20261020/source-review.json),
[remote checks](h5-joint-frame-cog-construction-20261020/main-ci-7c47f498.json), [raw evidence](h5-joint-frame-cog-construction-20261020/raw.zip)
and [manifest](h5-joint-frame-cog-construction-20261020/raw-manifest.json).
All 362 archive members, CRCs and byte hashes verify.
