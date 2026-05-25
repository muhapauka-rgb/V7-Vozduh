# User Switch Governance

This document is static governance only. `v7-user-switch` was read for analysis but not executed.

## Role

`v7-user-switch` moves one user IP to a target egress. It both changes live routing for that user's table and updates persistent assignment state.

## Inputs

```text
v7-user-switch <user_ip> <egress-id>
```

It validates:

- user IP shape through `v7_safe_ip`;
- egress ID through `v7_safe_id`;
- user row exists in `/opt/v7/egress/state/users.registry`;
- target egress exists and is enabled;
- target egress has an interface;
- user table is numeric.

## Reads

```text
/opt/v7/egress/state/users.registry
/usr/local/lib/v7-egress-lib
egress registry through v7_egress_exists / v7_egress_enabled / v7_egress_interface
node environment through v7_load_node_env when available
```

## Writes / Mutates

```text
ip route replace default dev <target-dev> table <user-table>
/opt/v7/egress/state/user-<ip>.assign
/opt/v7/egress/state/users.registry via temp file + mv
audit event through v7-audit-log when available
switch history through v7-switch-log when available
```

It then reads route evidence through:

```text
ip route get 8.8.8.8 from <user-ip> iif wg0
```

## Live Routing Boundary

The live route changes before the registry rewrite. That means partial failure after route replacement but before registry update is possible in principle. Future wrapper execution needs pre/post checks and a rollback target.

## Rollback

Rollback is conceptually available by switching the same user back to the previous egress:

```text
v7-user-switch <user_ip> <previous_egress>
```

This is not a passive rollback. It is another live mutation and must pass the same checks.

## Minimum Safe Blast Radius

The smallest safe blast radius is one user, one target egress, one explicit reason, with:

1. Generate `tools/v7-route-movement-preview user-switch ...`.
2. Confirm preview has `mutation=false` and no `errors`.
3. Pre-check target egress enabled and healthy.
4. Pre-check kill switch OK.
5. Switch one user only after separate approval.
6. Post-check route table for that user.
7. Post-check kill switch and leak guard.
8. Roll back to previous egress if route verification fails.

`v7-user-switch` can be the first canary mutation only after route movement preview tests pass and the one-user canary readiness checklist is satisfied.

## Forbidden Without Separate Approval

- Manual switch of multiple users.
- Switch into unverified or overloaded egress.
- Switch driven only by stale health/Trusted RU state.
- Switch without a known previous egress.
- Switch without a preview JSON artifact.
