# V7 Phase 5 Device Trust Foundation

## Purpose

Device trust helps the operator understand whether a profile/device is expected, stale, or suspicious.

This is not invasive surveillance.

## Allowed Signals

Allowed trust signals:

- device status;
- assigned VPN IP;
- public key;
- last seen timestamp;
- reconnect summary;
- profile delivery history;
- profile version;
- active runtime registry row;
- operator notes.

## Suspicious Conditions

Examples:

- revoked device still active in registry;
- duplicate active devices share one VPN IP;
- active delivery link exists for revoked device;
- profile delivery consumed but no connection ever appears;
- repeated reconnect failures after profile rotation.

## Bounded Response

The system may:

- warn operator;
- suggest revoke/rotate/reconnect;
- mark device stale or suspicious in future;
- block automatic risky actions.

The system must not silently revoke or reroute users without explicit policy and audit.

