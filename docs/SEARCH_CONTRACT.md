# Repeatable search contract (partially implemented)

The v1 MCP promise is that the same original job, engine version, seed and budget
produce the same successful layout. A seed combined with a wall-clock cutoff
does not satisfy that promise: scheduling changes how many search steps finish.

The shared core will therefore support a repeatable work-budget mode. A versioned,
documented mapping from `time_budget_s` and job complexity determines a fixed
number of search operations. Stable ordering and explicit random streams make
those operations repeatable. Worker scheduling must not select a different
winner; candidate ties and portfolio merge order have deterministic rules.
The exact work-unit definition/calibration will be measured and frozen with M2,
before quality tuning against the acceptance matrix.

The time parameter also supplies a hard execution limit, capped at 300 seconds.
If the deterministic quota cannot finish before that limit, return an explicit
timeout/incomplete outcome, with no supposedly repeatable final layout. Progress
previews may be retained separately and are labelled provisional. Cancellation
has the same explicit distinction. A successful exported result must complete its
quota and pass independent validation. Artifact paths/timestamps are provenance;
repeatability applies to canonical placements, scores and exported geometry.

Fair benchmark runs may explicitly request full wall-clock search so every tool
gets the same 60/300-second opportunity. That mode records the seed, completed
work and elapsed time but makes no identical-layout promise. Native CLI, browser
and MCP must expose the same supported search semantics; the MCP default is the
repeatable mode. M0 runs the published historical solver's wall-clock procedure
and is not evidence for this future contract.

Acceptance still requires real repeated-job tests, native/browser comparison,
progress/cancellation and actual timeout behavior. These notes resolve the intended
semantics. The constructor has an explicit seed and fixed sample count. Repacking
has fixed passes, specified integer shuffles over part types or individual copies,
initial translation/contact comparisons,
independent incumbent acceptance and per-pass progress. Native repeated-output
tests cover both. These experimental quotas do not yet implement time-budget
calibration, hard cancellation or the complete native/browser/MCP contract.
