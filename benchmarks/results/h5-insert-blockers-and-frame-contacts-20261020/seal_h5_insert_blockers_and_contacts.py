from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from h2_import_audit import source_digest
PREFIX = 'h5-insert-blockers-and-frame-contacts-20261020'
OUT = ROOT / 'benchmarks/results' / PREFIX
DIAG = ROOT / 'output/h5-full-insert-blockers-20261020'
CERT = ROOT / 'output/h5-insert-blocker-certificates-20261020'
FIXED = ROOT / 'output/h5-fixed-insert-completion-20261020'
POOL = ROOT / 'output/h5-insert-aligned-frame-pool-20261020'
EXPAND = ROOT / 'output/h5-insert-aligned-frame-completion-20261020'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()

def write(p, v):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, indent=2)
        f.write('\n')

def append(p, s):
    with p.open('a', encoding='utf-8', newline='\n') as f:
        f.write(s)

def main():
    OUT.mkdir()
    diag = load(DIAG / 'audit/checks.json')
    cert = load(CERT / 'checks.json')
    fixed = load(FIXED / 'audit/checks.json')
    expanded = load(EXPAND / 'audit/checks.json')
    graph = load(POOL / 'audit/checks.json')
    assert diag['all_returned_layouts_checked'] == 6 and diag['final_missing_core'] == {'frame': 2}
    assert cert['at_least_two_seed_core_deletions_certified']
    assert not cert['entire_diagnostic_optimum_certified_by_covers']
    assert fixed['best_frame_count'] == expanded['best_frame_count'] == 16
    assert graph['all_new_cliques_valid_and_complete'] and graph['new_frame_poses_checked'] == 240
    assert all(not r['full_target_witness'] for r in [diag, fixed, expanded])
    core = source_digest()
    assert core == '8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    prior = load(ROOT / 'benchmarks/results/h5-seeded-search-and-move-bounds-20261020/source-review.json')
    readmes = {p: digest(ROOT / p) for p in prior['current_readmes']}
    assert readmes == prior['current_readmes']
    roots = [DIAG, CERT, FIXED, POOL, EXPAND]
    inputs = {}
    for root in roots:
        for p, h in load(root / 'plan.json')['inputs'].items():
            assert digest(ROOT / p) == h
            if p in inputs:
                assert inputs[p] == h
            inputs[p] = h
        for p in root.rglob('validation-reuse-*.json'):
            row = load(p)
            assert row['rerun'] is False
            for name, h in row['source_files'].items():
                assert digest(ROOT / name) == h
                inputs[name] = h
    ci = json.loads(subprocess.check_output([
        'gh', 'run', 'view', '39446137827', '--json', 'status,conclusion,headSha,jobs,url'], cwd=ROOT))
    assert ci['headSha'] == '56f818acb3e21b747207eb4db60b40367ebb7f3a'
    assert ci['conclusion'] == 'success' and len(ci['jobs']) == 6
    assert all(j['conclusion'] == 'success' for j in ci['jobs'])
    current = json.loads(subprocess.check_output([
        'gh', 'run', 'view', '39452059520', '--json', 'status,conclusion,headSha,jobs,url'], cwd=ROOT))
    assert current['headSha'] == 'f321537c446b124f84d9ca98b28dbbcfc01aa988'
    remote = subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/main'], cwd=ROOT, text=True)
    assert remote.split()[0] == current['headSha']
    write(OUT / 'main-ci-56f818a.json', ci)
    write(OUT / 'main-ci-f321537.json', current)
    write(OUT / 'push-confirmation.json', {
        'checked_utc': datetime.now(timezone.utc).isoformat(),
        'remote': 'https://github.com/skulitom/Nestbolt.git',
        'ref': 'refs/heads/main', 'sha': current['headSha'],
        'previous_main_all_six_checks_passed_before_push': True})
    next_step = (
        'Do not repeat the fixed-insert completion calls or extend their limits. '
        'First test the necessary frame-only capacity of this fixed21-insert arrangement in the expanded pool, '
        'with all bracket/cog restrictions temporarily removed. Preserve its feasible16-frame seed and original18-frame cap. '
        'If even that relaxation cannot reach18, construct a different full insert arrangement instead of adding unchanged searches. '
        'If18 frames fit, diagnose the surviving bracket/cog capacity of the returned arrangement before a changed completion attempt. '
        'Temporary diagnostic omissions never satisfy original quantities. A full66-copy candidate still requires original geometry, '
        'frozen CLI, native margins and unchanged H5 material/cutting gates. H2 remains open under Artem’s original-denominator decision.')
    write(OUT / 'source-review.json', {
        'production_digest': core, 'current_readmes': readmes,
        'previous_main_all_six_checks_pass': True, 'last_pushed_commit': current['headSha'],
        'last_pushed_CI_status': current['status'], 'last_pushed_CI_conclusion': current['conclusion'],
        'runtime_changed': False, 'original_geometry_layout_audits': 10,
        'fresh_frozen_CLI_calls': 8, 'exact_frozen_CLI_results_reused': 2,
        'native_packing_calls': 0, 'quality_runs': 0, 'held_out_files_evaluated': 0,
        'full_target_witness': False, 'native_margin_qualified': False,
        'new_release_qualified': False, 'completion_percent': 60,
        'H2_complete': False, 'H5_complete': False, 'next_investigation': next_step})
    for p, name in [
        (DIAG / 'model-audit.json', 'blocker-model-audit.json'),
        (DIAG / 'result.json', 'blocker-result.json'),
        (DIAG / 'audit/checks.json', 'blocker-layout-audit.json'),
        (DIAG / 'audit/final-removed-placements.json', 'removed-frames.json'),
        (CERT / 'checks.json', 'blocker-certificates.json'),
        (FIXED / 'model-audit.json', 'fixed-model-audit.json'),
        (FIXED / 'audit/checks.json', 'fixed-results.json'),
        (POOL / 'generation.json', 'contact-generation.json'),
        (POOL / 'audit/checks.json', 'contact-audit.json'),
        (EXPAND / 'model-audit.json', 'expanded-model-audit.json'),
        (EXPAND / 'audit/checks.json', 'expanded-results.json')]:
        shutil.copyfile(p, OUT / name)
    members = {}
    for root in roots:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                members[root.name + '/' + p.relative_to(root).as_posix()] = p
    for name in inputs:
        p = ROOT / name
        members['source-inputs/' + p.relative_to(ROOT).as_posix()] = p
    for name in [
        'diagnose_h5_insert_blockers.py', 'audit_h5_insert_blockers.py',
        'certify_h5_insert_blocker_bounds.py', 'complete_h5_fixed_inserts.py',
        'audit_h5_fixed_insert_results.py', 'build_h5_insert_aligned_frames.py',
        'audit_h5_insert_aligned_frames.py', 'solve_h5_insert_aligned_frames.py',
        'reduce_h5_free_cog_pool.py', 'census_h5_one_part_moves.py',
        'audit_h5_cog_lattices.py', 'ccd1.py']:
        members['helpers/' + name] = ROOT / 'output' / name
    for name in [
        'output/h5-coordinated-placement-selection-20261018/library.json',
        'output/h5-coordinated-placement-selection-20261018/request.json',
        'output/h5-free-cog-pool-20261020/seed-layout.json']:
        members['source-inputs/' + name] = ROOT / name
    archive = OUT / 'raw.zip'
    manifest = []
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
        'all_inputs_hash_verified': True,
        'minimum_seed_core_deletions_for_21_inserts_independently_proven': 2,
        'deletion_sets_enumerated': 1036, 'clique_certificate_groups_verified': 15626,
        'original_geometry_layout_audits': 10, 'fresh_frozen_CLI_calls': 8,
        'exact_frozen_CLI_results_reused': 2,
        'new_frame_positions': 240, 'new_conflicts_independently_verified': 179683,
        'new_pairs_exhaustively_examined': 1117560,
        'full_target_witness': False, 'completion_percent': 60,
        'archive_members': len(manifest), 'archive_sha256': digest(archive)})
    shutil.copyfile(__file__, OUT / 'seal_h5_insert_blockers_and_contacts.py')
    ci_line = ('All six checks for f321537 also pass in its saved snapshot.'
               if current['conclusion'] == 'success' else
               'The f321537 checks are running in the saved snapshot; this later evidence remains local while they finish.')
    report = f'''# H5: full-insert blockers and new frame contacts — 2026-10-20

**At least two saved core poses must be removed to fit all 21 inserts within
the retained insert pool.** Original-geometry checks verify a concrete
21-insert arrangement after removing two frames. This is a diagnostic partial,
not a complete or better packing result. Restoring the required frames remains
unresolved after two bounded searches, including one with 240 new frame
positions. H2/H5 remain open at 60%.

## Diagnose the complete insert requirement

Following the [two-move limits](h5-seeded-search-and-move-bounds-20261020.md),
the diagnostic selects exactly 21 mutually compatible insert positions from
the 686 retained choices. Each of the saved 45 frames/brackets/cogs may stay
or be temporarily omitted. It introduces no replacement core poses.
The objective first maximizes retained core count, then retained rounded
filled-outer area. A coefficient exceeding the sum of every area tie makes
that order exact. Every field of the 731-variable, 3100-constraint model is
independently reconstructed.

One declared 20-second, eight-worker, seed-zero call finishes `OPTIMAL` in
**0.101566800 seconds**. Its five callbacks and distinct final selection are
all retained. The final arrangement has 16 frames, 12 brackets, 15 cogs and
21 inserts. Its missing frames are two adjacent 350 × 450 mm rectangles at
the lower left of sheet zero, with original candidate indices 178 and 192.

Independent geometry reproduces every insert/core blocker set over **21,759**
same-sheet pairs. All six returned partials pass original outline, rotation,
stock, clearance and material checks; six fresh frozen CLI checks reject only
their actual missing core quantities. The final result has exactly the two
reported frame blockers and no unnecessarily omitted core poses.

Although this has 64 parts, it contains **4,166,740.7841 mm²** of filled outer
area, less than the known 58-part partial's **4,323,340.7841 mm²**. Part count
alone does not establish progress in material packing. The original job still
requires both missing frames.

## Independent deletion certificates

A separate enumeration covers all **1036** ways to omit zero, one or two of
the 45 seed core poses while keeping the others fixed. It derives **910**
distinct available-insert sets and partitions each into original conflict
cliques or singletons. Explicit-set reconstruction verifies every deletion,
every available-insert set and all **15,626** cover entries.

With zero or one deletion, every insert upper bound is at most **20**.
Together with the geometry-verified 21-insert witness after two deletions,
this independently proves that the diagnostic minimum deletion count is two.
It is a statement about this seed and finite insert pool, not unrestricted
continuous placement.

The covers leave **89** two-deletion cases unresolved for 21 inserts: 65 frame
pairs, 15 frame/cog pairs and nine frame/bracket pairs. Their lower area cost
is weaker than the solver's reported optimum. The secondary rounded-area
optimum therefore remains solver-reported; the independent cover proof
establishes only the primary two-deletion count.

## Attempt to restore both frames

The next model fixes the final 21 inserts and allows every compatible
previously retained frame, bracket and cog pose to move. It requires all
12 brackets and 15 cogs, maximizing frames from the known feasible 16 up to
the original required 18. All 3988 variables, 12,533 constraints and the
complete feasible hint are reconstructed. One declared 20-second call returns
`FEASIBLE` after **20.086176900 seconds**, with 16 frames and upper bound 18.
The callback and distinct final layout are checked; one exact seed CLI result
is reused and the other receives a fresh quantity-only rejection.

## Add new frame positions aligned to the inserts

For both distinct rectangular frame orientations, the changed construction
crosses all feasible horizontal and vertical contacts with the fixed insert
rectangles and stock boundaries. Transforms retain their original floating
point values; only exact transform duplicates are discarded. The insert gap
is clearance + 0.001 mm and stock contact inset is 0.0001 mm. Neither choice
claims native-margin qualification.

Of **799** declared contact events, 557 conflict with fixed inserts, two are
exact existing transforms and **240** add new frame positions. All 9059 old
candidates and indices remain unchanged. Every original compatible core pose
is restored, including poses removed by the earlier dominance reduction:
new frame positions can invalidate old dominance relationships.

This produces 5076 original compatible core poses plus 240 new frames.
The graph is explicitly conditional on the fixed 21 inserts. It cannot be
reused for movable inserts without computing those missing edges.

Independent checks reconstruct every event, check **132,955** original
core/insert filter pairs, examine all **1,117,560** new same-sheet pairs and
reproduce **179,683** new conflicts. All 2061 new cliques are pairwise valid
and cover every new edge. Compression finishes without reaching its limit
and leaves no residual pair constraints.

The expanded model has 5316 variables (1719 frames, 1303 brackets, 2294 cogs),
15,131 constraints and a complete feasible 16-frame hint. All fields are
reconstructed before its single declared 30-second call. It returns `FEASIBLE`
after **30.097629300 seconds**, again with 16 frames and upper bound 18.
Both returned layouts pass original geometry and fail only the two missing
frames; one exact seed CLI result is reused and one validation is new.
This timeout does not prove an 18-frame completion impossible. No expired
search is restarted, and every result and soft cleanup overrun remains.

## Next work and repository state

{next_step}

All six hosted checks for **56f818a** now pass. The saved **f321537** checkpoint
was then pushed normally to main and its remote hash is confirmed. {ci_line}
Production source and the three READMEs retain their reviewed hashes.
No held-out evaluation, native packing, quality run or new release occurs.
The existing preview description remains accurate.

[Checks]({PREFIX}/checks.json), [diagnostic outputs]({PREFIX}/blocker-layout-audit.json),
[deletion certificate audit]({PREFIX}/blocker-certificates.json),
[original completion]({PREFIX}/fixed-results.json), [new contact audit]({PREFIX}/contact-audit.json),
[expanded completion]({PREFIX}/expanded-results.json),
[source review]({PREFIX}/source-review.json), [passing main checks]({PREFIX}/main-ci-56f818a.json),
[push confirmation]({PREFIX}/push-confirmation.json), [current CI snapshot]({PREFIX}/main-ci-f321537.json),
[all models, logs, layouts and certificates]({PREFIX}/raw.zip), and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent / (PREFIX + '.md')).write_text(report, encoding='utf-8', newline='\n')
    note = f'''**N4 complete-insert blockers and new frame contacts, 2026-10-20:** [the full audit](../benchmarks/results/{PREFIX}.md)
