# Dataset source provenance

The 13 standard strip sources are pinned to
[OR-Datasets revision e2e151c](https://github.com/Oscar-Oliveira/OR-Datasets/tree/e2e151cf241ab97d860f657cbfe515232e7096d7/Cutting-and-Packing/2D-Irregular).
That repository declares its converted collection under MIT; the complete
copyright and licence are retained in `OR_DATASETS_LICENSE`. Each manifest entry
records its licence scope, exact source URL, checksum and original-publication
index. The latter attributes the academic datasets to their original authors.

```powershell
python scripts/strip_sources.py
python scripts/strip_sources.py --verify-m0
```

The first command downloads/verifies pinned bytes under `.cache/or-datasets`.
The second also verifies all part contours, IDs, quantities and permitted angles
against historical Sparrow's M0 inputs. That comparison passed for all 13
instances on 2026-10-11. The only geometry-container difference is the paper's
declared 0.01% strip-height inflation in six inputs. Source units remain unitless.

This resolves a source/provenance question recorded as pending in the earlier
frozen M0 method; that historical manifest remains unchanged. It does not yet
freeze the final S/B benchmark job conversion or its settings.

## Sheet-source research queued for M1

Start with jagua-rs's BPP examples, then the irregular bin-packing collections in
[López-Camacho et al. (2013)](https://doi.org/10.1007/s10479-013-1341-4) and
[Martínez-Sykora et al. (2017)](https://doi.org/10.1016/j.ejor.2016.09.043).
The latter's [author-deposited manuscript](https://eprints.soton.ac.uk/400806/)
describes literature jigsaw sets and sheet variants of strip instances. Verify
the exact conversion formula, dimensions and dataset-specific terms before
freezing B; do not label new generated fixtures as published instances.

Maker source selection, 40 jobs, and the 10 never-tuned held-out jobs remain
outstanding. No optimiser tuning has begun.
