"""Seal the new cog constructions and continuous-position capacity certificates."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import ast, json, shutil, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX = 'h5-cog-free-regions-and-continuous-capacity-20261020'
OUT = ROOT/'benchmarks/results'/PREFIX
NAMES = ['h5-cog-free-region-contacts-20261020',
         'h5-cog-free-region-contacts-20261020-v2',
         'h5-free-region-cog-completion-20261020',
         'h5-cog-clique-cover-certificate-20261020',
         'h5-cog-center-capacity-20261020',
         'h5-cog-center-band-cover-20261020',
         'h5-cog-reachable-area-20261020']
FAIL,POOL,RUN,COVER,CENTER,BAND,AREA = [ROOT/'output'/n for n in NAMES]
load = lambda p:json.loads(p.read_bytes())
digest = lambda p:sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)

def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,indent=2)
        f.write('\n')

def append(path,s):
    with path.open('a',encoding='utf-8',newline='\n') as f:
        f.write(s)

def main():
    OUT.mkdir()
    base = git('rev-parse','HEAD').decode().strip()
    assert base=='e2bf4e1c505e6ad512f818d2eb18638b0994c672'
    core = source_digest()
    assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    prior = load(ROOT/'benchmarks/results/h5-frame-capacity-and-joint-small-parts-20261020/source-review.json')
    readmes = {p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']}
    assert readmes==prior['current_readmes']
    generation = load(POOL/'generation.json')
    pa = load(POOL/'audit/checks.json')
    layout = load(RUN/'audit/checks.json')
    cert = load(COVER/'checks.json')
    center = load(CENTER/'audit/checks.json')
    band = load(BAND/'checks.json')
    area = load(AREA/'audit/checks.json')
    assert generation['new_cog_poses']==437 and generation['pending_queries']==0
    assert pa['exact_conflicts']==194803 and pa['all_cliques_pairwise_valid_and_complete']
    assert layout['all_returned_layouts_checked']==2 and layout['fresh_frozen_CLI_calls']==1
    assert cert['independent_cog_upper_bound']==14
    assert center['passed'] and center['all_angle_cog_upper_bound']==18
    assert band['passed'] and band['all_angle_cog_upper_bound']==16
    assert area['passed'] and area['all_angle_cog_upper_bound']==13 and area['required15_ruled_out']
    inputs = {}
    for root in [POOL,RUN,COVER,CENTER,BAND,AREA]:
        for name,h in load(root/'plan.json')['inputs'].items():
            assert digest(ROOT/name)==h
            if name in inputs:
                assert inputs[name]==h
            inputs[name]=h
    for p in RUN.rglob('validation-reuse-*.json'):
        reuse = load(p)
        assert reuse['rerun'] is False
        for name,h in reuse['source_files'].items():
            assert digest(ROOT/name)==h
            inputs[name]=h
    remote = git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert remote=='abeb2739b1eedde18781b46fd82258f356970be0'
    ci = json.loads(subprocess.check_output(
        ['gh','run','view','39454262478','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==remote
    if ci['conclusion']=='success':
        assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(OUT/'main-ci-abeb2739.json',ci)
    next_step = ('Do not repeat cog-only searches around these51 fixed non-cog poses: a continuous all-angle upper bound13 excludes the required15. '
                 'Next examine a finite census that removes each non-cog obstacle in turn, recomputing the same conservative center/area bounds '
                 'while retaining the other50 poses. Removing a part is a necessary relaxation, not a completed layout. '
                 'A remaining bound below15 rules out changing only that pose; a larger bound merely identifies a possible joint-move target. '
                 'Independently audit the resulting certificates before constructing changed non-cog placements. '
                 'Do not reuse the old conditional cog conflict graph after non-cog moves. '
                 'All66 original copies, native margins and unchanged H5 material/cutting gates remain required. H2 stays open under Artem’s decision.')
    write(OUT/'source-review.json',{
        'reviewed_utc':datetime.now(timezone.utc).isoformat(),'source_head':base,
        'production_digest':core,'current_readmes':readmes,'README_change_needed':False,
        'remote_main':remote,'remote_CI_status':ci['status'],'remote_CI_conclusion':ci['conclusion'],
        'original_geometry_layout_audits':2,'fresh_frozen_CLI_calls':1,'exact_CLI_results_reused':1,
        'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'full_target_witness':False,'new_release_qualified':False,'completion_percent':60,
        'H2_complete':False,'H5_complete':False,'next_investigation':next_step})
    for p,name in [
        (POOL/'generation.json','generation.json'),(POOL/'audit/checks.json','pool-audit.json'),
        (RUN/'model-audit.json','cog-model-audit.json'),(RUN/'result.json','cog-result.json'),
        (RUN/'audit/checks.json','layout-audit.json'),(COVER/'checks.json','finite-cover-audit.json'),
        (COVER/'result.json','finite-cover-result.json'),(CENTER/'audit/checks.json','center-region-audit.json'),
        (BAND/'checks.json','band-cover-audit.json'),(AREA/'checks.json','area-bound.json'),
        (AREA/'audit/checks.json','continuous-capacity-audit.json')]:
        shutil.copyfile(p,OUT/name)
    members = {}
    for root in [FAIL,POOL,RUN,COVER,CENTER,BAND,AREA]:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for name in inputs:
        p=ROOT/name
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helper_names=['build_h5_cog_free_regions.py','audit_h5_cog_free_regions.py',
                  'solve_h5_free_region_cogs.py','audit_h5_free_region_cog_results.py',
                  'certify_h5_cog_cover.py','bound_h5_cog_centers.py','audit_h5_cog_center_capacity.py',
                  'cover_h5_cog_centers_by_bands.py','bound_h5_cog_reachable_area.py',
                  'audit_h5_cog_reachable_area.py','ccd1.py']
    pending=[ROOT/'output'/name for name in helper_names]
    visited=set()
    while pending:
        p=pending.pop()
        if p in visited:
            continue
        visited.add(p)
        members['helpers/'+p.name]=p
        tree=ast.parse(p.read_text(encoding='utf-8'))
        modules=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom) and node.module:
                modules.append(node.module.split('.')[0])
            elif isinstance(node,ast.Import):
                modules.extend(a.name.split('.')[0] for a in node.names)
        for module in modules:
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
        'passed':True,'all_source_hashes_verified':True,'new_cog_poses':437,
        'finite_pool_cog_choices':1045,'finite_pool_cover_bound':14,
        'initial_continuous_box_bound':18,'continuous_band_bound':16,
        'continuous_area_bound':14,'combined_continuous_upper_bound':13,
        'required15_impossible_with_these51_non_cog_poses':True,
        'impossible_after_non_cog_moves_claimed':False,'all_original_failures_preserved':True,
        'original_geometry_layout_audits':2,'fresh_frozen_CLI_calls':1,'exact_CLI_results_reused':1,
        'full_target_witness':False,'new_release_qualified':False,'completion_percent':60,
        'archive_members':len(manifest),'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    ci_note=('All six remote abeb2739 checks pass in the saved snapshot.' if ci['conclusion']=='success'
             else 'The remote abeb2739 checks are still running in the saved snapshot; five jobs pass and the Windows check remains in progress. No complete CI success is inferred.')
    report=f'''# H5: cog free regions and continuous capacity — 2026-10-20

**At most thirteen cogs can fit while the selected 51 non-cog parts stay fixed,
even with arbitrary cog angles and continuous positions.** The original job
requires fifteen. At least one frame, bracket or insert pose must therefore
change. This is a necessary upper bound, not a thirteen-cog layout, and it
does not exclude solutions after other parts move. H2/H5 remain open at 60%.

## New cog contacts and retained failures

The [prior joint construction](h5-frame-capacity-and-joint-small-parts-20261020.md)
supplies all 18 frames, 12 brackets, 21 inserts and nine cogs. Its 51 non-cog
poses stay fixed for this investigation. Original filled outer outlines,
stock, margins, 0.2 mm clearance and material target remain unchanged.

The first preparation stopped with a missing `Path` import before creating
a plan or doing geometry work. Its exact helper and traceback are preserved.
The repaired preparation uses a new directory and records that repair.

All 9299 original candidate entries remain unchanged. Original-geometry checks
retain 608 of the 3947 old cog poses. Eight conservative free translation
regions cover four declared phases (0°, 4.5°, 9°, 13.5°) on two sheets.
All 438 proposed boundary/representative samples are processed: 437 new poses
and one exact duplicate, leaving no pending queries. Generation takes
3.484624400 seconds within its declared 120-second/2000-new-pose bounds.

An independent audit reconstructs every region and sampling order, checks
159,831 original cog/fixed-part pairs and 18,306 new cog/fixed-part pairs,
and exhaustively examines all 357,456 same-sheet pairs in the 1045-cog pool.
The exact 194,803 conflicts are represented by 883 verified cliques.
All nine known seed cogs remain. This finite sampling is not an all-angle proof.

The fully reconstructed cog-only model has 1045 variables and 884 constraints.
Its single declared 20-second call returns `OPTIMAL` in 0.748112200 seconds,
with nine cogs and solver bound nine. Both returned selections pass original
geometry; the exact seed's frozen CLI result is reused by hash, and the new
final layout receives one fresh CLI call. Both fail only because six cogs
are missing. The new final uses three new contacts and has minimum clearance
0.200100 mm. Its material charge is 4,985,103.45 mm² and filled area is
4,181,364.4704 mm², unchanged from this seed. It is not native-margin qualified
or an improvement over the previously documented best partials.

A separate cover-certificate model starts from the weaker greedy bound 17.
Its one declared 10-second call finishes in 0.538477400 seconds; saved covers
have sizes 17, 16, 15 and 14. Independent graph checks prove each cover valid.
The final certificate allows at most 14 cogs in this finite pool. It does not
independently certify the solver's reported packing optimum nine.

## A bound for all angles and continuous positions

The next construction replaces finite sampling with necessary geometry:

1. Exact rational segment-distance checks prove that a disk of radius
   **109.1157 mm** fits inside the filled cog about its recorded local center.
   Every rotated cog contains that disk. A deliberately weaker **0.1999 mm**
   clearance yields necessary center separation **218.4313 mm**.
2. Seventy-five axis-aligned rectangles are verified strictly inside the
   original transformed non-cog polygons with exact rational predicates.
   Expanding these by integer rectangles contained in a disk gives conservative
   forbidden center regions. Stock center limits are rounded outward.
3. Independent exact rectangle sweeps reconstruct the entire possible-center
   superset: 139 cells on sheet zero and one on sheet one. Small-diameter
   rectangle covers first bound capacity at 15 + 3 = **18**; a finite band
   partition improves this to 13 + 3 = **16**. Both results are retained and
   are inconclusive by themselves.
4. An exact rational **140.0002 mm** circumradius contains every cog vertex
   and hence the filled cog at any angle. Expanding each possible-center cell
   by its radius square encloses all space any cog can occupy. Clip this to
   outward-rounded usable stock and subtract only the verified solid interior
   rectangles of fixed parts. The resulting area is an upper bound, including
   space an actual cog might never be able to use.
5. Disjoint cogs each consume their original filled area,
   **50,062.718937983 mm²**. A conservative 0.000001 mm² allowance weakens this
   lower bound. Three different exact integer area algorithms agree; a separate
   geometry check also matches the areas and retains all nine known seed cogs.

| Target sheet | Reachable area upper bound, mm² | Area-based cog bound | Band-cover cog bound | Combined bound |
| --- | ---: | ---: | ---: | ---: |
| First | 549,821.78082009 | 10 | 13 | 10 |
| Last | 250,038.34467349 | 4 | 3 | 3 |
| Total | — | 14 | 16 | **13** |

The separate audit rechecks the circumradius, rational polygon area, all
expanded/clipped rectangles, exact area totals and all four band covers.
Known cog centers lie in the certified center regions and their complete
filled polygons lie in the reachable-area superset. Strict conservative
offsets and closed cell coverage account for boundary positions.

This certificate is conditional on these 51 non-cog poses and the original
filled-outer policy. It establishes that changing cog positions or phases
alone cannot complete this arrangement. It does not relax any H5 acceptance
rule, prove that thirteen are attainable, or rule out a rearranged full job.

## Source, README and release

Core source retains digest `{core}`. The English README includes the
remote comparison-page addition and still accurately describes the published
v0.2.0-alpha.1 preview, stable v0.1.0 and 60% plan completion. All three README
hashes match the previous reviewed checkpoint; no further README edit is needed
for this diagnostic evidence. Published release assets remain unchanged.

{ci_note}

No native packing, quality run or reserved held-out evaluation occurs.
The two actual layouts remain quantity failures. No new release is qualified.

## Next work

{next_step}

[Checks]({PREFIX}/checks.json), [pool audit]({PREFIX}/pool-audit.json),
[layout audit]({PREFIX}/layout-audit.json), [finite certificate]({PREFIX}/finite-cover-audit.json),
[center-region audit]({PREFIX}/center-region-audit.json),
[band covers]({PREFIX}/band-cover-audit.json),
[continuous certificate audit]({PREFIX}/continuous-capacity-audit.json),
[source review]({PREFIX}/source-review.json), [remote checks]({PREFIX}/main-ci-abeb2739.json),
[raw evidence]({PREFIX}/raw.zip) and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 cog free regions and continuous capacity, 2026-10-20:** [the independently audited certificate](../benchmarks/results/{PREFIX}.md)
proves at most **13 cogs** fit around the current 51 fixed non-cog poses,
even allowing arbitrary angles and continuous positions. The original job
requires 15, so at least one frame, bracket or insert must move. Earlier
finite sampling adds 437 cog poses but still selects nine; both returned
layouts pass original geometry and retain their six-missing-cog CLI failures.
The weaker finite cover14, continuous box18 and band16 bounds are preserved.
Exact reachable-area checks allow10 cogs on the first sheet; an independently
verified diameter cover allows3 on the last. This is a conditional upper
bound, not an attainable13-cog layout or a claim after other parts move.
Next audit which single non-cog releases can remove this obstruction;
do not repeat the ruled-out cog-only search. Core source and all three README
hashes remain unchanged. No native quality run or new release is qualified.
H2/H5 remain open at60% under the original requirements.
'''
    assert (ROOT/'BENCHMARKS.md').read_bytes()==git('show','HEAD:BENCHMARKS.md')
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
        append(ROOT/name,'\n'+note)
    status=ROOT/'docs/STATUS.md'
    text=status.read_text(encoding='utf-8')
    marker='**N4 frame capacity and joint small parts, 2026-10-20:**'
    assert text.count(marker)==1
    status.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
                      'continuous_cog_upper_bound':13,'completion_percent':60}))

if __name__=='__main__':
    main()
