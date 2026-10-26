"""Seal the exact strip-capacity obstruction and preserved-original exchange."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-second-strip-capacity-and-insert-exchange-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'free_model':'h5-three-free-brackets-model-20261026','free_search':'h5-three-free-brackets-search-20261026','strip_source':'h5-second-strip-four-cogs-source-20261026','strip_probes':'h5-second-strip-four-cogs-probes-20261026','band_data':'h5-second-strip-band-capacity-20261026','band_model':'h5-second-strip-band-model-20261026','band_search':'h5-second-strip-band-search-20261026','dual':'h5-second-strip-band-dual-20261026','continuous':'h5-second-strip-continuous-capacity-20261026','exchange':'h5-insert36-cog53-exchange-20261026','review':'h5-second-strip-final-review-20261026','queue':'h5-thirteen-part-checkpoint-queue-20261026'}
base={k:ROOT/'output'/v for k,v in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='4817fefff0739e7d92a15cf0e710b6d29d6c51dc' and review['main_head']=='c22d3e39e315b040b3afc694acae3e1beca685f8';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
    audits=[('free_model','audit/checks.json'),('free_search','search-audit/checks.json'),('strip_source','audit/checks.json'),('strip_probes','model-audit/checks.json'),('strip_probes','response-audit/checks.json'),('band_data','audit/checks.json'),('band_model','audit/checks.json'),('band_search','audit/checks.json'),('dual','certificate-audit/checks.json'),('continuous','checks.json'),('exchange','checks.json')];assert len(audits)==11 and all(load(base[k]/n)['passed'] for k,n in audits);free=load(base['free_search']/'search-audit/checks.json');strip=load(base['strip_probes']/'response-audit/checks.json');band=load(base['band_search']/'audit/checks.json');dual=load(base['dual']/'result.json');continuous=load(base['continuous']/'checks.json');exchange=load(base['exchange']/'checks.json')
    assert free['terminal_status']=='UNKNOWN' and free['shared_budget_honored'] and strip['unknown_patterns']==3 and strip['shared_budget_honored'] and band['terminal_status']=='INFEASIBLE' and band['shared_budget_honored'] and dual['exact_candidate_positive'] and continuous['strict_integer_margin']==84052628 and exchange['all66_originals_accounted_for'];OUT.mkdir()
    for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
    copies=[('free_model','result.json','free-bracket-model.json'),('free_model','audit/free-brackets.json','free-bracket-domain-counts.json'),('free_search','shared-search/solve/result.json','free-bracket-result.json'),('strip_source','result.json','four-cog-source.json'),('strip_probes','inventory.json','strip-model-inventory.json'),('strip_probes','search/census.json','strip-search-results.json'),('band_data','result.json','band-coefficient-summary.json'),('band_data','audit/implication.json','band-model-implication.json'),('band_model','result.json','band-model.json'),('band_search','result.json','band-search-result.json'),('band_search','audit/pattern-implication.json','closed-strip-implication.json'),('dual','result.json','dual-search-result.json'),('dual','certificate-audit/certificate.json','integer-band-certificate.json'),('continuous','certificate.json','continuous-band-certificate.json'),('continuous','coverage.json','continuous-cell-coverage.json'),('exchange','replacement-insert.json','insert36-replacement.json'),('exchange','first-sheet-placements.json','verified-first-sheet55.json'),('exchange','mandatory-second-sheet-originals.json','mandatory-second-sheet9.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-c22d3e39-snapshot.json'),('queue','queue.json','prior-checkpoint-queue.json')]
    for k,n,dest in copies:shutil.copyfile(base[k]/n,OUT/dest)
    write(OUT/'closed-calls.json',{'cp_sat_calls':5,'lp_certificate_calls':1,'three_free_bracket_source':{'status':'UNKNOWN','solver_seconds':free['actual_solver_seconds'],'shared_seconds':free['actual_shared_seconds'],'soft_overrun_seconds':free['solver_soft_limit_overshoot_seconds']},'three_strip_patterns':load(base['strip_probes']/'search/census.json'),'strip_shared_seconds':strip['actual_shared_seconds'],'band_capacity':load(base['band_search']/'result.json'),'band_shared_seconds':band['actual_shared_seconds'],'lp_certificate_search':dual,'lp_shared_seconds':load(base['dual']/'process.json')['seconds'],'all_calls_closed':True,'all_shared_budgets_honored':True})
    next_action=('All five CP-SAT calls and the one LP certificate search are CLOSED. Preserve the full13-mover three-free-bracket source UNKNOWN and all three ten-part strip UNKNOWNs; do not retry, reseed or extend them. A new exact horizontal-band certificate independently excludes the four-bracket/two-insert/four-cog short-sheet composition at the current cog angle, including all bracket quarter-turn/mirror and both insert profiles. The certificate is extended to all continuous source-profile anchors in the full usable stock; its positive integer margin84052628 does not rely on grid, extra stock guard or solver status. It does not exclude other cog angles, compositions or the whole66-part job. Next pursue the verified insert36/cog53 exchange: insert36 now has a checked first-sheet pose strictly inside the removed cog53 outline, and the complete55-original first-sheet partial passes1485pairs/220edges. All originals remain mandatory. The new second-sheet inventory is originals21/22/25/26/37/53/63/64/65 (four brackets,one insert,four cogs); originals28/29 are still missing and required. Before any new coordinate call, adapt the audited673-variable band model to this distinct composition by changing only the insert count from2 to1 and its per-cell variable upper bounds from2 to1. Preserve every exact coefficient and63 capacity constraint; independently audit full restoration of the prior model and identity accounting through the exchange. One separately bounded necessary allocation call may follow. A positive allocation is not packing: use its bracket/insert profile counts and vertical cell positions to inform a fresh nine-original whole-strip source model, all coordinates free with hints only, and every guarded pair clause. Reuse unchanged source profile/collision geometry only after independent byte/provenance and inventory audits; the old ten-part count obstruction and old fixed-pose capacity must not transfer. Check any nine-part witness against full originals and native guards before combining with first55; this still leaves28/29 and complete66/native/material validation, production integration and the full13-job/two-kerf H5 matrix. Mainc22d3e39 CI40270374068 has five passed jobs and Windows still live at05:15UTC;4817feff and this checkpoint should be pushed normally once terminal checks and fresh ancestry allow. H2 original gate remains open and22reserved vectors untouched.')
    write(OUT/'next-step.json',{'action':next_action,'next_necessary_parent':base['band_model'].relative_to(ROOT).as_posix(),'original_exchange_evidence':base['exchange'].relative_to(ROOT).as_posix(),'mandatory_second_sheet_originals':[21,22,25,26,37,53,63,64,65],'next_counts':{'bracket':4,'insert':1,'cog':4},'other_missing_required_originals':[28,29],'next_call_opened':False,'H5_complete':False})
    members={};inputs={}
    for folder in base.values():
        for p in folder.rglob('*'):
            if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
        for p in folder.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h,n
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026','h5-conditional-selection-and-partial64-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpers=list((ROOT/'output').glob('*second_strip*.py'))+list((ROOT/'output').glob('*three_free_brackets*.py'))+[ROOT/'output'/n for n in ['audit_h5_insert36_cog53_exchange.py','record_h5_thirteen_part_checkpoint_queue.py','pack_h5_evidence_archive.py','ccd1.py']]+[Path(__file__)];seen=set()
    while helpers:
        p=helpers.pop()
        if p in seen:continue
        seen.add(p);assert p.is_file();members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
        for n in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",s):
            q=ROOT/'output'/n
            if q.is_file():helpers.append(q)
        for node in ast.walk(ast.parse(s)):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():helpers.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members);write(OUT/'checks.json',{'passed':True,'independent_audits_passed':11,'closed_cp_sat_calls':5,'closed_lp_certificate_calls':1,'all_shared_budgets_honored':True,'historical_coordinate_unknowns_retained':4,'exact_continuous_source_profile_capacity_certificate':True,'strict_integer_capacity_margin':84052628,'verified_first_sheet_exchange_originals':55,'new_second_sheet_originals_still_required':9,'other_missing_originals_still_required':[28,29],'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: short-sheet capacity and original insert exchange — 2026-10-26

**An exact weighted-area certificate excludes four brackets, two inserts and
four cogs on the short second sheet at the current cog angle. It covers
continuous positions and every bracket quarter-turn/mirror profile. A distinct
insert/cog exchange is verified on the first sheet and supplies the next
composition to test. H2/H5 remain open at 60%; no full target is claimed.**

## Retained coordinate searches

The full 53-fixed source is retained with all three brackets free across their
2,471 domains each, ten verified non-bracket domain memberships, all 26 free
coordinates, all 954 pair modes and 60 advisory hints. Whole-parent restoration
and import pass for **270,671 variables / 351,286 constraints**. Its sole call
is **UNKNOWN**, taking **46.744881 solver / 49.837429 shared seconds**. The
1.744881-second soft overrun is recorded; the 60-second shared limit passes.

To test moving one more cog onto the second sheet, release all old poses there
and require originals21/22/25/26/36/37/53/63/64/65: four brackets, two inserts
and four cogs. Three declared orientation patterns cover vertical bracket
pairs, horizontal opposite pairs and horizontal mirrored corners. All ten
parts remain mandatory, with 20 free coordinates and every one of 45 pairs.

Independent geometry reconstruction checks eight used original profiles, all
26 raw collision cases from **8,340 unmerged triangle-pair hulls**, 305 guarded
faces and 13,854 exact outside planes. Minimum raw-to-guarded separation is
0.2126 mm, above the required 0.211709 mm. Eighteen unchanged cases are reused
with provenance; eight new cases include the zero-degree insert.

All three complete coordinate models and solver imports pass independent
reconstruction. Each separate 12-second call returns UNKNOWN. Their shared
time is **37.193644 seconds**, with soft overruns **0.045521 / 0.113807 /
0.103892 seconds**. These calls remain closed and their historical UNKNOWN
results are preserved.

## Exact necessary capacity and continuous certificate

A different necessary model ignores horizontal positions and pair collisions.
It retains the exact family counts and all eight bracket profiles, both insert
orientations and the recorded cog angle. Every integer vertical anchor belongs
to one of **673** disjoint cells. For each cell and each of **63 horizontal
bands**, compute the exact minimum filled-outer area over all continuous
positions within the cell. Rational polygon slice integration includes every
vertex breakpoint and quadratic stationary point. A separate edge-integral
audit recomputes **42,399 coefficients** and verifies complete cell coverage.

The aggregate model has **673 count variables / 66 constraints**: three exact
family sums and 63 stock-band capacities. Its single call is **INFEASIBLE in
0.104902 solver / 0.809784 shared seconds**. An implication audit maps all
three earlier coordinate patterns into this necessary model without dropping
an original. This excludes those patterns while retaining their original logs.

A separately declared LP call proposes seven weighted bands. Its result is
used only to find a certificate. Independent integer arithmetic checks every
cell inequality, yielding a strict demand/capacity contradiction. The proof
then extends every cell by **0.014 mm** and verifies coverage of all continuous
anchors in the entire usable stock, including the previously excluded margins.
Moving a polygon vertically by this amount changes its area in any band by at
most its bounding width times 0.014 mm; exact conservative losses account for
that change.

After those losses, mandatory weighted demand is **7,526,487,628**, exceeding
weighted stock capacity **7,442,435,000** by **84,052,628 integer units**
(83.968659 mm² under the normalized weights). This verified contradiction
depends on neither solver status, the micrometre grid nor the extra stock
guard. Its scope remains these counts and the recorded cog angle; other cog
angles, compositions and the complete 66-part job are not excluded.

## A preserved-original exchange

Move insert36 from the second sheet to the center of first-sheet cog53's old
pose, then require cog53 in the next second-sheet search. The original
180 × 110 mm insert fits strictly inside the removed original cog outline,
with **3.641264 mm** to its boundary. All original cutouts are retained.

The resulting **55-original first-sheet partial** passes every one of
**1,485 original pairs and 220 stock edges**, retaining 67 cutouts and 6,908
hole vertices. Minimum pair gap is 0.2125 mm. The next second-sheet inventory
is **21/22/25/26/37/53/63/64/65**: four brackets, one insert and four cogs.
It has not been packed. Originals28/29 remain missing and mandatory; every
one of the 66 original identities is accounted for across these obligations.

Next adapt only the necessary band's insert count and corresponding count
variable bounds from two to one, auditing complete parent restoration and the
exchange identities before one new bounded call. A positive allocation may
guide a fresh nine-original coordinate construction, with all coordinates
free and every original pair clause. It is not itself a layout. Complete
original/native/material validation, production integration and the full H5
matrix remain required.

## Repository and evidence

At {review['utc']}, main **c22d3e39** has five passed checks and Windows remains
live in [CI40270374068](https://github.com/skulitom/Nestbolt/actions/runs/40270374068).
The prior checkpoint4817feff is queued. Preserve that run before the next normal
push. Production, READMEs, upstream heads/releases and 22 reserved H2 vectors
are unchanged; no new release is qualified.

All **five CP-SAT calls and one LP certificate call are closed**, with all
shared budgets honored. [Checks]({NAME}/checks.json),
[continuous certificate]({NAME}/continuous-band-certificate.json),
[verified exchange]({NAME}/exchange-checks.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}** aliases
are size/SHA-256/CRC verified across **{archive['archive_parts']}** archive parts.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 short-sheet capacity and insert exchange, 2026-10-26:** [the evidence]({link})
retains the three-free-bracket source call and three whole-strip calls as
UNKNOWN, with all soft overruns recorded and all shared budgets honored.
A new necessary band model independently verifies 42,399 exact area bounds
over 673 vertical cells and 63 bands, then returns INFEASIBLE. An independently
checked integer certificate extends to continuous positions in the whole usable
stock and excludes four brackets, two inserts and four cogs at the current cog
angle; other compositions, cog angles and the full job remain open. Its strict
adjusted margin is 84,052,628 weighted integer units. A distinct exchange places
insert36 inside cog53's old first-sheet outline with 3.641264 mm clearance to
that outline; all 55 retained first-sheet originals pass 1,485 pairs and 220
stock edges. Next test four brackets, one insert and four cogs on the second
sheet, keeping all nine originals mandatory; originals28/29 also remain required.
All five CP-SAT and one LP certificate calls are closed. Main c22d3e39 has five
checks passed and Windows live at 05:15 UTC; checkpoint4817feff is queued.
H2/H5 stay open at 60%; production, READMEs, releases and all 22 reserved vectors
are unchanged. No full target layout or new release is claimed.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
