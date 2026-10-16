# Isolated score-bound granularity candidate — 2026-10-16

The integrated preview's Chrome subset remains a failure at +1.046217% against
the unchanged +1% limit. Its original Firefox measurement continues. No release
is tagged, no production code is changed, and completed milestone weight is 45%.

This separate candidate checks the same monotone collision-score lower bound
after each eight pole pairs, including a partial final chunk, instead of after
an entire row. It keeps pole accumulation order, accepted-score arithmetic,
strict tie handling, the infinite-bound path, geometry, work charges, deadlines,
defaults and dependencies. Earlier profiles motivate reducing collision-scoring
work; extra bound checks might instead cost time. No benefit is established.

The [checks](h4-score-chunks-preparation-20261016/checks.json) pass in debug and
optimized builds. Two relevant tests compare 5,760 reference-score/bound
combinations and complete candidate evaluation with items, fixed blockers and
sheet boundaries. Explicit fixture pole counts of 16 and 15 exercise both full
and partial eight-pair chunks. The third filtered test is an unrelated existing
arc regression. Formatting, strict core-library lint, CLI/WASM builds, browser
types and the isolated browser bundle also pass on CCD1. A unique Cargo target
avoids the separately recorded shared-cache problem from the H5 preparation.

A cp1252 console error occurred while printing the successful Vite build log,
after its zero exit code and log hash had been saved. The subsequent sealer
refused the missing final metadata. Both failures and the original helper are
retained. A separate verifier checked all eight saved stages, original source
guards and outputs, then completed only that metadata; no build was repeated.

The [committed measurement plan](h4-score-chunks-probe-20261016/plan.json) first
requires eight independently valid native results in four exact equal-work
pairs: public letters and development gear-1, seeds 0/1, 20 work seconds and a
120-second hard deadline, two separate physical CCD0 cores. Every result field
except elapsed wall time must agree. Their timing is diagnostic, with no speed
claim. If these pass, one 99-attempt H4 subset follows: eleven jobs, seeds 0–2,
60 seconds, native/Chrome/Firefox, eight physical cores and the existing +1%
median/+5% per-job limits. It cannot start until the original preview matrix is
complete and sealed. A one-use marker prevents rerunning an opened plan.

Full G5, the 65-job native comparison, scale confirmation and integration checks
remain separate. No held-out geometry is read and no quality gate is waived.

The [raw archive](h4-score-chunks-preparation-20261016/raw.zip) retains 251 members,
5,487,426 bytes, SHA-256
`31cf348ebf55883cad32341938c72be0d2aa7e80dafd621cebc1b7e459e90003`.
CRC, every member size and every SHA-256 were checked against the
[inventory](h4-score-chunks-preparation-20261016/integrity.json). It includes the
isolated source, exact CLI/WASM/site, test/build logs, earlier candidate snapshots,
failure record, helper scripts and unmeasured runner.
