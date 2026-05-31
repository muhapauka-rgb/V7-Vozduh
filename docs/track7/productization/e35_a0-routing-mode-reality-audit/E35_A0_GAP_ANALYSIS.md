# E35.A0 Gap Analysis

## What Exists

| Area | Exists | Notes |
|---|---:|---|
| Live assignment truth | Yes | `users.registry.current` |
| Route table mapping | Yes | `users.registry.table` |
| Channel metadata | Yes | `egress.registry` and org egress policy |
| Manual operator switch | Yes | Admin `user-switch` action |
| Autoswitch planner | Yes | `tools/v7-users-autoswitch` |
| Autoswitch eligibility controls | Yes | channel/group/quality/load/safety/service gates |
| Sticky current route preference | Yes | soft score + reason |
| Group preferred egress | Yes | soft preference |
| Execution-only target isolation | Yes | readiness helper and tests |

## What Does Not Exist

| Gap | Status | Why It Matters |
|---|---|---|
| Per-user `routing_mode` for live users | Missing | E35.A cannot safely infer AUTO/MANUAL/PINNED from current state alone. |
| `OPERATOR_PINNED` semantics | Missing | Sticky score is not a hard operator pin. |
| Durable manual assignment mode | Missing | Manual switch changes route, but not durable intent. |
| Per-user autoswitch exclusion | Missing | Channel-level exclusion exists, user-level exclusion was not found. |
| Pin owner/reason/expiry | Missing | Needed for audit and safe override. |
| Ownership conflict resolution | Missing | Scheduler/governance/operator/autoswitch can conflict at larger scale. |
| Routing intent lineage | Missing | Current assignment does not explain decision lineage. |

## Reuse / Extend / Refactor / Replace Matrix

| Component | Recommendation | Reason |
|---|---|---|
| `users.registry` | Reuse | It is current runtime assignment truth. |
| `egress.registry` | Reuse | It is current channel identity/static metadata truth. |
| Org egress policy | Extend | Already stores channel and group constraints; can support more ownership metadata carefully. |
| Autoswitch gates | Reuse | Strong existing admission model. |
| Autoswitch scoring | Extend | Add awareness of explicit user routing mode/pins before selection. |
| Admin manual switch | Extend | Should record manual routing intent when E35.A introduces it. |
| `pending_profiles.route_mode` | Do not reuse as-is | It is profile/provisioning-related, not live routing authority. |
| Sticky score | Keep as soft preference | It is not pinning and should remain separate. |
| Group `preferred_egress` | Keep as soft preference | Useful, but not a hard lock. |
| Execution-only isolation | Reuse | Already proven for governed execution targets. |

## Risks If E35.A Proceeds Without Fixing Gaps

| Risk | Severity | Explanation |
|---|---|---|
| Manual movement misread as pin | High | A user manually moved once may later be autoswitched because no pin exists. |
| Sticky confused with governance | High | Sticky only adds score; it does not enforce authority. |
| User-level intent invisible | High | Operator cannot know if a user is AUTO or protected. |
| Policy conflict | Medium | Group preference, capacity gates, and manual operator intent may disagree. |
| Audit ambiguity | Medium | `current` tells where, not why. |
| Autonomous execution overreach | High | E35.A needs hard boundaries before autonomy expands. |

## Recommended Changes Before / In E35.A

1. Define explicit live routing modes:

```text
AUTO
MANUAL
OPERATOR_PINNED
```

2. Add a durable routing intent model separate from `users.registry.current`.

3. Make autoswitch selection consult routing intent before candidate scoring.

4. Treat pinned/manual modes as hard admission constraints unless containment/rollback explicitly overrides.

5. Extend admin to show routing mode and owner beside current assignment.

6. Preserve existing channel-level controls as target eligibility inputs.

7. Preserve group `preferred_egress` as soft preference, not pin.

8. Record manual switch lineage into routing intent once E35.A introduces the model.

## E35.A Readiness

```text
e35_a_ready=true
```

Rationale:

The audit found enough existing reality to design E35.A safely:

- assignment source is known;
- channel eligibility controls are known;
- current missing semantics are explicit;
- reuse/extend boundaries are clear.

E35.A should be a design/implementation block for execution authority and routing intent, not another discovery block.
