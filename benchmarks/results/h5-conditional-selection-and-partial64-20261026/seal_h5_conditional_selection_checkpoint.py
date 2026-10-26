"""Archive the conditional master, changed subsets, original64 partial and bracket scope."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-conditional-selection-and-partial64-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'master':'h5-conditional-domain-master-20261026','master_search':'h5-conditional-domain-master-search-20261026','selected':'h5-conditional-selected-model-20261026','selected_search':'h5-conditional-selected-search-20261026','changed':'h5-changed-insert-subsets-20261026','groups':'h5-selected-family-groups-20261026','partial64':'h5-insert-cog-partial64-20261026','free_bracket':'h5-free-bracket-source-model-20261026','free_bracket_search':'h5-free-bracket-source-search-20261026','review':'h5-conditional-selection-final-review-20261026','earlier_review':'h5-conditional-selection-source-review-20261026','sync':'h5-domain-selection-main-sync-20261026'}
base={k:ROOT/'output'/v for k,v in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']==review['main_head']=='b8535505cbe17167056041765648fd4770a8320b';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items());audits=[('master','certificate-audit/checks.json'),('master','audit/checks.json'),('master_search','selection-audit/checks.json'),('selected','audit/checks.json'),('selected_search','search-audit/checks.json'),('changed','model-audit/checks.json'),('changed','response-audit/checks.json'),('groups','model-audit/checks.json'),('groups','response-audit/checks.json'),('partial64','checks.json'),('free_bracket','audit/checks.json'),('free_bracket_search','search-audit/checks.json')];assert all(load(base[k]/n)['passed'] for k,n in audits);assert load(base['selected_search']/'search-audit/checks.json')['terminal_status']==load(base['free_bracket_search']/'search-audit/checks.json')['terminal_status']=='INFEASIBLE';assert load(base['partial64']/'checks.json')['original_parts_in_partial']==64;OUT.mkdir()
    for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
    copies=[('master','capacity-mapping.json','conditional-capacity-mapping.json'),('master_search','selection-audit/verified-domain-selection.json','new-domain-selection.json'),('changed','response-audit/unresolved-subsets.json','changed-unresolved-subsets.json'),('groups','response-audit/conditional-negative-subsets.json','family-group-negatives.json'),('groups','response-audit/verified-subset-witnesses.json','family-group-source-witness.json'),('partial64','partial64-placements.json','partial64-placements.json'),('partial64','verified-moving-anchors.json','partial64-moving-anchors.json'),('free_bracket','audit/free-brackets.json','released-bracket-options.json'),('free_bracket_search','shared-search/solve/result.json','free-bracket-search-result.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-b8535505-snapshot.json'),('sync','receipt.json','previous-main-push-receipt.json')]
    for k,n,dest in copies:shutil.copyfile(base[k]/n,OUT/dest)
    next_action=('All52 new calls are CLOSED; no restart, reseed or extension. The raw capacity has been audited and added to the necessary master. Its next selection changes only insert part2/item50 to query16 row15. The exact12-domain coordinate model is INFEASIBLE. The changed9pairs/36triples yield43 checked witnesses,2 UNKNOWN, no negatives. Larger groups show seven selected first-sheet cogs can fit with the insert; adding even one bracket in query0 row12 is INFEASIBLE. Independent actual-original reconstruction now verifies a64-part partial (54fixed+insert+ninecogs),84cutouts/9294vertices,1521pairs and256stockedges; brackets28/29 remain missing. A separate full66-required model releases both brackets to all16queries/2548domains each, keeps ten non-bracket domain equalities, and adds60 nonbinding partial64 hints. This larger conditional model is INFEASIBLE in25.180590solver/27.443101shared seconds. Thus these ten non-bracket domain choices cannot complete with any available bracket choice in the present source construction; this is not unrestricted packing impossibility. Next broaden source choices for the two bottom-strip cogs parts3/4 (originals53/54): retain only eight non-bracket domain equalities for parts2,5..11, preserve all original source constraints and both fully free brackets, keep the60 partial64 hints advisory. Both cogs regain all original source domains. Independently audit the complete retained parent, exactly eight restrictions, hint values and actual import before one separately declared bounded call. No copy-order constraints in this full-source model. An optional two-literal exclusion of both freed cogs simultaneously returning to query18 row3 would require an explicit exact conditional-model implication audit; do not infer a raw-geometry exclusion from the solver negative or silently add it. Keep all54fixed originals, all66mandatory, native guards, area/capacity rules and original material target. A positive still needs original66geometry/90cutouts/10026vertices/native validation and production/full13-job two-kerf H5 matrix. H2 original gate/22reserved vectors remain. Mainb8535505 CI40264589776 is live with4jobs passed at03:46UTC; preserve it before a normal push.')
    write(OUT/'next-step.json',{'action':next_action,'full_source_parent':'output/h5-projected-expanded-model-20261026','current_conditional_model':base['free_bracket'].relative_to(ROOT).as_posix(),'verified_partial64':base['partial64'].relative_to(ROOT).as_posix(),'proposed_free_parts':[0,1,3,4],'proposed_domain_restricted_parts':[2,5,6,7,8,9,10,11],'required_originals':66,'moving_originals':12,'fixed_originals':54,'H5_complete':False});members={};inputs={}
    for folder in base.values():
        for p in folder.rglob('*'):
            if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
        for p in folder.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h,n
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-domain-selection-and-triple-certificate-20261026','h5-projected-source-and-fresh-conflicts-20261026','h5-expanded-cog-neighborhood-20261026','h5-expanded-source-search-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpers=['prepare_h5_conditional_domain_master.py','audit_h5_conditional_master_certificate.py','audit_h5_conditional_domain_master.py','make_h5_conditional_master_runner.py','run_h5_conditional_domain_master.py','audit_h5_conditional_domain_selection.py','make_h5_conditional_selected_helpers.py','prepare_h5_conditional_selected_model.py','audit_h5_conditional_selected_model.py','run_h5_conditional_selected_search.py','audit_h5_conditional_selected_search.py','prepare_h5_changed_insert_subsets.py','audit_h5_changed_insert_subsets.py','make_h5_changed_insert_runner.py','run_h5_changed_insert_subsets.py','audit_h5_changed_insert_responses.py','make_h5_selected_family_group_helpers.py','prepare_h5_selected_family_groups.py','audit_h5_selected_family_groups.py','run_h5_selected_family_groups.py','audit_h5_selected_family_responses.py','audit_h5_insert_cog_partial64.py','prepare_h5_free_bracket_source_model.py','audit_h5_free_bracket_source_model.py','make_h5_free_bracket_runner.py','run_h5_free_bracket_source_search.py','audit_h5_free_bracket_source_search.py','review_h5_conditional_selection_checkpoint.py','review_h5_conditional_selection_final.py','push_h5_domain_selection_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/n for n in helpers]+[Path(__file__)];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p;text=p.read_text(encoding='utf-8')
        for name in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",text):
            q=ROOT/'output'/name
            if q.is_file():pending.append(q)
        for node in ast.walk(ast.parse(text)):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members);write(OUT/'checks.json',{'passed':True,'independent_audits_passed':12,'new_closed_calls':52,'conditional_master_rule_verified':True,'new_selection_changes_only_insert_domain':True,'exact_selected_tuple_infeasible':True,'changed_subset_positive_witnesses':43,'changed_subset_unknowns_preserved':2,'family_group_witnesses':1,'family_group_conditional_negatives':3,'partial64_original_geometry_passes':True,'missing_required_originals':[28,29],'both_brackets_full_source_options_exhausted_only_under_ten_domain_condition':True,'all_shared_budgets_honored':True,'two_small_soft_limit_overruns_preserved':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'production_and_readmes_unchanged':True,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: conditional selection, original64 partial and bracket scope — 2026-10-26

**Independent original-geometry checks now verify a 64-part partial at the target
stock bounds. Brackets 28/29 are still missing. Exhausting their source options
under the other ten selected domains shows that more cog domains must be opened.**
H2/H5 remain open at **60%**; no complete layout or native acceptance is claimed.

## Verified conditional rule and new selection

Replay the raw three-part certificate with exact rational arithmetic, then add
one copy-invariant inequality to the complete necessary master:
`sum(nine cog query18/row3 flags) + 8*(insert query16/row0 flag) <= 9`.
The audit checks all 20 Boolean/count cases, exact source-selector mappings,
whole retained parent and real solver import/export. The model now contains
**17,039 variables / 9,794 constraints / 36 advisory hints**.

Its single call finds a necessary domain assignment in **3.556931 solver /
4.832155 shared seconds**. Only the insert changes, from query16/row0 to row15.
This remains a necessary selection without coordinate feasibility. A separately
audited exact-coordinate model retains every full source clause, adds the twelve
selected domain equalities and clears advisory hints. Its sole call returns
**INFEASIBLE in 2.823710 solver / 5.077583 shared seconds**. The negative is scoped
only to that selected twelve-domain tuple.

## Changed subsets and larger coordinate groups

Only nine pairs and 36 triples include the changed insert. Reconstruct and audit
those **45 new models** from the original domain planes and every guarded source
pair clause. The other 37 pair / 84 triple calls remain closed. One bounded call
per changed subset yields **43 checked coordinate witnesses and two UNKNOWN**
in **8.331558 shared seconds**. Both small soft-limit overruns are preserved;
the maximum is **0.001259 seconds**. No UNKNOWN is used as an exclusion.

Four distinct larger coordinate groups then test the seven first-sheet cogs
with each relevant combination of insert and brackets. Complete reconstruction
and real import/export precede each single eight-second call, all within one
60-second shared envelope. Total elapsed time is **10.947849 seconds**:

| Added parts to the seven selected first-sheet cogs | Result |
|---|---|
| One bracket in query0/row12 | INFEASIBLE |
| Both brackets in query0/row12 | INFEASIBLE |
| Insert in query16/row15 | Checked source-coordinate witness |
| One bracket plus insert in those selected domains | INFEASIBLE |

These results concern those particular source domains. They do not establish
general incompatibility of these original parts. Every call is closed.

## Original-geometry validation of the partial

Combine the checked insert/seven-cog first-sheet witness with the earlier checked
two-cog second-sheet witness, then independently reconstruct every original job
outline and cutout. The resulting **64-original partial** contains all 54 fixed
originals at unchanged transforms, all 21 inserts and all 15 cogs, but only ten
of the twelve required brackets.

All **84 cutouts / 9,294 hole vertices** are preserved. All **1,521 same-sheet
pair checks** and **256 stock-edge checks** pass the unchanged original native
guards. Minimum pair distance is **0.2125000000000341 mm**, exceeding the required
**0.21170867250963943 mm**; maximum original/profile reconstruction discrepancy
is **5.08423e-13 mm**. Direct readback also checks 38 inside planes and 1,489 full
guarded moving-pair face clauses. No native validator is called on a partial.

## Both brackets released across all source options

Retain the full projected source parent, but restrict only the ten non-bracket
domains from the verified partial. Both mandatory brackets regain all **16 source
queries / 2,548 domains each**, including all declared rotations and mirrors.
All **24 original coordinates remain free**. Replace the old hints with **60
independently checked nonbinding partial hints**; no coordinate is fixed.

The complete retained-parent, restriction, hint and import audit passes:
**223,086 variables / 289,926 constraints**, all 66 originals mandatory and
all 538 full source pair modes preserved. Its single bounded call returns
**INFEASIBLE in 25.180590 solver / 27.443101 shared seconds**. Readback verifies
the exact model, response, parameters and timing. This rules out completion
under the ten non-bracket domain choices with the 54 fixed originals. It is not
an impossibility result for other domains, rotations or the unrestricted job.

Next reopen source domains for the two bottom-strip cogs, parts 3/4 (originals
53/54), alongside both brackets. Keep only the eight other non-bracket domain
restrictions and preserve the entire full-source parent. Audit before a distinct
bounded call. No solver-only negative is silently promoted to a raw geometry rule.
All **52 calls in this checkpoint are closed** and every shared budget passes.

A complete positive still needs all 66 originals, 90 cutouts and 10,026 hole
vertices, original material/stock/pair checks and native validation, followed by
production integration and the full 13-job/two-kerf H5 matrix.

## Repository and release state

The preceding checkpoint is on main **b8535505**. At 03:46 UTC,
[CI 40264589776](https://github.com/skulitom/Nestbolt/actions/runs/40264589776)
has four jobs passed and both platform checks still running; preserve this run
before a normal push. Upstream heads/releases show no stop-rule change. Product
source, READMEs, releases and all 22 reserved H2 vectors remain unchanged.
No release is newly qualified; H2 keeps the original gate.

Evidence: [partial64 audit]({NAME}/partial64-checks.json),
[free-bracket readback]({NAME}/free_bracket_search-search-audit-checks.json),
[checks]({NAME}/checks.json), [next step]({NAME}/next-step.json), and
[raw manifest]({NAME}/raw-manifest.json). **{archive['archive_members']:,}** canonical
files and **{archive['verified_aliases']:,}** exact aliases are size/SHA-256/CRC
verified in **{archive['archive_parts']}** independently readable archive part(s).
''';(ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 conditional selection and original64 partial, 2026-10-26:** [the evidence]({link})
adds and independently audits the raw three-part capacity in the necessary master.
Its new selection moves only the insert; exact coordinates remain INFEASIBLE for
that tuple. Only the 45 changed pair/triple subsets are called: 43 witnesses and
two UNKNOWN. Four larger groups isolate the bracket region and provide an
insert/seven-cog witness. Independent reconstruction verifies a64-original partial
with84cutouts/9294vertices,1521pair and256stock-edge checks; brackets28/29 remain
missing. A new full66-required model frees both brackets across16queries/2548domains
each while keeping ten non-bracket domains and60nonbinding partial hints. Its
single call is INFEASIBLE in27.443101shared seconds, scoped only to that condition.
Next reopen the two bottom-strip cog domains and audit the broader source model.
All52calls stay closed; all shared budgets pass and soft overruns remain recorded.
Mainb8535505 CI has four jobs passed at03:46UTC; preserve it before a normal push.
H2/H5 stay open at60%; production,READMEs,releases and22reserved vectors are unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
