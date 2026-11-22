# Version reconciliation R1

Reconciled 2026-11-21. **Corrected editable sources are ready for technical review; physical unknowns remain unknown.**

The owner confirms an Elegoo Uno R3. Version naming is proposed pending owner confirmation: V1 historical RC baseline, V2 current reconstruction/reliability/instrumentation, V3 future concepts. Pi 3B/Pi4 and range-sensor state remain conflicting.

## Latest CAD feedback

CAD-R2 refines the five models against three additional owner photographs. Yellow-handle end is confirmed front; bucket omitted by owner request. See [mechanical review guide](../../hardware/v2/mechanical/README.md). R1 documents below remain the earlier reconciliation baseline; current CAD-R2 geometry supersedes their older mechanical proxy descriptions. No PDFs were regenerated.

## Review files

- [Unified editable Word correction record](editable/LitterBuggy_Version_Reconciliation_R1.docx)
- [Normalized BOM](editable/LitterBuggy_BOM_R1.xlsx)
- [Corrected scorecard](editable/LitterBuggy_Scorecard_R1.xlsx)
- [Corrected review data system](editable/LitterBuggy_Review_Data_System_R1.xlsx)
- [Engineering sources in requested review order](../v2/README.md)
- [Machine-readable discrepancy register](reconciliation-register.json) and [source hashes](source-inventory.json)
- [PDF hold and historical hashes](export-status.json)

Original Downloads files remain unchanged. Six [annotated editable Word source copies and a text amendment](historical-editable) retain technical source wording under an explicit correction cover. The unified current Word record and three corrected workbooks are also stored in GitHub. S11’s unrelated biography is omitted from its public copy; the full source remains local. Original PDF and concept posters remain source evidence; no replacement PDF is generated.

## Source dispositions

- **S01 Junk-O-Matic_V1_to_V2_Scorecard_Report.xlsx**: Corrected editable scorecard. Candidate gates retained with scope notes; no physical completion or release inferred.
- **S02 Litterbuggy_V1.0_Design_Review (2).docx**: Annotated historical design review. Duplicate event analyses and subjective confidence are qualified; pavement travel does not establish current approval.
- **S03 Litterbuggy_SCX6_V1.0_Integrated_Product_Design_Specification_Rev0 (1) (2).docx**: Annotated historical product specification. Simulated consensus and development payloads are proposals. Requirement IDs are source-qualified IPDS0.
- **S04 Bill Of Material (1).xlsx**: Replaced for current use by normalized R1 BOM. Raw rows and original ambiguous symbols retained on Source catalog.
- **S05 Litterbuggy_Design_Review_Data_System_Rev0 (2).xlsx**: Corrected editable review system. Historical findings remain scoped to CFG-001. New current config has no fabricated test results or approval.
- **S06 LitterBuggy V2 Engineering Deep Research Report.docx**: Annotated research report. Field observations remain report-attributed. Pi3B, lost sensor and replacement proposals are carried as conflicts/open decisions.
- **S07 SCX6 Litterbuggy & Robotic Trash Picker Master Reference.md.pdf**: Original PDF unchanged per owner instruction. Reference overlap with S09 is not independent corroboration; this R1 correction record governs current use.
- **S08 Litterbuggy & Axial SCX6 Offline Master Guide.docx**: Annotated historical guide. Stock capacities, upgrades and generic common-ground directions are not approved as-built specifications.
- **S09 SCX6 Litterbuggy & Robotic Trash Picker Master Reference.md.txt**: Annotated local text copy. Generic payload, 3S/4S and fuse prescriptions are superseded by unverified current-state entries.
- **S10 Download the Litterbuggy Robotic Trash Picker Offline Engineering Reference.docx**: Annotated historical engineering reference. PCA9685/arm/closed-loop controls are proposals; purchased discussion is not installed inventory.
- **S11 Litterbuggy_Consolidated_Reference.docx**: Annotated historical consolidated reference. RevB rail/cradle/trailer and third-party test-count claims do not establish current integration.
- **S12 Attached concept poster V1**: V1 concept poster: Mega, tool-pack brands, autonomy, dimensions, payload and environmental claims not established as current hardware.
- **S13 Attached concept poster V2**: V2 concept poster: Milwaukee M18, Mega, autonomy, encoders, RTK, runtime and payload remain concept claims; not the owner-confirmed Uno baseline.
- **S14 Attached concept poster V3**: V3 concept poster: Nano, mixed 18V/24V Kobalt label, dual bins, intake, backup rail and autonomous modes remain future concepts.

