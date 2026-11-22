# Historical reference / preserved from docs/wiring_notes.md

Source: `adb9280f30513fd852968d12e9bc6479bd2e188d`. This is the former page snapshot, including its V1.0A material, not verified current V2 wiring, installed hardware, deployed software or passed tests. Use [the current review index](../../docs/v2/README.md).


Relative Markdown links below are rebased to their original file location at the baseline commit. Statements and code examples retain their historical scope.

---

# Wiring Notes

## Architecture

V1.0A uses two separated electrical domains.

## RC Drive System

- Stock SCX6 RC battery
- Stock SCX6 ESC
- Stock SCX6 receiver
- Stock SCX6 steering servo
- Stock SCX6 traction motor
- Stock RC transmitter

The RC drive system remains stock and independent. The Raspberry Pi and Arduino do not connect to ESC, steering, throttle, arming, deadman, or receiver control channels.

## Auxiliary Electronics System

- Kobalt 24V auxiliary battery
- Main fuse: TODO select fuse rating after measured load current
- Main switch
- 24V-to-5V buck converter
- 24V-to-12V buck converter
- Raspberry Pi 4B on 5V rail
- Arduino Nano on 5V rail
- USB or 5V camera, unless a documented 12V camera is selected
- Optional IMU, GPS, and environmental sensors
- Optional 12V light bar, fan, or camera load

## Grounding

Use a single-point auxiliary ground architecture for the auxiliary electronics domain.

Do not create a direct power tie between the RC battery and Kobalt auxiliary battery. Any future cross-domain connection must be documented as signal-only or observational before use.

## Pre-Test Checks

- Confirm the RC system drives normally with auxiliary electronics off.
- Confirm auxiliary electronics boot normally with RC system off.
- Confirm both systems can operate together without voltage drop, resets, or control anomalies.
- Confirm the Pi has no wiring path to steering, throttle, ESC, or receiver control outputs.
- Confirm all fuses and switches are accessible.

## TODO Hardware Values

- Main fuse rating
- Buck converter model numbers
- Wire gauge by segment
- Camera model and mount location
- Sensor part numbers and bus assignments
- Enclosure airflow plan
