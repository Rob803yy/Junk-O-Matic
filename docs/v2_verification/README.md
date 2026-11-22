# LitterBuggy V2 verification record / R1

Record opened and reconciled 2026-11-21. Initial main audit: b163861c78d02060da30a026469f19e3c1409d11. R1 adds the supplied S01–S14 references and preserves source-qualified historical claims.

**Owner-confirmed current controller: Elegoo Uno R3.** Its power, pins and running sketch remain separate verification items. Pi and range-sensor conflicts remain open. No new physical inspection or measurements were performed.

There are 118 bounded verification records: 15 confirmed, 4 conflicting, 12 proposed, 87 unknown. Counts are evidence states, not completion percentages. Confirmed includes repository/source facts, not installed-hardware certification.

See [38 discrepancy resolutions](../reconciliation/README.md), [current engineering review](../v2/README.md), [structured register](verification-register.json), [capture templates](capture-templates.json) and [verification procedure](verification-session.md). R0 historical media inspections are described in [source notes](../v2/sources_and_decisions.md).

## Status meanings

- **confirmed**: Supported bounded claim; evidence basis must be stated. Repository content and historical owner observations do not establish current physical condition.
- **conflicting**: Sources disagree or project definitions diverge; resolution pending or historical documents still need reconciliation.
- **proposed**: Suggested design, method or requirement; not evidence of installation or completion.
- **unknown**: Insufficient evidence for current state, exact value or operation; historical claims may exist.

Version naming remains provisional. Repeated assistant claims, concept posters, source quantities, simulated approvals and derived reports do not establish current physical condition. All measured CAD values are null. Current PDFs remain held; old R0 PDF content is stale for R1.

## Verification items

