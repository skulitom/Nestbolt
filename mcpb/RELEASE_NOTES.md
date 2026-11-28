This release brings the shop work on `main` to the native tools and the MCP server: offcut export, job quotes,
sending sheets to LightBurn, jobs of up to 10,000 parts, a nesting engine moved to jagua-rs 2.0.0, and a run of DXF
and SVG import and export fixes, many of them from Pedro Rangel (@PedroRangel7). The v1.1 plan is still in progress;
this release does not claim that all of its acceptance checks are complete.

### What's new

- **Offcuts you can cut again:** `nestbolt offcut` (MCP `export_offcut`) writes the leftover material of each sheet
  as SVG and DXF on the `SHEET` layer, with a report: a straight slab above the highest part (`rectangular`, the
  default) or the sheet minus the parts and their clearance (`exact`). Imported again, the remnant is offered as a
  stock outline for the next job (`from_import` in a request, or Imported sheet outline in the browser); the
  command-line import also lists it as a part, so request only your own parts. It never overwrites files, so give it
  a new output folder.
- **Job quotes:** `nestbolt quote` (MCP `quote_layout`) reports cut length measured on the source curves (less any
  common-line savings), pierces, utilization, trailing offcut area, cut time from your cut speed and pierce time, and
  costs from sheet or material price, machine rate and setup, as JSON, CSV or Markdown.
