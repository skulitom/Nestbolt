"""Seal fixed-core optima, reflected geometry and expanded frame-group coverage."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-wide-core-compound-limits-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-wide-core-compound-contacts-20261023';REF=ROOT/'output/h5-reflected-core-contacts-20261023';CAT=ROOT/'output/h5-reflected-small-compounds-20261023';COVER=ROOT/'output/h5-expanded-frame-group-coverage-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();records=[]
    for kind,base in [('rotated',BASE),('reflected',REF)]:
        gen=load(base/'result.json');graph=load(base/'audit/checks.json');red=load(base/'reduced/checks.json');hint=load(base/'hints/checks.json');model=load(base/'solve/model-audit.json');solved=load(base/'solve/result.json');layouts=load(base/'layout-audit/checks.json')
        assert all(x['passed'] for x in [graph,red,hint,model,layouts]) and not gen['pending_queries'] and gen['planned_queries']==gen['completed_queries']
        assert solved['status']=='OPTIMAL' and solved['objective']==solved['best_bound']==model['seed_score']==815800000 and model['full_score']==895800000
        assert hint['completed_cases']==80 and not hint['pending_cases'] and hint['original_seed_preserved'] and not layouts['full_target_witness']
        assert all(r['missing']=={'bracket':2} and sum(r['counts'].values())==64 for r in layouts['records'])
        records.append({'kind':kind,'generation':gen,'graph':graph,'reduction':red,'hints':hint,'model':model,'solver':solved,'layouts':layouts})
        for source,name in [('plan.json','plan.json'),('result.json','generation.json'),('audit/checks.json','graph-audit.json'),('reduced/checks.json','reduction-audit.json'),('hints/checks.json','hint-audit.json'),('solve/model-audit.json','model-audit.json'),('solve/result.json','solver-result.json'),('layout-audit/checks.json','layout-audit.json'),('layout-audit/layout-final.json','partial-layout.json'),('layout-audit/public-final.json','partial-public.json')]:shutil.copyfile(base/source,OUT/f'{kind}-{name}')
    original,reflected=records;cat=load(CAT/'checks.json');coverage=load(COVER/'checks.json')
    assert cat['passed'] and cat['completed_cases']==144 and cat['new_reflected_geometries']==114 and not cat['pending_cases']
    assert coverage['passed'] and coverage['whole_frame_groups']==29 and coverage['retained_small_candidates']==29631 and coverage['seed_group']==26 and coverage['seed_count']==64
    priorroot=ROOT/'benchmarks/results/h5-latest-wide-joint-progress-20261023';prior=load(priorroot/'source-review.json');assert source_digest()==prior['production_digest'] and prior['current_readmes']=={p:digest(ROOT/p) for p in prior['current_readmes']}
    previous_manifest={r['path']:r['sha256'] for r in load(priorroot/'raw-manifest.json')['files']};original_inputs=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original_inputs/name;assert digest(p)==previous_manifest['source-inputs/'+p.relative_to(ROOT).as_posix()]
    for name in ['job.json','conditional-target.json']:assert (original_inputs/name).read_bytes()==(ROOT/'output/h5-skeleton-contact-selection-20261020'/name).read_bytes()
    ci=json.loads(subprocess.check_output(['gh','run','view','39964600029','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']=='7cd00432e81324e1c2d8a006147ca5fa3ba5bbb5';write(OUT/'main-ci-7cd00432.json',ci)
    next_step=('Do not rerun or extend either completed fixed-core solve or resume their 126 and 64 capped member lists. Both finite models have a proven optimum at the preserved 64-part score, leaving two brackets missing; they do not prove unrestricted impossibility. Preserve output/h5-latest-wide-joint-20261023/layout-audit/layout-final.json as the best original partial and retain every alternate original layout. The next concrete model is output/h5-expanded-frame-group-coverage-20261023/mapping.json over the complete 35,488-pose source pool. It lets all three non-frame families move together while choosing exactly one of 29 whole 18-frame arrangements: all 26 earlier groups plus the exact wide, tall and mixed constructions at indices 26, 27 and 28. All 29,631 eligible choices, every group compatibility and the 64-part seed at group 26 are checked. Compared with the earlier 26-group model it has 24,329 additional choices; compared with the latest wide-only joint model it has 8,163 additions, while preserving all earlier choices. Declare fresh graph, reduction, compression, hint and single-solve limits. Rebuild the complete mutual graph from original geometry; do not reuse wide-only filtered adjacency or reductions. Any same-family substitution must preserve neighbor inclusion and every compatible frame group, and the mapped 64-part score floor. Preserve every residual edge and pending comparison, independently reconstruct all model fields, and validate every returned original layout. A complete 66-copy target witness must precede native-margin qualification and any production repair within the original limits/budget. Full H5 jobs and both kerfs remain required. H2 retains Artem\'s unchanged gate; the 22 reserved vectors stay unopened.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'best_partial_parts':64,'best_partial_missing':{'bracket':2},'fixed_core_finite_optima_below_full_inventory':True,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(CAT/'plan.json','reflection-plan.json'),(CAT/'checks.json','reflection-audit.json'),(COVER/'plan.json','coverage-plan.json'),(COVER/'checks.json','coverage-audit.json'),(COVER/'groups.json','frame-groups.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BASE,REF,CAT,COVER]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for name,h in load(root/'plan.json')['inputs'].items():
            if name in inputs:assert inputs[name]==h
            inputs[name]=h
    for base in [BASE,REF]:
        for mapping in [load(base/'reduced/plan.json')['inputs'],load(base/'hints/plan.json')['inputs'],load(base/'solve/model-audit.json')['input_hashes']]:
            for name,h in mapping.items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name.replace('\\','/')]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-latest-wide-joint-20261023',['layout-audit/layout-final.json','layout-audit/checks.json']),('h5-group-choice-20261023',['mapping.json','graph-audit/checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_wide_core_compound_contacts.py','prepare_h5_reflected_core_contacts.py','audit_h5_reflected_small_compounds.py','audit_h5_expanded_frame_group_coverage.py','ccd1.py']
    names += [prefix+'_h5_'+stem+'_'+suffix+'.py' for stem in ['wide_core_compound','reflected_core','tall_small_compound'] for prefix,suffix in [('build','contacts'),('audit','contacts'),('reduce','contacts'),('seed','contacts'),('solve','contacts'),('audit','layouts')]]
    pending=[ROOT/'output'/n for n in names];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    # Store a physical file once, retaining verified aliases for input references.
    canonical={};aliases=[];files=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            row={'path':name,'bytes':p.stat().st_size,'sha256':digest(p)};key=str(p.resolve()).casefold()
            if key in canonical:aliases.append({**row,'canonical':canonical[key]})
            else:canonical[key]=name;z.write(p,name);files.append(row)
    index={r['path']:r for r in files}
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(files)
        for r in files:assert len(z.read(r['path']))==r['bytes'] and sha256(z.read(r['path'])).hexdigest()==r['sha256']
        for r in aliases:
            assert r['path'] not in index and index[r['canonical']]['bytes']==r['bytes'] and index[r['canonical']]['sha256']==r['sha256'] and sha256(z.read(r['canonical'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':files,'aliases':aliases,'alias_format':'Each alias identifies the same physical input file stored once under canonical; byte length and SHA-256 are independently checked. No raw evidence is omitted.'})
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'original_inputs_match_previous_manifest':True,'both_geometry_graph_reduction_model_and_layout_audits_pass':True,'total_original_layouts_checked':sum(r['layouts']['layouts_checked_including_hint'] for r in records),'both_finite_optima_preserve_64_part_score':True,'new_reflected_geometries':114,'expanded_frame_groups':29,'expanded_small_choices':29631,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_members':len(files),'verified_input_aliases':len(aliases),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: compound limits around the improved core — 2026-10-23

**Both finite compound models retain the best 64-part score, missing two
brackets.** Neither improves the original 64-part layout. The candidate-model
optima are now known; unrestricted packing remains unresolved. H2/H5 remain
open at **60%**.

## Actual compound contacts and reflected geometry

The first model fixes only the checked 18 wide frames and 15 cogs from the new
64-part partial. It preserves the entire prior pool and its 31-part small seed,
then generates actual-outline contacts for all 36 saved compounds at four
quarter-turns plus single-part classes on both sheets. It does not substitute
a filled compound bounding rectangle for member outlines.

A separate reflection census checks 144 source-pattern/rotation cases. All 456
members match direct affine reflection under allowed transforms, including
rectangular inserts represented without a forbidden mirror flag. All 540 member
pairs pass. Maximum reconstruction error is 8.039×10⁻¹⁴ mm and maximum area
difference is 3.527×10⁻¹¹ mm². Family-preserving member matching identifies 24
cases equivalent to previous rotations and six equivalent to earlier reflections.
All equivalence certificates are rechecked, yielding **114 new compound
geometries**. The 1e-8 mm / 1e-6 mm² diagnostic deduplication tolerances are stated;
this is not an exhaustive continuous proof.

The second construction queries only those 114 reflected geometries on both
sheets. The previous single-part and unreflected queries are not repeated, and
no capped member list is resumed. Each model preserves the exact original
64-part baseline and original family caps.

| Checked result | Quarter-turn compounds | New reflected compounds |
| --- | ---: | ---: |
| Queries completed | 308/308 | 228/228 |
| Added brackets / inserts | 1,514 / 1,600 | 936 / 1,600 |
| Retained small choices | 6,594 | 9,130 |
| Complete conflict edges | 4,294,175 | 8,783,223 |
| Capped member lists preserved | 126 | 64 |
| Choices after certified substitution | 2,286 | 3,164 |
| Starting layouts checked | 80/80 | 80/80 |
| Single solve wall seconds | {original['solver']['seconds']:.9f} | {reflected['solver']['seconds']:.9f} |
| Proven finite optimum | 815,800,000 | 815,800,000 |
| Full inventory would require | 895,800,000 | 895,800,000 |

Both complete source prefixes, fixed and seed mappings, original stock bounds,
allowed transforms, member geometry, all query regions and every event are
independently checked. The first audit covers 12,746,553 same-sheet possibilities
and 4,859,252 exact distances; the second covers 23,960,484 possibilities and
9,945,558 exact distances. Every region reconstructs with zero area difference;
cache translation errors remain below 9.166×10⁻¹³ mm.

The first complete graph compresses without residuals. The second retains all
1,336,544 residual edges after its 20-second compression allowance. Both full
graphs are reconstructed independently. Fresh same-family substitutions verify
4,588,685 and 9,419,574 original neighbor relationships, preserve the entire
64-part score, and exactly preserve both induced graphs. No prior reduction is
reused; no original conflict is dropped.

Each model's every protobuf field is independently reconstructed. Each makes
exactly one eight-worker, seed-zero call with a 60-second allowance and finishes
early with `OPTIMAL`. Neither is repeated or extended. All six original layout
audits pass geometry and retain only the two missing-bracket violations: five
fresh frozen-CLI calls and one exact-layout reuse. Filled area remains
4,401,740.784070 mm² at charged material 4,988,890.203495 mm². The roughly
0.2001 mm minimum gap remains unqualified for native margins.

The saved generation timers cover query/proposal generation; complete graph
construction, serialization and independent audits are additional work. These
diagnostics are not production-budget or H5 quality results.

## Expanded frame-choice coverage

A new coverage audit preserves the full **35,488-entry** pool and the exact old
11,319-entry source prefix. It retains all 26 previous complete frame sets and
adds the exact wide, tall and mixed sets at indices 26–28. All **29 groups**
contain 18 original frames; their 141 distinct frame poses and all 32,989 small
poses receive stock/transform checks. Unused frame poses in the raw pool are
preserved, not included in this group-choice claim.

All 4,437 within-group frame pairs pass. Of 3,721,977 small/frame possibilities,
136,488 exact distances determine blockers. An independent comparison to each
whole group's polygon union checks 765,513 distances and all 956,681 membership
decisions. The resulting **29,631 compatible small choices** comprise 11,202
brackets, 13,272 inserts and 5,157 cogs. All 5,302 earlier group-model choices and
all 21,468 latest wide-model choices remain. The original 64-part seed maps to
group 26 and passes geometry and compatibility again. No new contact or solver
is run in this coverage audit; the complete mutual graph remains pending.

{next_step}

## Repository and evidence

Main is at pushed 7cd00432 with no incoming changes at this turn's fetch. Its
run 39964600029 is saved as `{ci['status']}` / `{ci['conclusion'] or 'pending'}`;
no unobserved pass is inferred. This checkpoint will follow the normal policy
of allowing the current checks to finish successfully before another push.
Original job, library, request and target hashes match the preceding archive.
Production source and all three READMEs remain unchanged. Current preview
wording stays accurate; neither a new application release nor gate completion
is claimed. No native packing, full quality matrix, registry publication or
reserved-input evaluation occurs.

Evidence: [rotation graph]({NAME}/rotated-graph-audit.json),
[rotation solve]({NAME}/rotated-solver-result.json), [rotation layouts]({NAME}/rotated-layout-audit.json),
[reflection census]({NAME}/reflection-audit.json), [reflected graph]({NAME}/reflected-graph-audit.json),
[reflected solve]({NAME}/reflected-solver-result.json), [reflected layouts]({NAME}/reflected-layout-audit.json),
[expanded coverage]({NAME}/coverage-audit.json), [frame sets]({NAME}/frame-groups.json),
[source review]({NAME}/source-review.json), [raw evidence]({NAME}/raw.zip),
and [manifest]({NAME}/raw-manifest.json). All {len(files)} archive members, CRCs,
byte hashes and {len(aliases)} input aliases verify. Identical physical input
files are stored once with explicit aliases; all raw evidence remains available.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 improved-core compound limits, 2026-10-23:** [the full audit](../benchmarks/results/{NAME}.md)
preserves the 64-part baseline through two newly bounded compound models. Both
reach a finite optimum with two brackets missing; no unrestricted impossibility
is claimed. All 536 queries, complete graphs, fresh reductions, model fields and
six original layouts are checked. The reflection census verifies 114 geometries
absent from previous queries; all 190 capped lists and 1,336,544 residual edges
remain preserved. A new 29-frame-group coverage audit checks every membership
and retains 29,631 compatible small poses plus the exact 64-part seed. Next build
its complete mutual graph and choose frames/cogs/brackets/inserts together under
fresh limits. Main's 7cd00432 checks remain separately recorded. Source, accurate
READMEs and releases remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(files),'verified_aliases':len(aliases),'archive_bytes':archive.stat().st_size,'best_parts':64,'expanded_groups':29,'expanded_choices':29631,'main_CI_status':ci['status']},flush=True)
if __name__=='__main__':main()
