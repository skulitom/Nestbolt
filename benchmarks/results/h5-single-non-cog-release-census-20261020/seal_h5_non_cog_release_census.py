"""Seal exact single-part release certificates and the successful remote checks."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-single-non-cog-release-census-20261020'
RUN=ROOT/'output'/PREFIX
OUT=ROOT/'benchmarks/results'/PREFIX
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)

def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,indent=2)
        f.write('\n')

def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as f:
        f.write(text)

def main():
    OUT.mkdir()
    head=git('rev-parse','HEAD').decode().strip()
    assert head=='00e244d939ebffdd50207f8fc0da2d7d4a45d6e0'
    core=source_digest()
    assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    result=load(RUN/'result.json')
    audit=load(RUN/'audit/checks.json')
    refined=load(RUN/'component-covers/checks.json')
    assert result['cases_completed']==51 and not result['pending_candidates'] and not result['limit_reached']
    assert audit['passed'] and audit['components_verified']==121 and audit['band_covers_verified']==242
    assert refined['passed'] and refined['single_pose_changes_ruled_out']==33
    assert refined['by_part']=={'frame':{'ruled_out':0,'inconclusive':18},
                               'bracket':{'ruled_out':12,'inconclusive':0},
                               'insert':{'ruled_out':21,'inconclusive':0}}
    prior=load(ROOT/'benchmarks/results/h5-cog-free-regions-and-continuous-capacity-20261020/source-review.json')
    readmes={p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']}
    assert readmes==prior['current_readmes']
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert remote=='abeb2739b1eedde18781b46fd82258f356970be0'
    ci=json.loads(subprocess.check_output(
        ['gh','run','view','39454262478','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==remote and ci['conclusion']=='success'
    assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(OUT/'main-ci-abeb2739-success.json',ci)
    inputs={}
    for root in [RUN,RUN/'component-covers']:
        for name,h in load(root/'plan.json')['inputs'].items():
            assert digest(ROOT/name)==h
            inputs[name]=h
    next_step=('Do not test single bracket or insert changes around this arrangement: the all-angle relaxation excludes all33. '
               'The18 frame releases remain inconclusive, with upper bounds15–17 and no returned placement. '
               'Next examine original-outline free translation regions for a moved frame at its allowed quarter-turn rotations while keeping the other50 non-cog poses fixed. '
               'Preserve the original frame pose and explicitly audit any new contact choices before considering a changed joint frame/cog construction. '
               'A released frame must be restored and all15 cogs placed; deleting a part never qualifies the original job. '
               'Multiple non-cog moves remain possible. Do not reuse a conflict graph conditional on the former fixed group.')
    write(OUT/'source-review.json',{
        'verified_utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'production_digest':core,
        'current_readmes':readmes,'README_change_needed':False,'remote_main':remote,
        'remote_main_all_six_checks_pass':True,'new_local_commit_checks_not_inferred':True,
        'original_geometry_layout_calls':0,'fresh_frozen_CLI_calls':0,'native_packing_calls':0,
        'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,
        'new_release_qualified':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,
        'next_investigation':next_step})
    for p,name in [(RUN/'result.json','census-result.json'),(RUN/'audit/checks.json','census-audit.json'),
                   (RUN/'component-covers/checks.json','component-cover-audit.json')]:
        shutil.copyfile(p,OUT/name)
    members={}
    for p in sorted(RUN.rglob('*')):
        if p.is_file():
            members[RUN.name+'/'+p.relative_to(RUN).as_posix()]=p
    for name in inputs:
        p=ROOT/name
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['census_h5_non_cog_releases.py','audit_h5_non_cog_releases.py',
                                      'refine_h5_non_cog_release_components.py','ccd1.py']]
    visited=set()
    while pending:
        p=pending.pop()
        if p in visited:
            continue
        visited.add(p)
        members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module
                  else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for module in mods:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():
                    pending.append(other)
    manifest=[]
    archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name)
            manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:
            assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{
        'passed':True,'all_inputs_verified':True,'cases_verified':51,'components_verified':121,
        'band_covers_verified':242,'initial_single_changes_ruled_out':32,
        'refined_single_changes_ruled_out':33,'all_bracket_and_insert_single_changes_ruled_out':True,
        'inconclusive_frame_changes':18,'frame_move_feasibility_claimed':False,
        'remote_main_all_six_checks_pass':True,'new_release_qualified':False,'completion_percent':60,
        'archive_members':len(manifest),'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: which single non-cog part could move? — 2026-10-20

**Moving one bracket or insert alone cannot complete this arrangement.**
All twelve bracket choices and all twenty-one insert choices are ruled out by
independently checked bounds allowing arbitrary cog angles and continuous
positions. Moving one of the eighteen frames remains inconclusive. This does
not prove a frame move can work or exclude changes to multiple non-cog parts.
H2/H5 remain open at 60%.

## A necessary relaxation for each part

The [preceding certificate](h5-cog-free-regions-and-continuous-capacity-20261020.md)
allows at most thirteen cogs with all 51 non-cog poses fixed. This census
removes each non-cog obstacle in turn while keeping the other fifty in place.
Omitting the removed part makes the problem more generous than relocating it:
if even that space cannot hold fifteen cogs, moving only that part cannot
solve the original job.

The census declares 51 cases in candidate-index order and a 90-second limit,
stopping only between cases. All 51 finish in **24.103865400 seconds**, with
no pending cases or limit extension. It makes no solver, native packing or
quality call and produces no new layout.

For each case, the conservative inscribed-disk center regions are recomputed
from the remaining original-geometry interior rectangles. Each region component
gets a reachable-area bound, a bounding-box diameter cover, and two finite band
covers. Whole-sheet area bounds remain available where tighter.

A separate audit verifies every obstacle removal, exact center-region
complement and reachable-area total, all **121 components** and **242 band
covers**. All original seed center regions remain included. Its independent
integer event sweep agrees with every area; the audit takes **7.276938200 seconds**.

## Tighten the one remaining insert case

The initial component bounds exclude 32 changes: all twelve brackets and
twenty inserts. Insert candidate **8529** initially remains inconclusive at
fifteen. Removing it creates two separate, small possible-center regions on
the first sheet; counting their capacities independently permits one cog in
each. Their centers cannot actually coexist: every corner pair of their
bounding boxes lies strictly closer than the necessary **218.4313 mm**
center separation.

A saved component-clique certificate covers those two regions together with
capacity one. Separate corner-pair checks verify this certificate and every
component partition across all 51 cases. Candidate 8529's bound drops from
15 to **14**, excluding it too. The original looser result is retained.

| Removed part family | Cases | Single change ruled out | Still inconclusive |
| --- | ---: | ---: | ---: |
| Frame | 18 | 0 | 18 |
| Bracket | 12 | 12 | 0 |
| Insert | 21 | 21 | 0 |

The eighteen frame releases have necessary upper bounds of **15–17 cogs**.
These are capacity bounds, not achievable counts or replacement frame
positions. Any candidate must restore the released frame, retain the other
parts and place all fifteen cogs before original validation can succeed.

## Source, checks and release

All six hosted checks on remote main **abeb2739** now pass, including Windows,
Linux, browsers, benchmark smoke and both maker rebuilds. This confirms that
exact remote checkpoint; it does not stand in for checks on the subsequent
local evidence commits.

Core source and all three README hashes remain unchanged. The README still
accurately describes v0.2.0-alpha.1, stable v0.1.0 and the open v1.1 work.
No release is qualified by these conditional bounds. No reserved held-out
file is evaluated, no acceptance rule changes and no additional CLI layout
validation is called because no new layout is produced.

## Next work

{next_step}

[Checks]({PREFIX}/checks.json), [original census]({PREFIX}/census-result.json),
[independent audit]({PREFIX}/census-audit.json),
[refined component certificates]({PREFIX}/component-cover-audit.json),
[successful remote checks]({PREFIX}/main-ci-abeb2739-success.json),
[source review]({PREFIX}/source-review.json), [all case certificates]({PREFIX}/raw.zip)
and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 single non-cog release census, 2026-10-20:** [all 51 independently audited cases](../benchmarks/results/{PREFIX}.md)
rule out completing the current arrangement by moving only one bracket or
insert: all 12 bracket and 21 insert choices have cog capacity below the
required 15, even when the removed part is omitted entirely. All 121 center
components and 242 diameter covers verify. A separate component certificate
tightens the last insert case from 15 to 14; its original loose result remains.
The 18 frame releases remain inconclusive at bounds of 15–17, with no new
layout or feasibility claim. Next analyze changed frame positions while
preserving the other 50 non-cog poses; multiple-part changes remain possible.
All six hosted checks on remote abeb2739 now pass. Core source, README and
release assets are unchanged; no native quality or held-out run occurs.
H2/H5 remain open at 60%.
'''
    assert (ROOT/'BENCHMARKS.md').read_bytes()==git('show','HEAD:BENCHMARKS.md')
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
        append(ROOT/name,'\n'+note)
    path=ROOT/'docs/STATUS.md'
    text=path.read_text(encoding='utf-8')
    marker='**N4 cog free regions and continuous capacity, 2026-10-20:**'
    assert text.count(marker)==1
    path.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
                      'single_changes_ruled_out':33,'completion_percent':60}))

if __name__=='__main__':
    main()
