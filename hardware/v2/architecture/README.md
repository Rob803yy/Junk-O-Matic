# Three architecture diagrams / ARCH-R2

ARCH-R2 (2026-11-22) refines the three diagrams for **CFG-V2-R1**, using the
reconciliation decisions, CAD-R3 owner/photo record and actual draft source code.
It is a document revision, not a new vehicle version or verification of a deployed
system. All three native `.drawio` files contain editable shapes, text rows,
connectors and evidence properties. Matching SVG/PNG previews are current.

| Document | Editable source | Review preview | Changes to review |
| --- | --- | --- | --- |
| 01 System overview | [drawio](v2_system_overview.drawio) | [SVG](v2_system_overview.svg) / [PNG](v2_system_overview.png) | Mechanical support separated from proposed power/data flow; fixed frame, below/above member ordering, rear hinge and driving front carried from CAD-R3. |
| 02 Power domains | [drawio](v2_power_domains.drawio) | [SVG](v2_power_domains.svg) / [PNG](v2_power_domains.png) | RC propulsion and auxiliary sources separated; U5A output open, U12 proposed, Pi/Uno power entries and USB coexistence unresolved. |
| 03 Data flow | [drawio](v2_data_flow.drawio) | [SVG](v2_data_flow.svg) / [PNG](v2_data_flow.png) | Actual draft producer, raw-first capture, framing, strict validation, valid/error storage, exports, sessions, health and provenance. |

## Read the status and its scope together

- **Confirmed / green:** only the stated claim is confirmed. In 01 this covers
  owner-confirmed identity/relationships. In 03 it means **source-code behavior
  only**, not fitted sensors, deployment, throughput or physical data.
- **Conflicting / red:** the source claims or historical availability disagree;
  the current state remains open. Pi 3B/Pi 4 and range-sensor availability persist.
- **Proposed / purple:** design intent or a candidate interface, not traced wiring.
- **Unknown / amber:** insufficient evidence for the current physical detail.

Solid green links in 01 are mechanical relationships; in 03 they are code flows.
Every electrical path in 01/02 is dashed and unverified. Power arrows allocate
functions; both supply and return, polarity, connectors and ratings remain to be
traced. There is no asserted common ground **or** proven galvanic isolation.
F1/S1/FB1 is a functional grouping, not a selected series order or fuse hierarchy.
U5/U5A ratings are source claims, not measured continuous capability. U5A has no
assigned output load or parallel/backup function. U12-to-lights is a proposal;
the fitted light voltage is unknown. Uno identity does not establish its supply.

The bucket omission is an owner display preference. Exact mounting dimensions,
hinge coordinates/orientation, latch, moving membership of minor brackets, travel
and physical clearances remain open in [CAD-R3](../mechanical/README.md). No load,
runtime, speed, weather rating or autonomy claim is validated by these diagrams.

The new code uses JSON protocol 2; it does not recover the old sketch or its serial
format. A valid default frame has `flags=5` and null measurements: **zero physical
samples**. A02YYUW UART is unselected and has no driver in this draft. Raw MPU
registers do not provide calibrated attitude or absolute heading. Host receive
timestamps do not establish synchronized sensor/video capture. Application code
sends no motion commands; USB opening can still reset the Uno through DTR.

## Evidence and editing

[architecture-model.json](architecture-model.json) holds text, four-state status,
claim scope, evidence IDs, layout, ports and waypoints. Its evidence map links to
the [38 reconciliation decisions](../../../docs/reconciliation/reconciliation-register.json),
[owner/photo observations](../mechanical/photo-observations.json),
[BOM](../../../docs/v2/bom.json), [protocol](../../../docs/v2/serial_protocol.md)
and exact software source paths. Raw private photographs stay outside Git.
In diagrams.net use **Edit Data** on a component to inspect its status, scope and
evidence IDs. Child text moves with its component; connectors attach to its ports.
Avoid resizing a component without reviewing the text and route layout.

Edit in diagrams.net for review. To retain manual changes, save a separate review
copy or apply them to the JSON before regeneration: the generator replaces the
three native files and their previews. With Pillow installed, run from repo root:

```powershell
python scripts/v2/architecture_diagrams.py
python scripts/v2/architecture_diagrams.py --check
```

`draft_drawings.py` now calls the same three-diagram renderer. It cannot generate
PDFs or overwrite digital connectivity. Arial was used for these exports; the
fallback DejaVu Sans can require a new layout review. The JSON, native cells and
SVG preserve real editable text rather than a screenshot.

## Checks and next feedback

[Validation receipt](../../../reports/v2/architecture-r2-validation.json) records
native XML readback, evidence references/input hashes, text fit, node boundaries,
orthogonal routes, endpoints/waypoints, code-contract invariants and all 13 held
PDF hashes. All three shared-scene previews were visually reviewed. This checks
document consistency; it does not substitute for physical trace or deployment.
Native diagrams.net application rendering was not exercised in this pass.

For compact feedback, identify a box or link and the corrected claim, for example
`02 / PWR-U5A — actual output goes to ... — photo or meter evidence ...`.
Next decisions: identify Pi/range hardware, trace both power conductors and USB
power, capture the original serial format, and measure the mounting interfaces.

The fourth [digital connectivity diagram](v2_digital_connectivity.drawio) remains
the **R1 logical-pin review**, unchanged in this three-document pass. Its blue
historical markings use the older legend; they do not confirm current fitting.
Current physical trace is still required. Its R1 authoring history is retained in
Git; the native source remains directly editable.

**PDFs remain held.** All existing R0 PDFs are stale and unchanged; use the current
native/SVG/PNG files for this review. Generate new PDFs after owner content review.
