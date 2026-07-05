# Controlled Source Degradation Owner Resolution

Timestamp: 2026-07-03T09:03:36+0700

Mode: Execution

Canonical authority:

`docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`

## Summary

Phase 4 MEDIUM_BATCH execution resumed from the current breakpoint:

`OWNER_RESOLUTION_REQUIRED_FOR_CONTROLLED_SOURCE_DEGRADATION`

Blocking Owner:

`v7-egress-guard` invoked by `v7-egress-set-state`

Owner Resolution terminal classification:

`POLICY_PROHIBITION`

No production mutation was performed.

No user was moved.

No Runtime, Planner, Authority, Restore Barrier owner, Wake owner, truth source, execution path, certification engine, automation framework, or architecture was created.

## Current Phase

`PHASE4_MEDIUM_BATCH_CERTIFICATION`

## Current Task

Run Owner Resolution for:

```text
v7-egress-set-state wireguard-1779454504-c43409 maintenance
  -> v7-egress-guard
  -> V7_EGRESS_GUARD=BLOCK
  -> reason=users_assigned
```

## Production Evidence

Read-only production host:

```text
host=v3119922.hosted-by-vdsina.ru
date=2026-07-03T05:02:55+03:00
```

Deployed owner tools:

```text
/usr/local/bin/v7-egress-guard
/usr/local/bin/v7-egress-set-state
98423fd446928e2867c1339fa3a556099fa74287e64eaeccf73b27dbd677f5fb  /usr/local/bin/v7-egress-guard
e578bdca30c50595b9f5abc714797e18b84bf358f040a72633771a6c9624f8a4  /usr/local/bin/v7-egress-set-state
```

The deployed hashes match the lineage records for the existing egress-lifecycle owners.

Assigned users on the controlled-production candidate source:

```text
ip=10.7.0.16 current=wireguard-1779454504-c43409 table=1014 enabled=1
ip=10.7.0.17 current=wireguard-1779454504-c43409 table=1015 enabled=1
ip=10.7.0.18 current=wireguard-1779454504-c43409 table=1016 enabled=1
ip=10.7.0.19 current=wireguard-1779454504-c43409 table=1017 enabled=1
ip=10.7.0.20 current=wireguard-1779454504-c43409 table=1018 enabled=1
ip=10.7.0.21 current=wireguard-1779454504-c43409 table=1019 enabled=1
ip=10.7.0.22 current=wireguard-1779454504-c43409 table=1020 enabled=1
ip=10.7.0.23 current=wireguard-1779454504-c43409 table=1021 enabled=1
ip=10.7.0.24 current=wireguard-1779454504-c43409 table=1022 enabled=1
ip=10.7.0.25 current=wireguard-1779454504-c43409 table=1023 enabled=1
ip=10.7.0.26 current=wireguard-1779454504-c43409 table=1024 enabled=1
```

Current real failed-source remaining users:

```text
ip=10.7.0.12 current=openvpn-1779388847-d2ad7c table=1010 enabled=1
ip=10.7.0.13 current=openvpn-1779388847-d2ad7c table=1011 enabled=1
ip=10.7.0.15 current=openvpn-1779388847-d2ad7c table=1013 enabled=1
```

No `certification`, `group`, or `pool` marker was present in `users.registry`.

## Owner Investigation

### v7-egress-guard

File:

`tools/runtime-support/v7-egress-guard`

Relevant behavior:

- reads `egress.registry`;
- reads `users.registry`;
- collects enabled users whose `current` equals the requested egress;
- returns `V7_EGRESS_GUARD=BLOCK reason=users_assigned` when any enabled user remains assigned.

The implementation has no certification-user exception, group check, pool check, or controlled-incident mode.

### v7-egress-set-state

File:

`tools/v7-egress-set-state`

Relevant behavior:

- supports `enabled`, `disabled`, and `maintenance`;
- before any non-enabled transition, invokes `v7-egress-guard`;
- if the guard exits non-zero, prints `ACTION=blocked` and exits before dry-run/apply continuation.

The implementation has no certification-aware path that can legally degrade a source with assigned users.

## Canonical Owner Evidence

Lineage owner:

`egress-lifecycle`

Lineage purpose for `v7-egress-guard`:

`Block disabling/maintenance when enabled users are still assigned to an egress.`

Admin lifecycle report:

`maintenance` and `disabled` are blocked if assigned users exist on that egress; this protects active users from being stranded by an admin click.

Controlled Production Certification Program Owner Mapping:

`Legal controlled source degradation procedure` remains mapped to existing observation / egress health / policy owners and is not currently implemented as a legal invocation path.

