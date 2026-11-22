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
The owner requested separation of historical data from current work. Older
V1A and dataset/model scaffold material now lives under archive/. Use
docs/repository-layout.md and archive/relocation-manifest.json to resolve old
paths in dated evidence. Do not promote archived constants, sample metrics or
old wiring assumptions into current V2 facts. Current working sources remain
in hardware/v2, software/v2 and docs/v2; deployment is still unverified.

## Working Rules
- Keep scripts idempotent where possible.
- Write validation receipts to reports/v2; keep native engineering sources and
  intentional review exports beside their subsystem under hardware/v2.
- Keep raw field media/logs and private configs out of Git.
- Favor explicit JSON/YAML schemas over ad-hoc dicts.
- Do not add heavyweight dependencies without justification.
