"""Seal the actual-package feature evidence without rerunning any operation."""
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import zipfile

root=Path(__file__).resolve().parents[1]
work=root/'output/preview-depth-published-feature-checks-20261016'
out=root/'benchmarks/results/preview-depth-published-features-20261016'
checks=json.loads((work/'checks.json').read_bytes())
assert checks['all_checks_pass'] and not (work/'failure.json').exists()
assert checks['authored_inputs_only'] and not checks['held_out_geometry_read']
assert not checks['new_quality_measurement'] and not checks['milestone_closed']
out.mkdir(exist_ok=False)
digest=lambda p:sha256(p.read_bytes()).hexdigest()
files=sorted(p for p in work.rglob('*') if p.is_file())
inventory={p.relative_to(work).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}
archive=out/'raw.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(work).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,row in inventory.items():
        data=z.read(name)
        assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256']
shutil.copyfile(work/'checks.json',out/'checks.json')
shutil.copyfile(__file__,out/'seal.py')
(out/'integrity.json').write_text(json.dumps({'archive':'raw.zip','sha256':digest(archive),
    'bytes':archive.stat().st_size,'members':inventory,'crc_and_every_member_verified':True},indent=2)+'\n',encoding='utf-8',newline='\n')
report=f'''# Downloaded preview: LightBurn and lead workflows — 2026-10-16

**The actual downloaded Windows CLI and MCPB pass the new-feature workflow.**
This exercises the published packages from commit `c36baa8`; it does not build
new executables, repeat quality measurements or reopen reserved inputs.
[Checks](preview-depth-published-features-20261016/checks.json) and
[raw evidence](preview-depth-published-features-20261016/raw.zip) retain all commands,
JSON replies, expected rejection messages, authored inputs and output files.

| Check | Downloaded CLI | Downloaded MCPB |
| --- | --- | --- |
| Uncached text gives the required LightBurn repair instruction, without a partial library | Pass | Pass |
| Mixed active/Tool group gives the regrouping instruction, without a partial library | Pass | Pass |
| Supported project imports after the rejections | Pass | Pass |
| Two copies of a rigid editable group nest and independently validate | Pass | Pass |
| Lead coverage: ten expected contours, eight reserved, two explicitly flagged | Pass | Pass |
| Preserved `.lbrn2` plus separate SVG/DXF cutting files with LEADIN guides | Pass | Pass |
| Independent validation retains the same lead report; repeated export files are byte-identical | Pass | Pass |
| Original editable children, starts, settings, notes, unknown elements and fixed Tool shape survive | Pass | Pass |

The XML check separately compares parsed trees, including all group descendants,
against the authored source. Only each outer group transform and an optional
added stock outline are outside that preservation comparison. Both saved layouts
contain the requested two copies. This functional fixture does not replace the
complete H3 geometry or H6 reservation evidence.

The downloaded bundle runs with its actual manifest through the existing stdio
client. Its extracted files and all input fixtures stay unchanged; its owned
working, home and temporary directories stay empty. The earlier package smoke
already checked the broader write-confinement contract. All operations here run
on CCD1, separately from any active quality measurements. Production digest remains
`{checks['production_digest']}`.

The three inputs are original MIT test fixtures pinned to the package commit.
Expected errors are retained as successful rejection checks, not hidden import
successes. This adds actual-download feature evidence to the
[three-platform package proof](preview-depth-published-20261016/publication-verification.json).
The packages are the actual published preview downloads, whose source tag,
checksums and provenance have already been verified. These functional checks
do not publish a registry version or close any additional milestone.

Raw archive SHA-256: `{digest(archive)}` ({archive.stat().st_size:,} bytes,
{len(inventory)} members). CRC, every member hash and byte length were verified.
'''
(out.parent/(out.name+'.md')).write_text(report,encoding='utf-8',newline='\n')

print(json.dumps({'sealed':str(out),'members':len(inventory),'bytes':archive.stat().st_size,'sha256':digest(archive)}))
