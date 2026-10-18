"""Seal a bounded finite-pool selection and its independently audited incomplete outcome."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from collections import Counter
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];RUN=ROOT/'output/h5-saved-placement-selection-20261018';OUT=ROOT/'benchmarks/results/h5-saved-placement-selection-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();plan=load(RUN/'plan.json');model=load(RUN/'model.json');result=load(RUN/'result.json');audit=load(RUN/'audit/checks.json');pool=load(RUN/'candidates.json');selected=load(RUN/'selected-indices.json');warm=load(RUN/'warm-indices.json')
    assert audit['complete'] and audit['selected_geometry_valid'] and not audit['public_original_job_valid']
    assert result['status']==1 and result['has_incumbent'] and result['missing']=={'cog':3} and result['selected_from']=='MILP incumbent'
    assert source_digest()==audit['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    origins=Counter(pool[i]['source']['kind'] for i in selected);overlap=len(set(selected)&set(warm))
    next_step=('The finite placement pool has been jointly selected and its full conflict graph independently '
        'checked. It still gives a 63/66 layout, missing three cogs. Do not repeat that pool, increase its '
        'solver allowance or present its reported dual bound as a global geometric proof. Its poses were '
        'generated mostly by the earlier limited beam, so joint selection does not cure missing contact '
        'locations. Next generate a materially different finite pose pool with original-outline contacts '
        'and sheet-boundary symmetry, including contact positions beyond the beam\'s three lowest choices. '
        'A 180-degree rotation of a candidate about its own target-sheet centre preserves this job\'s '
        'allowed free/quarter-turn rotations; verify each such transformed pose before adding it. '
        'Use the audited selected layout as an explicit feasible partial certificate, declare candidate '
        'and offline limits before running, and retain truncation, timeout and incomplete quantities. '
        'A complete original-stock, original-quantity witness is still required before any new runtime '
        'proposal or matched quality pilot. Native margins remain a separate qualification after physical '
        'geometry; never change reserved holes, material target, conversion guard, production budgets '
        'or the four-step repair cap.')
    review={'next_investigation':next_step,'selected_candidate_sources':dict(origins),'known_partial_candidates_retained':overlap,
        'reported_finite_pool_area_upper_bound_mm2':-result['mip_dual_bound']*model['required_total_area_mm2'],
        'bound_scope':'Uncertified HiGHS report for this finite discretization only; no global polygon feasibility or infeasibility claim.',
        'all_runtime_source_unchanged':True,'new_native_searches':0,'new_quality_runs':0,'production_digest':source_digest(),
        'readmes_unchanged':{p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']},'H5_complete':False,'completion_percent':60}
    write(OUT/'source-review.json',review);members=[]
    for p in sorted(RUN.rglob('*')):
        if p.is_file():members.append((p,'run/'+p.relative_to(RUN).as_posix()))
    for path,h in plan['sources'].items():
        p=ROOT/path;assert digest(p)==h;members.append((p,'source-inputs/'+p.relative_to(ROOT/'output').as_posix()))
    for name in ['select_h5_saved_placements.py','audit_h5_saved_placement_selection.py','construct_h5_pattern_layouts.py','diagnose_h5_concave_gaps.py']:
        members.append((ROOT/'output'/name,'helpers/'+name))
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p,name in members:
            assert '.claude' not in p.parts
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'model':model,'result':result,'audit':audit,
        'selected_candidate_origins':dict(origins),'known_partial_candidates_retained':overlap,'archive_members':len(manifest),'archive_sha256':digest(archive),
        'runtime_changed':False,'H5_complete':False,'completion_percent':60})
    shutil.copyfile(__file__,OUT/'seal_h5_saved_placement_selection.py')
    doc=f'''# H5: joint selection from saved placements — 2026-10-18

Joint selection finds an independently valid **63-part partial arrangement**, but
still leaves **three of the original 15 cogs unplaced**. No complete target witness
is found. This is a finite offline construction; production and H5 remain unchanged.

The [terminal diagnosis](h5-terminal-repair-diagnosis-20261018.md) showed local
repair trapped around a fixed frame block. This follow-up chooses compatible
placements together from the previously recorded geometry instead of placing
each part greedily. It uses the closest large-plates / 0.2 mm case with its
original stock, quantities, filled holes and 325.926902 mm second-sheet target.

The pool contains **2,614 unique placements**: 500 frames, 465 brackets, 137 inserts
and 1,512 cogs. Inputs include the known zero-native-loss partial, the in-bound
rejected terminal poses, all **25** previously generated frame configurations,
and individual members of **21,873** valid saved beam candidates. Compound members
become independently selectable, retaining their actual original transforms.
The 4,000-candidate cap is not reached; one out-of-stock terminal cog is excluded.
Deduplication rounds only identity keys, retaining unrounded original coordinates.

Actual filled-outer distances define **332,265 incompatible candidate pairs**.
A binary model selects at most each original family quantity, exactly all 18
frames, and at least the known partial's filled area, maximizing covered area.
The existing 63-part partial verifies as a feasible certificate for this exact
model before solving. No frame location is fixed by the selection constraints.

The solver reaches its declared 120-second limit after **121.329742 real seconds**
and returns an incumbent, with status **time limit reached**, not optimal. It
selects all 18 frames, 12 brackets and 21 inserts, plus 12 cogs: the same original
filled area as the known partial, **4,331,552.627256 mm²**. Only 24 of its 63 selected
candidate entries are from that known partial; the others come from the terminal,
frame catalog and beam. This is a newly selected arrangement, not a fallback.

The reported finite-model upper bound is **4,347,053.331371 mm²**, below the
4,481,740.784070 mm² required for all original parts. This is an uncertified solver
bound for these discrete choices, not a global geometric infeasibility result.
The time limit, missing inventory and lack of a complete witness remain explicit.

An independent audit reconstructs **every candidate's exact source provenance**,
rebuilds each original polygon with a separate matrix transform, and checks stock,
orientation and reflection requirements. It enumerates **2,700,951** same-sheet
candidate pairs, filters by an independently implemented bounding-box distance
bound, and evaluates **393,757** original-polygon distances. The resulting conflict
graph agrees exactly with all 332,265 recorded edges, without using the producer's
spatial-index query. All **1,303** selected-part pairs pass physical clearances;
the original public CLI rejects **only the missing cog quantity**.

[Checks](h5-saved-placement-selection-20261018/checks.json),
[raw pool, conflict graph, solve, sources and audits](h5-saved-placement-selection-20261018/raw.zip),
[manifest](h5-saved-placement-selection-20261018/raw-manifest.json),
[next investigation](h5-saved-placement-selection-20261018/source-review.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.

{next_step}

No native packing search, quality pilot, runtime change or release qualification
is performed. Published preview assets and all three accurate READMEs remain
unchanged. H2/H5 stay open at **60%**.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 joint saved-placement selection, 2026-10-18:** [a finite binary construction](../benchmarks/results/h5-saved-placement-selection-20261018.md)
selects among 2,614 original-outline poses, including all 25 prior frame
configurations. The known 63-part partial certifies model feasibility; all frame
locations are selectable. The 120-second solve ends at its limit with a different
63-part arrangement, still missing three cogs. An independent reconstruction
enumerates 2,700,951 candidate pairs and verifies the exact 332,265-edge conflict
graph; all 1,303 selected-part pairs pass, and the original CLI rejects only the
missing quantity. The solver's finite-pool bound is recorded without a global
infeasibility claim. Preserve the timeout and generate new contact positions
before any further selection attempt; no unchanged-pool or native search repeat.
Production, targets, limits, release assets and accurate READMEs stay unchanged;
H2/H5 remain open at 60%.
'''
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==prior
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 terminal repair diagnosis, 2026-10-18:**';assert s.count(marker)==1
    p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n');append(ROOT/'.gitattributes','\nbenchmarks/results/h5-saved-placement-selection-20261018/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'missing':result['missing']}),flush=True)
if __name__=='__main__':main()
