# Execution Path Identity Forensics

Timestamp: 2026-07-01_215211 Asia/Bangkok

Mode: READ_ONLY_FORENSIC

Code modified: NO
Runtime modified: NO
Planner modified: NO
Production modified: NO
Users moved: 0
Deploy performed: NO

## Verdict

```text
INVESTIGATION_SWITCHED_CANDIDATE
```

The investigation did not preserve one execution identity across the later forensic reports.

The first switch happened in:

```text
docs/reports/engineering/2026-07-01_212850_maximum_speed_autoswitch_forensic_sprint.md
```

Previous candidate:

```text
user: 10.7.0.5
source: awg0
target: vless
action: switch
move_type: failover
reason: current_egress_not_eligible
current_failures: []
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
```

New candidate:

```text
user: 10.0.0.2
source: openvpn-1779388847-d2ad7c
target: vless
action: keep
move_type: none
reason: restore_barrier_failover_suppressed
selected_move_for_candidate: null
```

## Evidence Boundary

This report uses only persisted reports and persisted artifacts. It does not reconstruct a missing Planner candidate.

The raw full Planner plan/candidate row for the original July L3 Production Validation candidate was not persisted:

```text
decision.user_ip == 10.7.0.5
decision.current_egress == awg0
decision.recommended_egress == vless
candidate.egress == awg0
```

This absence is explicitly documented in:

- `docs/reports/engineering/2026-07-01_191923_eligibility_root_cause_proof.md`, lines 155-176 and 198-246.
- `docs/reports/engineering/2026-07-01_193615_planner_candidate_evidence_recovery.md`, lines 16-29, 101-128, and 420-455.

## Candidate A Identity

Source lineage: original L3 Production Validation / awg0 failover candidate.

| Field | Persisted value |
| --- | --- |
| operation_id | `NOT_PERSISTED_FOR_RAW_CANDIDATE` |
| generation_id | `NOT_PERSISTED_FOR_RAW_CANDIDATE` |
| planner_generation | `NOT_PERSISTED_FOR_RAW_CANDIDATE` |
| user | `10.7.0.5` |
| source | `awg0` |
| target | `vless` |
| action | `switch` |
| move_type | `failover` |
| reason | `current_egress_not_eligible` |
| selected_move_hash | `NOT_PERSISTED_FOR_RAW_CANDIDATE` |
| selected_move_exists | `YES`, as reconstructed/report evidence |
| approved_plan_lock | `reported preserved / validation ok`, exact object not persisted here |
| restore_barrier_generation | `NOT_PERSISTED_FOR_RAW_CANDIDATE` |
| planner object path | `NOT_FOUND`; reconstructed in reports |
| artifact filename | no raw Planner artifact found; report evidence only |

Direct persisted report evidence:

- `2026-07-01_185831_world_model_provenance_trace.md` lines 9-17 identifies `10.7.0.5 / awg0 / vless`, reason `current_egress_not_eligible`, `move_type=failover`.
- Lines 19-26 identify `current_failures: []`, blockers `required_service_failure_required` and `confirmed_l3_wake_required`.
- Lines 60-70 repeat the candidate identity and Runtime evidence.
- Lines 162-168 state the selected move after Planner was `10.7.0.5 awg0 -> vless`, and Runtime derived no current failures.
- `2026-07-01_150144_system_invariant_proof.md` lines 95-99 identify selected move `10.7.0.5 awg0 -> vless`, reason `current_egress_not_eligible`, `move_evidence.current_failures: []`, and blocker `required_service_failure_required`.
- Lines 247-258 identify `final_verdict: STOP_SAFE`, selected user/source/target, approved lock validation ok, blockers, and empty current failures.

## Candidate B Identity

Source lineage: later OpenVPN persisted fixture candidate.

| Field | Persisted value |
| --- | --- |
| operation_id | `runtime_autoswitch_7d1a84de540d525fa249ac22` |
| generation_id | no separate generic `generation_id` field used for the candidate; operation has `planner_generation_id` |
| planner_generation | `5ac20d4906a172d0bdb9f8ecd5de019cdc9e054a967439c72730910538b8dc2e` |
| user | `10.0.0.2` |
| source | `openvpn-1779388847-d2ad7c` |
| target | `vless` |
| action | `keep` |
| move_type | `none` |
| reason | `restore_barrier_failover_suppressed` |
| selected_move_hash | `dd37cb09bf92e82e042f428ff0eda4bfe45a03c8db443c95fbe3587349849fe7`, belongs to unrelated plan selected move |
| selected_move_exists | `NO` for this candidate; `YES` for unrelated rebalance selected move |
| approved_plan_lock | `null` for the frozen candidate |
| restore_barrier_generation | no explicit generation persisted in frozen object; restore barrier fields persisted |
| planner object path | `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_all_no_target.json` |
| artifact filename | `fixture_all_no_target.json` |

