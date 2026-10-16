"""Verify current H4 scope and the shipped WASM memory contract without searches."""
from hashlib import sha256
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/h4-requirement-preflight-20261016'
out.mkdir(exist_ok=False)
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()
sys.path.insert(0, str(root/'scripts'))
import h4_preview_matrix as preview
import h4_scale as scale

plan = load(root/'benchmarks/results/h4-preview-score-release-20261016/plan.json')
rows, full, subset = preview.cases()
assert rows == plan['cases'] and preview.guards(rows) == plan['guards']
expected_subset = [f'm-public-gear-{i}' for i in range(1,5)] + [f'm-sign-{i}' for i in range(1,5)] + ['m-mechanical-cog-washers']
assert all(name in plan['subset_ids'] for name in expected_subset)
assert len(plan['subset_ids']) == 11 and len(plan['full_ids']) == 65
examples = [r for r in subset if 'library' in r]
assert len(examples) == 2
assert {'gears', 'letters'} == {Path(r['source']).stem for r in examples}
assert plan['seconds'] == 60 and plan['seeds'] == [0,1,2]
assert plan['cpus'] == [0,2,4,6,8,10,12,14] and plan['concurrency'] == 8
assert plan['new_attempts'] == {'native':201, 'chrome':201, 'firefox':201}
scale_plan = load(root/'benchmarks/results/h4-preview-score-scale-plan-20261016/plan.json')
for fixture in ['curves', 'g5']:
    assert scale.guards(fixture=fixture) == scale_plan['scale_guards'][fixture]

integration = load(root/'benchmarks/results/h4-score-integration-20261016/checks.json')
wasms = list((root/'web/dist/assets').glob('*.wasm'))
assert len(wasms) == 1 and digest(wasms[0]) == integration['wasm_sha256']
data = wasms[0].read_bytes()
assert data[:8] == b'\x00asm\x01\x00\x00\x00'

def number(buffer, index):
    value = shift = 0
    while True:
        assert index < len(buffer) and shift <= 63
        byte = buffer[index]
        index += 1
        value |= (byte & 127) << shift
        if not byte & 128:
            return value, index
        shift += 7

def name(buffer, index):
    size, index = number(buffer, index)
    assert index+size <= len(buffer)
    return buffer[index:index+size].decode('utf-8'), index+size

def value_type(buffer, index):
    byte = buffer[index]
    index += 1
    if byte in [0x63, 0x64]:
        _, index = number(buffer, index)
    else:
        assert byte in [0x7f,0x7e,0x7d,0x7c,0x7b,0x70,0x6f], hex(byte)
    return index

def limits(buffer, index):
    flags, index = number(buffer, index)
    assert flags <= 7
    minimum, index = number(buffer, index)
    maximum = None
    if flags & 1:
        maximum, index = number(buffer, index)
    return {'flags': flags, 'shared': bool(flags & 2), 'memory64': bool(flags & 4),
            'minimum_pages': minimum, 'maximum_pages': maximum}, index

memories, imports, sections = [], [], []
index = 8
while index < len(data):
    kind = data[index]
    size, start = number(data, index+1)
    end = start+size
    assert end <= len(data)
    payload = data[start:end]
    sections.append({'id': kind, 'bytes': size})
    if kind == 2:
        count, at = number(payload, 0)
        for _ in range(count):
            module, at = name(payload, at)
            field, at = name(payload, at)
            item_kind = payload[at]
            at += 1
            imports.append({'module': module, 'name': field, 'kind': item_kind})
            if item_kind == 0:
                _, at = number(payload, at)
            elif item_kind == 1:
                at = value_type(payload, at)
                _, at = limits(payload, at)
            elif item_kind == 2:
                memory, at = limits(payload, at)
                memories.append({'imported': True, **memory})
            elif item_kind == 3:
                at = value_type(payload, at)+1
            elif item_kind == 4:
                _, at = number(payload, at)
                _, at = number(payload, at)
            else:
                raise AssertionError(('Unknown import kind', item_kind))
        assert at == len(payload)
    elif kind == 5:
        count, at = number(payload, 0)
        for _ in range(count):
            memory, at = limits(payload, at)
            memories.append({'imported': False, **memory})
        assert at == len(payload)
    index = end
