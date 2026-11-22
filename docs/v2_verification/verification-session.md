# V2 verification session guide

This is a proposed collection procedure. None of these steps is recorded as completed.

## 1. Establish the configuration

Assign a dated hardware configuration identifier, for example V2-2026-11-21-A only if that is the actual inspection date. Record subsequent physical changes as a new revision. Keep physical revision distinct from repository software/test stage.

Confirm the assembly orientation before measuring: identify handle end, steering axle, front/rear and left/right in an annotated overall photo. Choose fixed datums and record axis directions. Use millimetres for geometry; preserve raw units and conversions when necessary. A dimension is usable only with endpoints, datum, method and uncertainty/resolution.

Photograph the complete assembly from front, rear, both sides, top and underside as accessible, followed by labels and mounting interfaces. A photograph of a label supports identification; it does not establish performance. Record which batteries, payload and accessories are present.

Begin with the confirmed Uno R3. Inventory the Pi, both battery systems, adapter, converters, protection, switches, controller/servos, sensors, lights, enclosure and structural interfaces. For optional equipment, explicitly record installed, removed or not installed with evidence. Do not turn optional plans into shopping requirements.

## 2. Preserve software before changing it

Locate original Uno sketches and build artifacts before replacing code. Record file paths, dates, source hashes, toolchain and libraries if found. If firmware readback is pursued, record the tool, read operation, two read results and hashes; assess whether a complete usable backup was obtained. A matching pair is evidence of repeatability, not automatic proof of full recoverability. A binary backup does not restore original variable names, comments or source structure.

Do not upload the repository stub as a recovery method. Preserve current LED/buzzer behaviour and serial output. USB recognition was historically unresolved, so record today's host/cable/port/device result rather than assuming an available COM port. Opening a serial connection can reset some boards; record startup effects.

On the Pi, identify the actual deployed logger file, launch command/service, dependencies, OS, clock state and storage. Compare deployed file hashes with the audited repository version. “Exists in Git” and “running on the Pi” are separate claims.

## 3. Trace actual connections

With sources disconnected, assign component and connector IDs and trace one circuit at a time. Never use resistance/continuity mode on an energized circuit. Record connector viewing direction so pin numbering is unambiguous.

Trace propulsion battery to ESC/motor and receiver/servo power first; then auxiliary pack to adapter, fuse, switch, converters, Pi, Uno and loads. Map actual return paths and any domain-crossing signals, grounds, shields or chassis paths. Repository intent is not evidence of physical separation.

For every conductor, record both connector pins, function, colour, gauge, length and routing. Explicitly distinguish Uno barrel input, VIN, 5V pin and USB power; record simultaneous sources before deciding whether the arrangement is appropriate. Identify breakout variants before validating power and logic compatibility. A suggested SDA/SCL assignment is not an observed connection.

Complete a connection record only when both endpoints are known and evidence identifies the traced route. Untraced wires remain unknown and appear as unresolved in drawings.

## 4. Measure geometry

Measure the overall envelope, wheelbase/track with precise definitions, cart envelope and offsets, mounting frame sections, hole patterns, enclosure usable volume, battery/dock and extraction space, and sensor positions/axes.

Record X/Y/Z coordinates from named datums, hole diameters and slot extents, fastener sizes and material thickness. Include the actual installed battery and latch access when checking the dock. Do not assume that the photographed dock recesses are mounting holes.

Measure representative steering and suspension clearances without changing setup. Record all four spring identities, preload collar settings, mounts and chassis-to-axle gaps before tuning. Photograph the setup and record payload state. Stock SCX6 dimensions and prior approximate image angles are not measured as-built geometry.

A dimension is accepted for CAD only when endpoints, units, configuration and resolution/uncertainty are recorded and fit-critical dimensions have an independent repeat check. Mark unresolved dimensions as unknown; do not fabricate dimensions to complete the model.

## 5. Measure electrical operation

After identifying connections, polarity and equipment ratings, record actual source voltage, converter settings, load input voltage and current in defined operating modes. Use instruments and measurement arrangements appropriate to the circuit. Do not place an ammeter directly across a battery.

