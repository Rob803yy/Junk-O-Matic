# Junk-O-Matic / LitterBuggy

**Current work: reconstruct and review the physical V2 configuration.** Start with
the [V2 engineering index](docs/v2/README.md) and the
[repository alignment review](docs/repository_review/README.md).

The owner confirms **Elegoo Uno R3** and the CAD-R3 mounting relationships. Pi
model, current range hardware, power/return paths, installed pins, running sketch
and measured dimensions remain open. Source-code checks and illustrative models
do not establish deployment, physical fit, load capacity or operating reliability.
The owner selected **assisted V3: camera detection, operator alerts and reliable
logging, with manual RC controlling motion**. [V3 planning information](docs/v3/README.md)
records carry-forward/change decisions; its hardware choices, implementation and
numeric acceptance limits remain proposed. V2 remains the working runtime baseline.

## Current engineering sources

| Area | Maintained entry | Revision / boundary |
| --- | --- | --- |
| System, power-domain and data-flow architecture | [Three editable diagrams](hardware/v2/architecture/README.md) | ARCH-R2; component scope is separate from connection status |
| Digital connectivity | [Logical interface review](hardware/v2/architecture/v2_digital_connectivity.drawio) | R1; current physical pins/wiring remain untraced |
| Power and harnesses | [QElectroTech](hardware/v2/electrical/README.md), [WireViz/registers](hardware/v2/wiring/README.md) | R1; proposed/untraced, not a build wiring plan |
| Mechanical assembly and mounts | [Five native FreeCAD models / STEP / previews](hardware/v2/mechanical/README.md) | CAD-R3; owner/photo relationships, no measured dimensions |
| BOM and source corrections | [BOM JSON](docs/v2/bom.json), [editable workbooks/Word](docs/reconciliation/editable), [38 decisions](docs/reconciliation/README.md) | R1; source-listed quantities are not installed quantities |
| Uno acquisition / Pi logger | [Uno draft](software/v2/arduino/README.md), [Pi draft](software/v2/raspberry_pi/README.md), [protocol](docs/v2/serial_protocol.md) | New JSON protocol 2, not the recovered running program |
| Verification | [Evidence plan](docs/v2/verification-plan.md), [scoped receipts](docs/v2/validation.md), [original register](docs/v2_verification/README.md) | No new physical tests or field approval |

**PDF generation remains held for owner content review.** The 13 prior R0 PDFs
are [archived unchanged](archive/exports-r0/README.md). Review native files and current SVG/PNG/STEP exports.

## Choose the right software path

The root requirements file now selects only the V2 serial logger dependencies.
Dashboard and historical requirements live with their archived tools.


[Environment/setup matrix](docs/environment-setup.md) separates the current logger,
drafting tools and historical dashboard. The current firmware defaults all sensor
drivers/feedback OFF. A valid null frame is transport evidence, not a sensor sample.
Replay is explicitly labeled and is not a physical test.

[archive/v1a](archive/v1a/README.md) preserves the older V1A stub/logger.
The stub emits constants. The older logger is incompatible with the V2 contract
and can count blank measurement rows; do not pair them for V2 validation.
[Contract/output comparison](docs/data_dictionary.md) explains the differences.

## Repository map

| Folder | Purpose now |
| --- | --- |
| `docs/` | [Current, historical and review documentation index](docs/README.md) |
| `hardware/v2/` | Current editable engineering drafts; parent folders route here |
| `software/v2/` | New acquisition draft, SQL, fixtures and software tests |
| `validation/` | [Evidence/scorecard guidance](validation/README.md); sample CSVs are examples |
| `test_data/` | [Local archive conventions](test_data/README.md); raw data excluded from Git |
| `archive/` | [Historical V1A, dataset/model scaffold, reference pages and stale PDFs](archive/README.md); examples are separated from current sources |
| `scripts/` | [Commands, outputs and regeneration limits](scripts/README.md) |
| `reports/` | [Fixtures versus revision-specific check receipts](reports/README.md) |
| `.github/ISSUE_TEMPLATE/` | Configuration/evidence-aware hardware and validation issue templates |

Commit editable source, schemas, small labeled examples and bounded receipts.
Keep full raw telemetry, video, private configs and field archives outside Git.
The [former root V1A overview](archive/reference-pages/v1a-overview.md) remains available as
a historical reference; its stock hardware, wiring and percentage targets are
not adopted current facts.
