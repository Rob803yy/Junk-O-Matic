"""Build a simple dataset inventory JSON from configured dataset roots."""

from datetime import datetime, timezone
from pathlib import Path
import json
import yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def count_images(root: Path) -> int:
    if not root.exists():
        return 0
    return sum(1 for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)


def main() -> None:
    datasets_cfg = yaml.safe_load(Path("configs/datasets.yaml").read_text(encoding="utf-8"))
    class_cfg = yaml.safe_load(Path("configs/classes.yaml").read_text(encoding="utf-8"))

    rows = []
    total_images = 0
    for ds in datasets_cfg.get("datasets", []):
        root = Path(ds["local_root"])
        images = count_images(root)
        total_images += images
        rows.append(
            {
                "name": ds["name"],
                "images": images,
                "annotations": 0,
                "classes_seen": class_cfg.get("classes", []),
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "taxonomy_version": "v0",
        "datasets": rows,
        "totals": {"images": total_images, "annotations": 0},
    }

    out = Path("reports/dataset_inventory.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote inventory: {out}")


if __name__ == "__main__":
    main()
