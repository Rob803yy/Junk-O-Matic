# Raspberry Pi Data Logger

This logger is data-only for **V1.0A - Instrumented RC Platform**.

It records run evidence and must never send steering, throttle, ESC, arming, deadman, or motion commands.

## Setup

```bash
cd junk-o-matic
python3 -m venv .venv
source .venv/bin/activate
pip install -r software/raspberry_pi/requirements.txt

cp software/raspberry_pi/config/data_logger_config.template.yaml \
  software/raspberry_pi/config/data_logger_config.local.yaml
```

Edit the local YAML for the actual serial port, camera settings, operator, buggy ID, and route ID.

If USB camera MP4 recording is enabled through this Python logger, uncomment `opencv-python` in `software/raspberry_pi/requirements.txt` and reinstall requirements.

## Run

```bash
python software/raspberry_pi/src/jom_data_logger.py \
  --config software/raspberry_pi/config/data_logger_config.local.yaml
```

## Keyboard Markers

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

## Output

Each run writes:

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

Raw evidence folders should stay local, in OneDrive, or on an external SSD. Do not commit full run evidence.