## 38 discrepancy resolutions

### REC-001 — Version labels

Source claim: V2 variously means autonomy, assisted collection, payload integration or reliability retrofit.

**R1:** Use distinct axes: V1 historical baseline, V2 current physical reconstruction/reliability/instrumentation, V3 future concepts. This editorial mapping is proposed for owner confirmation; legacy labels remain source-qualified.

Sources: S02 t27; S03 t15; S06 p64; S08 p8-p11; S12-S14. Disposition: pending owner nomenclature.


### REC-002 — Controller identity

Source claim: Mega in V1/V2 posters; Nano in V3, old repo; Nano/Pico in BOM.

**R1:** Current owner-confirmed controller is Elegoo Uno R3. Kits, Mega, Nano and Pico are historical alternatives, not current installed identity.

Sources: Owner 2026-11-21; S04 V1.0!C26; S04 V2.0!C14; S12-S14. Disposition: resolved documentary.


### REC-003 — Pi model

Source claim: Pi 4 in BOM/posters; Pi 3B in research report.

**R1:** Raspberry Pi model remains conflicting; no Pi-specific current rating or enclosure fit is confirmed.

Sources: S04 V1.0!C25; S06 p20,p87; S12-S14. Disposition: unresolved physical.
Physical follow-up: Read board label or /proc/device-tree/model.

### REC-004 — Tool battery family

Source claim: 18V generic/Milwaukee posters; V3 poster says 18V and Kobalt 24V MAX.

**R1:** Retain Kobalt 24V family as owner project scope. Pack label, capacity and voltage range remain unverified. Never substitute an 18V/20V-family cutoff.

Sources: Owner scope; S04 V1.0!C31; S12-S14. Disposition: resolved documentary.


### REC-005 — KB624-03 misidentification

Source claim: BOM calls KB624-03 a fuse switch.

**R1:** Official Kobalt documentation identifies KB 624-03 as a battery-pack model. Remove it as the switch/adapter part number. Physical pack identity still requires a label.

Sources: S04 V1.0!C30; https://pdf.lowes.com/useandcareguides/692042010705_use.pdf. Disposition: resolved documentary.


### REC-006 — Adapter quantity

Source claim: BOM lists two; photos show one photographed adapter.

**R1:** Record source-listed quantity 2 separately from installed quantity unknown. No inference of two fitted power feeds.

Sources: S04 V1.0!D31; S04 V2.0!D7; Historical adapter photos. Disposition: resolved documentary.


### REC-007 — Secondary 5V converter omitted in R0

Source claim: Source lists 5V 10A and separate 5V 3A converters; R0 drew only one.

**R1:** Add U5A secondary 5V source-listed candidate to architecture/power/connectivity and BOM. Leave output/load unconnected and never parallel outputs by assumption.

Sources: S04 V1.0!C32:C33; S04 V2.0!C8:C9. Disposition: resolved documentary.


### REC-008 — Converter ratings and 12V rail

Source claim: 10A/3A/5A labels presented as installed ratings.

**R1:** Treat as source-listed specifications, not verified output capability or measured load. 12V converter remains proposed/source-listed, not confirmed fitted.

Sources: S04; S12-S14. Disposition: resolved documentary.


### REC-009 — Protection ratings

Source claim: Generic 30A auxiliary and 60-80A traction fuses; mixed 5A/10A/15A kit.

**R1:** No installed fuse rating is established. Remove generic values from the active design; size against actual conductors, loads, connectors and source limits after verification.

Sources: S09 section 5; S04 V1.0!C34:C36. Disposition: resolved documentary.


### REC-010 — Grounds and isolation

