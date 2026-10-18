"""Reuse the archive and geometry audits unchanged, with an accurate candidate description."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def adapt(s):return s.replace('h5-contained-return','h5-free-return').replace('h5_contained_return','h5_free_return').replace('Contained-return','Free-space-return').replace('contained-return','free-space-return')
def save(name,s):
 compile(s,name,'exec');(root/'output'/name).write_text(s,encoding='utf-8',newline='\n')
s=adapt((root/'output/finish_h5_contained_return_pilot.py').read_text(encoding='utf-8'))
start=s.index("    'The candidate shifts fitting return");end=s.index("    'Four jobs, two kerfs",start)
s=s[:start]+'''    'The candidate searches at most 256 translations for each returned part',
    'against the current source and already placed returns. It keeps original',
    'orientations and reflections, reserves filled holes, charges geometry work',
    'and observes the shared deadline. The prior seed remains as fallback.',
    'Original choices, repair allocation and strict acceptance are unchanged.',
    '[Qualification](h5-free-return-preparation-20261018.md) retains 137 passing',
    'tests: 130 prior tests unchanged, three fixture expectations revised after',
    'independent validation of actual improvement, and four new regressions.',
    'The expected old-behavior failures, obsolete assumptions and corrected',
    'coordinate-frame oracle remain. Exact source reconstruction, deterministic',
    'public replays, independent authored checks, lint and build pass.','',
'''+s[end:]
save('finish_h5_free_return_pilot.py',s)
save('audit_h5_free_return.py',adapt((root/'output/audit_h5_contained_return.py').read_text(encoding='utf-8')))
s=adapt((root/'output/record_h5_contained_return_outcome.py').read_text(encoding='utf-8'))
# The currently inserted preparation note is the exact span replaced by its outcome.
start=s.index("start = old.index(");end=s.index('\n',start)
s=s[:start]+"start = old.index('**N4 free-space return preparation, 2026-10-18:**')"+s[end:]
# The previous contained-return outcome follows the new preparation.
start=s.index("end = old.index(");end=s.index('\n',start)
s=s[:start]+"end = old.index('**N4 contained-return', start)"+s[end:]
save('record_h5_free_return_outcome.py',s)
print('Prepared unchanged archive verification and filled-outer audit; outcome requires a reviewed interpretation.')
