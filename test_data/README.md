# Local evidence archives / two distinct generations

Keep raw media, full telemetry, private configuration and field archives outside
Git. `test_data/*` and `runs/` are ignored, apart from this tracked placeholder.
Archive directory names and manifests identify provenance; a name alone is not a
physical test result.

Current V2 example (default output root `runs`, not `test_data`):

```text
runs/LB-V2-<UTC>-<suffix>/
  manifest.json
  config_snapshot.yml
  serial.raw
  run.sqlite3
  telemetry.csv          # optional explicit derived export
  front.mp4              # optional separate capture, if performed
  front.json             # capture sidecar for front.mp4, if performed
```

The manifest labels replay/serial mode and configuration/source limits. An orderly
close finalizes raw hash/status/counts; abrupt-power-loss recovery is unverified.
Do not rename replay as field evidence or score valid null frames as samples.
Check actual [camera naming behavior](../software/v2/raspberry_pi/capture_video.py)
and [current dictionary](../docs/data_dictionary.md) when choosing output paths.

Historical V1A layout, retained for identifying old archives:

```text
test_data/JOM-V1A-YYYYMMDD-RUN##/
  run_manifest.json
  config_snapshot/data_logger_config.yaml
  video/front_camera.mp4
  logs/arduino_telemetry.csv
  logs/pi_health.csv
  logs/events.csv
  logs/faults.csv
  exports/summary_for_scorecard.csv
```

Do not expect these old filenames/columns from the new logger. Retain original
raw bytes and any reviewed correction as separate artifacts with configuration
and hashes. Only bounded, privacy-reviewed examples/receipts belong in Git.
