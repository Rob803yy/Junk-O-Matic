"""A CPU detector with multiscale proposals and a trainable crop classifier."""
import copy
import pickle
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.linear_model import SGDClassifier

from .data import BACKGROUND, load_dataset, read_json

# Size is relative to the shorter image dimension, so the same model accepts
# footage at different resolutions.
WINDOW_SIZES = (0.035, 0.055, 0.085, 0.13, 0.20, 0.31, 0.47)


def iou(first, second):
    x1, y1, x2, y2 = first
    a1, b1, a2, b2 = second
    intersection = max(0, min(x2, a2) - max(x1, a1)) * max(0, min(y2, b2) - max(y1, b1))
    union = (x2 - x1) * (y2 - y1) + (a2 - a1) * (b2 - b1) - intersection
    return intersection / union if union else 0.0


def windows(width, height):
    for scale in WINDOW_SIZES:
        size = max(8, round(min(width, height) * scale))
        for aspect in (0.55, 1.0, 1.8):
            w, h = round(size * aspect ** 0.5), round(size / aspect ** 0.5)
            if w > width or h > height:
                continue
            xs = list(range(0, width - w + 1, max(1, w // 2)))
            ys = list(range(0, height - h + 1, max(1, h // 2)))
            for y in sorted({*ys, height - h}):
                for x in sorted({*xs, width - w}):
                    yield x, y, x + w, y + h


def features(image, box):
    crop = image.crop(tuple(round(value) for value in box)).resize((16, 16), Image.Resampling.BILINEAR)
    rgb = np.asarray(crop, dtype=np.float32) / 255
    gray = rgb.mean(axis=2)
    dy, dx = np.gradient(gray)
    cells = rgb.reshape(4, 4, 4, 4, 3).mean(axis=(1, 3))
    gradients = np.stack([dx.clip(0), (-dx).clip(0), dy.clip(0), (-dy).clip(0)], axis=-1)
    edges = gradients.reshape(4, 4, 4, 4, 4).mean(axis=(1, 3))
    return np.concatenate((cells.ravel(), edges.ravel()))


def taco_samples(annotation_path, image_root, mapping_path, labels):
    coco = read_json(annotation_path)
    mapping = read_json(mapping_path)
    names = {category["id"]: category["name"] for category in coco["categories"]}
    if set(names.values()) != set(mapping) or any(label not in labels for label in mapping.values()):
        raise ValueError("The TACO map must map every source category to a configured visual label.")
    entries = {entry["id"]: (Path(image_root) / entry["file_name"], []) for entry in coco["images"]}
    for annotation in coco["annotations"]:
        x, y, w, h = annotation["bbox"]
        if w > 0 and h > 0:
            entries[annotation["image_id"]][1].append(
                ((x, y, x + w, y + h), mapping[names[annotation["category_id"]]])
            )
    return list(entries.values())


def fit(samples, labels, epochs, initial=None):
    rng = np.random.default_rng(7)
    classes = sorted({BACKGROUND, *labels})
    classifier = copy.deepcopy(initial) if initial is not None else SGDClassifier(
        loss="log_loss", alpha=0.001, average=True, random_state=7
    )
    if initial is not None and list(classifier.classes_) != classes:
        raise ValueError("The warm-start model must have the same labels.")
    vectors, targets = [], []
    for path, annotations in samples:
        with Image.open(path) as source:
            image = source.convert("RGB")
        for box, label in annotations:
            x1, y1, x2, y2 = box
            if not (0 <= x1 < x2 <= image.width and 0 <= y1 < y2 <= image.height):
                raise ValueError(f"Box outside image bounds: {path}, {box}")
            vectors.append(features(image, box))
            targets.append(label)
            for _ in range(5):
                dx, dy = rng.uniform(-0.15, 0.15, 2) * (x2 - x1, y2 - y1)
                jitter = (max(0, x1 + dx), max(0, y1 + dy),
                          min(image.width, x2 + dx), min(image.height, y2 + dy))
                vectors.append(features(image, jitter))
                targets.append(label)
        proposals = list(windows(*image.size))
        negatives = 0
        for index in rng.choice(len(proposals), min(len(proposals), max(250, len(annotations) * 60)),
                                replace=False):
            box = proposals[index]
            if max((iou(box, target) for target, _ in annotations), default=0) < 0.15:
                vectors.append(features(image, box))
                targets.append(BACKGROUND)
                negatives += 1
                if negatives >= max(12, min(45, len(annotations) * 12)):
                    break
    if BACKGROUND not in targets or set(targets) == {BACKGROUND}:
        raise ValueError("Training needs both labeled litter and background examples.")
    counts = {label: targets.count(label) for label in set(targets)}
    weights = np.asarray([len(targets) / (len(counts) * counts[label]) for label in targets])
    vectors, targets = np.asarray(vectors), np.asarray(targets)
    for _ in range(epochs):
        order = rng.permutation(len(targets))
        classifier.partial_fit(vectors[order], targets[order], classes=classes, sample_weight=weights[order])
    return classifier, counts


def train(dataset, output, epochs, taco=None):
    labels, clips = load_dataset(dataset, "train")
    root = Path(dataset).parent
    samples = []
    for clip in clips:
        item_labels = {item["id"]: item["label"] for item in clip["items"]}
        for frame in clip["frames"]:
            samples.append((root / frame["image"], [
                (box["xyxy"], item_labels[box["item"]]) for box in frame["boxes"]
            ]))
    initial = None
    if taco:
        initial, _ = fit(taco_samples(*taco, labels), labels, epochs)
    classifier, counts = fit(samples, labels, epochs, initial)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        pickle.dump({"classifier": classifier, "labels": labels, "taco_warm_start": bool(taco),
                     "training_examples": counts}, stream)
    return counts


def detect(image, classifier, threshold):
    proposals = list(windows(*image.size))
    if not proposals:
        return []
    vectors = np.asarray([features(image, box) for box in proposals])
    probabilities = classifier.predict_proba(vectors)
    background = list(classifier.classes_).index(BACKGROUND)
    scores = 1 - probabilities[:, background]
    candidates = np.flatnonzero(scores >= threshold)
    ordered = candidates[np.argsort(-scores[candidates], kind="stable")[:300]]
    selected = []
    for index in ordered:
        box = proposals[index]
        if any(iou(box, detection["box"]) >= 0.35 for detection in selected):
            continue
        selected.append({"box": box, "probabilities": {
            label: float(probability)
            for label, probability in zip(classifier.classes_, probabilities[index])
            if label != BACKGROUND
        }})
        if len(selected) == 50:
            break
    return selected
