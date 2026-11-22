# Historical V1A Pi logger / preserved, not selected for new V2

The original program, configuration and requirements remain unchanged for
traceability. For new work use [the V2 acquisition draft](../v2/raspberry_pi/README.md)
and its separate dependency/config/serial contract. Do not install or run this
older folder merely because it is the first Pi path in the tree.

## Known limits from source review

- The legacy parser accepts arbitrary JSON dictionaries, fills missing expected
  fields with blanks and still counts rows. An offline fake-port check confirmed
  a valid V2 frame becomes a counted row with all measurement columns blank.
  [Receipt](../../reports/repository_review/legacy-parser-reproduction.json).
- Original serial bytes are not preserved; strict schema/bounds/version checking
  and reconnect/session handling are not implemented here.
- Serial open failure exits its worker; read exceptions/worker failure do not
  reliably establish the final run's capture quality.
- `video_enabled` records requested configuration, not usable video. The legacy
  camera path does not provide the current separate capture sidecar checks.
- A clean main exit or existing summary file does not prove worker success,
  rail stability, reset-free operation or synchronized evidence.
- The example serial device, Pi4/Nano assumptions, 1Hz stub and voltage/attitude
  fields are historical defaults, not the current installed configuration.

No vehicle command writes are present in this source; that does not inspect all
physical interfaces. These limitations are contained by selecting the new V2 path,
not by claiming the preserved program has been repaired or qualified.

The [former setup guide](../../docs/history/v1a-pi-readme.md) is historical.
Use [the environment matrix](../../docs/environment-setup.md),
[contract dictionary](../../docs/data_dictionary.md) and
[V2 evidence plan](../../docs/v2/verification-plan.md) for next work.
