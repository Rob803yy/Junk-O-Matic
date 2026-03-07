from pathlib import Path
import json
import yaml


def load_yaml(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))
