use nestbolt_core::{clock::Timing, project::{Library, Request}, sheets::{Options, optimize}};
use nestbolt_validator::job::validate;
fn main() {
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
