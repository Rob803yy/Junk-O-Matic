# Reports / distinguish examples from check receipts

| Location | Status / allowed interpretation |
| --- | --- |
| `dataset_inventory.json` | Preserved March bootstrap fixture; zero images do not establish present local content. Its configured `classes_seen` and unchecked zero annotations are not observation evidence. |
| `model_runs/sample_run.json` | Preserved `baseline-placeholder` example. Nonzero mAP/precision/recall/F1 and matrix are not measured evaluation. |
| `v2/` | Revision-specific software/native/architecture/CAD receipts; check exact revision, method and limits. Not physical field approval. |
| `repository_review/` | REPO-R1 parser reproduction and local document/tool checks; no physical device contact. |
| `local/` | Ignored current local scans; not an automatically published result or deployed capability. |

The app displays the two older report examples with provenance warnings. Original
fixture bytes and original engineering check receipts remain unchanged. New real
model results need model/source/config IDs, dataset/split provenance, evaluation
method and reproducible raw evidence before use as engineering claims.

Do not refresh dates/counts in old receipts merely to make them look current.
Compile/replay/file validity is separate from timing, sensor accuracy, moving
clearance, payload, power stability, reset behavior or Pi deployment. See
[scoped validation](../docs/v2/validation.md) and
[the repository review](../docs/repository_review/README.md). Existing PDFs are
held and stale; no PDF was generated in this pass.
