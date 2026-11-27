Nestbolt DXF import: fixture run of 2026-11-27
==============================================

We make Nestbolt. This folder holds everything behind the dated "DXF import" line on
https://skulitom.github.io/Nestbolt/deepnest-alternative/ and https://skulitom.github.io/Nestbolt/compare/.
Only Nestbolt's command line was run. No other nesting tool was run on these files, and the hosted app was not tested.

What changed in Nestbolt
  On 24 November 2026 (UTC) two pull requests by PedroRangel7 were merged into main:
  https://github.com/skulitom/Nestbolt/pull/41  reads binary DXF and converts $INSUNITS length codes 1 to 21
                                                (22 to 24, the US survey inch, yard and mile, are still refused)
  https://github.com/skulitom/Nestbolt/pull/39  reads listed DXF layers that are off or frozen
  The v0.1.0 and v0.2.0-alpha.1 downloads were built before that.

The drawings (fixtures/, drawn by make_fixtures.py with ezdxf 1.4.3, a DXF library that shares no code with Nestbolt)
  Three plates, the same real size in every file: 80 x 50 mm with a 20 mm hole, 60 x 40 mm, and a 70 x 70 mm L bracket.
  plates-mm.dxf, plates-inch.dxf        text DXF marked millimetres and inches
  units/plates-insunits-01 ... 21.dxf   one file for each $INSUNITS length code from 1 to 21
  plates-r12-nounit.dxf                 R12 text DXF with no units, drawn in inches
  plates-mm-binary.dxf                  binary DXF, two-byte group codes
  plates-r12-binary.dxf                 binary R12 DXF, one-byte group codes
  plates-hidden-layers.dxf              the plates on a frozen layer (CUT) and a switched-off layer (PROFILE),
                                        with a visible 200 x 120 mm frame on a layer named NOTES
  27 drawings in all. The text files have LF line ends.

The checks (run_checks.py)
  U1-U6  units: the plates import at their drawn size in millimetres, inches and each code from 1 to 21; a file with
         no units stays at 1 mm per unit with a warning, and takes --dxf-unit-mm 25.4; units in the file win over
         that flag. Width and height must match to 0.000001 mm.
  B1-B2  binary DXF: both binary files give the same curves as their text twins, at the drawn size
  L1-L2  layers: named layers are read when frozen or off; with no --layers they stay out, with a warning
  Q1-Q2  quantities: 12 + 16 + 10 plates on 300 x 200 mm sheets, 5 mm margins, 2 mm spacing, 20 s, seed 1,
         --repeatable: all 38 placed on three sheets, and the three exported DXF files hold exactly those plates
  M1-M7  planted faults. Each one is a broken input that goes through the same check and must fail:
         M1 an inch drawing marked millimetres; M2 a truncated binary file; M3 the wrong layer chosen;
         M4 a sheet with one plate's outline deleted (its hole left behind); M5 a US-survey-foot drawing marked
         feet (2 parts in a million apart); M6 a sheet with one hole moved off its plate; M7 a sheet with one
         plate moved onto another. They show that the checks can fail, nothing more.
  Sizes come from Nestbolt's own import report. The exported sheets are read back with ezdxf: plates are counted by
  the area of each closed outline, every hole must sit at the middle of one 80 x 50 plate, every outline must lie
  inside the margins, and no two plates may be closer than 2 mm by our own segment-to-segment distances.
  `nestbolt validate` is run as well; it is Nestbolt's own validator, not an independent check.

Results (results/<build>/RESULTS.txt; Windows 11, 2026-11-27)
  main, commit 4ac32f7, built from source     12 of 12 checks pass. Smallest gap between plates on the three
                                               exported sheets: 2.015, 2.016 and 2.055 mm (2 mm asked).
  v0.2.0-alpha.1 download (16 Oct 2026)        7 of 12: it refuses both binary files ("binary DXF is not supported"),
                                               the named hidden layers and 16 of the 21 unit codes (it converts
                                               inches, feet, mm, cm and metres), and its exported sheets carry one
                                               zero-length LINE with each circle (results/v0.2.0-alpha.1/quantity-sheet-0.dxf)
  v0.1.0 download (14 Oct 2026)                6 of 12: the same five, plus Q1. Q1 fails there only because v0.1.0's
                                               `validate` has no --library form; its own report says 38 of 38 placed
                                               on three sheets
  All seven planted faults are caught on every build. On the two downloads M2 is caught only because they refuse
  every binary DXF.
  main still reports version 0.2.0-alpha.1 (`nestbolt --version`): the commit, not the version number, tells the
  builds apart.
  results/main-4ac32f7/ also holds the request, the layout, the three exported sheets and PLACEMENTS.tsv
  (sheet as Nestbolt named it, so sheet-0.dxf there is quantity-sheet-0.dxf here; then plate, position and size
  of each of the 38 plates, read from the exported DXF).

Limits
  - These are 27 small drawings we made, not other people's shop files.
  - Both binary files were written by ezdxf. Pull request 41 reports more binary files, one of them saved by
    AutoCAD; those were not run here.
  - $INSUNITS 22 to 24 (US survey inch, yard and mile) are refused with a message. There is no fixture for them.
  - The command line was run. The hosted browser app is built from main, but was not tested.
  - With no --layers, frozen and switched-off layers are left out (the import report says so). Name them to read them.
  - A drawing with no units is read at 1 mm per unit until you give the unit; Nestbolt warns, and does not detect
    inch drawings. Earlier builds do the same.
  - Polylines come back in the exported DXF as separate LINE entities that meet end to end, circles as CIRCLE.
  - A nest run with --repeatable gives the same layout for the same inputs, budget and seed on the same build.
    Another build may place the plates differently; the counts must still hold.

Run it again
  This folder is on Nestbolt's main branch from the commit that added it, not at 4ac32f7. So build at 4ac32f7,
  then come back to main:
    pip install ezdxf==1.4.3
    git clone https://github.com/skulitom/Nestbolt && cd Nestbolt
    git checkout 4ac32f7 && cargo build --release -p nestbolt-cli --locked && git checkout main
    cd web/public/compare/data/dxf-fixtures-2026-11-27
    python run_checks.py ../../../../../target/release/nestbolt fixtures out "main 4ac32f7"
  Or download this folder and run `python run_checks.py <path to nestbolt> fixtures out`.
  It prints PASS, FAIL, CAUGHT or MISSED for each line and exits 0 only when every check passes and every planted
  fault is caught. `python make_fixtures.py fixtures-new` draws the files again: a fresh set has new time stamps
  and ids in its headers and the same geometry.
