# Hardware documentation / current V2 and historical placeholders

Use [hardware/v2](v2/) for the current engineering drafts and
[the engineering index](../docs/v2/README.md) for review order.

| Source | Current material |
| --- | --- |
| [Architecture](v2/architecture/README.md) | ARCH-R2 system/power/data diagrams; R1 digital connectivity |
| [Electrical](v2/electrical/README.md) | Three-sheet QElectroTech draft; all nets untraced |
| [Wiring](v2/wiring/README.md) | Two WireViz harnesses, functional registers and diagram BOMs |
| [Mechanical](v2/mechanical/README.md) | CAD-R3 native files, STEP and previews; numeric dimensions unmeasured |
| [Master BOM](../docs/v2/bom.json) | Normalized evidence/status/quantity record; editable workbook in reconciliation |

The older `bom`, `wiring_diagrams` and `enclosure_layout` folders are retained
entry points, not competing build definitions. Uno R3 is owner-confirmed; Pi model,
sensor fitting, installed wiring and operating ratings remain open. No physical
control isolation, payload or assembled ingress rating is established. PDFs remain
held; use current native/SVG/PNG/STEP sources.
