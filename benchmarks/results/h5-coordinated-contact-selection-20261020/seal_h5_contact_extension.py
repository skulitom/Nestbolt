"""Seal retained coordinated selections and the newly audited contact extension."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,sys,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-coordinated-contact-selection-20261020'
OUT=ROOT/'benchmarks/results'/PREFIX
NAMES=['h5-coordinated-placement-selection-20261018',
       'h5-cog-skeleton-selection-20261018',
       'h5-insert-completion-selection-20261018',
       'h5-cog-skeleton-contacts-20261018',
       'h5-skeleton-contact-selection-20261020']
RUNS=[ROOT/'output'/n for n in NAMES]
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir()
    source=source_digest()
    assert source=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    previous=load(ROOT/'benchmarks/results/h5-aligned-pockets-and-rows-20261018/source-review.json')
    readmes={p:digest(ROOT/p) for p in previous['readmes_unchanged']}
    assert readmes==previous['readmes_unchanged']
    a,b,c,d,e=RUNS
    coordinated=load(a/'audit/checks.json'); full=load(a/'solve/result-audit.json')
    skeleton=load(b/'model-audit.json'); conditional=load(b/'result-audit.json')
    oldopt=load(c/'audit/checks.json'); contacts=load(e/'contacts-audit.json')
    graph=load(e/'graph-audit.json'); model=load(e/'model-audit.json'); newopt=load(e/'audit/checks.json')
    assert coordinated['complete'] and full['solver_status']=='UNKNOWN' and conditional['solver_status']=='UNKNOWN'
    assert all(not x['full_target_witness'] for x in [full,conditional,oldopt,newopt])
    assert newopt['incumbents'][-1]['missing']=={'insert':8}
    assert contacts['new_contacts']==2260 and graph['new_conflicts']==774312
    assert graph['complete_clique_coverage_exact'] and model['all_fields_independently_verified']
    assert load(c/'selected-indices.json')==load(e/'selected-indices.json')
    for run in [a,b,d,e]:
        plan=load(run/'plan.json')
        for field in ['sources','input_hashes','inputs']:
            for name,h in plan.get(field,{}).items():assert digest(ROOT/name)==h,name
    ci=json.loads(subprocess.check_output(['gh','run','view','39149585692','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']=='c9b01762f0163ac8167a8a02ac7e27ff1c7f2701'
    assert ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(OUT/'main-ci-c9b0176.json',ci)
    live=json.loads(subprocess.check_output(['gh','run','view','39394387011','--json','status,conclusion,headSha,url'],cwd=ROOT))
    assert live['headSha']=='c824e5a6060028eb4f71800faa2ed6190aff1abe'
    upstream={}
    for repo in ['sparrow','sparrow-studio']:
        commit=json.loads(subprocess.check_output(['gh','api',f'repos/JeroenGar/{repo}/commits/main'],cwd=ROOT))
        url=f"https://raw.githubusercontent.com/JeroenGar/{repo}/{commit['sha']}/README.md"
        with urllib.request.urlopen(url,timeout=30) as response: data=response.read()
        (OUT/f'upstream-{repo}-README.md').write_bytes(data)
        upstream[repo]={'commit':commit['sha'],'committed_at':commit['commit']['committer']['date'],
                        'url':url,'readme_sha256':sha256(data).hexdigest()}
    with urllib.request.urlopen('https://sparrowstudio.app/',timeout=30) as response:html=response.read()
    (OUT/'upstream-published.html').write_bytes(html)
    assert b'does not allocate parts across multiple fixed-size sheets' in html
    assert b'placing other parts inside holes is not supported' in html
    assert b'not published yet' in (OUT/'upstream-sparrow-studio-README.md').read_bytes()
    upstream.update(checked_utc=datetime.now(timezone.utc).isoformat(),published_url='https://sparrowstudio.app/',
        published_html_sha256=sha256(html).hexdigest(),fixed_sheets_shipped=False,part_in_part_shipped=False,stop_rule_triggered=False)
    write(OUT/'upstream-status.json',upstream)
    next_step=('The added exact contacts do not improve the known feasible partial. Do not repeat these four models or increase their time limits. '
        'Before another packing run, inspect the relaxation rather than add further arbitrary poses: derive necessary local stock-area capacities '
        'from original filled-outline intersections with a predeclared finite set of horizontal and vertical slabs. '
        'Conservative integer rounding must never exclude a physically valid selection. Independently reconstruct every coefficient, bound and '
        'whole-cog contribution before using any strengthened model, and retain the complete feasible 58-part hint. '
        'First test whether these necessary bounds sharpen the finite-pool insert upper bound; a bound of 21 still leaves all eight inserts unresolved. '
        'Any later full 66-part selection requires original CLI and filled-outer validation, native-margin qualification and unchanged H5 quality gates. '
        'No finite-pool failure proves the unrestricted geometry impossible. H2 is explicitly left open under Artem’s unchanged-denominator decision.')
    write(OUT/'source-review.json',{'production_digest':source,'readmes_unchanged':readmes,'runtime_changed':False,
        'native_packing_calls':0,'quality_runs':0,'full_target_witnesses':0,
        'new_pool_partial_identical_to_previous':True,'native_margin_qualified':False,
        'all_six_c9b0176_checks_pass':True,'pushed_checkpoint':live['headSha'],'current_main_CI_snapshot':live,
        'next_investigation':next_step,'H2_decision':'Keep the original gate and leave H2 open',
        'H2_complete':False,'H5_complete':False,'completion_percent':60})
    helpers=['build_h5_coordinated_selection.py','audit_h5_coordinated_pool.py','inspect_h5_coordinated_cog_sets.py',
        'prepare_h5_coordinated_cpsat.py','audit_h5_coordinated_cpsat_model.py','solve_h5_coordinated_cpsat.py','audit_h5_coordinated_selection_result.py',
        'prepare_h5_cog_skeleton_selection.py','audit_h5_cog_skeleton_selection.py','solve_h5_cog_skeleton_selection.py',
        'prepare_h5_skeleton_result_audit.py','audit_h5_skeleton_selection_result.py',
        'prepare_h5_insert_completion.py','audit_h5_insert_completion_model.py','solve_h5_insert_completion.py','audit_h5_insert_completion_result.py',
        'construct_h5_skeleton_contacts.py','prepare_h5_contact_extension.py','prepare_h5_contact_extension_model.py',
        'audit_h5_contact_extension_model.py','prepare_h5_contact_extension_runners.py','solve_h5_contact_extension.py',
        'audit_h5_contact_extension_result.py','construct_h5_pattern_layouts.py','diagnose_h5_concave_gaps.py','audit_h5_cog_lattices.py']
    members={}
    for run in RUNS:
        for p in sorted(run.rglob('*')):
            if p.is_file():members[run.name+'/'+p.relative_to(run).as_posix()]=p
    for name in helpers:members['helpers/'+name]=ROOT/'output'/name
    old=ROOT/'output/h5-contact-placement-selection-20261018'
    for name in ['candidates.json','conflicts.jsonl.gz','cliques.jsonl.gz','warm-indices.json','model.json','audit/checks.json','solve/selected-layout.json']:
        members['source-inputs/'+old.name+'/'+name]=old/name
    archive=OUT/'raw.zip'; manifest=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),
        'coordinated_pool':coordinated,'exact_inventory_result':full,'cog_model':skeleton,'cog_model_result':conditional,
        'initial_insert_optimization':oldopt,'new_contacts':contacts,'new_graph':graph,'new_model':model,
        'new_insert_optimization':newopt,'same_partial_selected':True,'archive_members':len(manifest),
        'production_digest':source,'H2_complete':False,'H5_complete':False,'completion_percent':60})
    shutil.copyfile(__file__,OUT/'seal_h5_contact_extension.py')
    report=f'''# H5: coordinated placements and cog-contact selection — 2026-10-20

**The expanded construction still returns 58 of the required 66 parts, missing
eight inserts.** Its selected positions are exactly the same as the previous
insert-completion attempt. No full target layout, native qualification or H5
completion is claimed. Completed milestone weight remains **60%**.

This checkpoint seals the unfinished October 18 selection evidence and the
October 20 contact-extension audit and search. All original shapes, quantities,
rotation permissions, margins, reserved frame holes and 0.2 mm clearance remain.
The last-sheet height target is 325.92690233 mm, corresponding to
4,988,890.353495 mm² of charged material. These are offline constructions.

## Coordinated pool and retained searches

The [previous checkpoint](h5-aligned-pockets-and-rows-20261018.md) supplies
24 retained partial layouts and 24 frame-only arrangements. Exact binary64
pose identity, without rounding, adds 261 candidates to the old 8,798-entry pool:
97 frames, 63 brackets, 66 inserts and 35 cogs. All 1,790 source events and the
entire original prefix are preserved. Independent enumeration of 1,901,998
added same-sheet pairs verifies all 132,531 new conflicts and their 2,277-clique
representation. Previously sealed hashes bind the unchanged original graph.

The four distinct complete fifteen-cog arrangements can also be treated as
selectable groups. Direct original-geometry checks cover 204,964 compatibility
pairs; all 4,522 eligible non-cog positions remain selectable. No frame is fixed.
Every variable domain, constraint and hint in both exact-inventory models is
independently consumed and checked.

| Finite construction | Variables | Constraints | Result | Seconds |
| --- | ---: | ---: | --- | ---: |
| All 9,059 poses, exact original inventory | 9,059 | 19,378 | UNKNOWN | {full['solver_seconds']:.9f} |
| Four cog arrangements, exact remaining inventory | 4,526 | 16,002 | UNKNOWN | {conditional['solver_seconds']:.9f} |
| Same cog arrangements, maximize inserts from 13 to 21 | 4,526 | 16,002 | FEASIBLE, 13 inserts | {oldopt['solver_seconds']:.9f} |
| New cog-contact positions, maximize inserts from 13 to 21 | 6,786 | 24,750 | FEASIBLE, 13 inserts | {newopt['solver_seconds']:.9f} |

Each run was declared before execution with seed 0, eight offline workers and
a 120-second solver limit. Measured soft overruns are retained above. UNKNOWN
means no complete selection was returned. The two optimization models allow
partial construction only; original-job acceptance still requires all 21 inserts.
Their complete feasible hints contain 58 original parts, including 13 inserts,
and neither search improves its hint. Both retain an insert upper bound of 21,
so neither proves a maximum of 13 or rules out a full arrangement. Portfolio
search activity remains in the full logs; zero counters in the winning-hint
response summary do not mean no search occurred.

## Contacts against all fifteen cogs

The saved generator computes free translation regions against each whole cog
arrangement, using original sheets and allowed quarter-turns/reflections.
It caches 32 zero-translation exclusion shapes and translates them by the
original cog positions. Across 112 queries, it retains 6,173 region points;
16 queries are empty. Empty conservative regions are not global impossibility
proofs. A declared round-robin selection cap gives **2,260 new exact poses**:
460 frames, 900 brackets and 900 inserts. The original 9,059 poses remain exact.

Independent original-vertex checks verify every retained contact's provenance,
stock bounds, allowed rotation and physical clearance. They cover 22,778 contact
versus cog pairs and 299,308 pairs for compatibility with all four arrangements.
There are **6,782 eligible non-cog positions**. Exhaustive enumeration of all
**10,571,998 added same-sheet pairs**, with 840,208 direct distances after an
independent bounding-box screen, reproduces exactly **774,312 new conflicts**.
The combined 21,788 cliques cover the complete graph, with no false conflicts.
The full 6,786-variable model, including all 24,750 constraints, objective and
complete zero/one hint, is independently checked before solving.

Both returned partials pass all 1,212 original filled-outer pair checks, but
the frozen CLI rejects each solely for `insert: expected 21, found 13`.
Charged material is 4,985,103.45 mm²; reporting that value does not make an
incomplete layout acceptable. Filled area is 4,323,340.784070 mm², still below
the earlier 63-part partial's 4,331,552.627256 mm². The old bracket arrangement's
minimum gap is about 0.2011 mm, which is not qualified for the native solver's
additional geometric margin. No production candidate is integrated.

## Decision and next work

Artem [keeps H2's original denominator and leaves H2 open](h2-gate-decision-20261020.md).
The original 95% requirement, negative fixtures and split remain unchanged;
the previously pending question is resolved. No reserved vector is opened.

{next_step}

[Checks]({PREFIX}/checks.json), [source review]({PREFIX}/source-review.json),
[raw attempts, failures, inputs and audit scripts]({PREFIX}/raw.zip), and
[verified archive manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and hashes verify.

All six checks on [main c9b0176]({PREFIX}/main-ci-c9b0176.json) pass.
The previous documentation checkpoint is pushed as c824e5a; its new CI state
is recorded separately. Product source, preview assets and the accurate English,
Japanese and Chinese READMEs stay unchanged.

The [upstream availability check]({PREFIX}/upstream-status.json) records
Sparrow Studio's published site as strip-only, without part-in-part; its repository
still describes the replacement app as unpublished. The plan's shipment stop
rule is not triggered. This is an availability check, not a performance comparison.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    h2note='''**H2 gate decision, 2026-10-20:** Artem [chose to keep the original 25-file
gate and leave H2 open](../benchmarks/results/h2-gate-decision-20261020.md).
The proposed positive-only denominator is not adopted. Two deliberate negatives
cap literal exact-import success at 92%, below the unchanged 95% requirement.
This is a classification bound, not a measured held-out result. The pending
question is resolved; frozen labels/split and once-only native outcomes remain,
and no remaining reserved vector is opened. Completion remains 60%.
'''
    note=f'''**N4 coordinated contact selection, 2026-10-20:** [the completed model audit](
../benchmarks/results/{PREFIX}.md) preserves three earlier bounded selections and
adds 2,260 exact cog-contact poses. Independent checks reproduce 774,312 new
conflicts over 10,571,998 added same-sheet pairs and verify all 24,750 model
constraints. The changed 120-second construction returns the identical 58-part
partial, missing eight inserts; its original CLI rejection and measured
121.154159-second elapsed time remain. The insert bound stays 21, so no full
layout or impossibility is proved. Next inspect necessary local area capacities
before another changed-model attempt; do not repeat these models or extend
their limits. All six c9b0176 checks pass and c824e5a is pushed to main.
No runtime, native-quality, release, README or gate change. H2/H5 remain at 60%.
'''
    # Keep a compact Markdown link on one line.
    note=note.replace('audit](\n../','audit](../')
    old=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes().startswith(old)
    append(ROOT/'BENCHMARKS.md','\n'+h2note.replace('../benchmarks/','benchmarks/')+'\n'+note.replace('../benchmarks/','benchmarks/'))
    append(ROOT/'docs/PLAN_V1_1.md','\n'+note)
    append(ROOT/'docs/V1_1_RESEARCH.md','\n'+h2note+'\n'+note)
    status=ROOT/'docs/STATUS.md'; text=status.read_text(encoding='utf-8')
    marker='**N4 aligned pockets and frame rows, 2026-10-18:**'
    assert text.count(marker)==1
    text=text.replace(marker,note+'\n'+marker)
    oldphrase='Two held-out negatives cap literal success at 92%; the held-out denominator clarification remains pending, with split unchanged'
    assert text.count(oldphrase)==1
    text=text.replace(oldphrase,'Two held-out negatives cap literal success at 92%; [Artem chose on October 20 to retain the original gate and leave H2 open](../benchmarks/results/h2-gate-decision-20261020.md), with split unchanged')
    status.write_text(text,encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
        'partial_improved':False,'completion_percent':60,'main_ci':live}),flush=True)
if __name__=='__main__':main()
