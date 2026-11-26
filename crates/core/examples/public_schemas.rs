use nestbolt_core::{
    offcut::OffcutReport,
    project::{Library, NestReport, Request, SheetImport},
    quote::JobQuote,
};

fn main() -> Result<(), serde_json::Error> {
    println!(
        "{}",
        serde_json::to_string_pretty(&serde_json::json!({
            "library.schema.json": schemars::schema_for!(Library),
            "request.schema.json": schemars::schema_for!(Request),
            "nest-report.schema.json": schemars::schema_for!(NestReport),
            "sheet-import.schema.json": schemars::schema_for!(SheetImport),
            "offcut-report.schema.json": schemars::schema_for!(OffcutReport),
            "job-quote.schema.json": schemars::schema_for!(JobQuote),
        }))?
    );
    Ok(())
}
