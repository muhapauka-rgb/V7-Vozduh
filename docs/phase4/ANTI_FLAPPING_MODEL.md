# V7 Phase 4 Anti-Flapping Model

## Purpose

Anti-flapping protects users from unstable routing churn. A slightly worse stable path is preferred over repeated movement between channels.

## Required Controls

Autoswitch must use these controls together:

- cooldown after a user move;
- target block after failed verification;
- user freeze after repeated unstable moves;
- egress quarantine after repeated failures;
- bounded move count per run;
- degradation persistence thresholds;
- minimum score improvement and minimum absolute score delta;
- load and capacity gates;
- recovery verification windows.

## Flapping Signals

The system should treat these as instability signals:

- repeated switches for the same user;
- failed post-switch verification;
- reconnect loops after a move;
- target egress repeatedly rejected;
- service quality oscillation;
- alternate path becoming degraded immediately after selection.

## Safety Response

When flapping risk is detected, autoswitch should prefer:

- freezing the affected user;
- blocking the failed target for that user;
- reducing planned moves;
- quarantining unstable egress after repeated verified failures;
- surfacing an operator-visible warning.

## Recovery Rule

Recovery must be slower than failover.

Users should not be moved back immediately after an egress looks healthy. The egress must pass a stability window first.

## Operator Summary

Operator UX should summarize anti-flap state as:

- users frozen;
- targets blocked;
- egress quarantined;
- cooldown active;
- last switch reason;
- next safe action.

It must not expose a giant raw scoring matrix on the main screen.

