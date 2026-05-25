# V7 Phase 5 User Readiness Model

## Purpose

User readiness translates identity and runtime state into operator-friendly status.

## Required States

- connected;
- no_handshake;
- degraded;
- reconnecting;
- outdated_profile;
- routing_mismatch;
- onboarding_incomplete.

## Current Foundation

Current admin computes readiness from:

- registry enabled state;
- client artifacts;
- smart profile validation;
- route/leak check;
- desired state;
- WireGuard handshake;
- client agent;
- VLESS activity;
- profile delivery state.

## Mapping

connected:

- recent handshake, client agent, or VLESS activity exists and route is safe.

no_handshake:

- profile exists but no connection is seen.

degraded:

- route or service state is degraded but access is not fully blocked.

reconnecting:

- reconnect evidence exists or delivery was consumed recently.

outdated_profile:

- profile conflict, missing runtime identity, or older profile material.

routing_mismatch:

- desired state or route verification does not match policy.

onboarding_incomplete:

- missing base config, smart profile, delivery, or first connection.

## UX Rule

Show readiness as compact status and next action first.

Raw route, handshake, and profile details stay in drill-down.

