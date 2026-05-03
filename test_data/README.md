# Test Data

This folder is a placeholder for local V1.0A run evidence.

Do not commit raw videos, full telemetry logs, large archives, rosbags, or private configs.

Each local run should look like:

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

Store long-term raw evidence locally, in OneDrive, or on an external SSD.
