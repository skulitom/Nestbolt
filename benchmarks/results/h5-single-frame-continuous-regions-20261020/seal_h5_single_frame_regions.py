"""Preserve continuous frame domains, coarse bounds and the bounded refinement."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-single-frame-continuous-regions-20261020'
OUT=ROOT/'benchmarks/results'/PREFIX
FRAME=ROOT/'output/h5-single-frame-center-regions-20261020'
COARSE=ROOT/'output/h5-single-frame-region-capacity-20261020'
REFINE=ROOT/'output/h5-single-frame-spatial-refinement-20261020'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)

def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,indent=2)
        f.write('\n')

def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as f:
        f.write(text)

def main():
    OUT.mkdir()
    head=git('rev-parse','HEAD').decode().strip()
    assert head=='7c47f4989d40a6ba81e7022457f175b3965c4e7d'
    core=source_digest()
    assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    fa=load(FRAME/'audit/checks.json')
    ca=load(COARSE/'audit/checks.json')
    ra=load(REFINE/'audit/checks.json')
    rr=load(REFINE/'result.json')
    assert fa['passed'] and fa['queries_verified']==72 and fa['original_frame_poses_retained']==18
    assert ca['passed'] and ca['regions_verified']==52 and len(ca['inconclusive_regions'])==36
    assert ra['passed'] and ra['new_nodes_verified']==165 and ra['pending_nodes']==49
    assert rr['time_limit_reached'] and not rr['all_single_frame_moves_ruled_out']
    excluded=[r['candidate'] for r in ra['frame_proofs'] if r['single_frame_move_ruled_out']]
    unresolved=[r['candidate'] for r in ra['frame_proofs'] if not r['single_frame_move_ruled_out']]
    assert len(excluded)==10 and len(unresolved)==8
    prior=load(ROOT/'benchmarks/results/h5-single-non-cog-release-census-20261020/source-review.json')
    readmes={p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']}
    assert readmes==prior['current_readmes']
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert remote==head
    ci=json.loads(subprocess.check_output(
        ['gh','run','view','39461163256','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==head
    if ci['conclusion']=='success':
        assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(OUT/'main-ci-7c47f498.json',ci)
    inputs={}
    for root in [FRAME,COARSE,REFINE]:
        for name,h in load(root/'plan.json')['inputs'].items():
            assert digest(ROOT/name)==h
            if name in inputs:
                assert inputs[name]==h
            inputs[name]=h
    next_step=('Do not resume or extend the expired120-second spatial tree unchanged. Its49 pending nodes retain exact center cells for eight unresolved frames. '
               'Use those cells as a finite construction source: propose original-geometry frame contacts within them, keep each original frame as a checked baseline, '
               'and discard any proposal violating the other50 non-cog poses or original stock/clearance. '
               'For each unresolved frame, new cog contacts may be generated around the other50 fixed non-cog parts before a changed joint choice of one frame and up to15 cogs. '
               'Every new candidate and all frame/cog and cog/cog conflicts need original-geometry audit; the old51-fixed graph cannot be assumed valid. '
               'A completed result requires restoring the frame and all66 original copies, independent geometry/CLI checks, native margins and unchanged H5 gates. '
               'The43 ruled-out single changes need no further single-part search around this arrangement. Multiple non-cog changes remain possible.')
    write(OUT/'source-review.json',{
        'verified_utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'production_digest':core,
        'current_readmes':readmes,'README_change_needed':False,'remote_main':remote,
        'remote_main_CI_status':ci['status'],'remote_main_CI_conclusion':ci['conclusion'],
        'single_frame_moves_ruled_out':excluded,'unresolved_frame_candidates':unresolved,
        'single_non_cog_moves_ruled_out_total':43,'fresh_CLI_calls':0,'native_packing_calls':0,
        'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,
        'new_release_qualified':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,
        'next_investigation':next_step})
    for p,name in [
        (FRAME/'result.json','frame-region-result.json'),(FRAME/'audit/checks.json','frame-region-audit.json'),
        (COARSE/'result.json','coarse-capacity-result.json'),(COARSE/'audit/checks.json','coarse-capacity-audit.json'),
        (REFINE/'result.json','refinement-result.json'),(REFINE/'audit/checks.json','refinement-audit.json')]:
        shutil.copyfile(p,OUT/name)
    members={}
    for root in [FRAME,COARSE,REFINE]:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for name in inputs:
        p=ROOT/name
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in [
        'build_h5_single_frame_center_regions.py','audit_h5_single_frame_center_regions.py',
        'bound_h5_single_frame_regions.py','audit_h5_single_frame_region_capacity.py',
        'refine_h5_single_frame_regions.py','audit_h5_single_frame_spatial_refinement.py','ccd1.py']]
    visited=set()
    while pending:
        p=pending.pop()
        if p in visited:
            continue
        visited.add(p)
        members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module
                  else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for module in mods:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():
                    pending.append(other)
    manifest=[]
    archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name)
            manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:
            assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{
        'passed':True,'all_source_hashes_verified':True,'frame_center_queries_verified':72,
        'original_frame_poses_retained':18,'initial_components_verified':52,
        'coarse_components_excluded':16,'new_refinement_nodes_verified':165,
        'pending_nodes_preserved':49,'refinement_time_limit_preserved':True,
        'frames_ruled_out':10,'frames_unresolved':8,'all_single_frame_moves_ruled_out':False,
        'single_non_cog_moves_ruled_out_including_previous_small_parts':43,
        'no_full_target_witness':True,'new_release_qualified':False,'completion_percent':60,
        'archive_members':len(manifest),'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    ci_note=('All six checks on the pushed 7c47f498 checkpoint pass in the saved snapshot.'
             if ci['conclusion']=='success' else
             'Checks on the pushed 7c47f498 checkpoint are still running in the saved snapshot. A complete pass is not inferred.')
    report=f'''# H5: continuous regions for a single frame move — 2026-10-20

**Ten of eighteen possible single-frame changes are now ruled out across all
allowed frame positions and rotations.** Together with the preceding bracket
and insert certificates, this excludes 43 of the 51 single non-cog changes
around this arrangement. Eight frames remain unresolved. No full layout,
material improvement or new release is established; H2/H5 remain open at 60%.

## Cover all possible positions of a released frame

The [single-part census](h5-single-non-cog-release-census-20261020.md) excludes
every individual bracket or insert move. For each remaining frame, the other
50 non-cog poses stay fixed. The original frame is a 450 × 350 mm rectangle
with four allowed quarter turns; its holes remain reserved under the unchanged
common-line filled-outer policy.

An axis rectangle inset **0.0002 mm per side** fits inside every rotated frame
about its transformed local center. Exact rational containment checks verify
this for all four allowed rotations. The two resulting axis-size classes
cover all four rotations. Certified interior rectangles of the fixed parts,
expanded by the frame half-extents and rectangles within a deliberately weaker
**0.1998 mm** clearance disk, define necessary forbidden center regions.
Stock center limits are rounded outward.

All **72 queries** (18 frames × 2 size classes × 2 sheets) complete in
**4.230176500 seconds**, within the declared 120-second bound. The last sheet
is too short for either frame size class. The first-sheet queries contain
**4625 free cells in 52 components**; all 18 original frame poses are retained
in their corresponding size classes.

The independent audit checks the four moving-frame containments, every
expanded rectangle and exact complementary area. It verifies all 72 queries
in **3.838829400 seconds**. These domains are supersets of valid positions,
so they support necessary bounds; they are not new accepted frame placements.

## Guaranteed occupied area across a whole region

For any center-region bounding box, intersect the frame's inner rectangle over
all center positions in that box. When nonempty, this common solid rectangle
is occupied by every possible frame pose in the region. Adding it to the
other 50 non-cog obstacles gives a necessary bound on cogs without selecting
a particular frame position.

Each region uses the previously audited cog inner disk and circumradius,
exact reachable-area bounds, small-diameter covers and verified cliques of
mutually incompatible center components. A single deterministic pass over
all 52 components takes **37.089722700 seconds**. Its independent audit checks
136 cog components and 272 band covers. **Sixteen whole regions are excluded;
36 remain inconclusive.** The coarse results are preserved.

## Bounded spatial refinement

The changed construction keeps those sixteen exclusions and divides the
36 unresolved center regions at integer midpoints along their longest dimension.
It clips the exact free cells into children and recomputes the guaranteed
frame core and cog bound. It declares **120 seconds**, at most **256 new nodes**
and depth at most **six**, with a breadth-first order and no retry.

The run stops at its time boundary after **120.343610200 seconds**:
**165 new nodes are evaluated and 49 remain pending**. The small overshoot
finishes the current indivisible case; no further case starts after the
between-case deadline. Of the evaluated nodes, 94 exclude their entire region.
No depth-six terminal case occurs. The exact pending queue is retained.

An independent audit verifies the complete tree and midpoint partitions,
every guaranteed frame core, **499 cog components** and **998 band covers**.
The unchanged last-sheet capacity-three certificate is reused byte-for-byte.
The audit takes **22.344450500 seconds**. Exclusion is propagated only through
fully covered trees; an unfinished branch never becomes an impossibility claim.

| Single-part change | Fully excluded | Still unresolved |
| --- | ---: | ---: |
| Bracket, from the previous census | 12 | 0 |
| Insert, from the previous census | 21 | 0 |
| Frame, after this audit | 10 | 8 |
| Total | **43** | **8** |

The unresolved frame candidates are **{', '.join(map(str,unresolved))}**.
Their 49 pending regions provide bounded locations for a different
construction. This evidence does not exclude multiple non-cog changes and
does not prove that any unresolved single-frame change is feasible.

## Source, README and checks

Core source retains its reviewed digest; all three README hashes are unchanged.
The README still accurately describes the published preview and open work.
No new layout or frozen CLI validation is produced, and no native packing,
quality run or reserved held-out evaluation occurs.

{ci_note} The previous abeb2739 checkpoint's six successful checks remain
recorded separately. Published releases and original acceptance requirements
are unchanged.

## Next work

{next_step}

[Checks]({PREFIX}/checks.json), [frame domains]({PREFIX}/frame-region-audit.json),
[coarse bounds]({PREFIX}/coarse-capacity-audit.json),
[refinement result]({PREFIX}/refinement-result.json),
[independent tree audit]({PREFIX}/refinement-audit.json),
[source review]({PREFIX}/source-review.json), [pushed-checkpoint checks]({PREFIX}/main-ci-7c47f498.json),
[all regions, nodes and pending work]({PREFIX}/raw.zip)
and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 continuous single-frame regions, 2026-10-20:** [the complete audited record](../benchmarks/results/{PREFIX}.md)
covers all 72 frame/size-class/sheet queries and retains all 18 original frame
poses. Guaranteed occupied rectangles exclude 16 of 52 whole center regions.
A changed midpoint subdivision stops at its declared 120-second boundary
after 165 new cases, preserving 49 pending nodes. Independent exact geometry,
area and tree-coverage checks rule out ten of the eighteen single-frame moves.
Together with the previous small-part certificates, 43 single non-cog changes
are excluded and eight frame choices remain unresolved. No unfinished tree
is treated as a proof. Next construct and audit changed frame/cog candidates
within the remaining regions; do not extend the expired tree unchanged.
Core source, README and releases remain unchanged. H2/H5 remain open at 60%.
'''
    assert (ROOT/'BENCHMARKS.md').read_bytes()==git('show','HEAD:BENCHMARKS.md')
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
        append(ROOT/name,'\n'+note)
    path=ROOT/'docs/STATUS.md'
    text=path.read_text(encoding='utf-8')
    marker='**N4 single non-cog release census, 2026-10-20:**'
    assert text.count(marker)==1
    path.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
                      'frames_excluded':10,'frames_unresolved':8,'completion_percent':60}))

if __name__=='__main__':
    main()
