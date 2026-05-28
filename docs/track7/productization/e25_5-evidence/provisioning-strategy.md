# E25.5 Provisioning Strategy

## Decision

`CREATE_DEDICATED_WIREGUARD_EXECUTION_TARGET`

Status:

`NO_WORKING_PROFILE`

## Reasoning

WireGuard remains the preferred protocol for a dedicated execution-only egress:

- readiness helper already supports WireGuard handshake-based diagnose;
- interface state and counters are observable;
- route behavior is predictable for one-user movement and rollback;
- governance reservation semantics have already been proven around WireGuard.

However, E25.5 did not find a spare, safe, ready-to-import outbound WireGuard execution profile.

## Discovery Findings

Existing active WireGuard egress:

- `wireguard-1779454504-c43409`
- interface `v7e06a394c478`
- already in `egress.registry`
- duplicate of draft `wg-1779455931-ba621c`
- known spiky from E25.2/E25.3

Draft `wg-1779455931-ba621c`:

- import pipeline status: `UPDATED_EXISTING`
- duplicate of `wireguard-1779454504-c43409`
- runtime profile path: `/etc/wireguard/v7e06a394c478.conf`
- not a new target

OpenVPN drafts:

- some are draft-only;
- one recent draft had runtime status `FAIL`;
- current active OpenVPN has diagnose `SUSPECT`.

Test profiles:

- `/etc/wireguard/wg-client-test.conf` is an inbound/server test profile with route hooks.
- `/etc/amnezia/amneziawg/awg-client-test.conf` is an inbound/server test profile with route/nft hooks.
- `/etc/wireguard/vps.conf` is a raw WireGuard client-like profile, but it is not V7-normalized, has `AllowedIPs=0.0.0.0/0`, and is unsafe to launch as-is because it could alter routing.

## Conclusion

No safe dedicated execution-only target can be created from current inventory without a separate provisioning operation that supplies or validates a real outbound profile and V7-normalized runtime wrapper.

No thresholds were weakened. No fake egress row was created.
