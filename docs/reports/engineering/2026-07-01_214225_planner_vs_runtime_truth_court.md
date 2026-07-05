# Planner vs Runtime Truth Court

Timestamp: 2026-07-01_214225 Asia/Bangkok

Mode: READ_ONLY_FORENSIC. No patch, no deploy, no production mutation, no user movement, no recomputation.

## Final Judgement

NO_DISAGREEMENT_STOP_SAFE_CORRECT

First disagreement: `NONE`

Responsible owner: `NONE_FOR_DISAGREEMENT`

Exact file/function:
- Frozen candidate producer: historical `tools/v7-users-autoswitch::_decision_for_user` in `fixture_all_no_target.json` lineage.
- Runtime stop consumer if apply were attempted with no selected move: `tools/v7-users-autoswitch::apply`, current lines 7530-7563.
- Current L3 validation envelope owner for post-selection execution eligibility: `tools/v7-users-autoswitch::_approved_l3_production_validation_envelope`, current lines 1082-1168.

Minimal correction direction: do not charge Runtime for refusing an object with no L3 selected move identity. If correction is desired, it belongs before Runtime: Planner/proposal layer must produce an L3 failover selected move plus approved plan lock, rollback readiness, verification readiness, and identity evidence. No implementation in this report.

## Canonical Contract Used

Canonical sources read:
- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/policies/POLICY_001_HARD_FAILURE.md`
- `docs/policies/POLICY_004_AUTHORITY.md`
- `docs/policies/POLICY_008_FRESHNESS.md`

Canonical rules applied:
- L3 starts only when all mandatory conditions are true.
- If any mandatory entry/readiness condition is false or unknown, L3 must `STOP_SAFE`.
- Planner selects candidate, target, action class, selected move identity, and explanation.
- Runtime executes or `STOP_SAFE`; Runtime must not invent decisions, replace Planner, rerun planning, or silently replace user/source/target/hash/authority/rollback/verification identity.
- Mutation must not rely on stale/missing identity or readiness evidence.

Reports read as evidence index, not canonical truth:
- 101 engineering reports from `2026-06-30_*` through latest `2026-07-01_*`.
- The latest direct producer trace is `2026-07-01_213255_restore_barrier_failover_suppressed_producer_trace.md`.

## Candidate Selection

Target incident: real failed OpenVPN production incident, source `openvpn-1779388847-d2ad7c`.

Chosen object:
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_all_no_target.json`
- updated: `2026-06-29T17:15:32.007703+00:00`
- reason for choosing: latest non-counterfactual full persisted OpenVPN incident artifact with complete `decisions`, candidate rows, source/target evidence, operation identity, restore barrier, authority gate, and selected move hash.

Excluded:
- `counterfactual_*` artifacts under the same directory. They contain later source failover rows, but are explicitly counterfactual and therefore not the real production candidate for this court.

## Frozen Candidate

Immutable candidate object:

```json
{
  "user": "10.0.0.2",
  "source": "openvpn-1779388847-d2ad7c",
  "target": "vless",
  "route_class": "VIDEO_OPTIMIZED",
  "required_services": ["youtube", "instagram", "telegram", "google", "google_auth"],
  "action": "keep",
  "move_type": "none",
  "reason": ["restore_barrier_failover_suppressed"],
  "current_candidate": {
    "egress": "openvpn-1779388847-d2ad7c",
    "eligible": false,
    "blocked": ["telegram_required_telegram_down_14s", "planned_hard_full"],
    "telegram": {
      "status": "TELEGRAM_DOWN_14S",
      "ok": false,
      "hard_blocked": true
    },
    "load": {"users": 14, "hard_limit": 14, "status": "HARD_FULL"}
  },
  "target_candidate": {
    "egress": "vless",
    "eligible": true,
    "blocked": [],
    "telegram": {
      "status": "OK",
      "ok": true,
      "hard_blocked": false
    },
    "load": {"users": 0, "hard_limit": 14, "status": "OK"}
  },
  "freshness": {
    "current_services": "AGING, accepted by serialized Planner decision",
    "target_services": "AGING, accepted by serialized Planner decision"
  },
  "authority": {
    "authority_class": "CANARY",
    "current_allowed_user_budget": 1,
    "selected_moves_after_gate": 1
  },
  "restore_barrier": {
    "active": true,
    "cleared": true,
    "failover_quarantine": true,
    "clearance_max_selected_moves": 0,
    "clearance_guard_reason": null
  },
  "approved_plan_lock": null,
  "selected_move_hash": "dd37cb09bf92e82e042f428ff0eda4bfe45a03c8db443c95fbe3587349849fe7",
  "selected_move_for_candidate": null,
  "apply_result": {"applied": false, "reason": "dry_run"}
}
```

