# H5: joint insert/cog geometry for the paired strip — 2026-10-26

**The joint model now requires both remaining inserts and all fifteen cogs.**
Its full geometry and model audits pass, but the single bounded call closes
UNKNOWN after search. It provides no source placement or neighborhood exclusion.
H2/H5 remain open at 60% by completed milestone weights.

## Complete current-owner geometry

Keep the checked 34-original first-sheet core and all fifteen short-sheet
originals. Inserts48/49 and cogs51..65 remain mandatory, accounting for every
one of the 66 originals once. No previously fixed owner is silently moved.

The prior exact clipped footprints contain 1,067 integer rectangles. Coalescing
only matching transverse intervals with overlapping or adjacent integer extents
reduces these to **29 domains**. Independent partitioning verifies **3,632 integer
atoms**, proving exact coverage of each assigned union. No possible floor-rounded
cog center is lost. Integer tiles with diagonal below the certified 254.297 mm
separation give valid domain capacities, while exact farthest corners prove
**85 conflicts** among capacity-one domains.

Each insert may use all four original quarter turns and a continuous ideal
anchor represented by its integer floor. Fresh exact trigonometric intervals
check **16 corners and 64 source edges** across every fractional anchor in
closed [0,1]² micrometres. A 4-micrometre inset keeps each model rectangle inside
its true filled outer; a 20-micrometre outward stock relaxation covers rounding
and angle error. The two moving inner rectangles and **24 current required-clearance
regions** obey global two-dimensional nonoverlap. Only intrinsic shape certificates
are reused; older fixed-owner coordinates are not transferred.

Each insert inner rectangle contains a circle of radius 54.996 mm. Together with
the cog's certified 109.115 mm inner disk and rounding allowance, this requires
at least 164.109 mm between the rounded cog center and the insert's model-circle
center. Exact scaling and downward facet rounding keep a 32-gon inside that
forbidden disk. The original certified 32-gon supplies the 254.297 mm cog/cog
necessity. Both are permissive bounds, not substitute source shapes.

## Full joint model audit

| Required relation | Count |
| --- | ---: |
| Mandatory inserts / cogs | 2 / 15 |
| Cog choices among complete domains | 435 |
| Cog/cog separation pairs | 105 |
| Cog/insert inner-circle pairs | 30 |
| Cog/insert support strips | 60 |
| Exact rational support-vertex boxes | 840 |

The model has **8,440 variables and 10,044 constraints**, with no objective or
hints. The independent auditor reconstructs every variable domain, mode table,
interval, stock row, occupancy count, conflict and outside-box/facet choice by
semantic name, without trusting the saved mapping. It checks integer arithmetic
bounds and the solver's actual import/export. Equal copies may be relabelled in
nondecreasing X, preserving feasible source geometry. All seventeen movers are
required throughout; the inserts are no longer omitted from this necessary test.

## One closed call

The sole 60-second solver call, inside 90 shared seconds, returns **UNKNOWN**.
Internal solver time is **60.052053 seconds**, returned-call time **60.060177
seconds**, and total shared-process time **60.999099 seconds**. Internal/returned
soft overruns of 0.052053/0.060177 seconds are preserved; the shared limit is
honored. Search advances beyond presolve, with all three primary workers
recording branches. The returned worker reports **1,526,058 branches and 250,475
conflicts**. Separate worker counters and the original response remain archived.

There is no solution assignment, source witness or formal unsat certificate.
The call is closed: no retry, reseed or extension. A future positive necessary
result would still need actual original cog angles, guarded source geometry,
full66 native/material validation, production integration within 60 seconds and
the complete H5 matrix. The next useful construction must change the core or
introduce materially different original-shape joint geometry. Preserve the
earlier 64-original partial and the alternative 49-original core.

## Repository and evidence

All three audits pass, with no failed checker attempts. At 2026-10-26T17:05:14.027139+00:00,
[all six checks on main cb7f7b1f](https://github.com/skulitom/Nestbolt/actions/runs/40359411459)
pass. This permits a normal two-commit push of the queued 183a160a checkpoint and
this evidence after staging and ancestry checks. Upstream heads and releases
remain unchanged. Production and READMEs are unchanged; no new release qualifies.
H2 retains its original gate and all 22 reserved vectors remain untouched.

[Checks](h5-paired-strip-joint-geometry-20261026/checks.json), [geometry](h5-paired-strip-joint-geometry-20261026/joint-geometry-checks.json),
[model](h5-paired-strip-joint-geometry-20261026/joint-model-checks.json), [response](h5-paired-strip-joint-geometry-20261026/joint-response-checks.json),
[geometry proof](h5-paired-strip-joint-geometry-20261026/geometry-necessity-proof.json),
[model proof](h5-paired-strip-joint-geometry-20261026/model-necessity-proof.json), [scope](h5-paired-strip-joint-geometry-20261026/scope.json),
[inventory](h5-paired-strip-joint-geometry-20261026/all66-inventory.json), [next step](h5-paired-strip-joint-geometry-20261026/next-step.json),
and [raw manifest](h5-paired-strip-joint-geometry-20261026/raw-manifest.json).
The archive verifies 57 canonical files and
23 aliases by bytes, SHA-256 and CRC.
