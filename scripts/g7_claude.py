"""G7 MCP acceptance with a real client: Claude Code in print mode.

Runs `claude -p --mcp-config <file> --strict-mcp-config` in a fresh workspace
holding examples/parts.svg. The client may use only the five Nestbolt tools
(no shell or code tools). It must list the tools, import the SVG, nest with a
10 s budget and export; the nest output is then checked with the independent
validator. Uses the Claude account logged in on this machine.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ['import_parts', 'nest', 'validate_layout', 'export_layout', 'estimate_sheets']
PROMPT = """Use only the nestbolt MCP tools for this task.
1. List the names of the nestbolt tools you have.
2. Import parts.svg with import_parts.
3. Call nest once: two copies of every imported part on one sheet 300 mm wide and
   200 mm high with 5 mm margins, spacing_mm 1, edge_spacing_mm 1, time_budget_s 10,
   seed 0, out_dir "run".
4. Call export_layout for that layout with out_dir "export".
Finish with only a JSON object, no other text:
{"tools": [...], "library_path": "...", "layout_path": "...", "valid": true or false,
 "export_files": [...]}"""


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', type=Path, default=ROOT/'target/release/nestbolt-mcp.exe')
    parser.add_argument('--cli', type=Path, default=ROOT/'target/release/nestbolt.exe')
    parser.add_argument('--claude', default=shutil.which('claude') or 'claude')
    args = parser.parse_args()
    started = datetime.now(timezone.utc)
    stamp = f"{started.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    workspace = ROOT/'output/g7'/stamp
    workspace.mkdir(parents=True)
    shutil.copy(ROOT/'examples/parts.svg', workspace/'parts.svg')
    config = workspace.parent/f'{stamp}-mcp.json'
    config.write_text(json.dumps({'mcpServers': {'nestbolt': {
        'command': str(args.server.resolve()), 'args': [],
        'env': {'NESTBOLT_WORKSPACE': str(workspace)}}}}, indent=2), encoding='utf-8')
    # The prompt goes on stdin: Windows argument passing cuts a multi-line
    # argument at its first newline, along with every flag after it. User-level
    # settings (and their hooks) stay out of the test.
    command = [args.claude, '-p', '--mcp-config', str(config), '--strict-mcp-config',
               '--allowedTools', ','.join(f'mcp__nestbolt__{t}' for t in TOOLS),
               '--restricted', '--no-session-persistence', '--setting-sources', 'project,local',
               '--output-format', 'json']
    done = subprocess.run(command, input=PROMPT, cwd=workspace, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=900)
    (workspace.parent/f'{stamp}-claude.json').write_text(done.stdout, encoding='utf-8')
    envelope = json.loads(done.stdout) if done.stdout.strip().startswith('{') else {}
    answer_text = envelope.get('result', '')
    start, end = answer_text.find('{'), answer_text.rfind('}')
    answer = json.loads(answer_text[start:end + 1]) if start >= 0 < end else {}
    run_dir = workspace/'run'
    checks = {
        'client_exit': done.returncode,
        # Claude Code names MCP tools mcp__<server>__<tool>.
        'listed_tools': sorted(t.removeprefix('mcp__nestbolt__') for t in answer.get('tools', [])) == sorted(TOOLS),
        'library_written': any(workspace.glob('nestbolt/*.json')) or Path(workspace, answer.get('library_path', '-')).is_file(),
        'nest_outputs': all((run_dir/f).is_file() for f in ['job.json', 'layout.json', 'report.json']),
        'exports': len(list((workspace/'export').glob('*.svg'))) >= 1 and len(list((workspace/'export').glob('*.dxf'))) >= 1,
    }
    validation = None
    if checks['nest_outputs']:
        checked = subprocess.run([str(args.cli), 'validate', '--job', str(run_dir/'job.json'),
                                  '--layout', str(run_dir/'layout.json')], capture_output=True, text=True)
        validation = json.loads(checked.stdout) if checked.stdout.strip().startswith('{') else None
        report = json.loads((run_dir/'report.json').read_text(encoding='utf-8'))
        checks['nest_budget_10s'] = report.get('time_budget_s') == 10
    checks['independent_validation'] = bool(validation and validation.get('valid'))
    passed = checks['client_exit'] == 0 and all(v is True for k, v in checks.items() if k != 'client_exit')
    version = subprocess.run([args.claude, '--version'], capture_output=True, text=True).stdout.strip()
    result = {'scope': 'G7 real MCP client (Claude Code print mode)', 'recorded_at': started.isoformat(),
              'claude_version': version, 'server_sha256': digest(args.server), 'command': command + ['< prompt on stdin'],
              'prompt': PROMPT, 'answer': answer, 'checks': checks,
              'validation_metrics': validation and validation.get('metrics'),
              'usage': {k: envelope.get(k) for k in ['num_turns', 'duration_ms', 'total_cost_usd', 'is_error']},
              'workspace': str(workspace.relative_to(ROOT)), 'pass': passed}
    out = ROOT/'benchmarks/results'/f'g7-claude-{stamp}'
    out.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    lines = ['# G7 MCP acceptance: Claude Code', '',
             f'{version}, `claude -p --mcp-config <file> --strict-mcp-config`, only the five Nestbolt tools '
             f'allowed, `--restricted` (no shell or code tools), fresh workspace with `examples/parts.svg`. '
             f'Server binary `{result["server_sha256"][:16]}`.', '',
             '| Check | Result |', '| --- | --- |']
    lines += [f'| {k} | {v} |' for k, v in checks.items()]
    if validation and validation.get('metrics'):
        m = validation['metrics']
        lines += ['', f"Independent validation: valid, {m['placed_parts']}/{m['requested_parts']} parts, "
                      f"{m['sheets_used']} sheet(s), material {m['normalized_material']:.4f}."]
    lines += ['', f"Client turns {envelope.get('num_turns')}, {envelope.get('duration_ms')} ms. "
                  f"Transcript summary and files: `{result['workspace']}`.", '',
              f"**Result: {'pass' if passed else 'fail'}.**"]
    out.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(out.with_suffix('.md'))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
