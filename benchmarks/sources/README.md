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
frozen M0 method; that historical manifest remains unchanged. The canonical
[academic benchmark freeze](../datasets/README.md) now contains 13 S and 35 B jobs.

## Sheet-source research for M1

We examined jagua-rs's BPP examples and the irregular bin-packing collections in
[López-Camacho et al. (2013)](https://doi.org/10.1007/s10479-013-1341-4) and
[Martínez-Sykora et al. (2017)](https://doi.org/10.1016/j.ejor.2016.09.043).
The latter's [author-deposited manuscript](https://eprints.soton.ac.uk/400806/)
describes literature jigsaw sets and sheet variants of strip instances. Its
[direct manuscript](https://eprints.whiterose.ac.uk/139290/1/BCP-EJOR.pdf) was
retrieved and read: section 6.1 defines the sheet-size formula, and Tables 1/5
provide rotations and published results. The 22 Nest-MB reconstructions use the
MIT-declared OR-Datasets contours, with every source/constraint distinction in
the manifest. Another 13 jobs are explicitly labelled Nestbolt derivatives.

The BALDACCI examples include piece-specific quality zones beyond v1's binary
keep-outs; they are not silently weakened into ordinary defect jobs. The
López-Camacho jigsaw sets and the other 12 families from Martínez-Sykora are not
part of this freeze. The plan's published sheet-instance requirement is covered
by the 11 overlapping Nest-MB families and their two rotation variants.

Maker source selection, 40 jobs, and the 10 never-tuned held-out jobs remain
outstanding. No optimiser tuning has begun.
