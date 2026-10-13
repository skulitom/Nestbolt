# Independent LightBurn oracle

These original MIT setup manifests pin the unmodified published MIT
`lbrn2-to-svg` package at 0.5.3 and its dependency integrity hashes. No upstream
implementation code is vendored here. The package's author and licence evidence
are already recorded under `jlucaso1/lbrn2-to-svg` in the corpus LICENSES.md.

Copy both manifests into `.cache/shop-oracle/`, then run
`npm ci --prefix .cache/shop-oracle --ignore-scripts --no-audit --no-fund`.
`node scripts/shop_lightburn_oracle.mjs` writes scratch conversions and captured
warnings under `output/shop-labels/lightburn-oracle/`.

This is reference tooling, not a product dependency. Read docs/LBRN2.md for the
observed unsupported shapes/sharing and nested-text transform limitation. Native
SVG exports provide additional independent evidence; conversion success is not
full geometry validation. After H1, never run authoring/tuning on held-out files.
