# Shop-file corpus (v1.1 N0)

The corpus contains 534 primary inputs, with 338 required part/unit labels and
148 reviewed reference renders. `manifest.json`, created once by
`scripts/shop_freeze.py --write`, is the authoritative H1 freeze: it records
source/licence/writer evidence, file and label hashes, every auxiliary corpus
file, and the writer-stratified train/held-out split. Its companion SHA-256 file
pins the manifest itself. `manifest.draft.json` remains the pre-freeze authoring
record and must not be used to select training cases.

| Set | Files | Labels |
| --- | ---: | ---: |
| Real designs, nine sources | 74 | 74 |
| Native LightBurn: 15 projects and 35 exports | 50 | 50 |
| Public LightBurn projects, five sources | 44 | 44 |
| Robustness suites | 183 | None by design |
| Seeded habits, 17 per each of ten bases | 170 | 170 |
| Paired published reference SVGs | 13 | Reference only |

Twenty-five real files have the full Fusion writer fingerprint; seven have
FreeCAD writer evidence. The remaining 42 retain an unknown writer rather than
an inference from their DXF version. The immutable source URLs and original
bytes are pinned in `sources.lock.json`. [LICENSES.md](LICENSES.md) gives
per-file attribution and preserves the reviewed permissive licence evidence.

The split holds out 15/74 real files (five Fusion, one FreeCAD, nine unknown)
and 10/50 native files. Native exports and their source design, same-source
DXF/SVG filename pairs and byte-identical originals share a partition. Selection
uses only these identities and writer metadata, with the recorded seed; it does
not consult labels, warnings, geometry or importer results. Never tune on held-out
files. Generated bases exclude the ten v1 held-out maker jobs as well.

Real/native SVG and DXF labels use independent ezdxf/Inkscape rendering and file
reading. Public-project labels use original XML membership/settings and native
SVG references validated against the unmodified published MIT reader with an
explicit reference-input adapter. `references/public/` contains auxiliary
native saves, exports and renders; these do not increase corpus counts and do
not constitute no-op round-trip evidence. Native re-save can change legacy layer
serialization and create text caches. Original project bytes remain unchanged.

Eleven malformed, empty or incomplete inputs are explicit negative fixtures.
They do not earn successful H2 imports. Valid LightBurn documents containing only
fixed shapes have an explicit no-movable-unit outcome. Degenerate open-line
proxies and missing text backups are recorded rather than silently discarded.
All cut-part counts in LightBurn labels mean the top-level nesting units from
the plan; a visual plate made of ungrouped cut shapes may therefore contain
several units. Group hole counts exclude engraved text/artwork.

`probes/` contains original MIT format experiments, separate from the required
real-design derivatives. The findings are documented in `docs/LBRN2.md`.
Authoring dependencies are pinned in the requirements file and `oracle-tool/`.
Authoring scripts refuse label changes once the frozen manifest exists.

From the repository root, verify source bytes with
`python scripts/shop_sources.py --check`, and the complete frozen corpus with
`python scripts/shop_freeze.py --check`. `scripts/shop_labels_audit.py` verifies
label/render identities without invoking Nestbolt. Product gate evaluations must
read `manifest.json` and preserve its split; integrity checks do not establish
import quality. The H1 evidence and allocation are recorded in BENCHMARKS.md
before any N1 change.
