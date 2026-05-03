#!/usr/bin/env python3
"""Data-only logger for Junk-O-Matic V1.0A."""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    import psutil
except ImportError:  # pragma: no cover - useful on minimal Pi images
    psutil = None

try:
    import serial
except ImportError:  # pragma: no cover
    serial = None

CONTROL_AUTHORITY = (
    "SCX6 RC transmitter receiver ESC servo and motor are sole drive-control authority"
)
STAGE = "V1.0A - Instrumented RC Platform"

EVENT_KEYS = {
    "s": "START_ROUTE",
    "e": "END_ROUTE",
    "l": "LITTER_OBSERVED",
    "p": "PICKUP_ATTEMPT",
    "f": "FAULT_OBSERVED",
    "b": "BATTERY_CONCERN",
    "c": "CONTROL_SURPRISE",
    "m": "MECHANICAL_ISSUE",
    "n": "NOTE_MARKER",
    "q": "STOP_RUN",
}

TELEMETRY_FIELDS = [
    "timestamp_utc",
    "aux_battery_voltage",
    "rail_12v",
    "rail_5v",
    "imu_roll_deg",
    "imu_pitch_deg",
    "imu_yaw_deg",
    "enclosure_temp_c",
    "estop",
    "fault_code",
]

HEALTH_FIELDS = [
    "timestamp_utc",
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "cpu_temp_c",
]

EVENT_FIELDS = ["timestamp_utc", "elapsed_s", "event_code", "event_name", "note"]
FAULT_FIELDS = ["timestamp_utc", "source", "fault_code", "message"]


@dataclass
class Counts:
    telemetry_rows: int = 0
    health_rows: int = 0
    event_rows: int = 0
    fault_rows: int = 0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def next_run_id(output_root: Path) -> str:
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"JOM-V1A-{today}-RUN"
    existing = sorted(output_root.glob(f"{prefix}*"))
    used: list[int] = []
    for path in existing:
        suffix = path.name.replace(prefix, "")
        if suffix.isdigit():
            used.append(int(suffix))
    return f"{prefix}{(max(used) + 1) if used else 1:02d}"


