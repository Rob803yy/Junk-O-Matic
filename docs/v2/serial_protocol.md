# Proposed serial protocol v2 / R1

This is a new draft contract between the supplied Uno and Pi programs. It is
not a transcription of the unrecovered original firmware's serial format.
Physical hardware revision V2 and protocol version 2 are separately versioned.

R1 reconciles the attachments while retaining this single JSON contract. The
CSV `D`/`H` records and 20Hz/1Hz schedule in S06 are alternative proposals,
not the existing serial format or an implemented compatibility mode. The new
draft emits at a proposed 10Hz. Neither the legacy 50–100Hz target nor the S06
20Hz acquisition target has been demonstrated. HC-SR04 is an optional historical
profile; S06 reports it lost. The proposed A02YYUW UART sensor is unselected and
has no driver in this revision. Its eventual integration requires a protocol
review of echo fields and sensor identity, not merely different pin numbers.

Transport: USB serial, proposed 115200 baud, 8N1. One UTF-8 JSON object per line;
firmware emits CRLF. Maximum frame is 512 bytes including line terminators. The
parser requires exactly the listed keys, rejects duplicate keys, wrong types,
nonfinite values, invalid flags and inconsistent nulls, and preserves rejected
bytes. Startup text from an old sketch will be retained and rejected, not silently
reinterpreted. No command channel or motor/servo output exists.

| Field | Type / unit | Meaning |
| --- | --- | --- |
| v | integer = 2 | Protocol version |
| type | string = telemetry | Message kind |
| fw | printable ASCII, 1..32 chars | Firmware's self-reported build ID; not proof of source/binary correspondence |
| seq | uint32 | Incremented per emitted sample; wraps modulo 2^32 |
| ms | uint32, milliseconds | Uno millis at start of acquisition; wraps modulo 2^32 |
| imu_raw | null or 7 signed int16 counts | Register order: ax, ay, az, internal_temp, gx, gy, gz |
| echo_us | null or integer 1..25000 us | Raw ultrasonic echo pulse duration |
| distance_mm | null or integer 0..4288 mm | Rounded echo_us * 0.343 / 2; approximate room-temperature conversion |
| flags | integer bit mask, 0..15 | Sensor availability/failure flags below |

| Bit/value | Meaning | Required measurement state |
| --- | --- | --- |
| 0 / 1 | IMU disabled in firmware configuration | imu_raw = null |
| 1 / 2 | IMU initialization/read failure | imu_raw = null |
| 2 / 4 | Ultrasonic driver disabled | echo_us and distance_mm = null |
| 3 / 8 | Ultrasonic echo timeout | echo_us and distance_mm = null |

Disabled and failed bits for the same sensor are mutually exclusive. With neither
IMU flag set, seven counts are required. With neither range flag set, both range
values are required. Default firmware flags=5 means **zero physical measurements**
even though the frame is syntactically valid. Sensor sample counts must be reported
separately from valid-frame counts.

Default disabled example (synthetic fixture):

```json
{"v":2,"type":"telemetry","fw":"v2-r1","seq":0,"ms":100,"imu_raw":null,"echo_us":null,"distance_mm":null,"flags":5}
```

Default emission interval is 100 ms, checked with wrap-safe unsigned subtraction.
It is a requested interval, not a guarantee of exact timing. Acquisition and serial
emission take time; ultrasonic pulseIn can block up to 25 ms. Long I2C failures
may extend a sample interval. Missed schedule slots are not replayed. No sample
duration or hardware synchronization guarantee is encoded in this revision.

Enabled MPU configuration is +/-2g (nominal 16384 LSB/g), +/-250deg/s (nominal
131 LSB/(deg/s)), DLPF config 3 and sample divider 9. Raw temperature is MPU die
temperature data, not enclosure temperature. No angle, absolute yaw, tilt alarm,
battery voltage or enclosure temperature is derived without calibration/hardware.
Mount axes, gyro bias and acceleration under motion require technical review.

The Pi adds receive UTC and host monotonic timestamps in SQLite. They are not
the device acquisition timestamp. Serial open may reset the Uno through DTR.
Each reconnect starts a new session and clears sequence tracking. Within a session,
the logger reports gaps, duplicates, or reset_or_out_of_order; it does not diagnose
an electrical reset from sequence numbers alone. Normal uint32 wrap is accepted.

Every raw byte is retained in serial.raw, including overlong/incomplete frames.
frames.raw_offset/raw_length locates the original bytes. Framing is bounded in
memory; invalid lines do not become telemetry. Raw file and database are flushed
during capture and finalized at shutdown; abrupt power-loss recovery is untested.

Changing keys, types, range configuration or sound-speed semantics requires a
protocol review/version change. Enabling drivers with unchanged units does not
establish their physical wiring; record firmware configuration separately.