Direct persisted artifact/report evidence:

- `2026-07-01_212850_maximum_speed_autoswitch_forensic_sprint.md` lines 38-45 identify `fixture_all_no_target.json`, operation id, planner generation id, and freshness boundary.
- Lines 54-60 identify `action=keep`, `move_type=none`, `recommended_egress=openvpn-1779388847-d2ad7c`, reason `restore_barrier_failover_suppressed`, sample user `10.0.0.2`.
- Lines 62-79 identify the source candidate and eligible target candidates including `vless`.
- Lines 84-89 identify the unrelated selected move `10.7.0.16 wireguard-1779454504-c43409 -> vless`, `move_type=rebalance`.
- `2026-07-01_214225_planner_vs_runtime_truth_court.md` lines 47-52 choose the OpenVPN fixture as the court object.
- Lines 61-112 freeze the candidate as `10.0.0.2 / openvpn-1779388847-d2ad7c / vless`, `action=keep`, `move_type=none`, reason `restore_barrier_failover_suppressed`, `approved_plan_lock=null`, selected hash `dd37...`, and `selected_move_for_candidate=null`.
- Lines 116-118 explicitly state that the operation hash belongs to an unrelated rebalance move and the frozen OpenVPN candidate has no selected move.

## Candidate Timeline

| Report | Candidate identity | Same as previous? | Reason for change | Intentional? | Evidence |
| --- | --- | --- | --- | --- | --- |
| `2026-07-01_185831_world_model_provenance_trace.md` | A: `10.7.0.5 / awg0 / vless`, `switch`, `failover`, `current_egress_not_eligible`, `current_failures=[]`, `confirmed_l3_wake_required` | N/A | First report in this identity audit set | N/A | Lines 9-17, 19-26, 60-70, 162-168 |
| `2026-07-01_191923_eligibility_root_cause_proof.md` | A: `10.7.0.5 / awg0 / vless`, `failover`, `current_egress_not_eligible`; raw current candidate not persisted | YES | Same explicit requested target | YES | Lines 12-18, 139-155, 198-246, 268-305 |
| `2026-07-01_212850_maximum_speed_autoswitch_forensic_sprint.md` | B: `10.0.0.2 / openvpn-1779388847-d2ad7c / vless`, `keep`, `none`, `restore_barrier_failover_suppressed`; plan selected unrelated rebalance | NO | Investigation changed to a full persisted OpenVPN fixture because the original raw A candidate was unavailable and the sprint targeted the real failed OpenVPN incident | Scope change YES; identity replacement was not explicitly documented as discontinuity from A | Lines 28-45, 54-60, 76-89, 206-214 |
| `2026-07-01_213255_restore_barrier_failover_suppressed_producer_trace.md` | B reason lineage only: `restore_barrier_failover_suppressed` from historical `_decision_for_user`; persisted in `fixture_all_no_target.json` | YES relative to B; NO relative to A | It traces the B-only reason introduced by the previous report | YES for B | Lines 11-15, 57-83, 171-176, 192-220 |
| `2026-07-01_214225_planner_vs_runtime_truth_court.md` | B frozen candidate: `10.0.0.2 / openvpn-1779388847-d2ad7c / vless`, `keep`, `none`, no selected move for candidate | YES relative to B; NO relative to A | Court selected latest non-counterfactual full persisted OpenVPN incident artifact | YES for B, but not a continuation of A | Lines 45-55, 61-118, 153-169, 177-233 |

## Special Checks

### A vs B same execution object?

```text
NO
```

They differ on user, source, action, move_type, reason, selected-move existence, raw artifact availability, and report lineage.

### Same Planner generation?

```text
NO / NOT PROVABLE SAME
```

B has persisted planner generation:

```text
5ac20d4906a172d0bdb9f8ecd5de019cdc9e054a967439c72730910538b8dc2e
```

A's raw Planner plan/generation was not persisted in the available evidence. There is no persisted identity field proving A shares B's generation.

### Same operation_id?

```text
NO / NOT PROVABLE SAME
```

B has:

```text
runtime_autoswitch_7d1a84de540d525fa249ac22
```

A's raw operation id was not persisted in the candidate evidence.

### Same selected_move_hash?

```text
NO / NOT PROVABLE SAME
```

B has:

```text
dd37cb09bf92e82e042f428ff0eda4bfe45a03c8db443c95fbe3587349849fe7
```

That hash belongs to an unrelated rebalance selected move, not to the OpenVPN candidate. A's hash was not persisted in the available raw candidate evidence.

