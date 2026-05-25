# V7 Phase 2 - Registry And Runtime Reconciliation

## Purpose

Provisioning must detect registry/runtime drift before enabling, disabling, maintenance, or rollback actions.

## Mismatch Categories

- `REGISTRY_ENABLED_RUNTIME_DEAD`
- `RUNTIME_ALIVE_REGISTRY_DISABLED`
- `RUNTIME_ALIVE_REGISTRY_MAINTENANCE`
- `STALE_INTERFACE`
- `STALE_ROUTE`
- `STALE_NFT_ENTRY`
- `STALE_RUNTIME_PROFILE`
- `PROFILE_DIFFERS_FROM_DRAFT`
- `FLAGS_STATE_MISMATCH`
- `DRAFT_METADATA_REGISTRY_MISMATCH`
- `HEALTH_STATE_STALE`
- `USERS_ON_DISABLED_EGRESS`
- `USERS_ON_MAINTENANCE_EGRESS`

## Existing Checks

Current safe checks:

- `hardening/v7-provisioning-reconcile-check`;
- `hardening/v7-killswitch-check`;
- `tools/v7-runtime-contract-validate`;
- `tools/v7-egress-lifecycle-validate`.

## Repair Policy

Repair must be:

- bounded;
- explicit;
- audited;
- followed by verification.

Forbidden:

- silently editing registry because interface exists;
- silently killing interface because registry is disabled;
- silently rebuilding nftables without reason/audit;
- silently moving users off an egress.

## Operator Summary

Show:

- mismatch count;
- highest severity;
- impacted users;
- safe suggested action.

Drill-down:

- exact registry row;
- exact interface/profile;
- evidence source;
- rollback context.
