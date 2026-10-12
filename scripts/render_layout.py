"""Render a polygon job's layout (validator job and layout JSON) to a PNG: one
colour per part type, holes left open, sheets stacked. Used for README and
results images.
"""
import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402

PALETTE = ['#7fb069', '#d9534f', '#4a90c2', '#e07b39', '#9b72b0', '#e8c547', '#5bb5a2', '#c77d9c']


def signed_area(points):
    return sum(points[i][0] * points[(i + 1) % len(points)][1] - points[(i + 1) % len(points)][0] * points[i][1]
               for i in range(len(points)))


def render(job, layout, out, landscape=False, dpi=100):
    parts = {p['id']: p for p in job['parts']}
    colours = {p['id']: PALETTE[i % len(PALETTE)] for i, p in enumerate(job['parts'])}
    stocks = {s['id']: s for s in job['stocks']}
    sheets = layout['sheets']
    first = stocks[sheets[0]['stock_id']]
    w, h = (first['height'], first['width']) if landscape else (first['width'], first['height'])
    fig, axes = plt.subplots(len(sheets), 1, figsize=(14, 14 * h / w * len(sheets)), squeeze=False)
    for ax, sheet in zip(axes[:, 0], sheets):
        stock = stocks[sheet['stock_id']]
        width = stock['width']
        frame = (lambda x, y: (y, width - x)) if landscape else (lambda x, y: (x, y))
        sw, sh = (stock['height'], stock['width']) if landscape else (stock['width'], stock['height'])
        ax.add_patch(plt.Rectangle((0, 0), sw, sh, facecolor='#f3eee3', edgecolor='#555', lw=1.2))
        for pl in layout['placements']:
            if pl['sheet_id'] != sheet['id']:
                continue
            t = pl['transform']
            c, s = math.cos(t['rotation_radians']), math.sin(t['rotation_radians'])
            for g in parts[pl['part_id']]['geometry']:
                verts, codes = [], []
                for k, ring in enumerate([g['outer'], *g['holes']]):
                    pts = []
                    for x, y in ring:
                        x = -x if t['mirrored'] else x
                        pts.append(frame(x * c - y * s + t['translation'][0], x * s + y * c + t['translation'][1]))
                    # Outer rings counter-clockwise, holes clockwise, so holes stay open.
                    if (signed_area(pts) > 0) != (k == 0):
                        pts.reverse()
                    verts += pts + [pts[0]]
                    codes += [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 1) + [MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts, codes), facecolor=colours[pl['part_id']],
                                       edgecolor='#222', lw=0.4, alpha=0.92))
        ax.set_xlim(-0.005 * sw, 1.005 * sw)
        ax.set_ylim(-0.005 * sh, 1.005 * sh)
        ax.set_aspect('equal')
        ax.axis('off')
    plt.subplots_adjust(0, 0, 1, 1)
    plt.savefig(out, dpi=dpi, facecolor='white')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job', type=Path)
    parser.add_argument('layout', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--landscape', action='store_true', help='turn portrait sheets a quarter turn')
    args = parser.parse_args()
    render(json.loads(args.job.read_text(encoding='utf-8')), json.loads(args.layout.read_text(encoding='utf-8')),
           args.out, args.landscape)
    print(args.out)


if __name__ == '__main__':
    main()
