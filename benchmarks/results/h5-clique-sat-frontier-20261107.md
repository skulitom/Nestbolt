# Complete clique-count certificate frontier — 2026-11-07

Independent proof checking excludes **20 more fixed29/current-cog arrangements**.
There are now **six remaining**, with **449 of 455 excluded at original 0.2 mm
clearance**; 427 of those were already excluded even at zero clearance. This
does not produce a placement or exclude any whole-job allocation. The 440
allocation candidates, full 66 source/native/material checks and H2/H5 remain
open at **60% completed milestone weight**.

## Process-tree supervision

The [Windows Job Object controls](h5-clique-sat-frontier-20261107/job-controls.json) assign a suspended
launcher before its initial thread resumes. The operating system then contains
its interpreter and descendants in the same job. Kill-on-close, an aggregate
committed-memory limit and a conservative peak-counter stop are configured.
Normal completion waits for a child even after its parent exits. Timeout and
memory-stop controls finish with zero active processes. A larger 256 MiB positive
control allows both 80 MiB children to allocate. An [external-stop control](h5-clique-sat-frontier-20261107/external-stop-control.json)
also terminates the entire child tree before a frozen deadline.

All failures remain preserved: a macro redefinition fails the first strict
build; Windows runtime exclusive-file mode prevents the next control report;
and the next memory control reports a peak above its configured limit despite
one rejected allocation. The final runner conservatively stops when that
counter exceeds the limit, rather than treating its accounting cause as known.
This is test infrastructure; no production dependency or benchmark meaning changes.
API sources and compiler/source/binary hashes are retained.

## Source-necessary Boolean models

Each model preserves every independently certified incompatible-cell pair.
The source conflict cliques form a complete partition of each family. A group
selector is equivalent to OR of its cells; pair clauses permit at most one
selected cell per group. Counting at least eight selected groups is therefore
exactly equivalent to counting at least eight cells. This reduces the threshold
logic from long per-cell chains while preserving every legal continuous completion.

Across 25 fresh models, independent audits verify **47,714,816 clauses**,
**111,518,237 graph pairs**, 5,912 threshold gates and 72,937 source-inner-rectangle
single-cell capacity proofs. Complete source covers preserve all boundaries and
mode aliases. The first [0,5,11] proof and the separate earlier [4,5,10] graph
both pass their [independent certificate checks](h5-clique-sat-frontier-20261107/first-certificate.json),
[including the earlier-cover check](h5-clique-sat-frontier-20261107/earlier-cover-certificate.json).
The earlier timed-out [0,5,12] pilot is never rerun.

The [23-case batch](h5-clique-sat-frontier-20261107/batch-audit.json) uses one fresh call for each other
arrangement, with 60 s search, 1,000,000 conflicts, 2 GiB aggregate memory and 64 MiB
binary-proof limits frozen before execution. Model construction and every-clause
audit precede each call. Native job containment protects every stage and returns
zero active descendants. The batch closes in 691.642932 s, within its 3600 s cap.
Seventeen normal executions have complete proofs accepted against their exact
DIMACS bytes. Five calls stop at the proof-byte limit; these remain unresolved.

## A failed producer and an independently proved contradiction

[5,10,12] writes UNSAT and later exits with Windows error 0xC0000409. Its original
audit rejects the run before invoking a proof checker. The full preserved binary
file contains 13,336,634 bytes, exceeding its pre-destructor telemetry 12,210,234.
The first artifact preflight preserves that size mismatch; the next rejects the
malformed full-file suffix. Neither invokes a checker.

A separately parsed, unchanged prefix ends in its first added empty clause at
byte 12,210,234. The independent binary parser agrees with the Python inspection.
This is only a syntactic candidate until every necessary lemma is checked.
The exact prefix is losslessly converted and the **first native checker call
accepts its complete derivation**. The [certificate-only result](h5-clique-sat-frontier-20261107/post-error-certificate.json)
therefore proves the fixed-arrangement contradiction. The full raw file, its
1,126,400-byte post-empty suffix, process error, earlier telemetry and failed
audits remain preserved. The producer is never relabelled successful and there
is no successful benchmark-construction claim or repeated search/checker call.

## Six unresolved source arrangements

The [combined audit](h5-clique-sat-frontier-20261107/frontier-audit.json) combines 19 proofs from successful
bounded producers and this one independently checked artifact. It deduplicates
the excluded choices and checks their source/model/proof bindings. The six
remaining choices are **[0,5,10], [0,5,12], [5,10,11], [10,11,12], [11,12,13]
and [12,13,14]**. Every earlier call stays closed.

[Read-only stream inspection](h5-clique-sat-frontier-20261107/incomplete-stream-inspection.json) checks
all five byte-limited files and the prior time-limited pilot. None contains a
complete prefix ending in an added empty clause; all end in truncated data.
No checker call or exclusion is claimed for any of them. There are no graph
witnesses or source-valid placements.

[Next](h5-clique-sat-frontier-20261107/next-step.json), assess genuinely stronger source clearance
polygons for those six retained graphs, using an inscribed 16-direction shape
strictly inside the original 200 um Euclidean clearance disk. Rebuild from
unexpanded source geometry and independently verify every new removal/edge.
A case must gain an actual new necessary constraint before any fresh call.
No closed model is simply rerun or given larger limits. All consumed preparation
and failures remain recorded; none of this is a full-job 60/90 s construction claim.

The two preceding checkpoints reached main **de1b6da8** by normal atomic
fast-forward after all six prior CI checks passed; the [receipt](h5-clique-sat-frontier-20261107/main-sync-receipt.json)
preserves all 52 remote README/site files. No release or registry version is added.

[The manifest](h5-clique-sat-frontier-20261107/raw-manifest.json) contains 1054 new
canonical members in 6 ZIP parts, totaling 249,183,160 bytes.
[Historical references](h5-clique-sat-frontier-20261107/external-evidence.json) and
[source bindings](h5-clique-sat-frontier-20261107/source-bindings.json) retain every original dependency.
Independent archive verification is required before commit.
