# Data Dictionary

## Run Manifest

| Field | Description |
| --- | --- |
| `run_id` | Run ID in `JOM-V1A-YYYYMMDD-RUN##` format |
| `stage` | Always `V1.0A - Instrumented RC Platform` |
| `started_at_utc` | UTC timestamp when the logger started |
| `operator` | Operator name or configured placeholder |
| `route_id` | Test route identifier |
| `buggy_id` | Physical vehicle identifier |
| `config_snapshot` | Relative path to captured config |
| `control_authority` | Statement that SCX6 RC system is sole drive control |
| `outputs` | Relative paths for logs, video, and exports |

## Arduino Telemetry

| Field | Unit | Required | Description |
| --- | --- | --- | --- |
| `timestamp_utc` | ISO-8601 | Yes | Pi receive timestamp |
| `aux_battery_voltage` | V | Yes | Kobalt auxiliary battery voltage |
| `rail_12v` | V | Yes | 12V buck output |
| `rail_5v` | V | Yes | 5V buck output |
| `imu_roll_deg` | deg | No | IMU roll |
| `imu_pitch_deg` | deg | No | IMU pitch |
| `imu_yaw_deg` | deg | No | IMU yaw |
| `enclosure_temp_c` | C | Yes | Enclosure temperature |
| `estop` | bool | No | Observational estop/fault input if installed |
| `fault_code` | integer | No | Arduino-side fault code |

## Pi Health

| Field | Unit | Description |
| --- | --- | --- |
| `timestamp_utc` | ISO-8601 | Sample timestamp |
| `cpu_percent` | percent | CPU utilization if available |
| `memory_percent` | percent | Memory utilization if available |
| `disk_percent` | percent | Disk utilization |
| `cpu_temp_c` | C | Pi CPU temperature if available |

## Events

| Field | Description |
| --- | --- |
| `timestamp_utc` | Event timestamp |
| `elapsed_s` | Seconds since logger start |
| `event_code` | Keyboard code |
| `event_name` | Marker name |
| `note` | Optional note text |

## Scorecard Summary

| Field | Description |
| --- | --- |
| `run_id` | Run identifier |
| `route_id` | Route identifier |
| `started_at_utc` | Run start timestamp |
| `ended_at_utc` | Run end timestamp |
| `duration_s` | Total run duration |
| `video_enabled` | Whether video was requested |
| `video_file` | Relative video path |
| `telemetry_rows` | Count of parsed telemetry rows |
| `pi_health_rows` | Count of Pi health rows |
| `event_rows` | Count of event rows |
| `fault_rows` | Count of fault rows |
| `control_authority` | V1.0A drive-control statement |
