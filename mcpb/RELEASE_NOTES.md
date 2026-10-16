This preview brings the v1.1 shop-file work to the native tools and MCP server.
The full v1.1 plan remains in progress; this release does not claim that all of
its acceptance checks are complete.

### What's new

- **Editable LightBurn projects:** import `.lbrn2` and legacy `.lbrn`, nest groups
  as rigid units, and write an editable `.lbrn2` per sheet. Artwork, text, images
  and layer settings are preserved; Tool and output-disabled shapes stay fixed.
- **More control over SVG/DXF imports:** choose cutting layers and colours,
  identify stock outlines, and review duplicate removal, unsupported geometry
  and optional gap repairs. Larger-gap repair is off by default.
- **Lead-in allowances:** reserve space, choose contour starts, and report
  shortened leads or contours that need attention. Lead-enabled LightBurn jobs
  include separate SVG/DXF cutting files beside the preserved project.
- **Optional common-line cutting:** export kerf-compensated shared straight
  segments. The search bonus is off by default.
- **Large drawing support:** optional Quick initial layout, automatic browser
  worker selection, and improvements to curve-heavy search and export.
- **Import explanations and curve repair:** clearer LightBurn messages for
  embedded text, bounding rectangles and missing curve controls, without repeated
  messages; a fix for a crash when nesting certain curved parts inside holes.

The CLI, MCP tools and browser share these features. See the updated
[README](https://github.com/skulitom/Nestbolt#readme) for setup and examples.
The hosted browser remains on v0.1.0; the newer browser features require a local
development build. This release supplies the native tools and MCP bundle.

### Current limits

Older LightBurn text without embedded outlines needs a save in LightBurn or
conversion to paths before nesting. Groups mixing active artwork with Tool or
output-disabled shapes need regrouping. See
[LightBurn preparation](https://github.com/skulitom/Nestbolt/blob/main/docs/LBRN2.md#required-preparation-for-older-or-mixed-projects).

LEADIN paths are review guides; the cutting program generates the actual leads.
COMMON paths need CAM preparation to avoid duplicate cuts. Common-line mode can
save cutting distance while using more material: two mechanical development jobs
exceed the planned +1% material limit, with a retained worst case of +6.51%.
See [lead setup](https://github.com/skulitom/Nestbolt/blob/main/docs/LEAD_INS.md)
and [common-line setup](https://github.com/skulitom/Nestbolt/blob/main/docs/COMMON_LINES.md).

Import acceptance and common-line material use remain open in the
[v1.1 verification record](https://github.com/skulitom/Nestbolt/blob/main/docs/STATUS.md).
The README's published comparison figures belong to frozen v1 build `75cbb32`;
this preview makes no new claim against competing tools.

### Downloads

Nestbolt nests parts on fixed sheets for laser, CNC, plasma, waterjet and fabric cutting. It has a command-line tool and an MCP server over stdio, and needs no network listener or account at runtime.

The Windows x64 ZIP, Linux x64 tar.gz and macOS arm64 tar.gz contain `nestbolt`, `nestbolt-mcp`, the README, `llms.txt`, the MIT licence and dependency notices. `nestbolt-windows-x64.mcpb` contains the Windows x64 MCP server for Claude Desktop: Settings > Extensions > Install from file, then choose an existing workspace folder.

Check downloads against `SHA256SUMS`. The bundle also has `nestbolt-windows-x64.mcpb.sha256`; on PowerShell compare `(Get-FileHash nestbolt-windows-x64.mcpb -Algorithm SHA256).Hash` with it. With sha256sum, run `sha256sum --check SHA256SUMS` after downloading every listed asset.

Verify build provenance (substitute another asset name to check it):

```sh
gh attestation verify nestbolt-windows-x64.mcpb --repo skulitom/Nestbolt --signer-workflow skulitom/Nestbolt/.github/workflows/release.yml
```

MCP Registry publication is a separate manual step after testing; see [Publishing](https://github.com/skulitom/Nestbolt/blob/main/mcpb/PUBLISHING.md).
