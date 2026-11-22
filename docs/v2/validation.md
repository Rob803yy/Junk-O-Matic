# Draft R1 validation and technical review boundary

## Completed software/artifact checks

- Four diagrams.net XML files parse: three architecture sources plus digital connectivity. Current SVG/PNG previews were inspected.
- QElectroTech 0.200.1 Qt6 opened and re-saved the embedded-symbol project, then
  exported its three sheets to PNG. Native PNG sheets were inspected; defective SVG scaling output was excluded. This checks
  file compatibility and layout, not electrical correctness.
- WireViz 0.4.1 with Graphviz 13.1.2 generated both harnesses, diagrams, HTML,
  connector inventories and BOM tables. Rendered diagrams were inspected.
- FreeCAD 1.1.4 generated five native files and five STEP exports; all reopened.
  139 exported component records across the current assembly/submodels passed validity checks. Additional native checks
  tested all saved shape objects, spreadsheet wheelbase propagation and tyre
  centre spacing. A centre/end placement inconsistency was corrected before
  the final model export. These are illustrative geometry checks, not fit tests.
- Uno R3 default build and compile-only enabled IMU/range/feedback build succeed
  on Arduino AVR Boards 1.8.8. Enabled test pins 6/7/8/9 and threshold 200 mm are
  compiler-test inputs only, not actual V2 assignments. A build enabling range
  without pins must fail the compile guard. R1 also rejects UART profile selection with the HC-SR04 driver. R1 also rejects UART profile selection with the HC-SR04 driver.
- 32 Python tests exercise strict parsing, null/fault consistency, invalid types,
  duplicate keys, raw byte offsets, chunked/overlong/incomplete frames, sequence
  wrap/gaps/reset indicators, SQLite/export behaviour, session boundaries,
  reconnection, port shutdown, low disk handling, bad config and unavailable camera.
- An end-to-end CLI replay produces two valid frames, zero sensor measurements,
  byte-identical raw capture, an integral SQLite database and replay manifest.

Machine-readable results and build/test receipts live in
[reports/v2](../../reports/v2). Re-run
`python scripts/v2/run_checks.py --arduino-cli PATH_TO_ARDUINO_CLI` with the
drafting/test dependencies installed. `check_freecad.py` uses FreeCAD's Python.
No generated HEX was uploaded or presented as a recovered firmware backup.

## Review still required

Electrical: actual polarity and nets, source separation/grounds, protection,
converter limits, Uno/Pi power entry, USB interactions, sensor logic voltage,
wire ratings and connector pin order.

Mechanical: every as-built dimension, datum, mounting hole and member section;
dock recess function and removal/latch access; enclosure and sensor placement;
suspension/steering clearance; mass distribution, lean and payload limits.

Firmware: original sketch preservation, exact installed pins/modules, driver
electrical compatibility, axes/calibration, timing, actual alarm behaviour and
hardware fault recovery. Default null output verifies no physical sensor function.

Pi: deployed OS/model, USB recognition and stable port identity, power stability,
field disk capacity, real serial timing/reconnection, real camera/video, clock
alignment, abrupt-power-loss recovery and systemd behaviour.

## Review completion record

For each subsystem record reviewer/date, hardware configuration, source revision,
resolved verification IDs, supporting evidence, remaining issues and disposition.
No subsystem is released for fabrication/deployment by this draft validation.
The historical V1A percentage and five-session goals are not marked passed.

## R1 document reconciliation checks

Fourteen input hashes, 38 discrepancy resolutions, three editable Excel workbooks
and one canonical Word correction record accompany the engineering sources.
Native Excel chart/drawing/validation and extension ZIP parts are preserved while
Artifact Tool-authored cell changes correct readiness formulas and configuration
scope. Before/after dashboard previews were inspected. Formula branches check
missing scores, missing evidence, recorded critical versus noncritical failure,
invalid score range and no-current-test denominators. Canonical BOM preserves
107 original rows and separates source quantities from installed quantities.

All 13 tracked R0 PDFs are byte-identical. PDF generation and Word pagination/PDF
proofing are intentionally held until owner content review. Current source/native
checks and previews do not substitute for those later PDF layout checks.

## CAD-R2 validation

Five FreeCAD and STEP files reopened. All constrained profile sketches are fully
constrained; wheelbase, cart length and vertically oriented case height edits
propagate to native geometry. Tub floor/open interior and wheel centres were checked.
Named draft intersections between case/tub, case/rim and case/blue pack were checked;
this is not a full assembly interference or real fit test. Native component grouping,
colors, construction/reference visibility and lid translucency are saved. Fourteen
photo observations and two owner decisions are recorded. No measured dimensions,
bucket, installed ultrasonic claim or new PDF was introduced. Software was unchanged
in this CAD-only feedback pass; its earlier 32-test receipt remains scoped to R1.

## CAD-R3 frame and pose checks

Native/STEP readbacks, hollow inner-member section, live frame-width edit,
rear-axis tub tipping with stationary outer frame, restored normal pose and
red axle-center placement are checked. The former hanging-strip and bumper-top
red feature are excluded. Seven photo references/24 bounded observations and
seven owner decisions support this revision. The 55-degree pose is a layout view;
numeric hinge placement, latch, moving bracket membership, maximum travel and
real-world clearance are unverified. Software is unchanged in this CAD pass.
All 13 prior PDFs remain held and unchanged.
