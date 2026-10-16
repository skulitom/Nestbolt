"""Preserve the Windows Python-launch fault and resume the unchanged package checks."""
from pathlib import Path
from hashlib import sha256
import ast
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/preview-depth-verification-recovery-20261016'
DOWNLOAD=ROOT/'output/preview-depth-published-20261016'
PROOF=ROOT/'benchmarks/results/preview-depth-published-20261016'
SEQ=ROOT/'output/preview-depth-publication-sequence-20261016'
original=ROOT/'output/verify_published_depth_preview.py'
generated=ROOT/'output/verify_published_depth_preview_packages.py'
assert not OUT.exists() and not PROOF.exists() and not (DOWNLOAD/'isolated-verifier').exists()
failure=(SEQ/'stage-0-stderr.log').read_text(encoding='utf-8')
assert 'WinError 193' in failure and "str(ROOT/'output/ccd1.py'),str(verifier)" in failure
assert json.loads((SEQ/'progress.json').read_bytes())[0]['exit_code']==1
assert json.loads((SEQ/'interruption.json').read_bytes())['stages'][0]['exit_code']==1
assert generated.is_file()
OUT.mkdir()
for p in [original,generated,SEQ/'plan.json',SEQ/'opened.json',SEQ/'progress.json',SEQ/'interruption.json',SEQ/'stage-0-stdout.log',SEQ/'stage-0-stderr.log']:
    shutil.copyfile(p,OUT/p.name)
(OUT/'original-download-metadata').mkdir()
for p in DOWNLOAD.iterdir():
    if p.is_file():shutil.copyfile(p,OUT/'original-download-metadata'/p.name)
source=original.read_text(encoding='utf-8')
replacements=[
 ("assert not DOWNLOAD.exists() and not OUT.exists(), 'Preserve any earlier verification attempt'\nDOWNLOAD.mkdir()",
  "assert DOWNLOAD.exists() and not OUT.exists(), 'Preserve the original downloaded files; the package checker has never started'"),
 ("subprocess.run(['gh','release','download',TAG,'-R',REPO,'-D',str(DOWNLOAD/'assets')],cwd=ROOT,check=True,timeout=180)",
  "# Original assets are retained and all original name/checksum/metadata checks run below."),
 ("    (DOWNLOAD/platform).mkdir()\n    shutil.copyfile(DOWNLOAD/'assets'/name,DOWNLOAD/platform/name)",
  "    assert (DOWNLOAD/platform).is_dir()\n    assert (DOWNLOAD/'assets'/name).read_bytes() == (DOWNLOAD/platform/name).read_bytes()"),
 ("    shutil.copyfile(DOWNLOAD/'assets'/name,DOWNLOAD/'windows'/name)",
  "    assert (DOWNLOAD/'assets'/name).read_bytes() == (DOWNLOAD/'windows'/name).read_bytes()"),
 ("subprocess.run(['gh','run','download',str(args.run),'-n','nestbolt-mcpb','-D',str(DOWNLOAD/'workflow-bundle')],\n    cwd=ROOT,check=True,timeout=180)",
  "assert (DOWNLOAD/'workflow-bundle').is_dir() # Original workflow bundle retained."),
 ("shutil.copyfile(DOWNLOAD/'workflow-bundle/server.registry.json',DOWNLOAD/'windows/server.registry.json')",
  "assert (DOWNLOAD/'workflow-bundle/server.registry.json').read_bytes() == (DOWNLOAD/'windows/server.registry.json').read_bytes()"),
 ("assert not verifier.exists()\ncompile(source,str(verifier),'exec')\nverifier.write_text(source,encoding='utf-8',newline='\\n')",
  "assert verifier.exists()\ncompile(source,str(verifier),'exec')\nassert verifier.read_text(encoding='utf-8') == source, 'The generated package-check logic must be unchanged'"),
 ("subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),str(verifier)],cwd=ROOT,check=True,timeout=300)",
  "subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),sys.executable,str(verifier)],cwd=ROOT,check=True,timeout=300)"),
]
for before,after in replacements:
    assert source.count(before)==1,before
    source=source.replace(before,after)
ast.parse(source)
runner=ROOT/'output/complete_published_depth_verification.py';assert not runner.exists()
runner.write_text(source,encoding='utf-8',newline='\n')
(OUT/'resume.py').write_bytes(runner.read_bytes())
(OUT/'prepare.py').write_bytes(Path(__file__).read_bytes())
inventory={p.relative_to(OUT).as_posix():{'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()}
plan={'cause':'Windows attempted to execute a .py file directly through CreateProcess; WinError 193 before the package checker started.',
 'changed_launch':'Pass the Python interpreter explicitly through the CCD1 wrapper.',
 'original_downloads_and_failed_logs_preserved':True,'package_checker_logic_unchanged':True,
 'same_checksum_tag_source_stable_latest_provenance_checks':True,'no_asset_replaced_or_redownloaded':True,
 'package_tests_previously_started':False,'release_republished':False,'registry_publication_started':False,
 'original_generated_package_verifier_sha256':sha256(generated.read_bytes()).hexdigest(),'captured_files':inventory,
 'command':['python','output/ccd1.py','python','-X','utf8','output/complete_published_depth_verification.py','--run','38882959832','--commit','c36baa8145e9e7b51e5667f4e4eaa0242256fc6e']}
(OUT/'recovery-plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'recovery_prepared':True,'original_launch_failure_preserved':True,'package_checks_unchanged':True}))
