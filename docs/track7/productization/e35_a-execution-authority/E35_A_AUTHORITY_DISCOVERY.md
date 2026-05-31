# E35.A Authority Discovery

## Scope

Question:

```text
What currently grants, blocks, or overrides authority to change a user's channel?
```

This is a discovery pass only. It does not design scoring, selection, suitability, service matrix behavior, or capacity logic.

## Current Authority-Like Concepts

| Concept | Current Reality | Grants Authority? | Blocks Authority? | Override Behavior |
|---|---|---:|---:|---|
| `users.registry.current` | Current assignment truth. | No | No | It records current state, not permission. |
| Admin manual switch | `/api/actions/user-switch` calls `v7-user-switch` with `V7_SWITCH_REASON=admin_manual`. | Yes, operator direct action. | No | Can rollback proxy/runtime failure to previous egress. |
| Autoswitch planner | `tools/v7-users-autoswitch` can select moves and apply with `v7-user-switch` when apply mode is enabled. | Partial | Yes | Blocked by policy, observe mode, no selected moves, gates. |
| Approval packets | `admin_core/operator_execution.py` validates packet, registry hashes, selected move hash and replay. | Yes, for governed packet scope. | Yes | Denies stale/replayed/invalid packets. |
| Restore-settle | Runtime stabilization gate from previous governance blocks. | No | Yes | Blocks forward movement; rollback remains allowed. |
| `selected_moves` | Current selected movement state. | No | Yes | Non-zero selected moves block record-only packet recheck. |
| `manual_only` channel | Channel may not be selected by automation. | No | Yes | Manual/operator/governed paths may still use explicit target if allowed by later authority. |
| `reserve_only` channel | Channel blocked for planned autoswitch. | No | Yes | Can be used by failover/governed flows if explicitly allowed. |
| `canary_reserved` / execution-only | Production assignment blocked; execution target isolation. | No | Yes | Governed execution-only flow can use explicit target after readiness. |
| Group policy | allowed/excluded/preferred/isolation/group ACL. | No | Yes | Allows/blocks candidate eligibility. Preferred is soft only. |
| Required services | Service availability gates. | No | Yes | Hard service failure blocks forward movement; containment may move away. |
| Sticky score | Current route gets score bonus. | No | Soft preference | Does not prevent movement. |
| Preferred egress | Group `preferred_egress` score/reason. | No | Soft preference | Does not prevent movement. |
| Rollback paths | Governed movement rollback and admin switch rollback on proxy failure. | Yes, containment/restore authority. | No | Can override forward denial only for restoring known previous state. |

## Existing Grant Sources

Current V7 can grant movement through:

1. Operator direct action:
   - admin `user-switch`;
   - explicit target selected by human.

2. Autoswitch apply:
   - guarded planner selected moves;
   - policy mode not observe;
   - `autoswitch_enabled` true;
   - candidate passes gates.

3. Governance execution:
   - approval packet;
   - fresh execution-time recheck;
   - exact allowed users and target;
   - replay protection;
   - rollback manifest.

4. Containment / rollback:
   - restore to previous known state;
   - emergency move away from unsafe target;
   - bounded by scope and audit.

## Existing Block Sources

Current V7 blocks movement through:

- packet expiry/replay/hash mismatch;
- selected moves mismatch;
- runtime registry mismatch;
- target not GO;
- restore-settle not GO;
- selected moves non-zero;
- hidden movers;
- runtime checker failures;
- channel `manual_only`;
- channel `reserve_only` for planned autoswitch;
- canary/execution reservation;
- group allowed/excluded/isolation constraints;
- health/severity/quality floors;
- service hard failures;
- capacity hard limits;
- safety quarantine/anti-flap gates.

## Existing Overrides

Current override semantics are implicit:

- Admin manual switch can move a user directly if the endpoint accepts target and runtime command succeeds.
- Governance packet can move exact allowed users under packet constraints.
- Rollback can restore known previous state after failure or observation window.
- Containment can be modeled from existing safety/rollback evidence, but no explicit authority object exists yet.

## Discovery Verdict

```text
authority_discovery_complete=true
explicit_authority_model_exists=false
current_grant_sources_identified=true
current_block_sources_identified=true
current_override_sources_identified=true
```
