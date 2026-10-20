from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from h2_import_audit import source_digest
PREFIX = 'h5-seeded-search-and-move-bounds-20261020'
OUT = ROOT / 'benchmarks/results' / PREFIX
FIXED = ROOT / 'output/h5-seeded-insert-search-20261020'
FREE = ROOT / 'output/h5-free-cog-pool-20261020'
ONE = ROOT / 'output/h5-one-core-move-census-20261020'
TWO = ROOT / 'output/h5-two-core-move-census-20261020'
ESCAPE = ROOT / 'output/h5-three-six-core-escape-20261020'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()

def write(p, value):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')

def append(p, s):
    with p.open('a', encoding='utf-8', newline='\n') as f:
        f.write(s)

def main():
    OUT.mkdir()
    fixed = load(FIXED / 'result-audit/checks.json')
    free = load(FREE / 'result-audit/checks.json')
    reduction = load(FREE / 'audit.json')
    two = load(TWO / 'audit.json')
    escape = load(ESCAPE / 'result.json')
    assert fixed['all_returned_layouts_checked'] == 8 and fixed['best_insert_count'] == 13
    assert all(not r['improved_on_case_seed'] for r in fixed['cases'])
    assert free['all_returned_layouts_checked'] == 2 and not free['improved_on_seed']
    assert reduction['substitutions_checked'] == 2247 and reduction['mapped_seed_geometry_checked']
    assert two['all_moves'] == 331 and two['any_improvement_ruled_out']
    assert escape['status'] == 'UNKNOWN' and escape['incumbents'] == 0 and not escape['feasible']
    assert not list(ESCAPE.glob('incumbent-*.json')) and not (ESCAPE / 'selected-indices.json').exists()
    core = source_digest()
    assert core == '8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    prior = load(ROOT / 'benchmarks/results/h5-dominated-poses-and-seeds-20261020/source-review.json')
    readmes = {p: digest(ROOT / p) for p in prior['current_readmes']}
    assert readmes == prior['current_readmes']
    inputs = {}
    roots = [FIXED, FREE, ONE, TWO, ESCAPE]
    for root in roots:
        for name in ['plan.json', 'model-plan.json']:
            p = root / name
            if not p.exists():
                continue
            for name, h in load(p)['inputs'].items():
                assert digest(ROOT / name) == h, name
                if name in inputs:
                    assert inputs[name] == h
                inputs[name] = h
        for p in root.rglob('validation-reuse-*.json'):
            r = load(p)
            assert r['rerun'] is False
            for name, h in r['source_files'].items():
                assert digest(ROOT / name) == h
                inputs[name] = h
    # Preserve every referenced exact frozen-CLI result and its original layout.
    for p in FIXED.rglob('*.json'):
        r = load(p)
        if isinstance(r, dict) and r.get('rerun') is False and 'source_files' in r:
            for name, h in r['source_files'].items():
                assert digest(ROOT / name) == h
                inputs[name] = h
    ci_old = json.loads(subprocess.check_output([
        'gh', 'run', 'view', '39439565169', '--json', 'status,conclusion,headSha,jobs,url'], cwd=ROOT))
    assert ci_old['headSha'] == 'f6edfb7149e2ac03ad221a033e00c45be2ed38bb'
    assert ci_old['conclusion'] == 'success' and len(ci_old['jobs']) == 6
    assert all(j['conclusion'] == 'success' for j in ci_old['jobs'])
    ci = json.loads(subprocess.check_output([
        'gh', 'run', 'view', '39446137827', '--json', 'status,conclusion,headSha,jobs,url'], cwd=ROOT))
    assert ci['headSha'] == '56f818acb3e21b747207eb4db60b40367ebb7f3a'
    remote = subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/main'], cwd=ROOT, text=True)
    assert remote.split()[0] == ci['headSha']
    write(OUT / 'main-ci-f6edfb7.json', ci_old)
    write(OUT / 'main-ci-56f818a.json', ci)
    write(OUT / 'push-confirmation.json', {
        'checked_utc': datetime.now(timezone.utc).isoformat(),
        'remote': 'https://github.com/skulitom/Nestbolt.git',
        'ref': 'refs/heads/main', 'sha': ci['headSha'],
        'includes_prior_local_commits': ['6cde1bd167c0c8c3989707960848c94fd17517b1', ci['headSha']]})
    next_step = (
        'Do not repeat the four fixed-cog optimizations, the free-cog search or the three-to-six-move feasibility search unchanged. '
        'The audited reduced pool cannot improve the saved 13-insert seed with at most two core moves. '
        'The larger search timed out without deciding three-to-six moves. Next diagnose the minimum frame/bracket/cog blockers '
        'of a mutually compatible 21-insert set, allowing only this temporary diagnostic to omit blocked core poses. '
        'Use the exact blocker sets to identify coordinated relocation regions and generate new original-geometry contact positions, '
        'rather than extending an expired search. Preserve every original core quantity in any subsequent completion model. '
        'Only an original 66-copy layout passing geometry, the frozen CLI, native margins and the unchanged material/cutting gates '
        'can qualify H5. H2 remains open under Artem’s original-denominator decision.')
    review = {
        'production_digest': core, 'current_readmes': readmes,
        'last_pushed_commit': ci['headSha'], 'last_pushed_CI_status': ci['status'],
        'last_pushed_CI_conclusion': ci['conclusion'],
        'previous_main_all_six_checks_pass': True,
        'runtime_changed': False, 'fresh_frozen_CLI_calls': 8, 'exact_CLI_results_reused': 3,
        'native_packing_calls': 0, 'quality_runs': 0, 'held_out_files_evaluated': 0,
        'full_target_witness': False, 'native_margin_qualified': False,
        'new_release_qualified': False, 'completion_percent': 60,
        'H2_complete': False, 'H5_complete': False, 'next_investigation': next_step}
    write(OUT / 'source-review.json', review)
    for p, name in [
        (FIXED / 'model-audit.json', 'fixed-model-audit.json'),
        (FIXED / 'result-audit/checks.json', 'fixed-results.json'),
        (FREE / 'result.json', 'free-pool-reduction.json'),
        (FREE / 'audit.json', 'free-pool-audit.json'),
        (FREE / 'model-audit.json', 'free-model-audit.json'),
        (FREE / 'result-audit/checks.json', 'free-results.json'),
        (ONE / 'audit.json', 'one-move-audit.json'),
        (TWO / 'result.json', 'two-move-results.json'),
        (TWO / 'audit.json', 'two-move-audit.json'),
        (ESCAPE / 'model-audit.json', 'escape-model-audit.json'),
        (ESCAPE / 'result.json', 'escape-result.json')]:
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
        'prepare_h5_seeded_insert_search.py', 'audit_h5_seeded_insert_model.py',
        'solve_h5_seeded_insert_search.py', 'audit_h5_seeded_insert_results.py',
        'reduce_h5_free_cog_pool.py', 'audit_h5_free_cog_reduction.py',
        'prepare_h5_free_cog_search.py', 'solve_h5_free_cog_search.py',
        'audit_h5_free_cog_results.py', 'census_h5_one_part_moves.py',
        'audit_h5_one_part_move_census.py', 'census_h5_two_part_moves.py',
        'audit_h5_two_part_move_census.py', 'probe_h5_coordinated_escape.py',
        'audit_h5_cog_lattices.py', 'ccd1.py']:
        members['helpers/' + name] = ROOT / 'output' / name
    for base in ['h5-skeleton-contact-selection-20261020', 'h5-coordinated-placement-selection-20261018']:
        for name in ['library.json', 'request.json']:
            p = ROOT / 'output' / base / name
            members['source-inputs/' + p.relative_to(ROOT).as_posix()] = p
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
    checks = {
        'verified_utc': datetime.now(timezone.utc).isoformat(),
        'all_inputs_hash_verified': True, 'seeded_fixed_searches': 4,
        'safe_free_pool_substitutions': 2247, 'retained_free_pool_candidates': 6812,
        'free_cog_searches': 1, 'original_geometry_layout_audits': 11,
        'fresh_frozen_CLI_calls': 8, 'exact_CLI_results_reused': 3,
        'one_move_feasible_replacements': 23, 'two_move_feasible_replacements': 307,
        'all_zero_one_two_moves_audited': 331, 'two_move_maximum_insert_bound': 13,
        'three_to_six_move_search_status': escape['status'],
        'full_target_witness': False, 'completion_percent': 60,
        'archive_members': len(manifest), 'archive_sha256': digest(archive)}
    write(OUT / 'checks.json', checks)
    shutil.copyfile(__file__, OUT / 'seal_h5_seeded_search_and_moves.py')
    fixed_table = '\n'.join(
        f"| {r['case']} | {load(FIXED / 'model-audit.json')['cases'][r['case']]['variables']} | "
        f"{r['seconds']:.9f} | {r['inserts']} | {r['solver_upper_bound']:.0f} |"
        for r in fixed['cases'])
    current_ci = ('All six hosted checks for **56f818a** also pass.'
                  if ci['conclusion'] == 'success' else
                  'The **56f818a** hosted checks are still running in the saved snapshot; no later push cancels them.')
    report = f'''# H5: seeded searches and exact local-move bounds — 2026-10-20

**No improved partial or complete layout is found.** The new exact result is
that none of the **331** arrangements reachable by changing zero, one or two
frame/bracket/cog poses about the saved seed can exceed **13 inserts** within
the audited retained pool. This is a local finite-pool statement, not an
unrestricted packing impossibility. H2/H5 remain open; completion stays 60%.

## Seeded searches with fixed cog arrangements

The [previous feasible hints](h5-dominated-poses-and-seeds-20261020.md) seed four
changed integer models. Each selects all 18 frames and 12 brackets together
with actual whole inserts, fixes one original 15-cog arrangement, preserves
all compatible insert choices and old frame exclusions, and maximizes inserts
up to the original cap of 21. All 58 previously audited area rows are
substituted exactly, including tautologies. Every model field and complete
hint is independently checked before solving.

Each case receives one declared 30-second call, eight workers and seed zero:

| Cog case | Variables | Measured seconds | Inserts returned | Final insert bound |
| --- | ---: | ---: | ---: | ---: |
{fixed_table}

All four calls return `FEASIBLE`, retaining only their starting counts.
The bound of 21 does not prove a 13-insert optimum. All callback and final
selections are retained; because they differ, **eight** layouts receive
original geometry checks. Six frozen CLI validations are new and two reuse
byte-verified exact prior layouts/results. Each fails only the unchanged
insert quantity. Soft cleanup overruns are recorded without extending or
repeating a search.

## Restore all cog positions

The existing fully audited **9059-pose** pool contains 1997 frame, 1875 bracket,
1240 insert and 3947 cog poses, with 2,649,582 original conflict edges.
It allows independent cog choices. The later 2260 contact additions have
conditional fixed-cog edges only; they are not silently included in this model.

One pose may replace another of the same family only if they conflict and,
excluding the compared pair, its entire original conflict neighborhood is
contained in the other's. The substitute must be a final survivor. This
preserves family quantities and completion existence within this finite pool.
Independent explicit-set checks verify **2247** replacements, leaving **6812**
poses: 1217 frames, 1593 brackets, 686 inserts and 3316 cogs. The bounded
reduction finishes in 2.255584 seconds after 9,118,943 comparisons.

Mapping the known seed changes five candidate indices. The resulting 58-part
partial passes all 1212 original same-sheet pair checks, with minimum clearance
0.201000 mm, and the frozen CLI rejects it only for eight missing inserts.
Its material charge is 4,985,103.45 mm², within the unchanged target, but it is
not a complete job or a native-margin-qualified result.

The new 6812-variable model requires exactly 18 frames, 12 brackets and 15 cogs,
allows 13–21 inserts, preserves every projected conflict and supplies the
complete feasible seed. All 18,704 constraints are reconstructed.
One declared 60-second search returns `FEASIBLE` after **60.397778600 seconds**,
with 13 inserts and final upper bound 21. Its callback and distinct final
selection pass original geometry checks and fail only insert quantity.
The callback reuses the exact newly checked seed result; the final selection
receives a fresh frozen CLI check. No packing improvement is claimed.

## Exhaustive one- and two-core-move checks

Here “core” means the seed's 18 frames, 12 brackets and 15 cogs. Inserts remain
free throughout. The census considers every retained same-family replacement
of one core pose, then every pair of replacements with matching family counts,
while leaving all other core poses fixed. It includes zero changes.

The one-move census finds **23** feasible replacements and **11** distinct
available-insert sets. The two-move extension checks all **990** removed pairs
and **89,371** candidate pairs, finding **307** exact two-move replacements.
Together there are **331** moves and **64** distinct available-insert sets.

For each set, the saved certificate partitions its candidates into original
pairwise-conflicting cliques or singleton vertices. At most one insert can be
selected from each group. Independent explicit-set enumeration reconstructs
every move and exact available-insert set, then checks all **689** cover groups.
Every cover has at most **13** groups. Thus no zero/one/two-core move can improve
the known 13-insert partial within this retained pool, even when all inserts
are reselected. The certificates do not restrict new continuous positions or
larger coordinated moves.

## A bounded larger move remains unresolved

Motivated by that proof, a changed feasibility model asks for **14–21 inserts**
while retaining 39–42 of the original 45 core poses: exactly three to six core
replacements. All original family counts and conflicts remain. The old objective
and hint are removed, because the 13-insert seed is not feasible for this target.
The entire 18,705-constraint model is reconstructed against the audited parent.

Its single declared 30-second, eight-worker, seed-zero call returns `UNKNOWN`
after **{escape['seconds']:.9f} seconds**, with no incumbent. This is neither
a new layout nor proof that three-to-six moves cannot work. The full log and
original timeout remain. There is no retry or hidden continuation.

## Next work and repository state

{next_step}

Prior local commits **6cde1bd** and **56f818a** are now confirmed on remote main.
All six hosted checks for **f6edfb7** pass, superseding its historical pending
snapshots. {current_ci}
Core source and the three READMEs retain their exact reviewed hashes. The
README already identifies the hosted app as a main preview and links the
qualified v0.2.0-alpha.1 release; no release-facing change is needed here.
No reserved held-out file, native quality run or new release is involved.

[Checks]({PREFIX}/checks.json), [fixed searches]({PREFIX}/fixed-results.json),
[free-pool audit]({PREFIX}/free-pool-audit.json), [free search]({PREFIX}/free-results.json),
[two-move certificate audit]({PREFIX}/two-move-audit.json),
[larger-move result]({PREFIX}/escape-result.json), [source/release review]({PREFIX}/source-review.json),
[push confirmation]({PREFIX}/push-confirmation.json),
[previous main CI]({PREFIX}/main-ci-f6edfb7.json), [current main CI snapshot]({PREFIX}/main-ci-56f818a.json),
[raw models, certificates, logs and layouts]({PREFIX}/raw.zip),
and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and hashes verify.
'''
    (OUT.parent / (PREFIX + '.md')).write_text(report, encoding='utf-8', newline='\n')
    note = f'''**N4 seeded search and local-move bounds, 2026-10-20:** [the complete audit](../benchmarks/results/{PREFIX}.md)
preserves four seeded fixed-cog searches and one search with all cog positions
movable; none improves its 12/13-insert starting count. Independent checks verify
2247 safe pose substitutions and all returned geometry. Exhaustive enumeration
and clique certificates prove that all 331 zero/one/two-core moves about the
mapped seed allow at most 13 inserts within the retained finite pool. A changed
three-to-six-move search for at least 14 inserts times out without a candidate;
larger moves and new continuous positions remain unresolved. Next diagnose
compatible insert sets and their exact core blockers before generating changed
contact positions. No unchanged search is repeated and no full-job credit is
awarded. Prior local 6cde1bd and 56f818a are pushed to main; all six f6edfb7
checks pass. The README accurately describes the existing preview. H2/H5
remain open at 60%; runtime and release assets are unchanged.
'''
    previous = subprocess.check_output(['git', 'show', 'HEAD:BENCHMARKS.md'], cwd=ROOT)
    assert (ROOT / 'BENCHMARKS.md').read_bytes() == previous
    append(ROOT / 'BENCHMARKS.md', '\n' + note.replace('../benchmarks/', 'benchmarks/'))
    for name in ['docs/PLAN_V1_1.md', 'docs/V1_1_RESEARCH.md']:
        append(ROOT / name, '\n' + note)
    p = ROOT / 'docs/STATUS.md'
    s = p.read_text(encoding='utf-8')
    marker = '**N4 certified reduction and starting layouts, 2026-10-20:**'
    assert s.count(marker) == 1
    p.write_text(s.replace(marker, note + '\n' + marker), encoding='utf-8', newline='\n')
    append(ROOT / '.gitattributes', f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed': True, 'archive_members': len(manifest),
                      'archive_bytes': archive.stat().st_size,
                      'completion_percent': 60, 'current_main_CI': ci['status'],
                      'current_main_conclusion': ci['conclusion']}), flush=True)

if __name__ == '__main__':
    main()
