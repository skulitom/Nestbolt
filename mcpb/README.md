# MCP bundle and release work

Packaging is required for M4; no bundle or registry entry is published or claimed
ready by this scaffold. Keep the bundle manifest's tools aligned with the server's
actual capabilities. At present there are no tools to advertise.

Implement against the reviewed [Cutbolt #2](https://github.com/skulitom/Cutbolt/pull/2)
and [Inkbolt #1](https://github.com/skulitom/Inkbolt/pull/1) patterns:

1. Tag-triggered native release builds: Windows x64, Linux x64, macOS arm64.
2. On Windows use `RUSTFLAGS=-C target-feature=+crt-static`; verify the resulting
   executable does not require the separate Visual C++ runtime.
3. Package binaries, licence texts and agent documentation, then write SHA-256 sums.
4. Build and validate MCPB, then produce `server.json` with the actual bundle URL
   and checksum. Validate using `mcp-publisher validate`.
5. Dispatch-only OIDC publication, after Artem's explicit go-ahead. Never replace
   existing release assets or publish a metadata-only version prematurely.

Future `.mjs`/`.py` bundle scripts and `.github/workflows/*.yml` are permitted;
there is no repository extension guard to block these files.
