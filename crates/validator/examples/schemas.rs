use nestbolt_validator::job::{Job, Layout, Report};

fn main() -> Result<(), serde_json::Error> {
    println!(
        "{}",
        serde_json::to_string_pretty(&serde_json::json!({
            "benchmark-job.schema.json": schemars::schema_for!(Job),
            "benchmark-layout.schema.json": schemars::schema_for!(Layout),
            "benchmark-validation.schema.json": schemars::schema_for!(Report),
        }))?
    );
    Ok(())
}
