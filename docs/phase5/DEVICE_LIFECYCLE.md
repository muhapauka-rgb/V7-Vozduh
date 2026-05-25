# V7 Phase 5 Device Lifecycle

## Purpose

A device is the concrete access unit for a user. Device lifecycle is separate from user lifecycle.

## Target States

- active;
- stale;
- reconnecting;
- suspicious;
- revoked;
- archived.

## Current Foundation

Current SQLite `devices` stores:

- user id;
- device name/type;
- VPN client;
- public key;
- assigned VPN IP;
- route table;
- config version;
- status;
- last seen/revoked timestamps.

## State Meanings

active:

- device is allowed and should have matching runtime access.

stale:

- device has not been seen recently or has old profile material.

reconnecting:

- device is expected to reconnect and should not be treated as permanently broken.

suspicious:

- bounded anomaly was detected, such as repeated failed reconnect or unexpected profile conflict.

revoked:

- device access must be disabled and delivery links revoked.

archived:

- retained history only; no active profile or runtime row should exist.

## Trust Foundation

Device trust may use:

- assigned VPN IP;
- public key;
- profile delivery history;
- reconnect summary;
- profile version;
- operator notes.

It must not use invasive tracking or content inspection.

## Consistency Rules

- Active device should have a valid assigned VPN IP.
- Revoked device must not have an active registry row.
- Duplicate active devices must not share the same assigned VPN IP.
- Delivery links for revoked devices should be revoked or expired.

