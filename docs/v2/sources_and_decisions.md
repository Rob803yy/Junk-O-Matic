# Source review and drafting decisions

## Project evidence

The verification baseline audits main commit
`b163861c78d02060da30a026469f19e3c1409d11`. Repository source is evidence of what
was documented/implemented, not what is physically installed. The owner selected
Junk-O-Matic and explicitly confirmed the Elegoo Uno R3 on 2026-11-21.

For this drafting pass the following media were directly re-opened or sampled:

- Adapter photos 1000063718-1000063721 from “V2 Field Testing Setup”: blue body,
  black KBT-marked guide, two contacts, red/black leads and recessed features.
  No ruler, readable electrical rating or verified mounting hole path was visible.
- Suspension photos 1000061963-1000061971 from “LitterBuggy Status Review”:
  raised black tub, metal support/frame, four-wheel chassis and coilovers.
  Their different load poses support preserving the roll problem in review,
  not assigning a spring fault or calibrated lean angle.
- Videos 1000062231, 1000062233 and 1000062235 from “Integration milestone update”:
  sampled frames near 15%, 50% and 80% show the raised cart, outdoor setting and
  lighting; 2231 includes a bag in the cart. Sparse sampling does not certify a
  full route, curb crossing, load mass, driver settings or stability margin.
- The Windows Device Manager screenshot from “Plan Raspberry Pi Build” shows
  an unknown USB device/descriptor failure. The owner previously reported it
  disappeared when the Uno was unplugged. Current recognition remains unknown.

The retrieved Pi chat contains assistant descriptions of MPU-6050, HC-SR04,
LED and buzzer but no retrievable close-up of the sensor circuit in that returned
attachment set. Those identities remain historical claims, not re-inspected parts.
OLED installation remains unknown. Original full media stays outside the public
repository; temporary preview paths and unrelated personal imagery are omitted.

## Decisions and alternatives

| Problem | Draft decision | Reason / boundary |
| --- | --- | --- |
| Nano references versus confirmed Uno | Use Uno R3 throughout new V2 files | Direct current owner confirmation overrides historical references |
| Missing as-built wiring | Show proposed functional paths and TBD power entries | Readable drafts can be reviewed without inventing physical pinouts |
| Unknown dimensions | Real parametric envelope models, measured values null | Makes assembly relationships editable while preventing false fit claims |
| High tub and roll observations | Preserve raised mounting relationship and coilover envelopes | No suspension redesign or assumed fix before measurements |
| Original sketch lost | New source clearly identified; preserve old firmware before upload | New code cannot honestly be described as recovered source |
| Old stub emits synthetic data | Null unavailable measurements plus explicit flags | Example constants must not pass as real sensor acquisition |
| Unknown IMU axes/calibration | Store raw register counts | No invented yaw or calibrated tilt; die temperature distinct from enclosure |
| USB failure and reconnect | Serial session boundaries, raw capture and reconnect support | Avoid merging partial lines across resets/disconnections |
| Logger reliability | Strict parsing, bounded framing, single database writer and graceful signal handling | Explicit failures and testable behaviour before field use |
| Optional camera | Separate capture process with failure metadata | Unknown camera model must not block serial acquisition or imply sync |

## Engineering format references

- [QElectroTech project XML](https://github.com/qelectrotech/qelectrotech-source-mirror/wiki/project_XML)
  and [official example](https://github.com/qelectrotech/qelectrotech-source-mirror/blob/master/examples/industrial.qet).
  The generated project uses embedded module symbols and terminal-linked
  conductors, then was opened/re-saved/exported by QElectroTech 0.200.1 Qt6.
- [WireViz syntax](https://github.com/wireviz/WireViz/blob/master/docs/syntax.md)
  and [tutorial](https://github.com/wireviz/WireViz/blob/master/tutorial/readme.md).
  Exports generated with WireViz 0.4.1 and Graphviz 13.1.2.
- [MPU register map](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map.pdf)
  and [Arduino AVR Wire](https://github.com/arduino/ArduinoCore-avr/blob/master/libraries/Wire/src/Wire.cpp).
  Register semantics informed optional acquisition code; breakout supply tolerance
  and sensor identity remain separate physical checks.

FreeCAD 1.1.4 native Python/OCC was available locally. No stock SCX6 manufacturer
dimension was silently substituted for a current-build measurement.
