use rmcp::{ServiceExt, model::CallToolRequestParams, transport::TokioChildProcess};
use serde_json::{Value, json};
use std::time::Duration;
use tokio::{process::Command, time::timeout};

fn args(value: Value) -> serde_json::Map<String, Value> {
    value.as_object().unwrap().clone()
}

#[tokio::test(flavor = "current_thread")]
async fn tools_import_nest_validate_export_and_estimate_inside_the_workspace() {
    let workspace = std::env::temp_dir().join(format!("nestbolt-mcp-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&workspace);
    std::fs::create_dir_all(&workspace).unwrap();
    std::fs::copy(
        concat!(env!("CARGO_MANIFEST_DIR"), "/../../examples/parts.svg"),
        workspace.join("parts.svg"),
    )
    .unwrap();
    timeout(Duration::from_secs(120), async {
        let mut command = Command::new(env!("CARGO_BIN_EXE_nestbolt-mcp"));
        command.env("NESTBOLT_WORKSPACE", &workspace);
        let client = ().serve(TokioChildProcess::new(command).unwrap()).await.unwrap();
        let info = client.peer_info().unwrap();
        assert_eq!(info.server_info.as_ref().unwrap().name, "nestbolt");
        let mut names: Vec<_> = client
            .list_all_tools()
            .await
            .unwrap()
            .into_iter()
            .map(|t| t.name.to_string())
            .collect();
        names.sort();
        assert_eq!(names, ["estimate_sheets", "export_layout", "import_parts", "nest", "validate_layout"]);

        let call = |name: &'static str, value: Value| {
            let client = &client;
            async move {
                client
                    .call_tool(CallToolRequestParams::new(name).with_arguments(args(value)))
                    .await
            }
        };
        let imported = call("import_parts", json!({"paths": ["parts.svg"]})).await.unwrap();
        let imported = imported.structured_content.unwrap();
        assert_eq!(imported["part_count"], 4);
        let library = imported["library_path"].as_str().unwrap().to_owned();
        let request = json!({
            "parts": [{"id": "parts-1", "quantity": 2}, {"id": "parts-2", "quantity": 6},
                      {"id": "parts-3", "quantity": 2}, {"id": "parts-4", "quantity": 3}],
            "sheets": [{"width_mm": 300, "height_mm": 200, "margins_mm": {"left": 3, "right": 3, "bottom": 3, "top": 3}}],
            "spacing_mm": 1.0, "edge_spacing_mm": 1.0
        });
        let mut layouts = vec![];
        let mut repeatable = true;
        for run in ["a", "b"] {
            let nested = call("nest", json!({"library_path": library, "request": request,
                "time_budget_s": 5, "seed": 3, "out_dir": format!("runs/{run}")}))
                .await
                .unwrap()
                .structured_content
                .unwrap();
            assert_eq!(nested["validation"]["valid"], true);
            assert!(nested["files"].as_array().unwrap().len() >= 2);
            // A slow (debug) build may reach the real-time limit first; that
            // run is reported as not repeatable and need not match.
            repeatable &= nested["repeatable"] == true;
            layouts.push(std::fs::read(workspace.join(nested["layout_path"].as_str().unwrap())).unwrap());
        }
        if repeatable && layouts[0] != layouts[1] {
            panic!("the same seed and budget gave different layouts");
        }
        let checked = call("validate_layout", json!({"library_path": library, "request": request,
            "layout_path": "runs/a/layout.json"})).await.unwrap().structured_content.unwrap();
        assert_eq!(checked["valid"], true);
        let exported = call("export_layout", json!({"library_path": library, "request": request,
            "layout_path": "runs/a/layout.json", "out_dir": "export", "sheet_outline": true}))
            .await.unwrap().structured_content.unwrap();
        assert!(exported["files"][0].as_str().unwrap().ends_with(".svg"));
        let estimate = call("estimate_sheets", json!({"library_path": library, "request": request}))
            .await.unwrap().structured_content.unwrap();
        assert!(estimate["sheets_lower_bound"].as_f64().unwrap() >= 1.0);
        // Paths outside the workspace are refused with an actionable message.
        let outside = call("import_parts", json!({"paths": ["../outside.svg"]})).await.unwrap_err();
        assert!(format!("{outside}").contains("workspace") || format!("{outside}").contains(".."));
        client.cancel().await.unwrap();
    })
    .await
    .expect("MCP session timed out");
    let _ = std::fs::remove_dir_all(&workspace);
}
