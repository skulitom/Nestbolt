"""Seal the finite source-inventory result and exact fixed-proxy slot coverage."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-source-inventory-and-proxy-slot-coverage-20261025';OUT=ROOT/'benchmarks/results'/NAME
SRC=ROOT/'output/h5-source-orientation-construction-20261025';SLOTS=ROOT/'output/h5-proxy-two-bracket-completion-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    sa=load(SRC/'audit/checks.json');sm=load(SRC/'solve/model-audit.json');sr=load(SRC/'solve/result.json');sh=load(SRC/'solve/hint-audit.json');sg=load(SLOTS/'generation.json');ss=load(SLOTS/'selection.json');sc=load(SLOTS/'audit/checks.json');prior=load(ROOT/'benchmarks/results/h5-orientation-aliases-and-source-hints-20261025/source-review.json');assert all(r['passed'] for r in [sa,sm,sh,sc]);assert sr['status']=='UNKNOWN' and sr['solver_calls']==1 and not sr['incumbents'] and not sr['has_full_relaxation_solution'];assert not(SRC/'solve/relaxed-positions.json').exists();log=(SRC/'solve/solver.log').read_text(encoding='utf-8');assert 'Starting search at 0.07s' in log and 'The solution hint is incomplete: 174 out of 292 non fixed variables hinted.' in log and not re.findall(r'^#Done',log,re.M);assert sg['queries_completed']==16 and not load(SLOTS/'pending.json') and sg['total_free_cells']==0 and not sg['cell_cap_reached'];assert ss['all_cell_pairs_exhausted'] and ss['cell_pairs_examined']==0 and not ss['capped'] and not ss['found_two_proxy_slots'];assert sc['free_bracket_anchors_with64_fixed_proxy_parts']==0 and sc['core_releases_censused']==33
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head.startswith('1cc63504') and mainhead.startswith('247e823a');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());ci=json.loads(subprocess.check_output(['gh','run','view','40233299884','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==mainhead
    action='The source-orientation construction call is complete and UNKNOWN; do not rerun it or extend time. The independent integer coverage audit proves no extra bracket slot with all64 proxy poses fixed, so stop attempts that only append the missing brackets. Investigate exact small relocation neighborhoods that change a frame/cog position. For each of the33 original core parts, remove its proxy obstacles temporarily and construct complete integer free-anchor regions for that same part and two additional mandatory brackets around the remaining63 original poses. Keep every original part:63 fixed plus the released part restored plus two brackets equals66. Use the existing source orientation inventory for a finite construction test, both allowed sheets, original material cap and original-area charges. First derive an outward union of reachable occupied proxy regions and compare it to the required proxy areas to reject only certified impossible neighborhoods; do not confuse an anchor-count ranking with physical free area. Only then consider a separately declared bounded three-part feasibility model for the surviving neighborhoods, with complete independent geometry/model checks. Preserve all33 release cases, caps and pending work. A negative is conditional on that neighborhood/inventory; a positive remains a proxy and needs full cog shapes/angles, original clearance/native guards, production budget and all13jobs/two kerfs. H2 stays open; no reserved-vector access, gate reduction or new release. Poll main CI40233299884 and push further evidence normally after it is terminal.'
    OUT.mkdir();write(OUT/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    for root,prefix in [(SRC,'inventory'),(SLOTS,'slots')]:
        for rel,name in [('plan.json','plan.json'),('generation.json','generation.json'),('audit/checks.json','audit.json')]:shutil.copyfile(root/rel,OUT/f'{prefix}-{name}')
    for rel,name in [('items.json','inventory-items.json'),('groups.json','inventory-groups.json'),('solve/model-audit.json','inventory-model-audit.json'),('solve/hint-audit.json','inventory-hint-audit.json'),('solve/result.json','inventory-solver.json')]:shutil.copyfile(SRC/rel,OUT/name)
    for rel,name in [('selection.json','slots-selection.json'),('audit/coverage.json','slots-coverage.json'),('audit/ranked-core-release-census.json','core-release-census.json')]:shutil.copyfile(SLOTS/rel,OUT/name)
    write(OUT/'main-ci.json',ci);write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'current_main_ci_id':40233299884,'next_investigation':action})
    members={};inputs={}
    for root in [SRC,SLOTS]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(SRC/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['prepare_h5_source_orientation_construction.py','audit_h5_source_orientation_construction.py','prepare_h5_source_inventory_solver.py','solve_h5_source_orientation_inventory.py','solve_h5_alias_source_hints.py','h5_compound_proxy_encoding.py','h5_verified_source_hints.py','build_h5_proxy_bracket_completion.py','audit_h5_proxy_bracket_completion.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'finite_orientation_inventory_and_copy_groups_audited':True,'all66_parts_required_and_positions_free_in_search':True,'all_model_fields_and1406_hint_values_verified':True,'one_bounded_solver_call_unknown_without_incumbent':True,'independent_fixed64_proxy_integer_coverage_complete':True,'all_touching_and_single_grid_coordinate_cases_covered':True,'no_extra_bracket_slot_with_all64_poses_fixed':True,'all64_single_part_and33_core_releases_censused':True,'no_missing_part_or_unrestricted_infeasibility_claim':True,'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: source orientation inventory and exact proxy-slot coverage — 2026-10-25

**The finite all-parts-movable construction remains `UNKNOWN`. A separate exact
check proves the 64-part starting arrangement has no place for even one extra
bracket in the simplified proxy model while every existing position stays
fixed.** Existing parts must move. The conclusion is conditional on those
fixed poses; it does not establish unrestricted packing impossibility.
H2/H5 remain open at **60%** completed milestone weight.

## Source-derived orientation inventory

This construction uses the committed 64-part target layout's orientations:
18 horizontal frames; eight horizontal and thirteen vertical inserts; ten
brackets in five recorded orientation/mirror groups; and all 15 cogs. Two
additional mandatory brackets retain every original orientation/mirror option.
All positions and permitted sheet assignments remain free. The same material
cap, original area charges and five-piece inner cog proxies are retained.

Independent source and group auditing matches nine inputs to committed
evidence, checks all 1,521 same-sheet original polygon pairs and all 6,186 proxy
component pairs, both partial area bounds and four complete sweep profiles.
Minimum source gap is 0.20010000000002037 mm. No new native-margin qualification
is inferred. The 64 poses become nonbinding hints only.

There are ten interchangeable orientation-option groups, **142** per-copy
modes and **56** within-group ordering constraints. Ordering never compares
copies with unequal fixed-orientation option sets. Every source part is
represented exactly once; the two additional brackets remain required and
unhinted. This is a finite orientation inventory for construction, not a
necessary relaxation of every original arrangement.

Preparation takes 0.012657 seconds and the independent source/group audit
takes 0.082611 seconds. Every field of **1,486 variables and 2,178 constraints**
is independently reconstructed, including all 1,406 nonbinding hinted values,
138 coupled inner rectangles, 552 optional intervals, two NoOverlap2D
constraints, four cumulative profiles and both original-area bounds. Model
construction takes 0.036492 seconds and encoding audit 0.024289 seconds.

One declared 60-second, eight-worker, seed-zero call starts search at
**0.07 seconds**. Its presolved hint covers 174 of 292 nonfixed variables.
The call returns **`UNKNOWN` in {sr['seconds']:.6f} seconds**, with 532,358
branches, 116,192 conflicts and no incumbent. The small soft-limit overrun is
preserved. It is not repeated, extended or called an infeasibility proof.

## Direct exact check of the two missing slots

Keep all 64 source proxy poses fixed only for this diagnostic. The two missing
brackets retain all eight orientation/reflection cases on both sheets. Their
coupled rectangle components and the 134 fixed inner components have exact
integer coordinates at 100 units/mm.

Two axis-aligned components overlap only when both coordinate intervals
overlap strictly. For an integer moving anchor, the forbidden x interval is
`[fixed_min_x - moving_max_x + 1, fixed_max_x - moving_min_x - 1]`, with the
same rule for y. Clip these inclusive integer rectangles to the unchanged
mode domain. Sweep every critical x slab and complement the merged forbidden
y intervals. This includes boundary touching and isolated one-grid-coordinate
rows or columns; no sampled candidate list stands in for complete coverage.

All **16** queries finish in **0.039943 seconds**, within the declared
120-second construction limit and 200,000-cell cap, with nothing pending.
Every query has **zero** free integer anchors. The bounded two-slot selector
therefore examines zero cell pairs and is fully exhausted without hitting a
cap. It makes no additional solver call.

An independent audit reconstructs all **1,950** forbidden rectangles and uses
per-owner two-dimensional prefix-sum arrays over every critical x/y cell.
This is separate from the construction's interval-merging sweep. Exact integer
widths times heights count **266,545,630,376 mode/anchor pairs** across
**145,251** critical cells. Every one is covered by at least one fixed part.
The independent audit takes **0.060711 seconds** and confirms zero free anchors,
including touching/degenerate-grid cases. Thus even one extra bracket requires
changing an existing position in this proxy model.

## Single-part release census

Coverage is counted by original part, with all components of one part unioned
before counting owners. Cells covered by exactly one owner identify precisely
which bracket anchors become available if that entire part is removed
temporarily. All 64 possible single-part releases are recorded, including all
**33** frame/cog releases. Each core release exposes at least one bracket anchor.

These are counts of possible placements across orientation modes, not physical
free area, and they do not show that two brackets plus the removed part fit.
The next investigation must restore the released part: 63 fixed originals plus
that original part and two new bracket copies totals the required **66**.
No deletion, partial inventory or relaxed native requirement is accepted.

{action}

## Repository and evidence

Engine source, all three accurate READMEs and release versions are unchanged.
Main 247e823a's existing run **40233299884** is captured as `{ci['status']}` /
`{ci['conclusion'] or 'pending'}`. The previous exact-alias checkpoint remains
local at source head {head[:8]} while this hosted run finishes. No unfinished
run is called a pass. No native packing, production-budget run, full H5 matrix
or held-out evaluation occurs. No new release is qualified.

Evidence: [inventory plan]({NAME}/inventory-plan.json),
[source/group audit]({NAME}/inventory-audit.json), [model audit]({NAME}/inventory-model-audit.json),
[bounded result]({NAME}/inventory-solver.json), [slot plan]({NAME}/slots-plan.json),
[independent coverage]({NAME}/slots-audit.json), [all query counts]({NAME}/slots-coverage.json),
[core-release census]({NAME}/core-release-census.json), [source review]({NAME}/source-review.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']} canonical members and {archive['verified_aliases']}
aliases retain exact bytes with CRC and SHA-256 checks, including the complete
model/log, every forbidden rectangle, source hints, coverage and release census.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 source orientation inventory and exact proxy-slot coverage, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) checks a finite source-derived
orientation inventory with all 66 parts mandatory and every position free.
Its 1,486-variable/2,178-constraint model and 1,406 nonbinding hint values audit
completely; one bounded call remains UNKNOWN in 60.111765 seconds. Separately,
all 16 missing-bracket mode domains around the fixed 64-part proxy layout are
covered exactly: 1,950 forbidden rectangles cover 266,545,630,376 integer
mode/anchor pairs, independently checked across 145,251 critical cells.
No extra bracket fits while those existing poses stay fixed, including at
touching boundaries. A complete single-part release census records all 64
parts and 33 frame/cog cases; released parts must be restored in any next
63-plus-3 construction. This is conditional evidence, not unrestricted
infeasibility or a full target witness. All original acceptance requirements
remain; source, accurate READMEs and releases are unchanged. H2/H5 stay open
at 60% completed milestone weight.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
