# Codex project guidance

## Current objective
Reconstruct and review LitterBuggy's existing physical V2 in this repository.
The owner confirms an Elegoo Uno R3. See docs/v2/README.md and the dated
docs/v2_verification/ record. New V2 source lives in hardware/v2 and software/v2.

## Priorities
1. System architecture, then power schematic, wiring, mechanical assembly,
   firmware and Pi logger, in the owner's requested review order.
2. Check evidence, create the draft, then inspect/test before the next stage.
3. Keep confirmed facts, conflicting claims, proposals and unknowns distinct.
4. Preserve original firmware and historical files. Do not infer old pins,
   measured dimensions, fuse ratings, calibration or passed field tests.

## Historical pipeline scope
The existing dataset/taxonomy/evaluation/dashboard and Jetson work remains in
its original paths. It does not override the owner's current V2 scope.

## Working Rules
- Keep scripts idempotent where possible.
- Write validation receipts to reports/v2; keep native engineering sources and
  intentional review exports beside their subsystem under hardware/v2.
- Keep raw field media/logs and private configs out of Git.
- Favor explicit JSON/YAML schemas over ad-hoc dicts.
- Do not add heavyweight dependencies without justification.