Important identity note:
- The operation has a `selected_move_hash`, but it belongs to the selected unrelated rebalance move in the plan.
- The frozen OpenVPN candidate has `selected_move_for_candidate = null`.

## Planner Trial

Planner receives only the frozen object.

Planner-owned conclusions:
- Current/source channel failed: true.
- Required service failure exists: true.
- Affected user exists: true.
- Safe target exists: true.
- Candidate action is not failover: false.
- Candidate move type is not failover: false.
- No selected move identity exists for this candidate: false for identity/execution readiness.

Planner cannot claim an L3 executable candidate from this frozen object because its own serialized fields are `action=keep`, `move_type=none`, and `selected_move_for_candidate=null`.

## Runtime Trial

Runtime receives exactly the same frozen object.

Runtime-owned conclusions:
- Runtime must not invent a selected move or rerun Planner.
- Runtime must preserve selected move identity; no candidate identity exists for this user/source/target.
- Approved plan lock is missing.
- Rollback readiness is missing.
- Verification readiness is missing.
- Execution readiness is false.

Runtime therefore must stop safely / no-op. This is aligned with the Runtime Model.

## Truth Table

| Mandatory truth | Planner | Runtime | Evidence | Owner | Producer | Consumer | Object | Function |
|---|---:|---:|---|---|---|---|---|---|
| CURRENT_CHANNEL_FAILED | TRUE | TRUE | current candidate `eligible=false`; blocker `telegram_required_telegram_down_14s`; Telegram hard blocked | Planner/service evidence | `tools/v7-users-autoswitch` serialized candidate | Planner/Runtime | `decision.candidates[current]` | `_candidate`, `_gate_service` |
| REQUIRED_SERVICE_FAILURE | TRUE | TRUE | Telegram status `TELEGRAM_DOWN_14S`, `hard_blocked=true` | service matrix / Planner consumer | service matrix consumed into candidate | Planner/Runtime | `current_candidate.telegram` | `_telegram_candidate_state`, `_gate_service` |
| AFFECTED_USER | TRUE | TRUE | user `10.0.0.2` current egress is failed source | user registry / Planner | `users.registry` consumed in plan | Planner/Runtime | `decision.user_ip/current_egress` | `_decision_for_user` |
| SAFE_TARGET | TRUE | TRUE | target `vless` eligible, blockers `[]`, Telegram OK, load OK | Planner/autoswitch | `tools/v7-users-autoswitch` | Planner/Runtime | `decision.candidates[vless]` | `_candidate` gates |
| FRESH_EVIDENCE | TRUE | TRUE | service freshness state `AGING`, not expired in serialized decision; no recomputation allowed | freshness/evidence owners | service suitability rows | Planner/Runtime | `service_suitability.per_service.*.freshness` | `_service_suitability` |
| ACTION_CLASS_FAILOVER | FALSE | FALSE | candidate `action=keep` | Planner | `tools/v7-users-autoswitch` | Runtime | `decision.action` | historical `_decision_for_user` |
| MOVE_TYPE_FAILOVER | FALSE | FALSE | candidate `move_type=none` | Planner | `tools/v7-users-autoswitch` | Runtime | `decision.move_type` | historical `_decision_for_user` |
| EXECUTION_CLASS_L3 | FALSE | FALSE | no selected OpenVPN failover move; no L3 execution envelope for this candidate | Planner/Runtime | Planner plan | Runtime apply path | `selected_move_for_candidate=null` | `plan`, `apply` |
| CURRENT_EGRESS_NOT_ELIGIBLE | TRUE | TRUE | current candidate `eligible=false` | Planner | `tools/v7-users-autoswitch` | Planner/Runtime | `current_candidate.eligible` | `_candidate` |
| TARGET_ELIGIBLE | TRUE | TRUE | `vless eligible=true` | Planner | `tools/v7-users-autoswitch` | Planner/Runtime | `target_candidate.eligible` | `_candidate` |
| AUTHORITY_PRESENT | TRUE | TRUE | authority budget gate: `CANARY`, allowed users `1` | authority policy / Planner consumer | `tools/v7-users-autoswitch` | Runtime | `safety.authority_budget_gate` | `_authority_budget_gate` |
| RESTORE_BARRIER_VALID | FALSE | FALSE | barrier active but `clearance_max_selected_moves=0`, no candidate clearance/guard reason | restore barrier owner | restore barrier file consumed into plan | Runtime | `safety.restore_barrier` | `_restore_barrier_status`, validation envelope |
| APPROVED_PLAN_LOCK_VALID | FALSE | FALSE | `approved_plan_lock=null` | approved-plan-lock owner | none in object | Runtime | `restore_barrier.approved_plan_lock_validation` | `_approved_plan_lock_validation` |
| IDENTITY_VALID | FALSE | FALSE | operation hash belongs to unrelated selected move; no selected move for candidate | Planner/packet owner | plan operation | Runtime | `selected_move_for_candidate=null` | `_selected_moves_hash`, selected move extraction |
| ROLLBACK_READY | FALSE | FALSE | no rollback/no-rollback readiness object for this candidate | rollback owners | absent | Runtime | frozen candidate | Runtime readiness contract |
| VERIFICATION_READY | FALSE | FALSE | no verification plan/status object for this candidate | verification owners | absent | Runtime | frozen candidate | Runtime readiness contract |
| EXECUTION_READY | FALSE | FALSE | action/move/identity/lock/rollback/verification are false | Runtime | frozen candidate | Runtime | full candidate | `apply`, validation envelope |

