# Historical V1A Arduino stub / not current V2 acquisition

`telemetry_logger_stub/telemetry_logger_stub.ino` is preserved unchanged. It emits
fixed example battery/rail voltages, roll/pitch/yaw, temperature and fault fields
at a 1000ms target interval. **Those constants are not physical measurements,
calibration or E-stop evidence.** Do not use its rows to pass validation gates.

For current work use [Uno R3 acquisition source](../v2/arduino/README.md) and
[protocol 2](../../docs/v2/serial_protocol.md). The current sketch starts with
drivers/feedback disabled and null measurements. Its physical pin map, supplies
and deployment remain open; it is separate from the unrecovered running sketch.

The legacy wire contract is incompatible with V2. See the
[contract/output comparison](../../docs/data_dictionary.md). The
[former readme and examples](../../docs/history/v1a-arduino-readme.md) are retained
for history, not an upload instruction. Preserve the existing device program
before any replacement; no upload or hardware verification occurred in this review.
