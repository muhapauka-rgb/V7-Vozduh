# E35.B Boundary Discovery

## Scope

E35.B defines where each authority ends.

This discovery audits existing boundary-like behavior before defining the constitutional model.

## Existing Boundary-Like Systems

| System | Existing Boundary | Classification |
|---|---|---|
| Safety gates | Quarantine, failed verification limits, blocked target, anti-flap pair reversal. | Reuse |
| Runtime trust / restore-settle | Blocks forward movement when runtime is unstable. | Reuse |
| Approval packets | Scope, expiry, replay protection, registry hashes, selected moves hash. | Reuse |
| Autoswitch gates | Basic, reservation, group, service, quality, load, safety gates. | Reuse |
| Group policy | `allowed_egress`, `excluded_egress`, `preferred_egress`, `isolation`. | Extend |
| Channel policy | `manual_only`, `reserve_only`, `canary_reserved`, execution-only. | Reuse |
| Required services | Hard service failures block suitability/admission. | Reuse |
| Capacity | Hard limits block planned/failover movement. | Reuse |
| Quality floors | avg/min Mbps and stability floors block candidates. | Reuse |
| Manual switch | Operator direct movement path exists. | Extend |
| Rollback | Restore/containment path exists. | Extend |
| Sticky/current route | Soft preference only. | Do Not Touch |
| Speed/score | Ranking only after hard gates. | Do Not Touch |
| `pending_profiles.route_mode` | Provisioning/profile field, not live authority. | Do Not Touch |

## What Already Limits Authority

- safety/quarantine;
- kill-switch/runtime trust when blocking;
- governance packet scope and replay protection;
- restore-settle;
- selected moves and hidden movers;
- channel `manual_only`;
- channel `reserve_only`;
- execution-only/canary reservation;
- group allowed/excluded/isolation constraints;
- required service hard failures;
- capacity hard limit;
- quality floors;
- anti-flap safety.

## What Already Overrides Authority

Current override behavior is partial and implicit:

- rollback can restore previous known state;
- admin manual switch can directly move one user if runtime command succeeds;
- governed execution packet can move exact approved scope;
- containment is implied by rollback/safety history but not explicit.

## What Already Blocks Movement

Movement is blocked by:

- packet invalid/stale/replayed;
- registry hash mismatch;
- selected move mismatch;
- target not GO;
- restore-settle not GO;
- runtime checkers fail;
- channel hard gates;
- service hard gates;
- capacity hard gates;
- safety gates.

## What Already Creates Exceptions

Existing exceptions:

- rollback after failed admin proxy switch;
- governed execution-only target allowed only through explicit execution mode;
- current user on canary-reserved target may be held but not production-drained without separate approval;
- failover may use different load limits than planned movement.

## Discovery Verdict

```text
boundary_discovery_complete=true
existing_boundaries_identified=true
existing_exceptions_identified=true
boundary_model_needed=true
```
