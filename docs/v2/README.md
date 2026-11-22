# LitterBuggy V2 / engineering draft R0

Prepared 2026-11-21 for technical review in Junk-O-Matic. This package reconstructs
the existing build as far as the supplied evidence allows. Proposed details are
visible and separate from current physical facts. **Elegoo Uno R3 is confirmed
by the owner.** Nothing was uploaded to the buggy or installed on the Pi.

## Review in requested order

| Stage | Editable source | Review export / supporting files |
| --- | --- | --- |
| 1 System overview | [System overview](../../hardware/v2/architecture/v2_system_overview.drawio), [power domains](../../hardware/v2/architecture/v2_power_domains.drawio), [data flow](../../hardware/v2/architecture/v2_data_flow.drawio) | [Overview PDF](../../hardware/v2/architecture/v2_system_overview.pdf), [domains PDF](../../hardware/v2/architecture/v2_power_domains.pdf), [data PDF](../../hardware/v2/architecture/v2_data_flow.pdf); matching SVGs |
| 2 Power schematic | [QElectroTech project](../../hardware/v2/electrical/v2_electrical.qet) | [Three-sheet native PDF export](../../hardware/v2/electrical/v2_electrical.pdf) |
| 3 Wiring | [Power YAML](../../hardware/v2/wiring/v2_power_harness.yml), [sensor YAML](../../hardware/v2/wiring/v2_sensor_harness.yml) | [Power diagram](../../hardware/v2/wiring/exports/v2_power_harness.svg), [sensor diagram](../../hardware/v2/wiring/exports/v2_sensor_harness.svg), HTML/PDF/PNG/BOM exports; [registers and caveats](../../hardware/v2/wiring/README.md) |
| 4 Mechanical assembly | [Assembly FCStd](../../hardware/v2/mechanical/v2_assembly.FCStd), [cart mount](../../hardware/v2/mechanical/v2_cart_mount.FCStd), [battery mount](../../hardware/v2/mechanical/v2_battery_mount.FCStd), [enclosure](../../hardware/v2/mechanical/v2_electronics_enclosure.FCStd), [sensor mounts](../../hardware/v2/mechanical/v2_sensor_mounts.FCStd) | [Assembly PDF](../../hardware/v2/mechanical/exports/v2_assembly.pdf), [STEP/PDF/PNG exports](../../hardware/v2/mechanical/exports), [parameters and generation guide](../../hardware/v2/mechanical/README.md) |
| 5 Firmware / Pi logger | [Uno source and build guide](../../software/v2/arduino/README.md), [Pi source and operation](../../software/v2/raspberry_pi/README.md) | [Serial contract](serial_protocol.md), [tests](../../software/v2/tests), [validation report](validation.md) |

Also provided: [component BOM](bom.csv), [assembly/operation draft](assembly_and_operation.md),
[source and decision notes](sources_and_decisions.md), [118-item verification record](../v2_verification/README.md).

## Read the evidence markings

Confirmed, conflicting, proposed and unknown retain the meanings in the
verification record. In diagrams, blue/historical means an observation from
earlier media, not current physical verification. Green is reserved for the
owner-confirmed Uno identity; its wires and program remain separate claims.
Dashed architecture links are unresolved/proposed. QET wires explicitly labelled
TBD are review hypotheses. Logical connector names are not physical pin numbers.

Mechanical models are **illustrative layout geometry**, with no measured
dimensions entered. Native documents and STEP are real editable solids; valid
geometry does not establish fit, strength or installation accuracy. All PDFs
identify the draft state. No fabrication holes, fuse sizes or cable gauges were
invented. The battery dock model records an envelope, not a designed new bracket.

The new firmware defaults all sensor drivers/feedback off until wiring review.
The implemented drivers compile when enabled with test assignments, which are
not claimed as installed wiring. The proposed serial format and Pi logger are
new drafts, distinct from the unrecovered original Arduino sketch. Synthetic
fixtures are explicitly labelled. No original alarm threshold is assumed.

## Check-do-check review sequence

1. Check references and evidence status for the subsystem.
2. Review the native file beside its export.
3. Compare uncertain details with the physical buggy and record corrections.
4. Regenerate the affected exports and repeat the relevant validation.
5. Record the reviewed configuration and evidence before releasing hardware use.

The existing V1A source and historical procedures remain in their original paths.
V2-R0 is a review revision, not a declaration that legacy field gates passed.
