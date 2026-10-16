"""Report already-verified diagnostic evidence after the retained formatting error."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json, shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'benchmarks/results/h5-exchange-diagnosis-20261016'
SEQ=ROOT/'output/depth-diagnosis-sequence-20261016'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
v=load(OUT/'verification.json');r=load(OUT/'results.json');traces=load(OUT/'rechecked-traces.json');inventory=load(OUT/'snapshot-integrity.json')
assert v['all_archives_and_members_verified'] and v['trace_counters_recomputed']
assert len(v['records'])==4 and all(x['valid'] for x in v['records']) and traces['all_trace_counts_match']
assert inventory['crc_and_every_member_verified'] and digest(OUT/'snapshots.zip')==inventory['sha256']
for p in SEQ.iterdir():
    if p.is_file():
        target=OUT/'sequence'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
shutil.copyfile(ROOT/'output/continue_depth_diagnosis.py',OUT/'sequence/continue.py')
shutil.copyfile(__file__,OUT/'report.py')
write(OUT/'report-format-failure.json',{'helper':'finish-rechecked.py','after_verification_and_snapshot_archive':True,'error':"TypeError: bad operand type for unary +: 'str'",'line':90,'effect':'The saved-artifact verification and snapshot archive completed; Markdown construction failed. This report-only helper reads those completed artifacts; no search, validation or archive is repeated.'})
groups=Counter()
for row in traces['records']:
    for t in row['diagnosis']['traces']:
        for a in t['attempts']:groups[(a['outcome'],a['blockers'])]+=1
write(OUT/'observed-stages.json',{'total_outcomes':v['total_outcomes'],'by_outcome_and_blocker_count':[{'outcome':o,'blockers':b,'count':n} for (o,b),n in sorted(groups.items())],'scope':'Observed stages only; no quality comparison or geometric-impossibility claim'})
lines=['# Directed-exchange repair-stage diagnosis — 2026-10-16','',
'**All four diagnostic layouts validate.** The saved traces identify observed failure stages.',
'They do not establish material or speed improvement. The earlier failed pilot remains unchanged.','',
'The [committed plan](h5-exchange-diagnosis-20261016/plan.json) fixes both mechanical',
'jobs, both kerfs, seed 0, 60 seconds and serial physical CCD0 CPU 8. It starts',
'after the H4 tree-depth pilot finishes and is sealed. The isolated observer',
'preserves the rejected algorithm and adds one aggregate trace per invocation.',
'Tracing can perturb deadlines; no quality comparison is claimed.','',
'| Job | Kerf mm | Invocations | Attempted exchanges | Recorded outcomes |',
'| --- | ---: | ---: | ---: | --- |']
for row in v['records']:
    outcomes=', '.join(f'{k}: {n}' for k,n in sorted(row['outcomes'].items())) or 'none'
    lines.append(f"| {row['job']} | {row['kerf_mm']} | {row['invocations']} | {row['attempts']} | {outcomes} |")
lines+=['','All attempt-level areas, blocker counts and repair losses remain in the',
'[rechecked traces](h5-exchange-diagnosis-20261016/rechecked-traces.json), with',
'original stderr in immutable per-attempt archives. Trace counts agree with',
'the saved solver statistics. Independent original-geometry/public validation,',
'all requested quantities, zero hole riders and public exports pass. The entire',
f"diagnostic session took {r['wall_seconds']/60:.3f} minutes.",'',
'## Retained reporting failures','',
'The original trace reader failed on two omitted `directed_exchanges` fields.',
'The source explicitly omits zero-valued counters. The corrected reader supplies',
'zero only under that serialization rule and checks the same saved traces.',
'The original `results.json` and both errors are retained unchanged; no search',
'was repeated. After archive verification succeeded, a separate Markdown',
'construction error interrupted the first corrected finisher. Its source and',
'failure record remain; this report reads the already verified artifacts.','',
'[Verification](h5-exchange-diagnosis-20261016/verification.json),',
'[stage aggregation](h5-exchange-diagnosis-20261016/observed-stages.json),',
'[original sequence failure](h5-exchange-diagnosis-20261016/sequence/interruption.json),',
'[report-format failure](h5-exchange-diagnosis-20261016/report-format-failure.json).','',
'CRC, every archive/member hash and source/binary/input guards pass. The observed',
'failures locate a repair stage; they do not prove geometric impossibility or',
'justify increasing budgets. Inspect proposal geometry before choosing a further',
'changed experiment. No candidate is integrated. H5 remains open; completion is 45%.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
write(SEQ/'reviewed-completion.json',{'h4_passed_pilot':True,'h5_all_layouts_valid':True,'h5_trace_counts_rechecked':True,'original_sequence_interruption_retained':True,'original_results_unchanged':True,'recovery':'Saved-output reader supplies explicitly omitted zero counters; separate report-only formatting correction; no search repeated','verification_sha256':digest(OUT/'verification.json'),'trace_sha256':digest(OUT/'rechecked-traces.json'),'report_sha256':digest(OUT.parent/(OUT.name+'.md'))})
shutil.copyfile(SEQ/'reviewed-completion.json',OUT/'sequence/reviewed-completion.json')
print(json.dumps({'valid':4,'outcomes':v['total_outcomes'],'groups':[{'outcome':o,'blockers':b,'count':n} for (o,b),n in sorted(groups.items())]}))
