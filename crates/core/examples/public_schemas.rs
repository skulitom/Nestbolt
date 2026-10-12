use nestbolt_core::project::{Library, NestReport, Request};

fn main() -> Result<(), serde_json::Error> {
    println!(
        "{}",
        serde_json::to_string_pretty(&serde_json::json!({
            "library.schema.json": schemars::schema_for!(Library),
            "request.schema.json": schemars::schema_for!(Request),
            "nest-report.schema.json": schemars::schema_for!(NestReport),
        }))?
    );
    Ok(())
}
