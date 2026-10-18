# Hosted curve-test confirmation — 2026-10-18

The corrected browser job on main `4b13a85` passes **86 tests with four opt-in
skips**. Both Chromium and Firefox pass the curve import/export test with the
explicit quick initial layout, the original five-second allowance and all
original assertions. The saved source at that exact commit matches the tested
file, including the added checks for all eight placements and the saved option.

The original [d414824 failure and local repair](browser-curve-initial-layout-20261018.md)
remain preserved. This confirms the browser test correction, not an application
performance gain or H5 result. The full workflow is still tracked separately;
its Windows checks are not inferred from the completed browser job.

[Hosted browser job](https://github.com/skulitom/Nestbolt/actions/runs/39130020220/job/117683115467),
[checks and workflow snapshot](browser-curve-hosted-confirmation-20261018/checks.json),
[original log](browser-curve-hosted-confirmation-20261018/web.log).
