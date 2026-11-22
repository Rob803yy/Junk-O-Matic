-- R1 observational data draft. Raw IMU die counts and Pi CPU health are not enclosure-temperature or heading measurements.
PRAGMA foreign_keys=ON;
CREATE TABLE metadata (key TEXT PRIMARY KEY, value_json TEXT NOT NULL);
CREATE TABLE sessions (id INTEGER PRIMARY KEY, source TEXT NOT NULL, started_utc TEXT NOT NULL, ended_utc TEXT, end_reason TEXT);
CREATE TABLE frames (
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL REFERENCES sessions(id),
  received_utc TEXT NOT NULL, received_monotonic_ns INTEGER NOT NULL,
  raw_offset INTEGER NOT NULL, raw_length INTEGER NOT NULL,
  valid INTEGER NOT NULL CHECK(valid IN (0,1)), error TEXT
);
CREATE TABLE telemetry (
  frame_id INTEGER PRIMARY KEY REFERENCES frames(id), fw TEXT NOT NULL,
  sequence INTEGER NOT NULL, uptime_ms INTEGER NOT NULL, flags INTEGER NOT NULL,
  imu_raw_json TEXT, echo_us INTEGER, distance_mm INTEGER
);
CREATE TABLE events (id INTEGER PRIMARY KEY, utc TEXT NOT NULL, monotonic_ns INTEGER NOT NULL, session_id INTEGER REFERENCES sessions(id), kind TEXT NOT NULL, detail TEXT NOT NULL);
CREATE TABLE health (id INTEGER PRIMARY KEY, utc TEXT NOT NULL, monotonic_ns INTEGER NOT NULL, disk_free_bytes INTEGER NOT NULL, cpu_temp_c REAL);
CREATE INDEX telemetry_sequence ON telemetry(sequence);
