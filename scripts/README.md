# Script use and regeneration matrix / REPO-R1

Run from repository root. Inputs and outputs have different evidence roles.
Keep manual/native source edits before regenerating: compare in an isolated copy
or checkout and review the diff before replacing reviewed files. Regeneration is
not physical verification, and no tool here establishes an installed configuration.

| Entry | Input / actual behavior | Output / overwrite boundary |
| --- | --- | --- |
| `download/bootstrap_datasets.py` | Configured enabled roots; directory-creation stub only | Creates local directories; no download, labels, splits or training |
| `convert/build_inventory.py` | Revised scanner counts images only; no annotation parser | New `reports/local/dataset_inventory.json`; refuses overwrite unless explicit `--overwrite`; does not replace the committed fixture |
| `v2/architecture_diagrams.py --check` | Scene JSON, evidence refs and protocol defaults | Read-only drawio/SVG comparison and checks; normal invocation regenerates three diagrams/previews/receipt; digital R1 and PDFs excluded |
| `v2/draft_drawings.py` | Compatibility wrapper for the same renderer | Same three-source overwrite boundary |
| `v2/build_power.py` | Embedded QET generator with draft hypotheses | Replaces `hardware/v2/electrical/v2_electrical.qet`; new UUIDs; manual edits/native re-save can be lost; regenerate in a copy |
| `v2/build_wiring.py` | Logical draft harness maps | Replaces both YAML files and registers; subsequent WireViz commands regenerate HTML/SVG/PNG/TSV |
| `hardware/v2/mechanical/build_models.FCMacro` | Native CAD-R3 parameters/source | Regenerates native/STEP/review geometry; may overwrite manual native edits; inspect mechanical guide first |
| `v2/render_mechanical.py` / `cad_preview.py` | Current exported review meshes | Replaces CAD-R3 previews/poses; no PDF; not a full physical interference test |
| `v2/check_freecad.py` | FreeCAD Python, five native/STEP sources | Writes a new scoped native receipt; does not measure the vehicle |
| `v2/run_checks.py` | Requires explicit Arduino CLI + dependencies | Rewrites named test/build/replay receipts with its R1 scope/date; not a review-freshness updater; never upload |
| `v2/build_review_book.py` | Historical R0 book assembly | Default refuses while held. An acknowledgement flag alone still assembles stale R0 PDFs; **not a current export workflow** |
| `repository_review/check_review.py` | Baseline inventory, links, dispositions, preserved sources/PDF hashes | Read-only checks by default; writes a new receipt only with explicit `--write-receipt` |

Example local inventory (the output is ignored):

```sh
python scripts/convert/build_inventory.py --output reports/local/dataset_inventory.json
python -m unittest discover -s scripts/repository_review/tests -v
python scripts/repository_review/check_review.py
```

Missing roots are not treated as verified empty datasets; disabled roots are not
scanned; observed classes/annotation counts stay null. Configured classes are
separate. Source URLs, live downloads, taxonomy mappings and model evaluation are
outside the scanner. The historical committed inventory is intentionally retained.

PDFs remain held under [export status](../docs/reconciliation/export-status.json).
A future export step must regenerate current subsystem PDFs, proof them, revise
the book's revision/content and update the hold/hash record after owner content
review. Do not combine stale R0 PDFs and label the result ARCH-R2/CAD-R3.
Manual checks exist; no GitHub Actions workflow or deployment was installed here.
