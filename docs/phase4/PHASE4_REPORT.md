# V7 Phase 4 Report

## Scope

Phase 4 inspected autoswitch as a self-healing routing layer and added only non-invasive governance artifacts plus a read-only review helper.

No routing behavior, nftables behavior, provisioning behavior, systemd units, or autoswitch runtime logic was changed.

## Current Autoswitch Strengths

The current `tools/v7-users-autoswitch` already contains important safety foundations:

- dry-run by default and guarded apply mode;
- route-class-aware candidate filtering;
- Telegram/service-aware scoring support;
- organization policy support;
- cooldown and freeze logic;
- bounded planned, failover, and reconnect move limits;
- target blocking after failed verification;
- egress quarantine after repeated failures;
- rejected candidate explanations;
- confidence labels;
- post-switch verification and rollback path.

## Main Weak Points

### Dry-run is not completely read-only

`v7-users-autoswitch --pretty` can update reconnect observation state because reconnect events are observed during planner initialization.

This is not a datapath mutation, but it is still a runtime state write. Operator endpoints that call dry-run should treat it as low-risk stateful observation, not a pure read-only command.

### Confidence is present but not yet a formal contract

Current output includes confidence, but Phase 4 formalizes the required meaning and minimum explanation contract.

### Historical and regional awareness are foundations only

Current logic reads several quality and service signals, but long-term regional/operator intelligence should remain future foundation work unless explicitly requested later.

## Added Artifacts

- `AUTOSWITCH_DECISION_MODEL.md`
- `ANTI_FLAPPING_MODEL.md`
- `DEGRADATION_PERSISTENCE.md`
- `SERVICE_ROUTE_CLASS_SWITCHING.md`
- `CLIENT_EXPERIENCE_AWARENESS.md`
- `CONFIDENCE_AND_BOUNDED_MIGRATION.md`
- `GRACEFUL_RECOVERY_AND_REPAIR_HOOKS.md`
- `ADAPTIVE_STEALTH_FOUNDATION.md`
- `REGIONAL_AND_HISTORICAL_FOUNDATION.md`
- `AUTOSWITCH_AUDIT_AND_UX.md`

## Added Tool

`tools/v7-autoswitch-safety-review` is a read-only preflight review helper.

It reads autoswitch-adjacent state and reports:

- policy bounds;
- anti-flap state;
- service awareness state;
- route-class awareness state;
- client experience signals;
- bounded migration constraints;
- historical reliability hints;
- dry-run safety notes.

It does not call `v7-users-autoswitch` and does not write state.

## Phase Boundary

Phase 4 did not start Phase 5.

Identity, onboarding, commercial multi-tenant behavior, and admin platform restructuring remain out of scope until a separate command.

