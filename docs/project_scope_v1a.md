# V1.0A - Instrumented RC Platform Scope

## Purpose

V1.0A validates Junk-O-Matic / Ideal Litterbuggy as an instrumented RC platform. The buggy is manually driven with the stock SCX6 RC system while auxiliary electronics record evidence.

## In Scope

- Manual RC driving through repeatable test routes
- Raspberry Pi camera recording
- Arduino telemetry logging over USB serial
- Pi health logging
- Run manifest generation
- Config snapshot per run
- Operator event marker logging
- CSV export for scorecard import
- Evidence folder link for each validation run

## Out of Scope

- Autonomy
- Computer driving
- Pi-to-ESC control
- Pi-to-steering control
- RC/computer relay handoff
- Automated scoop or manipulator control
- Assisted perception that changes vehicle motion
- Direct power tie between the RC drive battery and auxiliary electronics battery

## Control Authority

The stock Axial SCX6 transmitter, receiver, ESC, steering servo, and traction motor remain the only drive-control authority in V1.0A.

The Raspberry Pi must never send steering, throttle, deadman, arming, or motion commands.

## Success Statement

V1.0A is successful when repeated field sessions show that the auxiliary electronics can collect synchronized, reviewable evidence without disturbing RC control or power stability.
