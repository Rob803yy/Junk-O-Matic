# LitterBuggy V2 / engineering review R1

R1 reconciles the supplied V1/V2/V3 references on 2026-11-21. Start with the
[38 discrepancy resolutions](../reconciliation/README.md) and
[editable Word correction record](../reconciliation/editable/LitterBuggy_Version_Reconciliation_R1.docx).
**Elegoo Uno R3 is owner-confirmed.** Pi 3B/Pi 4 and the current range sensor
remain unresolved. The original version allocation was proposed. The owner has
since selected [assisted V3 planning](../v3/README.md): camera detection, operator
alerts and reliable logging with manual RC motion authority. This leaves the V2
physical evidence status and current runtime sources unchanged.

[Repository alignment review](../repository_review/README.md) covers the March/May
legacy folders; [next evidence plan](verification-plan.md) and
[environment setup](../environment-setup.md) distinguish current versus historical paths.

## Review in requested order

| Stage | Editable source | Current review material |
| --- | --- | --- |
| Architecture (ARCH-R2) | [Overview](../../hardware/v2/architecture/v2_system_overview.drawio), [power domains](../../hardware/v2/architecture/v2_power_domains.drawio), [data flow](../../hardware/v2/architecture/v2_data_flow.drawio) | Current SVG/PNG, evidence scopes and feedback IDs in [architecture review guide](../../hardware/v2/architecture/README.md) |
| Digital connectivity | [Connectivity diagram](../../hardware/v2/architecture/v2_digital_connectivity.drawio) | [SVG](../../hardware/v2/architecture/v2_digital_connectivity.svg); open UART replacement and power interfaces |
| Power schematic | [Three-sheet QElectroTech project](../../hardware/v2/electrical/v2_electrical.qet) | [Native PNG previews](../../hardware/v2/electrical/exports); all drawn nets untraced hypotheses |
| Wiring | [Power YAML](../../hardware/v2/wiring/v2_power_harness.yml), [sensor YAML](../../hardware/v2/wiring/v2_sensor_harness.yml) | [Registers and HTML/SVG/PNG/BOM](../../hardware/v2/wiring); logical functions, physical pins TBD |
| Mechanical assembly (CAD-R3) | [Assembly](../../hardware/v2/mechanical/v2_assembly.FCStd), [cart mount](../../hardware/v2/mechanical/v2_cart_mount.FCStd), [battery mount](../../hardware/v2/mechanical/v2_battery_mount.FCStd), [enclosure](../../hardware/v2/mechanical/v2_electronics_enclosure.FCStd), [sensor mounts](../../hardware/v2/mechanical/v2_sensor_mounts.FCStd) | [STEP/SVG/PNG](../../hardware/v2/mechanical/exports); [parameter provenance](../../hardware/v2/mechanical/dimensions.json) |
| Firmware and Pi logger | [Uno source](../../software/v2/arduino/README.md), [Pi logger/SQL/service](../../software/v2/raspberry_pi/README.md) | [Shared serial protocol](serial_protocol.md), [tests](../../software/v2/tests), [validation](validation.md) |

## Workbook and evidence controls

- [BOM Excel workbook](../reconciliation/editable/LitterBuggy_BOM_R1.xlsx), [CSV](bom.csv), [JSON](bom.json): source-listed versus installed quantities are separate; 23 future concepts stay outside current inventory.
- [Corrected scorecard](../reconciliation/editable/LitterBuggy_Scorecard_R1.xlsx): blank scores/evidence remain pending; category failure does not automatically claim a critical safety failure.
- [Corrected review data system](../reconciliation/editable/LitterBuggy_Review_Data_System_R1.xlsx): CFG-V2-R1 has no invented physical tests or approval. Historical CFG-001 results remain historical.
- [Verification register](../v2_verification/README.md), [source inventory](../reconciliation/source-inventory.json), [source decisions](sources_and_decisions.md), [assembly/operation draft](assembly_and_operation.md).

**PDF generation is held until owner review.** Existing R0 PDFs are historical
and stale for R1; [hashes and disposition](../reconciliation/export-status.json)
record the hold. Current review sources are editable files and SVG/PNG/STEP.
Word pagination and PDF proofing follow content review, as requested.

## Evidence markings and limits

Confirmed, conflicting, proposed and unknown have distinct meanings. ARCH-R2
uses these four states with a scope on every component. Green confirms only the
stated owner identity/relationship or source-only code behavior; it does not
verify installation, deployment or performance. The separate digital-connectivity
R1 diagram retains its historical legend. Dashed electrical links and QET TBD
nets are unresolved/proposed; no physical connector numbering is implied.

ARCH-R2 separates physical support, power allocation and draft acquisition flow.
It incorporates CAD-R3's fixed outer frame, lower fore/aft members, upper transverse
member(s) and rear hinge. It keeps U5A unassigned and Uno power entry open, and
shows raw-first capture, validation/error storage and provenance from the actual
logger source. Existing firmware, wiring, CAD and all PDFs are unchanged by this pass.

CAD-R3 uses seven photograph references, including under-frame/low-front views and owner confirmation of the rear hinge and fixed frame; [mechanical review guide](../../hardware/v2/mechanical/README.md) and [observation record](../../hardware/v2/mechanical/photo-observations.json) describe the changes. Yellow-handle end is owner-confirmed front; bucket is omitted by owner request.

All CAD measured dimensions remain null. The enclosure layout uses an unverified
source catalog size; the other layout numbers are illustrative. Native solid
validity does not establish fit, moving clearance, load capacity or fabrication
dimensions. The historical HC-SR04 reference is hidden and excluded from the assembly/STEP; the fifth document now shows front lighting and a reserved sensor interface. Replacement is open.

New firmware defaults sensor drivers and feedback off. The optional HC-SR04
profile must be explicitly selected and cannot drive the proposed UART sensor.
The single JSON contract remains protocol 2, with proposed 10Hz records. It is
new code, separate from the unrecovered running sketch. No motion commands,
field deployment, actual hardware tests or validated payload/runtime/IP67 claim
are made. The existing V1A software and source claims remain historical.

## Check-do-check sequence

1. Compare each source claim with its evidence and current status.
2. Inspect native sources beside current previews; record uncertain details.
3. Measure/trace the physical build and preserve existing software.
4. Update the affected source and run relevant native/software checks.
5. Complete owner technical review, then regenerate and inspect PDFs.
