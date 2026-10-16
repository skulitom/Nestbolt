"""Record the H4 preflight and refresh the narrowly defined competitor stop rule."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import base64
import json
import subprocess

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/competitor-stop-review-20261016'
out.mkdir(exist_ok=False)
commit_raw = subprocess.check_output(['gh','api','repos/JeroenGar/sparrow-studio/commits/main'], cwd=root)
commit = json.loads(commit_raw)
assert commit['sha'] == '2102a9a4ed8d78f4f5ad58bdef25a68fc7b96fe6'
documents = {}
for name in ['README.md', 'web/README.md', 'app/README.md']:
    response = json.loads(subprocess.check_output(['gh','api',
        'repos/JeroenGar/sparrow-studio/contents/'+name+'?ref='+commit['sha']], cwd=root))
    raw = base64.b64decode(response['content'])
    text = raw.decode('utf-8')
    documents[name] = {'url': 'https://github.com/JeroenGar/sparrow-studio/blob/'+commit['sha']+'/'+name,
                       'sha256': sha256(raw).hexdigest(), 'bytes':len(raw)}
    if name == 'README.md':
        assert 'not published yet' in text and '`web/`' in text and '`app/`' in text
    if name == 'web/README.md':
        assert 'Other parts cannot nest inside holes.' in text
    if name == 'app/README.md':
        assert 'until this one launches' in text
review = {'checked_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Availability/documentation check only; no new competitor measurements or code reuse.',
    'repository_head': commit['sha'], 'commit_utc':commit['commit']['committer']['date'],
    'commit_message':commit['commit']['message'], 'documents':documents,
    'published_site': {'url':'https://sparrowstudio.app/',
        'finding':'The published description explicitly excludes allocation across multiple fixed sheets and placing parts inside holes.'},
    'redesign_status':'The repository documents a separate app redesign that is not published yet; the existing web app remains deployed.',
    'stop_rule_triggered':False,
    'decision':'Continue: no shipped fixed-sheet allocation or part-in-part support is established. The unpublished redesign is not evidence of shipment.',
    'pinned_dependencies_or_existing_comparisons_changed':False,
    'checked_with':'Official site and README pages opened through web browsing; commit and exact README bytes verified through the GitHub API.'}
(out/'review.json').write_text(json.dumps(review,indent=2)+'\n', encoding='utf-8', newline='\n')
(out/'record.py').write_bytes(Path(__file__).read_bytes())

path = root/'docs/RELEASE_READINESS.md'
text = path.read_text(encoding='utf-8')
before = '  and site remain frozen through the sequence. Then finish the H4 requirement review.'
assert before in text
text = text.replace(before, '  and site remain frozen through the sequence. The [requirement preflight](../benchmarks/results/h4-requirement-preflight-20261016.md)\n  verifies the declared job set and actual unshared WASM memory. Finish the\n  requirement review after all measured outcomes are available.')
path.write_text(text, encoding='utf-8', newline='\n')
with (root/'docs/V1_1_RESEARCH.md').open('a', encoding='utf-8', newline='\n') as stream:
    stream.write('''

### 2026-10-16: competitor shipment check before the preview

The [published Sparrow Studio description](https://sparrowstudio.app/) still
explicitly excludes automatic allocation across multiple fixed sheets and
placing parts inside holes. Its [repository README](https://github.com/JeroenGar/sparrow-studio/blob/2102a9a4ed8d78f4f5ad58bdef25a68fc7b96fe6/README.md)
now distinguishes the deployed `web/` app from a separate, unpublished redesign.
The new app's Sheets tab does not establish a shipped fixed-sheet solver.
[Exact commit/README hashes and the review](../benchmarks/results/competitor-stop-review-20261016/review.json)
record this distinction. The plan's shipment stop rule is not triggered. This
availability check changes no dependency, frozen competitor result or README
comparison claim; it is not a new benchmark.
''')
with (root/'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as stream:
    stream.write('''

## 2026-10-16 — H4 requirement preflight and competitor shipment review

[The requirement preflight](benchmarks/results/h4-requirement-preflight-20261016.md)
verifies the exact eleven declared cases, 65-job development scope, budgets,
seeds, physical cores and current scale guards. Parsing the measured WASM
binary confirms one defined, unshared memory and no imported memory. Its
SHA-256 matches the integrated candidate. Actual browser quality/scale outcomes
remain pending; no partial result closes H4 or changes the 45% completion weight.

[The current competitor shipment review](benchmarks/results/competitor-stop-review-20261016/review.json)
confirms that Sparrow Studio's published description still excludes automatic
fixed-sheet allocation and nesting inside holes. The repository's redesigned
app is explicitly unpublished. Exact commit and README hashes are recorded;
the plan's shipment stop rule is not triggered. This is an availability check,
not a new competitor measurement. Pinned dependencies and v1 claims are unchanged.
''')
with (root/'.gitattributes').open('a', encoding='utf-8', newline='\n') as stream:
    for folder in ['h4-requirement-preflight-20261016', 'competitor-stop-review-20261016']:
        stream.write('\nbenchmarks/results/'+folder+'/** -text -whitespace\n')
print(json.dumps({'competitor_stop_rule_triggered':False,'commit':commit['sha'],
                  'H4_still_pending_quality_and_scale':True}))
