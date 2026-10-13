# N1 encoding and units checkpoint — 2026-10-13

**H2 remains incomplete; milestone completion is still 15%.**

All three surfaces now decode original bytes through the same core reader.
Legacy DXF follows `$DWGCODEPAGE`, defaulting to Windows-1252; R2007+ follows UTF-8.
DXF Unicode escapes, including surrogate pairs, retain non-ASCII layer names.
SVG follows its BOM or encoding declaration. Invalid bytes and unsupported
encodings request a corrected export rather than inserting replacement characters.
The pinned encoding_rs 0.8.35 dependency is unmodified; its Apache/MIT and WHATWG
BSD notices are retained and included in the browser bundle.

Declared DXF units take precedence. Missing units stay at the chosen fallback
(1 mm per unit by default). Selected geometry under 60 drawing units triggers an
inches warning without any automatic rescaling. UI offers mm/inches/cm per file;
CLI/MCP retain their explicit mm-per-unit parameter. Reports include the applied
scale, whether units were declared, the measured raw dimension and the warning
flag. Unsupported unit codes request a supported-unit re-export rather than
silently assuming a scale. Unicode case matching also applies to layer selection.

## Training and robustness

[Training report](h2-import-training-20261013T191255Z.json): 257 frozen training
vectors, 251 imported, six rejected; **247/257 match part/hole counts**. The two
legacy DXFs that previously failed UTF-8 reading now match. All 170 generated
files and 24 ordinary native DXF/SVG files still match; real count matches are
53/59. The four malformed native negatives and two empty SVG negatives reject.
Three other negative fixtures still partially import, and one overlapping switch
footprint drawing misses an enclosed island. These four mismatches remain visible
and keep H2 unpassed. Native projects, exact selection/warning acceptance and
independent re-export fidelity are outside this count diagnostic.

[Robustness report](h2-import-robustness-20261013T191404Z.json): 183 attempts,
82 imported, 101 rejected; no panic or timeout, slowest 0.859 s. Each native child
starts suspended, receives one CCD0 physical CPU, then resumes; four processes at
most and ten seconds per file. Source hashes stayed unchanged. No held-out
geometry or label was read; frozen files and split remain unchanged.

## Checks

- Five new core encoding/unit tests and all fourteen prior focused importer tests
  pass, including the 1,024 randomized cleanup cases.
- CLI and MCP tests read actual Windows-1252 bytes, retain the Unicode layer name
  and exercise an explicit inches fallback.
- Chromium and Firefox: 10/10 current import checks pass, including the byte
  decoder and per-file units dropdown.
- Full workspace test suite passes, with one pre-existing ignored Sparrow test.
- Strict Clippy, production WASM/web build, schema generation and dependency
  notice verification pass.

Remaining N1 work includes partial/ambiguous import handling, full label/fidelity
checks, the complete 10,000-case habit fuzz gate, sheet-outline use and export
palette/native LightBurn evidence. H2 held-out scoring remains awaiting the
already-raised clarification; neither the threshold nor the split was changed.
