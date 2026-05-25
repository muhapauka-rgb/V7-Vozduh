# V7 Phase 6 Safe Action UX

## Purpose

Dangerous actions must be safe to understand before they are safe to execute.

## Required Preview

Dangerous actions should show:

- action type;
- affected users/devices/channels;
- policy impact;
- runtime impact;
- rollback availability;
- required confirmation;
- audit actor.

## Required Backend Controls

Frontend must never bypass:

- role check;
- CSRF;
- safe mode;
- backend validation;
- audit logging;
- explicit confirm token.

## Current Foundation

Current admin already has:

- `ACTION_MIN_ROLE`;
- `GET_MIN_ROLE`;
- `SAFE_MODE_BLOCKED_ACTIONS`;
- explicit confirms like `REVOKE_DEVICE`, `DELETE_USER`, `AUTOSWITCH`, `SAVE_ORG_POLICY`;
- preview endpoints for many dangerous operations.

## Future Component Contract

Safe action components should be built around:

- preview;
- apply;
- result;
- rollback context;
- event link.

