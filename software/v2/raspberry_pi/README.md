# V2 Pi acquisition draft

Records observational telemetry only. Existing V1A code is preserved. This draft
does not establish what is currently deployed on the Pi.

## Setup and offline review

Python 3.10+; SQLite is bundled with Python. Install the small requirements list
in a virtual environment from the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r software/v2/raspberry_pi/requirements.txt
python software/v2/raspberry_pi/logger.py --config software/v2/raspberry_pi/config.example.yml --replay software/v2/tests/fixtures/disabled.ndjson --output-root runs
```

Replay is explicitly labelled in manifest metadata. It is not a sensor validation.
For live use, copy config.example.yml to a private local config and set the actual
verified /dev/serial/by-id/... or platform COM port after resolving recognition.
The port is intentionally null in the template. Run with --config pointing to
that file, optionally --duration-seconds 60. Opening USB serial may reset the Uno.

Each uniquely named run contains `manifest.json`, `config_snapshot.yml`,
`serial.raw` and `run.sqlite3`. The manifest records mode, config/hash, logger
hash, environment, counts, raw hash and completion/failure state. Firmware/source
correspondence remains unverified. SQLite contains sessions, all frames and
raw offsets, valid telemetry, events and disk/CPU-temperature samples.

Read timeouts preserve partial frames. Overlong or malformed input is retained
and rejected; reconnect does not combine two devices' partial lines. Disconnects
close sessions and reconnect automatically; failed opens retry at configured
intervals. Disk threshold failures terminate with nonzero exit status. Ctrl+C
and SIGTERM close the database and write final metadata. Forced power loss may
leave a running manifest; disk durability and recovery need physical tests.

```sh
python software/v2/raspberry_pi/export.py runs/RUN-ID runs/RUN-ID/telemetry.csv
```

Exports only validated telemetry, refuses to overwrite output, and retains raw
data/rejections in the original archive. Valid frames with null measurements
must not be scored as successful sensor acquisition. Expected telemetry/video
percentage and electrical rail stability are not inferred from these counts.

## Camera and operating notes

`capture_video.py` is optional, separate from serial logging, and requires
opencv-python plus a supported installed camera. It verifies capture/writer
opening and frame dimensions, and writes success/failure metadata. Example:

```sh
python software/v2/raspberry_pi/capture_video.py runs/RUN-ID/front.mp4 --seconds 60 --device 0
```

Video timestamps are not synchronized sensor sample times. Review actual footage
and frame count/duration; a completed call alone does not establish 95% usable
video. Pi CSI/libcamera integration is not implemented without a camera model.
Disk/CPU-temperature health is not undervoltage or reset evidence.

## Optional service draft

Automatic boot logging is proposed, not confirmed installed. The supplied service
assumes a dedicated litterbuggy user/group, dialout serial permissions, repository
and venv under /opt/litterbuggy, and a reviewed private config at
/etc/litterbuggy/config.yml. StateDirectory creates /var/lib/litterbuggy for run
data. Provision these explicitly, then install the unit under /etc/systemd/system
and enable it only after manual bench tests. No service was installed or enabled
by drafting these files. The unit uses SIGTERM for clean shutdown and does not
depend on a keyboard, GUI or network connection.

Test with `python -m pytest software/v2/tests -q` after installing pytest.

## R1 configuration reconciliation

The active example records CFG-V2-R1 and manifest stage V2-R1 draft. Pi3B versus
Pi4 remains conflicting; software compatibility on the user's actual Pi/OS is
not tested here. Source S06's CSV D/H messages and 20Hz/1Hz scheduling are not a
compatibility mode. This logger accepts only the documented JSON protocol 2.
The proposed firmware emits at 10Hz. SQL retains raw MPU die-temperature counts;
Pi health CPU temperature does not measure enclosure ambient or battery state.
Service restart is acquisition recovery, not a motion watchdog or E-stop.
