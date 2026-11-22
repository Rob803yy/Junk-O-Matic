from pathlib import Path
import json

import pandas as pd
import streamlit as st
import yaml


def load_yaml(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_runs(path: str = "reports/model_runs"):
    base = Path(path)
    runs = []
    if base.exists():
        for file in sorted(base.glob("*.json")):
            try:
                runs.append(load_json(str(file)))
            except json.JSONDecodeError:
                continue
    return runs


st.set_page_config(page_title="Junk-O-Matic Review", layout="wide")
st.title("Junk-O-Matic: Dataset + Model Review")
st.warning(
    "Historical dataset/model workspace. The committed inventory and sample run "
    "are bootstrap examples, not verified training, evaluation or vehicle evidence. "
    "Imported run metrics also require model, dataset, split and method provenance."
)
st.caption("Current V2 engineering review: docs/v2/README.md. This page does not control the buggy.")

classes_cfg = load_yaml("configs/classes.yaml")
datasets_cfg = load_yaml("configs/datasets.yaml")
inventory = load_json("reports/dataset_inventory.json")
runs = load_runs("reports/model_runs")

left, right = st.columns(2)

with left:
    st.subheader("Taxonomy")
    st.dataframe(pd.DataFrame({"class": classes_cfg.get("classes", [])}), use_container_width=True)

with right:
    st.subheader("Configured Datasets")
    st.dataframe(pd.DataFrame(datasets_cfg.get("datasets", [])), use_container_width=True)

st.divider()
st.subheader("Model Runs")

if not runs:
    st.info("No model run JSON files found in reports/model_runs/.")
else:
    run_ids = [r.get("run_id", f"run_{i}") for i, r in enumerate(runs)]
    selected = st.selectbox("Select run", options=run_ids, index=0)
    selected_run = runs[run_ids.index(selected)]
    st.info(
        "Evidence status is unverified in this viewer. sample_run_0001 is a placeholder; "
        "its metrics and confusion matrix must not be cited as measured performance."
    )

    summary = selected_run.get("summary", {})
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("mAP50", summary.get("mAP50", "n/a"))
    s2.metric("Precision", summary.get("precision", "n/a"))
    s3.metric("Recall", summary.get("recall", "n/a"))
    s4.metric("F1", summary.get("f1", "n/a"))

    st.markdown("Per-class metrics")
    per_class = selected_run.get("per_class", [])
    st.dataframe(pd.DataFrame(per_class), use_container_width=True)

    cm = selected_run.get("confusion_matrix", {})
    labels = cm.get("labels", [])
    matrix = cm.get("matrix", [])
    if labels and matrix:
        st.markdown("Confusion matrix")
        cm_df = pd.DataFrame(matrix, index=labels, columns=labels)
        st.dataframe(cm_df, use_container_width=True)

st.divider()
st.subheader("Dataset Inventory JSON")
st.json(inventory)
