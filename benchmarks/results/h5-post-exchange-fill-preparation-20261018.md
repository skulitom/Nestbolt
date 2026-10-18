# Gap filling after accepted exchanges — preparation, 2026-10-18

The [identity/stage diagnosis](h5-balanced-stage-20261018.md) found three
accepted exchanges with no immediate material/extent decrease. Two preserved
per-sheet inventory. Source inspection showed that any accepted exchange
short-circuited the following direct gap-fill step. That finding alone did not
establish whether continuing it would improve final packing.

The isolated candidate now runs the existing direct gap-fill step after an
exchange, including successful exchanges, before deciding whether relocation
is needed. It preserves the old relocation short circuit when an exchange or
direct fill succeeds. The exchange algorithm, repair/acceptance rules, gap
sampler, clock/work charges and overall search limits remain. With no accepted
exchange, execution order remains the same. Production is unchanged.

Two omitted-zero counters report post-exchange fill calls and moved parts.
The original runtime fails a new authored regression: its exchange succeeds
but no direct insertion occurs. With the fix, the same test requires a small
part to reach a known earlier-sheet gap, preserves geometry/material, and
checks the new counters plus disabled/expired behavior. The original failed
test log and source are retained.

All 98 optimized core tests pass, including all 97 previous tests. Strict
lint/build, ten authored fixed-work observer outcomes, four public CLI
comparisons and five adversarial harness checks pass. Normal full output is
exact apart from wall duration; common-mode replays and independent metrics
agree. Source, binary, archive CRC and every member hash verify.

The paired pilot retains four jobs, two kerfs, three seeds, three rotating
sequential arms on eight physical CCD0 cores and 60-second search limits.
Block, scoring, case and measurement functions are AST-identical to the prior
pilot. All original failures and the +1% material limit remain. The full
13-job H5 gate is still required; no reserved files or integration.
H2/H5 remain open; completed weight stays 60%.
