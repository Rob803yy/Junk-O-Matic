> REPO-R1 review 2026-11-22: Historical procedure only. Do not use it as the current V2 run checklist: source/output names differ, the legacy stub emits constants, and legacy row counts/video request flags/CPU health do not prove acquisition quality or no resets.
> Use the [current V2 evidence plan](v2/verification-plan.md) and [current engineering index](v2/README.md).

# Test Procedure V1.0A

## Objective

Verify that the buggy can be manually RC-driven while the auxiliary electronics reliably collect video, telemetry, health logs, metadata, and event markers.

## Required Equipment

- Junk-O-Matic V1.0A buggy
- SCX6 transmitter
- Charged SCX6 RC battery
- Charged Kobalt 24V auxiliary battery
- Raspberry Pi logger image or prepared SD card
- Arduino Nano telemetry firmware
- Camera
- External SSD or approved local evidence storage
- Test route map or route description

## Pre-Run

1. Inspect wiring, mounts, camera view, and enclosure.
2. Confirm RC drive system works with auxiliary system off.
3. Power auxiliary system and confirm Pi boot.
4. Start the Pi data logger.
5. Confirm `run_manifest.json` is created.
6. Confirm Arduino telemetry rows are arriving if hardware is connected.
7. Confirm video recording starts if enabled.

## Run

1. Press `s` at route start.
2. Manually drive the route with the SCX6 transmitter.
3. Press event markers as observations occur.
4. Press `e` at route end.
5. Press `q` to stop the run cleanly.

## Post-Run

1. Confirm the run folder contains manifest, logs, config snapshot, and export CSV.
2. Review video usability.
3. Check Pi health log for resets, high temperature, or disk issues.
4. Check Arduino telemetry row count against expected sample rate.
5. Copy raw evidence to local archive, OneDrive, or external SSD.
6. Do not commit raw video or full telemetry archives.

## Pass Criteria

- Run manifest exists.
- Event markers are present and timestamped.
- Camera video is reviewable when camera recording was enabled.
- Telemetry and health CSVs contain expected headers and rows.
- Summary scorecard CSV is generated.
- No RC control surprise is observed.
