"""Verify downloaded dry-run packages without observing the active benchmark tree."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tarfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DOWNLOAD=ROOT/'output/preview-score-release-dryrun-38840747735'
OUT=ROOT/'benchmarks/results/preview-score-release-dryrun-20261016'
ISOLATED=DOWNLOAD/'isolated-verifier'
VERSION='0.2.0-alpha.1'
digest=lambda b:sha256(b).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
OUT.mkdir(); ISOLATED.mkdir()
workflow=json.loads((DOWNLOAD/'workflow.json').read_bytes())
assert workflow['conclusion']=='success' and workflow['headSha']=='7eba929420d218d04169c1fdf24481051c8afae5'
assert all(j['conclusion']=='success' for j in workflow['jobs'] if j['name']!='release')
assert next(j for j in workflow['jobs'] if j['name']=='release')['conclusion']=='skipped'
shutil.copyfile(DOWNLOAD/'workflow.json',OUT/'workflow.json')
shutil.copyfile(__file__,OUT/'verify.py')
documents=['LICENSE','README.md','THIRD_PARTY_NOTICES','llms.txt']
expected_documents={p:subprocess.check_output(['git','show','7eba929:'+p],cwd=ROOT).replace(b'\r\n',b'\n') for p in documents}
rows=[]
for platform,target in [('linux','x86_64-unknown-linux-gnu'),('macos','aarch64-apple-darwin'),('windows','x86_64-pc-windows-msvc')]:
    suffix='.exe' if platform=='windows' else ''
    extension='zip' if platform=='windows' else 'tar.gz'
    archive=DOWNLOAD/platform/f'nestbolt-v{VERSION}-{target}.{extension}'
    executables=['nestbolt'+suffix,'nestbolt-mcp'+suffix]
    if platform=='windows':
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert len(z.namelist())==6 and set(z.namelist())==set(documents+executables)
            files={n:z.read(n) for n in z.namelist()}
    else:
        with tarfile.open(archive,'r:gz') as z:
            members=z.getmembers()
            assert len(members)==6 and {m.name for m in members}==set(documents+executables)
            assert all(m.isfile() for m in members)
            assert all((m.mode&0o777)==(0o755 if m.name in executables else 0o644) for m in members)
            files={m.name:z.extractfile(m).read() for m in members}
    for name in documents:assert files[name]==expected_documents[name],(platform,name)
    for name in executables:
        binary=files[name]
        if platform=='linux':
            assert binary[:6]==b'\x7fELF\x02\x01' and struct.unpack_from('<H',binary,18)[0]==62
        elif platform=='macos':
            assert struct.unpack_from('<II',binary)==(0xfeedfacf,0x0100000c)
        else:
            assert binary[:2]==b'MZ'
            pe=struct.unpack_from('<I',binary,0x3c)[0]
            assert binary[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',binary,pe+4)[0]==0x8664
            assert b'vcruntime140' not in binary.lower()
    rows.append({'platform':platform,'target':target,'file':archive.name,'bytes':archive.stat().st_size,
        'sha256':digest(archive.read_bytes()),'members':{n:{'sha256':digest(b),'bytes':len(b)} for n,b in files.items()},
        'architecture_correct':True,'documents_match_commit':True,'native_runner_version_smoke_passed':True})
    if platform=='windows':
        extracted=DOWNLOAD/'windows-extracted';extracted.mkdir()
        assert DOWNLOAD.resolve() in extracted.resolve().parents
        for name,binary in files.items():
            assert Path(name).name==name
            with (extracted/name).open('xb') as f:f.write(binary)
bundle=DOWNLOAD/'windows/nestbolt-windows-x64.mcpb'
expected=(DOWNLOAD/'windows/nestbolt-windows-x64.mcpb.sha256').read_text(encoding='utf-8').split()[0]
assert digest(bundle.read_bytes())==expected
metadata=json.loads((DOWNLOAD/'windows/server.registry.json').read_bytes())
assert metadata['version']==VERSION and metadata['packages'][0]['version']==VERSION
assert metadata['packages'][0]['fileSha256']==expected
assert metadata['packages'][0]['identifier']==f'https://github.com/skulitom/Nestbolt/releases/download/v{VERSION}/nestbolt-windows-x64.mcpb'
with zipfile.ZipFile(bundle) as z:
    assert z.testzip() is None
    assert z.read('server/nestbolt-mcp.exe')==(DOWNLOAD/'windows-extracted/nestbolt-mcp.exe').read_bytes()
    assert json.loads(z.read('manifest.json'))['version']==VERSION
shutil.copyfile(DOWNLOAD/'windows/server.registry.json',OUT/'server.registry.json')
for relative in ['Cargo.toml',*[p.relative_to(ROOT).as_posix() for p in (ROOT/'mcpb').glob('*.mjs')]]:
    source=ROOT/relative; target=ISOLATED/relative;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
    assert digest(target.read_bytes())==digest(subprocess.check_output(['git','show','7eba929:'+relative],cwd=ROOT).replace(b'\n',b'\n')) or target.read_bytes().replace(b'\r\n',b'\n')==subprocess.check_output(['git','show','7eba929:'+relative],cwd=ROOT)
smoke=ISOLATED/'smoke.mjs'
smoke.write_text("import { smoke } from './mcpb/archive.mjs';\nimport path from 'node:path';\nsmoke({cli:path.resolve('../windows-extracted/nestbolt.exe'),server:path.resolve('../windows-extracted/nestbolt-mcp.exe'),version:'0.2.0-alpha.1'});\nconsole.log('Downloaded Windows archive: CLI and MCP versions passed');\n",encoding='utf-8',newline='\n')
stages=[]
for name,command in [('archive-smoke',['node',str(smoke)]),('mcpb-smoke',['node',str(ISOLATED/'mcpb/verify.mjs'),str(bundle)])]:
    with (OUT/(name+'-stdout.log')).open('wb') as out,(OUT/(name+'-stderr.log')).open('wb') as err:
        r=subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),*command],cwd=ISOLATED,stdout=out,stderr=err,timeout=120)
    stages.append({'name':name,'command':command,'exit_code':r.returncode})
    write(OUT/'progress.json',stages)
    assert r.returncode==0,name
write(OUT/'checks.json',{'all_checks_passed':True,'release_commit':workflow['headSha'],'version':VERSION,
    'workflow_url':workflow['url'],'dry_run_only':True,'release_job_skipped':True,
    'archives':rows,'MCPB_sha256':expected,'MCPB_matches_native_archive_server':True,
    'downloaded_Windows_archive_and_MCPB_smokes':stages,'isolated_verifier_root':str(ISOLATED),
    'verifier_source_unchanged':True,'native_checks_on_other_platforms':'CI runners, not locally executed',
    'provenance_attestation':'Dry runs do not attest; verify published artifact attestation after release',
    'registry_metadata_validated_but_not_published':True,'performance_and_release_commit_CI_pending':True})
print(json.dumps({'all_checks_passed':True,'platforms':3,'MCPB_sha256':expected}))
