# Resumable development comparisons

`comparison_session.py` creates an immutable work queue from `matrix-plan.json`.
It includes all development jobs applicable to the selected tools, the frozen
60/300-second coverage and seeds 0–2. All ten held-out maker jobs are excluded.
This is development infrastructure; final acceptance, final settings sealing,
dataset rebuilding and the public results page remain separate work.

The settings file maps each tool to both explicit roles. The example selects
LBF's identical and upstream-default configurations; the second role name does
not establish that the configuration is empirically best.

```powershell
python scripts/comparison_session.py create --name development-example --settings benchmarks/session-smoke-settings.json
python scripts/comparison_session.py run --name development-example --tool lbf --limit 2
python scripts/comparison_session.py progress --name development-example
python scripts/comparison_session_report.py --name development-example
```

Preparation of the pinned tool and validator binaries precedes `create`. Repeat
`run` to continue with the next unattempted slots. Deepnest chunks must run inside
Anode. The runner bounds desktop chunks below 27 minutes and other chunks below
three hours using the worst-case per-attempt allowance. It serializes work within
one session; separate sessions still share the project's eight-run global limit.

The manifest records input, code, configuration, validator and native Rust binary
hashes. Every attempt records its original slot and manifest hash before starting.
On completion, the tool-specific independent evidence auditor checks the native
record and controls before a completion file is written. Valid, invalid,
unsupported, no-layout and failed outcomes remain completed attempts, never
quietly retried. Source changes prevent further execution of the old queue.

An attempt directory without an audited completion is an explicit interruption.
The runner refuses to repeat it automatically. Inspect the original process/job
handle and retained native evidence before deciding what happened. A lock left by
a killed controller likewise requires investigation; it is never removed merely
because time elapsed. Do not erase failed work to make an experiment appear green.

Four regression tests cover interrupted attempts, source changes, preservation of
failed outcomes, manifest edits, duplicate prevention and existing process locks.
The actual `queue-proof-20261011` trial ran two native LBF attempts and resumed in a
new process for the third. All three passed independent validation. This is a
3/450-slot controller proof, not a completed development matrix or M1.

The report audits every retained completion and lists every scheduled group,
including missing and failed seeds. Medians and inclusive quartiles describe valid
scores only; a row is eligible for comparison only after every declared seed is
valid (at least three). Four aggregation tests cover partial sets, failures,
configuration separation, duplicate seeds, differing metrics and LBF's independent
material score. The [actual partial-session table](results/comparison-session-20261011T214917Z-024c5add.md)
correctly has no eligible rows. It establishes neither a baseline gap nor a gate.
