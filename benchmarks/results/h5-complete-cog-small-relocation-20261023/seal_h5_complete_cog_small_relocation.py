"""Seal two new complete-cog small-part experiments, including every shortfall."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-complete-cog-small-relocation-20261023';OUT=ROOT/'benchmarks/results'/NAME
EIGHT=ROOT/'output/h5-group-small-completion-20261023'
JOINT=ROOT/'output/h5-complete-cog-small-pool-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();records=[]
    for tag,base in [('eight',EIGHT),('joint',JOINT)]:
        data={k:load(base/p) for k,p in [('generation','result.json'),('area','area-preflight.json'),('graph','audit/checks.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
        assert all(data[k]['passed'] for k in ['graph','model','layouts'])
        assert not data['generation']['pending_queries'] and not data['generation']['pending_proposal_lists'] and not data['generation']['compression_limit_reached']
        assert not data['layouts']['full_target_witness'] and not data['layouts']['native_margin_qualified']
        for k,v in data.items():write(OUT/f'{tag}-{k}.json',v)
        shutil.copyfile(base/'plan.json',OUT/f'{tag}-plan.json');records.append(data)
    a,b=records
    assert a['generation']['retained_candidates']==99 and a['generation']['new_candidates']=={'insert':56}
    assert a['solver']['status']=='OPTIMAL' and a['solver']['objective']==a['solver']['best_bound']==59400000
    assert a['layouts']['layouts_checked_including_hint']==2 and a['layouts']['fresh_frozen_CLI_calls']==2
    assert b['generation']['retained_candidates']==2045 and b['generation']['new_candidates']=={'bracket':180,'insert':171}
    assert b['solver']['status']=='FEASIBLE' and b['solver']['objective']==736200000 and b['solver']['best_bound']==763200000<b['model']['full_score']==895800000
    assert b['layouts']['layouts_checked_including_hint']==3 and b['layouts']['fresh_frozen_CLI_calls']==2 and b['layouts']['exact_CLI_results_reused']==1
    assert all(r['missing']=={'bracket':3,'insert':2} for r in b['layouts']['records'])
    prior=load(ROOT/'benchmarks/results/h5-dense-cog-limit-20261023/source-review.json')
    assert source_digest()==prior['production_digest'] and prior['current_readmes']=={p:digest(ROOT/p) for p in prior['current_readmes']}
    ci=json.loads(subprocess.check_output(['gh','run','view','39950507182','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']=='2333dd2c590750fa44a3170b34827c25320fe755';write(OUT/'main-ci-2333dd2c.json',ci)
    next_step=('Do not repeat either solve, extend its time limit, or treat this 61-part result as an improvement over the saved 64-part partial. The chosen cog arrangement came from minimum disruption of the old small parts; that ranking does not establish best packability after all small parts move. Next declare a finite comparison across the other saved complete-cog cases from output/h5-dense-group-blockers-20261023/cases.json. Retain the same 18 frames, reconstruct every 15-cog case from its source group/drop/last-cog specification, and independently validate any new compatibility graph against original geometry. Reuse the full bracket/insert source pool before fixed-cog filtering, including current new contacts; add group-conditioned contacts only under newly declared caps. Compare compatible small-part placements and use any checked stronger arrangement as a seed for one newly declared group-selection model. Keep each original case, excluded pose, failed result, bound and pending suffix. This changes the cog arrangement and the discrete group decision; it is not a retry of the expired single-group or free-all-small models. Any 66-part witness still needs native margins, unchanged production repair limits/budget, and the complete H5 scope. H2 retains Artem\'s original gate decision.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
      'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,
      'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,
      'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [EIGHT,JOINT]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for source in [load(root/'plan.json')['inputs'],load(root/'solve/model-audit.json')['input_hashes']]:
            for name,h in source.items():assert digest(ROOT/name)==h;inputs[name]=h
        for p in (root/'layout-audit').glob('validation-reuse-*.json'):
            for name,h in load(p)['source_files'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-dense-insert-gap-20261023',['layout.json','checks.json']),('h5-dense-group-blockers-20261023',['plan.json','cases.json','best-case.json','best-subassembly.json','audit/checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_group_small_completion.py','audit_h5_group_small_completion.py','solve_h5_group_small_completion.py','audit_h5_group_small_layouts.py','build_h5_complete_cog_small_pool.py','audit_h5_complete_cog_small_pool.py','solve_h5_complete_cog_small_pool.py','audit_h5_complete_cog_small_layouts.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'all_geometry_graph_model_and_layout_audits_pass':True,
      'best_retained_parts':64,'new_results_parts':61,'new_results_improve_retained_partial':False,'joint_upper_bound_below_full_inventory_score':True,
      'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,
      'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    passing=sum(j['conclusion']=='success' for j in ci['jobs'])
    ci_text=('All six checks on main `2333dd2c` pass.' if ci['conclusion']=='success' else f'The saved main `2333dd2c` snapshot is {ci["status"]}, with {passing} successful checks; a complete pass is not inferred.')
    report=f'''# H5: completing the selected cog group — 2026-10-23

**The best retained layout remains 64/66 parts.** Two new constructions around
the selected complete-cog arrangement reach 61/66, missing three brackets and
two inserts. Their smaller filled area does not improve the retained result.
The second model's upper bound excludes the full inventory in its finite pool,
but neither experiment proves continuous geometric impossibility. H2/H5 remain
open at **60%**.

## Eight missing parts around the checked 58-part subassembly

The [previous census](h5-dense-cog-limit-20261023.md) selected case 20, group 96
with member 3 omitted and the original last-sheet cog added. Exactly 18 frames,
15 cogs, nine brackets and 16 inserts stay fixed. Original stock and filled-area
arithmetic leave 644,250.519695 mm² free for the missing 219,000 mm². This necessary
area check passes; it does not establish that the gaps can hold those shapes.

Twenty newly declared translation-region queries cover all eight allowed bracket
orientations/reflections and both equivalent insert size classes on both sheets.
All finish within the 120-second generation allowance. All 16 bracket construction
regions are empty. The two first-sheet insert queries supply 56 new poses; all
last-sheet construction regions are empty. These are conservative, positively
padded regions, so their emptiness alone is not a continuous impossibility proof.
All 43 compatible prior poses are inserts, giving 99 total candidates. All 57
proposal events, including one duplicate, are preserved; nothing remains pending.

Independent checks cover 437,704 prior/fixed pairs, 2,622 proposal/fixed pairs,
the exact fixed subassembly and original stock. All 4,851 candidate pairs are
accounted for; 2,814 exact distances establish 2,814 conflicts, covered by 27
verified cliques. There are no rejected geometric proposals, residual edges or
compression expiry. Area arithmetic and the complete protobuf model are checked
independently. The empty bracket-family constraint is recorded as identically true.

One 30-second-limit, eight-worker, seed-zero solve finishes in 0.010675100 seconds
with a finite-pool optimum of three additional inserts. The hint and returned
layout receive fresh frozen-CLI calls; each fails only for the corresponding
missing quantities. The returned 61-part layout contains nine brackets, 19 inserts,
all 18 frames and all 15 cogs. Its 4,322,140.784070 mm² filled area is below the
saved 64-part layout's 4,381,615.346194 mm². Charged material remains
4,988,890.203495 mm², under the original target. No native margin is qualified.

## Move every bracket and insert together

A separately declared construction fixes only the 33 frame/cog poses, allowing
all 12 brackets and 21 inserts to move. It retains the complete nine-bracket,
19-insert seed and returns to the full prior source pool before small-part
filtering. Thus candidates previously blocked by the fixed small parts are
available again; no previous failed solve is retried.

All 20 new queries finish. The pool contains 1,694 compatible prior poses plus
180 new bracket and 171 new insert poses: 2,045 choices. All 496 proposal events
are retained, including 145 duplicates. Generation takes 9.742350500 seconds;
neither candidate cap nor time cap is reached, and no proposal is pending.

The independent audit checks 295,381 prior/fixed and 11,842 proposal/fixed pairs.
Among 1,149,136 same-sheet candidate pairs, 381,104 exact distances establish
342,611 conflicts. All are covered by 2,100 verified cliques without residual
edges or compression expiry. The original 28-small-part seed and every stock
bound are verified. All protobuf fields and the weighted filled-area objective
are reconstructed before solving.

One 30-second-limit call takes 30.040612200 seconds; the soft overrun is retained.
It returns `FEASIBLE` with the same 61 parts. Score 736,200,000 and upper bound
763,200,000 remain apart, so an optimum is not claimed. The full-inventory score
is 895,800,000: the returned bound excludes a complete packing within this
particular finite pool. It makes no claim about ungenerated poses or other
cog arrangements. No limit extension or second call is made.

The exact starting layout reuses its byte-verified frozen-CLI result. The callback
and different final layout each receive a fresh original CLI check. All three
layouts pass original filled-outer geometry, 1,242 same-sheet pairs each, and
retain precisely the three-bracket/two-insert quantity shortfall. The final uses
four newly generated poses but does not improve filled area. Minimum clearance
is about 0.2011 mm; native margins remain unqualified.

## Next action and repository state

{next_step}

{ci_text} The preceding `db703a0c` checkpoint is local and waiting for that run
to finish before the next normal push, avoiding cancellation of live checks.
Production source and all three README hashes remain unchanged. The published
preview is still accurate; diagnostic evidence alone does not qualify a new
application build. No production packing, quality matrix, new native LightBurn
check or reserved-input evaluation occurs. Original acceptance and repair limits
remain unchanged.

Evidence: [first plan]({NAME}/eight-plan.json), [first generation]({NAME}/eight-generation.json),
[first graph audit]({NAME}/eight-graph.json), [first model]({NAME}/eight-model.json),
[first result]({NAME}/eight-solver.json), [first original layouts]({NAME}/eight-layouts.json),
[joint plan]({NAME}/joint-plan.json), [joint generation]({NAME}/joint-generation.json),
[joint graph audit]({NAME}/joint-graph.json), [joint model]({NAME}/joint-model.json),
[joint result]({NAME}/joint-solver.json), [joint original layouts]({NAME}/joint-layouts.json),
[source review]({NAME}/source-review.json), [raw evidence]({NAME}/raw.zip), and
[manifest]({NAME}/raw-manifest.json). All {len(manifest)} archive members, CRCs and
byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 complete-cog small-part relocation, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
preserves the best 64/66 partial. Around the checked 58-part subassembly, all 20
new queries finish; 99 insert choices yield a finite optimum of three additional
inserts. A distinct model fixes only the 18 frames and all 15 cogs, freeing every
bracket and insert. Its 2,045 choices, 342,611 conflicts and full model pass
independent checks. One bounded solve retains 61 parts, missing three brackets
and two inserts. Its bound excludes the complete inventory in this finite pool;
no continuous impossibility or optimum is claimed. All returned original layouts
are audited and their quantity-only CLI failures retained. No pending list is
resumed and no solve repeated. Next compare other saved complete-cog arrangements
with small parts free, using fresh declared limits. Source, accurate READMEs and
releases remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'CI_status':ci['status'],'best_retained_parts':64,'new_results_parts':61})
if __name__=='__main__':main()
