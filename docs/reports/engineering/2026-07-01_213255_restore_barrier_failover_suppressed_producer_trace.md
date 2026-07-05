# V7 Producer Trace: restore_barrier_failover_suppressed

Timestamp: 2026-07-01_213255 Asia/Bangkok

Mode: READ_ONLY_FORENSIC. No patch, no deploy, no production mutation, no user movement.

## Verdict

PRODUCER_FOUND

First producer:
- commit/object: `736f0354:tools/v7-users-autoswitch`
- exact function: `AutoswitchPlanner._decision_for_user`
- exact line in that historical object: `1156`
- statement: `reason.append("restore_barrier_failover_suppressed")`

Current HEAD:
- no producer remains in `tools/v7-users-autoswitch`
- only current executable/support occurrence is `tools/v7-control-plane-governance-check:2806`, a report/evidence consumer

## Direct Code Proof

Historical first producer from `736f0354:tools/v7-users-autoswitch:1123-1170`:

```python
elif not current or not current.eligible:
    service_signal_restore_gate = (...)
    if current and bool_value(self.restore_barrier.get("failover_quarantine")):
        if bool_value(self.restore_barrier.get("post_ttl_blocking")):
            reason.append("restore_barrier_post_ttl_generation_clearance_required")
        else:
            reason.append("restore_barrier_failover_suppressed")
    elif service_signal_restore_gate:
        reason.append("restore_stage_service_signal_failover_requires_approval")
    else:
        failover_candidates = [...]
```

Historical parent `736f0354^` did not contain the string and went directly from `not current/current ineligible` to failover candidate construction.

Commit `8a8e38a6` removed this producer. Current HEAD instead does:
- create failover candidates in `_decision_for_user`
- append `current_egress_not_eligible`
- if restore barrier quarantine exists, append `restore_barrier_execution_blocked`
- selected moves are later blocked by `plan()` restore-barrier execution gate

## First Producer Classification

Occurrence: `736f0354:tools/v7-users-autoswitch:1156`

Classification: A. produces reason

Producer:
- `AutoswitchPlanner._decision_for_user`
- owner: `tools/v7-users-autoswitch`

Creates reason because:
- `current` exists
- `current.eligible == false`
- `self.restore_barrier.failover_quarantine == true`
- `self.restore_barrier.post_ttl_blocking == false`

Not because of:
- restore barrier budget: no
- restore barrier generation: no
- authority: no
- packet: no
- approved lock: no
- Runtime: no
- `_gate_basic`, `_gate_quality`, `_gate_service`, `_gate_load`, `_gate_safety`, `_candidate`, `_select_moves`, `plan`, `operator_execution`: no

Location:
- BEFORE selected move creation
- BEFORE failover candidate creation
- BEFORE `_select_moves`
- BEFORE `approved_plan_lock`
- BEFORE restore-barrier apply/execution gates
- BEFORE Runtime

Semantic class:
- Planner decision reason
- Planner suppression of failover proposal creation
- not Runtime suppression
- not execution suppression
- not report-only at the point of origin

## Propagation Chain

origin:
- restore barrier status object from `_restore_barrier_status`
- `failover_quarantine = enabled and (active or post_ttl_blocking)`

↓

first producer:
- `736f0354:tools/v7-users-autoswitch::_decision_for_user`
- object before: local `reason=[]`, `action="keep"`, `move_type="none"`, `recommended=user.current`
- object after: `reason=["restore_barrier_failover_suppressed"]`; action/move_type/recommended unchanged
- reason generated: yes
- reason appended: yes
- reason changed: yes, empty list to one reason

↓

decision serialization:
- `736f0354:tools/v7-users-autoswitch::plan`
- object before: Python decision dict returned by `_decision_for_user`
- object after: `plan["decisions"]` includes same reason list
- reason copied: yes
- reason filtered: no
- reason generated: no
- line evidence: `plan()` returns `"decisions": decisions`

↓

selected move:
- `_select_moves(decisions)`
- object before: decision has `action="keep"`, `move_type="none"`
- object after: no selected move from that decision
- reason consumed as selection predicate: no
- reason copied into selected move: no
- suppression mechanism: the producer left decision as `keep/none`, so `_select_moves` had no failover move to select

↓

approved_plan_lock:
- no selected move exists for the suppressed decision
- object before: no move
- object after: no approved-plan-lock move can be derived from that suppressed decision
- reason copied: no
- reason filtered: no
- reason generated: no

↓

restore_barrier:
- legacy producer read `restore_barrier.failover_quarantine`
- it did not write the restore barrier
- budget/generation guards did not create this reason
- reason copied into restore barrier: no

↓

Runtime:
- no Runtime consumption proven
- because the reason exists only on a keep/none planner decision and no selected move is produced from it

↓

