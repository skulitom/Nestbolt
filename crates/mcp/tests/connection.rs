use rmcp::{ServiceExt, model::CallToolRequestParams, transport::TokioChildProcess};
use serde_json::{Value, json};
use std::time::Duration;
use tokio::{process::Command, time::timeout};

fn args(value: Value) -> serde_json::Map<String, Value> {
    value.as_object().unwrap().clone()
}

#[tokio::test(flavor = "current_thread")]
async fn lead_allowances_report_flags_and_revalidate_identically() {
    let stamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let workspace =
        std::env::temp_dir().join(format!("nestbolt-mcp-leads-{}-{stamp}", std::process::id()));
    std::fs::create_dir_all(&workspace).unwrap();
    std::fs::write(
        workspace.join("leads.svg"),
        include_str!("../../core/tests/fixtures/leads.svg"),
    )
    .unwrap();
    timeout(Duration::from_secs(90),async {
        let mut command=Command::new(env!("CARGO_BIN_EXE_nestbolt-mcp"));command.env("NESTBOLT_WORKSPACE",&workspace);
        let client=().serve(TokioChildProcess::new(command).unwrap()).await.unwrap();
        let call=|name:&'static str,value:Value|{let client=&client;async move {
            client.call_tool(CallToolRequestParams::new(name).with_arguments(args(value))).await
        }};
        let imported=call("import_parts",json!({"paths":["leads.svg"]})).await.unwrap().structured_content.unwrap();
        let library=&imported["library_path"];
        let request=json!({"parts":[{"id":"leads-1","quantity":2}],"sheets":[{"width_mm":60,"height_mm":35}],
            "spacing_mm":0.2,"edge_spacing_mm":1,"lead_in":{"kerf_mm":0.2}});
        let nested=call("nest",json!({"library_path":library,"request":request,"out_dir":"nested","time_budget_s":1})).await.unwrap().structured_content.unwrap();
        assert_eq!(nested["validation"]["valid"],true);
        assert_eq!(nested["lead_in"]["expected_contours"],6);assert_eq!(nested["lead_in"]["flagged_contours"],2);
        assert_eq!(nested["lead_in"]["options"]["length_mm"],3.0);
        let checked=call("validate_layout",json!({"library_path":library,"request":request,"layout_path":"nested/layout.json"})).await.unwrap().structured_content.unwrap();
        assert_eq!(nested["lead_in"],checked["lead_in"]);
        assert_eq!(nested["validation"]["metrics"],checked["metrics"]);
        let exported=call("export_layout",json!({"library_path":library,"request":request,"layout_path":"nested/layout.json","out_dir":"exported"})).await.unwrap().structured_content.unwrap();
        assert_eq!(nested["lead_in"],exported["lead_in"]);
        for file in exported["files"].as_array().unwrap() {
            let name=file.as_str().unwrap();let text=std::fs::read_to_string(workspace.join(name)).unwrap();
            assert!(text.contains("LEADIN"));
            assert_eq!(text,std::fs::read_to_string(workspace.join("nested").join(std::path::Path::new(name).file_name().unwrap())).unwrap());
        }
        let mut bad=request;bad["lead_in"]["length_mm"]=json!(0.4);
        assert!(call("nest",json!({"library_path":library,"request":bad,"out_dir":"bad","time_budget_s":1})).await.unwrap_err().to_string().contains("between 0.5 and 50"));
        client.cancel().await.unwrap();
    }).await.unwrap();
}