## First Disagreement

First disagreement: `NONE`.

There is no row where Planner and Runtime differ. Both sides evaluate the same frozen object to the same truth values.

This is not a case of Runtime rejecting a valid Planner L3 selected move. The frozen object does not contain a valid L3 selected move for the failed OpenVPN candidate.

## Formal Proof

Let mandatory truth set be:

`M = {CURRENT_CHANNEL_FAILED, REQUIRED_SERVICE_FAILURE, AFFECTED_USER, SAFE_TARGET, FRESH_EVIDENCE, ACTION_CLASS_FAILOVER, MOVE_TYPE_FAILOVER, EXECUTION_CLASS_L3, CURRENT_EGRESS_NOT_ELIGIBLE, TARGET_ELIGIBLE, AUTHORITY_PRESENT, RESTORE_BARRIER_VALID, APPROVED_PLAN_LOCK_VALID, IDENTITY_VALID, ROLLBACK_READY, VERIFICATION_READY, EXECUTION_READY}`

Planner truth set:

`P_TRUE = {CURRENT_CHANNEL_FAILED, REQUIRED_SERVICE_FAILURE, AFFECTED_USER, SAFE_TARGET, FRESH_EVIDENCE, CURRENT_EGRESS_NOT_ELIGIBLE, TARGET_ELIGIBLE, AUTHORITY_PRESENT}`

Runtime truth set:

`R_TRUE = {CURRENT_CHANNEL_FAILED, REQUIRED_SERVICE_FAILURE, AFFECTED_USER, SAFE_TARGET, FRESH_EVIDENCE, CURRENT_EGRESS_NOT_ELIGIBLE, TARGET_ELIGIBLE, AUTHORITY_PRESENT}`

Intersection:

`P_TRUE ∩ R_TRUE = {CURRENT_CHANNEL_FAILED, REQUIRED_SERVICE_FAILURE, AFFECTED_USER, SAFE_TARGET, FRESH_EVIDENCE, CURRENT_EGRESS_NOT_ELIGIBLE, TARGET_ELIGIBLE, AUTHORITY_PRESENT}`

Difference:

`P_TRUE - R_TRUE = ∅`

`R_TRUE - P_TRUE = ∅`

False set shared by both:

`FALSE_SHARED = {ACTION_CLASS_FAILOVER, MOVE_TYPE_FAILOVER, EXECUTION_CLASS_L3, RESTORE_BARRIER_VALID, APPROVED_PLAN_LOCK_VALID, IDENTITY_VALID, ROLLBACK_READY, VERIFICATION_READY, EXECUTION_READY}`

Minimal inconsistent set:

`∅`

There is no Planner/Runtime inconsistency.

Single-fact removal proof:
- Removing only `RESTORE_BARRIER_VALID=false` does not make execution ready because action, move type, identity, approved lock, rollback, and verification remain false.
- Removing only `APPROVED_PLAN_LOCK_VALID=false` does not make execution ready because no candidate selected move identity exists.
- Removing only `IDENTITY_VALID=false` does not make execution ready because action/move type and readiness gates remain false.
- Changing only `ACTION_CLASS_FAILOVER` or only `MOVE_TYPE_FAILOVER` is not enough because selected move identity, approved lock, rollback, and verification remain false.
- Therefore no single fact change makes execution legal.

## Responsibility Determination

Choice: No disagreement.

Why STOP_SAFE/no-execution is correct:
- Canonical L3 requires all mandatory conditions true.
- The frozen candidate lacks the action class, move type, selected move identity, approved plan lock, rollback readiness, verification readiness, and execution readiness required for L3 execution.
- Runtime is canonically forbidden to invent or replace these fields.

The candidate is not mutated between parties in this court. Both parties receive the same object. The first disagreement set is empty.

## Final Court Finding

Verdict: `NO_DISAGREEMENT_STOP_SAFE_CORRECT`

Guilty party: none in Planner-vs-Runtime truth comparison.

Minimal correction direction:
- If the product goal is to move users from the failed OpenVPN source, produce a real Planner L3 failover selected move for the affected source and carry it through approved plan lock, identity, rollback, verification, and restore-barrier readiness.
- Do not charge Runtime with refusing to execute a candidate that lacks those mandatory L3 execution facts.
