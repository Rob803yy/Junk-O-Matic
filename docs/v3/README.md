# Assisted V3 planning information

V3-PLAN-R0, 2026-11-22. The owner selected **camera detection, operator alerts and
reliable logging, with manual RC controlling motion**. That mission scope is
confirmed. Detailed designs, component choices, numerical acceptance targets and
deployment remain proposed/unverified. The design ID CFG-V3-ASSISTED-R0 is reserved
for this proposal; it does not label a currently deployed configuration.

V2 remains the working engineering/runtime baseline. This planning set does not
rename V2 files, copy old passing results into V3 or create empty native/STEP/code
files that could look finished. The old V3 poster's autonomy, Nano, intake, dual-bin,
backup-power and performance claims are not adopted by this narrower scope.

| Review material | What it answers |
| --- | --- |
| [Carry-forward/change summary](change-summary.md) | What stays, changes or is new across the original deliverable set |
| [Editable review workbook](editable/LitterBuggy_V3_Change_Register.xlsx) | Deliverables, every baseline file, all component dispositions and requirement inputs |
| [Complete file impact JSON](file-impact-register.json) / [CSV](file-impact-register.csv) | One disposition per baseline tracked file; proposed target paths are plans, not existing files |
| [BOM plan JSON](bom-plan.json) / [CSV](bom-plan.csv) | All 55 current and 23 future baseline items plus a camera-mount candidate; quantities remain source/fitted/proposed separately |
| [Requirements](requirements.json) / [validation plan](validation-plan.md) | Tests/evidence and unresolved numeric acceptance limits; no passed V3 physical results |
| [Interfaces/data proposal](interfaces-and-data.md) | Serial compatibility, vision/frame/alert/run contracts and transfer |
| [Decisions and build sequence](decisions-and-sequence.md) | Choice dependencies and requested engineering review order |
| [Scope record](scope.json) / [deliverable plan](deliverable-plan.json) | Owner mission decision, preserved facts and proposed future artifact names |

The workbook is an editable review view generated from the JSON records. Reconcile
workbook review edits back to the owning JSON before regenerating. It is not a new
approved purchasing BOM, completed scorecard or automatic synchronization service.

Basis: merged main 902b8baeac3b8d834a162f9c4661b4664d3f53da,
[V2 index](../v2/README.md), [BOM](../v2/bom.json),
[CAD owner/photo record](../../hardware/v2/mechanical/photo-observations.json),
[serial protocol](../v2/serial_protocol.md), and the owner's current V3 scope answer.
Raw/private media remains outside Git. No native hardware export, firmware upload,
model training, physical test or PDF generation occurs in this planning pass.

Planning consistency and preservation checks: run `python scripts/v3/check_plan.py`
from the repository root. The [planning receipt](../../reports/v3/planning-validation.json)
covers record coverage, references, quantity/status inheritance and saved workbook
data. It is separate from the open physical/runtime acceptance requirements.
The checker is the only new V3 script in this planning pass; the listed future
runtime tests and engineering generators are not implemented.