Record unloaded and representative loaded conditions separately, including boot, logging and lighting. Write down instrument range/resolution, ambient temperature, pack state and measurement location. A single multimeter reading does not establish transient performance. Capture voltage traces if transient claims require them.

Select acceptance limits from the actual equipment documentation and agreed operating requirements. The old repository gives no measured fuse sizing or rail stability evidence. Compare identified conductor/connector/switch/converter ratings with measured loads. Document battery discharge protection and current power-entry arrangements.

## 6. Capture behaviour and validate software

Preserve raw serial bytes with port identity, baud, start/end times and configuration. Do not discard malformed lines or startup messages. Identify fields, units, timing and actual sensor source before choosing a final protocol.

Replay synthetic fixtures separately from real captures. Check incomplete and malformed lines, missing fields, wrong types, arrays/null, disconnection/reconnection and process shutdown. Test camera-unavailable behaviour and inspect generated video files/frames. Record expected and actual results with evidence; a passing source review is not a hardware test.

Capture a physical reference event visible in video and reflected in telemetry when checking time alignment. Record Pi clock accuracy and any serial/processing delay.

For percentage telemetry completeness, define the interval, expected sample rate, valid-row rule, sequence/drop accounting and startup/shutdown exclusions. Report received, valid, malformed and missing samples separately. “Rows exist” is not 95% complete.

For video usability, define recorded versus expected duration, playable frames, view obstruction and timestamp/alignment criteria. A configured video filename is not proof that recording succeeded.

For boot/no-reset claims, use dated independent runs and appropriate power/boot diagnostics. CPU temperature and row count alone do not establish reset-free operation or stable power.

## 7. Preserve mechanical observations without overclaiming

Keep the owner-reported left-of-centre book stack and right sag as historical evidence. Recover original media before relying on earlier assistant frame interpretations. Record original file hash, capture date if known, configuration and any missing context.

If measuring lean, use known secured loads and recorded positions, comparable surface/setup, and separate tub/chassis/axle references. Record four corner gaps and repeat settling from controlled disturbance. Do not infer a failed spring, completed repair or payload limit from one image or successful drive.

Define intended payload, offset, terrain and acceptable lean before claiming an operating envelope. Existing test targets and discussed load goals remain proposed until their applicability is agreed and results support them.

## 8. Close and publish records

For each record, retain the original claim, add dated evidence, state the precise resolved claim, and record reviewer and hardware/software revision. Use the resolution template for status transitions. For confirmed owner statements, say “owner confirmed”; for measured observations, identify the measurement. A physical claim needs physical evidence or explicit owner confirmation appropriate to that claim.

Unknown becomes confirmed only when its specific requested check is completed and the relevant component/connection/measurement/test fields are populated. Conflicting becomes confirmed when the discrepancy is explained and the current claim has support; update affected documents in a later scoped change. Proposed becomes confirmed only if the claim changes to a supported fact of adoption/installation/result; an approved requirement remains a requirement, not a test pass.

Store large raw evidence in a durable archive outside Git. Commit small project-relevant metadata, checksums and appropriately redacted evidence as needed. Avoid temporary preview paths, secrets and unrelated chat history. A hash identifies content; it does not prove when or how it was captured.

Keep this README and verification-register.json aligned. Record dates and sources for every closure. Update drawings, software and BOM only after the related facts are established, or label unresolved features visibly.

## First collection batch

1. Owner confirmation or label photo of the Pi model; Uno is already owner-confirmed.
2. Label photos of propulsion pack, Kobalt pack, adapter and each converter.
3. Current Uno power-entry connection and Pi-to-Uno cable endpoints.
4. Overall assembly and enclosure interior photos with named orientation.
5. Existing Uno source/backup location if known, current USB recognition result and an unedited serial capture if available.
6. Current installed sensor list, including whether OLED/camera/temperature/voltage sensors are fitted.

These six groups unlock the inventory and power trace without requiring all 118 records to be answered at once.
