> REPO-R1 review 2026-11-22: Historical target list only. These V1.0A-to-V1.0B/V1.5 gates have not been adopted or passed for current V2. Filename/version labels are retained for traceability; required evidence and thresholds must be reviewed for the actual configuration.
> Use the [current V2 evidence plan](../../../docs/v2/verification-plan.md) and [current engineering index](../../../docs/v2/README.md).

# V1.0A to V1.0B/V1.5 Exit Criteria

V1.0A must remain an instrumented RC platform until evidence shows that data collection is reliable and does not affect vehicle control.

## Required Gates

- 10/10 clean Pi boot and logger starts
- At least 95% usable camera video across validation runs
- At least 95% expected Arduino telemetry rows across validation runs
- No Pi resets across 5 field sessions
- 5V rail remains stable under expected loads
- 12V rail remains stable under expected loads
- Run manifest exists for 100% of runs
- Summary CSV generated for 100% of runs
- 5 x 45-minute field sessions completed
- Operator event markers used successfully
- Every test links to an evidence folder

## Review Before Expanding Scope

Before adding auxiliary actuators, assisted perception, or any control-adjacent behavior:

- Review all `CONTROL_SURPRISE`, `BATTERY_CONCERN`, `FAULT_OBSERVED`, and `MECHANICAL_ISSUE` markers.
- Confirm no control anomaly correlates with auxiliary electronics load.
- Confirm raw evidence storage and scorecard import process are reliable.
- Document the next-stage hazard analysis and wiring changes.

## Still Not Allowed Without New Scope Approval

- Pi-to-ESC control
- Pi-to-steering control
- Computer driving
- Autonomous route following
- Relay handoff between RC and computer control
