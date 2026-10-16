"""Remove only verified duplicate loose raw files after the original archive seal."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=(ROOT/'benchmarks/results/h4-preview-score-release-20261016').resolve()
digest=lambda p:sha256(p.read_bytes()).hexdigest()
inventory=json.loads((OUT/'integrity.json').read_bytes())
assert digest(OUT/'raw.zip')==inventory['sha256']
targets=[OUT/name for name in ['native','chrome','firefox','snapshots/engines','snapshots/site','records.json']]
removed=[]
with zipfile.ZipFile(OUT/'raw.zip') as archive:
    assert archive.testzip() is None
    for target in targets:
        resolved=target.resolve()
        assert resolved!=OUT and resolved.is_relative_to(OUT),resolved
        files=sorted(p for p in resolved.rglob('*') if p.is_file()) if resolved.is_dir() else [resolved]
        for p in files:
            name=p.relative_to(ROOT).as_posix()
            row=inventory['members'][name]
            assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
            assert sha256(archive.read(name)).hexdigest()==row['sha256']
        removed.append({'path':resolved.relative_to(ROOT).as_posix(),'verified_files':len(files)})
    # Every target is resolved and every file verified before removing any copy.
    for target in targets:
        resolved=target.resolve()
        assert resolved!=OUT and resolved.is_relative_to(OUT)
        if resolved.is_dir():shutil.rmtree(resolved)
        else:resolved.unlink()
record={'scope':__doc__,'archive_sha256':inventory['sha256'],'removed_duplicates':removed,
        'all_bytes_retained_in_verified_archive':True}
(OUT/'consolidation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,OUT/'consolidate.py')
shutil.copyfile(ROOT/'output/report_h4_preview_score_release.py',OUT/'report.py')
print(json.dumps(record))
