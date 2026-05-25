# V7 Phase 3 - Route Diagnostics Engine

## Purpose

Route diagnostics must answer why a path is degraded, not merely report that it is degraded.

## Required Questions

Diagnostics must explain:

- why traffic is slow;
- why health is degraded;
- why autoswitch did not act;
- why direct routing is broken;
- why trusted RU is unavailable;
- why path is unstable;
- why Telegram is degraded;
- why a client is reconnecting.

## Diagnostic Inputs

Inputs:

- desired registry and policy;
- effective route checks;
- kill switch checks;
- provisioning reconcile checks;
- service matrix;
- Telegram sentinel;
- egress quality summary;
- path benchmark;
- path samples;
- autoswitch plan/safety state;
- direct/RU diagnostics;
- client reconnect state;
- audit events.

## Cause Groups

Use grouped causes:

- Routing;
- Channels;
- Services;
- Users;
- Trusted RU;
- Autoswitch;
- Provisioning;
- Security;
- Direct routing.

## Diagnostic Output

Each diagnosis should include:

- category;
- severity;
- affected object;
- probable cause;
- evidence;
- suggested action;
- whether action is safe, risky, or manual;
- verification state.

## Forbidden Output

Do not show:

- wall of raw command output;
- unrelated metrics;
- unexplained "switched" or "failed";
- black-box recommendations.

## Phase 3 Boundary

This is a diagnostic contract. It does not change datapath or autoswitch behavior.