- **Send to LightBurn:** `nestbolt lightburn-send` posts an exported `.lbrn2`, `.svg` or `.dxf` sheet to LightBurn
  2.2 or later through its local REST API, into the open project or replacing it. It needs the API turned on, an app
  paired with the `upload` capability and its short-lived token in `LIGHTBURN_API_TOKEN`, and it talks only to this
  computer unless you pass `--allow-lan`. See
  [sending to LightBurn](https://github.com/skulitom/Nestbolt/blob/main/docs/LBRN2.md#send-an-exported-file-to-lightburn).
- **Larger jobs:** a job may ask for up to 10,000 copies, and a layout may hold up to 10,000 placements (was 2,000).
  Large jobs need time: in the browser, whose Time field stops at 300 s, a 10,000-copy job may not reach a first
  layout; give the command-line tool or the MCP server a larger budget.
- **Engine:** the nesting engine now runs on jagua-rs 2.0.0 and Sparrow `73c02f65`. At 60 seconds over three
  development seeds, this build used less material than the build before the move on 43 of 65 jobs and more on 16;
  the median change was -0.20%, and all 390 layouts validated. Browser performance and the common-line comparison
  have not been rerun on this engine. See the
  [runs, margins and calibration](https://github.com/skulitom/Nestbolt/blob/main/benchmarks/results/jagua-2-port-20261127.md).
- **In the browser:** a "Cut summary & quote" panel with CSV and Markdown downloads; Offcut SVG, Offcut DXF and
  Remnant SVG buttons on each sheet; saved sheet presets, with a Glowforge 12 x 12 in preset; and a Quick initial
  layout suggestion for jobs of 1,000 parts or more.
- **Common-line inserts:** common-line jobs can now nest parts inside holes when you ask for it
  (`--common-line-part-in-hole`, or `"allow_part_in_hole": true`); off by default. See the material limits below.
- **For library users:** `nestbolt-core` builds without the nesting engines (`default-features = false`) for import
  and export only; every import warning is also a structured entry in the import report; an import that finds no
  part returns an error that carries the report; and a search stopped by its deadline can be told apart from other
  errors. `nestbolt-validator` now carries its own README, licence and package metadata. The crates are not on
  crates.io yet. The MCP `nest` tool takes an optional `time_limit_s` for slower machines.

### Fixes

- **DXF export:** files now carry the complete AutoCAD 2007 structure, so AutoCAD opens them (#21, landed in #22),
  and no longer contain zero-length lines after arcs and circles (#18, landed in #22).
- **DXF import:** reads binary DXF and reports a truncated one (#41, #47); converts `$INSUNITS` length units 1 to 21
  (AutoCAD for Mac's US survey inch, yard and mile, 22 to 24, still ask for a re-export) (#41); reads layers you name
  even when they are off, frozen or named like bend or construction layers, and offers an off or frozen `SHEET`
  layer as stock (#39, #48); keeps paper-space title blocks out of the parts and places every `MINSERT` copy (#23,
  #24); and no longer mirrors entities drawn with a negative extrusion (#17, landed in #22).
- **SVG import:** shapes drawn with units such as `0.125in` keep their holes, and compact polygon points keep their
  cutouts; a malformed point list now stops the import with an error naming the element (#29, #30).
- **Placement:** a free-rotation part that fits only at an angle between quarter turns is now placed, and a part
  that fits no sheet is named at once instead of failing later with "allow more time" (#40).

Thank you to Pedro Rangel for #17, #18, #21 (all three landed together in #22), #23, #39, #40, #41, #42, #44, #47
and #48.

### Coming from v0.1.0

If you are still on v0.1.0: alpha.1 also added editable LightBurn projects (`.lbrn2` and
legacy `.lbrn`, a preview), layer and colour choice on import, lead-in allowances, optional common-line cutting and a
Quick initial layout; see the [v0.2.0-alpha.1 notes](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1).
Layouts and imports can differ from v0.1.0's for the reasons below.

### Check before you upgrade

- The nesting engine and the repeatable work clock changed (`nestbolt-work-v5`), so the same seed and budget can
  give a different layout than alpha.1.
- A job with a part that fits no sheet fails with a new message that names the part; scripts that matched the old
  "allow more time" text need updating.
- The same DXF or SVG can import differently than in alpha.1 (more `MINSERT` copies, no paper-space parts, named
  hidden layers read, holes kept, negative-extrusion entities no longer mirrored), so check saved jobs.
- DXF export files differ byte for byte from alpha.1's (the added AutoCAD 2007 sections).
- Rust: `common_line::Options` has a new public field, `allow_part_in_hole`.

### Current limits

LightBurn project nesting is a preview. Older LightBurn text without embedded outlines needs a save in LightBurn or
conversion to paths, and groups mixing active artwork with Tool or output-disabled shapes need regrouping; see
[LightBurn preparation](https://github.com/skulitom/Nestbolt/blob/main/docs/LBRN2.md#required-preparation-for-older-or-mixed-projects).

Common-line mode can save cutting distance while using more material. With the default policy, which keeps holes
free, both mechanical development jobs went over the planned +1% material limit, the worst by 6.51%. With **Nest
parts inside holes** and **Search for more shared cuts** both on, the 13 development jobs saved a median 13.031% of
cutting distance at 0.2 mm kerf and 13.101% at 1.5 mm, with at most about 0.0125% more material. These figures were
measured before the move to jagua-rs 2.0.0 and have not been rerun on it. Compare both on your own job; see
[common-line setup](https://github.com/skulitom/Nestbolt/blob/main/docs/COMMON_LINES.md). COMMON paths need CAM
preparation to avoid duplicate cuts.

LEADIN paths are review guides; the cutting program generates the actual leads; see
[lead setup](https://github.com/skulitom/Nestbolt/blob/main/docs/LEAD_INS.md).

Import acceptance (H2) remains open in the
[v1.1 verification record](https://github.com/skulitom/Nestbolt/blob/main/docs/STATUS.md): not every held-out shop
file imports exactly yet, so check each import report before cutting.

The README's published comparison figures belong to frozen v1 build `75cbb32`; this release makes no new claim
against competing tools. The [browser app](https://skulitom.github.io/Nestbolt/) is built from `main`, so it can be
newer than this release.

### Downloads

Nestbolt nests parts on fixed sheets for laser, CNC, plasma, waterjet and fabric cutting. It has a command-line tool and an MCP server over stdio, and needs no network listener or account at runtime.

The Windows x64 ZIP, Linux x64 tar.gz and macOS arm64 tar.gz contain `nestbolt`, `nestbolt-mcp`, the README, `llms.txt`, the MIT licence and dependency notices. `nestbolt-windows-x64.mcpb` contains the Windows x64 MCP server for Claude Desktop: Settings > Extensions > Install from file, then choose an existing workspace folder.

Check downloads against `SHA256SUMS`. The bundle also has `nestbolt-windows-x64.mcpb.sha256`; on PowerShell compare `(Get-FileHash nestbolt-windows-x64.mcpb -Algorithm SHA256).Hash` with it. With sha256sum, run `sha256sum --check SHA256SUMS` after downloading every listed asset.

Verify build provenance (substitute another asset name to check it):

```sh
gh attestation verify nestbolt-windows-x64.mcpb --repo skulitom/Nestbolt --signer-workflow skulitom/Nestbolt/.github/workflows/release.yml
```

MCP Registry publication is a separate manual step after testing; see [Publishing](https://github.com/skulitom/Nestbolt/blob/main/mcpb/PUBLISHING.md).
