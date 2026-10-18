from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/finish_h5_exact_state.py').read_text(encoding='utf-8').replace('h5_exact_state','h5_frontier_observer').replace('h5-exact-state','h5-frontier-observer')
start=s.index('accepted=[a for a in attempts')
s=s[:start]+'''summary={'attempts':len(attempts),'outcomes':dict(Counter(a['outcome'] for a in attempts)),
    'paired_attempts':sum(len(a['incoming'])==2 for a in attempts),
    'mixed_attempts':sum(len(set(a['incoming']))==2 for a in attempts),
    'quality_claim':False,'earlier_pilot_trajectory_reconstructed':False}
write(out/'observed-exchanges.json',{'summary':summary,'observations':observations,'attempts':attempts})
write(out/'verification.json',{'all_original_archives_verified':True,'all_traces_verified':True,
    'archives':archives,'valid':2,'actual_exchange_attempts':len(attempts),'unchanged_source_binary_input_guards':True,
    'original_job_metrics_and_quantities_verified':True,'H5_complete':False,'integrated':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'finish.py')
print(json.dumps(summary))
'''
path=root/'output/finish_h5_frontier_observer.py';compile(s,str(path),'exec');path.write_text(s,encoding='utf-8',newline='\n')
print('Prepared retained-archive and counter verification.')
