from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import gzip,json,shutil,subprocess,sys,zipfile
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-area-capacity-relaxations-20261020'
OUT=ROOT/'benchmarks/results'/PREFIX
CAP=ROOT/'output/h5-area-capacities-20261020'
CASES=ROOT/'output/h5-area-cog-conditioned-20261020'
REC=ROOT/'output/v1-1-reconcile-20261020'
FAIL=ROOT/'output/h5-area-capacities-preparation-failure-20261020'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir()
    prep=load(CAP/'preparation.json');audit=load(CAP/'result-audit.json');reconcile=load(REC/'checks.json')
    source=source_digest();assert source=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    assert prep['positive_coefficients_exactly_audited']==75957 and prep['area_cuts']==58
    assert audit['exact_certificates_independently_reconstructed']==6
    assert not audit['area_cuts_tighten_insert_bound'] and not audit['conditioning_tightens_insert_bound']
    with gzip.open(CAP/'inequalities.jsonl.gz','rt',encoding='utf-8') as f:base_rows=[json.loads(line) for line in f]
    active=[]
    for row in audit['results']:
        marginals=np.load(ROOT/row['path']/'solution.npz')['inequality_marginals']
        ids=np.flatnonzero(marginals)
        assert len(ids)==1 and ids[0]<len(base_rows)
        constraint=base_rows[int(ids[0])]
        assert constraint['kind']=='maximum-inserts' and constraint['rhs']==21
        assert set(constraint['coeffs'])=={1} and marginals[ids[0]]==-1.
        active.append({'path':row['path'],'active_row':int(ids[0]),'kind':'maximum-inserts','rhs':21,'multiplier':-1})
    write(OUT/'active-dual-check.json',active)
    assert reconcile['all_50_changed_files_exactly_preserved']
    assert all(digest(ROOT/p)==h for p,h in reconcile['current_readmes'].items())
    for run in [CAP,CASES]:
        for p,h in load(run/'plan.json')['inputs'].items():assert digest(ROOT/p)==h
    for name,h in prep['prepared_hashes'].items():assert digest(CAP/name)==h
    live=json.loads(subprocess.check_output(['gh','run','view','39434650389','--json','status,conclusion,headSha,url'],cwd=ROOT))
    assert live['headSha']==reconcile['merge_commit']
    next_step=('The explicit 21-insert quantity cap remains the sole active dual inequality in every saved optimal bound. '
        'All four fixed-cog cases retain 21 inserts fractionally, so neither local area cuts nor disaggregating the cog choice '
        'provides a smaller finite-pool bound. Do not repeat these relaxations or the prior timed-out integer models unchanged. '
        'Next investigate a bounded LP-guided binary construction using the saved fractional solutions: choose actual whole '
        'placement variables, propagate their original conflict cliques and exact family quotas, and retain both accepted and '
        'failed branch decisions. Declare the finite node/time limits before any new branch solves. A fractional solution, '
        'branch failure or a restricted finite-pool result cannot count as a physical layout or unrestricted impossibility. '
        'Any full 66-copy selection must pass the frozen original CLI, independent filled-outer checks and native-margin '
        'qualification before a runtime proposal; full unchanged H5 material/cutting gates remain required. H2 stays open '
        'under Artem’s explicit original-denominator decision.')
    write(OUT/'source-review.json',{'production_digest':source,'current_readmes':reconcile['current_readmes'],
        'runtime_changed_by_this_work':False,'native_packing_calls':0,'quality_runs':0,
        'full_physical_layouts':0,'integer_searches':0,'next_investigation':next_step,
        'pushed_checkpoint':reconcile['merge_commit'],'current_main_CI_snapshot':live,
        'remote_landing_pages_and_readmes_preserved':True,'hosted_browser_is_main_preview':True,
        'H2_complete':False,'H5_complete':False,'completion_percent':60})
    for source_name,dest in [('checks.json','reconciliation.json'),
        ('c824e5a-checks.json','main-ci-c824e5a.json'),('36edfbd-checks.json','main-ci-36edfbd.json'),
        ('36edfbd-pages.json','pages-36edfbd.json')]:shutil.copyfile(REC/source_name,OUT/dest)
    members={}
    for run in [CAP,CASES,REC,FAIL]:
        for p in sorted(run.rglob('*')):
            if p.is_file():members[run.name+'/'+p.relative_to(run).as_posix()]=p
    for name in ['prepare_h5_area_capacities.py','solve_h5_area_relaxations.py','solve_h5_area_cog_cases.py',
        'audit_h5_area_relaxation_results.py','audit_v11_remote_reconciliation.py','audit_h5_cog_lattices.py']:
        members['helpers/'+name]=ROOT/'output'/name
    SRC=ROOT/'output/h5-skeleton-contact-selection-20261020'
    for name in ['job.json','candidates.json','cog-skeletons.json','conditional-target.json','mapping.json',
        'model.pbtxt','model-audit.json','projected-cliques.jsonl.gz','audit/checks.json']:
        members['source-inputs/'+SRC.name+'/'+name]=SRC/name
    archive=OUT/'raw.zip';manifest=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'preparation':prep,
        'translation_audit':load(CAP/'translation-audit.json'),'result_audit':audit,'reconciliation':reconcile,
        'archive_members':len(manifest),'archive_sha256':digest(archive),'completion_percent':60})
    shutil.copyfile(__file__,OUT/'seal_h5_area_relaxations.py')
    names=['Original relaxation','With area capacities','Fixed cog arrangement 0','Fixed cog arrangement 1','Fixed cog arrangement 2','Fixed cog arrangement 3']
    table='\n'.join(f"| {name} | {row['seconds']:.9f} | {row['fractional_variables']} | {row['exact_upper_bound']} |" for name,row in zip(names,audit['results']))
    report=f'''# H5: local area capacities and fixed cog relaxations — 2026-10-20

**All six continuous relaxations retain an exact upper bound of 21 inserts.
The proposed capacities do not tighten the bound or produce a physical layout.**
The original eight-insert gap remains unresolved, and H2/H5 remain open at 60%.

The [audited contact model](h5-coordinated-contact-selection-20261020.md) supplies
the unchanged 6,786 binary variables, four alternative complete cog arrangements,
original candidate poses, conflicts, family quantities and stock target.
No integer packing search is repeated. No new placement is generated.

## Necessary geometric constraints

For each original usable sheet, take its full rectangle and horizontal/vertical
partitions into two, four and eight equal bands: **58 regions** in total.
Every selected part contributes the area of its original filled outer outline
inside the region. Frames continue to reserve their holes. Each cog choice
contributes the sum over its fifteen original cog placements.

Coefficients round area downward to whole mm² after subtracting 0.000001 mm²;
capacities round upward after adding that amount. An independent rational
half-plane clip and shoelace calculation checks **all 75,957 positive
coefficients** against exact binary64-vertex geometry. Zero coefficients are
trivially conservative. Every capacity is checked above the exact rational
rectangle area. The maximum discrepancy from the floating geometry calculation
is **1.74623×10⁻¹⁰ mm²**. The complete 58-part hint remains feasible, with at least
**1,730 mm²** of integer slack in every new capacity. Preparation takes
**{prep['seconds']:.9f} seconds**.

The saved CP model is independently parsed in full into 24,748 linear
inequalities and three equalities. Splitting its two-sided insert limit explains
the extra linear row. Objective, domains and complete hint match exactly;
only integrality is relaxed. The strengthened version appends the 58 audited
necessary capacities.

## Bounded relaxation results

| Relaxation | Seconds | Fractional variables | Exact insert upper bound |
| --- | ---: | ---: | ---: |
{table}

Each relaxation declares a 120-second limit, eight offline solver threads and
seed zero before execution. All finish optimally within that limit.
SciPy's warning that the thread and seed options are forwarded to HiGHS is
preserved in each result. These are construction diagnostics, not native quality
measurements.

The area-augmented relaxation initially mixes three mutually exclusive cog
arrangements. Four further declared cases fix one arrangement at a time; each
retains 342–386 fractional variables and 21 inserts. Each saved primal vector
passes all original linear constraints and applicable area/fixing rows within
the recorded numerical residuals. None is interpreted or exported as a layout.

All six upper bounds are independently reconstructed using exact rational
arithmetic. For a minimization objective with inequalities, equalities and unit
variable bounds, the audit evaluates the dual row totals plus the minimum
reduced cost over each unit interval. It does not trust the rounded solver
objective. **The only nonzero inequality multiplier in every bound is the
explicit 21-insert cap.** The new capacities do not close the gap between the
fractional and whole-placement problems. These results neither prove a full
physical arrangement exists nor prove the original geometry impossible.

The first preparation script has an unmatched bracket and fails before any
preparation or solve starts. Its original source and failure are retained.
The corrected preparation uses the same declared geometric method; no successful
measurement is repeated to replace a failed search.

{next_step}

## Repository and hosted browser reconciliation

Remote main advanced to **36edfbd** while local work was paused. Its 29 changed
landing-page, example, metadata and README files are disjoint from the 21 local
evidence files. The first ordinary push was rejected non-fast-forward; no remote
content changed. Merge **8a81205** preserves every changed file exactly from its
own parent, keeps both histories and verifies the benchmark log's original prefix.
The [merge audit]({PREFIX}/reconciliation.json) confirms the core-source digest
is unchanged. That merged checkpoint is now pushed to main.

All six checks on [c824e5a]({PREFIX}/main-ci-c824e5a.json), all six checks on
[36edfbd]({PREFIX}/main-ci-36edfbd.json), and its
[Pages deployment]({PREFIX}/pages-36edfbd.json) pass. The merged checkpoint's
separate CI state is retained in source review without assuming completion.
The current English, Japanese and Chinese READMEs correctly describe a hosted
preview from main. Earlier records describing hosted v0.1.0 refer to their
historical deployment. No release tag, asset or frozen benchmark claim changes.
Artem's decision to retain H2's original gate remains in force.

[Checks]({PREFIX}/checks.json), [source review]({PREFIX}/source-review.json),
[all raw coefficients, fractional solutions, certificates, scripts and failures]({PREFIX}/raw.zip),
and [verified archive manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify. No held-out
evaluation, native packing, quality run, production change or milestone credit.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 local-area bounds, 2026-10-20:** [58 necessary stock capacities](../benchmarks/results/{PREFIX}.md)
pass exact rational checks on 75,957 positive coefficients, preserving the
complete 58-part hint. All six continuous relaxations finish within their declared
limits; the four cases fixing each cog arrangement remain fractional. Exact
independent dual reconstruction keeps the insert bound at 21 in every case,
with only the original quantity cap active. No full layout or impossibility
is established and no integer search is repeated. The original preparation
syntax failure is retained. Next investigate a bounded whole-placement
construction guided by these fractions, retaining every branch and the original
acceptance rules. Remote landing pages and READMEs are reconciled exactly and
pushed as 8a81205; the hosted main preview is verified. H2/H5 remain open at 60%.
'''
    browser=f'''**Hosted preview and repository reconciliation, 2026-10-20:** [the merge audit](../benchmarks/results/{PREFIX}.md)
preserves all 29 remote landing-page/README changes and 21 local evidence files.
All checks and the Pages deployment for remote main 36edfbd pass; the current
READMEs identify the hosted browser as a preview from main. Historical statements
about hosted v0.1.0 remain tied to their earlier deployment. The merge is pushed
as 8a81205, with its separate CI still requiring its own result. Core source and
release assets are unchanged; H2/H5 remain open.

'''
    previous=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==previous
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
    marker='**Hosted browser confirmation, 2026-10-18:**';assert s.count(marker)==1;s=s.replace(marker,browser+marker)
    marker='**N4 coordinated contact selection, 2026-10-20:**';assert s.count(marker)==1
    p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
        'exact_insert_bounds':[21]*6,'completion_percent':60,'pushed_checkpoint':reconcile['merge_commit'],'new_CI_state':live['status']}),flush=True)
if __name__=='__main__':main()
