"""Install the verified Oct26 evidence and record the Oct28 upstream merge."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-cog-corner-support-20261026';READY=ROOT/'output'/f'{NAME}-checkpoint';OUT=ROOT/'benchmarks/results'/NAME
BASE='36f162d0df3d5c88eb4145c58004890b650fba61';LOCAL='babe73b661efe8ac84c4f73c5823a7178274ec00';UPSTREAM='effd34c5531a6187881ec37d460a59568ef5aefe'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
head=command(['git','rev-parse','HEAD']);parents=command(['git','rev-list','--parents','-n','1','HEAD']).split();assert parents==[head,LOCAL,UPSTREAM]
assert command(['git','ls-remote','origin','refs/heads/main']).split()[0]==UPSTREAM
old=load(ROOT/'benchmarks/results/h5-corrected49-flat-edge-20261026/source-review.json')
assert source_digest()==old['production_digest'];readmes={n:digest(ROOT/n) for n in old['current_readmes']};assert readmes==old['current_readmes']
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
 'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
 'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
 'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==old[k] for k in upstream)
preserved={}
for label,rev in [('local',LOCAL),('upstream',UPSTREAM)]:
    paths=command(['git','diff','--name-only',BASE+'..'+rev]).splitlines();rows=[]
    for path in paths:
        oid=command(['git','rev-parse',rev+':'+path]);assert command(['git','rev-parse','HEAD:'+path])==oid
        rows.append({'path':path,'blob':oid})
    preserved[label]=rows
assert len(preserved['upstream'])==14 and not ({r['path'] for r in preserved['local']}&{r['path'] for r in preserved['upstream']})
checks={}
for label,run,rev in [('local',40412648984,LOCAL),('upstream',40488718114,UPSTREAM)]:
    ci=json.loads(command(['gh','run','view',str(run),'--json','databaseId,status,conclusion,headSha,jobs,url']))
    assert ci['headSha']==rev and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    checks[label]=ci
manifest=load(READY/'raw-manifest.json');canonical={}
for archive in manifest['archives']:
    p=READY/archive['path'];assert p.stat().st_size==archive['bytes'] and digest(p)==archive['sha256']
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        for row in [r for r in manifest['files'] if r['archive']==p.name]:
            data=z.read(row['path']);assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256'];canonical[row['path']]=row
for row in manifest['aliases']:
    original=canonical[row['canonical']];assert all(row[k]==original[k] for k in ['bytes','sha256','archive'])
assert load(READY/'checks.json')['passed']
OUT.mkdir()
for p in READY.iterdir():
    if p.name in ['report.md','append-note.md','next-step.json']:continue
    assert p.is_file();shutil.copyfile(p,OUT/p.name)
shutil.copyfile(READY/'next-step.json',OUT/'prepared-next-step.json')
write(OUT/'merge-preservation.json',{'base':BASE,'local_parent':LOCAL,'upstream_parent':UPSTREAM,'merged_head':head,'conflicts':0,'disjoint_changed_paths':True,'files_preserved':preserved})
for label,ci in checks.items():write(OUT/(label+'-six-passed.json'),ci)
write(OUT/'publication-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'merged_head':head,'remote_main':UPSTREAM,
 'production_digest':source_digest(),'current_readmes':readmes,**upstream,'upstream_heads_and_releases_unchanged':True,
 'upstream_example_files_preserved':14,'both_parent_heads_have_all6_checks':True,'combined_head_ci_pending':True,
 'archive_canonical_files_reverified':len(canonical),'archive_aliases_reverified':len(manifest['aliases']),
 'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'new_release_qualified':False})
write(OUT/'next-step.json',{'action':'The new remote main effd34c5 example page is preserved in a clean two-parent merge with babe73b6. Both parent heads pass all6 Checks jobs; product source and READMEs are unchanged. Stage and byte-check this evidence-only installation, commit it, then normally fast-forward main only after checking it still equals effd34c5 and no main CI is live. Capture and preserve the new combined main CI until completion. Do not run the obsolete push_sparse_checkout_validated_main.py helper: its pre-change36f162d0 guard no longer applies. All previous feasibility searches stay closed. The first-sheet13-cog count is UNKNOWN at the shared200000-node cap; short<=3 is the only proven capacity. Actual-tooth corner boxes remove34 further cells, leaving4514, and preserve all15 reference centers. Do not repeat a feasibility search solely for this modest tightening. Next seek a materially stronger decomposition or different source construction, preserving all66 original parts, guards and material targets. H2 remains open as Artem requested,22 reserved vectors remain unopened, and no release qualifies.','completion_percent':60,'H2_complete':False,'H5_complete':False})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=(READY/'report.md').read_text(encoding='utf-8')+f'''

## Publication reconciliation — 2026-10-28

Remote main advanced to `effd34c5` with the layered laser-kit example page.
Its14 changed files are preserved by exact Git blob identity in a clean merge;
the local checkpoint's changed files are also preserved exactly, with no overlap
or conflict. [The local parent](https://github.com/skulitom/Nestbolt/actions/runs/40412648984)
and [new main parent](https://github.com/skulitom/Nestbolt/actions/runs/40488718114)
each pass all six jobs. The sparse-checkout browser run passes86 tests with
four opt-in skips; checkout takes10 seconds. The product source, README files
and Sparrow/Studio heads and releases remain unchanged. The combined head will
receive its own main CI run after the normal push. No new release is qualified.

[Merge preservation]({NAME}/merge-preservation.json),
[publication review]({NAME}/publication-review.json),
[next step]({NAME}/next-step.json).
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=(READY/'append-note.md').read_text(encoding='utf-8')+'''
Publication update2026-10-28: remote main's14 layered-kit example files are
preserved in a clean merge with the five queued checkpoints. Both parent heads
pass all six jobs; product source, READMEs and upstream releases are unchanged.
The combined main head will receive its own checks after the normal push.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'installed':NAME,'merged_head':head,'canonical_files_reverified':len(canonical),'upstream_files_preserved':14,'local_files_preserved':len(preserved['local'])})
