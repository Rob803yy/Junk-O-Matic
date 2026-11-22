# Data contracts and artifacts / current versus historical

The new V2 source uses [serial protocol 2](v2/serial_protocol.md) and
[schema.sql](../software/v2/raspberry_pi/schema.sql). The actual installed sketch,
original output and deployed logger remain unknown. The former dictionary is
[preserved separately](history/v1a-data-dictionary.md).

| Interface | Historical V1A example | New V2 draft |
| --- | --- | --- |
| Source | Constant-emitting telemetry stub; not measurements | Uno R3 sketch with optional verified drivers; all OFF by default |
| Wire fields | Unversioned battery/rails/attitude/temp/estop/fault keys | Exact `v,type,fw,seq,ms,imu_raw,echo_us,distance_mm,flags` |
| Schedule | Stub target 1000ms (1Hz) | Target 100ms (10Hz), physical timing not benchmarked |
| Transport | Example USB/115200; actual port unverified | Proposed USB/115200/8N1; configured physical port must be established |
| Parsing | Arbitrary dictionary keys can yield blank measurement columns counted as rows | Strict keys/types/ranges/null flags and bounded framing |
| Config | Legacy `arduino`, `camera`, `run` YAML sections | `schema_version=1`, CFG-V2-R1, serial/health/disk settings |
| Run ID | `JOM-V1A-YYYYMMDD-RUN##` | `LB-V2-<UTC timestamp>-<unique suffix>` |
| Manifest | `run_manifest.json` | `manifest.json`; replay/serial mode, hashes and sample counts |
| Raw serial | Not retained by the legacy logger | `serial.raw` appended/flushed before parsing |
| Storage | Legacy CSV logs + scorecard summary | `run.sqlite3`; derived `telemetry.csv` only when explicitly exported |
| Config snapshot | `config_snapshot/data_logger_config.yaml` | `config_snapshot.yml` |
| Operator keyboard markers | Implemented in historical logger | Not implemented in current V2 logger |
| Video | Optional integrated legacy capture; requested != usable | Optional separate `capture_video.py` and sidecar metadata |
| Scorecard summary | Historical `exports/summary_for_scorecard.csv` | No automatic equivalent implemented; manual evidence review required |

**Do not pair the V2 sketch with the legacy logger.** An offline fake-port check
fed a valid protocol-2 frame to that logger: it counted one row with all nine
measurement columns blank. [Reproduction receipt](../reports/repository_review/legacy-parser-reproduction.json).
Historical payloads are also rejected by the strict V2 parser; there is no silent
CSV/unversioned adapter.

## Current serial semantics

`v=2`, `type=telemetry`; `fw` is a self-report, not binary/source correspondence.
`seq` and `ms` are unsigned 32-bit device values; `ms` represents acquisition-start
uptime. They do not supply UTC clock synchronization. `imu_raw` is null or seven
raw signed registers: accel XYZ, internal die-temperature count and gyro XYZ.
It is not calibrated attitude, absolute yaw or enclosure ambient temperature.
Range fields are null when disabled/timed out; the optional implemented profile
is HC-SR04. A02YYUW UART remains unselected and unimplemented here.

Flags: 1 IMU disabled, 2 IMU failure, 4 range disabled, 8 range timeout. Disabled
and failed flags are mutually exclusive per sensor. The default `flags=5` frame
is valid transport with null measurements and **zero physical sensor samples**.
See the protocol for exact bounds, framing and conversion tolerances.

## Current SQLite and manifest

| Artifact/table | Meaning and limit |
| --- | --- |
| `serial.raw` | Original input bytes, including rejected input; flush alone is not a power-loss guarantee |
| `sessions` | Serial/replay session boundaries; reconnect resets framing/tracking |
| `frames` | Every framed outcome: validity/error, raw offset/length, session, host receive UTC/monotonic time |
| `telemetry` | Validated payloads only; null measurements remain null |
| `events` | Acquisition/session/sequence diagnostics, not keyboard route annotations or proven reset causes |
| `health` | Disk free bytes and Pi CPU temperature if available; no rail voltage, undervoltage or ambient sensing |
| `metadata` / `manifest.json` | Config/mode/environment, config/logger hashes, status; counts and raw hash finalized on orderly close |
| `config_snapshot.yml` | Config bytes used for this run; keep private operator/device data outside Git |
| Derived CSV | Query of valid telemetry; does not replace raw/error/archive evidence |

Valid-frame count, IMU sample count and range sample count are different measures.
Receive timestamps, sequence events or CPU health alone cannot establish complete
coverage, video synchronization, electrical stability or reset-free sessions.
The current schema does not contain battery/rail readings, calibrated roll/pitch/yaw,
E-stop state, GPS, autonomous commands or a V2 scorecard result.
