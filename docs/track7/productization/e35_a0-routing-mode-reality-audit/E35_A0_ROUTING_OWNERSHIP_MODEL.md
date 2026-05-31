# E35.A0 Routing Ownership Model

## Existing Ownership Reality

Current V7 routing ownership is distributed across several systems. No single explicit routing ownership model exists yet.

## Existing Owners

| Owner / System | What It Owns Today | Evidence |
|---|---|---|
| `users.registry` | Current live user -> egress assignment | `ip`, `current`, `table`, `enabled` rows |
| `egress.registry` | Channel identity and static channel metadata | egress id, role, enabled, capacity flags |
| Org egress policy | Group/channel constraints and autoswitch metadata | `/etc/v7/org-egress-policy.json`, admin policy editor |
| Autoswitch planner | Candidate selection and guarded movement plan | `tools/v7-users-autoswitch` |
| Admin manual switch | Operator manual movement | `/api/actions/user-switch` |
| Governed execution packets | Bounded approved movement | E25-E31 execution proofs |
| Execution-only readiness | Execution target isolation | second canary readiness helper/tests |

## Ownership Split

### Current State Ownership

Current state is owned by:

```text
users.registry.current
```

This answers:

```text
Where is the user now?
```

It does not answer:

```text
Why is the user there?
Who owns this placement?
Can autoswitch move this user?
Is this placement pinned?
Is this placement manual?
When does the placement expire?
```

### Channel Eligibility Ownership

Channel eligibility is owned by:

```text
egress.registry
org egress policy
readiness/quality/runtime state
```

Eligibility examples:

- `manual_only`
- `reserve_only`
- `canary_reserved`
- `exclusive_group`
- group ACLs
- capacity limits
- health code
- severity
- service fitness
- quality floors

### Decision Ownership

Decision ownership is currently mixed:

- autoswitch may recommend and apply selected moves when apply mode is used;
- admin can directly switch one user;
- governed execution packets can bound approved movement;
- policy and capacity are admission signals, not execution authority.

## Current Ownership Gaps

Missing explicit model:

| Gap | Why It Matters |
|---|---|
| User routing authority | E35.A needs to know whether autoswitch, operator, governance, or scheduler owns a user placement. |
| Pin owner | A pinned user needs a durable owner and reason. |
| Manual assignment semantics | Admin manual switch currently changes state, but does not persist a durable manual routing mode. |
| Expiry / lease | Temporary manual assignments need a safe end condition. |
| Conflict resolution | Future scheduler/governance/autoswitch can conflict without explicit ownership. |
| Audit lineage | Current state does not fully encode decision lineage. |

## Recommended Ownership Model For E35.A

Introduce explicit routing ownership metadata without replacing current runtime truth:

```text
current_state:
  source: users.registry
  field: current

routing_intent:
  mode: AUTO | OPERATOR_PINNED | MANUAL
  owner: autoswitch | operator | governance | scheduler
  target: egress id
  reason: string
  created_at: timestamp
  expires_at: timestamp optional
  evidence_bundle_id: optional
  proposal_id: optional
```

## Reality Verdict

```text
routing_ownership_identified=true
single_authoritative_ownership_model_exists=false
current_assignment_owner=users.registry
decision_owner=mixed
e35_a_requires_explicit_ownership_layer=true
```
