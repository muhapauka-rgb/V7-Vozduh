# BLOCK E35.A0 Routing Mode Reality Audit Report

## 1. Executive Summary

E35.A0 completed as a read-only discovery/audit block.

The current V7 system has strong partial routing-control reality, but it does not yet have a complete per-user routing-mode model.

Existing reality:

- `users.registry` is the live assignment truth.
- `tools/v7-users-autoswitch` is the main autonomous/guarded channel selection engine.
- Admin can manually switch one user through `POST /api/actions/user-switch`.
- Channel-level autoswitch eligibility exists.
- Group-level eligibility and preference exist.
- Sticky/current route preference exists.
- Execution-only target exclusion from autoswitch exists.

Missing reality:

- no durable per-user `AUTO / MANUAL / OPERATOR_PINNED` mode for live routing;
- no explicit per-user pinned target;
- no explicit pin owner/reason/expiry;
- no durable manual assignment intent;
- no single routing ownership model.

## 2. Existing Routing Ownership

Routing ownership is distributed:

| Owner | Current Role |
|---|---|
| `users.registry` | Current assignment truth: user -> current egress and table. |
| `egress.registry` | Channel identity/static metadata. |
| Org egress policy | Channel/group autoswitch eligibility metadata. |
| Autoswitch planner | Candidate selection and guarded movement planning/apply path. |
| Admin manual switch | Operator direct movement path. |
| Governed execution packets | Bounded execution authority for proven movement blocks. |
| Execution-only readiness | Target isolation validation. |

There is no single explicit routing ownership object yet.

## 3. Existing Assignment Model

Current live assignment is:

```text
users.registry.current
```

Route table is:

```text
users.registry.table
```

Autoswitch loads users through `_load_users` in `tools/v7-users-autoswitch` and resolves group ownership from registry row fields and org policy mappings.

Verdict:

```text
assignment_truth_source_identified=true
```

## 4. Existing Pinned Semantics

Explicit pinned semantics were not found.

Related but not equivalent:

- sticky score keeps the current route harder to beat;
- `sticky_keep_current` explains a keep decision;
- group `preferred_egress` adds soft preference;
- admin manual switch moves a user but does not persist a pin.

Verdict:

```text
pinned_semantics_exist=false
```

## 5. Existing Manual Semantics

Manual semantics exist partially:

- admin manual switch exists;
- channel `manual_only` exists;
- reserve-only channels exist;
- execution-only targets are intentionally excluded from autoswitch.

But user-level `MANUAL` routing mode was not found.

Verdict:

```text
manual_semantics_exist=true
manual_user_mode_exists=false
```

## 6. Existing Autoswitch Eligibility Controls

Autoswitch eligibility controls exist.

Hard/soft control sources:

- enabled/state/maintenance/quarantine;
- `manual_only`;
- `reserve_only`;
- `canary_reserved`;
- health code;
- severity;
- hard capacity limits;
- group allowed/excluded pools;
- exclusive groups;
- egress group ACLs;
- quality floors;
- service failures;
- load gates;
- safety quarantine;
- blocked target/user pair reversal gates.

Verdict:

```text
autoswitch_eligibility_controls_exist=true
```

## 7. Reuse / Extend / Refactor / Replace Matrix

| Area | Decision |
|---|---|
| `users.registry` | Reuse as current assignment truth. |
| `egress.registry` | Reuse as channel identity/static metadata truth. |
| Org egress policy | Extend carefully for routing intent integration. |
| Autoswitch gates | Reuse as admission inputs. |
| Autoswitch scoring | Extend to respect explicit routing modes before scoring. |
| Admin manual switch | Extend to record manual intent once E35.A defines it. |
| Sticky score | Keep as soft preference; do not treat as pin. |
| Group `preferred_egress` | Keep as soft preference; do not treat as hard pin. |
| `pending_profiles.route_mode` | Do not reuse as live routing ownership without refactor. |
| Execution-only isolation | Reuse. |

## 8. Risks

| Risk | Severity |
|---|---|
| Manual switch mistaken for durable pin | High |
| Sticky score mistaken for operator authority | High |
| Autonomous movement touching a user that should be pinned | High |
| Missing routing ownership lineage | Medium |
| Group preference conflicting with future per-user pin | Medium |
| Operator cannot see why a user is on a channel | Medium |

## 9. Recommendations For E35.A

E35.A should introduce explicit routing intent/authority metadata:

```text
routing_mode=AUTO | MANUAL | OPERATOR_PINNED
routing_owner=autoswitch | operator | governance | scheduler
target_egress=<egress>
reason=<text>
created_at=<timestamp>
expires_at=<optional timestamp>
evidence_bundle_id=<optional>
proposal_id=<optional>
```

E35.A should require autoswitch and future autonomous execution to evaluate routing mode before score ranking.

Recommended hard behavior:

- `OPERATOR_PINNED` blocks autonomous forward movement away from pinned target.
- `MANUAL` blocks autonomous movement unless explicit operator/governance override exists.
- `AUTO` allows normal autoswitch/governance admission.
- rollback/containment may remain allowed under explicit containment rules.

## 10. Safety Statement

This was a read-only audit.

No runtime mutation was performed.

No user movement was performed.

No routing mutation was performed.

No autoswitch apply was run.

No policy apply was run.

No kill switch control was changed.

## Required Verdicts

```text
e35_a0_completed=true
routing_mode_exists=false
preferred_channel_exists=false
pinned_semantics_exist=false
manual_semantics_exist=true
autoswitch_eligibility_controls_exist=true
assignment_truth_source_identified=true
routing_ownership_identified=true
e35_a_ready=true
```

## Final Safety

```text
runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_changed=false
```
