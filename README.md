# Junk-O-Matic / LitterBuggy

## Current engineering work: reconciled V2 review R1

[Start the engineering review](docs/v2/README.md): three editable architecture
diagrams, digital connectivity, three-sheet QElectroTech power schematic, two
WireViz harnesses, five FreeCAD/STEP models, Uno firmware and Pi logger/SQL/tests.

[38 source discrepancies](docs/reconciliation/README.md) reconcile the supplied
V1/V2/V3 references and concept posters. Corrected editable BOM, scorecard,
review-data workbook and unified Word correction record are in
[editable review documents](docs/reconciliation/editable).

The owner confirms **Elegoo Uno R3**. Pi model, current range sensor, actual wiring
and all measured dimensions remain unresolved. Future concept claims are not
installed capabilities. No hardware upload, Pi deployment or field validation
was performed. Version naming is proposed pending owner confirmation.

Latest CAD feedback: [CAD-R2 photo-informed models and previews](hardware/v2/mechanical/README.md), with owner-confirmed front orientation and no bucket.

**PDF generation is held for owner review.** Prior R0 PDFs remain historical and
stale for R1. Current SVG/PNG previews accompany the editable sources.

## Historical V1.0A scope (preserved below)

The following describes the prior repository stage and contains historical Nano
and stock-system references requiring reconciliation. It is not a current as-built
description of V2.

### Junk-O-Matic / Ideal Litterbuggy V1.0A

Instrumented RC-based litter buggy platform. V1.0A focuses on Raspberry Pi data collection, telemetry logging, camera recording, and validation evidence generation while the SCX6 RC system remains the only drive-control authority.

## Stage

**V1.0A - Instrumented RC Platform**

This repository exists to make the V1.0A test campaign reproducible. It stores the system definition, validation procedures, data logger code, scorecard import format, and small example files.

The Raspberry Pi does **not** control steering, throttle, ESC, arming, deadman, or vehicle motion in V1.0A. The stock Axial SCX6 transmitter, receiver, ESC, steering servo, traction motor, and RC battery remain the only drive-control system.

## Electrical Domains

V1.0A keeps two separated electrical domains:

- RC drive system: stock SCX6 RC battery, receiver, ESC, steering servo, traction motor, and transmitter control authority.
- Auxiliary electronics system: Kobalt 24V auxiliary battery, main fuse, main switch, 24V-to-5V buck, 24V-to-12V buck, Raspberry Pi 4B, Arduino Nano, camera, and optional telemetry sensors.

There is no direct power tie between the RC battery and the auxiliary electronics battery. Any future interface between domains must be signal-only or observational and documented before testing.

## What V1.0A Proves

The goal is to prove the buggy can be manually RC-driven through repeatable test routes while the Raspberry Pi reliably records video, telemetry, run metadata, Pi health, and operator event markers without affecting vehicle control.

Validation gates include:

- Pi boot and logging: 10/10 clean starts
- Camera recording: at least 95% usable video
- Arduino telemetry: at least 95% expected rows
- No Pi resets across 5 field sessions
- Stable 5V rail and 12V rail under expected loads
- Run manifest exists for 100% of runs
- Summary CSV generated for 100% of runs
- 5 x 45-minute field sessions completed
- Operator event markers used successfully
- Every test links to an evidence folder

## Repository Layout

```text
docs/                         Project scope, wiring notes, procedures, dictionaries
software/raspberry_pi/         Data-only Pi logger and config template
software/arduino/              Arduino telemetry stub
hardware/                      Wiring diagram, BOM, and enclosure placeholders
validation/                    Scorecard guidance and sample CSVs
test_data/                     Local-only run evidence placeholder
app/                           Existing local dashboard workspace
configs/                       Existing taxonomy/dataset configuration
data/                          Existing processed data workspace
reports/                       Existing evaluation and dashboard artifacts
scripts/                       Existing bootstrap and conversion scripts
src/                           Existing Python package code
```

## Raspberry Pi Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r software/raspberry_pi/requirements.txt

cp software/raspberry_pi/config/data_logger_config.template.yaml \
  software/raspberry_pi/config/data_logger_config.local.yaml

python software/raspberry_pi/src/jom_data_logger.py \
  --config software/raspberry_pi/config/data_logger_config.local.yaml
```

The default logger writes each run under `test_data/JOM-V1A-YYYYMMDD-RUN##/`.

## Operator Markers

During a run, the Pi logger accepts these keyboard markers:

```text
s START_ROUTE
e END_ROUTE
l LITTER_OBSERVED
p PICKUP_ATTEMPT
f FAULT_OBSERVED
b BATTERY_CONCERN
c CONTROL_SURPRISE
m MECHANICAL_ISSUE
n NOTE_MARKER
q STOP_RUN
```

## Data Policy

Commit code, docs, procedures, wiring notes, config templates, schemas, and small sample CSVs.

Do not commit raw full test data, videos, large telemetry archives, rosbag files, or private local configs. Store raw evidence locally, in OneDrive, or on an external SSD. GitHub should store the reproducible test logic and system definition, not the full field evidence archive.

## Next Stage Boundary

V1.0B/V1.5 may add auxiliary actuators or assisted perception only after the V1.0A data-collection gates pass. This repo should not imply autonomy before that evidence exists.
