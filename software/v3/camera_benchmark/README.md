# Assisted V3 offline camera benchmark

This prototype uses recorded ground-view footage to measure when litter becomes recognizable and how consistently camera predictions agree across the approach. Provisional sorting destinations and pickup deadlines provide offline test labels. Assisted V3 uses manual RC, advisory camera detection, and logging. The benchmark has no vehicle-control or live-alert integration.

## Collect the first drives

Plug in the USB camera and select it in your computer’s camera app. Record four short clips for a first test: a training clip with a few passes, a validation clip with different objects, a test clip with another set of objects, and a litter-free test clip. Save them as video files such as MP4 or MOV. Run the commands below from `software/v3/camera_benchmark/`. Keep recordings, checkpoints, and result files outside Git.

1. Rigidly mount a forward-facing camera angled down toward the approach path and the pickup area. At normal driving speed, record short runs at two mounting angles with the same kinds of items. Calibrate the pickup point on the ground and mark the last frame where a decision would be usable. Allow for the actual mechanism's response time when setting that deadline.
2. For each angle, compare how many items are recognizable by the deadline and how long before it they become recognizable. Check the footage for blur, vibration, glare, and small items leaving the frame. Pick the angle before recording the larger benchmark. Keep repeated passes over the same physical items together when assigning splits.
3. Collect pavement, grass, and gravel or dirt in sunny, overcast, and wet conditions. Stage some crushed, dirty, and partly hidden items. Include litter-free drives with lookalikes such as rocks, leaves, and puddle reflections. Use separate drives and staged items for training, validation, and testing. Record approximate speed and camera angle in the clip notes.
4. Inspect the litter in person and record its material and actual destination independently of what appears in the footage. Identify ambiguities the camera cannot resolve. If image evidence cannot reliably separate two destinations, the decision threshold should favor `unknown` over a wrong-bin commitment.

## Prepare and annotate

Requires Python 3.10 or later and FFmpeg with the `libx264` encoder for annotated MP4s.

```sh
python -m pip install -r requirements.txt
python -m litterbuggy prepare clips.json data/buggy --fps 5
```

Create `clips.json` beside the videos or use paths relative to that file. The labels map visual classes to sorting destinations. The example uses provisional destinations. When testing actual material-based sorting, define the intended destinations and distinguish the visual classes the camera should learn. A visual class can also map to `unknown`.

```json
{
  "labels": {
    "bottle": "bottles",
    "can": "cans",
    "wrapper_or_bag": "flexible_packaging",
    "other_litter": "other"
  },
  "clips": [
    {
      "id": "test_wet_01",
      "video": "footage/test_wet_01.mp4",
      "drive": "drive_07",
      "group": "staged_item_set_07",
      "split": "test",
      "terrain": "gravel",
      "weather": "wet",
      "camera": "mount_a",
      "notes": "Use notes for mounting angle, speed, and any conditions worth recording."
    }
  ]
}
```

Add clip rows for all three splits. A drive, group of related passes, or supplied physical item ID may only occur in one split. Each clip should have consistent terrain and weather. Use short clips for the pilot. At 5 FPS the test has 200 ms timing resolution. Increase the rate if recognizable views last only a few frames.

Edit the generated `data/buggy/dataset.json`. Add one entry per item encounter to the clip's `items` array. Reuse `physical_id` across repeat passes. Include staged items that turn out to be invisible so the benchmark can count misses. Frame indices are zero-based and refer to the extracted frames in the manifest.

```json
{
  "id": "item_01",
  "physical_id": "staged_can_014",
  "label": "can",
  "material": "aluminum",
  "bin": "cans",
  "first_recognizable": 6,
  "last_decision_frame": 13
}
```

Set `first_recognizable` to `null` if the item is never recognizable. The deadline still comes from where the buggy would have needed to make a decision. For each reviewed frame, mark `annotated` true and add boxes for all visible items. Use pixel coordinates `[left, top, right, bottom]` in the extracted image. Leave `boxes` empty on reviewed frames with no visible litter. An entirely litter-free clip has an empty `items` list.

```json
{
  "image": "frames/test_wet_01/000006.jpg",
  "annotated": true,
  "boxes": [{"item": "item_01", "xyxy": [80, 120, 112, 148]}]
}
```

Run `python -m litterbuggy inspect data/buggy/dataset.json` on annotated pilot drives to compare mounting angles before training. The summary counts encounters that are recognizable by the deadline and reports the median time available to make a decision. It also measures the time represented by annotated views between first recognition and the deadline.

## Train and evaluate

```sh
python -m litterbuggy train data/buggy/dataset.json runs/buggy.pkl
python -m litterbuggy evaluate data/buggy/dataset.json runs/buggy.pkl runs/validation --split val
python -m litterbuggy evaluate data/buggy/dataset.json runs/buggy.pkl runs/test --split test --render
```

The CPU baseline scores multiscale image crops using a classifier trained on color and edge features. It associates boxes by overlap across adjacent frames. Both methods commit once they reach the decision threshold. The multi-frame method requires two observations and weights the evidence using apparent size and edge sharpness. These are confidence scores from the classifier. Select the detection and decision thresholds on validation drives with `--detection-threshold` and `--decision-threshold`, then pass the exact selected values to the test run. Higher thresholds generally trade more unknowns and misses for fewer confident errors. Only load checkpoints you trust because they contain a serialized Python model.

If the training set is small, optionally start with TACO's COCO-format annotations and image directory. Create a JSON object that maps each TACO category name to one of the configured visual labels. Use a catch-all litter label for categories that do not correspond to a target class. Run the same validation and test commands with the warm-start checkpoint and keep the buggy data splits fixed.

```sh
python -m litterbuggy train data/buggy/dataset.json runs/taco_then_buggy.pkl \
  --taco /path/to/annotations.json /path/to/taco-images /path/to/taco-label-map.json
```

- `report.json` gives both methods' outcome counts and rates overall and by terrain, weather, and camera. Read the counts with the rates, especially for sparsely sampled conditions.
- `predictions.json` gives per-item outcomes and per-track boxes, IDs, predictions, confidence scores, and decision timestamps. A track is matched to an item only through box overlap by its deadline. A matched item with no commitment at the deadline is an unknown. An unmatched item is missed. If the expected destination is explicitly `unknown`, a matched abstention is correct and is excluded from the known-bin sort rate.
- With `--render`, each sampled clip is reconstructed as an annotated MP4. Green boxes show the annotated item, expected destination, and deadline. Orange boxes show the multi-frame model. Use the JSON to compare both methods. A null rate indicates a missing denominator, such as a test condition without any litter-free minutes.

This prototype measures offline sorting performance. Actual field accuracy requires representative annotated footage. The classifier and tracker are a starting point for measuring how much useful evidence the camera provides. Fast motion and small or low-contrast litter can defeat box association and crop scoring.
