# Directed-exchange repair diagnosis preparation — 2026-10-16

**The isolated diagnostic build and authored trace checks pass. No measured searches yet.**

The [rejected early-call pilot](h5-early-exchange-pilot-20261016.md) reached 179
proposals and accepted ten exchanges, but five of eight material pairs failed.
Its counters did not identify which repair or acceptance stage rejected a proposal.
This copy adds per-invocation reporting of receiver repair, source repair,
deadline, independent geometry and material-guard outcomes. Proposal generation,
repair logic, budgets and acceptance remain unchanged. Tracing may affect wall
time, so the diagnostic cannot establish performance or quality improvement.

Only the isolated exchange module changes. The prior candidate and production
sources retain their hashes. A unique build target prevents cross-workspace
cache reuse. All 82 optimized core tests, strict lint and observer build pass.
Three authored trace checks distinguish an accepted exchange, a failed source
repair and expired/disabled no-work behavior. Source before/after formatting,
both complete source copies, logs, exact binary and helpers remain archived.
CRC, every member size and every SHA-256 are verified.

[Build](h5-exchange-diagnosis-preparation-20261016/build.json),
[trace checks](h5-exchange-diagnosis-preparation-20261016/trace-checks.json),
[raw archive](h5-exchange-diagnosis-preparation-20261016/raw.zip),
[integrity](h5-exchange-diagnosis-preparation-20261016/integrity.json).

The planned diagnostic fixes the two mechanical jobs, both kerfs, seed 0 and
60 seconds, serially on physical CCD0 CPU 8. It waits for the H4 tree-depth
pilot to finish and be sealed, and for its own plan to be committed. Every
layout is independently validated and exported; all traces and failures stay.
No original failed result is replaced or rescored. No held-out geometry is read.
H5 remains open, the candidate is not integrated, and completion stays 45%.
