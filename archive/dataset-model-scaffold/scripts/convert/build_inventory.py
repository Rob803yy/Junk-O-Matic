"""Count configured local image filenames; annotation/class observations stay unknown.

Preserves the committed bootstrap inventory by default. No dataset download,
annotation parsing, media-integrity check, training or hardware access occurs.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def build_inventory(datasets_cfg: dict, class_cfg: dict, base: Path) -> dict:
    if not isinstance(datasets_cfg, dict) or not isinstance(datasets_cfg.get("datasets"), list):
        raise ValueError("datasets config requires a datasets list")
    if not isinstance(class_cfg, dict) or not isinstance(class_cfg.get("classes"), list):
        raise ValueError("class config requires a classes list")
    classes = class_cfg["classes"]
    if any(not isinstance(c, str) or not c.strip() for c in classes):
        raise ValueError("configured classes must be nonempty strings")
    rows = []
    total = scanned = missing = disabled = 0
    for ds in datasets_cfg["datasets"]:
        if not isinstance(ds, dict) or not all(isinstance(ds.get(k), str) and ds[k].strip() for k in ("name", "local_root")):
            raise ValueError("each dataset requires name and local_root strings")
        enabled = ds.get("enabled", True)
        if type(enabled) is not bool:
            raise ValueError("enabled must be a YAML boolean")
        root = base / ds["local_root"]
        images = None
        if not enabled:
            state = "disabled"
            disabled += 1
        elif not root.exists():
            state = "missing_root"
            missing += 1
        elif not root.is_dir():
            raise ValueError(f"dataset root is not a directory: {ds['name']}")
        else:
            # A filename/suffix count is not a decoded-image or annotation validation.
            images = sum(1 for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
            state = "scanned"
            total += images
            scanned += 1
        rows.append({"name": ds["name"], "enabled": enabled, "local_root": ds["local_root"],
                     "scan_state": state, "images": images, "annotations": None, "classes_seen": None})
    return {"schema_version": 2, "generated_at": datetime.now(timezone.utc).isoformat(),
            "evidence_type": "local_filename_scan_not_annotation_or_model_validation",
            "configured_classes": classes, "datasets": rows,
            "totals": {"images": total, "annotations": None, "scope": "scanned_enabled_roots_only",
                       "scanned_roots": scanned, "missing_roots": missing, "disabled_roots": disabled},
            "limits": ["Images counts filenames by extension, not decoded valid images.",
                       "Annotations and observed classes are unknown; no parser or taxonomy mapping exists.",
                       "Missing/disabled roots are not verified empty datasets."]}


def write_inventory(output: Path, payload: dict, overwrite: bool = False) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create avoids accidental replacement, including a concurrent writer.
    with output.open("w" if overwrite else "x", encoding="utf-8") as f:
        f.write(json.dumps(payload, indent=2, allow_nan=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datasets", type=Path, default=Path("configs/datasets.yaml"))
    parser.add_argument("--classes", type=Path, default=Path("configs/classes.yaml"))
    parser.add_argument("--output", type=Path, default=Path("reports/local/dataset_inventory.json"))
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace an existing output.")
    args = parser.parse_args()
    datasets_cfg = yaml.safe_load(args.datasets.read_text(encoding="utf-8"))
    class_cfg = yaml.safe_load(args.classes.read_text(encoding="utf-8"))
    payload = build_inventory(datasets_cfg, class_cfg, Path.cwd())
    write_inventory(args.output, payload, args.overwrite)
    print(f"Wrote local inventory: {args.output} (filename scan only)")


if __name__ == "__main__":
    main()
