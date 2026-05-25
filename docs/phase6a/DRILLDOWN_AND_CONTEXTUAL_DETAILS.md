# V7 Phase 6A Drill-Down and Contextual Details

## Purpose

Detailed diagnostics should appear in the context of a specific operator question.

## Context Examples

Degraded channel:

- summary: channel is degraded;
- details: affected services/users;
- diagnostics: service matrix and route tests;
- telemetry: command output and raw state.

Trusted RU issue:

- summary: trusted RU unavailable or temporary;
- details: policy blockers and route class state;
- diagnostics: service checks and selected egress;
- telemetry: per-domain probe output.

User reconnect issue:

- summary: user is reconnecting;
- details: profile/device/routing status;
- diagnostics: route reality and client signals;
- telemetry: recent events.

## Rule

Details without context create cognitive load. Every technical detail should answer a question the operator has just asked.

