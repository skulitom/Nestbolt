# Actual joint-repair diagnosis — 2026-10-18

**Extra-member migration works, but most observed gains are small and panel lowering does not reduce height.**

Four serial diagnostics retain the two mechanical development jobs, both
kerfs, seed zero, 60 seconds and physical CCD0 CPU 8. The qualified observer
preserves decision logic, deadlines and charged work. Logging can change wall
trajectories; these are diagnostic observations, not a quality or speed comparison.
The session takes 4.088 minutes. All four final layouts and public exports validate.

## What happened

Fifteen joint attempts produce ten completed repairs and five expiries:
three during separation and two during source lowering. Five completed
repairs commit; five are rejected because whole-job material increases.
The material increase itself is observed; concurrent expiry is not sampled
separately on that short-circuit branch. Eight completed repairs change the
source inventory beyond the initial swap, including all five accepted repairs.
Net part-type counts can miss same-family copy swaps that cancel.

| Job | Kerf | Attempts | Completed | Committed | Material-increase rejection | Expired |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 2 | 2 | 2 | 0 | 0 |
| m-mechanical-large-plates | 1.5 | 6 | 4 | 3 | 1 | 2 |
| m-mechanical-panel-hardware | 0.2 | 4 | 3 | 0 | 3 | 1 |
| m-mechanical-panel-hardware | 1.5 | 3 | 1 | 0 | 1 | 2 |

The five committed step gains are **455.576, 33,589.956, 124.047,
512.421 and 982.543 mm²**. They are individual before/after differences,
not a claim about final pilot improvement or an additive whole-job saving.
All six observed panel lowering stages leave the source top unchanged, even
though four change between four and eleven source poses. Two other lowering
stages expire without moving a source pose.

Two panel trials with unchanged source inventories increase material by only
0.00375 and 0.0025 mm². Independent reconstruction reproduces the exact
validator values. They remain rejections; no tolerance or scoring exception
is introduced. Their selected and returned groups are both pairs of inserts.
The same-part swap by itself does not demonstrate useful inventory progress.

## Verified geometry and next target

All 40 unique saved baselines, trials, repaired pairs and final layouts
independently validate. The filled-outer audit checks 173,333 pairs
at the unchanged 1e-7 mm tolerance. All 21 whole-job material values are
recomputed exactly from original transformed outer vertices and stock dimensions.
Nonselected and frozen sheets remain exact. Component pair checks use selected
quantities and full original stock geometry; original whole-job availability
and the native exact-crop checks remain separately authoritative.

Exact physical-pose matching identifies the selected copies. Twelve of the
fifteen selections expose a lower source boundary when removed, ranging from
0.082271 to 22.456299 mm. Four panel selections expose 10.901367 mm.
These are conditional geometric opportunities before returned members are
placed, not constructed layouts or proof of achievable saving.

The next distinct hypothesis is a source boundary derived from the actual selected copies. When removing the selected top copies exposes a lower boundary, use the existing fitted-container calculation on that remaining source as an explicit target for joint repair. Displaced return members must fit below that target or migrate to the receiver, with both exact containers and the original whole job validated. The current joint helper receives the original window crop and can finish immediately after returning equal inserts to the just-vacated top band. In the panel traces, the selected top pair exposes a 10.901367 mm band, but all six lowering stages leave the source top unchanged. This motivates a target; it does not prove the returned parts fit or that the search will find a packing. First author or capture a case where existing repair restores the top band and actual targeted joint repair finds an independently valid lower layout. Preserve the short phase, total deadline, validation reserve, cap, exact crop checks, quantity/orientation accounting, frozen sheets, reserved holes, strict final material guard and rollback. Qualify that changed policy before another matched pilot. Do not relax the material guard for the tiny increases, repeat the unchanged quality pilot or increase the cap blindly.

[All observations](h5-joint-observer-20261018/observed-exchanges.json),
[independent geometry](h5-joint-observer-20261018/geometry-checks/checks.json),
[selected-copy frontiers](h5-joint-observer-20261018/source-frontiers.json),
[interpretation](h5-joint-observer-20261018/interpretation.json) and
[original archive verification](h5-joint-observer-20261018/verification.json).

All six hosted checks on main `e0945cd` pass, including Windows, Linux,
browsers and both maker rebuilds. That confirms the pushed checkpoint,
not the quality of this isolated experiment. [Hosted checks](h5-joint-observer-20261018/main-ci-e0945cd.json).
Production and v0.2.0-alpha.1 remain unchanged. All three READMEs remain
accurate; no new qualified application build is ready to release.
H2/H5 remain open, with completed milestone weight 60%.