Source claim: Some guides mandate common ground while others call the domains isolated.

**R1:** Separate source positives; actual returns and crossing signals must be traced. No RC/auxiliary ground tie or galvanic isolation is asserted.

Sources: S08 p40-p46; S09 section 5; S10 p88-p100. Disposition: resolved documentary.


### REC-011 — Uno power entry

Source claim: External buck discussed historically; research proposes Pi USB power.

**R1:** USB-A-to-B is the proposed data link. Uno external VIN/barrel/5V entry and simultaneous USB power remain unresolved; do not add a duplicate supply path.

Sources: S06 p74-p75; Historical Pi chat. Disposition: unresolved physical.
Physical follow-up: Trace both power entry routes and actual USB cable.

### REC-012 — Propulsion 3S versus 4S

Source claim: Generic reference permits 3S/4S; integrated spec retains 3S.

**R1:** Retain 3S as current project design scope. Actual pack and installed ESC limits remain verification items; no 4S change is adopted.

Sources: Owner scope; S03 t20r2; S09 section 5. Disposition: resolved documentary.


### REC-013 — 4WD versus RWD

Source claim: Prior chat review mentioned RWD; research rejects a stock transmitter 2WD mode.

**R1:** Stock SCX6 is 4WD with a two-speed transmission. Installed driven axles remain unknown until mechanical modifications are inspected; high/low gear is not 2WD/4WD selection.

Sources: S06 p7,p247; https://www.axialadventure.com/by-platform/scx6/. Disposition: unresolved physical.
Physical follow-up: Inspect shafts/axles and document any modifications.

### REC-014 — Range sensor current state

Source claim: Historical HC-SR04; research says lost and recommends A02YYUW.

**R1:** Record HC-SR04 as historical; present installation/replacement unknown. A02YYUW is a proposal, not a drop-in trigger/echo replacement.

Sources: S06 p21-p26,p87; Historical Pi chat. Disposition: unresolved physical.
Physical follow-up: Owner confirms sensor fitted or absent; inspect model.

### REC-015 — A02YYUW interface

Source claim: Replacement discussed beside HC-SR04 code.

**R1:** Manufacturer SEN0311 uses 9600-baud UART, not trigger/echo. Do not connect it to the HC-SR04 harness or enable that driver. Replacement needs its own pin/power/protocol review.

Sources: S06 p123-p124; https://wiki.dfrobot.com/sen0311/; https://wiki.dfrobot.com/sen0311/docs/21651. Disposition: resolved documentary.


### REC-016 — MPU heading and temperature

Source claim: BOM claims heading; old schema includes yaw/enclosure temperature.

**R1:** MPU raw axes and die-temperature counts do not establish absolute heading or enclosure temperature. Keep raw acquisition; no calibrated angles, compass or enclosure readings are invented.

Sources: S04 V2.0!F21; S06 p80; R0 protocol. Disposition: resolved documentary.


### REC-017 — Camera GPS lidar encoders and PCA9685

Source claim: Posters depict them; guides discuss purchases and integration.

**R1:** Classify as historical inventory claim or future proposal. Fitting, deployment and current part identity are unknown; exclude them from current mandatory wiring and actuator control.

Sources: S04 V2.0!C22:C31; S10 t4r2,t27r4; S12-S14. Disposition: resolved documentary.


### REC-018 — Autonomy and pickup claims

Source claim: Posters advertise autonomy, classification, return to base, anti-jam intake and dual bins.

**R1:** These are future concepts. Current source package is RC-observational acquisition; no deployed autonomy, powered intake, physical sorting or manipulator is established.

Sources: S12-S14; S02 t27; S03 t15; R0 source. Disposition: resolved documentary.


### REC-019 — BOM checkmarks

Source claim: Checkmarks/coloured symbols with no legend; ✔❌ ambiguous; footer rows shifted.

**R1:** Preserve raw rows as source catalog. Use explicit evidence status and separate listed/proposed quantity from verified installed quantity. Deduplicate shifted tail rows; never total ambiguous quantities as actual inventory.

