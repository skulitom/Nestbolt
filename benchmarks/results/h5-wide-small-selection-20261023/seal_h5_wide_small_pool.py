"""Preserve the wider-frame construction, complete audits, and measured limitations."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-wide-small-selection-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-wide-small-pool-20261023';CAT=ROOT/'output/h5-wide-catalogue-coverage-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();generated=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');red=load(BASE/'reduced/checks.json')
    model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json');layouts=load(BASE/'layout-audit/checks.json');coverage=load(CAT/'checks.json')
    assert all(r['passed'] for r in [audit,red,model,layouts,coverage])
    assert generated['retained_candidates']==10066 and audit['conflicts']==generated['conflicts']==5286767
    assert red['kept_candidates']==model['variables']==7776 and red['removed_candidates']==2290
    assert solved['status']=='FEASIBLE' and solved['incumbents']==7 and solved['counts']=={'frame':18,'bracket':12,'cog':11,'insert':21}
    assert layouts['layouts_checked_including_hint']==layouts['fresh_frozen_CLI_calls']==9 and not layouts['full_target_witness']
    assert coverage['new_cog_poses']==488 and coverage['placed_groups']==135
    # Independent arithmetic for the necessary area relaxation and prior-frame identity.
    job=load(ROOT/'output/h5-skeleton-contact-selection-20261020/job.json');st=job['stocks'][0];m=st['margins'];e=F(job['edge_clearance'])
    target=load(ROOT/'output/h5-skeleton-contact-selection-20261020/conditional-target.json');preflight=load(BASE/'preflight.json')
    def area(points):return abs(sum(F(x)*F(v)-F(u)*F(y) for (x,y),(u,v) in zip(points,points[1:]+points[:1])))/2
    required=sum(area(p['geometry'][0]['outer'])*p['quantity'] for p in job['parts'] if p['id']!='frame')
    free=(F(st['width'])-F(m['left'])-F(m['right'])-2*e)*(F(st['height'])+F(target['required_used_height_mm'])-2*(F(m['bottom'])+F(m['top'])+2*e))-18*F(157500)
    assert abs(float(free)-preflight['free_area_upper_bound_mm2'])<1e-7 and abs(float(required)-preflight['required_small_filled_area_mm2'])<1e-7
    frames=load(ROOT/'output/h5-cog-lattices-20261018/frames.json');assert preflight['prior_balanced_orientation_pattern']==[{'index':i,'rotations':r['rotations'],'counts':r['counts'],'method':r['method']} for i,r in enumerate(frames) if r['rotations']==[False]*3 and r['counts']==[6]*3]
    previous=load(ROOT/'benchmarks/results/h5-group-choice-20261023/source-review.json')
    assert source_digest()==previous['production_digest'] and previous['current_readmes']=={p:digest(ROOT/p) for p in previous['current_readmes']}
    earlier_ci=load(ROOT/'output/h5-wide-frame-hosted-checks-20261023.json');assert earlier_ci['conclusion']=='success' and len(earlier_ci['jobs'])==6 and all(j['conclusion']=='success' for j in earlier_ci['jobs'])
    write(OUT/'main-ci-44ff9cc4.json',earlier_ci)
    ci=json.loads(subprocess.check_output(['gh','run','view','39945225743','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']=='37edb1d2cf11afed380a5c355a1ba0396a65e6ae';write(OUT/'main-ci-37edb1d2.json',ci)
    releases=json.loads(subprocess.check_output(['gh','api','repos/skulitom/Nestbolt/releases'],cwd=ROOT));write(OUT/'releases.json',[{k:r[k] for k in ['tag_name','prerelease','published_at','html_url','target_commitish']} for r in releases])
    assert releases[0]['tag_name']=='v0.2.0-alpha.1' and releases[0]['prerelease']
    best=max(layouts['records'],key=lambda r:r['filled_area_mm2']);prior=max(load(ROOT/'output/h5-group-choice-20261023/layout-audit/checks.json')['records'],key=lambda r:r['filled_area_mm2'])
    assert best['filled_area_mm2']<prior['filled_area_mm2']
    next_step=('Do not retry the expired wider-frame model or resume its capped proposal lists. The catalogue coverage audit supplies 488 exact cog positions absent from that pool, from previously checked aligned/staggered and ragged groups. Build a changed individual-pose model using those positions and new bracket/insert contacts around the denser original cog outlines, keeping the full small-family counts free. Retain prior feasible hints after exact mapping; recompute and independently audit every changed conflict, and declare fresh finite generation/search bounds before work. The old fixed-component rectangle studies and this finite-pool timeout do not settle unrestricted feasibility. Only all 66 original parts within the original material target, passing frozen CLI and independent filled-outer checks, can advance to native-margin and production-budget qualification. Full original H5 requirements remain required; H2 stays open under the retained-denominator decision.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
      'production_digest':source_digest(),'current_readmes':previous['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
      'completion_percent':60,'H2_complete':False,'H5_complete':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(BASE/'plan.json','plan.json'),(BASE/'preflight.json','preflight.json'),(BASE/'result.json','generation.json'),(BASE/'audit/checks.json','graph-audit.json'),
      (BASE/'reduced/checks.json','reduction-audit.json'),(BASE/'solve/model-audit.json','model-audit.json'),(BASE/'solve/result.json','solver-result.json'),
      (BASE/'layout-audit/checks.json','layout-audit.json'),(CAT/'checks.json','catalogue-audit.json'),(BASE/'partial-layout.png','partial-layout.png')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BASE,CAT]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for plan in [BASE/'plan.json',BASE/'reduced/plan.json',CAT/'plan.json']:
        for name,h in load(plan)['inputs'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name,h in model['input_hashes'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),
      ('h5-group-choice-20261023',['layout-audit/checks.json','layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json','mapping.json']),
      ('h5-cog-lattices-20261018',['frames.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_wide_small_pool.py','audit_h5_wide_small_pool.py','reduce_h5_wide_small_pool.py','solve_h5_wide_small_pool.py','audit_h5_wide_small_layouts.py','audit_h5_wide_catalogue_coverage.py','plot_h5_wide_small_pool.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
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
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'all_original_geometry_graph_and_model_audits_pass':True,'area_preflight_independently_checked':True,
      'no_improvement_over_previous_best':True,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,
      'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    passing=sum(j['conclusion']=='success' for j in ci['jobs'])
    ci_text=(f'All six checks on main `37edb1d2` pass.' if ci['conclusion']=='success' else f'The saved snapshot of main `37edb1d2` has {passing} passing checks; the remaining jobs are still running. A complete pass is not inferred.')
    report=f'''# H5: small-part selection around wider frames — 2026-10-23

**The new arrangement places 62 of 66 parts and still misses four cogs.**
Its filled area is 4,281,489.908318 mm², below the prior best
4,342,015.346194 mm². The bounded search is not an optimum or an impossibility
proof. H2/H5 remain open at **60%**, with the original quantities and target.

## Geometry and candidate coverage

The [checked wider frame group](h5-cog-insert-regions-20261023.md) keeps 18 original
450 × 350 mm frames in three columns and six rows. Eleven side-strip insert
poses are optional. This orientation/count pattern appeared in the October 18
rectangle study; the present coordinates and individual-outline conflict model
are different. No claim of a first-ever orientation pattern is made.

An independently recomputed necessary area check leaves 2,071,991.303765 mm²
outside the frames, against 1,646,740.784070 mm² required for all small parts.
It is inconclusive: sufficient area alone does not establish a packing.

The pool retains 4,057 compatible old small-part poses. Twenty-eight free-region
queries and 2,851 translations/quarter turns of 108 saved compound patterns add
1,767 bracket, 2,242 cog and 2,000 insert positions. The total is 10,066 choices.
Generation takes 4.519206900 seconds. The insert cap leaves 834 recorded proposal
lists pending; a list stops when its next member reaches its family cap, including
any later members of other families. No suffix is resumed. All queries complete.

The independent audit verifies 135,198 old/fixed pairs, 119,808 proposal/fixed
pairs, every query and compound placement, 1,158 compound pairs and all pending
lists. Among 32,508,456 small-pair possibilities, 6,289,379 exact distances establish
5,286,767 conflicts. The 20-second compression limit leaves 523,186 edges explicit,
alongside 4,538 cliques. Every conflict remains covered; no edge is dropped.

## Safe reduction and bounded selection

Same-family substitutions remove a pose only for an adjacent retained alternative
whose other original conflicts are a subset. Independent enumeration checks
1,691,182 replacement-neighbor relations. The ten-million-comparison cap is reached
after 3.357768200 seconds; unprocessed poses remain. All 2,290 removals preserve
family counts and area, leaving 7,776 variables and 352,739 projected clique/edge
constraints with complete conflict coverage.

Exactly 40 declared greedy starting layouts are checked. The best has 18 frames,
12 brackets, 11 cogs and 17 inserts. Every protobuf model field is independently
reconstructed before one eight-worker, seed-zero, 60-second call. It returns
`FEASIBLE` after 60.278050300 seconds, with seven callbacks and a different final
layout. The upper bound still permits full inventory; optimality is not proved.

The best result has all 18 frames, 12 brackets and 21 inserts, but only 11 of 15
cogs. It improves this experiment's starting hint, not the previous best result.
The hint, seven callbacks and distinct final layout all pass independent original
stock, rotation, mirror, pair-distance and material checks. Nine fresh frozen-CLI
calls fail only for their recorded missing quantities. Final material is
4,988,890.203495 mm², within the unchanged 4,988,890.353495 mm² allowance. Minimum
final clearance is 0.2011 mm; native construction margins are not qualified.
No native packing, quality matrix or reserved-input evaluation occurs.

![Audited partial, missing four cogs; frame holes remain reserved]({NAME}/partial-layout.png)

## Changed geometry available for the next investigation

The earlier [aligned and staggered cog study](h5-aligned-pockets-and-rows-20261018.md)
contains denser components than the sampled-phase groups used in this pool.
A finite coverage audit takes its 15 nondominated groups and six selected ragged
groups, both whole-group quarter turns, and the corners/center of the three
saved free rectangles. It verifies 1,128 component pairs, 135 placed groups,
4,925 placed-member pairs and 18,090 fixed-frame pairs. Of 489 distinct cog poses,
488 are absent from the completed pool; ten placed groups contain all 15 cogs.
Minimum checked clearance is 0.2126 mm. These are valid subassemblies only:
coexistence with every bracket and insert remains unproved. Earlier rectangle
studies of these components remain preserved and are not rerun.

{next_step}

## Repository and release status

All six checks on main `44ff9cc4` now pass. The two prior evidence commits are
pushed normally to main as `37edb1d2`. {ci_text}
Core source and all three READMEs remain byte-identical to the preceding checkpoint.
The README accurately describes v0.2.0-alpha.1, the hosted preview from main, and
the two open gates. No new application build is qualified for release. The existing
release authorization remains; stable v0.1.0 and registry versions are unchanged.

Evidence: [generation]({NAME}/generation.json), [graph audit]({NAME}/graph-audit.json),
[reduction audit]({NAME}/reduction-audit.json), [model audit]({NAME}/model-audit.json),
[solver result]({NAME}/solver-result.json), [all layout checks]({NAME}/layout-audit.json),
[catalogue coverage]({NAME}/catalogue-audit.json), [source review]({NAME}/source-review.json),
[raw inputs and outcomes]({NAME}/raw.zip), and [manifest]({NAME}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 wider-frame small-part selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
checks 10,066 poses and all 5,286,767 conflicts. Certified same-family substitutions
retain 7,776 choices; every dropped alternative preserves counts and filled area.
The insert cap, 834 pending lists, compression cap and reduction cap are preserved.
One bounded 60-second solve places 62/66 parts, missing four cogs; its filled area
is below the prior best. All nine hint/returned layouts pass geometry and retain
their original CLI quantity failures. No optimum or full witness is claimed.
A finite audit of saved denser cog groups finds 488 absent poses and verifies
135 placed subassemblies. Next combine those coordinates with new small-part
contacts under fresh declared limits; do not repeat the expired model. All six
44ff9cc4 hosted checks pass and the prior checkpoint is pushed as 37edb1d2.
Core source, accurate READMEs and releases remain unchanged. H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'main_CI':ci['status'],'report':str(OUT.parent/(NAME+'.md'))})
if __name__=='__main__':main()
