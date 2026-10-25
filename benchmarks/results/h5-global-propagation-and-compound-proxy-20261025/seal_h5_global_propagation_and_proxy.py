"""Seal two distinct bounded global investigations, retaining unresolved outcomes."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-global-propagation-and-compound-proxy-20261025';OUT=ROOT/'benchmarks/results'/NAME
PROP=ROOT/'output/h5-global-packing-propagation-20261025';PROXY=ROOT/'output/h5-compound-cog-proxy-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    pa=load(PROP/'audit/checks.json');pm=load(PROP/'solve/model-audit.json');pr=load(PROP/'solve/result.json');pb=load(PROP/'baseline-audit/checks.json');ca=load(PROXY/'audit/checks.json');cm=load(PROXY/'solve/model-audit.json');cr=load(PROXY/'solve/result.json');cb=load(PROXY/'baseline-audit/checks.json');prior=load(ROOT/'benchmarks/results/h5-guarded-core-and-global-relaxation-20261025/source-review.json');assert all(v['passed'] for v in [pa,pm,pb,ca,cm,cb]);assert pr['status']==cr['status']=='UNKNOWN';assert pr['solver_calls']==cr['solver_calls']==1 and not pr['incumbents'] and not cr['incumbents'];assert not(PROP/'solve/relaxed-positions.json').exists() and not(PROXY/'solve/relaxed-positions.json').exists()
    for root,at in [(PROP,'1.75'),(PROXY,'0.13')]:
        log=(root/'solve/solver.log').read_text(encoding='utf-8');assert f'Starting search at {at}s' in log and 'status: UNKNOWN' in log;assert not re.findall(r'^#Done',log,re.M)
    correction=load(PROXY/'baseline-audit/metadata-correction.json');assert digest(PROXY/'baseline-audit/checks-original.json')==correction['original_checks_sha256'] and digest(PROXY/'baseline-audit/checks.json')==correction['corrected_checks_sha256'];assert cb['same_part_bracket_pairs']==10 and cb['same_part_cog_pairs']==150
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head.startswith('bf8daa5b') and mainhead.startswith('8f941426');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());ci=json.loads(subprocess.check_output(['gh','run','view','40229962984','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==mainhead
    action='Both global searches remain UNKNOWN; do not retry them unchanged, raise limits or interpret the smaller proxy as original geometry. Before another call, audit exact orientation aliases: frame and insert quarter-turn/reflection modes may share identical normalized components and stock domains, but every original orientation must retain an explicit equivalent representative and reconstruction map. Do not merge bracket modes merely because bounding boxes agree. Independently map the original66-part production layout into the all-movable model as possible source-derived hints: certify its quantities, provenance, transforms, proxy relations and stock violations against the target; retain every omitted or out-of-domain hint with its reason. Hints must never fix placements or reduce quantities. Review whether this verified data and exact alias reduction offer a materially different, bounded construction test; declare the scope and sole call before execution, retaining every prior UNKNOWN. Any positive proxy arrangement requires the larger disk/polygon conditions and original cog-outline/angle diagnosis, followed by original clearance/native guards, material target, production budget and the complete13-job/two-kerf H5 matrix. H2 stays open as instructed; do not open22 reserved vectors or repeat its denominator question. Push the committed evidence normally once the existing main CI run is terminal; no diagnostic result qualifies a new release.'
    OUT.mkdir();write(OUT/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    for root,prefix in [(PROP,'propagation'),(PROXY,'compound')]:
        for rel,name in [('plan.json','plan.json'),('generation.json','generation.json'),('audit/checks.json','geometry-audit.json'),('solve/model-audit.json','model-audit.json'),('solve/plan.json','model-plan.json'),('solve/result.json','solver.json'),('baseline-audit/checks.json','baseline-audit.json')]:shutil.copyfile(root/rel,OUT/f'{prefix}-{name}')
    shutil.copyfile(PROXY/'baseline-audit/metadata-correction.json',OUT/'baseline-metadata-correction.json');write(OUT/'main-ci.json',ci);write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':2,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'next_investigation':action})
    members={};inputs={}
    for root in [PROP,PROXY]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(PROP/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    helpers=['prepare_h5_global_propagation.py','audit_h5_global_propagation_geometry.py','prepare_h5_global_propagation_solver.py','h5_global_propagation_encoding.py','solve_h5_global_propagation.py','solve_h5_global_disks.py','audit_h5_global_propagation_baseline.py','prepare_h5_compound_cog_proxy.py','audit_h5_compound_cog_proxy.py','prepare_h5_compound_proxy_solver.py','solve_h5_compound_proxy.py','h5_compound_proxy_encoding.py','prepare_h5_compound_baseline_audit.py','audit_h5_compound_proxy_baseline.py','correct_h5_compound_baseline_metadata.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/n for n in helpers];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'original_area_and_sheet_capacities_audited':True,'all_inner_components_cover_floor_error_square':True,'both_complete_models_independently_verified':True,'two_distinct_models_one_call_each':True,'both_results_unknown_without_incumbents':True,'no_unrestricted_infeasibility_claim':True,'both_original64_part_sanity_checks_only':True,'metadata_label_correction_preserves_original':True,'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: global packing propagation and compound cog proxy — 2026-10-25

**Both new all-parts-movable searches remain `UNKNOWN`, with no incumbent.**
The first adds independently checked global constraints to the prior polygon
relaxation. The second uses a much smaller, weaker inner-rectangle model to
seek an arrangement for diagnosis. Neither result proves the original target
impossible or supplies an accepted layout. H2/H5 remain open at **60%**.

## Original area and floor-safe components

Independent exact-rational triangulation rechecks the four original filled
outer areas, retaining the holes-reserved rule. The 66 parts total
**4,481,740.784069745 mm²**. Flooring individual areas to 0.001 mm² yields
4,481,740,770 integer area units; the original usable sheet capacities round
outward to **4,441,669,000** and **465,322,304** units. Assignment of original
part areas must fit each sheet, including full cog areas even where a smaller
geometric proxy represents the cogs. These are necessary area conditions,
not material acceptance from a proxy.

Each original non-cog rectangle component is inset by 0.01 mm on every edge
after its anchor is floored to a 0.01 mm grid. Checking the four corners of the
entire floor-error square proves every inset rectangle remains inside every
corresponding original component. The audit covers all 24 orientation/component
cases with 96 error-corner checks. The bracket's own components are disjoint
and remain coupled to one position and orientation.

Each cog initially adds one centered square with half-width **77.14 mm**.
All 16 square-vertex/error-square combinations lie strictly inside the already
certified all-angle disk of radius 109.1157 mm. This gives 78 inner rectangles
for 66 parts. The two per-sheet NoOverlap2D constraints and four orthogonal
cumulative profiles therefore hold for every valid original arrangement.
Profile capacities are rounded outward from the original usable dimensions.
All original sheet/orientation modes and the material-height target remain.

Construction takes 0.010154 seconds and independent geometry auditing takes
0.115529 seconds. Eight source files match committed evidence. The inherited
continuous polygon geometry remains byte-identical to the earlier audit.

## Strengthened polygon model

The first model retains all earlier polygon/rectangle separating relations and
adds the original-area bounds and global inner-rectangle constraints. Every
field of **31,935 variables and 37,849 constraints** is independently rebuilt,
including 312 optional intervals, both NoOverlap2D constraints, all four
cumulative profiles, two area bounds and unchanged exact counts. Construction
takes 1.039861 seconds and encoding audit 0.321061 seconds, within the declared
120-second caps. Every template change and dependency hash is recorded.

One declared 60-second, eight-worker, seed-zero call starts search at
1.75 seconds and returns **`UNKNOWN` in {pr['seconds']:.6f} seconds**. It has
163,993 branches, 2,786 conflicts and no incumbent. The solver's small soft-limit
overrun is retained. This call is not resumed, extended or repeated.

The preserved original 64-part layout satisfies all new conditions: 74 inner
rectangles, 1,908 same-sheet rectangle-pair checks, including ten same-part
bracket pairs, both original-area bounds and four complete sweep profiles.
It still lacks two brackets and is never treated as a 66-part solution or hint.

## Smaller compound cog model

Earlier rectangle models used finite recipes containing fixed cog groups.
This new model gives every original part its own movable anchor. Each cog is
represented by five coupled, mutually disjoint rectangles: a central square
and four side pieces. The audit checks all **80** vertex/error-square combinations
against the certified disk and all ten within-cog component pairs for
nonoverlap. Their total area is **31,699.5264 mm² per cog**. The original cog's
larger filled area is still charged to its assigned sheet.

This different necessary relaxation omits the pairwise polygon/rectangle
separation disjunctions and uses global constraints on all **138** inner
rectangles. It may admit overlap of the larger cog disks, full outlines or
non-inset part boundaries; a positive outcome would only be a starting point
for diagnosis. It preserves all 66 mandatory parts, permitted non-cog
orientations, both original stock domains and the target material height.
There is no fixed frame/cog arrangement, hint or partial-inventory objective.

Every field of the resulting **1,806 variables and 2,824 constraints** is
independently checked, including 552 optional intervals and all original-area
and global propagation constraints. The metadata's zero explicit physical-pair
count denotes removed pairwise disjunctions; global NoOverlap2D still covers
every pair of inner rectangles on each sheet, including components of one cog.
Construction takes 0.039590 seconds and encoding audit 0.024321 seconds.

One separate declared 60-second call starts search at 0.13 seconds and returns
**`UNKNOWN` in {cr['seconds']:.6f} seconds**, with 122,429 branches, 97,083
conflicts and no incumbent. A smaller encoding has not supplied an arrangement
within this bounded call. It is not an infeasibility proof, and no original
outline/native validation is manufactured from an absent solution.

The same preserved 64-part sanity check now has 134 inner rectangles and all
6,186 same-sheet pairs pass, together with both area bounds and four complete
profiles. Its 160 within-part pairs comprise ten bracket and 150 cog pairs.
The copied audit initially labelled that total as bracket pairs; an independent
recount corrects the metadata while preserving the original checks, correction
hashes and unchanged geometric evidence. No search or audit was rerun.

## Next step and repository state

{action}

Engine source, all three accurate READMEs and releases remain unchanged.
Main 8f941426's existing hosted run is captured as `{ci['status']}` /
`{ci['conclusion'] or 'pending'}`; four newer evidence commits remain local at
source head {head[:8]} while it finishes, avoiding cancellation by a new push.
No native packing, production-budget run, full H5 matrix or held-out evaluation
occurs here. Evidence-only changes do not require repeating production tests.

Evidence: [propagation plan]({NAME}/propagation-plan.json),
[geometry proof]({NAME}/propagation-geometry-audit.json),
[complete model audit]({NAME}/propagation-model-audit.json),
[bounded result]({NAME}/propagation-solver.json),
[compound plan]({NAME}/compound-plan.json),
[compound geometry]({NAME}/compound-geometry-audit.json),
[compound model]({NAME}/compound-model-audit.json),
[compound result]({NAME}/compound-solver.json),
[source review]({NAME}/source-review.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases retain exact bytes with
CRC and SHA-256 checks, including complete models, logs, templates and audits.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 global packing propagation and compound proxies, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) independently verifies original
filled-area bounds, outward sheet capacities and floor-safe inner rectangles
for every part. Adding two global NoOverlap2D and four cumulative constraints
to the all-movable polygon model yields 31,935 variables/37,849 constraints,
fully audited. One bounded call remains UNKNOWN in 60.188312 seconds. A distinct
smaller model replaces pairwise polygon disjunctions with five disjoint inner
rectangles per cog, preserving full original-area charges and all66 counts.
Its 1,806 variables/2,824 constraints also audit completely; one call remains
UNKNOWN in 60.176534 seconds. Neither search returns an incumbent or proof.
Both original64-part sanity checks pass the new conditions but still miss two
brackets. Next audit exact orientation aliases and source-derived, nonbinding
hints before considering a different bounded construction test. All original
limits, native checks and H5 matrix requirements remain. Source, accurate
READMEs and releases are unchanged; H2/H5 stay open at 60%.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
