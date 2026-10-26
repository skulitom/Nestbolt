"""Seal exact single-cog completion exclusions without repeating proof work."""
from pathlib import Path
from datetime import datetime, timezone
import ast, json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-single-cog-obstruction-20261026'
REG=ROOT/'output/h5-focused-other-regions-20261026'
PAIR=ROOT/'output/h5-focused-bracket-cog-pairs-20261026'
OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    audits=[load(REG/f'release-{p}/audit/checks.json') for p in [4,7,8]]
    checks=load(PAIR/'audit/checks.json');result=load(REG/'result.json');pairs=load(PAIR/'summary.json')
    assert checks['passed'] and checks['ordered_pairs']==2362 and checks['all_single_cog_releases_conditionally_excluded_with_prior_proofs']
    assert all(a['passed'] and a['all4_queries_and1105_original_domains_replayed'] and a['pending_domains']==0 for a in audits)
    assert result['completed_cases']==3 and result['pending_cases']==result['pending_domains']==0
    previous=load(ROOT/'benchmarks/results/h5-fixed-six-completion-20261026/source-review.json')
    assert source_digest()==previous['production_digest'] and all(digest(ROOT/n)==h for n,h in previous['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head=='30fbefa90a70109c33dcecb5f4d2ec1a71d1351a' and mainhead=='822a5f67428e6dfdecab7bcea45e7c89cc31b159'
    ci=json.loads(subprocess.check_output(['gh','run','view','40248595273','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==mainhead
    OUT.mkdir();write(OUT/'main-ci-snapshot.json',ci)
    success=sum(j['conclusion']=='success' for j in ci['jobs'])
    for p in [4,7,8]:
        for n,short in [('result.json','result'),('summary.json','queries'),('audit/checks.json','audit'),('audit/conditional-region-summary.json','regions')]:shutil.copyfile(REG/f'release-{p}'/n,OUT/f'release-{p}-{short}.json')
    for n,short in [('result.json','pair-result.json'),('summary.json','pair-summary.json'),('audit/checks.json','pair-audit.json'),('audit/conditional-no-single-cog-completion.json','conditional-certificate.json')]:shutil.copyfile(PAIR/n,OUT/short)
    shutil.copyfile(REG/'result.json',OUT/'region-result.json')
    next_action=('All six single-cog-position releases are now conditionally excluded under the original source orientations/domains, the other five witness cog poses and fixed57. Do not construct or search the planned four-mover models for the proved-empty cases. Widen to at least two released cog positions (both brackets28/29,insert50 and both cogs remain mandatory: five movers,61 fixed originals), or change another fixed pose/source orientation/domain inventory. Never transfer these conditional exclusions into a model that moves their fixed witnesses. Prepare complete source regions with correct original pair direction and retain boundaries, then audit all full mutual clauses and exact area charges before a separately declared one-shot bounded search. Offline preparation is not production qualification. A full66-original native-valid material target, production integration and full13-job/two-kerf matrix are still required. Keep H2 open under its original gate, the22 reserved vectors untouched, and every completed solver closed. Wait for terminal main CI before the next normal main push, preserving remote changes. No new release is qualified.')
    write(OUT/'next-step.json',{'action':next_action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':previous['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','new_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,'current_main_ci_id':40248595273,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':next_action})
    members={};inputs={}
    for base in [REG,PAIR]:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    extra=['output/h5-fixed-six-completion-20261026/audit/provenance-repair.json','output/h5-fixed-six-completion-20261026/audit-provenance-repaired/conditional-no-bracket-completion.json','output/h5-single-cog-release-20261026/audit-recovered/checks.json','output/h5-single-cog-release-20261026/audit-recovered/release-comparison.json','output/h5-single-cog-release-20261026/audit-recovered/witness-source-provenance.json','output/h5-top-cog-bracket-capacity-20261026/audit/checks.json','output/h5-top-cog-bracket-capacity-20261026/audit/at-most-one-certificate.json']
    inputs.update(load(ROOT/extra[4])['inputs'])
    for n in extra:inputs[n]=digest(ROOT/n)
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for prior in ['h5-fixed-six-completion-20261026','h5-bounded-source-search-20261026','h5-guarded-cell-search-20261025']:
        p=ROOT/'benchmarks/results'/prior/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_focused_region_helpers.py','prove_h5_focused_other_regions.py','audit_h5_focused_other_regions.py','run_h5_focused_other_regions.py','prove_h5_single_cog_release.py','audit_h5_single_cog_release.py','prove_h5_focused_bracket_cog_pairs.py','audit_h5_focused_bracket_cog_pairs.py','pack_h5_evidence_archive.py','ccd1.py']
    pending=[ROOT/'output'/n for n in names];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'all3315_insert_cog_domain_cases_independently_replayed':True,'all2362_bracket_cog_pairs_independently_excluded':True,'lower_dimensional_boundaries_preserved':True,'correct_original_pair_direction_verified':True,'all_six_single_cog_releases_conditionally_excluded_with_prior_proofs':True,'no_redundant_focused_solver_run':True,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {item} | {r['bracket_fragments']} | {r['cog_fragments']} | {r['planned_pairs']} | {r['box_excluded']} | {r['continuously_excluded']} |" for item,r in zip([57,64,65],pairs))
    report=f'''# H5: all single-cog changes conditionally excluded — 2026-10-26

**Moving only one of the six witness cogs cannot complete all 66 original
parts within the recorded source angles/domains and fixed 57 poses.** This
extends the [prior fixed-six/capacity proofs](h5-fixed-six-completion-20261026.md)
to the three remaining releases. It does not prove unrestricted packing
impossible. H2/H5 remain open at **60%** completed milestone weight.

## Complete insert and released-cog regions

For each of original cogs 57, 64 and 65, retain the other five exact cog
positions and all 57 source placements. Both brackets, insert and released
cog remain mandatory. Examine all **1,105** original insert/cog inward domains
per release: 338 insert and 767 cog domains, across both sheets.

Exact rational clipping preserves every closed boundary, line and point.
Signed displacement follows the original ascending part order, including a
released cog after its fixed partner. All **3,315** cases finish in a shared
**{result['seconds']:.6f}s**, with no pending domains/cases or exhausted cap.
Independent source/provenance checks and separate convex-hull clipping replay
all cases in **{sum(a['seconds'] for a in audits):.6f}s**, rechecking 427 full
cog-witness clauses per case and
**{sum(a['exact_integer_corner_evaluations'] for a in audits):,}** integer corner
values. No new source angle, inset or simplification is introduced.

## Necessary bracket/cog coexistence

Pair every previously audited bracket fragment with every new released-cog
fragment. All pairs share a sheet. An outward integer difference box is
excluded only when every outside edge of one complete original collision
clause strictly fails throughout it. Remaining pairs use the exact rational
convex difference hull and every full source separation clause.

| Released original cog | Bracket fragments | Cog fragments | Complete pairs | Box exclusions | Exact hull exclusions |
|---|---:|---:|---:|---:|---:|
{table}

All **2,362** pairs are empty. Independent gift-wrapped hull reconstruction,
four-corner evaluation and separate clause-union clipping verify all results
in **{checks['seconds']:.6f}s**: **372,736** corner inequalities and **578**
changed-clause events, including every boundary. There are no unfinished or
possible pairs. Even one bracket cannot coexist with the released cog in
these cases, so the planned four-mover solvers would have no feasible target
and are not run. No solver, native validation or quality run occurs here.

With the earlier exclusions for cogs 54/62 and capacity-at-most-one proof for
cog 58, all six single-position releases are ruled out **only under their
recorded fixed-pose and source-domain conditions**. These certificates must
not constrain a model in which their fixed cogs move.

## Next work and repository state

Widen to at least two released cog positions, or another fixed source pose or
orientation/domain inventory. A two-cog case has five mandatory movers and
61 fixed originals; retain all original shapes, counts, area charges, native
clearance and material target. Offline preparation is not a production-budget
pass. A complete native-valid 66-original target, production integration and
the full 13-job/two-kerf H5 matrix remain required.

Current main is 822a5f67. [CI 40248595273]({ci['url']}) is
**{ci['status']}**, with **{success}/6** successful jobs at the saved snapshot.
Queue this checkpoint behind 30fbefa9 until that run is terminal before a
normal push, preserving remote changes. Product source, READMEs, preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged. H2 retains its original
gate; all 22 reserved vectors remain untouched. No new release is qualified.

Evidence: [region audits]({NAME}/release-4-audit.json),
[complete pair audit]({NAME}/pair-audit.json),
[conditional certificate]({NAME}/conditional-certificate.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
The archive retains **{archive['archive_members']:,}** canonical files and
**{archive['verified_aliases']:,}** exact-content aliases, verified by size,
SHA-256 and CRC.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 single-cog obstruction completed, 2026-10-26:** [the exact proof]({link})
examines all 3,315 insert/released-cog domain cases for original cogs 57, 64
and 65 and independently excludes all 2,362 bracket/cog fragment pairs.
All boundaries and original source pair directions are retained. Combined
with the prior proofs for 54, 58 and 62, no single-cog-position change can
complete this layout within the recorded source angles/domains and fixed
57 poses. The empty focused models are not sent to a solver. Next widen to
at least two cog positions (five mandatory movers, 61 fixed originals), or
another fixed pose/orientation/domain inventory; never apply these conditional
exclusions when their fixed poses move. This is not unrestricted impossibility
or H5 qualification. No solver/native/quality call occurs. Full original/native
material evidence, production integration and the full matrix remain required.
H2/H5 remain open at 60%; original gate limits, production, READMEs, releases
and all 22 reserved H2 vectors remain unchanged. Main CI 40248595273 is tracked
before the next normal push.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
