"""Seal the fresh13-part search and independently derived sheet exclusion."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-thirteen-part-selection-and-sheet-exclusion-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={
 'source':'h5-free-bracket27-source-model-20261026',
 'conflicts':'h5-free-bracket27-domain-conflicts-20261026',
 'master':'h5-free-bracket27-domain-master-20261026',
 'failed_runner':'h5-free-bracket27-domain-master-search-20261026',
 'master_search':'h5-free-bracket27-domain-master-search-repaired-20261026',
 'failed_certificate':'h5-free-bracket27-triple-collision-20261026',
 'selected':'h5-free-bracket27-selected-model-20261026',
 'selected_search':'h5-free-bracket27-selected-search-20261026',
 'three_brackets':'h5-bracket27-three-bracket-probe-20261026',
 'cross_groups':'h5-bracket27-cross-family-probes-20261026',
 'coupled_groups':'h5-bracket27-coupled-group-probes-20261026',
 'separation':'h5-bracket27-sheet-separation-20261026',
 'conditional_master':'h5-bracket27-conditional-master-20261026',
 'conditional_master_search':'h5-bracket27-conditional-master-search-20261026',
 'conditional_selected':'h5-bracket27-conditional-selected-model-20261026',
 'conditional_selected_search':'h5-bracket27-conditional-selected-search-20261026',
 'early_review':'h5-bracket27-source-review-20261026',
 'review':'h5-bracket27-final-review-20261026',
 'sync':'h5-broader-source-main-sync-20261026'}
base={k:ROOT/'output'/v for k,v in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']==review['main_head']=='c22d3e39e315b040b3afc694acae3e1beca685f8'
    assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items());assert load(base['sync']/'receipt.json')['remote_main_verified']
    audits=[('source','audit/checks.json'),('conflicts','audit/checks.json'),('conflicts','groups/audit/checks.json'),('conflicts','copy-symmetry/checks.json'),('master','audit/checks.json'),('master_search','selection-audit/checks.json'),('selected','audit/checks.json'),('selected_search','search-audit/checks.json'),('three_brackets','model-audit/checks.json'),('three_brackets','response-audit/checks.json'),('cross_groups','model-audit/checks.json'),('cross_groups','response-audit/checks.json'),('coupled_groups','model-audit/checks.json'),('coupled_groups','response-audit/checks.json'),('separation','checks.json'),('conditional_master','audit/checks.json'),('conditional_master_search','selection-audit/checks.json'),('conditional_selected','audit/checks.json'),('conditional_selected_search','search-audit/checks.json')]
    assert len(audits)==19 and all(load(base[k]/n)['passed'] for k,n in audits)
    assert load(base['failed_runner']/'failure-audit.json')['solver_calls']==0 and load(base['failed_certificate']/'failure-record.json')['new_exclusions']==0
    calls=[]
    for key,audit_path in [('master_search','selection-audit/checks.json'),('selected_search','search-audit/checks.json'),('conditional_master_search','selection-audit/checks.json'),('conditional_selected_search','search-audit/checks.json')]:
        r=load(base[key]/audit_path);assert r['solver_calls']==1 and r['shared_budget_honored'];calls.append({'group':key,'calls':1,'status':r['terminal_status'],'solver_seconds':r['actual_solver_seconds'],'shared_seconds':r['actual_shared_seconds'],'soft_overrun_seconds':r['solver_soft_limit_overshoot_seconds']})
    for key in ['three_brackets','cross_groups','coupled_groups']:
        r=load(base[key]/'response-audit/checks.json');c=load(base[key]/'search/census.json');assert r['actual_shared_seconds']<=60;calls.append({'group':key,'calls':r['closed_calls'],'counts':c['counts'],'solver_seconds':r['sum_solver_seconds'],'shared_seconds':r['actual_shared_seconds'],'soft_limit_overruns':r['soft_limit_overruns'],'max_soft_overrun_seconds':r['max_soft_limit_overrun_seconds']})
    assert sum(r['calls'] for r in calls)==10 and [calls[i]['status'] for i in range(4)]==['OPTIMAL','INFEASIBLE','OPTIMAL','INFEASIBLE']
    OUT.mkdir()
    for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
    copies=[('source','result.json','full-source-model.json'),('conflicts','result.json','raw-conflict-census.json'),('conflicts','groups/result.json','conflict-groups.json'),('master','result.json','initial-master-model.json'),('master_search','selection-audit/verified-domain-selection.json','first-selection.json'),('failed_runner','failure-audit.json','precall-runner-failure.json'),('failed_certificate','failure-record.json','inapplicable-old-box-proof.json'),('separation','conditional-exclusion.json','first-sheet-exclusion.json'),('separation','second-sheet-witness.json','independent-second-sheet-witness.json'),('conditional_master','result.json','conditional-master-model.json'),('conditional_master_search','selection-audit/verified-domain-selection.json','second-selection.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-c22d3e39-snapshot.json'),('sync','receipt.json','main-push-receipt.json'),('sync','prior-ci.json','main-ci-679e97e0-complete.json')]
    for k,n,dest in copies:shutil.copyfile(base[k]/n,OUT/dest)
    write(OUT/'closed-calls.json',calls)
    first=load(OUT/'first-selection.json')['movable_parts'];second=load(OUT/'second-selection.json')['movable_parts'];changes=[{'part':a['part'],'item':a['item'],'before':[a['query'],a['domain_row']],'after':[b['query'],b['domain_row']]} for a,b in zip(first,second) if a!=b];assert changes==[{'part':3,'item':50,'before':[16,0],'after':[16,1]}];write(OUT/'selection-changes.json',changes)
    next_action=('All10 solver calls here are CLOSED. The unrestricted53-fixed/13-mover source model was prepared and audited but has never been solved. Both master-selected13-domain tuples are INFEASIBLE; this does not exclude the full source. The original tuple yields an independently audited first11-domain exclusion by sheet separation, because second-sheet originals64/65 have a simultaneous source witness. The conditional master changes only insert50 from query16 row0 to row1, but that new full coordinate tuple is also negative. Six subset calls give four positive source subsets and two UNKNOWNs; do not reopen either UNKNOWN or infer exclusions from it. The old54-fixed raw insert/two-cog box proof does not apply and was not transferred. Next use the current53-fixed geometry and full270671-variable parent to make a distinct conditional source subproblem: allow all three bracket originals27/28/29 every audited query/domain and retain only the ten verified original partial-domain memberships for insert50 and cogs53/54/56/57/58/61/62/64/65. In particular, the verified insert anchor belongs to current query16 row181, not either failed master row0/1. All26 coordinates must remain free; preserve every full original pair clause and the60 advisory hints. Independently audit the whole retained parent and10 appended selector constraints before one separately declared bounded call. This is a genuinely broader three-bracket choice test than the two closed exact13-tuples, not a retry or a claim that differently triangulated old/new sources nest. A positive requires all66 originals/90cutouts/10026hole vertices, material target and native validation, then production integration and the complete13-job/two-kerf H5 matrix. No new release is qualified. Mainc22d3e39 includes the two prior checkpoints; preserve live CI40270374068 before the next normal push. H2 original gate stays open;22reserved vectors untouched.')
    write(OUT/'next-step.json',{'action':next_action,'full_source_parent':base['source'].relative_to(ROOT).as_posix(),'partial_membership_source':'output/h5-free-bracket27-joint-prepared-20261026/audit/verified-partial-domain-membership.json','free_bracket_originals':[27,28,29],'retained_domain_originals':[50,53,54,56,57,58,61,62,64,65],'new_call_opened':False,'H5_complete':False})
    members={};inputs={}
    for folder in base.values():
        assert folder.is_dir()
        for p in folder.rglob('*'):
            if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
        for p in folder.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h,n
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-seven-part-obstruction-and-broader-source-20261026','h5-focused-partial-obstruction-20261026','h5-conditional-selection-and-partial64-20261026','h5-domain-selection-and-triple-certificate-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpers=list((ROOT/'output').glob('*bracket27*.py'))+[ROOT/'output'/n for n in ['push_h5_broader_source_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py']]+[Path(__file__)];seen=set()
    while helpers:
        p=helpers.pop()
        if p in seen:continue
        seen.add(p);assert p.is_file();members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
        for n in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",s):
            q=ROOT/'output'/n
            if q.is_file():helpers.append(q)
        for node in ast.walk(ast.parse(s)):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():helpers.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members);write(OUT/'checks.json',{'passed':True,'independent_audits_passed':19,'closed_solver_calls':10,'master_necessary_positives':2,'exact_selected_source_negatives':2,'subset_source_positives':4,'subset_unknowns':2,'all_shared_budgets_honored':True,'subset_soft_overrun_seconds':[.006047200062312186,.19000020006205887],'full_unrestricted_source_calls':0,'first_sheet_exclusion_independently_derived':True,'failed_pre_call_runner_and_inapplicable_certificate_preserved':True,'old_raw_certificate_not_transferred':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: thirteen-part selection and first-sheet exclusion — 2026-10-26

**The new 53-fixed source is fully modelled and audited. Two selected domain
tuples fail their exact coordinate checks. A separate decomposition confines
the first failure to its eleven first-sheet choices. The full source remains
unresolved; no complete target layout or H5 pass is claimed.**

## Fresh source and necessary selection

All 66 original identities remain mandatory: 53 fixed and 13 moving. The full
coordinate model has **270,671 variables / 351,276 constraints / 60 advisory
hints**, with 26 free coordinates and every original guarded pair face.
Independent reconstruction verifies all 954 pair modes and the one-sided
direction sharing. No unrestricted call on this full model has been opened.

The new raw-original conflict census checks all **8,836,883 domain pairs**
across 164 query combinations and certifies **3,938,040** whole-box conflicts.
Independent reconstruction uses all 82 original collision regions and 9,824
unmerged triangle-pair hulls. Lossless grouping retains **37,378,521 physical
conflict uses** in 7,206 groups, with 6,210 auxiliary flags and 1,641,171 literals.
The copy audit checks 6,019,570 transpose bits with no asymmetry. Ten family
orders apply to the necessary master only. The fresh second-sheet capacity of
two and both original area rules are retained.

The necessary master has **21,093 variables / 13,536 constraints / 40 hints**.
An initial runner fails before opening any solver call because a generated
assertion accidentally changes the expected group count from 7,206 to 13,206.
The zero-call failure and identical imported model are preserved. A separate
repaired runner returns a compatible domain selection in 4.646816 solver /
6.107018 shared seconds. This is not a layout.

An attempted reuse of the old insert/two-cog box argument fails its fresh
geometry check. The current insert domain has different bounds despite the
same query and row identifiers. Both failed checks and the new bounds are
retained; **no old certificate or exclusion transfers**.

## Exact checks and decomposition

The complete source parent plus 13 chosen-domain equalities is independently
audited and returns **INFEASIBLE in 15.129950 solver / 18.292381 shared seconds**.
Only those domain choices are excluded. Six distinct subset calls then retain
all original selected-domain planes and full pair-face disjunctions:

| Selected subset | Result |
|---|---|
| Three brackets | Feasible source witness |
| Three brackets plus insert | Feasible source witness |
| Three brackets plus two lower cogs | Feasible source witness |
| Insert plus seven first-sheet cogs | UNKNOWN at the eight-second limit |
| Three brackets, insert and two lower cogs | Feasible source witness |
| Three brackets plus seven first-sheet cogs | UNKNOWN at the eight-second limit |

Every positive is checked against all returned variables, active constraints
and original source planes. None is a full-job witness. The two soft overruns
are retained: **0.006047 and 0.190000 seconds**; all 60-second shared limits pass.
No subset negative or exclusion is inferred from either UNKNOWN.

The sheet-separation audit checks all **351,276 full-model constraints**:
80,269 belong to individual parts, 271,005 to physical pairs, and two area
rules depend only on the fixed sheet choices. There are 55 active first-sheet
pairs, one second-sheet pair and no cross-sheet interactions. The prior anchors
for originals64/65 directly satisfy their current selected domains, all six
inside planes and all 61 guarded pair faces. Any feasible first-sheet solution
could combine with that verified second-sheet witness and extend to the full
model's direction flags. The recorded full-model negative therefore excludes
**the eleven first-sheet domain choices alone**. This is a scoped solver-derived
finite-source exclusion, not a raw-geometry theorem or formal UNSAT certificate.

Append precisely that exclusion to the unchanged necessary master. Independent
parent restoration, all eleven selector mappings, all 2,048 Boolean cases and
actual solver import pass. Its call selects a new tuple in **4.679923 solver /
6.128471 shared seconds**, changing only insert50 from query16 row0 to row1.
The separately audited exact coordinate model for this tuple also returns
**INFEASIBLE, in 13.294581 solver / 16.361457 shared seconds**. Both calls are
closed. The broader 53-fixed source is not excluded by either result.

## Next step and repository state

Use the ten original partial-domain memberships as the next conditional source
construction, allowing **all three brackets every current source choice**.
The verified insert anchor belongs to query16 **row181**, not failed rows0/1.
Retain all 26 free coordinates, all full source clauses and the 60 advisory
hints. Audit the full parent plus ten selector equalities before one bounded
call. Any positive still needs all-original geometry, material and native
validation, production integration and the complete H5 matrix.

All ten calls here remain closed; the two UNKNOWNs are not retried. At
{review['utc']}, the previous two checkpoints are normally pushed to main
**c22d3e39** after all six checks on 679e97e0 pass. Its new
[CI40270374068](https://github.com/skulitom/Nestbolt/actions/runs/40270374068)
has three jobs passed and remains live. Preserve it before the next push.
Production, READMEs, upstream heads/releases and all 22 reserved H2 vectors
are unchanged. No new release is qualified. H2/H5 remain open at **60%**.

Evidence: [checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[sheet exclusion]({NAME}/first-sheet-exclusion.json),
[second-sheet witness]({NAME}/independent-second-sheet-witness.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}** aliases
are size/SHA-256/CRC verified across **{archive['archive_parts']}** archive parts.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 thirteen-part selection and first-sheet exclusion, 2026-10-26:** [the evidence]({link})
audits the full 53-fixed/13-mover source and all 8,836,883 fresh domain pairs,
including 3,938,040 raw-original conflicts. The necessary master selects a tuple,
but its exact coordinate model is INFEASIBLE. Six distinct subset calls yield
four checked partial witnesses and two UNKNOWNs; both soft overruns and all
failures are retained. A complete sheet-separation audit verifies independent
second-sheet coordinates and derives an eleven-domain first-sheet exclusion.
Adding that one scoped clause yields a new insert-domain selection, whose exact
coordinate model is also INFEASIBLE. All ten calls are closed; all shared limits
pass. No old raw box proof transfers and the unrestricted full source is untested.
Next allow all three brackets every current domain while retaining the ten
verified partial-domain memberships, including insert query16 row181. No new
call is opened yet. The previous two checkpoints are pushed as c22d3e39 after
all six prior main checks pass; its new CI40270374068 is live with three passed
at04:48UTC. H2/H5 stay open at60%; production, READMEs, releases and all22reserved
vectors remain unchanged. No complete target layout or new release is claimed.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
