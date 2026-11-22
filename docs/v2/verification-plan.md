# V2 evidence plan / next physical and software review

REPO-R1, 2026-11-22. This is a prioritized collection plan for CFG-V2-R1, using
ARCH-R2 and CAD-R3. It records no completed physical test, adopted acceptance
threshold, payload approval or deployment. Use [the original claim register](../v2_verification/README.md)
and [38 reconciliation decisions](../reconciliation/README.md) for exact claim IDs.
New evidence should update the affected record rather than replace uncertainty
with a plausible number. No new field operation is authorized by document checks.

| Priority | Evidence item | Required bounded record | Close only when |
| --- | --- | --- | --- |
| High / before changing power or wiring | Pack, adapter, converters and protection | Actual model/label/contact views; both conductors traced; polarity, fuse/switch order, wire/connectors and installed ratings | Named physical routes and ratings have supporting evidence; catalog labels alone do not establish loaded behavior |
| High / before choosing supply entry | Pi identity and Uno power/USB coexistence | Pi board/model/OS, actual input connector, USB path and any simultaneous external supply | Proposed connection is reconciled to traced hardware; no generic duplicated 5V feed assumed |
| High / before enabling a driver | Sensor/feedback identity and electrical mapping | Board/breakout markings, supplies/pull-ups, physical pin/view, driver interface and calibration method | Exact installed circuit matches the enabled profile; A02YYUW UART is not paired with trigger/echo code |
| High / before replacing running software | Existing sketch and output preservation | Source/build search, readable backup/recovery outcome, file hashes and original serial bytes/settings | Recovery/capture outcome is explicitly recorded; a compile is not a recovered program |
| High / before relying on geometry for fabrication or loaded motion | Mount, tub/hinge and clearances | Measured datums/sections/joints, hinge/latch/moving membership, actual travel, battery/case access and moving clearance | Measurements and method support each dimension; photo ratios and 55-degree review pose remain illustrative until measured |
| Medium / verified bench configuration | New producer/parser/logger behavior | Compile IDs; labeled replay versus physical mode; real timing/null/fault behavior; raw/SQLite/session/export artifacts | Observations match the contract and an agreed test method; valid null frames are not physical samples |
| Medium / deployment selection | Pi service/disk/reconnect/shutdown | Actual OS/permissions/port, controlled disconnect and shutdown evidence; independent power/boot record if assessing resets | Behavior is demonstrated on named hardware; service restart is not an E-stop or motion watchdog |
| Medium / optional camera | Actual camera fitting and usable capture | Model, capture settings/file/sidecar, footage review and alignment method | Usable duration/coverage and any synchronization claim have explicit evidence and limits |
| Later / controlled field evidence | Load/route/reliability and operator events | Identified configuration, reviewed load/route, independent observations, raw archive and defined metrics | Agreed criteria and actual evidence exist; old example sessions or percentage targets do not count |

For each item record: claim/status, configuration and source revision, who/when,
method/conditions/units, evidence reference/hash, result, limits and affected files.
Use null/pending for missing evidence or denominator. If a failure is observed,
record it as an observation and assess severity separately; a blank is not a pass,
automatic critical failure or invented zero.

## Acceptance rules still to agree

The old 10/10 starts, 95% telemetry/video and five 45-minute sessions are
historical targets. Timing proposals also differ among references. Select the
enabled sensors, schedule, expected-sample denominator, tolerated faults/missing
data, video usability definition and load/power limits for the actual configuration
before using a metric as an acceptance gate. The logger's expected interval is
configuration metadata, not an implemented completeness/stale-input evaluator.

V2 currently supplies no voltage/GPS/E-stop measurements, route keyboard markers,
automatic scorecard summary or calibrated attitude. Those need independent evidence
or a separate scoped implementation. [Contract/output dictionary](../data_dictionary.md)
and [scorecard guidance](../../validation/scorecard/README.md) prevent silent substitution.

## Source update sequence

1. Preserve original evidence; identify the exact claim and status change.
2. Correct the canonical editable source and affected linked register/BOM/code.
3. Recheck source/export consistency using tools appropriate to that change.
4. Present the correction for technical review with remaining uncertainty visible.
5. After content review, regenerate/proof current PDFs under a revised export record.

The physical Uno identity and owner-confirmed frame/tipping relationships remain
valid bounded inputs; this plan does not reopen them merely due to age. Their
numeric dimensions, pins, supplies and installed software are separate open claims.
