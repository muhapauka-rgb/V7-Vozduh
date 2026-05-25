# V7 Phase 4 - Graceful Recovery Model

## Purpose

Recovery must not create oscillation.

When a degraded egress recovers, users should not immediately bounce back.

## Recovery Rules

- require stability window before healthy;
- keep current stable routes unless there is strong reason;
- remove quarantine only after verification;
- keep user freeze/cooldown semantics;
- avoid automatic "return to preferred" behavior;
- prefer operator-visible recommendation over immediate move-back.

## Recovery States

- recovering;
- verified stable;
- eligible;
- production preferred.

## Suggested Evidence

- service matrix OK over time;
- quality trend improving;
- fail rate low;
- no reconnect spikes;
- kill switch/reconcile OK;
- target capacity safe.
