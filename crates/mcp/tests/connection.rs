use rmcp::{ServiceExt, transport::TokioChildProcess};
use std::time::Duration;
use tokio::{process::Command, time::timeout};

#[tokio::test(flavor = "current_thread")]
async fn native_binary_negotiates_mcp_without_advertising_unbuilt_tools() {
    timeout(Duration::from_secs(10), async {
        let transport =
            TokioChildProcess::new(Command::new(env!("CARGO_BIN_EXE_nestbolt-mcp"))).unwrap();
        let client = ().serve(transport).await.unwrap();
        let info = client.peer_info().unwrap();
        assert_eq!(info.server_info.as_ref().unwrap().name, "nestbolt");
        assert!(info.capabilities.tools.is_none());
        assert!(
            info.instructions
                .as_ref()
                .unwrap()
                .contains("No nesting tools")
        );
        client.cancel().await.unwrap();
    })
    .await
    .expect("MCP handshake timed out");
}
