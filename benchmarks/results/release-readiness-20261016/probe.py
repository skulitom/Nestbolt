"""Preserve the failed CI log and reproduce it without changing measured sources."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'benchmarks/results/release-readiness-20261016'
PROBE = ROOT / 'output/ci-curve-probe'
sys.path.insert(0, str(ROOT / 'scripts'))
import h4_full_matrix as full

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')

def run(command, name, env=None):
    with (OUT / (name + '-stdout.txt')).open('wb') as out, (OUT / (name + '-stderr.txt')).open('wb') as err:
        proc = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err, env=env,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        psutil.Process(proc.pid).cpu_affinity(list(range(16, 32)))
        code = proc.wait(timeout=900)
    return {'command': [str(p) for p in command], 'exit_code': code,
            'stdout_sha256': digest(OUT / (name + '-stdout.txt')),
            'stderr_sha256': digest(OUT / (name + '-stderr.txt'))}

OUT.mkdir(exist_ok=False)
PROBE.mkdir(exist_ok=False)
(PROBE / 'src').mkdir()
plan = full.load(ROOT / 'benchmarks/results/h4-full-development-20261015/plan.json')
before = full.guards(full.cases())
assert before == plan['guards']
log = subprocess.check_output(['gh', 'api', 'repos/skulitom/Nestbolt/actions/jobs/116712070745/logs'], cwd=ROOT)
(OUT / 'linux-ci-job.log').write_bytes(log)
assert b'random_curved_svg_parts_nest_validly' in log and b'minimal failing input' in log
manifest = '''[package]
name = "nestbolt-ci-curve-probe"
version = "0.0.0"
edition = "2024"
[workspace]
[dependencies]
nestbolt-core = { path = "../../crates/core" }
nestbolt-validator = { path = "../../crates/validator" }
jagua-rs = { version = "=1.1.0", features = ["bpp", "spp"] }
serde_json = "1.0"
[profile.dev.package."*"]
opt-level = 3
'''
(PROBE / 'Cargo.toml').write_text(manifest, encoding='utf-8', newline='\n')
shutil.copyfile(ROOT / 'Cargo.lock', PROBE / 'Cargo.lock')
source = r'''use jagua_rs::{collision_detection::quadtree::qt_traits::QTQueryable, geometry::primitives::{Edge, Point, Rect}};
use nestbolt_core::{clock::Timing, project::{Library, Request}, sheets::{Options, optimize}};
use nestbolt_validator::job::validate;
fn main() {
    if std::env::args().nth(1).as_deref() == Some("primitive") {
        let edge = Edge { start: Point(21.975176, -22.350315), end: Point(22.223839, -22.143082) };
        let rect = Rect { x_min: 21.743834, y_min: -22.61575, x_max: 22.61575, y_max: -21.743834 };
        let quadrants = rect.quadrants();
        println!("{:?}", edge.collides_with_quadrants(&rect, [&quadrants[0], &quadrants[1], &quadrants[2], &quadrants[3]]));
        return;
    }
    let circles = [(12.478479167719012_f64, 0.0_f64, 1_u32), (2.6805745106261756, 0.0, 2), (13.120391613622374, 0.0, 1)];
    let (rx, ry, bulge, seed) = (2.0, 5.610405755197782, 0.1, 659);
    let mut elements = String::new();
    for (i, (r, offset, _)) in circles.iter().enumerate() {
        let x = 40.0 * i as f64 + 20.0;
        let h = r * 0.3;
        elements += &format!(r#"<path id="ring{i}" fill-rule="evenodd" d="M {a} 20 A {r} {r} 0 1 0 {b} 20 A {r} {r} 0 1 0 {a} 20 Z M {c} 20 A {h} {h} 0 1 0 {d} 20 A {h} {h} 0 1 0 {c} 20 Z"/>"#,
            a = x - r, b = x + r, c = x - h + offset * (r - h) * 0.9, d = x + h + offset * (r - h) * 0.9);
    }
    elements += &format!(r#"<ellipse id="tab" cx="60" cy="70" rx="{rx}" ry="{ry}"/>"#);
    elements += &format!(r#"<path id="lens" d="M 100 70 A {bulge} {bulge} 0 0 1 112 70 A {bulge} {bulge} 0 0 1 100 70 Z"/>"#);
    let svg = format!(r#"<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="100mm" viewBox="0 0 200 100">{elements}</svg>"#);
    let out = std::path::PathBuf::from(std::env::args().nth(2).expect("output folder"));
    std::fs::create_dir(&out).unwrap();
    std::fs::write(out.join("input.svg"), &svg).unwrap();
    let library = Library::import(&[("fuzz.svg".to_owned(), svg)], &Default::default()).unwrap();
    let quantities: Vec<u32> = circles.iter().map(|c| c.2).collect();
    let parts: Vec<_> = library.parts.iter().enumerate().map(|(i,p)| serde_json::json!({
        "id":p.id,"quantity":quantities.get(i).copied().unwrap_or(2),"rotations":{"kind":"free"}
    })).collect();
    let request: Request = serde_json::from_value(serde_json::json!({
        "parts":parts,"sheets":[{"width_mm":120,"height_mm":80,"margins_mm":{"left":2,"right":2,"bottom":2,"top":2}}],
        "spacing_mm":0.5,"edge_spacing_mm":0.5
    })).unwrap();
    let (job, _) = request.job(&library).unwrap();
    std::fs::write(out.join("job.json"), serde_json::to_vec_pretty(&job).unwrap()).unwrap();
    let result = optimize(&job, Options {seconds:2.0, seed, timing:Timing::Work, ..Options::default()}, |_,_|{}).unwrap();
    assert!(result.validation.valid);
    assert!(validate(&job,&result.layout).unwrap().valid);
    std::fs::write(out.join("result.json"),serde_json::to_vec_pretty(&result).unwrap()).unwrap();
    println!("independent validation passed for {} placements", result.layout.placements.len());
}
'''
(PROBE / 'src/main.rs').write_text(source, encoding='utf-8', newline='\n')
shutil.copyfile(PROBE / 'src/main.rs', OUT / 'probe.rs')
shutil.copyfile(PROBE / 'Cargo.toml', OUT / 'probe-Cargo.toml')
shutil.copyfile(__file__, OUT / 'probe.py')
env = os.environ.copy()
env['CARGO_TARGET_DIR'] = str(ROOT / 'target')
env['RUST_BACKTRACE'] = '1'
result = {'created_utc':datetime.now(timezone.utc).isoformat(), 'ci_run':38819422170,
          'ci_job':116712070745, 'ci_commit':'e897e91182e2e5b457f905a92c05465c0efa8ea8',
          'ci_log_sha256':digest(OUT/'linux-ci-job.log'), 'before_guard_matches':True,
          'scope':'Functional reproduction on CCD1; no benchmark, no production edits.', 'steps':{}}
result['steps']['build'] = run(['cargo','build','--offline','--manifest-path',str(PROBE/'Cargo.toml')], 'build', env)
write(OUT/'probe-results.json', result)
if result['steps']['build']['exit_code'] == 0:
    binary = ROOT/'target/debug/nestbolt-ci-curve-probe.exe'
    result['steps']['primitive'] = run([binary,'primitive'],'primitive',env)
    write(OUT/'probe-results.json', result)
    result['steps']['search'] = run([binary,'search',OUT/'search'],'search',env)
result['after_guard_matches'] = full.guards(full.cases()) == before
assert result['after_guard_matches']
write(OUT/'probe-results.json', result)
print(json.dumps(result,indent=2))
