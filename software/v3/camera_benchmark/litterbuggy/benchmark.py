"""Track detections and score sort decisions against pickup deadlines."""
import pickle
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .data import UNKNOWN, load_dataset, write_json
from .model import detect, iou

MATCH_IOU = 0.30
MODES = ("single_frame", "multi_frame")
OUTCOMES = ("correct", "wrong_bin", "unknown", "missed")


def assign(pairs):
    """Greedily assign highest-quality pairs, with each side used at most once."""
    left_used, right_used = set(), set()
    for _, left, right in sorted(pairs, reverse=True):
        if left not in left_used and right not in right_used:
            left_used.add(left)
            right_used.add(right)
            yield left, right


def view_quality(image, box):
    crop = image.crop(box).convert("L")
    pixels = np.asarray(crop, dtype=np.float32) / 255
    dx, dy = np.gradient(pixels)
    detail = np.hypot(dx, dy).mean()
    relative_size = min(crop.size) / min(image.size)
    return float(np.clip(relative_size / 0.08, 0.25, 2) * np.clip(detail / 0.08, 0.25, 2))


def track_frames(frames, fps, predictor):
    tracks = []
    active = {}
    gap = max(1, round(fps * 0.5))
    for index, image in enumerate(frames):
        detections = predictor(image)
        active = {key: observation for key, observation in active.items()
                  if index - observation["frame"] <= gap}
        pairs = []
        for track_id, previous in active.items():
            for detection_id, detection in enumerate(detections):
                overlap = iou(previous["box"], detection["box"])
                if overlap >= 0.15:
                    pairs.append((overlap, track_id, detection_id))
        matches = {detection_id: track_id for track_id, detection_id in assign(pairs)}
        for detection_id, detection in enumerate(detections):
            track_id = matches.get(detection_id)
            if track_id is None:
                track_id = len(tracks)
                tracks.append([])
            observation = dict(detection, frame=index, quality=view_quality(image, detection["box"]))
            tracks[track_id].append(observation)
            active[track_id] = observation
    return tracks


def decisions(track, labels, threshold, fps, mode):
    """Generate causal decisions using only frames observed so far."""
    total = Counter()
    weight_sum = 0
    committed = None
    history = []
    for index, observation in enumerate(track):
        probabilities = observation["probabilities"]
        if mode == "multi_frame":
            weight = observation["quality"]
            weight_sum += weight
            total.update({label: score * weight for label, score in probabilities.items()})
            probabilities = {label: score / weight_sum for label, score in total.items()}
        label = max(probabilities, key=probabilities.get)
        confidence = probabilities[label]
        if (committed is None and confidence >= threshold and labels[label] != UNKNOWN
                and (mode == "single_frame" or index >= 1)):
            committed = {"label": label, "bin": labels[label], "confidence": confidence,
                         "decision_frame": observation["frame"],
                         "decision_seconds": observation["frame"] / fps}
        history.append(committed or {"label": UNKNOWN, "bin": UNKNOWN, "confidence": confidence,
                                    "decision_frame": None, "decision_seconds": None})
    return history


def match_items(clip, tracks):
    by_frame = defaultdict(list)
    for track_id, track in enumerate(tracks):
        for observation in track:
            by_frame[observation["frame"]].append((track_id, observation["box"]))
    items = {item["id"]: item for item in clip["items"]}
    overlaps = defaultdict(list)
    for frame_id, frame in enumerate(clip["frames"]):
        for truth in frame["boxes"]:
            item = items[truth["item"]]
            if frame_id > item["last_decision_frame"]:
                continue
            for track_id, box in by_frame[frame_id]:
                overlap = iou(box, truth["xyxy"])
                if overlap >= MATCH_IOU:
                    overlaps[item["id"], track_id].append(overlap)
    pairs = [(sum(values), item_id, track_id) for (item_id, track_id), values in overlaps.items()]
    return dict(assign(pairs))


def score_clip(clip, tracks, labels, threshold):
    matches = match_items(clip, tracks)
    fps = clip["fps"]
    results = {}
    for mode in MODES:
        histories = [decisions(track, labels, threshold, fps, mode) for track in tracks]
        rows = []
        for item in clip["items"]:
            deadline = item["last_decision_frame"]
            track_id = matches.get(item["id"])
            decision = {"label": UNKNOWN, "bin": UNKNOWN, "confidence": None,
                        "decision_frame": None, "decision_seconds": None}
            outcome = "missed"
            if track_id is not None:
                decision = next(result for observation, result in
                                reversed(list(zip(tracks[track_id], histories[track_id])))
                                if observation["frame"] <= deadline)
                if decision["bin"] == UNKNOWN:
                    outcome = "correct" if item["bin"] == UNKNOWN and decision["decision_frame"] is None else "unknown"
                else:
                    outcome = "correct" if decision["bin"] == item["bin"] else "wrong_bin"
            rows.append({"item": item["id"], "material": item["material"], "expected_bin": item["bin"],
                         "first_recognizable": item["first_recognizable"], "deadline_frame": deadline,
                         "track_id": track_id, "outcome": outcome, **decision})
        results[mode] = {
            "items": rows,
            "tracks": [{"track_id": track_id, "observations": [
                {"frame": observation["frame"], "seconds": observation["frame"] / fps,
                 "box": observation["box"], **result}
                for observation, result in zip(track, history)
            ]} for track_id, (track, history) in enumerate(zip(tracks, histories))],
        }
    return results


