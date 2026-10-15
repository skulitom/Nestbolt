# Publishing Nestbolt

**Release and registry publication follow Artem's authorization.** v0.1.0 was
released and listed in the MCP Registry on 2026-10-14. On 2026-10-16 Artem
authorized the next GitHub release when ready; see
[reviewed decision 7](../docs/PLAN_V1_1.md#10-reviewed-decisions). The next preview
still needs its release checks. Registry publication is a separate step.

Pushing a version tag runs **Release**: locked Rust 1.98.1 builds of `nestbolt`
and `nestbolt-mcp` for Windows x64 (C runtime linked statically, so no Visual C++
Redistributable is needed), Linux x64 and macOS arm64; version checks of both
executables; native archives; the Windows MCPB build, a real import-nest-validate
smoke test of the bundled server, the Node tests and MCPB 2.1.2 validation; and
`mcp-publisher validate` of the generated registry entry. After every check
passes, it attests the archives and bundle and creates the GitHub release with
checksums. Reruns skip identical release assets and fail on different bytes; they
never replace assets. Tags with a prerelease suffix produce a GitHub prerelease
and never become Latest. Only the highest stable tag becomes Latest. A rerun
refuses to change an existing release's preview status.

Pull requests that touch the distribution workflows, `mcpb/` or `server.json`,
and manual Release runs with an empty tag, run the same builds and checks as a
dry run, without attestation or release:

```sh
gh workflow run release.yml -R skulitom/Nestbolt
``` Registry publication is always a separate manual dispatch after
testing. It uses GitHub OIDC and skips versions already listed.

**Published registry versions are immutable. Publishing metadata-only permanently
prevents that version from ever getting its bundle.** The `metadata_only`
dispatch checkbox is an explicit fallback only when the release has no bundle.

## Release

Bump `[workspace.package] version` in `Cargo.toml`, commit, then tag that commit
and push the tag:

```sh
git tag vX.Y.Z
git push origin vX.Y.Z
```

The tag must be `v` plus that version: `X.Y.Z` for a stable release, or a SemVer
prerelease such as `0.2.0-alpha.1` for a preview. Build metadata (`+...`) is not
accepted. A manual Release run also requires an existing tag. Never reuse a tag
for changed bytes. The manifest
template has no version: the builder inserts Cargo's. `server.json` stays
metadata-only; the entry writer stamps the release version, bundle URL and
SHA-256 into a generated copy and never edits the source metadata.

Preview builds still validate their generated metadata, but the separate
**Publish to MCP Registry** workflow accepts stable tags only. A GitHub preview
does not publish a new registry version.

The builder reads the server's live tool catalog and logs added or dropped names;
`mcpb/manifest.json` keeps curated one-line descriptions as display overrides.
A new tool uses the first sentence of its server description, at most 160
characters on a word boundary. A test checks the manifest names the server's tools.

## Test the download, then publish

On Windows, in a checkout whose Cargo.toml matches the release, with Node 20 or
newer (substitute the tag):

```sh
gh release download vX.Y.Z -R skulitom/Nestbolt -p nestbolt-windows-x64.mcpb -p nestbolt-windows-x64.mcpb.sha256 -D target/release-test
gh attestation verify target/release-test/nestbolt-windows-x64.mcpb --repo skulitom/Nestbolt --signer-workflow skulitom/Nestbolt/.github/workflows/release.yml
node mcpb/verify.mjs target/release-test/nestbolt-windows-x64.mcpb
```

The verifier extracts the bundle to fresh folders under `target/`, launches the
manifest command with a temporary workspace, imports a small SVG, nests it for
two seconds and validates the layout. It fails on writes outside the workspace,
changes to the extracted bundle or to repository sources, then removes its
folders. This is a regression check, not an OS sandbox. Non-Windows runs fail
unless given `--allow-skip`; a skip is not verification.

Optionally install the bundle in Claude Desktop (**Settings > Extensions >
Install from file**), choose an existing workspace and nest a drawing. Then:

```sh
gh workflow run publish-registry.yml -R skulitom/Nestbolt -f tag=vX.Y.Z
```

Publication requires the release, verifies the bundle's attestation, validates
the entry with checksum-pinned mcp-publisher 1.8.1 and reads back the published
`fileSha256`.

## Local checks

```sh
cargo build --release --locked -p nestbolt-cli -p nestbolt-mcp
node --test mcpb/mcpb.test.mjs
node mcpb/build.mjs --binary target/release/nestbolt-mcp.exe
node mcpb/verify.mjs target/dist/mcpb/nestbolt-windows-x64.mcpb
node mcpb/build.mjs --registry-entry --tag vX.Y.Z --bundle target/dist/mcpb/nestbolt-windows-x64.mcpb
```

ZIP entry order, timestamps and text line endings are fixed; the same binary and
Node/zlib version give byte-identical bundles. Existing different outputs need a
fresh `--out`. Outputs default to `target/dist/`, which Git ignores. Both the
bundle and the archives carry `LICENSE` and `THIRD_PARTY_NOTICES`; archives also
carry `README.md` and `llms.txt`.

The packaging scripts are adapted from skulitom's MIT-licensed Inkbolt
distribution scripts. Glama and awesome-mcp-servers submissions are manual.
