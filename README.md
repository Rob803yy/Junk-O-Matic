# Junk-O-Matic
Design, develop, and deploy autonomous robots capable of collecting and sorting waste in various public settings, particularly in public areas, creating cleaner and more sustainable communities.

Local-first workspace for waste dataset aggregation, taxonomy normalization, and early model evaluation.

## Quickstart

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

python scripts/download/bootstrap_datasets.py
python scripts/convert/build_inventory.py
streamlit run app/streamlit_app.py
```

## Project Layout

```text
app/
configs/
data/
reports/
scripts/
src/
```

## Status

This scaffold includes:
- Taxonomy and dataset config files
- Streamlit dashboard for run metrics and dataset inventory
- Stub dataset bootstrap script
- Inventory builder script
- Sample run artifact for immediate UI validation
