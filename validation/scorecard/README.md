# Scorecard use / configuration and evidence required

Use the [corrected editable scorecard](../../docs/reconciliation/editable/LitterBuggy_Scorecard_R1.xlsx)
and [review data system](../../docs/reconciliation/editable/LitterBuggy_Review_Data_System_R1.xlsx)
with the [source corrections](../../docs/reconciliation/README.md). Do not mix
historical CFG-001 results, CFG-V2-R1 observations and example CSVs.

The old logger generates `exports/summary_for_scorecard.csv`. The current V2 logger
does **not** generate that file or automatically populate these workbooks. It
produces raw/SQLite/manifest artifacts and an optional validated-telemetry CSV.
No new automatic import/mapping is implemented in this review.

| Proposed review measure | Evidence needed / current limit |
| --- | --- |
| Physical sample coverage | Enabled/configured sensors, observed non-null samples and an agreed expected-sample denominator; valid null frames do not count |
| Video usability | Actual file, duration/frame review and defined usable criteria; enabled/requested flag is insufficient |
| Power/rail stability | Appropriate physical measurements, units, method/load and agreed limits; neither logger infers rail stability |
| Reset/recovery behavior | Independent boot/power evidence and method; sequence gaps or CPU temperature alone do not prove resets/no resets |
| Field duration and route events | Independent operator/run record; V2 has no legacy keyboard-marker or route-metadata integration |
| Traceability | Configuration/source IDs, raw archive reference/hashes, replay/bench/field mode and reviewer/date |

10/10 starts, 95% coverage/video and five 45-minute sessions remain historical
targets, not current adopted acceptance thresholds. Leave score/evidence/denominator
pending when unavailable; do not invent zeros or import the example 45-minute run.
Existing workbook formulas were corrected in R1; no workbook was changed here.
