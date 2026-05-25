# Canary Integrity Gates

These gates decide whether a future one-user canary can proceed. Current status remains NO-GO.

## HARD FAIL

Any of these blocks canary:

- `v7-killswitch-check` is not OK.
- `v7-user-route-check` is not OK.
- `v7-provisioning-reconcile-check` is not OK.
- route table for the candidate user is missing or points to the wrong egress.
- candidate user's `ip rule` is missing in stable `ip -4 rule show`.
- autoswitch can run `--apply` during the canary window.
- `v7-reconcile-check` FAIL is unexplained.
- target egress is disabled, missing an interface, overloaded, or below quality floor without waiver.
- rollback command or rollback verification is unclear.
- the plan requires `v7-routing-sync` as first live mutation.

## CONDITIONAL WAIVER

Waivers must be explicit and one-user scoped:

- Reconcile FAIL waiver: allowed only if stable `ip rule show`, route table, route-get, user-route-check, kill-switch-check, and provisioning reconcile all pass for the candidate.
- Target quality waiver: allowed only for routing-mechanics canary, not user-experience migration.
- Trusted RU stale waiver: allowed only if the candidate route path does not touch Trusted RU/Gosuslugi-sensitive logic.
- Anti-flap waiver: allowed only with autoswitch held.

## SAFE ENOUGH FOR ONE-USER CANARY

Safe enough requires all:

- autoswitch authority held;
- candidate user stable;
- candidate rule and table verified immediately before execution;
- target egress acceptable or explicitly waived;
- rollback preview and command ready;
- kill switch and route checks OK;
- operator approval names exactly one user and one target egress.

## Current Status

```text
NO-GO
```

Reason: autoswitch authority is still active and reconcile FAIL remains unexplained under a quiet control-plane window.