### Same report lineage?

```text
NO
```

A lineage:

```text
L3 Production Validation selected move
10.7.0.5 awg0 -> vless
current_egress_not_eligible
current_failures=[]
confirmed_l3_wake_required
STOP_SAFE
```

B lineage:

```text
fixture_all_no_target.json
10.0.0.2 openvpn-1779388847-d2ad7c -> vless
keep / none
restore_barrier_failover_suppressed
selected_move_for_candidate=null
unrelated selected rebalance exists
```

### Same production validation attempt?

```text
NO / NOT PROVABLE SAME
```

A is the failed L3 Production Validation candidate. B is a dry-run historical autoswitch operation with `apply_result.reason=dry_run` and an unrelated selected rebalance. No persisted field ties them to the same production-validation execution identity.

### Same production incident?

```text
NO AS EXECUTION OBJECT
```

Both discussions reference OpenVPN-world failure context in the broad historical investigation, but the execution objects are different. Evidence of an OpenVPN failed channel cannot make `10.7.0.5 / awg0 / vless / failover` the same candidate as `10.0.0.2 / openvpn-1779388847-d2ad7c / vless / keep`.

### When exactly did the investigation switch?

```text
2026-07-01_212850_maximum_speed_autoswitch_forensic_sprint.md
```

The report scope changes to:

```text
source channel: openvpn-1779388847-d2ad7c
primary historical source object: fixture_all_no_target.json
sample user: 10.0.0.2
action: keep
move_type: none
reason: restore_barrier_failover_suppressed
```

### Who switched it?

```text
Codex, following the new Maximum Speed Autoswitch Forensic Sprint scope and the historical artifact limitation for A.
```

The user task changed the target to the real failed OpenVPN incident. The previous evidence recovery had already established that A's raw Planner candidate was not persisted.

### Was the switch explicitly documented?

```text
PARTIAL / NO
```

The Maximum Speed Sprint explicitly documented the new OpenVPN scope and source artifact, but it did not explicitly state:

```text
This is a different execution candidate from 10.7.0.5 / awg0 / vless / failover.
```

### Did later conclusions accidentally use B to explain A?

```text
YES, if read as a continuous root-cause lineage.
```

The following conclusions are valid only for B and must not be used as proof for A:

- `AUTHORITY_RESTORE_LOCK_DEFECT`
- `restore_barrier_failover_suppressed` as the first actionable blocker
- `AutoswitchPlanner._decision_for_user` line 1156 as first producer for the original A candidate
- `NO_DISAGREEMENT_STOP_SAFE_CORRECT` for the original A Planner-vs-Runtime dispute

### Does Truth Court investigate the same candidate that produced current_failures=[], confirmed_l3_wake_required, STOP_SAFE?

```text
NO
```

The `current_failures=[]`, `confirmed_l3_wake_required`, `STOP_SAFE` evidence belongs to A:

```text
10.7.0.5 / awg0 / vless / failover / current_egress_not_eligible
```

The Truth Court froze B:

```text
10.0.0.2 / openvpn-1779388847-d2ad7c / vless / keep / none / restore_barrier_failover_suppressed
```

The Truth Court's no-disagreement proof is therefore a correct internal proof for B, but it is not a verdict on A.

## Reclassification

Conclusions that remain valid for A:

- The raw A Planner candidate was not found.
- A reached reports as `10.7.0.5 / awg0 / vless / failover / current_egress_not_eligible`.
- A later had `current_failures=[]` and blockers including `required_service_failure_required` and `confirmed_l3_wake_required`.
- The exact first `_candidate()` gate for A remains unproven because the raw candidate row and ordered gate trace were not persisted.

Conclusions that must be reclassified as B-only:

- `restore_barrier_failover_suppressed` producer trace.
- `AUTHORITY_RESTORE_LOCK_DEFECT` from the Maximum Speed Sprint.
- Truth Court `NO_DISAGREEMENT_STOP_SAFE_CORRECT`.
- Any claim that restore barrier suppression explains A's `current_egress_not_eligible` / `failover` selected move.

## Report To Rerun

Rerun:

```text
Planner vs Runtime Truth Court
```

using the original A identity:

```text
10.7.0.5 / awg0 / vless / failover / current_egress_not_eligible
```

Current blocker:

```text
The raw full Planner object for A was not persisted, so a strict same-object court cannot be completed until that object is recovered or a new production-validation attempt persists the full candidate identity and candidate row.
```

If no A raw object is recovered, the strongest permissible verdict remains evidence-limited, not restore-barrier-based.

## Final Verdict

```text
INVESTIGATION_SWITCHED_CANDIDATE
```
