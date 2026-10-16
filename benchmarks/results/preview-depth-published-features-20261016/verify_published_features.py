"""Apply the already reviewed authored-feature checks to published Windows downloads."""
from pathlib import Path
from hashlib import sha256
import ast
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
proof=json.loads((ROOT/'benchmarks/results/preview-depth-published-20261016/publication-verification.json').read_bytes())
assert proof['all_checks_passed'] and proof['all_four_artifacts_have_verified_provenance']
commit=proof['commit'];assert len(commit)==40 and all(c in '0123456789abcdef' for c in commit)
source=(ROOT/'output/check_downloaded_depth_features.py').read_text(encoding='utf-8')
replacements=[('preview-depth-feature-checks-20261016','preview-depth-published-feature-checks-20261016'),
    ('preview-depth-release-dryrun-38854620093','preview-depth-published-20261016'),
    ('preview-depth-release-dryrun-20261016','preview-depth-published-20261016'),('23442be',commit)]
for before,after in replacements:
    assert before in source,before
    source=source.replace(before,after)
ast.parse(source)
runner=ROOT/'output/check_published_depth_features.py';assert not runner.exists()
runner.write_text(source,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),'python',str(runner)],cwd=ROOT,check=True,timeout=300)
seal=(ROOT/'output/seal_downloaded_depth_features.py').read_text(encoding='utf-8')
# The original sealer also edited then-current release documents. Keep its
# archive checks unchanged and prepare current publication documentation separately.
cut="path=root/'docs/RELEASE_READINESS.md'"
assert seal.count(cut)==1
seal=seal[:seal.index(cut)] + "print(json.dumps({'sealed':str(out),'members':len(inventory),'bytes':archive.stat().st_size,'sha256':digest(archive)}))\n"
replacements=[('preview-depth-feature-checks-20261016','preview-depth-published-feature-checks-20261016'),
    ('preview-depth-features-20261016','preview-depth-published-features-20261016'),
    ('preview-depth-release-dryrun-20261016.md','preview-depth-published-20261016/publication-verification.json'),
    ('packages from dry-run commit `23442be`', 'published packages from commit `'+commit[:7]+'`'),
    ('All operations here run\non CCD1, separately from the active H4 measurements.',
     'All operations here run\non CCD1, separately from any active quality measurements.'),
    ('Full current quality/scale/export review and hosted checks remain required.\nNo release, registry publication or milestone closure occurs; completion is 45%.',
     'The packages are the actual published preview downloads, whose source tag,\nchecksums and provenance have already been verified. These functional checks\ndo not publish a registry version or close any additional milestone.')]
for before,after in replacements:
    assert before in seal,before
    seal=seal.replace(before,after)
ast.parse(seal)
sealer=ROOT/'output/seal_published_depth_features.py';assert not sealer.exists()
sealer.write_text(seal,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),'python',str(sealer)],cwd=ROOT,check=True,timeout=120)
out=ROOT/'benchmarks/results/preview-depth-published-features-20261016'
(out/'verify_published_features.py').write_bytes(Path(__file__).read_bytes())
write={'published_commit':commit,'release_url':proof['release_url'],'all_checks_passed':True,
    'same_reviewed_functional_checks_on_new_published_artifacts':True,
    'runner_sha256':sha256(runner.read_bytes()).hexdigest(),'sealer_sha256':sha256(sealer.read_bytes()).hexdigest(),
    'publication_verification_sha256':sha256((ROOT/'benchmarks/results/preview-depth-published-20261016/publication-verification.json').read_bytes()).hexdigest()}
(out/'published-binding.json').write_text(json.dumps(write,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(write))
