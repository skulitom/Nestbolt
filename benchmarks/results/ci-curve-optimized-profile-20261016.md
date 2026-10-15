# Curve repair with optimized engine crates — 2026-10-16

The isolated hole-index repair passes the exact Linux CI failure and **128
generated curve cases** with core, validator and dependencies at `opt-level=3`
and debug assertions enabled. This addresses the optimization-profile limitation
of the [first isolated probe](ci-curve-flat-index-probe-20261016.md). Production
integration, full regression checks and measured performance remain required.

The candidate is the [native diagnostic prototype](h2-native-diagnostics-candidate-20261016.md):
only its hole grouping index differs in search behaviour. The three reader
message changes do not affect these SVG inputs. All source hashes match that
prototype's inventory. Every used dependency has the production lock's exact
version, source and checksum.

The exact input is unchanged: job SHA-256
`cb3a509cba4751e1e4992a7391264bbffb312a21cd8324e25232e14fbafe564e`.
Seed 659 and the original two-second work budget produce all **eight requested
placements**, independently valid with zero overlap or outside-area violations.
The standalone harness calls the independent validator again before reporting
success. The original optimized-release success and debug failure remain
preserved; this result does not erase either one.

The expanded `random_curved_svg_parts_nest_validly` property uses the same fixed
generation seed, `20261016`, and 128 cases. All pass. As in the original property,
a generated request may return an independently valid layout or a clean error;
this is not a claim that all 128 requests produced layouts. No timing or quality
comparison is inferred from the test's elapsed time.

A separate [authored regression](ci-curve-optimized-profile-20261016/hole_index_regression.rs)
is ready for integration with its exact generated SVG fixture. It requires a
successful result with all eight placements and independent validation, rather
than accepting a clean error. It keeps the original work budget and seed while
allowing ten seconds of real time on a slower CI machine. That test also passes.
Its [record](ci-curve-optimized-profile-20261016/authored-regression.json) identifies
the observed tool output and source/fixture hashes; no separate raw log was
captured for this final authored test.

[Complete checks](ci-curve-optimized-profile-20261016/checks.json),
[expanded property output](ci-curve-optimized-profile-20261016/curves-128-stdout.log),
[build/test diagnostics](ci-curve-optimized-profile-20261016/curves-128-stderr.log)
and [source/artifact inventory](ci-curve-optimized-profile-20261016/integrity.json)
retain the original probe and full captured output. The authored regression was
added afterwards and has its own record, without changing that inventory.
Scripts are snapshots executed from `output/`. These functional checks ran on
CCD1; no reserved inputs or measured searches were opened. The running H4
production source, binaries, site and runner guards remained unchanged.