#[tokio::test(flavor = "current_thread")]
async fn common_line_parameter_controls_spacing_and_export_report() {
    let stamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let workspace = std::env::temp_dir().join(format!(
        "nestbolt-mcp-common-{}-{stamp}",
        std::process::id()
    ));
    std::fs::create_dir_all(&workspace).unwrap();
    std::fs::write(
        workspace.join("panel.svg"),
        include_str!("../../core/tests/fixtures/common-panels.svg"),
    )
    .unwrap();
    timeout(Duration::from_secs(90),async {
        let mut command=Command::new(env!("CARGO_BIN_EXE_nestbolt-mcp"));command.env("NESTBOLT_WORKSPACE",&workspace);
        let client=().serve(TokioChildProcess::new(command).unwrap()).await.unwrap();
        let call=|name:&'static str,value:Value|{let client=&client;async move {
            client.call_tool(CallToolRequestParams::new(name).with_arguments(args(value))).await
        }};
        let imported=call("import_parts",json!({"paths":["panel.svg"]})).await.unwrap().structured_content.unwrap();
        let library=&imported["library_path"];
        let request=json!({"parts":[{"id":"panel-1","quantity":2}],"sheets":[{"width_mm":86,"height_mm":36}],
            "spacing_mm":5,"edge_spacing_mm":1,"common_line":{"kerf_mm":0.2}});
        let nested=call("nest",json!({"library_path":library,"request":request,"out_dir":"nested","time_budget_s":1})).await.unwrap().structured_content.unwrap();
        assert_eq!(nested["validation"]["valid"],true);assert_eq!(nested["parts_in_holes"],0);
        assert!((nested["common_line"][0]["saved_length_mm"].as_f64().unwrap()-30.0).abs()<0.01);
        let exported=call("export_layout",json!({"library_path":library,"request":request,"layout_path":"nested/layout.json", "out_dir":"exported","format":"svg"})).await.unwrap().structured_content.unwrap();
        assert_eq!(nested["common_line"],exported["common_line"]);
        let svg=std::fs::read_to_string(workspace.join(exported["files"][0].as_str().unwrap())).unwrap();assert!(svg.contains("id=\"COMMON\""));
        let mut bad=request;bad["common_line"]["kerf_mm"]=json!(0.01);
        let error=call("nest",json!({"library_path":library,"request":bad,"out_dir":"bad","time_budget_s":1})).await.unwrap_err();
        assert!(error.to_string().contains("at least 0.05"));
        client.cancel().await.unwrap();
    }).await.unwrap();
}