def make_run_dirs(run_dir: Path) -> dict[str, Path]:
    dirs = {
        "config": run_dir / "config_snapshot",
        "logs": run_dir / "logs",
        "video": run_dir / "video",
        "exports": run_dir / "exports",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def write_manifest(run_dir: Path, config: dict[str, Any], run_id: str, started_at: str) -> None:
    outputs = {
        "config_snapshot": "config_snapshot/data_logger_config.yaml",
        "arduino_telemetry": "logs/arduino_telemetry.csv",
        "pi_health": "logs/pi_health.csv",
        "events": "logs/events.csv",
        "faults": "logs/faults.csv",
        "summary_for_scorecard": "exports/summary_for_scorecard.csv",
    }
    if config.get("camera", {}).get("enabled", False):
        outputs["video"] = f"video/{config.get('camera', {}).get('output_file', 'front_camera.mp4')}"

    manifest = {
        "run_id": run_id,
        "stage": STAGE,
        "started_at_utc": started_at,
        "operator": config.get("run", {}).get("operator", "TODO_OPERATOR"),
        "buggy_id": config.get("run", {}).get("buggy_id", "JOM-V1A-TODO"),
        "route_id": config.get("run", {}).get("route_id", "ROUTE-TODO"),
        "evidence_folder": config.get("run", {}).get("evidence_folder", "TODO_LOCAL_OR_ONEDRIVE_PATH"),
        "control_authority": CONTROL_AUTHORITY,
        "outputs": outputs,
        "motion_control": {
            "raspberry_pi_controls_vehicle_motion": False,
            "pi_to_esc_control": False,
            "pi_to_steering_control": False,
        },
    }
    with (run_dir / "run_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")


def copy_config_snapshot(config_path: Path, snapshot_path: Path) -> None:
    shutil.copy2(config_path, snapshot_path / "data_logger_config.yaml")


def open_csv(path: Path, fields: list[str]) -> tuple[Any, csv.DictWriter]:
    handle = path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    handle.flush()
    return handle, writer


def pi_cpu_temp_c() -> float | None:
    thermal_path = Path("/sys/class/thermal/thermal_zone0/temp")
    if thermal_path.exists():
        try:
            return round(int(thermal_path.read_text(encoding="utf-8").strip()) / 1000.0, 2)
        except (OSError, ValueError):
            return None
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = result.stdout.strip().replace("temp=", "").replace("'C", "")
    try:
        return float(text)
    except ValueError:
        return None


def health_row() -> dict[str, Any]:
    if psutil is None:
        return {
            "timestamp_utc": utc_now(),
            "cpu_percent": "",
            "memory_percent": "",
            "disk_percent": "",
            "cpu_temp_c": pi_cpu_temp_c() or "",
        }
    return {
        "timestamp_utc": utc_now(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(os.getcwd()).percent,
        "cpu_temp_c": pi_cpu_temp_c() or "",
    }


def health_worker(stop: threading.Event, writer: csv.DictWriter, handle: Any, counts: Counts, interval_s: float) -> None:
    while not stop.is_set():
        writer.writerow(health_row())
        handle.flush()
        counts.health_rows += 1
        stop.wait(interval_s)


def telemetry_worker(
    stop: threading.Event,
    writer: csv.DictWriter,
    fault_writer: csv.DictWriter,
    telemetry_handle: Any,
    fault_handle: Any,
    counts: Counts,
    config: dict[str, Any],
) -> None:
    arduino_cfg = config.get("arduino", {})
    if not arduino_cfg.get("enabled", True):
        return
    if serial is None:
        fault_writer.writerow({
            "timestamp_utc": utc_now(),
            "source": "pi",
            "fault_code": "SERIAL_IMPORT",
            "message": "pyserial is not installed",
        })
        fault_handle.flush()
        counts.fault_rows += 1
        return

    try:
        port = serial.Serial(
            arduino_cfg.get("serial_port", "/dev/ttyUSB0"),
            int(arduino_cfg.get("baud_rate", 115200)),
            timeout=float(arduino_cfg.get("timeout_s", 0.2)),
        )
    except Exception as exc:  # noqa: BLE001 - serial exceptions vary by platform
        fault_writer.writerow({
            "timestamp_utc": utc_now(),
            "source": "arduino",
            "fault_code": "SERIAL_OPEN",
            "message": str(exc),
        })
        fault_handle.flush()
        counts.fault_rows += 1
        return

    with port:
        while not stop.is_set():
            raw_line = port.readline()
            if not raw_line:
                continue
            try:
                payload = json.loads(raw_line.decode("utf-8").strip())
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                fault_writer.writerow({
                    "timestamp_utc": utc_now(),
                    "source": "arduino",
                    "fault_code": "JSON_PARSE",
                    "message": str(exc),
                })
                fault_handle.flush()
                counts.fault_rows += 1
                continue

            row = {field: payload.get(field, "") for field in TELEMETRY_FIELDS}
            row["timestamp_utc"] = utc_now()
            writer.writerow(row)
            telemetry_handle.flush()
            counts.telemetry_rows += 1


def camera_worker(stop: threading.Event, output_path: Path, config: dict[str, Any]) -> None:
    try:
        import cv2
    except ImportError:
        print("Camera enabled but opencv-python is not installed.", file=sys.stderr)
        return

    camera_cfg = config.get("camera", {})
    capture = cv2.VideoCapture(int(camera_cfg.get("device_index", 0)))
    width = int(camera_cfg.get("width", 1280))
    height = int(camera_cfg.get("height", 720))
    fps = float(camera_cfg.get("fps", 30))
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    try:
        while not stop.is_set():
            ok, frame = capture.read()
            if ok:
                writer.write(frame)
            else:
                time.sleep(0.1)
    finally:
        writer.release()
        capture.release()


class KeyReader:
    def __enter__(self) -> "KeyReader":
        self.is_windows = platform.system().lower().startswith("win")
        if self.is_windows:
            import msvcrt

            self.msvcrt = msvcrt
            return self

        import select
        import termios
        import tty

        self.select = select
        self.termios = termios
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if not self.is_windows:
            self.termios.tcsetattr(self.fd, self.termios.TCSADRAIN, self.old_settings)

    def read_key(self) -> str | None:
        if self.is_windows:
            if self.msvcrt.kbhit():
                return self.msvcrt.getwch().lower()
            return None
        ready, _, _ = self.select.select([sys.stdin], [], [], 0)
        if ready:
            return sys.stdin.read(1).lower()
        return None


def event_loop(stop: threading.Event, writer: csv.DictWriter, handle: Any, counts: Counts, start_monotonic: float) -> None:
    print("Press keys for event markers. Press q to stop the run.")
    print(", ".join(f"{key}={name}" for key, name in EVENT_KEYS.items()))
    with KeyReader() as keys:
        while not stop.is_set():
            key = keys.read_key()
            if key in EVENT_KEYS:
                row = {
                    "timestamp_utc": utc_now(),
                    "elapsed_s": round(time.monotonic() - start_monotonic, 3),
                    "event_code": key,
                    "event_name": EVENT_KEYS[key],
                    "note": "",
                }
                writer.writerow(row)
                handle.flush()
                counts.event_rows += 1
                print(f"Marked {EVENT_KEYS[key]}")
                if key == "q":
                    stop.set()
                    break
            time.sleep(0.05)


def write_summary(run_dir: Path, config: dict[str, Any], run_id: str, started_at: str, ended_at: str, counts: Counts) -> None:
    summary_path = run_dir / "exports" / "summary_for_scorecard.csv"
    video_file = ""
    if config.get("camera", {}).get("enabled", False):
        video_file = f"video/{config.get('camera', {}).get('output_file', 'front_camera.mp4')}"
    fields = [
        "run_id",
        "route_id",
        "started_at_utc",
        "ended_at_utc",
        "duration_s",
        "video_enabled",
        "video_file",
        "telemetry_rows",
        "pi_health_rows",
        "event_rows",
        "fault_rows",
        "control_authority",
        "evidence_folder",
    ]
    started_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    ended_dt = datetime.fromisoformat(ended_at.replace("Z", "+00:00"))
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "run_id": run_id,
            "route_id": config.get("run", {}).get("route_id", "ROUTE-TODO"),
            "started_at_utc": started_at,
            "ended_at_utc": ended_at,
            "duration_s": round((ended_dt - started_dt).total_seconds(), 3),
            "video_enabled": bool(config.get("camera", {}).get("enabled", False)),
            "video_file": video_file,
            "telemetry_rows": counts.telemetry_rows,
            "pi_health_rows": counts.health_rows,
            "event_rows": counts.event_rows,
            "fault_rows": counts.fault_rows,
            "control_authority": CONTROL_AUTHORITY,
            "evidence_folder": config.get("run", {}).get("evidence_folder", "TODO_LOCAL_OR_ONEDRIVE_PATH"),
        })


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Junk-O-Matic V1.0A data-only logger")
    parser.add_argument(
        "--config",
        default="software/raspberry_pi/config/data_logger_config.template.yaml",
        help="Path to logger YAML config",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    config = load_config(config_path)
    output_root = Path(config.get("run", {}).get("output_root", "test_data"))
    output_root.mkdir(parents=True, exist_ok=True)

    run_id = next_run_id(output_root)
    run_dir = output_root / run_id
    dirs = make_run_dirs(run_dir)
    started_at = utc_now()
    copy_config_snapshot(config_path, dirs["config"])
    write_manifest(run_dir, config, run_id, started_at)

    counts = Counts()
    stop = threading.Event()
    start_monotonic = time.monotonic()

    telemetry_handle, telemetry_writer = open_csv(dirs["logs"] / "arduino_telemetry.csv", TELEMETRY_FIELDS)
    health_handle, health_writer = open_csv(dirs["logs"] / "pi_health.csv", HEALTH_FIELDS)
    events_handle, events_writer = open_csv(dirs["logs"] / "events.csv", EVENT_FIELDS)
    faults_handle, faults_writer = open_csv(dirs["logs"] / "faults.csv", FAULT_FIELDS)

    threads = [
        threading.Thread(
            target=health_worker,
            args=(
                stop,
                health_writer,
                health_handle,
                counts,
                float(config.get("pi_health", {}).get("sample_interval_s", 5)),
            ),
            daemon=True,
        ),
        threading.Thread(
            target=telemetry_worker,
            args=(stop, telemetry_writer, faults_writer, telemetry_handle, faults_handle, counts, config),
            daemon=True,
        ),
    ]

    if config.get("camera", {}).get("enabled", False):
        output_file = config.get("camera", {}).get("output_file", "front_camera.mp4")
        threads.append(
            threading.Thread(
                target=camera_worker,
                args=(stop, dirs["video"] / output_file, config),
                daemon=True,
            )
        )

    print(f"Started {run_id}")
    print(f"Run folder: {run_dir}")
    print("V1.0A data-only logger. No motion-control commands are sent.")

    try:
        for thread in threads:
            thread.start()
        event_loop(stop, events_writer, events_handle, counts, start_monotonic)
    except KeyboardInterrupt:
        stop.set()
    finally:
        stop.set()
        for thread in threads:
            thread.join(timeout=2)
        ended_at = utc_now()
        write_summary(run_dir, config, run_id, started_at, ended_at, counts)
        for handle in [telemetry_handle, health_handle, events_handle, faults_handle]:
            handle.close()
        print(f"Stopped {run_id}")
        print(f"Scorecard export: {run_dir / 'exports' / 'summary_for_scorecard.csv'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
