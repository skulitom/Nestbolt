use nestbolt_core::import::{Options, import_dxf};

fn drawing(extra: &str) -> String {
    format!(
        "0\nSECTION\n2\nHEADER\n9\n$HANDSEED\n5\nA1\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n\
         0\nSECTION\n2\nTABLES\n0\nLAYER\n2\nCUT\n62\n7\n0\nENDSEC\n\
         0\nSECTION\n2\nBLOCKS\n0\nBLOCK\n2\npart\n10\n0\n20\n0\n\
         0\nCIRCLE\n5\nA1\n8\n0\n10\n0\n20\n0\n40\n5\n0\nENDBLK\n0\nENDSEC\n\
         0\nSECTION\n2\nENTITIES\n0\nINSERT\n5\nB1\n8\ncut\n2\npart\n10\n10\n20\n10\n\
         0\nINSERT\n5\nB2\n8\nCUT\n2\npart\n10\n30\n20\n10\n{extra}0\nENDSEC\n0\nEOF\n"
    )
}

#[test]
fn block_instances_and_header_seed_are_not_duplicate_handles() {
    let result = import_dxf(&drawing(""), &Options::default()).unwrap();
    assert_eq!(result.parts.len(), 2);
    assert!(
        !result
            .warnings
            .iter()
            .any(|w| w.contains("handle") || w.contains("undefined layer"))
    );
}

#[test]
fn duplicate_handles_and_undefined_annotation_layers_are_reported_without_dropping_parts() {
    let extra = "0\nTEXT\n5\n00a1\n8\nMissingNotes\n1\nannotation\n10\n0\n20\n0\n";
    let result = import_dxf(&drawing(extra), &Options::default()).unwrap();
    assert_eq!(result.parts.len(), 2);
    assert!(
        result
            .warnings
            .iter()
            .any(|w| w.contains("duplicate entity handle A1") && w.contains("2 DXF records"))
    );
    assert!(
        result
            .warnings
            .iter()
            .any(|w| w.contains("undefined layer \"MissingNotes\"") && w.contains("re-export"))
    );
    assert!(
        result
            .warnings
            .iter()
            .any(|w| w.contains("TEXT") && w.contains("ignored"))
    );
}
