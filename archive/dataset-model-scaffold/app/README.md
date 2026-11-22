# Historical dataset/model dashboard

This Streamlit page reviews configured dataset/taxonomy scaffolding and model-run
JSON examples. It does not implement vehicle telemetry, train a model, prove AI
litter detection, sort litter or command the buggy.

From `archive/dataset-model-scaffold`, in a separate historical dashboard environment:

```sh
pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

`configs/classes.yaml` has seven project labels. `configs/datasets.yaml` names
candidate roots; enabled flags are configuration, not downloaded content.
`reports/dataset_inventory.json` is the old bootstrap snapshot and
`reports/model_runs/sample_run.json` is a placeholder result. Its nonzero metrics
and confusion matrix are **not measured evaluation or deployed performance**.
The app now displays an explicit provenance warning; original fixture JSON stays
unchanged. Additional imported run JSON also needs dataset/model/method/source
provenance before it may be treated as evidence.

The preserved page loads paths relative to this archive workspace and must be
started from `archive/dataset-model-scaffold`, not the repository root.
Missing input files/schema errors are not comprehensively handled; malformed run
JSON is silently skipped. No automated dashboard/UI integration test or dependency
lock exists. REPO-R1 checks syntax/labels only; it does not claim a running browser
test. See [src limits](../src/README.md), [config semantics](../configs/README.md),
[report disposition](../../../reports/README.md) and [environment matrix](../../../docs/environment-setup.md).
