# Codex project guidance

## Objective
Build a local-first data and evaluation pipeline for Junk-O-Matic.

## Priorities
1. Public dataset bootstrap and normalization
2. Stable taxonomy and manifests
3. Reliable evaluation artifacts for dashboard consumption
4. Jetson deployment readiness after local metrics stabilize

## Working Rules
- Keep scripts idempotent where possible.
- Write outputs to `reports/` and `data/processed/`.
- Favor explicit JSON/YAML schemas over ad-hoc dicts.
- Do not add heavyweight dependencies without justification.
