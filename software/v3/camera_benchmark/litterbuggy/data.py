"""Video sampling and annotation validation."""
import json
import math
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from statistics import median

BACKGROUND = "__background__"
UNKNOWN = "unknown"


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def sample_video(config_path, output, fps):
    if not math.isfinite(fps) or fps <= 0:
        raise ValueError("Sampling FPS must be positive.")
    config_path = Path(config_path)
    manifest = read_json(config_path)
    validate_splits(manifest)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    for clip in manifest["clips"]:
        source = config_path.parent / clip["video"]
        directory = output / "frames" / clip["id"]
        directory.mkdir(parents=True)
        subprocess.run([
            "ffmpeg", "-nostdin", "-v", "error", "-i", str(source),
            "-an", "-vf", f"fps={fps}:start_time=0:round=up", "-threads", "1",
            "-q:v", "2", "-start_number", "0", str(directory / "%06d.jpg"),
        ], check=True)
        paths = sorted(directory.glob("*.jpg"))
        if not paths:
            raise ValueError(f"No frames decoded for {clip['id']}.")
        clip.update(fps=fps, items=[], frames=[
            {"image": path.relative_to(output).as_posix(), "annotated": False, "boxes": []}
            for path in paths
        ])
    path = output / "dataset.json"
    write_json(path, manifest)
    return path


def validate_splits(manifest):
    labels = manifest["labels"]
    if not labels or any(
        not label or label in (UNKNOWN, BACKGROUND)
        or not isinstance(destination, str) or not destination or destination == BACKGROUND
        for label, destination in labels.items()
    ):
        raise ValueError("Specify visual labels and their sorting destinations.")
    clip_ids = set()
    groups = defaultdict(set)
    for clip in manifest["clips"]:
        clip_id = clip["id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", clip_id) or clip_id in clip_ids:
            raise ValueError(f"Invalid or duplicate clip ID: {clip_id}")
        clip_ids.add(clip_id)
        split = clip["split"]
        if split not in ("train", "val", "test"):
            raise ValueError(f"Invalid split: {split}")
        for key in ("drive", "group", "terrain", "weather", "camera"):
            if not isinstance(clip.get(key), str) or not clip[key].strip():
                raise ValueError(f"{clip_id} requires {key}.")
        for key in ("drive", "group"):
            groups[key, clip[key]].add(split)
        for item in clip.get("items", []):
            if item.get("physical_id"):
                groups["physical item", item["physical_id"]].add(split)
    for (kind, identifier), splits in groups.items():
        if len(splits) > 1:
            raise ValueError(f"{kind} {identifier} crosses splits.")


def load_dataset(path, split):
    manifest = read_json(path)
    validate_splits(manifest)
    clips = [clip for clip in manifest["clips"] if clip["split"] == split]
    if not clips:
        raise ValueError(f"No clips in the {split} split.")
    labels = manifest["labels"]
    for clip in clips:
        validate_clip(clip, labels)
    return labels, clips


def validate_clip(clip, labels):
    frames = clip["frames"]
    if not frames or not math.isfinite(clip["fps"]) or clip["fps"] <= 0:
        raise ValueError(f"{clip['id']} needs frames and positive FPS.")
    items = {}
    for item in clip["items"]:
        item_id = item["id"]
        if not item_id or item_id in items or not item.get("material"):
            raise ValueError(f"{clip['id']} has an invalid item ID or material.")
        items[item_id] = item
        if item["label"] not in labels or item["bin"] not in {*labels.values(), UNKNOWN}:
            raise ValueError(f"Invalid label or bin for {item_id}.")
        first = item["first_recognizable"]
        deadline = item["last_decision_frame"]
        if type(deadline) is not int or not 0 <= deadline < len(frames):
            raise ValueError(f"Invalid decision deadline for {item_id}.")
        if first is not None and (type(first) is not int or not 0 <= first < len(frames)):
            raise ValueError(f"Invalid first recognizable frame for {item_id}.")
    observations = defaultdict(set)
    for index, frame in enumerate(frames):
        if frame.get("annotated") is not True:
            raise ValueError(f"{clip['id']} frame {index} needs annotation review.")
        seen = set()
        for box in frame["boxes"]:
            item_id = box["item"]
            if item_id not in items or item_id in seen:
                raise ValueError(f"Invalid or duplicate item {item_id} in {clip['id']} frame {index}.")
            seen.add(item_id)
            x1, y1, x2, y2 = box["xyxy"]
            if not all(math.isfinite(value) for value in box["xyxy"]) or not (
                0 <= x1 < x2 and 0 <= y1 < y2
            ):
                raise ValueError(f"Invalid box for {item_id} in {clip['id']} frame {index}.")
            observations[item_id].add(index)
    for item_id, item in items.items():
        first = item["first_recognizable"]
        if first is not None and first not in observations[item_id]:
            raise ValueError(f"{item_id} needs a box in its first recognizable frame.")


def inspect_camera(path, split):
    _, clips = load_dataset(path, split)
    by_camera = defaultdict(list)
    for clip in clips:
        by_camera[clip["camera"]].append(clip)
    report = {}
    for camera, camera_clips in sorted(by_camera.items()):
        lead_times, view_times = [], []
        encounters = 0
        for clip in camera_clips:
            encounters += len(clip["items"])
            views = defaultdict(list)
            for index, frame in enumerate(clip["frames"]):
                for box in frame["boxes"]:
                    views[box["item"]].append(index)
            for item in clip["items"]:
                first, deadline = item["first_recognizable"], item["last_decision_frame"]
                if first is not None and first <= deadline:
                    lead_times.append((deadline - first) / clip["fps"])
                    count = sum(first <= index <= deadline for index in views[item["id"]])
                    view_times.append(count / clip["fps"])
        report[camera] = {
            "clips": len(camera_clips), "items": encounters, "recognizable_by_deadline": len(lead_times),
            "median_recognition_lead_seconds": median(lead_times) if lead_times else None,
            "median_annotated_view_seconds": median(view_times) if view_times else None,
        }
    return report
