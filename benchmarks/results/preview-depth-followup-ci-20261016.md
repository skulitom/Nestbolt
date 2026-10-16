# Follow-up main CI browser observation — 2026-10-16

The [separate main check on c36baa8](https://github.com/skulitom/Nestbolt/actions/runs/38883652469)
has **85 passed, one failed, four skipped** browser tests. Firefox never shows
`.lead-report` within the original 90-second expectation in the one-second lead
fixture. The job did not upload its error context, so the actual page state and
root cause are unknown. This is not relabelled as a pass or an infrastructure
failure. The separately successful release workflow and actual published native
download checks remain recorded in the [publication report](preview-depth-published-20261016.md).

All sixteen local repetitions of the unchanged Firefox functional test pass on
CCD1 with eight concurrent workers and the original one-second search budget.
The first diagnostic command matched no tests because its title expression was
anchored; that launch and the corrected, explicitly listed selection are retained.
Local success does not replace the hosted failure or establish its cause.

The test now waits for either the result or the app's fatal alert and reports the
alert text. An intermediate attempt reused a helper that treated all `.error`
elements as fatal, including expected contour-review flags; both resulting local
failures and screenshots are retained. The helper now uses the application's
`role=alert`, preserving all lead coverage, geometry, export and flagged-contour
assertions. The complete affected feature suite passes **28/28** in Chromium and
Firefox on CCD1. No product behavior, search budget or acceptance limit changed.

Hosted failures now retain screenshot, Playwright trace and error-context files
for seven days. Fresh hosted confirmation is pending; the original cause remains
unresolved. The [diagnosis](preview-depth-followup-ci-20261016/diagnosis.json)
and [raw archive](preview-depth-followup-ci-20261016/raw.zip) preserve all observations.
No new quality measurement, reserved evaluation or milestone change occurs.
