"""Independently validate a larger-return-area pair swap without optimizer runs."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import itertools,json,shutil,subprocess
from shapely.geometry import Polygon
import shapely
root=Path(__file__).resolve().parents[1]
old=root/'benchmarks/results/h5-mixed-exchange-witness-20261018'
out=root/'benchmarks/results/h5-larger-return-witness-20261018';out.mkdir(exist_ok=False)
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
job=load(old/'job.json');before=load(old/'before.json');after=load(old/'mixed-after.json')
job['name']='Authored mixed pair with larger returned area'
returned=next(p for p in job['parts'] if p['id']=='return')
returned['geometry']=[{'outer':[[0,0],[30,0],[30,31],[0,31]],'holes':[]}]
for layout in [before,after]:
    for p in layout['placements']:
        if p['part_id']=='return':p['transform']['translation']=[2,[2,33.5,65][p['copy_index']]]
write(out/'job.json',job);write(out/'before.json',before);write(out/'larger-return-after.json',after)
cli=root/'target/release/nestbolt.exe'
expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
reports=[];geometry=[];parts={p['id']:p for p in job['parts']}
for name,layout in [('before',before),('larger-return-after',after)]:
    command=[str(cli),'validate','--job',str(out/'job.json'),'--layout',str(out/(name+'.json'))]
    r=subprocess.run(command,capture_output=True,timeout=60)
    (out/(name+'-stdout.json')).write_bytes(r.stdout);(out/(name+'-stderr.log')).write_bytes(r.stderr)
    write(out/(name+'-command.json'),{'command':command,'exit_code':r.returncode})
    assert r.returncode==0,(name,r.stderr)
    report=json.loads(r.stdout);assert report['valid'];reports.append(report)
    assert Counter(p['part_id'] for p in layout['placements'])==Counter({p['id']:p['quantity'] for p in job['parts']})
    assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==7
    sheets={};stock=Polygon([(1,1),(99,1),(99,99),(1,99)])
    for p in layout['placements']:
        t=p['transform'];assert t['rotation_radians']==0 and not t['mirrored']
        part=parts[p['part_id']];assert part['rotations']=={'kind':'list','degrees':[0]} and not part['allow_mirror']
        shape=Polygon([(x+t['translation'][0],y+t['translation'][1]) for x,y in part['geometry'][0]['outer']])
        assert shape.is_valid and stock.covers(shape)
        sheets.setdefault(p['sheet_id'],[]).append(shape)
    pairs=[(a,b) for rows in sheets.values() for a,b in itertools.combinations(rows,2)]
    assert all(a.disjoint(b) and a.distance(b)>=job['clearance'] for a,b in pairs)
    geometry.append({'layout':name,'parts':7,'same_sheet_pairs':len(pairs),'minimum_clearance_mm':min(a.distance(b) for a,b in pairs),'inside_original_edge_inset':True})
assert reports[0]['metrics']==reports[1]['metrics'] and reports[0]['metrics']['material_area']==19700
bounds=[]
for chosen,other in [(40,50),(50,40)]:
    for count in range(4):
        receiver=chosen+(3-count)*31;source=other+count*31
        assert receiver>98 or source>98
        bounds.append({'incoming_height':chosen,'returned_rectangles':count,'receiver_height_lower_bound':receiver,'source_height_lower_bound':source,'cannot_fit_both_98mm_heights':True})
incoming_area=30*(40+50);returned_area=30*31*3
assert returned_area>incoming_area and 40+50+.2<=98 and 31*3+.2*2<=98
assert 40+50+31>98
source=root/'output/h5-mixed-exchange-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs'
code=source.read_text(encoding='utf-8');fragment='        if area > incoming_area {\n            continue;\n        }';assert code.count(fragment)==1
checks={'authored_only':True,'optimizer_runs':0,'CLI_validation_runs':2,'both_layouts_valid':True,'all_metrics_identical':True,'parts':7,'material_mm2':19700,
    'incoming_dimensions_mm':[[30,40],[30,50]],'returned_dimensions_mm':[[30,31]]*3,
    'incoming_group_area_mm2':incoming_area,'returned_group_area_mm2':returned_area,'returned_area_increase_mm2':returned_area-incoming_area,
    'scope':'The selected distinct incoming rectangles move as one group and all three returned rectangles move back. A 60x94 filler stays on each sheet. All rotations are zero and mirrors disabled.',
    'usable_width_and_height':98,'combined_side_space':38,'combined_top_bottom_space':4,
    'single_incoming_bounds':bounds,'paired_with_one_return_left_height_lower_bound':121,
    'bound_ignores_positive_clearance_conservatively':True,'filler_exact_positions_not_required_by_bound':True,
    'does_not_rule_out_other_part_selections_or_global_layouts':True,'independent_geometry':geometry,'shapely_version':shapely.__version__,
    'mechanical_applicability_proven':False,'runtime_regression_test_executed':False,'production_changed':False,'H5_complete':False,'cli_sha256':expected,
    'current_filter_source':source.relative_to(root).as_posix(),'current_filter_source_sha256':digest(source),'current_filter_fragment':fragment,
    'current_filter_line':code[:code.index(fragment)].count('\n')+1}
write(out/'checks.json',checks);shutil.copyfile(__file__,out/'check.py');assert digest(cli)==expected
files={p.name:{'sha256':digest(p),'bytes':p.stat().st_size} for p in out.iterdir() if p.is_file()}
write(out/'integrity.json',{'members':files,'all_hashes_verified':all(digest(out/n)==r['sha256'] for n,r in files.items())})
doc='''# Pair exchange with larger returned area — 2026-10-18

Two incoming rectangles, 30x40 and 30x50 mm, can exchange with three 30x31 mm
rectangles while preserving all seven parts and exactly 19,700 mm2 charged
material. The returning group has **2,790 mm2**, exceeding the incoming
group's **2,700 mm2**. Both authored layouts pass the frozen public CLI and
independent filled-outer, spacing, edge and quantity checks. All metrics are
identical. No optimizer run occurs.

A 60x94 mm filler stays on each 100x100 mm sheet. With the one-millimetre edge
inset, at most 38 mm combined side width and 4 mm combined top/bottom height
remain around a filler. These 30 mm wide small parts therefore need one side
lane no higher than 98 mm, even if the filler moves. Either incoming part
moving alone, with any zero-to-three return count, makes a height sum exceed
98 mm on at least one sheet. All eight conservative bounds are recorded.
Moving both incoming parts needs 90.2 mm; the returns need 93.4 mm, including
the required 0.2 mm spacing. The authored coordinates satisfy both. Leaving
one return with the incoming pair would need at least 121 mm before spacing.

The current paired proposal rule rejects a complete return set when its area
exceeds incoming area. This witness shows that rule can exclude a valid
exchange with unchanged material. It does not show that allowing the exchange
improves a mechanical workload. An actual original-runtime regression and
complete candidate/quality checks remain necessary before any integration.
Whole-job geometry, quantity, pose and strict material guards must remain.

[Checks and conservative bounds](h5-larger-return-witness-20261018/checks.json),
[before](h5-larger-return-witness-20261018/before.json),
[after](h5-larger-return-witness-20261018/larger-return-after.json) and
[integrity](h5-larger-return-witness-20261018/integrity.json) retain all evidence.
This scoped witness makes no global infeasibility or H5 claim. Production and
reserved inputs are unchanged; completed milestone weight remains 60%.
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
print(json.dumps({'both_valid':True,'all_metrics_identical':True,'material':19700,'incoming_area':incoming_area,'returned_area':returned_area,'optimizer_runs':0}))
