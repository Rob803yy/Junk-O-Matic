# Historical reference / preserved from software/arduino/README.md

Source: `adb9280f30513fd852968d12e9bc6479bd2e188d`. This is the former page snapshot, including its V1.0A material, not verified current V2 wiring, installed hardware, deployed software or passed tests. Use [the current review index](../../docs/v2/README.md).


Relative Markdown links below are rebased to their original file location at the baseline commit. Statements and code examples retain their historical scope.

---

# Arduino Telemetry

The Arduino publishes JSON-lines telemetry over USB serial for the Raspberry Pi logger.

In V1.0A, Arduino telemetry is observational. It does not command steering, throttle, ESC, arming, deadman, or vehicle motion.

## Expected JSON-Line Format

```json
{
  "aux_battery_voltage": 23.7,
  "rail_12v": 12.1,
  "rail_5v": 5.05,
  "imu_roll_deg": 1.2,
  "imu_pitch_deg": -0.7,
  "imu_yaw_deg": 85.4,
  "enclosure_temp_c": 34.2,
  "estop": false,
  "fault_code": 0
}
```

## Minimum Format

```json
{
  "aux_battery_voltage": 23.7,
  "rail_12v": 12.1,
  "rail_5v": 5.05,
  "enclosure_temp_c": 34.2
}
```

Replace the stub constants with calibrated sensor reads before using telemetry for validation gates.
