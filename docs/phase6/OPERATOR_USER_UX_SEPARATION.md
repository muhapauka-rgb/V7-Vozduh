# V7 Phase 6 Operator/User UX Separation

## Purpose

Operator UX and user UX are separate products.

## Operator UX

Operator sees:

- platform health;
- affected users;
- incidents;
- policy;
- safe actions;
- diagnostics.

## User UX

User sees:

- connect;
- import profile;
- reconnect;
- restore access.

User must not see:

- route classes;
- egress;
- transport selection;
- diagnostic metrics;
- kill switch internals.

## Current Foundation

Current code already separates:

- `/admin-v2` for operators;
- `/connect` and profile delivery/import pages for users.

Future frontend extraction must preserve this separation.

