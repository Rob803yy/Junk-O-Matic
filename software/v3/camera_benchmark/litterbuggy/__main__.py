"""Command-line entry point for the offline Litterbuggy benchmark."""
import argparse
import json
import subprocess

from .data import inspect_camera, sample_video


def probability(value):
    number = float(value)
    if not 0 < number <= 1:
        raise argparse.ArgumentTypeError("Use a number in (0, 1].")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="Sample video and create an annotation manifest.")
    prepare.add_argument("config")
    prepare.add_argument("output")
    prepare.add_argument("--fps", type=float, default=5)
    inspect = commands.add_parser("inspect", help="Compare camera angles before training.")
    inspect.add_argument("dataset")
    inspect.add_argument("--split", choices=("train", "val"), default="train")
    train = commands.add_parser("train", help="Train a detector on the training drives.")
    train.add_argument("dataset")
    train.add_argument("checkpoint")
    train.add_argument("--epochs", type=int, default=12)
    train.add_argument("--taco", nargs=3, metavar=("COCO_JSON", "IMAGE_DIR", "LABEL_MAP"))
    evaluate = commands.add_parser("evaluate", help="Compare two decision methods on held-out drives.")
    evaluate.add_argument("dataset")
    evaluate.add_argument("checkpoint")
    evaluate.add_argument("output")
    evaluate.add_argument("--split", choices=("val", "test"), default="val")
    evaluate.add_argument("--detection-threshold", type=probability, default=0.60)
    evaluate.add_argument("--decision-threshold", type=probability, default=0.80)
    evaluate.add_argument("--render", action="store_true", help="Write an annotated MP4 for each clip.")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            print(sample_video(args.config, args.output, args.fps))
        elif args.command == "inspect":
            print(json.dumps(inspect_camera(args.dataset, args.split), indent=2))
        elif args.command == "train":
            from .model import train as train_model

            if args.epochs < 1:
                parser.error("--epochs must be a positive integer.")
            counts = train_model(args.dataset, args.checkpoint, args.epochs, args.taco)
            print(f"Saved {args.checkpoint}. Training examples by label: {counts}")
        else:
            from .benchmark import evaluate as evaluate_model

            report = evaluate_model(args.dataset, args.checkpoint, args.split, args.output,
                                    args.detection_threshold, args.decision_threshold, args.render)
            for name, method in report["methods"].items():
                summary = method["overall"]
                print(f"{name}: {summary['correct']} correct, {summary['wrong_bin']} wrong bin, "
                      f"{summary['unknown']} unknown, {summary['missed']} missed")
            print(f"Reports saved to {args.output}")
    except (KeyError, OSError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
