# Frozen-source download outage — 2026-10-15

The Linux and Windows maker rebuilds for `2eecbf1` failed before generating
anything: Openclipart's `/download/22109` endpoint returned HTTP 504 after
retries. Windows also saw an initial TLS EOF; Linux first timed out.

- [Linux job](https://github.com/skulitom/Nestbolt/actions/runs/38706368094/job/116326668619)
- [Windows job](https://github.com/skulitom/Nestbolt/actions/runs/38706368094/job/116326668526)
- [Retained logs and checksums](ci-openclipart-outage-20261015/evidence.json)

The already verified source cache contained the exact original 12,855-byte
CC0 **Gear** by Steren. A [copy with attribution](../makers/source-downloads/LICENSES.md)
now accompanies the maker setup files. Its SHA-256 is the existing frozen pin
`43124915a6287e48c26959696e0aa23fda6ff71924059506468117f2da9a02ca`.
No source geometry, generator, matrix, held-out split or published result changed.
The file was copied and hashed without inspecting or tuning its geometry.

`maker_setup.py` uses a bundled source when present and verifies it against the
same pin before creating the isolated cache. A corrupt local copy fails clearly;
it is not silently replaced by an online download. Sources without a bundled
copy retain the existing retried download and checksum verification.

Three tests pass: the real frozen file works with all network access mocked out,
a corrupt local file is rejected, and unbundled downloads still require the
frozen checksum. `maker_freeze.py --check` also passes for all 40 frozen maker
jobs, curve sources, notices and ten held-out reservations. These are source
integrity checks, not new benchmark runs. CI must separately confirm the clean
Linux and Windows rebuilds after this repair.

Follow-up: both clean maker rebuilds in [run 38709347553](https://github.com/skulitom/Nestbolt/actions/runs/38709347553)
passed at repaired commit `43684ad`. The frozen source could be rebuilt on Linux
and Windows without the unavailable Openclipart endpoint. This statement covers
those two completed jobs; other jobs in that run were still completing when
this follow-up was recorded.
