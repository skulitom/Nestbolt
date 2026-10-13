# Shop-file corpus (v1.1 N0)

**Collection in progress; H1 is not frozen.** No Nestbolt importer changes have
been made against these files. The held-out assignment will be recorded before N1.

The initial real set contains 74 drawings (63 DXF, 11 SVG) from nine repositories.
The immutable source URLs, original filenames and SHA-256 digests are in
`sources.lock.json`; [LICENSES.md](LICENSES.md) gives per-file attribution and
preserves the reviewed licence documents. Only four explicitly licensed designs
from OpenStickCommunity/Hardware are included, not its other assets.

Rebuild the reviewed source bytes with `python scripts/shop_sources.py` from the
repository root. Verify them offline with `python scripts/shop_sources.py --check`.
Neither command runs Nestbolt or establishes an import gate.

`probes/` holds original MIT test geometry and projects saved by LightBurn 2.1.01
in Anode. These format probes are separate from the 15 required LightBurn
derivatives of real designs. Their observations belong in `docs/LBRN2.md`.

Still required for H1: local LightBurn derivatives and exports, at least 40 public
LightBurn projects, 150 robustness-suite files, the seeded shop-habit generator,
all labels and rendering evidence, writer evidence, and a stratified held-out
freeze with checksums recorded in BENCHMARKS.md.
