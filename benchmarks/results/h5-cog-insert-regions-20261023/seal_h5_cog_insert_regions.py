"""Seal capacity checks, changed contacts, and the distinct next frame construction."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys,zipfile
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-cog-insert-regions-20261023';OUT=ROOT/'benchmarks/results'/NAME
BOUND=ROOT/'output/h5-group-choice-regions-20261023';CONTACT=ROOT/'output/h5-cog-insert-contacts-20261023';WIDE=ROOT/'output/h5-wide-frame-group-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();bounds=load(BOUND/'audit/checks.json');contacts=load(CONTACT/'audit/checks.json');generated=load(CONTACT/'result.json')
    model=load(CONTACT/'solve/model-audit.json');result=load(CONTACT/'solve/result.json');audit=load(CONTACT/'layout-audit/checks.json');wide=load(WIDE/'checks.json')
    assert all(r['passed'] for r in [bounds,contacts,model,audit,wide])
    assert [r['upper_bound'] for r in bounds['records']]==[18,22,35]
    assert generated['new_candidates']=={'cog':196,'insert':72} and generated['pending_queries']==generated['pending_proposal_lists']==0
    assert result['status']=='OPTIMAL' and result['seconds']<30 and result['objective']==result['best_bound']==model['seed_score']
    assert audit['all_returned_layouts_checked']==audit['fresh_frozen_CLI_calls']==2 and not audit['full_target_witness']
    assert all(r['missing']=={'cog':2,'insert':2} for r in audit['records'])
    previous=load(ROOT/'benchmarks/results/h5-group-choice-20261023/source-review.json')
    assert source_digest()==previous['production_digest']
    assert previous['current_readmes']=={p:digest(ROOT/p) for p in previous['current_readmes']}
    ci=json.loads(subprocess.check_output(['gh','run','view','39940832610','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']=='44ff9cc4ce02dcf354b2361a3ba24bb0c33e3214';write(OUT/'main-ci-44ff9cc4.json',ci)
    next_step=('Do not repeat the contact model with 30 fixed frames/brackets. Next complete the distinct all-wide frame construction: '
      'retain all original quantities and stock/material limits; treat the11 side-strip inserts as optional candidate positions. '
      'Generate and independently audit bracket, cog and insert candidates against the new18-frame group, including translated previously audited cog groups '
      'to populate open interior regions as well as boundary contacts. Check conditional capacity first, declare finite generation and solver limits, '
      'and preserve every failure. Do not reuse the old conditional conflict graph. Any full66-copy witness still needs native margins and unchanged full H5 gates.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
      'production_digest':source_digest(),'current_readmes':previous['current_readmes'],'README_change_needed':False,
      'new_release_qualified':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,
      'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(BOUND/'audit/checks.json','capacity-audit.json'),(CONTACT/'result.json','generation.json'),(CONTACT/'audit/checks.json','contacts-audit.json'),
                   (CONTACT/'solve/model-audit.json','model-audit.json'),(CONTACT/'solve/result.json','solver-result.json'),(CONTACT/'layout-audit/checks.json','layout-audit.json'),
                   (WIDE/'checks.json','wide-frame-audit.json'),(WIDE/'prior-frame-census.json','prior-frame-census.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BOUND,CONTACT,WIDE]:
        for name,h in load(root/'plan.json')['inputs'].items():
            p=ROOT/name;assert digest(p)==h;inputs[p.relative_to(ROOT).as_posix()]=h
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for name,h in model['input_hashes'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),
                         ('h5-group-choice-20261023',['layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json','mapping.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    picture=ROOT/'output/h5-group-choice-20261023/partial-layout.png';shutil.copyfile(picture,OUT/'seed-layout.png');members['seed-layout.png']=picture
    pending=[ROOT/'output'/n for n in ['bound_h5_group_choice_regions.py','audit_h5_group_choice_regions.py','build_h5_cog_insert_contacts.py',
      'audit_h5_cog_insert_contacts.py','solve_h5_cog_insert_contacts.py','audit_h5_cog_insert_layouts.py','build_h5_wide_frame_group.py','plot_h5_group_choice.py','ccd1.py']];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all_source_hashes_verified':True,'all_geometry_and_graph_audits_pass':True,'no_filled_area_improvement':True,
      'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,
      'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    ci_text=('All six checks on main44ff9cc4 now pass.' if ci['conclusion']=='success' else 'Five checks on main44ff9cc4 pass; the Windows native-check job remains live in the saved snapshot. No complete CI pass is inferred.')
    report=f'''# H5: continuous capacity and cog/insert contacts — 2026-10-23

**The changed contact model still places 62 of the original66 copies.** Its finite
candidate-set optimum retains13 cogs and19 inserts with all18 frames and12 brackets.
No full witness or filled-area improvement is found. A distinct wider-frame group
is now geometry-checked for the next construction. H2/H5 remain open at60%.

## Continuous-space diagnosis

The [previous62-part partial](h5-group-choice-20261023.md) has narrow gaps between
the large frame block, brackets and cogs. The side strip beside its frame block
is too narrow for the rectangular inserts. Frame holes remain reserved.

![The audited62-part seed, with frame holes reserved]({NAME}/seed-layout.png)

Three necessary all-angle cog-capacity relaxations complete within the declared
90-second allowance. Exact rational interior rectangles, outward stock domains,
inscribed/circumscribed cog disks, reachable area and diameter covers give:

| Held fixed | First-sheet bound | Last-sheet bound | Total upper bound |
| --- | ---: | ---: | ---: |
| 18 frames, 12 brackets, 19 inserts | 17 | 1 | 18 |
| 18 frames and 12 brackets | 19 | 3 | 22 |
| 18 frames | 28 | 7 | 35 |

All three bounds are **inconclusive** for the required15 cogs; they do not prove
that those counts are attainable or that omitted families can also fit. The
independent audit checks73 strictly interior rectangles, six center components,
twelve diameter covers and every exact complement/reachable-area computation.
All13 original cog placements remain in each relaxation. No solver is used here.

## New joint contacts and complete graph

The new model fixes the saved30 frame/bracket poses while allowing every cog and
insert to move. All compatible old poses remain:1,470 choices. Twelve free-region
queries cover four cog phases and two insert orientations on both sheets. Their
representative points, vertices and edge midpoints add196 cog and72 insert poses.
All268 proposals complete in5.358254800 seconds, with no cap, rejection or pending
query. New proposals include0.0126 mm positive construction padding; old poses
retain their original coordinates, and original acceptance tolerances stay unchanged.

All cog/cog, insert/insert and cog/insert conflicts are recomputed. The1,738-pose
graph has259,549 conflicts represented by1,999 verified cliques, with no residual
edges or compression limit. Independent checking covers140,728 old/fixed pairs,
5,780 proposal/fixed pairs and948,773 small-pair possibilities. Every actual
proposal and original transform/stock bound is checked; the complete13-cog,
19-insert seed remains feasible. Every protobuf model field is independently
reconstructed before solving.

One30-second maximum, eight-worker, seed-zero call finishes in4.219901600 seconds
and reports `OPTIMAL` for this finite pose set. Its filled-area objective equals
the starting seed; it does not prove continuous or unrestricted impossibility.
One callback and a different final layout both pass original geometry. Their two
fresh frozen-CLI checks fail only for two missing cogs and two missing inserts.
The callback uses four new poses and the final uses seven; neither increases
the4,342,015.346194 mm² filled area. Final charged material is4,988,890.203495 mm²,
within the unchanged allowance. Minimum clearance remains0.201 mm, so native
construction margins are not qualified. No native packing or quality run occurs.

## Distinct frame construction prepared

Inspection of all26 reviewed frame groups confirms that none has all18 frames in
the450-by-350 orientation. A new three-column/six-row arrangement uses exactly
those original frames,0.225 mm pair gaps and0.025 mm extra stock margin. It leaves
a136.525 mm side strip and885.85 mm above the frames. Eleven optional inserts,
rotated to110-by-180, fit in the side strip. All406 pairs in this29-part construction
pass independent original-vertex geometry, rotation and stock checks; minimum
distance is0.225 mm. The eleven insert poses are optional future candidates.

This is a checked subassembly, not an improvement over the62-part partial. Its
small-family completion and native qualification have not been run. The capacity
bounds and conditional graph above apply to the earlier frame group and must
not be reused as certificates for this different arrangement.

## Repository and next investigation

{ci_text} Core source and all three README hashes remain unchanged. The published
v0.2.0-alpha.1 preview is still accurately described; no additional release or
registry publication is made. H2 keeps Artem’s unchanged-denominator decision,
and no reserved input is opened. The existing release authorization remains.

{next_step}

Evidence: [capacity audit]({NAME}/capacity-audit.json), [contact audit]({NAME}/contacts-audit.json),
[model audit]({NAME}/model-audit.json), [solver result]({NAME}/solver-result.json),
[layout audit]({NAME}/layout-audit.json), [wide-frame audit]({NAME}/wide-frame-audit.json),
[source review]({NAME}/source-review.json), [raw inputs and all outcomes]({NAME}/raw.zip),
and [verified manifest]({NAME}/raw-manifest.json). All{len(manifest)} archive members,
CRCs and byte hashes verify.
'''
    # Normalize prose-only number joins; keep identifiers and links untouched.
    replacements={'original66':'original 66','retains13':'retains 13','and19':'and 19','all18':'all 18','and12':'and 12','at60':'at 60',
      'previous62':'previous 62','audited62':'audited 62','required15':'required 15','checks73':'checks 73','All13':'All 13','saved30':'saved 30',
      'remain:1,470':'remain: 1,470','add196':'add 196','and72':'and 72','All268':'All 268','in5.358':'in 5.358','include0.0126':'include 0.0126',
      'The1,738':'The 1,738','has259,549':'has 259,549','by1,999':'by 1,999','covers140,728':'covers 140,728','and948,773':'and 948,773',
      'complete13':'complete 13','One30':'One 30','in4.219':'in 4.219','the4,342':'the 4,342','is4,988':'is 4,988','remains0.201':'remains 0.201',
      'all26':'all 26','the450':'the 450','frames,0.225':'frames, 0.225','and0.025':'and 0.025','a136.525':'a 136.525','and885.85':'and 885.85',
      'to110':'to 110','All406':'All 406','this29':'this 29','is0.225':'is 0.225','the62':'the 62','main44ff':'main 44ff',
      'the11':'the 11','new18':'new 18','full66':'full 66',f'All{len(manifest)}':f'All {len(manifest)}'}
    for a,b in replacements.items():report=report.replace(a,b)
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 continuous capacity and cog/insert contacts, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
checks three continuous cog-capacity bounds (18, 22 and 35), all inconclusive.
Around the saved 30 frame/bracket poses, 12 queries add 196 cog and 72 insert
poses. All 259,549 conflicts, full clique coverage and the model pass independent
checks. One bounded solve reports a finite-pool optimum with the same 62 parts;
both returned layouts pass geometry and retain their two-cog/two-insert CLI
shortfalls. No filled-area improvement or unrestricted impossibility is claimed.
A distinct three-column/six-row group of all 18 wider frames and 11 optional
side-strip inserts passes 406 geometry pairs. Next complete its small families
with newly audited candidates and conflicts; do not retry the fixed-core model.
Core source, README and releases remain unchanged. H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'main_CI':ci['status'],'report':str(OUT.parent/(NAME+'.md'))})
if __name__=='__main__':main()