Sources: S04 V1.0!E2:E53; S04 V2.0!A48:F56. Disposition: resolved documentary.


### REC-020 — Payload ratings

Source claim: 15-20kg safe continuous; posters 10-25kg; 15lb/20lb development plan; 50/60lb objectives.

**R1:** No validated modified-vehicle payload rating exists in the supplied evidence. Preserve these as separate source targets. Rough total litter collected is not simultaneous payload capacity.

Sources: S09 section 2; S12-S14; S03 p20; S06 p3,p54,p249; S11 t1r5. Disposition: resolved documentary.


### REC-021 — Runtime speed mass dimensions

Source claim: Posters advertise 2.4-3.6h, 0-1.5 or 1-5m/s, 15-25kg and 80-95cm dimensions.

**R1:** All are concept targets/estimates without current measurement. They do not populate measured CAD, runtime or operating-envelope cells.

Sources: S12-S14. Disposition: resolved documentary.


### REC-022 — Weather and IP67

Source claim: Posters label entire electronics system IP67; guides recommend sealed hardware.

**R1:** A component rating does not qualify the assembled enclosure/vehicle. Actual glands, seals, modifications and ingress tests remain unknown.

Sources: S12-S14; S06 p76; S03 OD-08. Disposition: resolved documentary.


### REC-023 — Current geometry versus Rev B/trailer proposal

Source claim: Photos show raised cart; consolidated reference calls rail pods, four-post/five-truss Rev B and tractor/trailer adopted.

**R1:** Keep raised-cart reconstruction as current historical geometry. Rev B cradle, rail pods, closed ring, removable-module Case 4 and passive trailer remain source-described proposals, not fitted parts.

Sources: Historical photos 1963-1971; S11 sections 5-9; S03 sections 5-7. Disposition: resolved documentary.


### REC-024 — Enclosure dimensions

Source claim: BOM lists 11.5 x 7.5 x 5.1in; R0 CAD used 210 x 130 x 90mm placeholder.

**R1:** Record source candidate as 292.1 x 190.5 x 129.54mm, not measured. Use it only as an explicitly source-listed layout envelope; actual box identity/fit remains unknown.

Sources: S04 V1.0!C16; R0 dimensions.json. Disposition: resolved documentary.


### REC-025 — Stock dimensions versus as built

Source claim: Stock width/wheelbase and poster totals are mixed with CAD values.

**R1:** Keep stock product specs, source candidates, illustrative layout and measured dimensions in separate fields. Overall width is not automatically tyre-centre track spacing.

Sources: S10 t8r9; S12-S14; R0 dimensions.json. Disposition: resolved documentary.


### REC-026 — Rollover counts and confidence

Source claim: Review calls clips 2/4/5/7 four independent failures and assigns 90-92% confidence.

**R1:** Source itself describes clip 5 as same route/analysis and clip 7 as repeated event. Do not count four independent experiments or treat subjective confidence as measured probability. Preserve source claims and require unique original evidence IDs.

Sources: S02 t3r3,t3r5,t3r6,t3r8,t5; S05 Evidence Log. Disposition: resolved documentary.


### REC-027 — Historical versus current operating approval

Source claim: Review and data workbook mark pavement Approved with unnamed approval evidence.

**R1:** Demonstrated travel is not a released operating envelope. Keep historical observations but no current approval, load limit or reviewer sign-off is inferred.

Sources: S02 t18; S05 Operating Envelope!N5:Q14. Disposition: resolved documentary.


### REC-028 — Simulated stakeholder consensus

Source claim: Integrated spec reports a simulated panel and unanimous decisions.

**R1:** Simulation is design reasoning, not approval by actual reviewers. Requirements remain candidate requirements until owner/review adoption is recorded.

Sources: S03 section 3; S03 t38. Disposition: resolved documentary.


### REC-029 — Requirement ID collisions

Source claim: SYS-001 etc mean different requirements across integrated and offline references.

**R1:** Preserve legacy IDs with source namespaces IPDS0: and OFFLINE1:. Do not join or score solely on the bare ID.

Sources: S03 t16; S10 t21; S05 Requirements. Disposition: resolved documentary.


