# Assisted V3 interfaces and data proposal

Detailed interfaces below are proposed design information, not implemented V3 code.
Keep [Uno serial protocol 2](../v2/serial_protocol.md) and the existing raw-first
telemetry database semantics. The firmware supplies acquisition only; no application
command, model output, advisory or viewer action is routed back to Uno/RC motion.
USB hardware is bidirectional; the no-command requirement describes application
behavior, not a physically one-way or isolated cable.

## Existing contract to reuse

Retain strict keys/units/null flags, bounded framing, serial.raw, sessions/frames/
telemetry/events/health/metadata, raw offsets, host receive UTC/monotonic time and
separate valid/IMU/range counts. Default flags=5 still means zero physical sensor
samples. Preserve each original V2 run database. A V3 coordinator may launch/reuse
that core, but must not insert V3 keys into the strict V2 YAML or silently migrate
an existing database. Packaging changes need V2 regression coverage.

## Proposed additive V3 run bundle

| Artifact | Proposed information / boundary |
| --- | --- |
| `run_context.json` | Vehicle/configuration/source IDs, actual hardware/profile, operator/route/load/conditions, process start/stop and provenance. Private identifying fields stay in the private archive. |
| Existing telemetry artifacts | Original serial.raw, run.sqlite3, config_snapshot.yml and manifest.json retain their established meanings. A parent V3 manifest links them rather than relabeling an old V2 replay. |
| Original camera video + capture metadata | Selected camera ID, settings, resolution/orientation, encoding and explicit completion/failure; original video retained. |
| `video_frames.ndjson` | Run/camera/stream/frame IDs, encoded-frame index, host capture monotonic_ns, receive/capture UTC where available, clock domain and any measured timing limit. |
| `detections.ndjson` | Frame ID, model/class-map/preprocessing IDs, timing, input/source dimensions and outcome: ok, error, dropped, disabled or unavailable. `objects=[]` is healthy no objects only when outcome=ok; unavailable results use null. |
| Detection objects | Label/class-map ID, confidence, normalized original-frame xyxy box with 0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1. Record reverse crop/resize/letterbox/orientation transforms before mapping boxes to source frames. |
| `alerts.ndjson` | Advisory ID/state, source frame/model, creation/expiry/acknowledgment if used, health and reason. No motion action. Expired/stale/no-model states are visible, not an all-clear. |
| `model_manifest.json` | Immutable weight hash, origin, runtime/export/quantization, input/preprocessing, class map, training dataset/split IDs and evaluation reference. |
| `upload_manifest.json` | Closed-run artifact list/lengths/hashes, archive ID, transfer/destination verification and missing/unfinished files. No public credentials or private access URLs in Git. |
| `qc_report.json` / review output | Explicit enabled-sensor/frame denominators, missing/error/drop counts, timing/coverage and operator notes; no invented voltage, calibrated attitude, GPS or scorecard result. |

These names define a proposed contract. Schemas and validation examples will be
implemented with the selected camera/model/runtime, not represented by empty files.

## Timing and resource behavior

Use the Pi host monotonic clock for capture/inference/alert timing and record its
clock domain. Uno acquisition uptime and host receive time remain distinct.
Video writer nominal FPS is not a synchronized sensor clock. Resolve video frame
indices and timestamps explicitly; do not match files only by nearby filenames or
assume exact frame-to-IMU alignment. Record measured uncertainty before claiming
alignment precision.

Use a bounded inference queue and record skipped/dropped work. A stale result
must not become a current alert. Acquisition/archive remains independent of a
slow/failed inference or disconnected viewer; resource budgets and limits require
real Pi benchmarks. UI/advisories require an available operator display/link;
local logging can continue during disconnection, but live alerts are unavailable.

## Alerts and model/data workflow

The first proposed alert channel is an operator display. Physical buzzer/OLED or
other alert circuitry is optional and unselected. Existing Uno range-feedback
code is not a camera-alert command interface. Choose display location, update
cadence, stale expiry, alert grouping and acknowledgment behavior in the decision
record before implementing an operator workflow.

Capture representative litter and negative scenes, define an annotation rubric,
sample independent images, and split whole outings/locations/days before training.
The seven archived labels are candidate names only. No archived placeholder
metric or configured class is an observed/trained result. Train/evaluate a selected
baseline off the acquisition Pi; benchmark the exported candidate on the actual
Pi and run advisory-only observation trials. Dataset/model/threshold/preprocessing
changes need new identities and comparable held-out evaluation.
