# One-User Canary Readiness

One-user canary is the first allowed live movement pattern, but it is not approved by this document. This is the readiness checklist for a future separately approved run.

## Required Before Canary

- Route movement preview exists and has `mutation=false`.
- Preview has no `errors`.
- Current user assignment captured.
- Previous egress captured.
- Target egress exists, is enabled, has an interface, and is not at hard capacity.
- `v7-killswitch-check` is OK.
- `v7-user-route-check` is OK.
- Provisioning reconcile check is OK.
- Autoswitch timer authority is understood.
- No autoswitch storm is active.
- Affected user is explicitly named.
- Blast radius is exactly one user.
- Rollback command is prepared.

## Pre-Check Evidence

Required evidence packet:

```text
user_ip
from_egress
to_egress
route_table
target_interface
preview_json_sha256
kill_switch_status
user_route_check_status
rollback_command
operator approval
```

## Post-Checks

- User route table changed as expected.
- User traffic path uses target interface.
- `users.registry` assignment is expected.
- `user-<ip>.assign` is expected.
- Switch log entry exists.
- Audit entry exists if audit logger is available.
- `v7-killswitch-check` remains OK.
- `v7-user-route-check` remains OK.
- No route leak is detected.

## Rollback

Rollback must be exact:

```text
v7-user-switch <user_ip> <previous_egress>
```

Rollback is also mutation. It needs the same post-checks as the forward switch.

## Stop Conditions

Stop and do not apply broader movement if:

- preview has errors;
- kill switch check fails;
- route check fails;
- target egress is missing/disabled/full;
- Trusted RU state is stale but relevant to the route class;
- autoswitch is concurrently moving users;
- rollback command is not known;
- previous egress cannot be verified.

