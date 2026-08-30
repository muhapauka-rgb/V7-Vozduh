# V7 Core-primary stable route-class repair and live 7-second recovery

Discover → Reuse → Extend → Implement.

Continue OMP.

Mission: `V7_CORE_PRIMARY_STABLE_ROUTE_CLASS_REPAIR_AND_LIVE_7S_RECOVERY`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

This is a bounded repair of the existing Core-primary routing owner. It is not
a new routing system, allocator, registry, route writer, Matrix, Planner,
queue, timer, Runtime or Authority.

## Preconditions: current truth, not historical assertion

Before modifying code, read fresh CPS, OMP, Matrix, the Runtime receipt,
`users.registry`, `egress.registry`, current Core-primary/nft/policy state and
the active Candidate/Packet/Lease/Barrier/operation state. Historical current
state documents whose capture predates the deployed Runtime fingerprint are
evidence only.

Proceed with this repair only if the current V7-owned receipt proves:

```text
core_primary_cohort_not_admissible_before_authority_consumption
```

and its owner-backed detail proves that positional class allocation is the
cause. If it does not, do not apply a speculative stable-ID migration; diagnose
and repair only the actual current generic blocker.

## Engineering / Runtime separation

Codex may inspect, repair the generic existing Core-primary implementation,
test and deploy through `tools/v7-safe-deploy`, then observe the ordinary V7
caller.

Codex must not invoke `v7-user-switch` for an affected user, choose a target,
edit an assignment, create or advance Candidate/Packet/Lease/Barrier, open
operation control, manually rebuild Core-primary, wake Matrix, invoke Planner
or replay the incident. A partly manual recovery is invalid evidence.

The only valid recovery provenance is:

```text
v7-health.service -> Matrix -> affected scope -> automatic Authority
-> Planner -> Candidate -> Packet -> Lease -> Barrier -> Apply
-> existing v7-user-switch -> Core-primary cohort commit
-> route/kernel verification -> required-service S11
```

## Product invariant

A route-class is an identity, not the position of an occupied channel in a
sorted list. For every still-configured egress, unrelated membership changes
must not change its class, mark, table or other existing routing identity.

An empty egress retains its class identity while it remains in canonical
topology. This does **not** make it routable: a disabled, stale or unhealthy
egress must remain ineligible as a target. Retirement is not part of this
recovery hot path and is allowed only through an already-existing explicit
topology/owner lifecycle after all consumers are closed.

Reuse the existing canonical egress registry, extending its current rows with
the stable Core-primary mark/table identity only after proving the existing
mark/table ranges, reserved values and collision rules. Do not equate a
registry ID with a mark/table number without that proof. Do not reuse
`route-classes.registry`: it owns service/profile route classes, not
Core-primary egress identity.

Required relation:

```text
canonical stable egress identity -> stable Core-primary class
-> unchanged existing fwmark/table association
```

Membership may change independently. No ordinary recovery may compact classes,
renumber unrelated users or rebuild the whole system.

## Minimal implementation and safe migration

Repair only the existing Core-primary/routing owner and retain `v7-user-switch`
as the sole route writer. Preserve the current architecture:

```text
user -> semantic class membership -> class egress -> fwmark/policy routing
```

If the deployed map is positional, perform at most one bounded owner-backed
migration. It must be deterministic and atomic from the observed data-plane
perspective. Before it, prove for every enabled user:

```text
old user -> old class -> old egress
new user -> stable class -> same egress
```

Migration must preserve every assignment, profile and effective egress. It may
not move the current VLESS acceptance users or manufacture a recovery target.
On any failure, old kernel map, current projection and assignments remain
authoritative; no projection may claim a committed map before its nft/policy
transaction is verified.

## Tests

Add focused tests for:

1. A/B/C classes; B becomes empty; A/C marks and mappings stay unchanged.
2. B later receives a member and reuses its old class.
3. Added D changes none of A/B/C; actual topology removal affects only its own
   retired identity through the existing lifecycle.
4. A 2-, 3- and 4-member cohort leaves a source; only selected membership
   changes, including when the source becomes empty.
5. No global rebuild, no unrelated user mark/mapping mutation, and restart
   preserves the mapping.
6. Range/reserved/collision validation for every stable mark/table identity.
7. Injected migration/commit failure: route/kernel map, assignment and
   published Core-primary truth remain the exact preimage.
8. Existing authority ordering remains: full Core-primary admissibility before
   irreversible Authority consumption.

Measure Core-primary preparation/commit separately. It must be affected-cohort
only and must not introduce recurring work above 100 ms without a measured
decomposition.

## Deploy and live proof

Run relevant routing/Core-primary, user-switch, autoswitch, governed-executor,
rollback, Authority/control-window and route-verification regressions. Deploy
only through `tools/v7-safe-deploy`; then prove local = GitHub = deploy manifest
= Runtime, and `v7-health.service` is active.

Return control to normal V7. If the same current failure, affected ordinary
scope and healthy target remain, V7 must re-enter without a manual wake or new
operator action.

For the first homogeneous post-fix automatic operation record:

```text
T_FIRST_VALID_FAILURE_OBSERVATION, T0, scope, decision, Candidate, Packet,
Lease, Barrier, control window, Core-primary admission, Apply, assignment,
Core-primary commit, kernel path, and each member's required-service S11.
```

`GLOBAL_ALL_AFFECTED_S11_SERVER_SIDE_RECOVERY_VERIFIED` is the maximum of the
members' S11 timestamps. Do not call it client traffic recovery/T11 unless
independent client telemetry proves that separately.

The single live operation must be <= 7 seconds from first fresh valid failure
observation to global S11; any functionally valid sample > 8 seconds is a
product failure. A final SLO claim also requires the Program's homogeneous
distribution rule, not one lucky sample.

If the routing repair works but the timing fails, use the timeline to repair
the next measured generic cause, test, deploy and return control to V7. Do not
start a new owner, perform a manual recovery or stop merely at code, migration
or deploy completion. Stop only at a genuine external/Authority/product
boundary, with the exact remaining interval and successor.
