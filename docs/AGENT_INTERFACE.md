# Agent interface

**Status: connection scaffold only.** The native executable uses rmcp 3.5.1 over
stdio and negotiates with MCP clients. It intentionally advertises no tools yet.
The integration test starts the actual process and checks that handshake and
capability declaration. This is not the final Claude Code acceptance test.

## Development connection

Build from the repository root:

```sh
cargo build -p nestbolt-mcp --locked
```

Use an absolute executable path. For this checkout on Windows, examples are:

```powershell
claude mcp add --transport stdio --scope local nestbolt -- C:/DEV/Nestbolt/target/debug/nestbolt-mcp.exe
codex mcp add nestbolt -- C:/DEV/Nestbolt/target/debug/nestbolt-mcp.exe
```

These commands register the development server; they have not been run by the
repository setup. Change the path for another checkout or operating system.
On Linux/macOS the binary has no `.exe` suffix. No credentials or network endpoint
are required by Nestbolt.

For a project-specific Claude Code configuration or Claude Desktop's MCP settings,
merge this object into the appropriate configuration file:

```json
{
  "mcpServers": {
    "nestbolt": {
      "command": "C:/DEV/Nestbolt/target/debug/nestbolt-mcp.exe",
      "args": []
    }
  }
}
```

For Codex, the corresponding configuration is:

```toml
[mcp_servers.nestbolt]
command = 'C:\DEV\Nestbolt\target\debug\nestbolt-mcp.exe'
```

## Required v1 tools

| Tool | Contract to implement |
| --- | --- |
| `import_parts` | Read local SVG/DXF; write part geometry to files; return compact areas/bounds/warnings |
| `nest` | Read a job file; use seed and budget (at most 300 s); send progress; write placements, validation and exports |
| `validate_layout` | Independently check placements against the input sheets and all constraints |
| `export_layout` | Preserve original curves; write one SVG/DXF per sheet |
| `estimate_sheets` | Return an explicitly labelled lower bound, not a packing or feasibility guarantee |

Heavy geometry belongs in files, replies below about 50 KB. File identity and
hashes should link source jobs, layouts and exports. Define workspace confinement,
overwrite policy, cancellation, errors and deterministic budgets before implementing
the tools. Never advertise a successful nest based only on the collision engine's
own report. See [architecture notes](ARCHITECTURE.md).

## Acceptance and packaging

Before marking G7 green, connect real Claude Code using
`claude -p --mcp-config <file> --strict-mcp-config`, import a sample SVG, run a
10-second nest, export and pass the independent validator. That future test may use
the user's existing client account; the current protocol test does not start an LLM.

Before release, build and validate the MCPB bundle and validate registry metadata
with `mcp-publisher validate`. Prepare Windows/Linux/macOS archives with notices and
checksums, a tag-triggered release workflow and a dispatch-only OIDC publishing
workflow. Follow [Cutbolt #2](https://github.com/skulitom/Cutbolt/pull/2) and
[Inkbolt #1](https://github.com/skulitom/Inkbolt/pull/1). Do not publish until Artem
says go, and do not publish a metadata-only version before its bundle is ready.
