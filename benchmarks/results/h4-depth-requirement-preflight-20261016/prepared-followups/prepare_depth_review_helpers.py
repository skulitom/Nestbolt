"""Adapt completed read-only reviews to the current candidate and distinct pilot."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def derive(source, destination, replacements):
    text = (root/source).read_text(encoding='utf-8')
    for before, after in replacements:
        assert before in text, before
        text = text.replace(before, after)
    target = root/destination
    assert not target.exists()
    compile(text, str(target), 'exec')
    target.write_text(text, encoding='utf-8', newline='\n')

derive('benchmarks/results/h4-requirement-preflight-20261016/verify.py',
       'output/verify_h4_depth_requirements.py', [
    ('h4-requirement-preflight-20261016', 'h4-depth-requirement-preflight-20261016'),
    ('h4-preview-score-release-20261016', 'h4-preview-depth-release-20261016'),
    ('h4-preview-score-scale-plan-20261016', 'h4-preview-depth-scale-plan-20261016'),
    ('h4-score-integration-20261016', 'h4-depth-integration-20261016'),
    ('7eba929', 'aba989e'),
    ('Local integration and all six hosted checks pass on the candidate',
     'Local integration passes; current hosted checks and downloaded-package verification remain pending'),
])

derive('output/finish_h5_early_exchange_pilot.py',
       'output/finish_h5_obstruction_set_pilot.py', [
    ('h5-early-exchange-pilot-20261016', 'h5-obstruction-set-pilot-20261016'),
    ('h5_early_exchange_pilot', 'h5_obstruction_set_pilot'),
    ('Early directed common-line exchange pilot', 'Atomic obstruction-set common-line exchange pilot'),
    ('[Committed early-call plan]', '[Committed obstruction-set plan]'),
    ("'obstruction on an earlier sheet, repairs both sheets, and accepts only after',",
     "'obstruction set of up to three parts on an earlier sheet, repairs both sheets,',\n    'and accepts only after',"),
    ("'The current 7eba929 baseline and candidate both include the finer score bound.',",
     "'Both matched arms include the current aba989e collision-tree depth change.',\n    'The candidate returns all actual blockers together when their combined area',\n    'is smaller, preserving relative transforms and the existing single-part',\n    'fallbacks. It changes neither budget nor coefficients. Production is unchanged.',"),
    ('h5-early-exchange-preparation-20261016.md', 'h5-obstruction-set-preparation-20261016.md'),
    ("'The [earlier late-call pilot](h5-exchange-pilot-v2-20261016.md) remains',\n    'preserved with 72 valid outcomes, four failed mechanical material pairs',\n    'and zero attempted exchanges. The targeted authored window test proves',\n    'early-call reachability; only this measured pilot establishes whether it',\n    'reaches useful proposals on these development jobs. No quality or material',",
     "'The [earlier single-blocker pilot](h5-early-exchange-pilot-20261016.md) remains',\n    'preserved with 72 valid outcomes, five failed material pairs and ten accepted',\n    'exchanges. Separate traces found 35 of 37 proposals fail receiver repair,',\n    'with two or three blockers in every attempt. Those traces locate an observed',\n    'failure stage; they do not establish infeasibility or a material benefit.',\n    'Only this distinct pilot evaluates the complete-group hypothesis on these',\n    'development jobs. No quality or material',"),
])

print('Prepared current H4 preflight and H5 original-archive verification; no measured search started.')
