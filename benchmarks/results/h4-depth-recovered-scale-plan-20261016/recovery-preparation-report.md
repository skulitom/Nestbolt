# H4 recovery after Windows servicing restart — 2026-10-16

**The original comparison was interrupted; it is not recorded as complete or
passing.** Windows servicing requested a restart at 05:59:24 UTC. Shutdown
followed at 06:00:07 and the new boot began at 06:00:33. Both the measurement
process and its conditional scale process are absent. No scale run had begun.
[Restart evidence](h4-depth-reboot-recovery-20261016/restart-evidence.json)
records the event identities and times without publishing machine/user names.

The original session had completed all 201 native and 201 Chrome outcomes;
every layout is valid. Firefox 157.0 had started its first batch, but saved no
layout, result, error or validation file. The precise number of started worker
jobs was not recorded; zero saved results is not claimed to mean zero attempts.
All original files, logs and the interrupted Firefox plan remain preserved in
[the verified archive](h4-depth-reboot-recovery-20261016/interrupted-session.zip).
The original directory and one-use marker are unchanged.

[Independent checks of the completed outcomes](h4-depth-reboot-recovery-20261016/retained-verification.json)
confirm exact saved metrics, original requested quantities and public-example
validation. All three Chrome execution and affinity checks pass. Native's
development median is +0.000614% versus frozen v1 (limit +0.5%). Chrome's curve
subset median is +0.851159% (limit +1%), worst +2.455588% (limit +5%). Its full
development comparison also passes aggregate and each-seed limits. These
completed results are retained without replacement or score selection.

The [recovery plan](h4-depth-reboot-recovery-20261016/plan.json) retains those
402 current-build outcomes and all 195 previously verified frozen-v1 outcomes,
then runs the missing 201 Firefox outcomes once. It uses the unchanged build,
67 jobs, seeds 0–2, 60-second budgets, one worker per job, at most eight physical
CCD0 cores and the original quality limits. Firefox is still version 157.0;
its executable is now pinned. Every original source, executable, site, input,
runner and environment-override guard still matches. The recovery records the
new boot/OS environment explicitly; it is a separate session after an external
restart, not a claim that the earlier session continued uninterrupted.

The recovery has a one-hour operational cap and its own one-use marker. The
original four-hour plan and its interrupted disposition stay intact. Every new
failure or incomplete outcome is retained and prevents acceptance; no completed
outcome is rerun or substituted. The complete comparison must pass before the
fixed scale workflows, all-placement curve fidelity checks, screenshot review
and final H4 requirement audit. Source/builds remain frozen throughout.

H4 stays open, and completion remains **45%**. The common-line pilot remains
unopened; the preview release has not been published. Hosted checks and actual
package verification remain valid for this unchanged code. The newer main CI
run at `21835ba` has also finished successfully.
