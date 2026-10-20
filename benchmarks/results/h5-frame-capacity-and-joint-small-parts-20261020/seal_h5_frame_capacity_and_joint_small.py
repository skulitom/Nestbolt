from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from h2_import_audit import source_digest
PREFIX = 'h5-frame-capacity-and-joint-small-parts-20261020'
OUT = ROOT / 'benchmarks/results' / PREFIX
FRAME = ROOT / 'output/h5-fixed-insert-frame-capacity-20261020'
SMALL = ROOT / 'output/h5-fixed-frame-small-capacity-20261020'
JOINT = ROOT / 'output/h5-joint-full-frame-small-search-20261020'
POOL = ROOT / 'output/h5-insert-aligned-frame-pool-20261020'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()
BASE = 'f321537c446b124f84d9ca98b28dbbcfc01aa988'
LOCAL = 'ee375935cd24d60f5e516db3ccced693f54088db'
REMOTE = 'abeb2739b1eedde18781b46fd82258f356970be0'
MERGE = '09f59894fa43e3be7ef57e92d4afeec57671a396'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def write(p, v):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, indent=2)
        f.write('\n')

def append(p, s):
    with p.open('a', encoding='utf-8', newline='\n') as f:
        f.write(s)

def main():
    OUT.mkdir()
    frame = load(FRAME / 'audit/checks.json')
    small = load(SMALL / 'audit/checks.json')
    joint = load(JOINT / 'audit/checks.json')
    assert frame['all_returned_layouts_checked'] == 4 and frame['complete_18_frame_groups'] == 2
    assert small['all_returned_layouts_checked'] == 6
    assert [r['cog_upper_bound'] for r in small['independently_verified_cover_bounds']] == [8, 6]
    assert all(r['full_original_counts_ruled_out_by_covers'] for r in small['independently_verified_cover_bounds'])
    assert joint['all_returned_layouts_checked'] == 8 and joint['best_small_parts'] == 21
    assert all(not x['full_target_witness'] for x in [frame, small, joint])
    core = source_digest()
    assert core == '8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    assert git('rev-parse', 'HEAD').decode().strip() == MERGE
    assert git('rev-list', '--parents', '-n', '1', MERGE).decode().split() == [MERGE, LOCAL, REMOTE]
    remote_files = git('diff', '--name-only', BASE, REMOTE).decode().splitlines()
    local_files = git('diff', '--name-only', BASE, LOCAL).decode().splitlines()
    assert len(remote_files) == 11 and len(local_files) == 25
    assert set(remote_files).isdisjoint(local_files)
    remote_hashes, local_hashes = {}, {}
    for source, paths, hashes in [(REMOTE, remote_files, remote_hashes), (LOCAL, local_files, local_hashes)]:
        for p in paths:
            original = git('show', source + ':' + p)
            assert git('show', MERGE + ':' + p) == original
            assert git('hash-object', '--', p).strip() == git('rev-parse', MERGE + ':' + p).strip()
            hashes[p] = sha256(original).hexdigest()
    write(OUT / 'merge-audit.json', {
        'base': BASE, 'local_parent': LOCAL, 'remote_parent': REMOTE, 'merge': MERGE,
        'disjoint_changes': True, 'remote_files_exact': remote_hashes,
        'local_files_exact': local_hashes, 'worktree_matches_merged_blobs': True,
        'production_digest_unchanged': core,
        'remote_scope': 'README link, agent index links, static comparison page and its v0.1.0 source records; no runtime changes.'})
    prior = load(ROOT / 'benchmarks/results/h5-insert-blockers-and-frame-contacts-20261020/source-review.json')
    readmes = {p: digest(ROOT / p) for p in prior['current_readmes']}
    assert readmes['README.md'] != prior['current_readmes']['README.md']
    assert all(readmes[p] == prior['current_readmes'][p] for p in readmes if p != 'README.md')
    inputs = {}
    for root in [FRAME, SMALL, JOINT]:
        for p, h in load(root / 'plan.json')['inputs'].items():
            assert digest(ROOT / p) == h
            if p in inputs:
                assert inputs[p] == h
            inputs[p] = h
        for p in root.rglob('validation-reuse-*.json'):
            reuse = load(p)
            assert reuse['rerun'] is False
            for name, h in reuse['source_files'].items():
                assert digest(ROOT / name) == h
                inputs[name] = h
    previous = json.loads(subprocess.check_output([
        'gh', 'run', 'view', '39452059520', '--json', 'status,conclusion,headSha,jobs,url'], cwd=ROOT))
    assert previous['headSha'] == BASE and previous['conclusion'] == 'cancelled'
    current = json.loads(subprocess.check_output([
        'gh', 'run', 'view', '39454262478', '--json', 'status,conclusion,headSha,jobs,url'], cwd=ROOT))
    assert current['headSha'] == REMOTE
    if current['conclusion'] == 'success':
        assert len(current['jobs']) == 6 and all(j['conclusion'] == 'success' for j in current['jobs'])
    assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == REMOTE
    write(OUT / 'main-ci-f321537-cancelled.json', previous)
    write(OUT / 'main-ci-abeb2739.json', current)
    next_step = (
        'Do not repeat the frame-only relaxation, the two fixed-frame completions or the joint30-second model unchanged. '
        'The joint final layout supplies all18 frames,12 brackets and21 inserts but only9 cogs. '
        'Next hold its51 non-cog poses fixed and construct conservative original-outline free translation regions for cog phases '
        '0,4.5,9,13.5 degrees on both target sheets. Keep every compatible original cog pose and the nine audited seed cogs. '
        'Add bounded, declared free-region boundary contact samples; independently verify every new pose and every cog-pair conflict '
        'before one changed cog-only completion model capped at the original15. Record incomplete regions or generation limits without '
        'an impossibility claim. This is a new conditional construction, not an extension of the expired search. '
        'Only all66 copies passing original geometry, frozen CLI, native margins and unchanged H5 material/cutting gates can qualify H5. '
        'H2 remains open under Artem’s original-denominator decision.')
    write(OUT / 'source-review.json', {
        'production_digest': core, 'previous_readmes': prior['current_readmes'], 'current_readmes': readmes,
        'README_change_from_remote_preserved': True, 'local_merge_commit': MERGE,
        'remote_main_commit': REMOTE, 'remote_main_CI_status': current['status'],
        'remote_main_CI_conclusion': current['conclusion'],
        'previous_f321537_checks_cancelled_after_new_remote_main': True,
        'runtime_changed': False, 'original_geometry_layout_audits': 18,
        'fresh_frozen_CLI_calls': 17, 'exact_CLI_results_reused': 1,
        'native_packing_calls': 0, 'quality_runs': 0, 'held_out_files_evaluated': 0,
        'full_target_witness': False, 'native_margin_qualified': False, 'new_release_qualified': False,
        'completion_percent': 60, 'H2_complete': False, 'H5_complete': False,
        'next_investigation': next_step})
    for p, name in [
        (FRAME / 'model-audit.json', 'frame-model-audit.json'),
        (FRAME / 'result.json', 'frame-result.json'),
        (FRAME / 'audit/checks.json', 'frame-layout-audit.json'),
        (SMALL / 'model-audit.json', 'small-model-audit.json'),
        (SMALL / 'results.json', 'small-results.json'),
        (SMALL / 'audit/checks.json', 'small-layout-and-capacity-audit.json'),
        (JOINT / 'model-audit.json', 'joint-model-audit.json'),
        (JOINT / 'result.json', 'joint-result.json'),
        (JOINT / 'audit/checks.json', 'joint-layout-audit.json')]:
        shutil.copyfile(p, OUT / name)
    members = {}
    for root in [FRAME, SMALL, JOINT]:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                members[root.name + '/' + p.relative_to(root).as_posix()] = p
    for name in inputs:
        p = ROOT / name
        members['source-inputs/' + p.relative_to(ROOT).as_posix()] = p
    for name in [
        'diagnose_h5_fixed_insert_frame_capacity.py', 'audit_h5_fixed_insert_frame_capacity.py',
        'diagnose_h5_fixed_frame_small_capacity.py', 'audit_h5_fixed_frame_small_capacity.py',
        'search_h5_joint_full_frames.py', 'audit_h5_joint_full_frames.py',
        'reduce_h5_free_cog_pool.py', 'census_h5_one_part_moves.py', 'audit_h5_cog_lattices.py', 'ccd1.py']:
        members['helpers/' + name] = ROOT / 'output' / name
    for name in ['job.json', 'library.json', 'request.json', 'conditional-target.json']:
        p = ROOT / 'output/h5-coordinated-placement-selection-20261018' / name
        members['source-inputs/' + p.relative_to(ROOT).as_posix()] = p
    p = ROOT / 'output/h5-full-insert-blockers-20261020/audit/layout-final.json'
    members['source-inputs/' + p.relative_to(ROOT).as_posix()] = p
    for name in remote_files:
        members['remote-merged-files/' + name] = ROOT / name
    manifest = []
    archive = OUT / 'raw.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, p in sorted(members.items()):
            z.write(p, name)
            manifest.append({'path': name, 'bytes': p.stat().st_size, 'sha256': digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) == len(manifest)
        for row in manifest:
            assert sha256(z.read(row['path'])).hexdigest() == row['sha256']
    write(OUT / 'raw-manifest.json', {'archive_sha256': digest(archive), 'files': manifest})
    write(OUT / 'checks.json', {
        'verified_utc': datetime.now(timezone.utc).isoformat(),
        'all_inputs_hash_verified': True, 'frame_capacity_18_reached': True,
        'distinct_complete_frame_groups': 2, 'conditional_small_count_optima': [16, 13],
        'independent_cog_upper_bounds': [8, 6], 'joint_seed_small_parts': 16,
        'joint_final_small_parts': 21, 'joint_final_missing_cogs': 6,
        'original_geometry_layout_audits': 18, 'fresh_frozen_CLI_calls': 17,
        'exact_CLI_results_reused': 1, 'remote_files_preserved': 11, 'local_files_preserved': 25,
        'full_target_witness': False, 'completion_percent': 60,
        'archive_members': len(manifest), 'archive_sha256': digest(archive)})
    shutil.copyfile(__file__, OUT / 'seal_h5_frame_capacity_and_joint_small.py')
    table = '\n'.join(
        f"| {r['case']} | {r['seconds']:.9f} | {r['brackets']} | {r['cogs']} | {r['small_parts']} | "
        f"{small['independently_verified_cover_bounds'][r['case']]['cog_upper_bound']} |"
        for r in load(SMALL / 'results.json'))
    ci_line = ('All six checks on remote abeb2739 pass in the saved snapshot.'
               if current['conclusion'] == 'success' else
               'The abeb2739 hosted checks are still running in the saved snapshot; the local merge is not pushed over them.')
    report = f'''# H5: frame capacity and joint small-part construction — 2026-10-20

**All 18 frames can fit around the selected 21 inserts.** Two such frame
arrangements pass original geometry checks, but independent finite-pool bounds
allow at most eight and six cogs alongside them, below the required fifteen.
A changed joint search improves its own seed from 16 to 21 small parts,
retaining all 18 frames, 12 brackets, 21 inserts and nine cogs. Six cogs are
still missing. This is not a complete or overall better packing result.
H2/H5 remain open at 60%.

## Necessary frame capacity

The [preceding construction](h5-insert-blockers-and-frame-contacts-20261020.md)
fixes 21 insert positions and supplies an expanded pool with 240 new frame
contacts. A necessary relaxation removes bracket/cog restrictions, keeps
all 1719 compatible frame choices and their conflicts, and maximizes frames
from the feasible 16 through the original required 18. Every model field and
complete feasible hint is reconstructed.

One declared 10-second, eight-worker, seed-zero call finishes `OPTIMAL` in
**0.776407200 seconds**, reaching 18 frames. All three callbacks and the
distinct final selection pass original geometry and frozen CLI geometry
checks; their deliberate missing bracket/cog quantities remain failures.
There are two distinct complete 18-frame sets.

## Diagnose what those frames leave for brackets and cogs

Each complete frame set and all 21 inserts are fixed in turn. Every compatible
original bracket/cog pose and projected conflict remains. The diagnostic
allows at most the original 12 brackets and 15 cogs, maximizing their combined
count, then rounded filled area. A count-dominating integer weight makes the
ordering exact. Complete feasible hints use compatible old small-part poses.
Both models and all filters are independently reconstructed.

Each case declares one 20-second limit, eight workers and seed zero. Both
finish `OPTIMAL` quickly:

| Frame case | Seconds | Brackets at optimum | Cogs at optimum | Small-part count | Independent cog upper bound |
| --- | ---: | ---: | ---: | ---: | ---: |
{table}

The bracket/cog columns describe the selected best count and area tie; they
are not separate maximum cog counts. All six returned layouts pass original
geometry and fail the frozen CLI only for their actual missing quantities.
Independent geometry checks **228,448** small-part/fixed-part pairs and
reproduces every eligibility decision.

Separate saved clique covers bound cogs at **8** and **6**, and combined small
parts at **23** and **18**. Every cover entry is verified against an original
pairwise-conflicting clique or singleton. These certificates independently
exclude the required 15 cogs for both fixed frame arrangements. They do not
exclude other frame arrangements or new continuous positions.

## Select frames and small parts together

The expanded parent model is changed to require all **18 frames**, preserve
the **21 fixed inserts**, and jointly choose 0–12 brackets and 0–15 cogs.
It requires at least the best audited seed's 16 small parts, maximizing their
actual count and then rounded filled area. All 5316 variables and 15,132
constraints are reconstructed against the audited parent; every original
and new conflict remains. A complete feasible hint contains 18 frames,
11 brackets, five cogs and 21 inserts.

Its single declared 30-second, eight-worker, seed-zero call returns `FEASIBLE`
after **30.091457300 seconds**. Seven retained callbacks progress through
small-part counts 16, 17, 17, 18, 19, 20 and 21. The final arrangement has
all 12 brackets and nine of the required 15 cogs. The final objective bound
still permits all 27 small parts, so no optimum or impossibility is proved.
There is no retry or extended search.

All seven callbacks and the distinct final selection receive original
geometry checks. Seven frozen CLI calls are fresh; one reuses an exact,
hash-recorded prior layout and result. Every result fails only its original
quantity shortfall. The final minimum geometric clearance is 0.201000 mm
and material charge is 4,985,103.45 mm², within the unchanged target.
Neither is native-margin qualification.

The final 60-part partial contains **4,181,364.4704 mm²** of filled outer area,
below the previously documented 58-part partial's **4,323,340.7841 mm²**.
The gain over this changed model's seed is therefore not reported as a new
best overall partial or H5 improvement. It supplies a new arrangement of all
required non-cog parts for a different cog-contact construction.

## Remote changes and README

Remote main advanced to **abeb2739**, adding a static comparison page about
nesting tools for AI agents, its v0.1.0 records, navigation/index links and a
three-line README link. Its push cancelled the older f321537 workflow:
four jobs passed and the Windows/Linux checks were cancelled. This is not
reported as a successful complete check run.

The disjoint changes merge locally as **09f59894**. The merge audit compares
every incoming file with its exact remote parent and every local evidence
file with its local parent: **11 remote files and 25 local files are preserved**,
and the working tree matches the merged Git blobs. Core source retains its
reviewed digest. English README changes come only from the remote addition;
Japanese and Chinese README hashes remain unchanged. Existing preview,
stable-release and v1 benchmark descriptions are preserved.

{ci_line} No release is made, and these comparison-page changes receive no
v1.1 benchmark credit.

## Next work

{next_step}

No reserved held-out evaluation, native packing or quality run occurs.
All original acceptance rules and published benchmark results remain intact.

[Checks]({PREFIX}/checks.json), [frame outputs]({PREFIX}/frame-layout-audit.json),
[small-part capacity and outputs]({PREFIX}/small-layout-and-capacity-audit.json),
[joint outputs]({PREFIX}/joint-layout-audit.json), [merge verification]({PREFIX}/merge-audit.json),
[cancelled earlier workflow]({PREFIX}/main-ci-f321537-cancelled.json),
[current remote CI]({PREFIX}/main-ci-abeb2739.json), [source review]({PREFIX}/source-review.json),
[all models, certificates, layouts and logs]({PREFIX}/raw.zip),
and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent / (PREFIX + '.md')).write_text(report, encoding='utf-8', newline='\n')
    note = f'''**N4 frame capacity and joint small parts, 2026-10-20:** [the complete audit](../benchmarks/results/{PREFIX}.md)
finds two geometry-verified 18-frame arrangements around all 21 inserts. Their
fixed-group small-part optima are 16 and 13; independent clique certificates
allow at most 8 and 6 cogs, below the required 15. A changed joint model keeps
all 18 frames and increases its own seed from 16 to 21 small parts, ending with
all 12 brackets and 9 cogs after one 30-second limit. All 18 returned layouts
pass original geometry and retain their quantity-only CLI failures. Six cogs
are still missing, and filled area remains below the known 58-part partial.
Next construct new cog contacts around the final 51 non-cog poses; do not
repeat expired searches. Remote abeb2739's comparison page and README link
merge cleanly as 09f59894, preserving 11 incoming and 25 local files. Its push
cancelled f321537's remaining Windows/Linux checks. No complete CI success
or release is inferred. H2/H5 remain open at 60%; core source is unchanged.
'''
    assert (ROOT / 'BENCHMARKS.md').read_bytes() == git('show', 'HEAD:BENCHMARKS.md')
    append(ROOT / 'BENCHMARKS.md', '\n' + note.replace('../benchmarks/', 'benchmarks/'))
    for name in ['docs/PLAN_V1_1.md', 'docs/V1_1_RESEARCH.md']:
        append(ROOT / name, '\n' + note)
    p = ROOT / 'docs/STATUS.md'
    s = p.read_text(encoding='utf-8')
    marker = '**N4 complete-insert blockers and new frame contacts, 2026-10-20:**'
    assert s.count(marker) == 1
    p.write_text(s.replace(marker, note + '\n' + marker), encoding='utf-8', newline='\n')
    append(ROOT / '.gitattributes', f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed': True, 'archive_members': len(manifest),
                      'archive_bytes': archive.stat().st_size, 'completion_percent': 60,
                      'remote_CI_status': current['status'], 'remote_CI_conclusion': current['conclusion']}), flush=True)

if __name__ == '__main__':
    main()
