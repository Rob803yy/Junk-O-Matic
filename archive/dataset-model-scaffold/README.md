# Dataset/model scaffold archive / examples only

This is the older, independent dataset/model workspace, not the current V2
acquisition system. The seven-label taxonomy, configured dataset roots and
nonzero placeholder model metrics do not establish trained/deployed perception.
Current engineering: [V2 index](../../docs/v2/README.md).

Contents retain their relative structure: `app/`, `configs/`, `src/`,
`reports/dataset_inventory.json`, `reports/model_runs/sample_run.json`,
`scripts/download`, `scripts/convert` and scanner behavior tests.
Original code/config/fixture bytes are preserved from the prepared REPO-R1 snapshot.
The scanner's REPO-R1 correction reports filename counts only; no annotation parser,
observed taxonomy mapping or dataset/model training is implemented.

Optional historical dashboard, from the repository root in its own environment:

```sh
cd archive/dataset-model-scaffold
python -m pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

To inspect local scan behavior from this archive directory:

```sh
python scripts/convert/build_inventory.py --output reports/local/dataset_inventory.json
python -m unittest discover -s scripts/repository_review/tests -v
```

Run from this archive directory so the preserved relative paths resolve. New
local inventories, raw datasets and virtual environments remain ignored. The
repository root requirements now select the small V2 logger dependency list;
archived Streamlit/legacy dependencies are not installed by that default.
No dashboard browser or live dataset download was exercised during cleanup.
