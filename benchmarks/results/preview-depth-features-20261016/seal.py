"""Seal the actual-package feature evidence without rerunning any operation."""
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import zipfile

root=Path(__file__).resolve().parents[1]
work=root/'output/preview-depth-feature-checks-20261016'
out=root/'benchmarks/results/preview-depth-features-20261016'
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
This exercises the packages from dry-run commit `23442be`; it does not build
new executables, repeat quality measurements or reopen reserved inputs.
[Checks](preview-depth-features-20261016/checks.json) and
[raw evidence](preview-depth-features-20261016/raw.zip) retain all commands,
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
on CCD1, separately from the active H4 measurements. Production digest remains
`{checks['production_digest']}`.

The three inputs are original MIT test fixtures pinned to the package commit.
Expected errors are retained as successful rejection checks, not hidden import
successes. This adds actual-download feature evidence to the
[three-platform package proof](preview-depth-release-dryrun-20261016.md).
Full current quality/scale/export review and hosted checks remain required.
No release, registry publication or milestone closure occurs; completion is 45%.

Raw archive SHA-256: `{digest(archive)}` ({archive.stat().st_size:,} bytes,
{len(inventory)} members). CRC, every member hash and byte length were verified.
'''
(out.parent/(out.name+'.md')).write_text(report,encoding='utf-8',newline='\n')

path=root/'docs/RELEASE_READINESS.md'
text=path.read_text(encoding='utf-8')
before='- [Current hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38854287845)\n'
assert before in text
text=text.replace(before,'''- [Downloaded Windows feature checks](../benchmarks/results/preview-depth-features-20261016.md)
  also pass through CLI and MCPB: explicit repair/rejection messages, preserved
  editable groups/settings/fixed shapes, separate lead cutting files, matching
  validation reports and byte-identical repeat exports on authored fixtures.
'''+before)
path.write_text(text,encoding='utf-8',newline='\n')
path=root/'BENCHMARKS.md'
before=path.read_bytes()
assert before.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with path.open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — New LightBurn/lead workflows in actual downloaded tools

[The downloaded Windows CLI and MCPB](benchmarks/results/preview-depth-features-20261016.md)
pass two explicit repair/rejection cases each, then import/nest/validate/export
two copies of the supported rigid-group fixture. All editable children, starts,
settings, notes, unknown elements and the fixed Tool shape are preserved by an
independent XML-tree comparison. Lead coverage is 10 expected / 8 reserved /
2 flagged; SVG/DXF cutting sidecars stay separate from the editable project.
Validation reports agree and repeat exports are byte-identical on each surface.
Actual manifest/executable bytes, input/output files and every expected error
are retained in a CRC/member-hash-verified archive. This authored functional
check runs on CCD1 and makes no new performance claim or reserved evaluation.
Production remains frozen; current full quality, scale/export review and hosted
checks remain required. No milestone closes and completion stays 45%.
''')
assert path.read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\nbenchmarks/results/preview-depth-features-20261016/** -text -whitespace\n')
print(json.dumps({'sealed':str(out),'members':len(inventory),'bytes':archive.stat().st_size,'sha256':digest(archive)}))
