"""Preserve a full necessary assignment and an all-angle fixed-position obstruction."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-retained64-proxy-witness-and-disk-proof-20261026';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-retained64-proxy-regions-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-coupled-allocation-model-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('086f0123') and main==previous['remote_main'] and command(['git','rev-parse','HEAD~3'])==main
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40393931732','--json','databaseId,status,conclusion,headSha,jobs,url']))
assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success'
assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
audits={'regions':BASE/'audit-order-insensitive/checks.json','model-assignment':BASE/'completion-model-audit/checks.json',
    'original-source':BASE/'completion-source-audit/checks.json','disk-exclusion':BASE/'disk-exclusion/audit/checks.json'}
assert all(load(p)['passed'] for p in audits.values())
assignment=load(audits['model-assignment']);source=load(audits['original-source']);proof=load(audits['disk-exclusion'])
assert assignment['all_serialized_constraints_satisfied']==5016 and assignment['closed_unknown_model_proved_feasible_by_construction']
assert not source['full_source_valid'] and source['full_source_pair_failures']==14 and source['full_physical_intersection_pairs']==8
assert proof['complete_integer_anchor_cells_verified']==26 and proof['fixed_position_obstruction_verified']
OUT.mkdir()
for n,p in audits.items():shutil.copyfile(p,OUT/(n+'-checks.json'))
for p,n in [(BASE/'prepared.json','prepared-regions.json'),(BASE/'construction/result.json','construction-result.json'),
    (BASE/'construction/chosen-pair.json','chosen-pair.json'),(BASE/'construction/copy-bijection.json','copy-bijection.json'),
    (BASE/'completion-model-audit/assignment.json','all609-variable-assignment.json'),
    (BASE/'disk-exclusion/certificate.json','disk-certificate.json'),(BASE/'audit/failure.json','preserved-reader-failure.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-ff5036af-success.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,
    'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,
    'main_ci':40393931732,'main_ci_status':'completed','main_ci_successful_jobs':6,'push_qualified_now':True,
    'unpublished_prior_checkpoints':3,'completion_percent':60,'H2_complete':False,'H5_complete':False,
    'reserved_H2_vectors_evaluated':0,'solver_calls':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all66_originals_retained':True,'existing64_source_transforms_unchanged':True,
    'necessary_coupled_model_feasibility_proved':True,'actual_source_valid':False,'new_physical_collision_pairs':8,
    'fixed64_position_obstruction_proved':True,'arbitrary_cog_angles_allowed_in_obstruction':True,
    'existing_non_cog_pose_or_cog_center_must_change':True,'unrestricted_exclusion':False,
    'solver_calls':0,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The closed609-variable coupled model now has an independently checked direct assignment satisfying all5016 constraints, so its UNKNOWN was not infeasibility. The assignment is physically invalid:8 new bracket/cog intersections plus6 retained64 gap failures and3 retained stock-guard failures. More strongly, exact source-contained109113um disks cover all26 complete coarse-free bracket anchor cells with the64 existing non-cog poses and cog centers fixed. Arbitrary cog rotations cannot repair this configuration; at least one existing non-cog pose or cog center must change. Do not continue fixed64 bracket insertion or phase-only repair, and do not rerun the unchanged closed coupled model. A materially different next model can add mixed-family source-contained cog/rectangle separation constraints for the demonstrated collisions while retaining every sheet/mode option and allowing all existing positions to move. An exact integer regular octagon inside the all-angle cog disk could provide a compact convex forbidden-region representation; prove its source containment and whether it excludes the recorded invalid cells before using conditional separation disjunctions for every relevant bracket variant and both sheet choices. Preserve the concrete assignment as evidence, not a full-source success or permission for native validation. H2 unchanged and22 reserved vectors unopened. All6 main ff5036af checks now pass; after committing this report, the four queued checkpoints may be pushed normally. No release qualifies.',
    'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for p in BASE.rglob('*'):
    if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
for p in BASE.rglob('plan.json'):
    for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
model_root=ROOT/'output/h5-allocation-model-20261026'
for p in [model_root/'model.pb',model_root/'mapping.json',model_root/'model-audit/checks.json']:
    inputs[p.relative_to(ROOT).as_posix()]=digest(p)
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=[ROOT/'output'/n for n in ['h5_fixed_proxy_regions.py','prepare_h5_retained64_proxy_regions.py',
    'audit_h5_retained64_proxy_regions.py','audit_h5_retained64_proxy_regions_ordered.py',
    'construct_h5_retained64_proxy_completion.py','audit_h5_retained64_completion_source.py',
    'audit_h5_constructed_allocation_assignment.py','prove_h5_retained64_disk_exclusion.py',
    'audit_h5_retained64_disk_exclusion.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':4,'preserved_failed_auxiliary_reader':1,
    'all609_variables_assigned':True,'all5016_constraints_satisfied':True,'actual_full_source_valid':False,
    'new_physical_intersections':8,'all26_fixed_position_anchor_cells_excluded_for_all_cog_angles':True,
    'minimum_strict_squared_disk_margin_um2':3428577728,'unrestricted_exclusion':False,
    'solver_calls':0,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: a complete proxy assignment and an all-angle fixed-position obstruction — 2026-10-26

**The closed coupled necessary model is feasible, but the preserved 64-part
configuration cannot accept another bracket while its existing positions stay
fixed, even if every cog may rotate freely.** The evidence proves both statements
without a solver call. Neither statement completes H5 or excludes the unrestricted
job. H2/H5 remain open at 60% by completed gate weights.

## Complete anchor regions around the retained layout

The construction keeps the 55 first-sheet transforms from the earlier 64-source
layout and the independently repaired short nine. Both missing bracket copies
10 and 11 remain mandatory. Their short-sheet choices are ruled out by the
existing full count frontier: neither can join four brackets, two inserts and
three cogs. They must both use the first sheet while these 64 placements stay.

Mapping the retained parts to the all-angle proxies passes all stock domains,
2,347 coarse-rectangle pairs and eight source/cog-only capacity profiles. Exact
integer overlap inequalities and an X sweep find the entire coarse-free anchor
lattice for all eight bracket modes: **5, 0, 7, 0, 7, 0, 7, 0 cells**. The four
turned modes have no free cell. Single-bracket capacity checks retain these
26 cells.

An independent reader verifies unchanged source transforms, 909 baseline
capacity slabs, the entire integer lattice regions through axis-aligned geometry
union/difference, and 21,344 critical anchor intervals for the single-bracket
capacity tests. One initial auxiliary reader incorrectly compared forbidden-box
lists in source enumeration order. Its failure is preserved. The repaired reader
compares the exact box multiset, including duplicates; geometry is unchanged.

## Direct feasibility of all 5,016 necessary constraints

A deterministic finite construction uses the center and four corners of each
cell, producing 130 poses. Its first successful pair is reached after 15 tests:
12 prior pairs fail mutual coarse geometry and two fail combined capacity.
Both missing brackets are added; all 64 existing source transforms remain.

Equivalent copies are separately relabelled by sheet/Y/X to satisfy the coupled
model's copy ordering. Original-copy-labelled placements and the complete
66-entry within-family bijection are preserved. Every original source identity
still occurs exactly once, and relabelling changes no transform or geometry.

An independent assignment reader verifies all **609 variable domains and all
5,016 serialized constraints** of model
`1027dd1d8bf01231e52b0fe4d5ff9ac42832a07e77ce1eae0b8e8317dd0585b2`.
It checks 1,140 selected optional intervals, 2,764 coarse pairs and 933 cumulative
events. The short counts are `[4,2,3]`. This is an explicit necessary-model
witness; the earlier UNKNOWN therefore was not an infeasibility proof.

## Original source still fails

Independent original-ring readback covers all 66 parts, 90 cutouts/10,026 hole
vertices, 1,632 same-sheet pairs and 264 stock edges. The full candidate has
**14 failed pairs and three failed stock guards**. Six pair failures and all
three stock failures already belong to the retained 64 under the current native
guard; those parts have zero physical intersections. The new brackets add
**eight physical intersections**. Their original labels are copies 10/11; after
the recorded model-order relabelling they are copies 2/5.

No native call is made, no gap/stock guard is weakened, and the older partial
evidence remains intact. A complete assignment to these necessary constraints
is not a valid source layout.

## Why rotation alone cannot repair this layout

For **every one of the 26 complete coarse-free cells**, the certificate identifies
a fixed cog center and one source-contained bracket rectangle. At all four
anchor-cell corners, the exact distance from that center to the translated
rectangle is strictly below the **109.113 mm** all-angle source disk radius.
The forbidden anchor region is convex, so all four corners inside it imply
every anchor in the cell lies inside it. This uses the coarse-only regions;
the extra capacity restrictions are not needed for the exclusion.

The independent certificate reader verifies all **104 squared corner distances**,
complete cell coverage, the source-contained disk proof and the short-count
exclusion. The minimum strict squared margin is **3,428,577,728 µm²**, giving a
positive radial penetration lower bound of `214286108/13639125` mm. Therefore
neither missing bracket can be inserted with the existing non-cog poses and cog
centers fixed, even with arbitrary cog angles. At least one existing non-cog pose
or cog center must change. This is a fixed-position obstruction, not a claim
that no complete arrangement exists.

Four independent audits pass, with one failed auxiliary reader preserved.
No solver or native call occurs. The next different model can add compact,
source-contained mixed cog/rectangle separation constraints while leaving every
existing position and sheet/mode option free; fixed-position insertion and
phase-only repairs are no longer useful for this configuration.

## Checkpoint and evidence

At {review['utc']}, [all six main ff5036af checks pass](https://github.com/skulitom/Nestbolt/actions/runs/40393931732).
The three queued checkpoints and this report may be pushed normally after
commit. Production, READMEs, upstream heads/releases and the 22 reserved H2
vectors remain unchanged. No new release qualifies.

[Checks]({NAME}/checks.json), [complete regions]({NAME}/regions-checks.json),
[model assignment]({NAME}/model-assignment-checks.json), [original source]({NAME}/original-source-checks.json),
[all-angle exclusion]({NAME}/disk-exclusion-checks.json), [certificate]({NAME}/disk-certificate.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json) and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 retained64 proxy witness and all-angle obstruction, 2026-10-26:** [the evidence]({link})
constructs both missing bracket copies without changing the 64 retained source
transforms. All 609 domains/5,016 constraints of the closed coupled model pass,
proving that necessary model feasible without another solve. Original-ring
readback still fails: eight new physical intersections plus six retained gap
failures and three retained stock-guard failures. An independent exact disk
certificate covers all 26 complete coarse-free bracket cells across all eight
modes, even with arbitrary cog angles. Thus at least one existing non-cog pose
or cog center must change; phase-only repair and fixed64 insertion cannot work.
Four audits pass; one auxiliary list-order reader failure is preserved. No solver
or native call occurs. All six main ff5036af checks now pass, allowing the next
normal push. H2/H5 stay open at 60%; no full-quality run or release qualifies and
all 22 reserved H2 vectors remain unopened.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'independent_audits_passed':4,'main_ci_successful_jobs':6,'push_qualified_now':True})
