# E25.4 First Movement Safety Review

## Question

Is a dedicated execution target now safer than `wireguard-1779454504-c43409`?

## Answer

`dedicated_target_safer_than_original=false`

Reason: no dedicated execution target has been created yet.

## Existing WireGuard Target

The existing WireGuard target remains the best existing candidate, but only conditionally:

- zero-user: true
- reservation metadata: present
- diagnose/load: can be OK
- quality: spiky
- E25.2 execution-time NO-GO: true
- E25.3 long-window recovery: true

This is not production-clean enough for the first governed movement if a dedicated egress can be provisioned.

## First Movement Verdict

`first_movement_now_safe=false`

Reason:

- no dedicated execution-only target exists;
- the existing target is known to oscillate;
- first movement should not depend on a spiky target.

## Required To Become Safe

One of:

1. Provision and validate a dedicated execution-only target.
2. Accept a conditional retry using current WireGuard only after a fresh sustained GO window and immediate execution-time GO.

Preferred path:

`E25_5_DEDICATED_EXECUTION_EGRESS_PROVISIONING_AND_VALIDATION`
