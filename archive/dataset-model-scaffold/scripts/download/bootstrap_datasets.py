"""Dataset bootstrap script.

This file is intentionally a stub for now. It validates config and creates
expected local directories for later real download/parsing steps.
"""

from pathlib import Path
import yaml


def main() -> None:
    cfg_path = Path("configs/datasets.yaml")
    if not cfg_path.exists():
        raise FileNotFoundError(f"Missing config: {cfg_path}")

    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    datasets = data.get("datasets", [])

    for ds in datasets:
        if not ds.get("enabled", True):
            continue
        root = Path(ds["local_root"])
        root.mkdir(parents=True, exist_ok=True)
        print(f"Prepared dataset directory: {root}")

    print("Bootstrap stub complete. Add real downloader logic next.")


if __name__ == "__main__":
    main()
