"""Author and independently validate a mixed-dimension two-for-three exchange."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import copy,itertools,json,shutil,subprocess
from shapely.geometry import Polygon
import shapely
root=Path(__file__).resolve().parents[1];old=root/'benchmarks/results/h5-balanced-exchange-witness-20261017';out=root/'benchmarks/results/h5-mixed-exchange-witness-20261018';out.mkdir(exist_ok=False)
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
job=load(old/'job.json');before=load(old/'before.json');after=load(old/'balanced-after.json')
original=next(p for p in job['parts'] if p['id']=='incoming');job['parts']=[p for p in job['parts'] if p['id']!='incoming'];job['name']='Authored mixed-dimension two-to-three exchange'
for name,height in [('short-incoming',40),('tall-incoming',50)]:
    p=copy.deepcopy(original);p.update(id=name,quantity=1);p['geometry']=[{'outer':[[0,0],[30,0],[30,height],[0,height]],'holes':[]}];job['parts'].append(p)
for layout in [before,after]:
    for p in layout['placements']:
        if p['part_id']=='incoming':
            tall=p['copy_index']==1;p['part_id']='tall-incoming' if tall else 'short-incoming';p['copy_index']=0;p['transform']['translation']=[2,44 if tall else 2]
write(out/'job.json',job);write(out/'before.json',before);write(out/'mixed-after.json',after)
cli=root/'target/release/nestbolt.exe';expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
reports=[];geometry=[];parts={p['id']:p for p in job['parts']}
for name,layout in [('before',before),('mixed-after',after)]:
    command=[str(cli),'validate','--job',str(out/'job.json'),'--layout',str(out/(name+'.json'))]
    r=subprocess.run(command,capture_output=True,timeout=60)
    (out/(name+'-stdout.json')).write_bytes(r.stdout);(out/(name+'-stderr.log')).write_bytes(r.stderr);write(out/(name+'-command.json'),{'command':command,'exit_code':r.returncode})
    assert r.returncode==0,(name,r.stderr);report=json.loads(r.stdout);assert report['valid'];reports.append(report)
    assert Counter(p['part_id'] for p in layout['placements'])==Counter({p['id']:p['quantity'] for p in job['parts']})
    assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==7
    sheets={};stock=Polygon([(1,1),(99,1),(99,99),(1,99)])
    for p in layout['placements']:
        t=p['transform'];assert t['rotation_radians']==0 and not t['mirrored'];part=parts[p['part_id']]
        assert part['rotations']=={'kind':'list','degrees':[0]} and not part['allow_mirror']
        shape=Polygon([(x+t['translation'][0],y+t['translation'][1]) for x,y in part['geometry'][0]['outer']]);assert shape.is_valid and stock.covers(shape)
        sheets.setdefault(p['sheet_id'],[]).append(shape)
    pairs=[(a,b) for rows in sheets.values() for a,b in itertools.combinations(rows,2)]
    assert all(a.disjoint(b) and a.distance(b)>=job['clearance'] for a,b in pairs)
    geometry.append({'layout':name,'parts':7,'same_sheet_pairs':len(pairs),'minimum_clearance_mm':min(a.distance(b) for a,b in pairs),'inside_original_edge_inset':True})
assert reports[0]['metrics']==reports[1]['metrics'] and reports[0]['metrics']['material_area']==19700
bounds=[]
for chosen,other in [(40,50),(50,40)]:
    for returned in range(4):
        receiver=chosen+(3-returned)*30;source=other+returned*30
        assert receiver>98 or source>98
        bounds.append({'incoming_height':chosen,'returned_squares':returned,'receiver_height_lower_bound':receiver,'source_height_lower_bound':source,'cannot_fit_both_98mm_heights':True})
assert 40+50+.2<=98 and 30*3+.2*2<=98
checks={'authored_only':True,'optimizer_runs':0,'CLI_validation_runs':2,'both_layouts_valid':True,'all_metrics_identical':True,'parts':7,'material_mm2':19700,'incoming_dimensions_mm':[[30,40],[30,50]],'incoming_group_area_mm2':2700,'returned_group_area_mm2':2700,'scope':'Selected incoming parts are the distinct 30x40 and 30x50 rectangles. Returned parts are three 30x30 squares. One 60x94 filler stays on each sheet; all rotations are zero and mirrors disabled.','usable_width_and_height':98,'combined_side_space':38,'combined_top_bottom_space':4,'single_incoming_bounds':bounds,'bound_ignores_positive_clearance_conservatively':True,'filler_exact_positions_not_required_by_bound':True,'does_not_rule_out_other_part_selections_or_global_layouts':True,'independent_geometry':geometry,'shapely_version':shapely.__version__,'mechanical_applicability_proven':False,'production_changed':False,'H5_complete':False,'cli_sha256':expected}
write(out/'checks.json',checks);shutil.copyfile(__file__,out/'check.py');assert digest(cli)==expected
files={p.name:{'sha256':digest(p),'bytes':p.stat().st_size} for p in out.iterdir() if p.is_file()};write(out/'integrity.json',{'members':files,'all_hashes_verified':all(digest(out/n)==r['sha256'] for n,r in files.items())})
doc='''# Mixed-dimension exchange witness — 2026-10-18

Two distinct incoming rectangles, **30 × 40 mm and 30 × 50 mm**, can trade
places with three 30 × 30 mm squares. A 60 × 94 mm filler remains on each
100 × 100 mm sheet. Both authored layouts independently validate, contain
all seven parts, and use exactly 19,700 mm2 of charged material. The exchange
preserves 2,700 mm2 of incoming/returned area. It is a useful assignment change
without immediate material reduction, so the existing changed-inventory
nonincrease rule should continue to allow it.

The frozen public CLI checks both layouts. Shapely separately verifies every
filled outer ring, pair spacing, edge inset and quantity. Rotations are fixed
to zero and mirroring is disabled. No optimizer or performance run occurs.

With one filler on each sheet, the remaining combined side width is 38 mm,
less than the 60 mm needed for two lanes of these 30 mm wide parts. The total
space above and below the filler is only 4 mm, less than every small part's
height. Therefore the small parts must stack in one side lane, whose usable
height cannot exceed 98 mm, even if the filler moves. For either chosen
incoming rectangle and each possible return count from zero to three, at
least one sheet's height sum exceeds 98 mm, ignoring positive clearance
conservatively. All eight explicit bounds are in [checks](h5-mixed-exchange-witness-20261018/checks.json).

The paired height sums are 90.2 mm for the two rectangles and 90.4 mm for
the three squares, including 0.2 mm spacing; the authored coordinates fit.
The current same-original-item pair selector cannot select the two distinct
incoming parts together. A new mixed-pair candidate still needs an actual
regression against that runtime, allowed-pose/rollback checks, and the
unchanged paired quality comparison.

This restricted assignment witness does not rule out other selected parts
or global layouts, prove usefulness on the mechanical jobs, or meet H5.
Original failures and the full 13-job material/cutting requirements remain.
H2/H5 stay open at 60% completed weight.
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:f.write('\nbenchmarks/results/h5-mixed-exchange-witness-20261018/** -text -whitespace\n')
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:f.write('''

## 2026-10-18 — Author a mixed-dimension exchange witness

[Two distinct rectangles can replace three squares](benchmarks/results/h5-mixed-exchange-witness-20261018.md)
while retaining all seven parts and exactly 19,700 mm2 charged material.
The 30x40 and 30x50 mm incoming rectangles together equal the three 30x30 mm
returns' 2,700 mm2 area. Frozen CLI and independent Shapely checks validate
both layouts. Eight conservative height bounds rule out single chosen
incoming moves while one filler remains on each sheet, even if it moves.

This is an authored assignment witness, not an optimizer result, a global
impossibility claim or evidence of mechanical quality. A mixed-pair candidate
still needs a failing original-runtime regression, complete correctness
checks and the unchanged quality gates. No production change or H5 credit;
H2/H5 remain open at 60%.
''')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'both_layouts_valid':True,'material_mm2':19700,'incoming_dimensions':[[30,40],[30,50]],'single_assignment_bounds':len(bounds),'optimizer_runs':0}))
