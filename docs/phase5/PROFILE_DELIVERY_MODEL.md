# V7 Phase 5 Safe Profile Delivery Model

## Purpose

Profile delivery must be safe, low-friction, and auditable.

The user should import a profile and connect. The user should not choose transports, route classes, or egress manually.

## Current Foundation

Current platform supports:

- smart profile generation;
- one-time profile delivery tokens;
- import/download QR links;
- TTL and expiry;
- consumed-token tombstones;
- delivery revocation;
- public gateway path allowlist.

## Delivery Contract

Every profile delivery should include:

- target IP/device;
- adapter and mode;
- created timestamp;
- expiration timestamp;
- creator actor;
- delivery id;
- consumed/downloaded timestamp;
- revoke timestamp when revoked.

## Safety Rules

Profile delivery must:

- expire;
- be one-time or explicitly bounded;
- avoid exposing profile paths after consumption;
- be revocable;
- be tied to device/user context when available;
- be audited when created or revoked.

## Rotation And Revocation

Profile rotation should:

- create new profile material;
- revoke active delivery links for old material;
- preserve previous assignment context;
- avoid silent user migration.

Device revoke should:

- disable runtime access;
- mark device revoked;
- revoke active delivery links;
- retain audit history.

## Public Gateway

Public delivery surface must remain narrow:

- `/connect`;
- `/api/connect/start`;
- `/api/connect/status`;
- profile delivery/import QR endpoints;
- token-scoped profile delivery/import endpoints.

No admin endpoints should be exposed through the public gateway.

