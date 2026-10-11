# Local browser controllers

`svgnest.mjs` is the automated comparator described in [its method](../svgnest/README.md).
`cpu-limit.mjs` applies/observes its CPU constraint; on Windows `cpu-job.ps1`
uses the operating system's job affinity for future child processes as well.
The lockfile pins Playwright and its matching browser revision.

`deepnest-probe.mjs` and `deepnest-bootstrap.cjs` are development probes only.
The probe opens an unmodified deepnest-next checkout in an isolated profile,
checks the exposed import/solver API and closes its own windows. It starts no
nesting and produces no benchmark score. On Windows it was run successfully
inside the separate Anode desktop, not Artem's working desktop.

The inspected deepnest-next checkout is revision
`1e7ba6e2382557f337ad481ca3251fc22032ca0f`. Its locked Electron is 40.10.2.
Local preparation used `npm ci --ignore-scripts`, the checkout's TypeScript
compiler and Electron's install script. The native NFP package loaded successfully.
An automated bounded solve/import/output adapter and reproducible setup command
are still pending. Do not treat the probe as a baseline or import that app's
code into the product: upstream includes GPL-3.0 engine code and an
AGPL-3.0-only preprocessor despite the root package's MIT declaration.

Playwright's complete LICENSE/NOTICE files are retained in `THIRD_PARTY_NOTICES`.
Competitor sources and downloaded runtime binaries stay in ignored caches.
