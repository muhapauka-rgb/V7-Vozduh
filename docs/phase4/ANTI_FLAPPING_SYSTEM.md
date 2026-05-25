# V7 Phase 4 - Anti-Flapping System

## Purpose

Autoswitch must not oscillate users or chase transient changes.

Anti-flapping is a safety foundation, not a tuning nicety.

## Required Controls

Controls:

- cooldown per user;
- freeze periods after repeated moves;
- blocked target memory;
- egress quarantine after failed verification;
- bounded moves per run;
- degradation persistence thresholds;
- switch confidence thresholds;
- projected target load checks.

## Current Controls

Current autoswitch already has:

- `cooldown_seconds`;
- `user_freeze_switches_1h`;
- `user_freeze_switches_24h`;
- `target_block_seconds`;
- `egress_quarantine_failed_verifications_1h`;
- `autoswitch_max_planned_per_run`;
- `autoswitch_max_failover_per_run`;
- `autoswitch_max_reconnect_per_run`;
- projected load target adjustment.

## Guardrail Defaults

Recommended safe defaults:

- planned moves: `1`;
- cooldown: at least `180s`;
- reconnect rotation cooldown: at least `180s`;
- freeze after repeated moves;
- failover moves bounded by capacity;
- no automatic move to quarantined/maintenance/manual-only egress.

## Operator Summary

Show:

- users frozen;
- egress quarantined;
- selected moves;
- blocked by cooldown;
- confidence.

Do not show the full scoring matrix by default.
