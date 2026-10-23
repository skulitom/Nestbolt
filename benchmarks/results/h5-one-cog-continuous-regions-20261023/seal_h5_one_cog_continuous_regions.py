"""Seal the failed obstacle checks, explicit polygon repair and audited new cog contacts."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-one-cog-continuous-regions-20261023';FAILED=ROOT/'output'/NAME;BASE=ROOT/'output'/(NAME+'-v2');INSPECT=ROOT/'output/h5-current-cog-gap-inspection-20261023';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    gen=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');mitre=load(FAILED/'translation-diagnosis/result.json');rounded=load(FAILED/'round-repair-diagnosis-v2/checks.json');repair=load(FAILED/'polygon-repair-diagnosis/checks.json');nextstep=load(BASE/'next-step.json')
    assert audit['passed'] and repair['passed'] and not rounded['passed'] and not nextstep['full_target_witness'] and not list((FAILED/'regions').glob('*.json'))
    assert gen['new_cog_poses']==audit['new_poses_independently_checked']==4000 and gen['regions_completed']==120 and gen['pending_proposal_lists']==60
    priorroot=ROOT/'benchmarks/results/h5-one-cog-release-joint-20261023';prior=load(priorroot/'source-review.json');assert source_digest()==prior['production_digest'] and {p:digest(ROOT/p) for p in prior['current_readmes']}==prior['current_readmes'];previous=load(priorroot/'raw-manifest.json');hashes={r['path']:r['sha256'] for r in previous['files']+previous['aliases']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==hashes['source-inputs/'+p.relative_to(ROOT).as_posix()]
    OUT.mkdir()
    for p,name in [(BASE/'plan.json','plan.json'),(BASE/'result.json','generation.json'),(BASE/'audit/plan.json','audit-plan.json'),(BASE/'audit/checks.json','audit.json'),(BASE/'next-step.json','next-step.json'),(BASE/'obstacle-cache-audit.json','obstacle-cache-audit.json'),(FAILED/'translation-diagnosis/result.json','mitre-diagnosis.json'),(FAILED/'round-repair-diagnosis-v2/checks.json','round-diagnosis.json'),(FAILED/'polygon-repair-diagnosis/checks.json','polygon-repair.json'),(FAILED/'failure.txt','original-failure.txt'),(INSPECT/'seed.png','original-seed.png')]:shutil.copyfile(p,OUT/name)
    cis=[]
    for run,head in [('39976658315','752b1c60e38adfaa554d9220382177b935eabf72'),('39984899040','facf0f388f865768ab60d7a8549eef67198ae714')]:
        ci=json.loads(subprocess.check_output(['gh','run','view',run,'--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==head;write(OUT/f'main-ci-{head[:8]}.json',ci);cis.append(ci)
    assert cis[0]['conclusion']=='success' and len(cis[0]['jobs'])==6 and all(j['conclusion']=='success' for j in cis[0]['jobs'])
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'main_head':subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'best_checked_parts':64,'best_checked_missing':{'bracket':2},'full_target_witness':False,'native_margin_qualified':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':nextstep['action']};write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,FAILED,INSPECT]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('*.json'):
            if p.name not in ['plan.json','inspection.json']:continue
            value=load(p)
            for name,hsh in value.get('inputs',value.get('source_hashes',{})).items():
                if name in inputs:assert inputs[name]==hsh
                inputs[name]=hsh
    for name,hsh in inputs.items():
        p=ROOT/name;assert digest(p)==hsh;members['source-inputs/'+name.replace('\\','/')]=p
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/name for name in ['build_h5_one_cog_continuous_regions.py','build_h5_one_cog_continuous_regions_v2.py','prepare_h5_one_cog_continuous_regions_v2.py','audit_h5_one_cog_continuous_regions.py','diagnose_h5_cog_obstacle_translation.py','check_h5_round_obstacle_repair.py','check_h5_polygon_obstacle_repair.py','conservative_h5_round_obstacles.py','conservative_h5_polygon_obstacles.py','inspect_h5_current_cog_gaps.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            modules=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'all_original_inputs_match_previous_manifest':True,'all_input_hashes_verified':True,'failed_checks_and_all_diagnostics_preserved':True,'explicit_clearance_polygon_verified':True,'every_new_pose_and_all_30_core_memberships_checked':True,'all_queue_events_and_pending_lists_preserved':True,'new_variable_graph_and_selection_pending':True,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(manifest['archives'],1))
    report=f'''# H5: continuous cog contacts and clearance-outline repair — 2026-10-23

**4,000 new cog poses pass original geometry and independent membership checks
against all 30 repair cores.** Of these, 3,971 have centers more than 0.05 mm
from every old cog center on their sheet, and 2,075 make at least one old
bracket candidate available relative to the released cog. These are candidate
positions, not additional placed parts. No new layout selection occurs here;
the best checked layout remains **64/66**, missing two brackets. H2/H5 stay
open at **60%** completed milestone weight.

## Failed check and repaired clearance construction

The original attempt stopped at its first cached-obstacle equivalence check,
before any region query completed or placement was generated. Its source,
plan and traceback remain intact. The original fixed cog shape and its
translated copy are exactly equal. Their unbuffered Minkowski obstacles differ
by only {repair['unbuffered_translation_hausdorff_mm']:.3g} mm, but mitred
clearance buffering amplifies the difference to
**{mitre['hausdorff_error_mm']:.12f} mm**, with symmetric-difference area
{mitre['difference_area_mm2']:.12f} mm². This failed the existing strict check.

A proposed round-buffer replacement also failed the same equivalence threshold:
{rounded['new_round_translation_hausdorff_mm']:.12f} mm. Its stopped assertion
and the subsequent diagnostic that records all values are preserved. Neither
failure is omitted or counted as a completed placement search.

The repaired helper constructs an explicit circumscribed **128-gon** around
the required 0.2 mm clearance plus the existing 0.0001 mm construction margin.
Every chord is independently checked to lie at least 0.2001 mm from its center.
The resulting radius is {repair['circle']['construction_radius_mm']:.12f} mm.
The helper forms the Minkowski sum by uniting the original obstacle with each
boundary segment swept by this convex polygon; hole rings are included.
This identity is independently checked against sums over exact convex pieces
for concave and holed examples, with zero difference.

On the unchanged failed case, the globally constructed and translated repaired
obstacles agree within **{repair['polygon_translation_hausdorff_mm']:.3g} mm**
and {repair['polygon_translation_area_mm2']:.3g} mm². All eight actual
family/orientation cache cases also pass the original 1e-7 mm / 1e-4 mm²
equivalence limits. Original part vertices, clearance and acceptance tolerances
are unchanged. This is a development helper repair; production code is unchanged.

## Completed region and bounded proposal passes

The new directory uses the same **120-second region allowance**, **60-second
proposal allowance** and **4,000-new-pose cap**. It considers the original wide
seed's 15 cores, each fixing 18 frames and 14 cogs, on both sheets. Four sampled
angles use the original **-2.2428996024478143 radians (-128.508681091830°)**
plus 0°, 4.5°, 9° and 13.5°. Cogs are never mirrored. These are finite free-angle
samples, not an exhaustive rotation search.

All **120/120** regions complete in **{gen['region_seconds']:.6f} seconds**;
none is empty. Representatives, boundary vertices and edge midpoints are
preserved for every region. Proposal lists are processed round-robin with exact
transform deduplication. The pass reaches its 4,000-pose cap after
**{gen['proposal_seconds']:.6f} seconds** and {gen['events']:,} events:
4,000 additions and 14,339 exact duplicates. There are no original-geometry
rejections. **60 unfinished proposal lists remain recorded**, and are not
resumed or silently completed. Conservative regions cannot prove impossibility.

## Independent original-geometry audit

All **35,488 original pool records** remain exactly equal as parsed JSON,
with all original indexes and seeds intact. Independent original-vertex
reconstruction checks all 4,000 new poses, their transforms, allowed stock
domains, source query points, areas and generating-core distances. It verifies
all {audit['original_generation_pairs_verified']:,} original generation pairs.
Every one of the {audit['queue_events_replayed']:,} queue events and every
pending-list cursor replays exactly; all 120 saved regions and proposal lists
verify.

Compatibility is then checked against **all 30 cores**, including the second
seed's frame positions. All **{audit['new_pose_core_memberships_checked_both_methods']:,}**
memberships agree between individual fixed-part distances and distances to
the full filled core unions. This includes
{audit['new_pose_distinct_fixed_part_pairs']:,} distinct fixed-part pairs and
120,000 union distances. The future conditional pool therefore retains all
**16,058 old variable choices plus 4,000 new cogs: 20,058 choices**. All 30
mapped 64-part baselines remain present.

Bracket effects are independently recalculated with a sequential bounds scan
and **{audit['bracket_diagnostic_exact_pair_checks']:,}** exact distances,
rather than the generator's spatial-tree lookup. Every gain/loss list matches.
The largest single gain is **{audit['maximum_newly_available_bracket_choices']} bracket
candidate positions**. This is not a claim that 290 brackets, or even one
additional bracket, can be placed together with the required inventory.
Nearest original cog centers are independently reconstructed by affine
centroid transforms. The complete audit takes {audit['seconds']:.6f} seconds.

## Next action and gate status

{nextstep['action']}

No solver, native packing, production-budget qualification, complete H5 matrix
or held-out evaluation occurs. All 66 original copies, the original material
target, native guard, original production budget and all 13 jobs at both kerfs
remain required. The original cores are not native-margin qualified; the new
contact construction does not change that. No milestone or new release is
qualified by this diagnostic.

All six hosted checks for 752b1c60 pass. The queued d49d0ff6 and facf0f38
checkpoints were then pushed normally to main, with no incoming changes.
The new facf0f38 run 39984899040 is saved as
`{cis[1]['status']}` / `{cis[1]['conclusion'] or 'pending'}`. Source and all
three accurate READMEs remain unchanged; preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain current.

Evidence: [original seed view]({NAME}/original-seed.png),
[failed mitre check]({NAME}/mitre-diagnosis.json), [failed round check]({NAME}/round-diagnosis.json),
[polygon repair]({NAME}/polygon-repair.json), [cache checks]({NAME}/obstacle-cache-audit.json),
[generation]({NAME}/generation.json), [independent audit]({NAME}/audit.json),
[source review]({NAME}/source-review.json), raw evidence {links}, and
[manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases are byte-verified, with archive
CRCs and SHA-256 hashes checked. Each ZIP part is independently readable and
below 50 MiB; all original paths remain represented.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 continuous cog contacts, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
preserves a failed mitre-buffer equivalence check and a failed round-buffer
alternative, then verifies an explicit circumscribed 128-gon clearance helper.
All 120 new one-cog region queries complete; 4,000 new poses pass original
geometry and all 120,000 memberships across 30 fixed cores. There are 3,971
new centers beyond 0.05 mm and 2,075 poses opening old bracket choices, which
are candidate diagnostics rather than additional placed parts. All 60 capped
proposal lists remain recorded. The 20,058-choice joint graph and selection
are pending; best checked inventory remains 64/66. Both queued checkpoints
are pushed to main facf0f38 after all six 752b1c60 checks pass. Source, READMEs,
releases and gate requirements are unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
