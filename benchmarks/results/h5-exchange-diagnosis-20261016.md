# Directed-exchange repair-stage diagnosis — 2026-10-16

**All four diagnostic layouts validate.** The saved traces identify observed failure stages.
They do not establish material or speed improvement. The earlier failed pilot remains unchanged.

The [committed plan](h5-exchange-diagnosis-20261016/plan.json) fixes both mechanical
jobs, both kerfs, seed 0, 60 seconds and serial physical CCD0 CPU 8. It starts
after the H4 tree-depth pilot finishes and is sealed. The isolated observer
preserves the rejected algorithm and adds one aggregate trace per invocation.
Tracing can perturb deadlines; no quality comparison is claimed.

| Job | Kerf mm | Invocations | Attempted exchanges | Recorded outcomes |
| --- | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | 1 | 3 | accepted: 1, receiver_repair_failed: 2 |
| m-mechanical-large-plates | 1.5 | 1 | 8 | accepted: 1, receiver_repair_failed: 7 |
| m-mechanical-panel-hardware | 0.2 | 1 | 13 | receiver_repair_failed: 13 |
| m-mechanical-panel-hardware | 1.5 | 1 | 13 | receiver_repair_failed: 13 |

All attempt-level areas, blocker counts and repair losses remain in the
[rechecked traces](h5-exchange-diagnosis-20261016/rechecked-traces.json), with
original stderr in immutable per-attempt archives. Trace counts agree with
the saved solver statistics. Independent original-geometry/public validation,
all requested quantities, zero hole riders and public exports pass. The entire
diagnostic session took 4.065 minutes.

## Retained reporting failures

The original trace reader failed on two omitted `directed_exchanges` fields.
The source explicitly omits zero-valued counters. The corrected reader supplies
zero only under that serialization rule and checks the same saved traces.
The original `results.json` and both errors are retained unchanged; no search
was repeated. After archive verification succeeded, a separate Markdown
construction error interrupted the first corrected finisher. Its source and
failure record remain; this report reads the already verified artifacts.

[Verification](h5-exchange-diagnosis-20261016/verification.json),
[stage aggregation](h5-exchange-diagnosis-20261016/observed-stages.json),
[original sequence failure](h5-exchange-diagnosis-20261016/sequence/interruption.json),
[report-format failure](h5-exchange-diagnosis-20261016/report-format-failure.json).

CRC, every archive/member hash and source/binary/input guards pass. The observed
failures locate a repair stage; they do not prove geometric impossibility or
justify increasing budgets. Inspect proposal geometry before choosing a further
changed experiment. No candidate is integrated. H5 remains open; completion is 45%.
