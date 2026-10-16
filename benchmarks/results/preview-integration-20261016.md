# Preview production integration — 2026-10-16

**All production checks pass for `0.2.0-alpha.1`.** The reviewed flat hole index,
exact CI regression, LightBurn diagnostic coverage and duplicate-message repair
are integrated. The README, LightBurn preparation guide, agent links, package
descriptions and release notes describe these features and their limitations.
No version tag, GitHub release or registry publication exists at this checkpoint.

[Check stages](preview-integration-20261016/checks.json),
[verification](preview-integration-20261016/verification.json),
[archive inventory](preview-integration-20261016/integrity.json),
[candidate geometry and surface proof](native-diagnostics-surfaces-20261016.md).

- 302 workspace tests pass; one existing test remains ignored.
- All 27 optimized CLI feature tests, two optimized Sparrow tests and four
  stock-helper tests pass. The exact Linux curve regression passes in production.
- Formatting and strict all-target workspace lint pass; both native release
  executables and both debug WASM crates build. The release WASM/site build and
  browser type checks pass.
- All 86 enabled Chromium/Firefox tests pass; four opt-in tests remain skipped.
  New diagnostics tests require each requested message to enter the viewport,
  unique message arrays and unchanged source XML in the downloaded project.
- Packaging has 23 passing tests and one platform-inapplicable skip. Both real
  release binaries pass the version smoke test; the actual Windows MCPB imports,
  nests and validates in its temporary workspace. This is local package evidence,
  not the separate three-platform CI dry run or published-download check.
- All 1,181 frozen corpus hashes retain manifest
  `02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`.
  No reserved geometry was evaluated. The complete production core equals the
  reviewed candidate; only the package version and additional tests/docs differ.

Checks run on CCD1. The version agrees across Cargo, its five local lock entries,
browser metadata and server metadata. Third-party dependency pins are unchanged.
Two helper launch mistakes are recorded: an omitted Python interpreter and a
global Python missing the shop oracle dependency. Both stopped before evaluation;
the explicit interpreter and pinned shop environment passed their checks.

The raw archive has 84 members and 855,147 bytes,
SHA-256 `9c7311a8e9eccd3f6a64639a2fb5770a9bb452cea2e828e1521c31dc784e9df8`. CRC and every member hash/size were verified
before consolidating copied browser artifacts. Logs and source snapshots remain
readable beside the archive.

## Performance and release checks still required

The earlier [full bounded-score comparison](h4-full-development-20261016.md)
passes all limits with 780 valid layouts, but its measurements apply to that
recorded build. The repair changes the hole collision index. A new committed
plan covers all 65 development jobs plus the two browser examples, seeds 0–2,
60 seconds, one worker per browser job and at most eight physical CCD0 lanes.
It measures 603 fresh attempts and reuses only the 195 hash-verified frozen-v1
baseline outcomes. It retains the unchanged subset, full-G5 and native limits.
Current scale confirmation and the H4 requirement review remain separate.

Green CI on the release commit, Windows/Linux/macOS packaging dry runs and
download verification are required before the authorized GitHub preview.
Registry publication and a fresh final acceptance are separate actions.
H2/H4/H5 remain open; completed milestone weight stays **45%**.
