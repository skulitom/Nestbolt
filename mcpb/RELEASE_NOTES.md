Nestbolt nests parts on fixed sheets for laser, CNC, plasma, waterjet and fabric cutting. It has a command-line tool and an MCP server over stdio, and needs no network listener or account at runtime.

The Windows x64 ZIP, Linux x64 tar.gz and macOS arm64 tar.gz contain `nestbolt`, `nestbolt-mcp`, the README, `llms.txt`, the MIT licence and dependency notices. `nestbolt-windows-x64.mcpb` contains the Windows x64 MCP server for Claude Desktop: Settings > Extensions > Install from file, then choose an existing workspace folder.

Check downloads against `SHA256SUMS`. The bundle also has `nestbolt-windows-x64.mcpb.sha256`; on PowerShell compare `(Get-FileHash nestbolt-windows-x64.mcpb -Algorithm SHA256).Hash` with it. With sha256sum, run `sha256sum --check SHA256SUMS` after downloading every listed asset.

Verify build provenance (substitute another asset name to check it):

```sh
gh attestation verify nestbolt-windows-x64.mcpb --repo skulitom/Nestbolt --signer-workflow skulitom/Nestbolt/.github/workflows/release.yml
```

MCP Registry publication is a separate manual step after testing; see [Publishing](https://github.com/skulitom/Nestbolt/blob/main/mcpb/PUBLISHING.md).