## Owner Resolution Decision

Question:

Why did this owner block?

Answer:

The owner blocked because enabled users remain assigned to the egress.

Is this expected policy?

`YES`

The block is intentional egress-lifecycle policy for the existing `v7-egress-set-state` path.

Is implementation missing?

For the existing admin lifecycle owner path:

`NO`

For the future controlled certification degradation path:

`YES, but not inside the current owner path without policy extension.`

Is owner invocation missing?

`NO`

The correct owner was invoked and it blocked according to its contract.

Is implementation defective?

`NO`

The owner behaved exactly as documented and deployed.

Is the behavior intentionally forbidden?

`YES`

Disabling or placing an egress into maintenance while enabled users remain assigned is intentionally forbidden by the current egress-lifecycle policy.

Is canonical impossibility proven?

`NO`

The architecture can still be extended through existing owners with a legal controlled source degradation / controlled incident materialization procedure.

## Terminal Classification

`POLICY_PROHIBITION`

## Exact Root Cause

The current existing owner path for opening a controlled failed-source incident attempts to use `v7-egress-set-state maintenance`, but that path is an admin egress-lifecycle mutation path whose safety owner, `v7-egress-guard`, intentionally forbids disabling or maintenance while enabled users remain assigned.

The production users on `wireguard-1779454504-c43409` are assigned and enabled, and `users.registry` has no certification-user / certification-group / certification-pool marker that could legally scope an exception to dedicated certification users.

Therefore the current controlled source degradation route is policy-prohibited.

## Required Resolution

Existing OMP / Authority / Production Maturity / egress-lifecycle owners must define and certify a legal controlled source degradation or controlled incident materialization path.

That future path must, at minimum:

- distinguish Certification Users from ordinary users through an existing user / group / policy owner;
- preserve Reality First;
- preserve `v7-egress-guard` for ordinary admin lifecycle mutations;
- avoid stranding ordinary users;
- open a real controlled incident through existing Observation / Wake / Incident owners;
- keep Authority, Restore Barrier, Runtime, Verification, Rollback, Learning, and Production Restoration unchanged.

Until that path exists, Phase 4 cannot legally open a controlled failed-source incident by using `v7-egress-set-state maintenance` on an egress with assigned users.

## Automation Debt Delta

Manual actions:

- read canonical program;
- read Current Program State;
- inspect local owner code and lineage records;
- run bounded read-only SSH commands;
- create Owner Resolution report;
- update Current Program State.

Classification:

`BLOCKED_BY_FUTURE_CAPABILITY`

Delta:

`created=1; closed=1; remaining_unclassified=0`

## Workflow Debt Delta

Manual workflow:

Owner Resolution required separate code, lineage, report, and production read-only checks.

Pipeline Candidate:

`CONTROLLED_CERTIFICATION_OWNER_RESOLUTION_PIPELINE`

Delta:

`created=1; closed=1; remaining_unclassified=0`

## Synchronization Debt Delta

Current Program State synchronized.

Passport / OMP / Production Maturity projection remains consumer synchronization work unless an existing safety owner requires it before the next owner-resolution task.

Delta:

`created=1; closed=0; remaining_non_safety=1`

## Owner Resolution Delta

`created=1; closed=1; terminal_classification=POLICY_PROHIBITION`

## Certification Infrastructure Delta

`POOL_SUFFICIENT_FOR_MEDIUM_BATCH`

The blocker is not user count. The blocker is legal controlled incident materialization.

## Terminal State

`HOLD`

## Capability Produced

`NONE`

## Current Capability State

`SMALL_BATCH_CERTIFIED`

## Next Engineering Task

`CONTROLLED_SOURCE_DEGRADATION_POLICY_EXTENSION_OR_CONTROLLED_INCIDENT_MATERIALIZATION`

## Final Result

Current Phase:

`PHASE4_MEDIUM_BATCH_CERTIFICATION`

Terminal State:

`HOLD`

Exact Root Cause:

`CURRENT_EGRESS_LIFECYCLE_POLICY_PROHIBITS_MAINTENANCE_OR_DISABLED_WITH_ASSIGNED_USERS`

Responsible Existing Owner:

`v7-egress-guard` / `v7-egress-set-state` / OMP / Authority / Production Maturity

Owner Resolution Classification:

`POLICY_PROHIBITION`

Required Resolution:

Define and certify a legal controlled source degradation / controlled incident materialization path through existing owners.

Next Phase:

`PHASE4_CONTROLLED_SOURCE_DEGRADATION_POLICY_EXTENSION_OR_CONTROLLED_INCIDENT_MATERIALIZATION`