report/artifact:
- persisted planner outputs and reports preserve/report `plan.decisions[*].reason`
- classification: D. reports reason, or B. propagates serialized planner decision

## Occurrence Matrix

Current executable/support code:

| Occurrence | Classification | Producer/consumer | Notes |
|---|---:|---|---|
| `tools/v7-control-plane-governance-check:2806` | C/D | consumer/report evidence check | Reads text in a rehold/report artifact: `"decisions included \`restore_barrier_failover_suppressed\`"`. Does not create planner reason. |

Historical executable code:

| Occurrence | Classification | Producer/consumer | Notes |
|---|---:|---|---|
| `736f0354:tools/v7-users-autoswitch:1156` | A | first producer | Appends reason in `_decision_for_user` before failover candidates. |
| `736f0354:tests/unit/test_v7_users_autoswitch_policy.py:231` | C | test consumer | Asserts reason is present. |
| `736f0354:tests/unit/test_v7_users_autoswitch_policy.py:251` | C | test consumer | Asserts reason is present. |
| `8a8e38a6` diff | E/removal | producer removed | Replaces legacy reason with visible failover proposal plus `restore_barrier_execution_blocked`. |

Persisted planner artifacts:

| Occurrence class | Classification | Notes |
|---|---:|---|
| `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_all_no_target.json` | B/D | Serialized planner decision. Example line 17918 contains the reason. |
| `fixture_all_no_target.stdout`, `fixture_user_*.json/stdout`, `fixture_summary.json`, `fixture_all_no_target_affected_summary.json` | B/D | Serialized or summarized historical planner output. |
| `program_ab_evidence`, `program_ac_evidence`, `PR1_EVIDENCE`, `LOOP1_EVIDENCE`, `source_bundle_lease_chain_evidence` | D | Evidence snapshots or code excerpts. |

Reports/reference docs:

| Occurrence class | Classification | Notes |
|---|---:|---|
| `docs/reports/engineering/2026-06-30_001720_openvpn_d2ad7c_selected_move_break_trace.md` | D | Report-only trace. |
| `docs/reports/engineering/2026-06-30_004017_restore_barrier_contract_and_trace_audit.md` | D | Report-only audit; correctly identifies old producer. |
| `docs/reports/engineering/2026-06-30_004804_patch_impact_and_safety_certification.md` | D | Report-only patch impact. |
| `docs/reports/engineering/2026-06-30_074939_phase1_restore_barrier_planner.md` | D | Report-only states legacy suppression removed. |
| `docs/reports/engineering/2026-07-01_212850_maximum_speed_autoswitch_forensic_sprint.md` | D | Previous report; classification should be narrowed by this producer trace. |
| `docs/track7/control-plane/...` | D | Reference/evidence docs. |

## Special Questions

1. Exact function FIRST creating the reason:
   `AutoswitchPlanner._decision_for_user` in `736f0354:tools/v7-users-autoswitch:1156`.

2. Generated inside:
   `_decision_for_user`.

   Not generated inside:
   `_gate_basic`, `_gate_reservation`, `_gate_org`, `_gate_quality`, `_gate_service`, `_gate_load`, `_gate_safety`, `_candidate`, `_select_moves`, `plan`, `operator_execution`, restore barrier writer, or Runtime.

3. Producer condition:
   Generated because restore barrier already existed as `failover_quarantine=true`, and `post_ttl_blocking=false`, while current candidate was ineligible.

   Not directly generated because of budget, generation, authority, packet, approved lock, or Runtime.

4. Producer location:
   BEFORE selected move creation.

5. Reason type:
   Planner decision reason.

6. Effect:
   Suppresses failover candidate/proposal creation by skipping the `else` branch that builds `failover_candidates`.

   It does not suppress apply directly. It does not filter selected moves directly. It explains and causes an already rejected keep/none decision.

7. Could removing this producer allow L3 failover?
   Partially proven:
   - Removing this producer can allow L3 failover proposal creation. Commit `8a8e38a6` did exactly that: tests changed from `candidate_moves_total=0` to `candidate_moves_total=1`, and decision became `action=switch`, `move_type=failover`.
   - Removing it alone does not prove Runtime movement would occur, because current code still blocks selected moves at the restore-barrier execution gate unless approval/emergency conditions pass.

## Correction Direction

Do not classify `restore_barrier_failover_suppressed` itself as a Runtime or execution blocker.

Correct classification:
- legacy Planner pre-selection suppression reason
- produced in `_decision_for_user`
- consumed mostly by tests/reports
- prevents failover proposal creation before selected moves exist

Correction direction:
- preserve proposal visibility;
- keep execution/apply blocking in post-selection restore-barrier gates;
- update reports to distinguish legacy `restore_barrier_failover_suppressed` from current `restore_barrier_execution_blocked`.
