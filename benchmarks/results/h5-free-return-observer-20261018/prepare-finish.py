"""Reuse archive and baseline geometry audits, extending file identities to four cases."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def adapt(s):return s.replace('h5-exchange-failure-observer','h5-free-return-observer').replace('h5_exchange_failure_observer','h5_free_return_observer')
s=adapt((root/'output/finish_h5_exchange_failure_observer.py').read_text(encoding='utf-8'))
start=s.index("try:cmd=psutil.Process(");end=s.index("assert result['guards_unchanged']",start)
s=s[:start]+"pid_check=runner.prior.require_runner_stopped(opened,'h5_free_return_observer.py')\n"+s[end:]
s=s.replace("len(result['records'])==2", "len(result['records'])==4").replace("'archives':archives,'valid':2", "'process_identity_check':pid_check,'archives':archives,'valid':4")
s=s.replace("['traces','attempt_rows']", "['traces','attempt_rows','attempt_observations']")
p=root/'output/finish_h5_free_return_observer.py';compile(s,str(p),'exec');p.write_text(s,encoding='utf-8',newline='\n')
s=adapt((root/'output/check_h5_exchange_failure_observer_layouts.py').read_text(encoding='utf-8'))
s=s.replace('folder/f"k{row[\'kerf_mm\']}-i{invocation}"','folder/f"{row[\'job\']}-k{row[\'kerf_mm\']}-i{invocation}"')
s=s.replace("record={'kerf_mm':row['kerf_mm']", "record={'job':row['job'],'kerf_mm':row['kerf_mm']")
p=root/'output/check_h5_free_return_observer_layouts.py';compile(s,str(p),'exec');p.write_text(s,encoding='utf-8',newline='\n')
print('Prepared unchanged archive/baseline audits, qualified process identity check, and distinct four-case paths.')
