import unittest

from PIL import Image

from litterbuggy.benchmark import score_clip, summarize, track_frames
from litterbuggy.data import validate_splits


class BenchmarkTest(unittest.TestCase):
    def setUp(self):
        self.box = (8, 8, 26, 28)
        self.labels = {"can": "metal", "bottle": "plastic"}
        self.clip = {
            "fps": 5, "frames": [{"boxes": [{"item": "item", "xyxy": self.box}]}] * 3,
            "items": [{"id": "item", "first_recognizable": 0, "last_decision_frame": 1,
                       "bin": "metal", "material": "aluminum"}],
        }

    def test_decisions_are_causal_and_compare_both_methods(self):
        predictions = iter([
            [{"box": self.box, "probabilities": {"can": 0.48, "bottle": 0.52}}],
            [{"box": self.box, "probabilities": {"can": 0.98, "bottle": 0.02}}],
            [{"box": self.box, "probabilities": {"can": 0.01, "bottle": 0.99}}],
        ])
        tracks = track_frames([Image.new("RGB", (40, 40))] * 3, 5, lambda _: next(predictions))
        results = score_clip(self.clip, tracks, self.labels, 0.50)
        single = results["single_frame"]["items"][0]
        multi = results["multi_frame"]["items"][0]
        self.assertEqual((single["outcome"], single["decision_seconds"]), ("wrong_bin", 0))
        self.assertEqual((multi["outcome"], multi["decision_seconds"]), ("correct", 0.2))
        self.clip["items"][0]["last_decision_frame"] = 0
        early = score_clip(self.clip, tracks, self.labels, 0.50)["multi_frame"]["items"][0]
        self.assertEqual(early["outcome"], "unknown")
        self.assertIsNone(early["decision_seconds"])

    def test_only_post_deadline_detections_are_misses(self):
        tracks = [[{"frame": 2, "box": self.box, "probabilities": {"can": 1}, "quality": 1}]]
        result = score_clip(self.clip, tracks, self.labels, 0.50)
        self.assertEqual(result["single_frame"]["items"][0]["outcome"], "missed")

    def test_false_tracks_per_minute_uses_only_litter_free_clips(self):
        mode = "multi_frame"
        tracks = [[{"frame": 0, "box": self.box, "probabilities": {"can": 1}, "quality": 1}]]
        empty_clip = dict(self.clip, frames=[{"boxes": []}] * 3, items=[])
        result = {"duration_seconds": 30, "fps": 5,
                  "methods": score_clip(empty_clip, tracks, self.labels, 0.50)}
        summary = summarize([result], mode)
        self.assertEqual(summary["false_detection_tracks_per_minute"], 2)
        self.assertEqual(summary["false_sort_decisions"], 0)
        self.assertIsNone(summary["correct_sort_rate"])

    def test_repeated_physical_item_cannot_cross_splits(self):
        clip = {"id": "one", "split": "train", "drive": "a", "group": "a", "weather": "wet",
                "terrain": "grass", "camera": "a", "items": [{"physical_id": "same"}]}
        other = dict(clip, id="two", split="test", drive="b", group="b")
        with self.assertRaisesRegex(ValueError, "physical item same crosses splits"):
            validate_splits({"labels": self.labels, "clips": [clip, other]})


if __name__ == "__main__":
    unittest.main()
