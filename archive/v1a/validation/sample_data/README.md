# Legacy sample CSVs / format examples, not field evidence

The four CSVs in this folder are preserved unchanged from the May 2026 V1A
scaffold. Their timestamps, plausible voltages/attitude/temperature, route duration
and row counts have no accepted raw-run provenance in this repository. Treat them
as examples only; do not import them as current V2 measurements or passed gates.

| File | Meaning and limit |
| --- | --- |
| `sample_arduino_telemetry.csv` | Legacy column example; values match the constant-emitting stub, not verified sensing |
| `sample_events.csv` | Legacy keyboard-marker shape; current V2 logger has no route-marker keyboard loop |
| `sample_pi_health.csv` | Legacy utilization/CPU-temperature shape; no rail, ambient or reset proof |
| `sample_summary_for_scorecard.csv` | Example legacy 45-minute summary; not completed field-session evidence |

Current V2 [protocol/schema](../../../../docs/data_dictionary.md) and
[scorecard rules](../../../../validation/scorecard/README.md) differ. Example dates do not establish
capture dates or approval. These files were not edited or regenerated in REPO-R1.
