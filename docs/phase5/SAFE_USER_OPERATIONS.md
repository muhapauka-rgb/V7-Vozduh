# V7 Phase 5 Safe User Operations

## Purpose

User operations can affect access. They must be bounded, audited, and reversible where possible.

## Dangerous Operations

Dangerous identity operations include:

- issue device;
- quick issue config;
- create pending profile;
- revoke device;
- delete user/runtime assignment;
- rotate profile;
- suspend user;
- lower device limit below active devices;
- update org policy.

## Required Controls

Dangerous operations must include:

- actor;
- reason or workflow context;
- before state;
- after state;
- affected users/devices;
- runtime result;
- rollback context when files/runtime were changed.

## Current Foundation

Current code already has:

- safe mode guard;
- dry-run paths for issue flows;
- explicit confirms such as `REVOKE_DEVICE`, `DELETE_USER`, `LOWER_DEVICE_LIMIT`;
- audit entries;
- delivery revocation on device revoke;
- backup creation for registry line removal.

## Gap To Formalize

Runtime consistency should be checked after identity mutation:

- active device has registry row;
- revoked device has no active registry row;
- profile delivery links match current device state;
- pending profile expiration is not stale.

## Operator UX

Operator action views should show:

- what will change;
- who is affected;
- whether profile delivery links will be revoked;
- whether runtime access will be disabled;
- rollback availability.

