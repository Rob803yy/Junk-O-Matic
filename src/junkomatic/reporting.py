from pathlib import Path
import json


def load_model_runs(model_runs_dir: str = "reports/model_runs"):
    base = Path(model_runs_dir)
    if not base.exists():
        return []

    runs = []
    for p in sorted(base.glob("*.json")):
        try:
            runs.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return runs
