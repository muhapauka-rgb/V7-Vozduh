# V7 Phase 7 Failure Domain Isolation

## Purpose

Failure in one domain must not destabilize the whole platform.

## Failure Domains

Egress:

- one channel degraded, blocked, overloaded, or quarantined.

Organization:

- one org policy, onboarding group, or profile cohort affected.

Transport:

- one driver family affected, such as OpenVPN, AWG, VLESS, or sing-box.

Service class:

- Telegram, video, DNS, HTTPS, trusted RU, or global traffic degraded.

Runtime component:

- admin API, autoswitch, sentinel, service matrix, quality compaction, systemd unit.

## Isolation Rules

- one egress failure should produce quarantine or local migration, not global churn;
- one org issue should not expose or affect another org;
- one service degradation should not imply full reroute unless user impact and confidence justify it;
- one transport driver issue should not invalidate unrelated drivers;
- diagnostics failure should not disable core routing.

## Operator Summary

Failure reports should show:

- domain;
- affected scope;
- blocked actions;
- safe next action;
- rollback availability.

