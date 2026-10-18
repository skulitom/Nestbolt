# Curve-fidelity browser test: explicit initial layout — 2026-10-18

The [browser job on d414824](https://github.com/skulitom/Nestbolt/actions/runs/39128166075/job/117677582736)
fails one Chromium import/export test: nesting does not produce a complete layout
within its requested five seconds. The log reports 85 passes, one failure and
four opt-in skips. The downloaded diagnostic artifact matches GitHub's published
SHA-256; its trace contains the exact original test source. The saved page has
all eight imported parts, a five-second allowance and quick initial layout off.
The failure precedes either export. These records establish an incomplete search;
they do not establish host scheduling as the cause or prove a solver regression.

The test now explicitly enables the existing quick initial layout option before
nesting. Its purpose remains importing both formats and preserving curved export
entities. All original assertions and the five-second search allowance remain.
Two additional assertions check that the saved project records the chosen option
and contains all eight placements. No retry, application change, default change,
benchmark limit change or claimed performance improvement is introduced.

The browser app rebuild and test type checks pass. The full local suite passes
**86 tests with four opt-in skips**, using the same two-worker concurrency and
zero retries. Chromium and Firefox both complete the edited import/export test.
Product-source hashes remain unchanged. The original hosted failure, screenshot,
trace, source, logs and local results are preserved in the checked archive.

Hosted confirmation of the corrected test remains pending. The previous failed
run is not replaced or described as passing. This test-only change does not
justify another application release or close H2/H5. The READMEs remain accurate.

[Local checks](browser-curve-initial-layout-20261018/checks.json),
[test-change scope](browser-curve-initial-layout-20261018/plan.json),
[original hosted failure](browser-curve-initial-layout-20261018/hosted-job.json) and
[archive integrity](browser-curve-initial-layout-20261018/integrity.json).
