---
name: Configuration-specific validation record
about: Plan or record replay, bench or field evidence without mixing generations
title: "Validation record: "
labels: validation
---

## Identity and mode

- Planned / performed:
- Mode: offline replay / software artifact check / physical bench / field:
- Configuration ID, source commit and actual hardware identity if physical:
- Run ID / date / reviewer or operator:
- Method, conditions, load/route if applicable:
- Acceptance rule: proposed / adopted for this configuration / not yet agreed:

## Evidence and result

- Original raw archive ID/hash (keep private media/paths outside Git):
- Actual result with units, denominator and missing/failure detail:
- Status of claim: confirmed / conflicting / proposed / unknown:
- Current V2, if used: manifest.json, config_snapshot.yml, serial.raw, run.sqlite3:
- Legacy V1A, if used: identify legacy files/contract explicitly:
- Video/capture metadata and usability review, if performed:
- Valid frames versus non-null physical sample counts, if relevant:
- Remaining uncertainty / affected source corrections:

## Evidence boundaries

- [ ] Replay/default null rows are not counted as physical measurements
- [ ] Counts, CPU temperature and sequence events are not rail/reset proof
- [ ] Actual control arrangement is recorded; no new software motion path is implied
- [ ] No passed field gate is inferred from compile/file validity or an example CSV
- [ ] Raw evidence remains outside Git; supporting bounded references are provided

Reference: [current evidence plan](https://github.com/Rob803yy/Junk-O-Matic/blob/main/docs/v2/verification-plan.md).
