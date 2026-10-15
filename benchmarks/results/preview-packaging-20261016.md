# Preview packaging preparation

The release packaging now accepts SemVer prerelease versions such as
`0.2.0-alpha.1`, without build metadata. The exact version propagates from Cargo
to the MCPB manifest, all three native archive filenames and generated registry
metadata. Malformed versions, numeric prerelease identifiers with leading
zeroes and filename-unsafe separators remain rejected.

The release workflow uses `mcpb/release.mjs` to classify the existing tag. A
prerelease always gets `--prerelease=true --latest=false`; stable tags are
compared numerically. An existing release with different preview status is
rejected before any asset upload. Existing asset-byte checks remain in place.
The separate registry publication workflow continues to accept stable tags only.

Local checks pass: 21 packaging tests, with one platform-specific skip and two
real-binary integration tests excluded from this invocation. The added checks
exercise preview version propagation through the bundle, Windows/Linux/macOS
archive creation and generated metadata; older stable releases and previews
cannot become Latest in the tested policy cases. These fixtures use stand-in
binary bytes, so they do not replace native builds or runtime verification.

The workflow YAML parses and all eight Bash fragments pass syntax checking with
GitHub expressions replaced by placeholders. The actual policy command selects
the existing stable `v0.1.0` correctly and rejects the absent preview tag. This
is local syntax/policy verification, not a completed GitHub workflow run.
[Checks](preview-packaging-20261016/checks.json) record source hashes, commands,
test scope and the pending native packaging dry run. The first test execution
was observed in the tool output; no separate raw test log was captured.

No Cargo version, product source, measured executable, tag, release or registry
entry changed. The H4 source/binary/site guards still match their frozen plan.
The release remains subject to the [readiness checks](../../docs/RELEASE_READINESS.md),
including the curve-search repair, performance review and final native builds.
