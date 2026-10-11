use rmcp::{
    ServerHandler, ServiceExt,
    model::{Implementation, ServerConfig},
    transport::stdio,
};

struct Nestbolt;

impl ServerHandler for Nestbolt {
    fn get_info(&self) -> ServerConfig {
        ServerConfig::default()
            .with_server_info(Implementation::new("nestbolt", env!("CARGO_PKG_VERSION")))
            .with_instructions(format!(
                "Nestbolt development scaffold using {}. No nesting tools are available yet. \
                 import_parts, nest, validate_layout, export_layout and estimate_sheets \
                 are planned for v1. Do not claim this server can produce cutting layouts.",
                nestbolt_core::ENGINE_VERSION
            ))
    }
}

#[tokio::main(flavor = "current_thread")]
async fn main() -> anyhow::Result<()> {
    // stdout belongs exclusively to the MCP transport. Errors go to stderr.
    let service = Nestbolt.serve(stdio()).await?;
    service.waiting().await?;
    Ok(())
}
