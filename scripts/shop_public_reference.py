"""Prepare explicit compatibility inputs for the published N0 reference reader.

The unmodified package is still run on original source bytes separately. This
authoring-only adapter handles observed package omissions on native re-saves,
then the resulting vectors must be checked against native SVG exports. It is
not a Nestbolt reader and cannot author labels after the corpus freeze.
"""
from copy import deepcopy
import json
from math import cos, sin, pi
from pathlib import Path
import re
import xml.etree.ElementTree as E
import numpy as np
from shop_reference_labels import ROOT, CORPUS, write_json


def matrix(text):
    a,b,c,d,e,f=map(float,(text or '1 0 0 1 0 0').split())
    return np.array([[a,c,e],[b,d,f],[0,0,1]])


def matrix_text(m):
    return ' '.join(format(x,'.14g') for x in [m[0,0],m[1,0],m[0,1],m[1,1],m[0,2],m[1,2]])


def prepare():
    if (CORPUS/'manifest.json').exists(): raise ValueError('N0 authoring ended at freeze')
    source=ROOT/'output/shop-public-native';dest=source/'compatibility-inputs'
    dest.mkdir(parents=True,exist_ok=True)
    rows=json.loads((source/'collection.json').read_text(encoding='utf-8'))['rows']
    reports=[]
    for row in rows:
        root=E.parse(source/(row['id']+'.lbrn2')).getroot();changes=[]
        bitmap_data={s.get('SourceHash'):s.get('Data') for s in root.iter('Shape')
                     if s.get('Type')=='Bitmap' and s.get('Data')}
        def visit(parent, world=np.identity(3)):
            for index,shape in enumerate(list(parent)):
                if shape.tag!='Shape': continue
                kind=shape.get('Type'); own=matrix(shape.findtext('XForm'))
                if kind=='Text' and shape.find('BackupPath') is not None:
                    backup=deepcopy(shape.find('BackupPath'));backup.tag='Shape'
                    backup.set('CutIndex',shape.get('CutIndex','0'))
                    cache=matrix(backup.findtext('XForm'))
                    backup.find('XForm').text=matrix_text(cache)
                    parent.remove(shape);parent.insert(index,backup);shape=backup
                    changes.append('Text BackupPath promoted to Path with cached world coordinates preserved')
                    kind='Path'
                    own=None  # The native text cache is already in world coordinates.
                if kind=='Bitmap' and not shape.get('Data') and shape.get('SourceHash') in bitmap_data:
                    shape.set('Data',bitmap_data[shape.get('SourceHash')]);changes.append('Shared bitmap Data materialized by SourceHash')
                if kind=='Polygon':
                    # Native L07 SVG confirms the regular polygon's phase and
                    # ellipse scaling (N=6, Rx=57.380001, Ry=57.925541).
                    n=int(shape.get('N'));rx=float(shape.get('Rx'));ry=float(shape.get('Ry'))
                    shape.set('Type','Path')
                    for key in ['N','Rx','Ry']:shape.attrib.pop(key)
                    E.SubElement(shape,'VertList').text=''.join(f'V{rx*cos(2*pi*j/n):.14g} {ry*sin(2*pi*j/n):.14g}' for j in range(n))
                    E.SubElement(shape,'PrimList').text=''.join(f'L{j} {(j+1)%n}' for j in range(n))
                    changes.append('Regular Polygon expanded to its native-confirmed straight edges')
                prim=shape.find('PrimList');verts=shape.find('VertList')
                if prim is not None and (prim.text or '').strip() in ('LineOpen','LineClosed') and verts is not None:
                    n=len(re.findall('V',verts.text or ''));closed=prim.text.strip()=='LineClosed'
                    prim.text=''.join(f'L{j} {j+1}' for j in range(n-1))+(f'L{n-1} 0' if closed and n else '')
                    changes.append('Compact linear primitive run expanded to explicit L indices')
                if kind=='Group':
                    children=shape.find('Children')
                    if children is not None:visit(children,world@own)
                    shape.find('XForm').text='1 0 0 1 0 0'
                    changes.append('Group transforms composed into leaves; wrapper omitted at reference conversion to avoid repeated SVG y reflection')
                elif own is not None:
                    shape.find('XForm').text=matrix_text(world@own)
        visit(root)
        # The published parser resolves shared IDs after the defining run has
        # been expanded; no reference-reader code is copied or changed.
        (dest/(row['id']+'.lbrn2')).write_text(E.tostring(root,encoding='unicode',xml_declaration=True),encoding='utf-8',newline='\n')
        reports.append({'id':row['id'],'changes':changes})
    write_json(dest/'adapter-manifest.json',{'purpose':'N0 reference normalization only; must validate against native SVG','rows':reports})
    print('Prepared compatibility inputs:',len(reports))


if __name__=='__main__':prepare()
