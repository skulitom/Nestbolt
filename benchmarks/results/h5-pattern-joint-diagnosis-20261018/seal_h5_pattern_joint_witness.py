"""Publish the bounded failed repair diagnosis and preserve all input, build and audit failures."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'output/h5-pattern-joint-probe-20261018'
OUT=ROOT/'benchmarks/results/h5-pattern-joint-diagnosis-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();audit=load(RAW/'audit-verified/checks.json');native=load(RAW/'native-runs/checks.json');plan=load(RAW/'native-plan.json')
    assert audit['all_stated_scope_checks_passed'] and native['complete']
    assert native['successes']==0 and audit['complete_target_layouts']==0
    assert len(audit['cases'])==4 and all(c['expired']==1 and c['failed']==0 and not c['success'] for c in audit['cases'])
    assert all(c['wall_seconds']<60 for c in audit['cases'])
    assert source_digest()==plan['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    ci=load(RAW/'main-ci-912cd5b.json');assert ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==prior
    followup=('Do not integrate this offline constructor or rerun the quality pilot. First export the exact native '
        'inflated polygons, container bounds and per-item collision partners for the already-saved partials, without '
        'calling separation. Independently compare native vertices with the original transformed outer contours, '
        'decompose pair and static losses, and distinguish the known conversion margins from any transform or '
        'observer mismatch. The partial layouts have only 0.0011 mm added part clearance, while conversion_guard '
        'is 0.011444091796875 mm for large plates and 0.0095367431640625 mm for panel hardware. This makes '
        'margin-driven collisions plausible, but the current aggregate losses alone do not prove their sole cause. '
        'Only after that diagnosis should a native-compatible initial construction be considered, retaining the '
        'original physical geometry, conversion guard, containers, quantities and target. The helper does not return '
        'a failed best snapshot here, so no final overlap or distance-to-feasibility claim is supported. Original '
        'budgets, four-step cap, hole reservation, thresholds and reserved-input isolation remain unchanged.')
    review={'followup':followup,'all_runtime_source_unchanged':True,'all_prior_171_tests_unchanged':True,
        'native_calls':4,'native_work_allowance_each':12.0,'native_seed':0,'serial_cpu':[8],
        'successful_repairs':0,'expired_repairs':4,'new_quality_runs':0,'H5_complete':False,
        'guard_is_only_cause_proven':False,'geometric_infeasibility_proven':False,
        'readme_sha256':{p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']},
        'native_binary_sha256':digest(RAW/'native-tests.exe'),'production_digest':source_digest()}
    write(OUT/'source-review.json',review)
    for name in ['recover_h5_partial_joint_inputs.py','prepare_h5_pattern_joint_witness.py','build_h5_pattern_joint_witness.py',
        'recover_h5_pattern_joint_build.py','run_h5_pattern_joint_witness.py','audit_h5_pattern_joint_witness.py',
        'recover_h5_pattern_joint_audit.py','audit_h5_pattern_joint_witness_recovery.py','recover_h5_pattern_joint_zero_stats.py',
        'audit_h5_pattern_joint_witness_complete.py','finish_h5_pattern_joint_audit.py','audit_h5_pattern_joint_witness_verified.py']:
        p=RAW/'helpers'/name;p.parent.mkdir(exist_ok=True);assert not p.exists();shutil.copyfile(ROOT/'output'/name,p)
    members=[]
    for p in sorted(RAW.iterdir()):
        if p.is_file() and p.name!='native-tests.exe':members.append((p,'raw/'+p.name))
    for name in ['inputs','native-runs','audit','audit-recovery','audit-complete','audit-verified','helpers']:
        for p in sorted((RAW/name).rglob('*')):
            if p.is_file():members.append((p,'raw/'+p.relative_to(RAW).as_posix()))
    # Full source of the compiled diagnostic, plus the failed appended test,
    # permits reproduction without including generated targets or executables.
    for entry in plan['source_files']:
        p=RAW/'candidate-recovery'/entry['path'];members.append((p,'source/'+entry['path']))
    members.append((RAW/'candidate'/plan['changed_file'],'failed-source/'+plan['changed_file']))
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p,name in members:
            assert '.claude' not in p.parts
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    assert len({r['path'] for r in manifest})==len(manifest)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={r['path'] for r in manifest}
        for r in manifest:assert sha256(z.read(r['path'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    summary={**audit,'verified_utc':datetime.now(timezone.utc).isoformat(),'native_calls':4,'expired_repairs':4,
        'work_budget_each':12.0,'seed':0,'native_cpu':[8],'sampled_provisional_scores':sum(c['scored_poses_checked'] for c in audit['cases']),
        'input_geometry_pairs':sum(c['partial']['pairs']+c['proposal']['pairs'] for c in audit['cases']),
        'selected_insertion_score_pairs':sum(c['selected_score_pairs'] for c in audit['cases']),
        'raw_archive_sha256':digest(archive),'raw_members':len(manifest),'completion_percent':60}
    write(OUT/'checks.json',summary);shutil.copyfile(RAW/'main-ci-912cd5b.json',OUT/'main-ci-912cd5b.json')
    shutil.copyfile(__file__,OUT/'seal_h5_pattern_joint_witness.py')
    rows=[]
    for c in audit['cases']:
        label=c['case'].removeprefix('m-mechanical-').removesuffix('-s0-candidate')
        loss=c['native_loss_observations'];affected=sum(p['items_with_loss'] for p in loss[0]['per_sheet'])
        placed=sum(c['partial']['counts'].values());requested=sum(c['proposal']['counts'].values())
        rows.append(f"| {label} | {placed}/{requested} | {c['inserted_parts']} | {affected}/{placed} | {loss[0]['joined_pinned_loss']:,.3f} | {loss[1]['joined_pinned_loss']:,.3f} | expired |")
    doc=f'''# H5: joint repair of saved partial constructions — 2026-10-18

Four deliberately overlapping complete proposals call the existing native joint
repair helper once each. **All four expire; none returns a complete target layout.**
This is a mechanism diagnosis, not a new quality comparison or evidence of geometric
infeasibility. H2/H5 remain open at 60%.

The [previous independent construction](h5-outline-construction-20261018.md)
provided physically legal partial layouts. Every original pose is preserved in
the new inputs. Missing original copies are restored using the original allowed
rotations/reflections: free parts sample 15-degree angles; positions come from an
11×11 legal translation grid and alignments with neighbours. All **308,326** scores
are saved, and the selected lexicographic minima are independently checked.
The original public library/request validator rejects all four complete proposals
only for overlap/clearance, including the aggregate `total_overlap` code.

The native observer measures each saved partial before calling repair, using a
separate clock and no separation. Every placed part already has positive native
collision loss. These loss values are internal scores, **not overlap areas**.

| Saved case | Partial inventory | Restored copies | Partial items with native loss | Partial joined loss | Complete proposal loss | Repair |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

Each actual helper call keeps seed 0, the pre-existing authored allowance of 12
work seconds, the exact target containers (rounded down to f32) and the original
conversion guard. Runs are serial on logical CPU 8 (CCD0). They stop at 12.009–12.057
charged seconds due to the existing work-check granularity; actual process times
are 13.505–18.899 seconds, below the 60-second hard limit. No budget, four-step
runtime cap or quality gate changes. Expiry returns no repaired layout, so the
failed internal best placements and final losses are unavailable from this helper.

Independent filled-outer checks cover **32,527** original partial/proposal pairs
and **5,395** selected-insertion comparisons. All missing quantities are restored,
all original partial poses remain exact, and both target stock bounds hold.
The complete proposals' overlaps are retained and never counted as valid results.
The native JSON echoes are also checked with original coordinates and unchanged
geometry tolerances.

The initial input checker omitted the expected aggregate overlap code; its first
proposal and all scores were reused unchanged. The first native build failed
because the appended test tried to clone a non-Clone report; a fresh isolated
source and target fix only that test initializer. The audit initially assumed
exact cross-language float equality and explicit zero counters. Native JSON
echoes have one-ULP differences (at most 4.55×10⁻¹³), and the declared serializer
omits zero counters. Every difference is enumerated and bounded to one ULP;
original files and target values remain authoritative. Three audit failures and
the intermediate generator's predicate-name error are preserved. **No search or
native repair was repeated during these corrections.** Runtime source and all
171 prior test bodies remain exact. The diagnostic itself passes four times by
correctly recording four failed repairs.

All {len(manifest)} archived files, CRCs and SHA-256 digests verify. The archive
includes the compiled diagnostic's source, failed source, inputs, logs, outputs
and auditors; the binary is retained locally and identified by SHA-256.

[Checks](h5-pattern-joint-diagnosis-20261018/checks.json),
[raw evidence and source](h5-pattern-joint-diagnosis-20261018/raw.zip),
[manifest](h5-pattern-joint-diagnosis-20261018/raw-manifest.json),
[source review](h5-pattern-joint-diagnosis-20261018/source-review.json).

{followup}

[All six hosted jobs on preceding main `912cd5b` pass](h5-pattern-joint-diagnosis-20261018/main-ci-912cd5b.json),
including Windows, Linux, browser tests and maker rebuilds. This confirms that
specific checkpoint, not subsequent commits. Production, v0.2.0-alpha.1 release
assets and the accurate English/Japanese/Chinese READMEs remain unchanged.
There is no newly qualified release candidate.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 saved-partial joint repair, 2026-10-18:** [four bounded native attempts](../benchmarks/results/h5-pattern-joint-diagnosis-20261018.md)
restore every missing original copy in explicit overlapping proposals; all original
partial poses remain exact. All four existing helper calls expire under seed 0
and their original 12-work-second diagnostic allowance, producing no complete
target layout. Every physically legal partial part already has positive native
collision loss. Next inspect exact native polygons and collision partners before
attributing this solely to conversion margins or designing another construction.
Rankings of all 308,326 recorded scores are checked; independent geometry checks
cover 32,527 original pairs and 5,395 selected-insertion comparisons. Input/build/audit harness failures remain
preserved; no native repair or quality run was repeated. Runtime, guard, budgets,
thresholds and release assets are unchanged; H2/H5 remain open at 60%.
'''
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';text=p.read_text(encoding='utf-8');marker='**N4 actual-outline construction, 2026-10-18:**'
    assert text.count(marker)==1;text=text.replace(marker,note+'\n'+marker)
    text=text.replace('confirms the test-only correction; the separate Windows workflow checks are\nstill pending.',
        'confirms the test-only correction; the separate Windows checks have since passed.\n[All six jobs on subsequent main 912cd5b also pass](../benchmarks/results/h5-pattern-joint-diagnosis-20261018/main-ci-912cd5b.json).')
    text=text.replace('with four skips, two workers and zero retries; hosted confirmation is pending.',
        'with four skips, two workers and zero retries; hosted confirmation is recorded above.')
    p.write_text(text,encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-pattern-joint-diagnosis-20261018/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'native_calls':4,'expired':4,'complete_layouts':0,'raw_members':len(manifest),
        'archive_bytes':archive.stat().st_size,'production_unchanged':True}),flush=True)
if __name__=='__main__':main()
