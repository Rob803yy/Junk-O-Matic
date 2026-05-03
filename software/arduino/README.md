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