#[tokio::test(flavor = "current_thread")]
async fn lightburn_units_nest_and_export_without_losing_project_settings() {
    let stamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let workspace = std::env::temp_dir().join(format!(
        "nestbolt-mcp-lightburn-{}-{stamp}",
        std::process::id()
    ));
    std::fs::create_dir_all(&workspace).unwrap();
    std::fs::write(
        workspace.join("roundtrip.lbrn2"),
        include_str!("../../core/tests/fixtures/roundtrip.lbrn2"),
    )
    .unwrap();
    timeout(Duration::from_secs(120),async {
        let mut command = Command::new(env!("CARGO_BIN_EXE_nestbolt-mcp"));
        command.env("NESTBOLT_WORKSPACE",&workspace);
        let client = ().serve(TokioChildProcess::new(command).unwrap()).await.unwrap();
        let call = |name:&'static str,value:Value| {
            let client = &client;
            async move {client.call_tool(CallToolRequestParams::new(name).with_arguments(args(value))).await}
        };
        let imported = call("import_parts",json!({"paths":["roundtrip.lbrn2"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(imported["part_count"],3);
        assert_eq!(imported["lightburn"]["layers"][0]["kerf_mm"],0.2);
        assert!(imported["lightburn"].get("xml").is_none());
        let library = imported["library_path"].as_str().unwrap();
        let request = json!({"sheets":[{"width_mm":34,"height_mm":24}],"spacing_mm":1,"edge_spacing_mm":0.5});
        let estimate = call("estimate_sheets",json!({"library_path":library,"request":request})).await.unwrap().structured_content.unwrap();
        let expected:f64 = imported["parts"].as_array().unwrap().iter().map(|p|p["area_mm2"].as_f64().unwrap()).sum();
        // Import areas use the validator's 1e-6 mm grid; the estimator uses
        // unrounded bitmap corners. Their area difference is below 0.0001 mm².
        assert!((estimate["net_part_area_mm2"].as_f64().unwrap()-expected).abs()<1e-4);
        let nested = call("nest",json!({"library_path":library,"request":request,"out_dir":"nested","time_budget_s":1})).await.unwrap().structured_content.unwrap();
        assert_eq!(nested["validation"]["valid"],true);
        assert!(nested["files"].as_array().unwrap().len()>=2);
        for file in nested["files"].as_array().unwrap() {
            let file = file.as_str().unwrap();
            assert!(file.ends_with(".lbrn2"));
            let xml = std::fs::read_to_string(workspace.join(file)).unwrap();
            assert!(xml.contains("Original MIT rigid-unit integration fixture"));
            let doc = nestbolt_core::lightburn::Document::read(&xml,0.005).unwrap();
            assert!(doc.scene.shapes.iter().any(|s|s.fixed&&s.bounds_mm==Some([0.0,0.0,34.0,24.0])));
        }
        let exported = call("export_layout",json!({"library_path":library,"request":request,
            "layout_path":"nested/layout.json","out_dir":"without-outline","format":"lbrn2","sheet_outline":false})).await.unwrap().structured_content.unwrap();
        for file in exported["files"].as_array().unwrap() {
            let xml = std::fs::read_to_string(workspace.join(file.as_str().unwrap())).unwrap();
            let doc = nestbolt_core::lightburn::Document::read(&xml,0.005).unwrap();
            assert!(!doc.scene.shapes.iter().any(|s|s.fixed&&s.bounds_mm==Some([0.0,0.0,34.0,24.0])));
        }
        let lossy = call("export_layout",json!({"library_path":library,"request":request,
            "layout_path":"nested/layout.json","out_dir":"lossy","format":"svg"})).await.unwrap_err();
        assert!(lossy.to_string().contains("retain its text"));
        std::fs::write(workspace.join("legacy.lbrn"), include_str!("../../core/tests/fixtures/legacy.lbrn")).unwrap();
        let legacy = call("import_parts",json!({"paths":["legacy.lbrn"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(legacy["part_count"],1);
        let legacy_nested = call("nest",json!({"library_path":legacy["library_path"],
            "request":{"sheets":[{"width_mm":34,"height_mm":14}],"spacing_mm":1,"edge_spacing_mm":0.5},
            "out_dir":"legacy-nested","time_budget_s":1})).await.unwrap().structured_content.unwrap();
        assert_eq!(legacy_nested["validation"]["valid"],true);
        assert_eq!(legacy_nested["files"].as_array().unwrap().len(),1);
        let xml = std::fs::read_to_string(workspace.join(legacy_nested["files"][0].as_str().unwrap())).unwrap();
        assert_eq!(nestbolt_core::lightburn::Document::read(&xml,0.005).unwrap().scene.format_version,1);
        assert_eq!(xml.matches("<VertList>").count(),2);
        assert_eq!(xml.matches("<PrimList>").count(),2);
        assert!(xml.contains("Future=\"a &amp; b\""));
        client.cancel().await.unwrap();
    }).await.expect("LightBurn MCP session timed out");
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
        std::fs::write(workspace.join("gap.svg"),r#"<svg width="50mm" viewBox="0 0 50 50"><path id="outline" d="M0 0 H20 V20 H0 V0.2"/><rect x="30" width="10" height="10"/></svg>"#).unwrap();
        let open=call("import_parts",json!({"paths":["gap.svg"]})).await.unwrap_err();
        assert!(format!("{open}").contains("Close gaps up to 0.200000 mm"));
        assert!(format!("{open}").contains("no partial library was created"));
        let repaired=call("import_parts",json!({"paths":["gap.svg"],"close_gaps_mm":0.2})).await.unwrap().structured_content.unwrap();
        assert_eq!(repaired["part_count"],2);
        assert_eq!(repaired["imports"][0]["report"]["closed_gaps"][0]["size_mm"],0.2);
        std::fs::write(workspace.join("layers.svg"),r##"<svg width="100mm" viewBox="0 0 100 100"><g id="CUT" stroke="black"><rect width="20" height="20"/></g><g id="SCORE" stroke="red"><rect x="40" width="10" height="10"/><text>label</text></g></svg>"##).unwrap();
        for (selection,expected_x) in [(json!({"paths":["layers.svg"],"layers":["SCORE"]}),40.0),
            (json!({"paths":["layers.svg"],"colors":["#000000"]}),0.0)] {
            let selected=call("import_parts",selection).await.unwrap().structured_content.unwrap();
            assert_eq!(selected["part_count"],1);
            assert_eq!(selected["parts"][0]["bounds_mm"][0],expected_x);
            assert_eq!(selected["imports"][0]["report"]["layers"].as_array().unwrap().len(),2);
        }
        std::fs::write(workspace.join("cleanup.svg"),r#"<svg width="100mm" viewBox="0 0 100 100"><path d="M0 0 H12 M8 0 H20 V20 H0 V0 M20 0 V20 M0 0 L0 0"/></svg>"#).unwrap();
        let cleaned=call("import_parts",json!({"paths":["cleanup.svg"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(cleaned["part_count"],1);
        assert_eq!(cleaned["imports"][0]["report"]["cleanup"],json!({"duplicate_segments_removed":1,"zero_length_segments_removed":1,"overlapping_segments_merged":1}));
        std::fs::write(workspace.join("closed-retrace.svg"),include_str!("../../core/tests/fixtures/closed-retrace.svg")).unwrap();
        let retraced=call("import_parts",json!({"paths":["closed-retrace.svg"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(retraced["parts"].as_array().unwrap().len(),1);
        assert_eq!(retraced["parts"][0]["holes"],1);
        assert_eq!(retraced["imports"][0]["report"]["cleanup"]["closed_path_overlaps_preserved"],2);
        assert!(retraced["warnings"].as_array().unwrap().iter().any(|w| w.as_str().unwrap().contains("keep closed paths connected")));
        std::fs::write(workspace.join("viewport.svg"),include_str!("../../core/tests/fixtures/viewport.svg")).unwrap();
        std::fs::write(workspace.join("width.dxf"),include_str!("../../core/tests/fixtures/polyline-width.dxf")).unwrap();
        let physical=call("import_parts",json!({"paths":["viewport.svg","width.dxf"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(physical["part_count"],2);
        for (value,expected) in physical["parts"][0]["bounds_mm"].as_array().unwrap().iter().zip([65.4,-62.7,85.4,-42.7]) {
            assert!((value.as_f64().unwrap()-expected).abs()<1e-9);
        }
        assert_eq!(physical["parts"][1]["bounds_mm"],json!([0.0,0.0,10.0,5.0]));
        assert!(physical["warnings"].as_array().unwrap().iter().any(|w|w.as_str().unwrap().contains("polyline widths ignored")));
        let legacy="0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\nCUT_Ø\n70\n1\n90\n4\n10\n0\n20\n0\n10\n20\n20\n0\n10\n20\n20\n10\n10\n0\n20\n10\n0\nENDSEC\n0\nEOF\n";
        std::fs::write(workspace.join("arranged.svg"),include_str!("../../core/tests/fixtures/prearranged-sheet.svg").replace("id=\"SHEET\"","id=\"MATERIAL\"")).unwrap();
        let arranged=call("import_parts",json!({"paths":["arranged.svg"],"sheet_layers":["MATERIAL"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(arranged["part_count"],2);
        assert_eq!(arranged["sheet_outlines"][0]["width_mm"],200.0);
        assert!(arranged["sheet_outlines"][0].get("outline_mm").is_none(),"heavy geometry stays in the library");
        let sheet_request=json!({"sheets":[{"from_import":"arranged-sheet-1","count":1}],"spacing_mm":1,"edge_spacing_mm":1});
        let on_sheet=call("nest",json!({"library_path":arranged["library_path"],"request":sheet_request,"time_budget_s":2,"out_dir":"sheet-run"})).await.unwrap().structured_content.unwrap();
        assert_eq!(on_sheet["validation"]["valid"],true);
        let checked_sheet=call("validate_layout",json!({"library_path":arranged["library_path"],"request":sheet_request,"layout_path":on_sheet["layout_path"]})).await.unwrap().structured_content.unwrap();
        assert_eq!(checked_sheet["valid"],true);
        let sheet_job:Value=serde_json::from_slice(&std::fs::read(workspace.join("sheet-run/job.json")).unwrap()).unwrap();
        assert_eq!(sheet_job["stocks"][0]["outline"][0]["holes"].as_array().unwrap().len(),1);
        std::fs::write(workspace.join("legacy.dxf"),legacy.chars().map(|c|c as u8).collect::<Vec<_>>()).unwrap();
        let decoded=call("import_parts",json!({"paths":["legacy.dxf"],"layers":["CUT_Ø"],"dxf_unit_mm":25.4})).await.unwrap().structured_content.unwrap();
        assert_eq!(decoded["part_count"],1);assert_eq!(decoded["parts"][0]["bounds_mm"][2],508.0);
        assert_eq!(decoded["imports"][0]["report"]["units"]["declared"],false);
        assert_eq!(decoded["imports"][0]["report"]["units"]["possible_inches"],true);
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
        let svg = std::fs::read_to_string(workspace.join("export/sheet-0.svg")).unwrap();
        let dxf = std::fs::read_to_string(workspace.join("export/sheet-0.dxf")).unwrap();
        assert!(svg.contains(r##"<g id="CUT" fill="none" stroke="#000000""##));
        assert!(svg.contains(r##"<g id="SHEET" fill="none" stroke="#f36926""##));
        assert!(dxf.contains("2\nSHEET\n70\n0\n62\n30\n420\n15952166\n"));
        assert!(dxf.contains("\n8\nSHEET\n62\n256\n"));
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