### REC-030 — Blank scorecard produces Kill

Source claim: Blank measured scores calculate 0%, triggering Kill/Repurpose; safety says Pending/Pass.

**R1:** Guard missing/invalid scores and evidence. Default becomes Pending evidence, not a failure or pass. Distinguish critical failures from noncritical category failure.

Sources: S01 V1_to_V2_Scorecard!E2:E9,G9; S01 Dashboard!A5:E5. Disposition: resolved documentary.


### REC-031 — Scorecards mix legacy and current configs

Source claim: Historical source assessments drive dashboard as current data.

**R1:** Filter dashboard and requirement summaries to CFG-V2-R1. Preserve historical rows and source-reported outcomes separately; no current physical pass rate exists without measured results.

Sources: S05 Dashboard; S05 Requirement Assessments. Disposition: resolved documentary.


### REC-032 — Threshold conflicts

Source claim: 95% versus99.5% logging, 10/20/50-100Hz, 65/85/90C, 2/5/10min setup.

**R1:** Retain source-scoped candidate thresholds; no arbitrary global threshold is declared approved. Current draft firmware is 100ms/10Hz coupled acquisition, not a 50-100Hz validated stream.

Sources: S01 Gate_Criteria; S03 requirements; S06 p81,p182,p186; R0 config.h. Disposition: resolved documentary.


### REC-033 — Serial formats

Source claim: Research proposes CSV D/heartbeat lines; old repo JSON synthetic; R0 introduces strict JSON v2.

**R1:** Use documented proposed JSON protocol v2 for the new code only. Preserve existing raw firmware output first; no claim that original code uses it. Legacy CSV requires an explicit adapter, not silent parser fallback.

Sources: S06 p80,p156; R0 serial_protocol.md. Disposition: resolved documentary.


### REC-034 — Software test counts

Source claim: Consolidated reference claims 113 CV tests; R0 has32 acquisition tests.

**R1:** These refer to separate codebases. 32 local draft acquisition tests are checked; 113 CV tests are source-reported/unverified here and do not prove deployed perception.

Sources: S11 p55,p115; R0 test receipts. Disposition: resolved documentary.


### REC-035 — Historical field outcome

Source claim: Research reports two-mile trip, ~10lb collected, lost sensor, unusable mount, no usable field data.

**R1:** Retain as report-attributed observations, not a verified new field dataset. Their dates/configuration and original ten videos must be linked before closing physical records.

Sources: S06 p3-p11,p244-p249. Disposition: unresolved evidence.
Physical follow-up: Obtain original run manifest/media or owner confirmation.

### REC-036 — Quoted costs and evidence dates

Source claim: Research contains current verified prices; source reviews say May2026 without original run records.

**R1:** Treat prices as historical quotes/allowances, not new prices or purchase evidence. Source dates are document assertions, not verified test dates.

Sources: S06 t3,p88; S02 t1r2; S05 Review Register!D5. Disposition: resolved documentary.


### REC-037 — Unverified deployment and service

Source claim: Existing diagrams/firmware could imply installed working logger and hardware protection.

**R1:** New sources are engineering drafts. Compile/replay/native validity checks are distinct from deployment, bench results, field reliability or physical protection.

Sources: R0 validation; S06 missing data. Disposition: resolved documentary.


### REC-038 — PDF and derivative control

Source claim: Old R0 PDF exports would disagree after native edits.

**R1:** Freeze PDF bytes for this pass. Mark them stale for R1 and link current editable/SVG/STEP sources. Regeneration occurs only after owner review.

Sources: Owner request current turn. Disposition: resolved documentary.


## Verification boundary

Claims in S06 are report-attributed; this pass did not re-inspect its ten original videos. Source-derived documents and repeated clip analysis are not independent corroboration. Missing measurements, source listings, synthetic tests and simulated approvals never become current physical verification.

Annotated source copies retain historical technical wording for editing and traceability; their R1 amendment supersedes conflicting claims. They do not compete with the unified current record or grant physical approval. Word PDF/pagination proofing is intentionally deferred with PDF generation at the owner’s request.
