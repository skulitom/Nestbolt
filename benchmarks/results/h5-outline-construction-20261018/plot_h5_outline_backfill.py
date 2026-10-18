from pathlib import Path
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'output/h5-outline-backfill-20261018/m-mechanical-large-plates-k0.2-s0-candidate'
load=lambda p:json.loads(p.read_bytes())
job=load(folder/'job.json');layout=load(folder/'layout.json');target=load(folder/'conditional-target.json');result=load(folder/'result.json')
parts={p['id']:p for p in job['parts']};stock=job['stocks'][0]
colors={'frame':'#8db8dc','cog':'#edb36b','bracket':'#86bda7','insert':'#baa3cf'}
heights=[stock['height'],target['required_used_height_mm']]
fig,axes=plt.subplots(2,1,figsize=(8,13),gridspec_kw={'height_ratios':heights},layout='constrained')
for i,ax in enumerate(axes):
    ax.set_xlim(0,stock['width']);ax.set_ylim(0,heights[i]);ax.set_aspect('equal');ax.set_facecolor('#fafafa')
    for p in layout['placements']:
        if p['sheet_id']!=f'sheet-{i}':continue
        t=p['transform'];c=math.cos(t['rotation_radians']);s=math.sin(t['rotation_radians']);pts=[]
        for x,y in parts[p['part_id']]['geometry'][0]['outer']:
            if t['mirrored']:x=-x
            pts.append((c*x-s*y+t['translation'][0],s*x+c*y+t['translation'][1]))
        ax.add_patch(Patch(pts,facecolor=colors[p['part_id']],edgecolor='#304050',linewidth=.4))
    ax.set_title(f"Sheet {i+1}: allowed height {heights[i]:.3f} mm",fontsize=10)
    ax.set_xlabel('mm');ax.set_ylabel('mm')
fig.suptitle('Saved construction: 63 of 66 parts placed\nThree cogs remain unplaced; holes stay reserved',fontsize=13)
fig.savefig(folder/'layout-map.png',dpi=130)
plt.close(fig)
print(folder/'layout-map.png')
