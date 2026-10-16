"""Check every original saved curve export after the fixed depth-candidate scales."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json, subprocess, traceback
ROOT=Path(__file__).resolve().parents[1];SEQ=ROOT/'benchmarks/results/h4-depth-recovered-scale-plan-20261016'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def folder(index):
    rows=[]
    for line in (SEQ/f'stage-{index}.log').read_text(encoding='utf-8',errors='replace').splitlines():
        try:r=json.loads(line)
        except json.JSONDecodeError:continue
        if isinstance(r,dict) and 'folder' in r:rows.append(Path(r['folder']).resolve())
    assert rows and len(set(rows))==1
    p=rows[0];assert p.parent==(ROOT/'benchmarks/results').resolve();return p
curves,g5=folder(2),folder(3)
curve_results,g5_results=load(curves/'results.json'),load(g5/'results.json')
assert curve_results['passes'] and g5_results['passes'], 'Preserve failed scale outcomes; no scale pass is inferred from process exit'
assert curve_results['fixture_kind']=='curves' and g5_results['fixture_kind']=='g5'
OUT=SEQ/'curve-export-fidelity';OUT.mkdir();records=[]
try:
    for browser in ['chrome','firefox']:
        project=curves/browser/'project.zip';before=digest(project)
        log=OUT/(browser+'.log');result=OUT/(browser+'.json')
        command=[str(ROOT/'.cache/shop-venv/Scripts/python.exe'),'-X','utf8',str(ROOT/'output/h4_curve_export_check_v3.py'),'--project',str(project),'--out',str(result)]
        started=datetime.now(timezone.utc).isoformat()
        with log.open('xb') as f:r=subprocess.run(command,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
        row={'browser':browser,'project':project.relative_to(ROOT).as_posix(),'project_sha256':before,'project_unchanged':digest(project)==before,'command':command,'exit_code':r.returncode,'started':started,'finished':datetime.now(timezone.utc).isoformat(),'log_sha256':digest(log)}
        records.append(row);write(OUT/'progress.json',records)
        assert r.returncode==0 and row['project_unchanged']
        assert result.is_file()
        checked=load(result)
        assert checked['all_checks_pass'] and checked['full_project_checked']
        assert checked['total_placements_checked']==2000
        assert checked['project_zip_sha256']==before and checked['limit_mm']==0.01
        assert checked['searches_run']==0 and not checked['exports_regenerated']
        row['placements_checked']=checked['total_placements_checked']
        row['report_sha256']=digest(result)
    write(OUT/'verification.json',{'all_checks_pass':True,'curves':curves.relative_to(ROOT).as_posix(),'g5':g5.relative_to(ROOT).as_posix(),'both_scale_workflows_pass':True,'every_curve_sheet_selected':True,'records':records,'H4_complete':False,'visual_review_and_requirement_audit_remaining':True})
except BaseException:
    write(OUT/'failure.json',{'error':traceback.format_exc(),'records':records});raise