assert index == len(data) and len(memories) == 1
assert not any(m['shared'] for m in memories)
assert not any(m['imported'] for m in memories)
record = {
    'scope': __doc__, 'candidate': integration['release_candidate_commit'],
    'product_digest': integration['product_digest'],
    'matrix_plan_sha256': digest(root/'benchmarks/results/h4-preview-score-release-20261016/plan.json'),
    'declared_subset_exact': True, 'subset_ids': plan['subset_ids'],
    'full_development_jobs': len(full), 'new_attempts': plan['new_attempts'],
    'one_worker_per_job_runner': 'scripts/h4_quality.py + web/bench/run.mjs',
    'physical_cores_and_original_budget_seed_method': True,
    'scale_fixture_and_engine_guards_match': True,
    'wasm_path': wasms[0].relative_to(root).as_posix(), 'wasm_sha256': digest(wasms[0]),
    'wasm_memory_declarations': memories, 'wasm_imports': imports, 'wasm_sections': sections,
    'no_imported_or_shared_WASM_memory': True,
    'full_quality_result_pending': True, 'current_scale_result_pending': True,
    'H4_complete': False, 'held_out_geometry_read': False,
}
(out/'checks.json').write_text(json.dumps(record,indent=2)+'\n', encoding='utf-8', newline='\n')
(out/'verify.py').write_bytes(Path(__file__).read_bytes())
report = '''# H4 requirement preflight — 2026-10-16

**Current scope and the no-WASM-threads constraint are verified; H4 remains open.**
This reads existing source/builds/plans only. It performs no new search, changes
no threshold and opens no reserved geometry. [Exact checks](h4-requirement-preflight-20261016/checks.json)
bind the review to candidate `7eba929` and the engine currently under measurement.

| Requirement | Evidence needed | Current finding |
| --- | --- | --- |
| Declared development subset | Exact IDs, source bytes and public example inputs | Verified: gear-1–4, sign-1–4, cog-washers, gears and letters; eleven unique cases |
| Original G5 method | Sixty seconds, seeds 0–2, one fresh worker per job, physical CCD0 cores | Committed plan and runner match; live outcomes remain pending |
| Subset material | Both browsers median at most +1%, every job at most +5% | Current full matrix must prove both; isolated subset is supporting evidence only |
| Full G5 development quality | All 65 development jobs, original browser bounds | Current full matrix must prove aggregate and each-seed median/total limits |
| Native regression | All 195 layouts valid, median within +0.5% of frozen v1 | Current full matrix must prove this against its verified archived baseline |
| No previously fitting input becomes invalid | Original jobs/requests and quantities, independent validation | All matrix outcomes must satisfy the unchanged original constraints |
| No WASM threads | Actual shipped memory declarations and application worker model | Verified: one defined, unshared WASM memory; no imported/shared memory. Separate Web Workers run independent engines |
| 2,000-part curved drawing | Actual import, nest and SVG/DXF export in both browsers | Committed curve fixture and built-site/engine hashes match; current workflow pending |
| Memory and responsiveness | Browser-process-tree RSS/private samples below 1.5 GB; heartbeat/Long Tasks at most 200 ms | Existing instrumented runner covers import, nesting and export; current measurements pending |
| Original G5 scale regression | Original simple workload, quick start off, automatic workers | Separate current Chrome/Firefox workflows are fixed in the sequence; pending |
| Preserve exact output geometry | Original curves/gear rings, independent saved-project validation and per-sheet cutting files | Current scale exports must be checked; earlier outputs cannot replace them |
| Integrated product behavior | Native/CLI/MCP/browser, schemas, package verification | Local integration and all six hosted checks pass on the candidate |
| Preserve failures and v1 meaning | Frozen inputs/results, prior failed measurements and option/default disclosures | Original failed comparisons remain sealed; the README identifies the frozen v1 build; no new competitor claim |

The memory check parses the measured WASM binary's import and memory sections,
including limits flags; it does not infer thread behavior from a filename or
source comment. The automatic browser worker count is separate from WASM shared
memory. The current fixed scale runners measure process-tree memory every 200 ms,
a 20 ms main-thread heartbeat and Long Tasks where supported. These are the
precommitted observations, not a universal memory/latency guarantee.

The final review must inspect the complete original matrix, saved raw layouts,
all scale outcomes/exports and their unchanged guards. A failed comparison or
missing scale outcome keeps H4 open. Until that review passes, completion stays
45%; H2 and H5 remain independently open.
'''
(out.parent/(out.name+'.md')).write_text(report, encoding='utf-8', newline='\n')
print(json.dumps({'declared_subset_exact': True, 'full_jobs':len(full), 'WASM_memories':memories,
                  'wasm_sha256':digest(wasms[0]), 'H4_complete':False}))