verifies a 21-insert diagnostic after temporarily removing two frames. Exact
clique certificates over all 1036 zero/one/two-core deletions prove that at
least two saved core poses must be removed within this insert pool; they do
not independently prove the secondary area tie. The 64-part diagnostic packs
less filled area than the known 58-part partial and receives no improvement
credit. Two bounded completion searches, the second adding 240 new exact frame
contacts and restoring original core choices, both retain only 16 frames.
Independent geometry verifies all ten returned layouts, 179,683 new conflicts
and complete clique coverage. Both original missing frames remain required.
Next check frame-only capacity before selecting a different insert arrangement
or diagnosing bracket/cog obstructions. All six 56f818a hosted checks pass and
f321537 is pushed to main. H2/H5 remain open at 60%; runtime, README and release
assets are unchanged.
'''
    original_bench = subprocess.check_output(['git', 'show', 'HEAD:BENCHMARKS.md'], cwd=ROOT)
    assert (ROOT / 'BENCHMARKS.md').read_bytes() == original_bench
    append(ROOT / 'BENCHMARKS.md', '\n' + note.replace('../benchmarks/', 'benchmarks/'))
    for name in ['docs/PLAN_V1_1.md', 'docs/V1_1_RESEARCH.md']:
        append(ROOT / name, '\n' + note)
    p = ROOT / 'docs/STATUS.md'
    text = p.read_text(encoding='utf-8')
    marker = '**N4 seeded search and local-move bounds, 2026-10-20:**'
    assert text.count(marker) == 1
    p.write_text(text.replace(marker, note + '\n' + marker), encoding='utf-8', newline='\n')
    append(ROOT / '.gitattributes', f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed': True, 'archive_members': len(manifest),
                      'archive_bytes': archive.stat().st_size, 'completion_percent': 60,
                      'current_main_CI_status': current['status'], 'current_main_CI_conclusion': current['conclusion']}), flush=True)

if __name__ == '__main__':
    main()
