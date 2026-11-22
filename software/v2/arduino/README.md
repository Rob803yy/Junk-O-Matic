# Uno R3 acquisition draft

Board: **Elegoo Uno R3**, owner-confirmed. Build target `arduino:avr:uno`.
This is new source implementing a proposed protocol, not the recovered original
sketch. Preserve existing firmware/source before uploading. No upload was performed.

Defaults: all sensors/feedback disabled, pins -1, 100 ms emission, 115200 baud.
The default sketch emits null measurements and flags=5; no sensor output pins
are configured. It is buildable for review without claiming known wiring.

R1: the historical HC-SR04 is reported lost in S06. No replacement is selected.
Enabling that optional driver also requires `-DRANGE_PROFILE=1`; this identifies
the HC-SR04 timing profile and does not confirm hardware availability. A02YYUW
/ SEN0311 uses a different UART protocol and is not implemented here. Compile
guards reject using an unselected or UART profile with the trigger/echo driver.
Current firmware ID is `v2-r1`; the shared JSON protocol remains version 2.

The optional drivers are implemented, not TODO sensor constants:

- MPU-6050: identity check, wake/configure, bounded I2C transactions, raw 14-byte
  register burst, retry after failure. Range +/-2g and +/-250deg/s; DLPF config 3,
  internal sample divider 9. Axis mounting/bias calibration remains pending.
- HC-SR04: bounded echo pulse timing, null on timeout, proposed sound-speed
  approximation 0.343 mm/us. Conversion is not a calibrated accuracy claim.
- LED/passive buzzer: optional active-high range alarm, disabled until verified
  pins, driver circuit, polarity and threshold are supplied. No original alarm
  thresholds or original behaviour are claimed.

Before enabling, reconcile `config.h` with the traced harness, confirm module
identity/supply/pullups and set digital pins. Compile guards reject missing or
overlapping assignments. A4/A5 are the Uno hardware I2C pins, not verified wires.
OLED, camera, voltage, enclosure temperature, yaw and estop are not fabricated
features. MPU internal temperature is retained as raw counts, not enclosure temp.

Build with Arduino AVR Boards 1.8.8 and its bundled Wire library (no third-party
Arduino libraries required):

```text
arduino-cli compile --fqbn arduino:avr:uno software/v2/arduino/litterbuggy_v2
```

Compile-only test assignments used in validation are not a physical wiring plan.
Enabling drivers may alter sensor configuration; preserve current firmware and
complete the technical review before deployment.

References: [MPU register map](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map.pdf),
[AVR Wire implementation](https://github.com/arduino/ArduinoCore-avr/blob/master/libraries/Wire/src/Wire.cpp).