| ID | Subject | Status | Bounded recorded value | Sources | Next verification |
| --- | --- | --- | --- | --- | --- |
| V2-001 | Project repository | confirmed | Rob803yy/Junk-O-Matic selected by owner | U01 | Retain repository identity in all records. |
| V2-002 | Physical build name | confirmed | Owner calls current physical configuration V2 | U02 | Assign a dated configuration revision after inventory. |
| V2-003 | Repository stage mismatch | conflicting | Repository describes V1.0A; owner requests current V2 reconstruction | R01, U02 | Define physical build revision separately from software/test stage; owner confirms terminology. |
| V2-004 | Controller identity | confirmed | Elegoo Uno R3; owner explicitly confirmed on 2026-11-21 | U03, C02 | Optional dated board-label photograph strengthens identification; do not substitute Nano. |
| V2-005 | Historical Nano references | conflicting | README, BOM, wiring notes and test procedure specify Nano; current controller is Uno R3 | R01, R02, R04, R07, U03 | Reconcile affected documents after recording exact Uno wiring and power. |
| V2-006 | Pi hardware identity | conflicting | S06 proposes reuse of Pi3B; S04/posters/repository name Pi4. Actual board identity remains unknown. | R01, R07, S04, S06 | Read board label and OS model output; capture RAM and board revision. |
| V2-007 | SCX6 identity | unknown | SCX6 is described in project scope and prior reviews; exact installed variant unverified | R01, C03, C04 | Record product label, chassis variant and installed modifications. |
| V2-008 | Cart identity | unknown | Prior reviews describe Gorilla Cart; exact model unverified | C03, C04 | Record cart label/model and distinguish tub from complete original cart. |
| V2-009 | Configuration date and change history | unknown | No dated current as-built inventory established | U02 | Owner records last modifications and inspection date. |
| V2-010 | Front and left/right convention | confirmed | Owner confirms yellow-handle end is driving front. CAD-R2 +X forward, +Z up; -Y enclosure side. | C04, CAD-U01 | Record physical left/right from this datum before measuring. |
| V2-011 | Control authority | proposed | Repository intends manual RC drive with Pi/Arduino observational only | R01, R04 | Owner confirms actual current control interfaces; trace wiring before asserting separation. |
| V2-012 | Drive modifications | unknown | Prior assistant review mentions rear-wheel drive; not independently verified in this audit | C04 | Photograph drivetrain and record installed/disconnected shafts and current driven axles. |
| V2-013 | Auxiliary battery identity | unknown | Kobalt 24V described in repository and prior adapter discussion | R01, C01 | Photograph pack label; record model, capacity, condition and exact nominal/max label ratings. |
| V2-014 | Kobalt adapter identity | unknown | Prior chat identifies photographed part as Kobalt dock; manufacturer/model unverified | C01 | Record adapter markings, connector and mounting provisions. |
| V2-015 | Propulsion battery | unknown | Owner task names 3S propulsion power; installed pack details unverified | U02 | Record label, chemistry, capacity, cell count, connector and retention. |
| V2-016 | 5V converter | unknown | S04 lists a primary 24V-to-5V 10A converter. Actual model, continuous capability and load unverified. | R02, R07, S04 | Record model, labelled input/output ranges and current rating. |
| V2-017 | 12V converter | unknown | Repository calls for 24V-to-12V buck; installed unit unverified | R02, R07 | Record model, labelled ranges and actual connected loads. |
| V2-018 | Other converters | unknown | S04 V1.0 C33 separately lists 24V-to-5V 3A converter U5A. Fitting and routing unverified; no parallel output assumed. | R02, S04 | Inventory every converter and identify its source and loads. |
| V2-019 | Main fuse | unknown | Repository lists fuse with TODO rating; installation unverified | R02 | Record location, holder type, installed rating and protected wire segments. |
| V2-020 | Branch fuses | unknown | No current branch protection inventory | R02 | Inspect each source branch and record installed protection or explicitly absent. |
| V2-021 | Main switch | unknown | Main switch is a repository architecture item | R02 | Record installed switch model, rating, poles and interrupted conductor. |
| V2-022 | RC receiver | unknown | Repository calls receiver stock; actual model unverified | R01, R02 | Read label and record channel wiring. |
| V2-023 | ESC | unknown | Repository calls ESC stock; actual model/settings unverified | R01, R02 | Record model and current configuration without changing settings. |
| V2-024 | Motor and gearing | unknown | Repository calls traction motor stock; actual hardware unverified | R01, R02 | Record motor label, gearing and transmission configuration. |
| V2-025 | Steering and shift servos | unknown | Installed servo models and supply paths unverified | R02 | Record labels, channels and any external BEC. |
| V2-026 | IMU | unknown | Prior assistant identifies MPU-6050 breakout; current installation not re-inspected | C02 | Photograph board and markings; identify breakout variant and orientation. |
| V2-027 | Ultrasonic sensor | conflicting | Historical HC-SR04; S06 reports it lost. A02YYUW UART is a proposal. Current installed/absent/replaced state unknown. | C02, S06 | Photograph label and installed connector. |
| V2-028 | LED and resistor | unknown | Prior assistant describes red LED on breadboard | C02 | Record installed LED, series resistance and wiring. |
| V2-029 | Buzzer | unknown | Prior assistant describes buzzer; active/passive type unverified | C02 | Identify installed module/type and drive circuit. |
| V2-030 | OLED | proposed | Prior discussion considered OLED; installed status unverified | C02 | Owner confirms fitted or absent; if fitted record markings and controller. |
| V2-031 | Camera | unknown | Repository supports optional camera; no current model established | R01, R06 | Record camera type, interface, mounting and installed status. |
| V2-032 | Temperature sensor | unknown | Repository schema includes enclosure temperature; sensor presence unverified | R03, R08 | Record actual sensor or explicitly absent. |
| V2-033 | Voltage sensing hardware | unknown | Stub mentions voltage dividers but does not read them | R08 | Inventory actual dividers/ADC modules and calibrated ratios; do not infer fitted sensors. |
| V2-034 | GPS and environmental sensors | proposed | Optional repository items without installation evidence | R02 | Owner confirms absent or identifies each fitted module. |
| V2-035 | Lighting and fan loads | unknown | Prior reviews mention lighting; repository lists optional 12V loads | C04, R02 | Inventory each light/fan and record source, model and measured load. |
| V2-036 | Breadboard and interconnects | unknown | Prior chat describes breadboard sensor circuit | C02 | Record current breadboard/terminal arrangement and all connector identifiers. |
| V2-037 | Electronics enclosure | unknown | Prior reviews describe orange enclosure; dimensions and model unknown | C01, C03 | Record material, dimensions, ingress provisions and mounting method. |
| V2-038 | Connection trace completeness | unknown | No pin-to-pin current wiring drawing in reviewed repository | R02, R10 | Assign component/connector IDs and trace every conductor with power disconnected. |
| V2-039 | Propulsion positive and return path | unknown | 3S-to-ESC path not traced | U02, R02 | Record battery connector, switch/protection if fitted, ESC input polarity and return. |
| V2-040 | ESC motor connections | unknown | Installed motor phase/power wiring unverified | R02 | Trace ESC outputs to motor; label wires and connectors. |
| V2-041 | Receiver/ESC/BEC path | unknown | Receiver power and BEC topology unverified | R02 | Trace receiver ports and supply conductors; record external BEC if any. |
| V2-042 | Steering/shift channel paths | unknown | Channel assignments not recorded | R02 | Record receiver channel, servo connector orientation and supply source. |
| V2-043 | Auxiliary battery-to-adapter | unknown | Adapter contact polarity and connector pin numbers unverified | C01 | Map labelled contacts and output leads; verify polarity with appropriate measurement. |
| V2-044 | Adapter-to-fuse-to-switch | unknown | Repository lists intended elements; installed order unverified | R02 | Trace exact order, distances from source and unprotected segments. |
| V2-045 | Converter input distribution | unknown | Parallel feeds and terminal distribution unverified | R02 | Record each converter input source, connector pin, polarity and protection. |
| V2-046 | Pi power entry | unknown | 5V rail intended; USB-C versus GPIO or other entry unverified | R02 | Trace actual entry connector and cable; record any alternate power inputs. |
| V2-047 | Uno external power entry | unknown | Prior chat mentions buck supply; barrel/VIN/5V pin path unknown | C02, R02 | Record exact pin/connector and supply setting; inspect simultaneous USB/external power arrangement. |
| V2-048 | Pi-to-Uno link | unknown | USB serial intended; current physical link and recognition unverified | R04, C02 | Record cable endpoints, data capability, serial identity and USB power path. |
| V2-049 | Auxiliary common returns | unknown | Single-point ground is a repository instruction, not verified implementation | R02 | Map actual return junctions, conductor paths and chassis connections. |
| V2-050 | RC/auxiliary separation | unknown | Repository asserts independent domains; physical isolation not established | R01, R02 | Trace all shared grounds/signals/shields/metal contact paths and document actual topology. |
| V2-051 | Uno-to-IMU wiring | unknown | I2C discussed; actual SDA/SCL/power/return pins unverified | C02 | Trace each wire; record breakout supply and pull-up rail after identifying module. |
| V2-052 | Uno-to-ultrasonic wiring | unknown | Trigger/echo assignments and sensor supply unverified | C02 | Record Uno pin, sensor pin, voltage and any interface components. |
| V2-053 | Uno-to-LED wiring | unknown | Pin, polarity and resistance unverified | C02 | Trace digital output through resistor and LED to return. |
| V2-054 | Uno-to-buzzer wiring | unknown | Pin, polarity and driver components unverified | C02 | Trace supply/control and record transistor/diode if fitted. |
| V2-055 | OLED bus/power wiring | unknown | Proposed I2C arrangement must not be treated as installed | C02 | If fitted trace actual VCC/GND/SDA/SCL and identify voltage compatibility. |
| V2-056 | Camera wiring | unknown | Camera interface and supply unverified | R02, R06 | Trace USB/CSI/other data and power cables. |
| V2-057 | Voltage sense paths | unknown | Battery/rail inputs not mapped | R03, R08 | If fitted record resistor values, reference, ADC channel and calibration; verify before energizing. |
| V2-058 | Temperature and optional inputs | unknown | Sensor bus/pins and observational estop input not mapped | R03 | Record only fitted hardware and label absent schema fields explicitly. |
| V2-059 | Wire and connector specifications | unknown | Gauges, colours, lengths and connector part numbers not established | R02 | Record both ends, pin numbers, connector viewing direction, gauge, colour and length for each cable. |
| V2-060 | Harness strain relief and routing | unknown | No current routing evidence | R10 | Photograph route, abrasion points, moving clearances and strain relief. |
| V2-061 | USB connection history | confirmed | Owner previously reported Windows unknown-device entry disappears when Uno unplugged | C02 | Historical report only; repeat recognition check to establish current state. |
| V2-062 | Current USB health | unknown | No confirmed resolution found in reviewed chat | C02 | Record cable/host/port, OS recognition and stable serial capture result. |
| V2-063 | Auxiliary pack voltage | unknown | No measured current pack voltage established; stub 23.7 is synthetic | R08 | Record meter, pack state, time and terminal voltage; never use stub value as measurement. |
| V2-064 | Propulsion pack voltage | unknown | No current measurement established | U02 | Record pack total and cell readings using appropriate equipment. |
| V2-065 | Converter outputs unloaded | unknown | Stub 12.1/5.05 are fixed constants | R08 | Measure actual converter outputs with loads isolated as appropriate and record settings. |
| V2-066 | Converter outputs loaded | unknown | No loaded rail measurements established | R05 | Measure at converter and load during representative boot/logging/lighting load. |
| V2-067 | Pi input stability | unknown | No measured input minimum or transient evidence | R05 | Record input voltage under startup and combined loads; capture reset/undervoltage evidence. |
| V2-068 | Load currents | unknown | Auxiliary total and branch currents not measured | R02 | Record instrument/range, operating mode and steady/peak current per branch. |
| V2-069 | Fuse/wire adequacy | unknown | Fuse selection remains TODO in repository | R02 | Compare actual measured loads with identified conductor, connector, switch and converter ratings; document selection rationale. |
| V2-070 | Battery discharge protection | unknown | Prior adapter discussion raised cutoff question; installed protection unknown | C01 | Identify pack/adapter protection documentation and actual configured cutoff; record observed low-battery procedure. |
| V2-071 | Logic voltage compatibility | unknown | Exact sensor breakout tolerances/pull-ups unverified | C02 | Identify modules and their specifications; measure bus rail as needed before validating interfaces. |
| V2-072 | Thermal operating measurements | unknown | No current converter/enclosure temperature dataset established | R05 | Record ambient and component/enclosure temperatures during representative operation. |
| V2-073 | Dimension reference and state | proposed | Use mm with explicit datums; record payload, battery, surface and suspension condition | U02 | Label datums in photos; record instrument resolution and uncertainty for every measurement. |
| V2-074 | Overall assembly envelope | unknown | No current measured length/width/height | R10 | Measure assembled extremes including handle, lights and protrusions. |
| V2-075 | Wheelbase and track | unknown | Stock dimensions in prior research are not measurements of this build | C04 | Measure axle centres and tyre contact/centre references; state exact definition. |
| V2-076 | Ground and moving clearances | unknown | No measured current clearance envelope | C04 | Record underside clearance and interference through steering/suspension travel. |
| V2-077 | Cart dimensions and position | unknown | Tub length/width/depth and installed offsets unknown | C04 | Measure tub envelope, floor/rim heights and offsets from assembly datums. |
| V2-078 | Cart-to-chassis structure | unknown | Rectangular gray frame, inner members and tub brackets exposed in CAD-P04/P06. Owner confirms same mounting hardware and fixed gray frame with normal rear-hinged tub. Sections, dimensions, joints and load capacity unverified. Owner clarifies longitudinal members beneath frame and transverse member(s) above it. | C03, C04, CAD-P04, CAD-P06, CAD-U03, CAD-U04, CAD-U05, CAD-U06, CAD-U07 | Measure member sections, spans, attachment points and joint hardware. |
| V2-079 | Mount hole patterns | unknown | No measured cart/frame/enclosure/dock hole coordinates | C01, R10 | Record X/Y/Z, diameter, spacing, slot extent, fastener and datum for each interface. |
| V2-080 | Battery and dock envelope | unknown | Actual pack/dock dimensions and removal travel unknown | C01 | Measure installed envelope, latch access, slide direction and required extraction space. |
| V2-081 | Dock mounting recesses | unknown | Prior photos did not establish whether recesses are mounting holes | C01 | Inspect with battery removed; record hole/boss type without assuming usable screw paths. |
| V2-082 | Battery mounting proposal | proposed | Plate and secondary strap suggested previously; not confirmed installed | C01 | Record actual mounting first; keep any redesign separate from as-built drawing. |
| V2-083 | Proposed plate size | proposed | Prior suggested roughly 4x6 inch plate and material thicknesses were estimates | C01 | Do not manufacture from suggestion; derive geometry from measured interfaces and loads. |
| V2-084 | Enclosure dimensions and layout | unknown | Enclosure broad vertical face is visible outside long wall (CAD-P01/P02). Actual dimensions/internal layout unknown; source nominal size is not measured. | R10, S04, CAD-P01 | Measure actual case, mounting and internal clearances. |
| V2-085 | Sensor positions and axes | unknown | Two white front light points observed (CAD-P02); sensor installation/orientation unresolved. Historical ultrasonic excluded from CAD-R2 assembly. | C02, CAD-P02 | Inspect actual sensor module and mount; distinguish light hardware.  |
| V2-086 | Mass distribution | unknown | No complete current assembly/equipment mass record | C03 | Weigh components and assembly; record four-wheel loads on equal-height supports if available. |
| V2-087 | Suspension setup | unknown | Actual spring IDs, preload positions, shock mounts and oil state unknown | C03 | Photograph and record four corner settings before any adjustment. |
| V2-088 | Suspension travel and settling | unknown | Prior review reports asymmetric settling; no current calibrated corner measurements | C03 | Measure comparable chassis-to-axle gaps and repeat settling with fixed known load. |
| V2-089 | Historical right lean | confirmed | Owner described right sag during removal/replacement of books; books were left of centre | C03 | Preserve as historical owner observation; quantify separately in current configuration. |
| V2-090 | Roll mechanism and root cause | unknown | Prior assistant inferred suspension roll; fault/root cause not established | C03, C04 | Separate tub/chassis/axle motion with fixed references and repeatable loading. |
| V2-091 | Payload limits | unknown | Prior demonstrations and discussed targets do not establish validated capacity | C03, C04 | Define intended mass/offset/lean requirements and validate bounded operating conditions. |
| V2-092 | Loaded mobility history | unknown | Prior assistant reports loaded travel in videos 2231/2235; original media not re-reviewed here | C04 | Locate original media and link configuration, load, date and observed result. |
| V2-093 | Repository firmware nature | confirmed | telemetry_logger_stub.ino emits fixed illustrative values at nominal 1 s interval | R08 | Keep simulation explicitly identified; no sensor-acquisition claims. |
| V2-094 | Running Uno firmware | unknown | Owner reported code on Uno and lost sketch; running image not identified | C02 | Locate original source/build artifacts; record source hash or unknown and preserve firmware before replacement. |
| V2-095 | Firmware preservation | proposed | Search original source first; preserve readable firmware and verify repeat reads before upload | C02 | Record tool/version, exact operation, result and hashes; binary backup is not recovered source. |
| V2-096 | IDE/toolchain/libraries | unknown | Actual IDE, board package and library versions unrecorded | C02 | Record installed tool versions and board selection; capture reproducible compile output once source recovered. |
| V2-097 | Existing sensor behaviour | unknown | Original sample timing, alarms and filtering unrecorded | C02 | Capture observed output/LED/buzzer behaviour without overwriting firmware. |
| V2-098 | Actual serial format | unknown | Running serial format unknown. R1 new code uses JSON protocol2 at proposed115200/10Hz; S06 CSV D/H is a competing proposal, not recovered format. | R08, C02, S06 | Capture unedited serial bytes with port/baud/time; retain headers, malformed lines and startup output. |
| V2-099 | Stub/logger format pairing | confirmed | Stub JSON field names align with logger telemetry columns; runtime compatibility untested | R03, R08, R09 | Replay synthetic lines separately from physical sensor validation. |
| V2-100 | Protocol metadata | proposed | Document version, units, timestamps, sequence, validity and missing-data rules after current output capture | R03, R09 | Define one shared contract and distinguish simulator values from measured values. |
| V2-101 | Sensor calibration | unknown | No current bias/scale/orientation/distance calibration evidence | C02 | Record procedures, reference values, residual error and calibration version per sensor. |
| V2-102 | Pi operating environment | unknown | Current OS, Python, dependencies and storage unknown | R06 | Record OS/model/Python/package versions, time sync, storage free space and output path. |
| V2-103 | Pi logger deployment | unknown | Repository contains jom_data_logger.py; installation/running process unverified | R09 | Locate deployed file, hash and command; compare with repository commit. |
| V2-104 | Logger startup/service | unknown | No demonstrated current service/boot setup | R06, R09 | Record actual manual/service launch, user, working directory and shutdown procedure. |
| V2-105 | Serial disconnect handling | confirmed | Inspected logger has no reconnect loop; readline failures are not handled in worker | R09 | Test unplug/replug using test harness or controlled bench; define expected recovery before field use. |
| V2-106 | Telemetry validation gaps | confirmed | Logger accepts JSON objects without required-field/type checks; non-object JSON can raise on .get | R09 | Test missing fields, wrong types, arrays/null, partial lines and document results before reuse. |
| V2-107 | Sample provenance gaps | confirmed | Logger adds Pi receive time but does not preserve raw lines or device sequence/sample time fields | R09 | Define raw capture and sample provenance needed for validation; verify actual deployed behaviour. |
| V2-108 | Camera success reporting | confirmed | Code records requested video path but does not check capture/writer isOpened or report camera faults into faults.csv | R09 | Test unavailable camera and review actual file/frames before claiming usable recording. |
| V2-109 | Summary interpretation | confirmed | telemetry_rows counts parsed objects; summary does not calculate expected-row percentage or camera usable percentage | R09, R05 | Define denominators, timing and validity rules; assess validation separately from file creation. |
| V2-110 | Pi health evidence | confirmed | Code samples CPU/memory/disk/temp; it does not directly log undervoltage flags or reset cause | R09 | Capture independent power/reset evidence for any no-reset or rail-stability claim. |
| V2-111 | Time alignment | unknown | Actual Pi clock accuracy and sensor/video synchronisation unverified | R09 | Record clock source/offset and align a visible event with serial/log timestamp. |
| V2-112 | Software tests and field proof | unknown | No current hardware test result established by inspected source/sample files | R05, R09 | Run meaningful offline replay then bench tests; attach actual outputs and limitations. |
| V2-113 | Validation targets | proposed | Repository defines 10/10 starts, >=95% video/telemetry, five 45-minute sessions and rail stability | R05 | Owner reviews applicability to V2 and defines measurement methods; targets are not completed results. |
| V2-114 | Evidence archive | proposed | Large raw media/logs remain outside Git; commit lightweight metadata and hashes | R01, R05 | Choose durable archive and record accessible relative paths or links, not temporary preview paths. |
| V2-115 | Historical media traceability | unknown | Chat attachment names exist but original media content was not re-inspected in this audit | C01, C02, C03, C04 | Recover originals, hash files and associate with configuration/date/record IDs. |
| V2-116 | As-built drawing release | proposed | Create system overview, verified pin-to-pin wiring and dimensioned assembly from closed records | U02 | Label unresolved links/dimensions explicitly; no invented pins or manufacturing dimensions. |
| V2-117 | Repository guidance mismatch | confirmed | Current AGENTS.md now explicitly prioritizes owner-authorized V2 reconstruction, preserving historical dataset work separately. | R11, U02, U01 | Update guidance alongside later scope reconciliation; current owner instruction governs this work. |
| V2-118 | Change validation discipline | proposed | Record baseline then change one factor and repeat a comparable check | C03 | Link change, before/after configuration, result and any rollback; retain failed/negative evidence. |
