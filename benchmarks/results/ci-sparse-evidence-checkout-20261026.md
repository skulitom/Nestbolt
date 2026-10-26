# CI: omit historical evidence ZIPs from test checkouts — 2026-10-26

**Main's browser retry spends 18m07s checking out the repository, then reaches
the 30-minute limit during browser dependency installation. Tests never start.**
The earlier attempt also timed out, primarily during dependency downloads.
Both failures and the other five successful jobs remain preserved.

The current tree contains 4,134,207,071 bytes across 12,000 files. Historical ZIPs
under `benchmarks/results/` account for **3,512,792,276 bytes in 2,496 files**.
All four checkout steps now use the non-cone patterns `/*` and
`!/benchmarks/results/**/*.zip`. All other files remain selected. The pinned
[checkout implementation](https://github.com/actions/checkout/blob/d23441a48e516b6c34aea4fa41551a30e30af803/src/git-source-provider.ts#L182)
automatically fetches with `blob:none` when sparse checkout is supplied, so the
omitted archives need not be downloaded before checkout. Its original MIT licence
is preserved with the inspected upstream sources in the archive.

No repository evidence is deleted. Test commands, assertions, timeouts, tool
versions, action pins and benchmark budgets are unchanged. Build fixtures,
frozen inputs, result JSON, reports and published web assets remain available.

## Local validation

A fresh isolated Git checkout uses the exact non-cone patterns. All **9,504
selected files** match their original Git blob IDs; all **2,496 ZIPs** are absent.
The retained tree contains 621,414,795 bytes. The review follows 65 Python modules
reachable from CI entry points; historical-result reads use retained JSON files.
Product and browser tests do not reference the omitted evidence archives.

All **31 existing Python CI commands pass in this checkout**, including notices,
schemas, frozen dataset verification, maker manifests and the report/adapter
tests. Native schema generators also build as part of those checks. Full hosted
native tests, maker rebuilds, benchmark smoke and browser tests remain pending;
local selection and Python passes alone do not replace them.

## Publication sequence

Validate the exact candidate on the existing working branch with the complete
six-job Checks workflow. The old main run is terminal and no working-branch run
is active; starting this validation cancels neither. After all six pass, verify
remote main is unchanged, fast-forward the queued checkpoints and CI repair to
main, then observe that new main run. No release follows from this repair.
H2/H5 remain open at **60%** and all 22 reserved H2 vectors stay unopened.

[Local checks](ci-sparse-evidence-checkout-20261026/local-checks.json), [selection inventory](ci-sparse-evidence-checkout-20261026/selection.json),
[dependency review](ci-sparse-evidence-checkout-20261026/dependency-review.json), [retry timings](ci-sparse-evidence-checkout-20261026/attempt2-step-times.json),
[timeout annotations](ci-sparse-evidence-checkout-20261026/attempt2-annotations.json), [workflow](ci-sparse-evidence-checkout-20261026/candidate-ci.yml),
[next step](ci-sparse-evidence-checkout-20261026/next-step.json), [manifest](ci-sparse-evidence-checkout-20261026/raw-manifest.json).
The raw archive verifies 99 canonical files and
36 identical-content aliases by bytes, SHA-256 and CRC.
