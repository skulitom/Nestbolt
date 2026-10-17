# Lead browser-test allowance — 2026-10-17

The [bf9e880 hosted browser job](https://github.com/skulitom/Nestbolt/actions/runs/39074673874/job/117519249876)
reports **85 passes, four opt-in skips and one Chromium failure**. The lead
functional test requests a one-second search; the app explicitly reports no
complete layout within that allowance. The screenshot and accessibility snapshot
show the correct two-part request, lead settings and empty result. The original
log, trace and entire diagnostic artifact remain preserved; its downloaded
SHA-256 matches GitHub's published artifact digest exactly.

The test now uses the existing setup helper's normal five-second allowance.
Every control, reservation count, coverage, area, shortening, preview and SVG/DXF
export assertion remains unchanged. The change concerns a functional test;
production settings, published packages and every performance gate are unchanged.

A fresh browser build and test type check pass. The complete local suite passes
**86 tests with four opt-in skips**, using two workers to match the failed hosted
run and no retries. Both Chromium and Firefox pass the lead test. This local
result is not yet hosted confirmation. The earlier c36baa8 Firefox failure's
cause remains unknown; this captured error does not retroactively explain it.

[Checks](browser-lead-budget-20261017/checks.json),
[review](browser-lead-budget-20261017/review.json) and
[raw archive integrity](browser-lead-budget-20261017/integrity.json)
preserve every source version, command, log, trace and retained attachment.
No milestone or release asset changes. H2/H5 remain open; completion stays 60%.
