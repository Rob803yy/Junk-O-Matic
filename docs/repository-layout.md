# Repository layout / active V2 versus archive

LAYOUT-R1, 2026-11-22. The active engineering basis remains CFG-V2-R1 with
ARCH-R2 and CAD-R3. Cleanup changes file placement/navigation, not the physical
configuration or the deployed program.

```text
README.md                  Current entry and evidence boundary
requirements.txt           V2 logger dependency entry only
docs/v2/                   Current source index, protocol, BOM, evidence plan
docs/reconciliation/       Current source decisions and editable corrections
docs/v2_verification/      Original evidence claims / still applicable unknowns
docs/repository_review/    Dated review, findings and Six Thinking Hats decisions
hardware/v2/               Current native architecture / QET / WireViz / CAD
software/v2/               Current Uno/Pi draft, SQL, labeled fixtures and tests
scripts/v2/                Current drafting and scoped check tools
reports/v2/                Revision-specific engineering receipts
reports/repository_review/ Review and cleanup check receipts
validation/                Current evidence / scorecard guidance
test_data/                 Local evidence convention; raw data excluded
archive/v1a/               Old firmware/logger/procedures/sample CSVs/placeholders
archive/dataset-model-scaffold/ Independent older dashboard/datasets/examples
archive/reference-pages/   Former page snapshots
archive/exports-r0/        Thirteen stale PDFs, original bytes preserved
```

The [relocation manifest](../archive/relocation-manifest.json) maps all 50 moves,
records source hashes and distinguishes unchanged bytes from navigation-only
Markdown edits. Old baseline inventories, citation paths and receipts remain
historical: resolve them through the manifest, not by rewriting their dates/results.
New cleanup validation is recorded separately in
[the layout receipt](../reports/repository_review/layout-r1-validation.json).

Current V2 native source, STEP, SVG/PNG, firmware/logger/SQL and protocol paths stay
stable. Labeled V2 synthetic protocol fixtures stay with their tests. Historical
input annotations in reconciliation remain explicitly labeled because they support
the current review; current editable Office corrections are not archived.

All 13 old PDFs moved out of the active source folders without byte changes.
The export hold register follows their new locations; a move does not regenerate
them or make them current. No license content was reviewed or moved.

Use [the environment matrix](environment-setup.md) for current defaults. Archived
dashboard setup starts inside its archive directory. Root dependency installation
selects only the active V2 logger; no archived tool is a startup/default code path.
No hardware upload, Pi service install or physical validation was performed.
