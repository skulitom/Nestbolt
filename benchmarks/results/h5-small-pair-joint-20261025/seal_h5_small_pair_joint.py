"""Seal pair-contact evidence begun October23 and completed after the October25 merge."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-small-pair-joint-20261025';BASE=ROOT/'output/h5-small-pair-joint-20261023';REG=ROOT/'output/h5-small-pair-contacts-20261023';REC=ROOT/'output/h5-pair-reconciliation-20261025';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    data={k:load(root/name) for k,root,name in [('generation',REG,'result.json'),('geometry',REG,'audit/checks.json'),('geometry-provenance',REG,'audit/provenance.json'),('graph',BASE,'result.json'),('audit',BASE,'audit/checks.json'),('graph-provenance',BASE,'provenance.json'),('reduction',BASE,'reduced/checks.json'),('hints',BASE,'hints/checks.json'),('encoding',BASE,'solve/encoding-audit.json'),('model',BASE,'solve/model-audit.json'),('solver',BASE,'solve/result.json'),('layouts',BASE,'layout-audit/checks.json'),('retention',BASE,'selection-summary.json'),('reconciliation',REC,'checks.json')]}
    assert all(v['passed'] for k,v in data.items() if k not in ['generation','graph','solver'])
    gen,geo,g,a,r,m,s,l,t,rec=[data[k] for k in ['generation','geometry','graph','audit','reduction','model','solver','layouts','retention','reconciliation']]
    assert s['status']=='FEASIBLE' and s['objective']==816200000 and s['best_bound']==895800000 and not l['full_target_witness'];assert m['seed_score']==815800000 and m['hint_score']==816200000 and m['full_score']==895800000 and m['cp_model_presolve'] is False
    assert all(row['counts']=={'bracket':11,'insert':19,'frame':18,'cog':15} for row in l['records'])
    action='Assess a continuous geometric area relaxation for all seven fixed 33-part cores before another pose-enrichment search. Use all original permitted bracket and insert orientations/reflections, both unchanged stock domains and zero-clearance translation regions as an intentional relaxation of the positive-clearance requirement. Construct conservative outer covers of every possible occupied point, with explicit numerical padding and coverage checks, then compare combined and per-family area bounds with the full 12-bracket/21-insert inventory. Verify every known compatible pose and both 64-part and both 63-part seeds are contained before drawing any conditional conclusion. A bound above the required area is inconclusive; a finite candidate failure is not a geometric impossibility proof. Declare bounds and preserve partial work before execution. Do not repeat or extend the completed pair-contact solve, resume its 27 deferred insert lists or the older 1,950 member lists, weaken counts, or lower the native guard. All 66 original parts, original material target and production budget, native qualification and all 13 jobs at both kerfs remain required.'
    write(BASE/'next-step.json',{'full_target_witness':False,'action':action})
    prior=load(ROOT/'benchmarks/results/h5-shifted-core-small-joint-20261023/source-review.json');assert source_digest()==prior['production_digest']==rec['production_digest'];assert {p:digest(ROOT/p) for p in prior['current_readmes']}==prior['current_readmes'];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();main=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head==main==rec['head']
    ci=load(REC/'ci-40081381157.json');assert ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs']);current=json.loads(subprocess.check_output(['gh','run','view','40228140192','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert current['headSha']==head
    OUT.mkdir()
    for k,v in data.items():write(OUT/(k+'.json'),v)
    write(OUT/'main-ci-55835d7c.json',current)
    for path,name in [(REG/'plan.json','generation-plan.json'),(REG/'audit/plan.json','geometry-plan.json'),(BASE/'plan.json','plan.json'),(BASE/'reduced/plan.json','reduction-plan.json'),(BASE/'next-step.json','next-step.json'),(REC/'ci-40081381157.json','main-ci-4045822e.json'),(REC/'ci-40083254178.json','pages-4045822e.json')]:shutil.copyfile(path,OUT/name)
    for stem in ['layout','public']:shutil.copyfile(BASE/f'layout-audit/{stem}-final.json',OUT/f'final-{stem}.json')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':main,'generation_and_graph_date':'2026-10-23','reduction_and_selection_date':'2026-10-25','previous_checkpoint_pushed':rec['local_checkpoint_preserved'],'incoming_website_commit_preserved':rec['remote_merged'],'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'previous_highest_part_count_preserved':64,'current_returned_part_count':63,'current_missing':{'bracket':1,'insert':2},'filled_area_improvement_mm2':0,'full_target_witness':False,'native_margin_qualified':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'stop_rule_triggered':False,'next_investigation':action};write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,REG,REC]:
        for path in root.rglob('*'):
            if path.is_file():members[root.name+'/'+path.relative_to(root).as_posix()]=path
        for path in root.rglob('*.json'):
            if path.name not in ['plan.json','model-audit.json']:continue
            value=load(path)
            for name,hsh in value.get('inputs',value.get('input_hashes',{})).items():
                if name in inputs:assert inputs[name]==hsh
                inputs[name]=hsh
    for name,hsh in inputs.items():
        path=ROOT/name;assert digest(path)==hsh;members['source-inputs/'+path.relative_to(ROOT).as_posix()]=path
    for name in ['geometry-provenance','graph-provenance']:
        for row in data[name]['source_members_matching_committed_evidence']:
            for path,hsh in [(ROOT/row['source'],row['sha256']),(ROOT/row['manifest'],row['manifest_sha256'])]:assert digest(path)==hsh;members['source-inputs/'+path.relative_to(ROOT).as_posix()]=path
    for name,hsh in l['original_validation_input_hashes'].items():
        path=ROOT/name;assert digest(path)==hsh
        if path.suffix!='.exe':members['source-inputs/'+name]=path
    for name in ['mapping.json','layout-audit/layout-hint.json','layout-audit/public-hint.json','layout-audit/command-hint.json']:
        path=ROOT/'output/h5-expanded-frame-joint-20261023'/name;members['source-inputs/'+path.relative_to(ROOT).as_posix()]=path
    helpers=['build_h5_small_pair_contacts.py','audit_h5_small_pair_contacts.py','build_h5_small_pair_joint.py','audit_h5_small_pair_joint.py','prepare_h5_small_pair_selection.py','reduce_h5_small_pair_joint.py','seed_h5_small_pair_joint.py','solve_h5_small_pair_joint.py','audit_h5_small_pair_layouts.py','summarize_h5_small_pair_joint.py','reduce_h5_shifted_core_small_joint.py','seed_h5_shifted_core_small_joint.py','solve_h5_shifted_core_small_joint.py','audit_h5_shifted_core_small_layouts.py','check_h5_pair_reconciliation.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/n for n in helpers];seen=set()
    while pending:
        path=pending.pop()
        if path in seen:continue
        seen.add(path);members['helpers/'+path.name]=path
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            modules=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'all_inputs_and_committed_provenance_verified':True,'all_regions_queue_events_caps_and_memberships_checked':True,'every_graph_row_reconstructed':True,'all_four_baselines_preserved':True,'every_model_and_parameter_field_checked':True,'all_returned_original_layouts_checked':True,'remote_and_local_merge_contents_byte_exact':True,'production_digest_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(manifest['archives'],1));final=l['records'][-1]
    report=f'''# H5: contacts from coordinated small-part pair releases — 2026-10-25

**No improvement on the checked 63-part area result.** The new global search
returns 11 brackets, 19 inserts, all 18 frames and all 15 cogs. One bracket
and two inserts remain missing. Both earlier 64-part baselines are preserved.
The full bound remains unresolved; H2/H5 remain open at **60%** completed weight.
Generation and graph audits finished on October 23. After the interruption,
their saved results were verified and reduction/search completed on October 25.
No completed generation or search was restarted.

## Updated repository and stop rules

Main added the [Inkbolt key-rack example](https://github.com/skulitom/Nestbolt/commit/4045822eb1fce0bb9253d637ca56df8b22cc8b6e)
and related website links. All six checks and its Pages deployment pass.
Merge **55835d7c** preserves all nine incoming files and all 37 files from local
checkpoint **23cb3074** byte for byte. The merge and checkpoint were pushed
normally to main. The merge's own run 40228140192 is captured as
`{current['status']}` / `{current['conclusion'] or 'pending'}`.
The engine/benchmark source digest and all three READMEs remain unchanged.

The [published Studio description](https://sparrowstudio.app/) still explicitly
excludes fixed-sheet allocation and placing parts in holes. GitHub API evidence
confirms unchanged Sparrow head 1fe3e314, latest v0.3.0 and Studio head c0bb9e86.
The cached browser release page was stale; the saved current API response is
the release evidence. No stop rule fires. Preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain current; this diagnostic work does not qualify a new release.

## Fresh pair-conditioned contacts

Both distinct 63-part layouts from the previous search are retained exactly.
A complete census measures **582** same-sheet small-part pairs. The declared
25 mm adjacency rule selects **60** pairs. Each neighborhood temporarily
releases its pair and fixes the remaining 61 original placements. Ten permitted
orientation/reflection classes are queried on the released sheet. The other
sheet is unchanged from the previously checked empty full-layout insertion
regions. These pair restrictions generate geometry only: the later global
model can move every small part across any of the seven original fixed cores.

All **600 queries** finish in **{gen['query_seconds']:.6f} seconds** within
90 seconds; 438 regions are empty. Every one of 150 cached obstacle first uses
agrees with a direct global original-outline calculation. The verified explicit
128-sided offset provides 0.0126 mm construction padding against the remaining
parts and stock. It does not qualify the unchanged cores for the native guard.

The separate 90-second proposal phase finishes in {gen['proposal_seconds']:.6f}
seconds. It records 6,330 events: **3,435 new positions** (1,435 brackets and
2,000 inserts) and 2,895 exact duplicates. All bracket lists finish. The insert
cap leaves **27 deferred lists**, preserved with exact cursors. None is resumed.
Every new pose is blocked by at least one released part; no valid simple
append opportunity is found in either original 63-part layout.

Independent verification in **{geo['seconds']:.6f} seconds** matches 15 source
members to committed manifests; reconstructs the complete pair census, ordering,
all regions/proposals and the capped queue; and checks 306,525 original fixed-part
relationships plus 12,660 released-part relationships. All **24,045** new
position/core memberships agree between individual-part and complete core-union
distances. The audit checks 144,240 distinct core-part distances and 3,066 core
pairs, retaining all 14,046 old memberships only after exact mapping/hash checks.
Both 64-part and both 63-part baselines pass all 5,976 same-sheet pair checks.

## Global graph, reduction and one bounded search

The complete graph includes **17,481 choices**: 7,632 brackets and 9,849 inserts.
The unchanged old graph contributes 19,719,151 geometric conflicts. Fresh
construction adds **9,256,960** new-old/new-new conflicts, for **28,976,111**
total. No derived cog clique or compatibility-based conflict omission is used.
Construction takes {g['seconds']:.6f} seconds. Independent reconstruction takes
{a['seconds']:.6f} seconds, considers 34,797,215 same-sheet possibilities and
checks 11,260,927 exact distances. Every row matches and every old-old row remains
unchanged; all four baseline mappings stay valid.

Fresh same-family substitutions require adjacency, every conflict neighbor
and a superset of compatible cores. They finish in **{r['seconds']:.6f} seconds**
and 14,517,128 comparisons within 30 seconds / 50 million comparisons, retaining
**5,182** choices. Independent certificates enumerate 33,296,614 neighbor
relationships and 68,589 core memberships. The induced 4,497,418-edge graph
compresses completely into 10,073 cliques in **{r['compression_seconds']:.6f}
seconds**, within 20 seconds. Every edge reconstructs; there are no residuals.
All four baselines retain their original counts and area. No extra greedy search
is run. Retained choices include **426 new positions** (178 brackets and 248
inserts). Every core retains some compatible new positions. Of the 3,009 removed
new choices, 1,067 have certified old replacements and 1,942 have new replacements;
311 old choices have certified new replacements.

Every binary model and parameter field independently reconstructs. The model
has **{m['variables']:,} variables** (5,182 poses plus seven cores) and
**{m['constraints']:,} constraints**. The original area floor remains 815,800,000;
the 63-part hint scores 816,200,000 and full inventory requires 895,800,000.
Exactly one 18-frame/15-cog core and the original 12-bracket/21-insert caps apply.
The higher-area hint does not exclude the two 64-part baseline solutions.

One eight-worker, seed-zero, presolve-disabled call uses the declared 60-second
allowance. Actual wall time is **{s['seconds']:.6f} seconds**, preserving the soft
overrun. The hint appears at 0.164122 seconds and search starts at 0.22 seconds;
worker logs show 1,206,401 branches for the core worker. One callback and a
distinct final result retain score 816,200,000 in core 3. Status is `FEASIBLE`,
with full bound 895,800,000 unresolved. The call is not repeated or extended.

All **{l['layouts_checked_including_hint']}** returned/hint layouts pass original
transforms, stock, material and all 1,467 same-sheet pair checks apiece. Two
fresh frozen-CLI checks and one exact-layout reuse fail only the original
missing quantities. Filled area remains {final['filled_area_mm2']:.9f} mm² and
material {final['material_mm2']:.9f} mm². Minimum separation is
{final['minimum_distance_mm']:.12f} mm; native-margin qualification remains absent.
The final uses five new pair-contact positions. No production quality run,
native packing call or held-out evaluation occurs.

## Next geometry question

{action}

Evidence: [generation]({NAME}/generation.json), [original geometry]({NAME}/geometry.json),
[graph]({NAME}/graph.json), [independent graph audit]({NAME}/audit.json),
[reduction]({NAME}/reduction.json), [model]({NAME}/model.json),
[solver]({NAME}/solver.json), [original layouts]({NAME}/layouts.json),
[final layout]({NAME}/final-layout.json), [retained positions]({NAME}/retention.json),
[merge/stop-rule audit]({NAME}/reconciliation.json), [source review]({NAME}/source-review.json),
raw evidence {links}, and [manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']} canonical members and {archive['verified_aliases']}
aliases are byte-verified, with CRC and SHA-256 checks. Each ZIP part is
independently readable and below 50 MiB.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 pair-contact selection and repository refresh, 2026-10-25:** [the complete audit](../benchmarks/results/{NAME}.md)
checks 60 paired-release neighborhoods, 600 regions and 3,435 new small-part
positions. All memberships and the complete 28,976,111-conflict graph verify.
Certified reduction preserves both 64-part and both 63-part baselines. One
bounded search returns the same 63-part area result, missing one bracket and
two inserts; all three original layout checks fail only on quantities. The
full bound remains unresolved and all 27 deferred insert lists remain saved.
The next investigation is a continuous occupied-area relaxation for the seven
fixed cores, with conservative coverage checks before any negative conclusion.
Merge 55835d7c preserves the nine incoming Inkbolt example/website files and
all 37 local checkpoint files byte for byte, and is pushed to main. Main
4045822e passed all six checks and Pages; the refreshed upstream stop rule
does not fire. Engine source, READMEs and releases remain unchanged; H2/H5 stay open
at 60% completed milestone weight.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
