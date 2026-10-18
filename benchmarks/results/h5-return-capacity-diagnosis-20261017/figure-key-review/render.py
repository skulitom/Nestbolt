"""Plot the first attempted return assignment in each completed diagnostic case."""
from pathlib import Path
from hashlib import sha256
import json,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-return-capacity-diagnosis-20261017'
results=json.loads((out/'results.json').read_bytes());figures=[]
assert results['all_valid']
for record in results['records']:
    indexed=[(t,a) for t in record['diagnosis']['traces'] for a in t['attempts']]
    if not indexed:continue
    trace,attempt=indexed[0];context=trace['contexts'][attempt['context_index']]
    existing={p['key'] for p in context['source_after_removal']['items']}
    fig,axes=plt.subplots(1,2,figsize=(8,8),layout='constrained')
    for ax,name in zip(axes,['source_initial','source_repaired']):
        value=attempt[name]
        if value is None:ax.set_title('Repair not reached');continue
        ax.add_patch(Polygon(value['container'],facecolor='none',edgecolor='black',linewidth=1.4))
        for item in value['items']:
            returned=item['key'] not in existing
            ax.add_patch(Polygon(item['polygon'],facecolor='#ed8e25' if returned else '#6996bd',alpha=.28,edgecolor='#b65300' if returned else '#154f7d',linewidth=.6))
        ax.autoscale_view();ax.set_aspect('equal');ax.set_xlabel('Search-frame x (mm)');ax.set_ylabel('Search-frame y (mm)')
        ax.set_title('Initial return positions' if name=='source_initial' else 'Best returned repair snapshot')
    fig.suptitle(record['job']+' / '+str(record['kerf_mm'])+' mm kerf\nFirst attempted exchange only; orange = returned parts\nDiagnostic geometry, not a quality comparison',fontsize=10)
    path=out/(record['job']+'-'+str(record['kerf_mm']).replace('.','p')+'-first-attempt.png')
    fig.savefig(path,dpi=140);plt.close(fig)
    figures.append({'path':path.name,'sha256':sha256(path.read_bytes()).hexdigest(),'archive':record['archive'],'selection':'first attempted exchange','outcome':attempt['outcome']})
(out/'figures.json').write_text(json.dumps({'figures':figures,'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'visualization_only':True},indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'render.py')
print(json.dumps({'figures':len(figures)}))
