"""Transpose the authored witness to preserve the validator's used-height metric."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'output/check_h5_area_witness.py').read_text(encoding='utf-8')
replacements=[
    ('h5-area-witness-20261017','h5-area-witness-height-20261017'),
    ("rect('filler',60,94)","rect('filler',94,60)"),
    ("rect('incoming',30,85)","rect('incoming',85,30)"),
    ("placement('return',i,0,64,2+32*i)","placement('return',i,0,2+32*i,64)"),
    ("p['transform']['translation']=[64,2]","p['transform']['translation']=[2,64]"),
    ("p['transform']['translation']=[2,2+32*p['copy_index']]","p['transform']['translation']=[2+32*p['copy_index'],2]"),
]
for before,after in replacements:
    assert source.count(before)==1,before
    source=source.replace(before,after)
exec(compile(source,__file__,'exec'))
