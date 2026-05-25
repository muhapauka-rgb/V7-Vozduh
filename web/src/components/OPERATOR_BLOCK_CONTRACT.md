# V7 Operator Block Contract

## Purpose

Reusable operator blocks must preserve Phase 6A information architecture.

## Required Structure

Summary:

- status;
- impact;
- reason;
- urgency;
- next safe action.

Details:

- affected objects;
- grouped diagnostic reason;
- confidence or verification state;
- drill-down link.

Deep diagnostics:

- telemetry;
- command result;
- route reality;
- raw state.

## Rules

- Summary is visible by default.
- Details require expand or navigation.
- Deep diagnostics require explicit operator intent.
- Dangerous actions must show preview, impact, and rollback context.
- A block that starts with a raw table violates Phase 6A.

