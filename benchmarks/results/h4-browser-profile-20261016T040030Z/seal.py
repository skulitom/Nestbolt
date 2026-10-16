"""Verify and preserve the completed current-build CPU profiles, no new search."""
from pathlib import Path
from hashlib import sha256
import json,shutil,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h4-browser-profile-20261016T040030Z'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(ROOT/'scripts'))
import h4_quality
plan=load(OUT/'plan.json');result=load(OUT/'results.json');aggregate=load(OUT/'aggregate.json')
assert result['guards_unchanged'] and len(result['rows'])==3
assert plan['guards']['product']=='c571ee083d17419941bbd36440c7ff859b5aab72b1bc4139d11a8443bf2fe208'
assert h4_quality.source_digest()==plan['guards']['product']
execution=load(OUT/'execution.json');assert execution['exit_code']==0 and not execution['affinity_deviations']
checked=[]
for row in result['rows']:
    folder=OUT/row['job'];validation=load(folder/'validate-stdout.json');saved=load(folder/'result.json');layout=load(folder/'layout.json')
    assert validation['valid'] and saved['validation']['valid'] and row['validation']['status']=='valid'
    assert h4_quality.equivalent(validation['metrics'],saved['validation']['metrics'])==0
    assert digest(folder/'layout.json')==row['validation']['layout_sha256']
    source=next(r for r in plan['jobs'] if r['id']==row['job'])
    assert len(layout['placements'])==sum(p['quantity'] for p in load(Path(source['path']))['parts'])
    if row['job']=='example-gears':
        public=load(folder/'public-validate-stdout.json');assert public['valid'] and h4_quality.equivalent(public['metrics'],validation['metrics'])==0
    a=next(r for r in aggregate if r['job']==row['job'])
    assert sum(r['seconds'] for r in a['all_self_functions'])-a['sampled_seconds']<1e-8
    checked.append({'job':row['job'],'layout_sha256':digest(folder/'layout.json'),'all_requested_parts':len(layout['placements']),'metrics_identical':True,'profile_sha256':digest(folder/'cpu.cpuprofile'),'profile_span_seconds':a['profile_span_seconds'],'sampled_seconds':a['sampled_seconds'],'unattributed_gap_seconds':a['unattributed_gap_seconds']})
for name,expected in plan['guards']['files'].items():
    source=ROOT/name;assert digest(source)==expected,name
    target=OUT/'snapshots'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for name in ['output/aggregate_current_h4_profiles.py','output/run_current_h4_profiles.py']:
    shutil.copyfile(ROOT/name,OUT/Path(name).name)
write(OUT/'verification.json',{'all_checks_pass':True,'candidate':'7eba929420d218d04169c1fdf24481051c8afae5','guarded_files_unchanged':True,'affinity_deviations':0,'rows':checked,'profile_only_not_quality_gate':True,'held_out_geometry_read':False,'H4_complete':False})
shutil.copyfile(__file__,OUT/'seal.py')
files=sorted(p for p in OUT.rglob('*') if p.is_file());archive=OUT/'raw.zip';assert not archive.exists()
inv={p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inv)
    for name,e in inv.items():
        raw=z.read(name);assert len(raw)==e['bytes'] and sha256(raw).hexdigest()==e['sha256']
write(OUT/'integrity.json',{'sha256':digest(archive),'bytes':archive.stat().st_size,'members':inv,'crc_and_every_member_verified':True})
# Remove only resolved in-folder duplicates whose exact bytes remain in the archive.
for name in [*[r['job'] for r in result['rows']],'snapshots']:
    target=(OUT/name).resolve();assert target!=OUT and target.is_relative_to(OUT.resolve())
    for p in target.rglob('*'):
        if p.is_file():assert digest(p)==inv[p.relative_to(OUT).as_posix()]['sha256']
    shutil.rmtree(target)
lines=['# Current preview CPU diagnosis — 2026-10-16','','**All three diagnostic layouts validate. Edge/quadtree traversal is the main sampled cost.**',
'These profiles investigate the failed preview; they are not a repeated quality',
'comparison or an H4 pass. No production code, settings or geometry changed.','',
'## Method','',
'Candidate `7eba929`, source digest `'+plan['guards']['product']+'`.',
'The [committed diagnostic plan](h4-current-profile-plan-20261016/plan.json) fixes',
'gear-1, sign-1 and example-gears, 60 seconds, seed 0, serial Chrome pages and',
'physical CCD0 CPU 8. CDP samples the same WASM entry point at 1 ms. Sampling and',
'main-page execution differ from the app-worker/G5 method; reported times are',
'diagnostic. Every original requested part and independent metric agrees,',
'including the public gears library/request. All guards pass with no affinity',
'deviation. The complete profiling process took '+f"{execution['wall_seconds']:.3f}"+' seconds.','',
'## Sampled costs','',
'All call nodes with the same function name are aggregated. Function shares refer',
'only to sampled time; complete profiles and all-function aggregation are retained.','',
'| Job | Span / sampled s | Edge collection | Edge/quadrant test | Bounding-box generation |',
'| --- | ---: | ---: | ---: | ---: |']
for a in aggregate:
    def share(test):return sum(r['percent_of_samples'] for r in a['all_self_functions'] if test(r['function']))
    edge=share(lambda n:'collect_collisions_until' in n and 'primitives::edge::Edge' in n and 'separate::Evaluator' in n)
    quadrant=share(lambda n:'collides_with_quadrants' in n and 'primitives::edge::Edge' in n)
    bbox=share(lambda n:'generate_bounding_box' in n)
    lines.append(f"| {a['job']} | {a['profile_span_seconds']:.6f} / {a['sampled_seconds']:.6f} | {edge:.3f}% | {quadrant:.3f}% | {bbox:.3f}% |")
lines += ['', 'The difference between profile span and sampled deltas is only 0.000144–0.000154 s',
'in these observations; the large missing-time interval in the earlier gear profile',
'is not present here. This does not establish a speed gain. Scoring still accounts',
'for 12.234% of sign-1 samples, but traversal is a larger target in all three jobs.','',
'The next hypothesis is a shallower collision-index configuration in an isolated',
'copy, retaining the original outlines and independent validation. Test one change',
'at a time; fewer tree visits could instead increase leaf work. No setting change',
'or improvement is established by profiling alone. Do not repeat rejected generic',
'SIMD/allocator trials or treat this diagnostic as a replacement quality result.','',
'[Verification]('+OUT.name+'/verification.json), [aggregation]('+OUT.name+'/aggregate.json),',
'[raw archive]('+OUT.name+'/raw.zip). The archive contains '+f'{len(inv):,}'+' members,',
f"{archive.stat().st_size:,} bytes, SHA-256 `{digest(archive)}`.",
'CRC, every member size and SHA-256 pass. Original source, bindings/WASM, validator,',
'input snapshots, profiles, layouts, validation output and runner remain retained.',
'H4 stays open; the preview remains unreleased and completion stays 45%.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'verified':3,'archive_sha256':digest(archive),'members':len(inv),'bytes':archive.stat().st_size}))
