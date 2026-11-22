> Historical REPO-R1 preparation record. The subsequent [layout cleanup](../repository-layout.md) publishes these corrections together with the active/archive separation. Old paths below retain their dated meaning; use the [relocation map](../../archive/relocation-manifest.json).

# Repository alignment review / REPO-R1

Prepared 2026-11-22 against merged `main` commit
`adb9280f30513fd852968d12e9bc6479bd2e188d` (PR #3 merged). The review identifies
baseline gaps, orders them by severity, applies Six Thinking Hats, and records
bounded corrections. The local branch/package is prepared for the next GitHub
posting step; this review does not itself change remote settings or publish a PR.

## Coverage and age

193 baseline tracked files were inventoried, excluding LICENSE/license.md content.
36 older March/May files were read as text/code/examples (including the empty
placeholder): 10 last changed March 6, 2026 (261 days), and 26 last changed May 2,
2026 (204 days). These correspond to the screenshot's approximate older groups.
The remaining 157 files were inventoried and selected current references compared.
No new full native CAD, electrical, Office or PDF technical review is claimed.
Per-file scope and exclusions are explicit in [baseline inventory](baseline-inventory.json)
and [folder table](folder-review.csv). Last content commit is **not** last review.

The current comparison basis is CFG-V2-R1 / ARCH-R2 / CAD-R3. Owner-confirmed Uno
identity and frame/hinge relationships are retained; unmeasured dimensions,
untraced electrical paths, Pi/range identity and deployed software remain open.
The review does not infer a physical fault solely from age or an unresolved TODO.

## Findings in severity order

20 findings: **6 high, 11 medium, 3 low**. No critical/immediate severe condition
was established by this document/source review. High severity means a path can
mislead configuration, acquisition or evidence acceptance; it is not a claim that
hardware damage occurred. Definitions, baseline line citations, all six hats,
changed files and residual actions are in [the gap register](gap-register.json).

| Priority | Severity | Finding | Disposition / residual |
| ---: | --- | --- | --- |
| 1 / REV-001 | HIGH | Old wiring and component descriptions compete with current V2 | document corrected physical open; Owner physical trace still needed for polarity, returns, protection, USB coexistence and sensor supply. |
| 2 / REV-002 | HIGH | Historical Arduino constants can resemble physical readings | contained legacy not qualified; Original running sketch and real sensor/calibration evidence remain unrecovered. |
| 3 / REV-003 | HIGH | Legacy logger silently miscounts V2 records | contained legacy not qualified; If the legacy logger is ever revived, add strict validation, raw preservation and fault/session tests before relying on it. |
| 4 / REV-004 | HIGH | Validation percentages and examples can imply passed gates | document corrected evidence open; Physical tests, agreed thresholds and supporting run evidence remain open. |
| 5 / REV-005 | HIGH | Dashboard renders placeholder model metrics as ordinary results | corrected labeling only; Real training/evaluation dataset hashes, split, procedure and run provenance are still absent. |
| 6 / REV-019 | HIGH | Physical V2 evidence gaps remain open after document reconciliation | open physical evidence; Owner measurements/labels/continuity, original software capture and controlled bench/field evidence are required to close these items. |
| 7 / REV-006 | MEDIUM | Inventory generator calls configured classes observed and unchecked annotations zero | corrected tool semantics; Annotation parsing, taxonomy mapping and source dataset acquisition remain future work. |
| 8 / REV-007 | MEDIUM | Historical logger failure limits are not documented | contained legacy not qualified; Legacy runtime hardening is deferred unless that code path is selected again. |
| 9 / REV-008 | MEDIUM | Hardware parent folders still describe placeholders only | corrected; None for this document correction. |
| 10 / REV-009 | MEDIUM | Issue templates hardcode V1A and incompatible evidence files | corrected; None for this document correction. |
| 11 / REV-010 | MEDIUM | Run schemas, serial fields and scorecard import are not cross-mapped | corrected; None for this document correction. |
| 12 / REV-011 | MEDIUM | Root dependency/setup instructions mix separate tools | document corrected environment open; A portable locked dependency environment and actual Pi/OS compatibility remain unverified. |
| 13 / REV-012 | MEDIUM | Dataset bootstrap and taxonomy are scaffold, not perception capability | corrected; None for this document correction. |
| 14 / REV-013 | MEDIUM | Validation overview mixes historical and current revision claims | corrected; None for this document correction. |
| 15 / REV-014 | MEDIUM | Regeneration commands can replace reviewed sources; PDF book is frozen R0 | document corrected export open; A future PDF workflow must regenerate/proof all current subsystem derivatives and update the hold manifest after owner content review. |
| 16 / REV-015 | MEDIUM | No cross-folder review record distinguishes last commit from actual review | corrected; None for this document correction. |
| 17 / REV-020 | MEDIUM | GitHub sidebar capability wording exceeds the reconstruction evidence | prepared remote setting pending; Apply prepared About text in repository settings when publishing the reviewed package. |
| 18 / REV-016 | LOW | Duplicate loaders and src package have no integration contract | document corrected implementation deferred; Package consolidation and robust run ingestion remain optional future implementation work. |
| 19 / REV-017 | LOW | Root page is dominated by historical setup and stage claims | corrected; None for this document correction. |
| 20 / REV-018 | LOW | No automated review freshness/link workflow exists | manual check implemented ci deferred; Optional future CI integration, with its own environment/tool choices, is not installed. |

## Concrete corrections

- Current source entry points replace competing Nano/Pi4/grounding/12V assumptions;
  historical text is retained with clear scope and baseline-rebased links.
- The legacy constant-emitting sketch and permissive logger remain unchanged and
  explicitly unqualified for new V2 work. An offline fake-port reproduction shows
  a valid V2 frame becoming a counted legacy row with every measurement blank.
- Current versus legacy serial/config/output/scorecard contracts are mapped.
  Example CSVs, historical gates and placeholder model metrics are clearly labeled.
- Hardware parents, docs, setup matrix, issue templates and archive conventions
  route to current sources while keeping unknowns and proposed thresholds visible.
- Two bounded tool changes accompany the docs: dashboard provenance notices and
  truthful local inventory scanning. The scanner separates missing/empty/disabled
  roots, does not invent annotations/observed classes, and refuses default overwrite.
- The current validation index distinguishes original R1 software checks, CAD-R3,
  ARCH-R2 and this repository review without retimestamping original receipts.
- A prioritized [V2 evidence plan](../v2/verification-plan.md) and prepared
  [GitHub About text](github-about.txt) support the next review/posting step.

## Six Thinking Hats decisions

[Decision summary](six-hats-decisions.md) describes the choices by problem family;
the register applies all six hats to each of the 20 prioritized findings. These
are analytical lenses, not votes, simulated experts or stakeholder approval.
Red-hat concerns are anticipated reader reactions, not claims about the owner's
feelings. The selected approach keeps useful history and corrects its current use.

## Checks and remaining work

[Validation receipt](../../reports/repository_review/validation.json) records
links, structured records, original-source/PDF preservation, Python syntax and
inventory behavior tests. [Parser reproduction](../../reports/repository_review/legacy-parser-reproduction.json)
used an in-memory fake port and no physical serial connection. The dashboard
notices were source-checked; a browser/Streamlit integration run is not claimed.
Original 32-test/compile/replay receipts remain historical and unchanged; this
document pass does not claim to rerun the physical or full native engineering suite.

All native engineering source/exports, four legacy sample CSVs, original legacy
firmware/logger, model/inventory fixture JSON and 13 PDFs are preserved. No PDF,
Word or workbook generation was performed. The only historical executable changes
are the inventory scanner and dashboard labels, listed in the review diff.

Document corrections and containment are not closure of hardware or legacy
runtime issues. Physical labels/trace/measurements, original sketch/output capture,
actual Pi deployment, calibration, controlled tests and adopted acceptance rules
still require evidence. A dependency lock, ingestion/model evaluation pipeline,
optional helper consolidation and CI integration also remain unimplemented.
The prepared GitHub About text is not yet applied remotely.

For compact feedback: `REV-ID / file or box / corrected fact / evidence`.
After content review, post this prepared source patch/package to a new GitHub
review branch. PDFs remain held until the separate corrected-content export step.
