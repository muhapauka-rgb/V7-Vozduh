# V7 Phase 37: Subnet expansion preview

Date: 2026-05-07

## Goal

Prepare a safe maintenance path from the current `10.0.0.0/24` user network to
`10.0.0.0/23`, without changing the live network yet.

This is needed because the current `/24` supports only about 253 clients, while
the target scale is 500 users.

## Added

### `/usr/local/bin/v7-subnet-expand-preview`

Read-only tool that prints:

- Current `wg0` address and NAT rules.
- Proposed `/23` target network.
- Files that must change.
- Required maintenance order.
- Required validation commands.
- Rollback order.

## Validation

Command run:

```bash
v7-subnet-expand-preview 23
```

Result:

- Preview generated successfully.
- Current network detected as `10.0.0.1/24`.
- Target network shown as `10.0.0.0/23`.
- No live network settings were changed.

## Why This Is Deferred

Actual subnet expansion affects:

- `wg0`.
- NAT.
- kill switch.
- user provisioning allocator.
- admin validation.
- live client testing.

This should be applied during a maintenance step after explicit confirmation.
