---
name: Hardware verification or correction
about: Record a bounded component/interface finding against an identified configuration
title: "Hardware review: "
labels: hardware
---

## Configuration and claim

- Configuration ID / source revision (current draft CFG-V2-R1, or identify legacy):
- Component / net / drawing ID:
- Specific claim or required value, with units:
- Status: confirmed / conflicting / proposed / unknown:
- Severity and observed consequence (do not infer a physical fault from a TODO):

## Evidence

- Photo/label/continuity/measurement/source reference, date and hash where useful:
- Connector view / datum / method / conditions:
- What this evidence establishes, and what remains unverified:
- Proposed source correction and affected diagrams/BOM/code:

## Scope check

- [ ] Board identity is separate from pins, power entry and installed software
- [ ] Source/catalog ratings and proposed values are not recorded as measurements
- [ ] No unverified polarity, fuse rating, dimension or common ground is assumed
- [ ] No new Pi/Uno vehicle-control interface is implied
- [ ] Private raw media/configs stay outside Git; bounded evidence reference supplied

Reference: [V2 evidence plan](https://github.com/Rob803yy/Junk-O-Matic/blob/main/docs/v2/verification-plan.md).