def summarize(results, mode):
    rows = [row for result in results for row in result["methods"][mode]["items"]]
    counts = Counter(row["outcome"] for row in rows)
    empty = [result for result in results if not result["methods"][mode]["items"]]
    minutes = sum(result["duration_seconds"] for result in empty) / 60
    false_tracks = sum(len(result["methods"][mode]["tracks"]) for result in empty)
    false_sorts = sum(track["observations"][-1]["decision_frame"] is not None
                      for result in empty for track in result["methods"][mode]["tracks"])
    recognizable = [
        (row["deadline_frame"] - row["first_recognizable"]) / result["fps"]
        for result in results for row in result["methods"][mode]["items"]
        if row["first_recognizable"] is not None and row["first_recognizable"] <= row["deadline_frame"]
    ]
    actionable = [row for row in rows if row["expected_bin"] != UNKNOWN]
    return {
        "clips": len(results), "items": len(rows), **{key: counts[key] for key in OUTCOMES},
        "items_with_known_bin": len(actionable),
        "correct_sort_rate": sum(row["outcome"] == "correct" for row in actionable) / len(actionable)
        if actionable else None,
        "expected_unknown": len(rows) - len(actionable),
        "recognizable_by_deadline": len(recognizable),
        "median_recognition_lead_seconds": float(np.median(recognizable)) if recognizable else None,
        "litter_free_minutes": minutes, "false_detection_tracks": false_tracks,
        "false_detection_tracks_per_minute": false_tracks / minutes if minutes else None,
        "false_sort_decisions": false_sorts,
        "false_sort_decisions_per_minute": false_sorts / minutes if minutes else None,
    }


def render_clip(clip, result, root, destination):
    predictions = defaultdict(list)
    for track in result["methods"]["multi_frame"]["tracks"]:
        for observation in track["observations"]:
            predictions[observation["frame"]].append((track["track_id"], observation))
    truth = {item["item"]: item for item in result["methods"]["multi_frame"]["items"]}
    with tempfile.TemporaryDirectory() as tmp:
        for index, frame in enumerate(clip["frames"]):
            with Image.open(root / frame["image"]) as source:
                image = source.convert("RGB")
            draw = ImageDraw.Draw(image)
            for box in frame["boxes"]:
                item = truth[box["item"]]
                deadline = item["deadline_frame"]
                suffix = f" / {item['outcome']}" if index >= deadline else ""
                draw.rectangle(box["xyxy"], outline="lime", width=2)
                draw.text((box["xyxy"][0], box["xyxy"][1] + 2),
                          f"GT {item['expected_bin']} / due {deadline}{suffix}", fill="lime",
                          stroke_fill="black", stroke_width=1)
            for track_id, observation in predictions[index]:
                box = observation["box"]
                draw.rectangle(box, outline="orange", width=2)
                draw.text((box[0], max(0, box[1] - 13)),
                          f"#{track_id} {observation['bin']} {observation['confidence']:.2f}",
                          fill="orange", stroke_fill="black", stroke_width=1)
            draw.text((4, 4), f"{clip['id']}  {index / clip['fps']:.2f}s",
                      fill="white", stroke_fill="black", stroke_width=1)
            image.save(Path(tmp) / f"{index:06d}.jpg")
        subprocess.run([
            "ffmpeg", "-nostdin", "-v", "error", "-y", "-framerate", str(clip["fps"]),
            "-i", str(Path(tmp) / "%06d.jpg"), "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(destination),
        ], check=True)


def load_tracks(root, clips, classifier, threshold):
    def images(clip):
        for frame in clip["frames"]:
            with Image.open(root / frame["image"]) as source:
                yield source.convert("RGB")

    return [track_frames(images(clip), clip["fps"], lambda image: detect(image, classifier, threshold))
            for clip in clips]


def evaluate(dataset, checkpoint, split, output, detection_threshold, decision_threshold, render):
    labels, clips = load_dataset(dataset, split)
    root = Path(dataset).parent
    with Path(checkpoint).open("rb") as stream:
        model = pickle.load(stream)
    if labels != model["labels"]:
        raise ValueError("Checkpoint labels and destination mapping differ from the dataset.")
    all_tracks = load_tracks(root, clips, model["classifier"], detection_threshold)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for clip, tracks in zip(clips, all_tracks):
        result = {key: clip[key] for key in ("id", "terrain", "weather", "camera", "fps")}
        result["duration_seconds"] = len(clip["frames"]) / clip["fps"]
        result["methods"] = score_clip(clip, tracks, labels, decision_threshold)
        if render:
            render_clip(clip, result, root, output / f"{clip['id']}.mp4")
        results.append(result)
    report = {"split": split, "checkpoint": str(checkpoint), "taco_warm_start": model["taco_warm_start"],
              "labels": labels, "detection_threshold": detection_threshold,
              "decision_threshold": decision_threshold, "match_iou": MATCH_IOU}
    report["methods"] = {}
    for mode in MODES:
        summary = {"overall": summarize(results, mode)}
        for dimension in ("terrain", "weather", "camera"):
            summary[dimension] = {
                value: summarize([result for result in results if result[dimension] == value], mode)
                for value in sorted({result[dimension] for result in results})
            }
        report["methods"][mode] = summary
    write_json(output / "report.json", report)
    write_json(output / "predictions.json", results)
    return report
