"""Retain publication evidence and update the release documentation after verification."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/preview-depth-published-20261016'
audit = root/'benchmarks/results/preview-depth-publication-audit-20261016'
audit.mkdir(exist_ok=False)
proof = json.loads((out/'publication-verification.json').read_bytes())
feature = json.loads((root/'benchmarks/results/preview-depth-published-features-20261016/published-binding.json').read_bytes())
assert proof['all_checks_passed'] and feature['all_checks_passed']
assert proof['commit'] == feature['published_commit']
assert proof['all_four_artifacts_have_verified_provenance']
assert proof['stable_latest_and_asset_snapshot_unchanged']
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace(path, before, after):
    text=path.read_text(encoding='utf-8')
    assert text.count(before)==1,(path,before)
    path.write_text(text.replace(before,after),encoding='utf-8',newline='\n')
for name,src in [('tag','output/preview-depth-tag-20261016'),
                 ('original-sequence','output/preview-depth-publication-sequence-20261016'),
                 ('launcher-recovery','output/preview-depth-verification-recovery-20261016')]:
    shutil.copytree(root/src,audit/name)
shutil.copyfile(__file__,audit/'record.py')
shutil.copyfile(root/'output/verify_published_depth_features.py',audit/'feature-wrapper-after-doc-adaptation.py')
shutil.copyfile(root/'output/finish_published_depth_attestations.py',audit/'finish-provenance.py')
original=json.loads((audit/'original-sequence/plan.json').read_bytes())
assert digest(audit/'launcher-recovery/feature-wrapper-before-doc-adaptation.py') == original['helpers']['output/verify_published_depth_features.py']
for name in ['output/check_downloaded_depth_features.py','output/check_downloaded_depth_features.mjs','output/seal_downloaded_depth_features.py','output/verify_preview_depth_dryrun.py']:
    assert digest(root/name) == original['helpers'][name]
write(audit/'completion.json',{'all_published_checks_pass':True,'release':proof['release_url'],
    'commit':proof['commit'],'completed_at':datetime.now(timezone.utc).isoformat(),
    'publication_proof_sha256':digest(out/'publication-verification.json'),
    'feature_binding_sha256':digest(root/'benchmarks/results/preview-depth-published-features-20261016/published-binding.json'),
    'original_sequence_preserved_as_interrupted':True,
    'launcher_recovery':'Explicit Python interpreter; package-check logic and original downloaded assets unchanged.',
    'provenance_recovery':'Sequential checks with the same policy after three concurrent verifiers hit Windows shared-cache locks. Original logs preserved.',
    'feature_wrapper_pre_run_adaptation':'Keep the original archive checks and feature tests; omit obsolete dry-run document mutations, update report paths and published commit description. Captured both wrapper versions before the feature tests began.',
    'package_smokes_executed_once':True,'authored_feature_checks_executed_once':True,
    'no_asset_replaced_or_release_republished':True,'stable_latest':'v0.1.0',
    'registry_publication':False,'milestone_completion_percent':60,'remaining_gates':['H2','H5']})
write(audit/'integrity.json',{p.relative_to(audit).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
    for p in sorted(audit.rglob('*')) if p.is_file()})

report='''# Published preview verification — 2026-10-16

**[v0.2.0-alpha.1 is published](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)**
as a prerelease at `c36baa8145e9e7b51e5667f4e4eaa0242256fc6e`.
The [five release jobs](https://github.com/skulitom/Nestbolt/actions/runs/38882959832)
pass. [Downloaded-package checks](preview-depth-published-20261016/checks.json),
[publication and provenance verification](preview-depth-published-20261016/publication-verification.json)
and [actual Windows feature checks](preview-depth-published-features-20261016.md)
all pass. Stable Latest remains v0.1.0, including the same release ID and every
asset ID, name, size and digest. No registry version was published.

The tag preflight binds the release to the tested product, complete H4 review,
local integration, previous six-job hosted checks and successful dry-run packages.
Only documented evidence and release notes differ from those tested commits.
The [publication audit](preview-depth-publication-audit-20261016/completion.json)
retains that preflight, tag push and ordinary main push, original sequence,
launch error, recovery scripts and byte inventories.

## Published downloads

All three native archives have exactly the expected six members, target
architecture, documents, executable permissions where applicable, and versions.
Linux/macOS executable version checks ran on their native hosted runners; their
binaries were not executed locally. Every release download matches SHA256SUMS
and GitHub's recorded digest. The published Windows MCPB matches its workflow
artifact and native server executable; generated registry metadata validates.

The actual downloaded Windows CLI and MCPB each pass import, nesting, independent
layout validation and the applicable write-confinement checks. Authored LightBurn
fixtures also pass explicit text-repair and mixed-group rejections, then import,
nest and export two rigid editable groups. Lead coverage is ten expected, eight
reserved and two flagged. XML contents/settings/fixed shapes are preserved;
separate SVG/DXF cutting files and repeat exports match. These are functional
checks on CCD1, without a new quality measurement or reserved input evaluation.

All four binary assets have verified GitHub-hosted build provenance, constrained
to this repository, release workflow, exact source commit and tag. Verification
rejects self-hosted runners. Full verifier output and checksums are retained.

## Preserved verification interruptions

The original launcher tried to execute a Python file directly on Windows and
failed with WinError 193 before any package test started. The recovery supplies
the explicit interpreter and uses the unchanged checker and original downloads.
Package tests then pass. Three of four concurrent provenance commands fail
while opening/renaming GitHub CLI's shared Sigstore cache; the fourth succeeds.
Sequential verification of all four assets passes with the same provenance
policy. Original failures remain at their original paths. No package test,
quality search, publication or asset upload is repeated to replace a failure.

Before the authored-feature check starts, its wrapper is adapted to omit obsolete
dry-run documentation edits and to describe the actual published commit. Both
wrapper versions are retained; feature checks and archive integrity checks are
unchanged apart from package/output paths and the pinned commit.

H1, H3, H4 and H6 remain complete: **60% of v1.1**. H2 import acceptance and H5
common-line material use remain open. Release notes disclose those limits. The
hosted browser remains on v0.1.0, and the frozen v1 benchmark claims are unchanged.
'''
(out.parent/(out.name+'.md')).write_text(report,encoding='utf-8',newline='\n')

replace(root/'README.md','''The current development build supports editable LightBurn project nesting, lead-in
allowances and improvements for large curved drawings. The v1.1 plan is still
in progress; [current verification and remaining work](docs/STATUS.md) distinguish
completed features from open checks. Downloaded releases contain the features
listed in their own release notes. The hosted browser was last deployed from
[v0.1.0](https://github.com/skulitom/Nestbolt/actions/runs/38572138348); to try the
newer browser features, [build the development app locally](#browser-app).
The benchmark figures below belong to the frozen `75cbb32` build, not a new
comparison of the development build.''','''**[Try the v0.2.0-alpha.1 preview](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)**
for editable LightBurn project nesting, lead-in allowances and improvements for
large curved drawings. Windows x64, Linux x64 and macOS Apple silicon tools are
available, plus the Windows MCP bundle. Their [published-download checks](benchmarks/results/preview-depth-published-20261016.md)
pass. Import acceptance and common-line material use remain under development;
the [v1.1 plan is 60% complete](docs/STATUS.md). Stable v0.1.0 remains available.

The hosted browser still runs [v0.1.0](https://github.com/skulitom/Nestbolt/actions/runs/38572138348).
To try the newer browser features, [build the app locally](#browser-app).
The benchmark figures below belong to the frozen `75cbb32` build; this preview
makes no new comparison against competing tools.''')
replace(root/'README.md','''silicon** from [Releases](https://github.com/skulitom/Nestbolt/releases). Each
archive contains''','''silicon** from the [v0.2.0-alpha.1 preview](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
or [stable v0.1.0](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0). Each
archive contains''')
replace(root/'README.md','''[Open it](https://skulitom.github.io/Nestbolt/) and pick an example (finger-jointed
boxes, letters inside letters, a 138-part mechanical kit, a FreeSewing T-shirt
pattern on a fabric roll, interlocking gears), or drop your own SVG/DXF files or
one LightBurn project.''','''[Open the hosted v0.1.0 app](https://skulitom.github.io/Nestbolt/) and pick an example
(finger-jointed boxes, letters inside letters, a 138-part mechanical kit, a
FreeSewing T-shirt pattern on a fabric roll, interlocking gears), or drop your
own SVG/DXF files. LightBurn import, lead allowances and the newer large-drawing
features are available in the local build described below.''')

replace(root/'docs/STATUS.md','The goal is active under [PLAN_V1_1.md](PLAN_V1_1.md).','The plan is tracked in [PLAN_V1_1.md](PLAN_V1_1.md).')
replace(root/'docs/STATUS.md','''including a README update. Preview `0.2.0-alpha.1` is being prepared; a new candidate
passes its full quality, scale and export-fidelity review; this does not close the remaining v1.1 gates
or authorize a new final acceptance run. Registry publication remains separate.''','''including a README update. [Preview v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is now published at `c36baa8`; [actual download and provenance checks](../benchmarks/results/preview-depth-published-20261016.md)
and [Windows LightBurn/lead workflows](../benchmarks/results/preview-depth-published-features-20261016.md)
pass. Stable Latest and its assets remain v0.1.0. This does not close the remaining
v1.1 gates or authorize a new final acceptance run. No new registry version was published.''')
replace(root/'docs/STATUS.md','''is integrated. No preview tag or release exists; completed milestone weight is 60%.''','''is integrated. The qualified preview is now published and verified; completed
milestone weight remains 60%. The release record above supersedes the earlier
dry-run and prepublication checkpoints.''')

replace(root/'docs/RELEASE_READINESS.md','# Next preview release','# Published preview v0.2.0-alpha.1')
replace(root/'docs/RELEASE_READINESS.md','''candidate `aba989e` is version `0.2.0-alpha.1`; it passes local integration,''','''product candidate `aba989e` was released as `v0.2.0-alpha.1` at `c36baa8`;
the [published downloads and provenance](../benchmarks/results/preview-depth-published-20261016.md)
and [Windows feature workflows](../benchmarks/results/preview-depth-published-features-20261016.md)
pass. It also passes local integration,''')
replace(root/'docs/RELEASE_READINESS.md','''  is now complete. Verify the chosen tag commit retains those tested inputs
  before publication, then verify the actual published downloads.''','''  is now complete. The [tag preflight](../benchmarks/results/preview-depth-publication-audit-20261016/tag/preflight.json)
  verifies unchanged tested product inputs, and the actual published downloads
  have subsequently passed all checks.''')
replace(root/'docs/RELEASE_READINESS.md','''After all current-candidate checks pass, publish the verified `v0.2.0-alpha.1`
as a prerelease without replacing stable Latest. Verify actual published
downloads, checksums and source/tag provenance, including the Windows bundle.
Evidence-only commits must retain the tested product digest. No preview tag
or release has been created. Registry publication remains separate.''','''[v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is published as a prerelease; stable Latest remains v0.1.0 with unchanged assets.
All five release jobs pass. Actual downloads match their checksums, package
contents and exact source/tag provenance; Windows CLI/MCPB import, nesting,
validation, confinement and authored LightBurn/lead workflows pass. The
[publication audit](../benchmarks/results/preview-depth-publication-audit-20261016/completion.json)
preserves the original launcher and shared-cache errors and their limited
verification recoveries. No release asset was replaced or redownloaded during
recovery. Registry publication remains separate and was not performed.''')
replace(root/'docs/RELEASE_READINESS.md','''acceptance comparison remain separate actions. No preview tag or release exists yet.''','''acceptance comparison remain separate actions. H2/H5 remain open at 60% completed weight.''')
replace(root/'mcpb/PUBLISHING.md','''[reviewed decision 7](../docs/PLAN_V1_1.md#10-reviewed-decisions). The next preview
still needs its release checks. Registry publication is a separate step.''','''[reviewed decision 7](../docs/PLAN_V1_1.md#10-reviewed-decisions).
[v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is published as a prerelease with [verified downloads and provenance](../benchmarks/results/preview-depth-published-20261016.md).
Stable Latest remains v0.1.0. Registry publication is a separate step; this
preview did not publish a registry version.''')

checkpoint='''

**Preview published, 2026-10-16:** [v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is published at `c36baa8` under Artem's release authorization. All five release
jobs pass; [actual downloads and all four build attestations](../benchmarks/results/preview-depth-published-20261016.md)
verify, including exact tag/source binding and unchanged stable Latest/assets.
[Published Windows CLI/MCPB feature checks](../benchmarks/results/preview-depth-published-features-20261016.md)
pass with authored inputs only. The original Python-launch and shared-cache
verification errors remain preserved alongside their limited recoveries.
The README links the preview and separates hosted v0.1.0 from newer local
browser features. No new registry version, reserved evaluation or public
competitor claim. H2/H5 remain open; completed milestone weight stays 60%.
'''
for rel in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    with (root/rel).open('a',encoding='utf-8',newline='\n') as f:f.write(checkpoint)
before=(root/'BENCHMARKS.md').read_bytes()
assert before.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — v0.2.0-alpha.1 published and actual downloads verified

[The qualified preview](benchmarks/results/preview-depth-published-20261016.md)
is published at `c36baa8`; all five release jobs pass. Three native archives and
the Windows MCPB match checksums, contents and target architectures. All four
binary assets have verified GitHub-hosted provenance for the exact repository,
workflow, source commit and tag. Stable Latest v0.1.0 and all its assets remain
unchanged. Linux/macOS version checks ran on their native hosted runners.

[Actual Windows CLI and MCPB feature checks](benchmarks/results/preview-depth-published-features-20261016.md)
pass alongside import/nest/validate and confinement checks: two explicit
rejections per surface, two preserved rigid groups, ten expected/eight reserved/
two flagged leads, separate cutting files and identical repeat exports.
The 57-member raw archive is 2,874,696 bytes, SHA-256
d1c0d9bd3153328888a1580ae8b33386ded2d88402667d8a66c9d404ed3c037d;
CRC and every member length/hash pass. All functional checks run on CCD1.

The original Python launcher error occurred before package tests. Its explicit
interpreter recovery preserves all downloads and checker logic. Three concurrent
provenance commands then hit Windows shared-cache locks; sequential verification
passes unchanged policy, retaining every original log. No package/search test
or publication is repeated to replace a failed outcome. The feature wrapper was
adapted before execution only for published paths/commit and current reporting.

README and release records distinguish preview features from hosted v0.1.0,
disclose import/common-line limits and retain frozen v1 comparison claims.
No registry publication or reserved evaluation. H2/H5 remain open; completed
milestone weight stays 60%. All isolated H5 candidates remain unintegrated.
''')
assert (root/'BENCHMARKS.md').read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:
    for name in [out.name,audit.name,'preview-depth-published-features-20261016']:
        f.write('\nbenchmarks/results/'+name+'/** -text -whitespace\n')
print(json.dumps({'publication_recorded':True,'published_features_verified':True,'documentation_updated':True}))
