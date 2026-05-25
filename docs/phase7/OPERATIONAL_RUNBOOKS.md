# V7 Phase 7 Operational Runbooks

## Purpose

Operators should not depend on memory during incidents.

## Degraded Channel

1. Open channel summary.
2. Check affected users/orgs.
3. Verify service matrix and route class impact.
4. If persistent, move to maintenance or quarantine through guarded workflow.
5. Confirm alternate capacity before migration.
6. Verify after action.

## Platform Outage

1. Preserve logs and state snapshot.
2. Check admin API, systemd timers, and required commands.
3. Run read-only validators.
4. Verify kill switch.
5. Avoid provisioning or autoswitch apply until state is verified.

## Backup Restore

1. Create before-restore snapshot.
2. Verify backup integrity.
3. Preview affected files/users/egress.
4. Restore into safe posture.
5. Run contract/lifecycle/reconcile/killswitch checks.
6. Exit safe posture only after verification.

## Upgrade Failure

1. Keep safe mode enabled.
2. Preserve failed version state.
3. Run compatibility and contract checks.
4. Roll back if post-upgrade verification fails.
5. Document actor, reason, and affected scope.

## Resource Pressure

1. Identify pressure family: CPU, RAM, disk, conntrack, nftables, routes, file descriptors, bandwidth.
2. Check affected workflows.
3. Avoid increasing probe frequency.
4. Prefer grouping, throttling, maintenance, or quarantine.
5. Do not hide degraded state.

