# PROGRAM D - Autonomy, Failure, Blast Radius And Production Runtime Certification

Project: V7 Vozduh  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Final commit under test: `9b2268834e954d2267fbb8804a1fc4c683f81d72`  
Evidence folder: `program_d_evidence`

## Final Result

PROGRAM D does not reach PASS.

Single proven blocker:

`blast_radius_5_blocked_by_production_policy_limit`

Production has enough candidate users for blast 5, but the active production policy caps failover selection at 3:

- `/etc/v7/policy.json`: `autoswitch_max_failover_per_run=3`
- requested Program D blast radius: `--max-selected-moves 5`
- planner candidate switch decisions: 12
- planner pre-guard selected moves: 3
- restore-barrier guard verdict: `restore_barrier_clearance_selected_moves_exceed_budget`
- operation terminal state: `DRY_RUN`

Raising this limit is a policy change and is outside Program D's allowed scope. No policy bypass, manual route mutation, direct user switch, or alternate rollback path was used.

## Discovery Gate

Fresh truth checks were executed before and after runtime work.

Final truth:

- `runtime_access_status=READY`
- `runtime_truth_status=KNOWN`
- `state_truth_status=KNOWN`
- `convergence_status=FULLY_ALIGNED`
- `final_verdict=PASS`
- warning: `documentation_dirty_ignored`

Evidence:

- `program_d_evidence/phase0_truth_check.txt`
- `program_d_evidence/phase3_after_packet_fix_truth_check.txt`
- `program_d_evidence/final_truth_check_after_phase4_rollback.txt`
- `program_d_evidence/remote_program_d_execution_summary.json`

## Runtime Ownership

Existing ownership was reused and extended only where contradictory internal ownership blocked Program D:

| Authority | Owner | Program D result |
| --- | --- | --- |
| Runtime planner | `/usr/local/bin/v7-users-autoswitch` | Reused |
| Approval packet | `/usr/local/bin/v7-operator-execution-packet`, `admin_core/operator_execution.py` | Reused, fixed selected-count consistency |
| Restore barrier lifecycle | `admin_core/operator_execution.py` | Reused |
| Runtime execution | `/usr/local/bin/v7-users-autoswitch --apply --verify` | Reused |
| Operation-scoped rollback | `/usr/local/bin/v7-users-autoswitch --rollback-packet --apply --verify` | Reused, fixed bounded multi-user rollback |
| Audit/closure | existing autoswitch/operator audit and closure records | Reused |

No parallel orchestrator, duplicate execution path, duplicate rollback path, manual bypass, service restart, timer change, or policy mutation was introduced.

## Root Cause Closures During Program D

### 1. Approval Packet Selected-Move Mismatch

Failure observed:

- blast1 packet generation initially failed with `rollback_manifest_count_mismatch`.

Root cause:

- `admin_core/operator_execution.py:selected_moves_from_plan()` used all switch decisions when building rollback manifest constraints, even when planner restore-barrier data already carried a capped `clearance_selected_moves_before_guard`.

Fix:

- `selected_moves_from_plan()` now truncates moves to the restore-barrier selected count before packet constraints and rollback manifest construction.

Tests:

- `program_d_evidence/test_operator_execution_packet_selected_count_fix.txt`
- `program_d_evidence/test_full_unittest_discover_selected_count_fix.txt`

Commit:

- `6b261d6a62c60f8f1f66a3626c996da349b4f5c7`

### 2. Bounded Multi-User Rollback Rejection

Failure observed:

- blast2 forward apply succeeded for 2 users.
- operation-scoped rollback packet was generated for 2 users.
- rollback validator rejected its own generated packet with `rollback_scope_exceeds_one_user`.

Root cause:

- rollback packet generator set `max_rollback_users=len(items)`, but `_validate_rollback_packet()` still had a hard-coded single-user rollback ceiling.

Fix:

- rollback validator now honors `max_rollback_users` and still rejects empty, over-budget, mismatched, missing-user, wrong-target, and lineage-invalid packets.

Tests:

- `program_d_evidence/test_v7_users_autoswitch_policy_multi_user_rollback.txt`
- `program_d_evidence/test_full_unittest_discover_multi_user_rollback.txt`

Commit:

- `9b2268834e954d2267fbb8804a1fc4c683f81d72`

## Certified Phases

### Phase 1 - Autonomy

Systemd ownership was discovered read-only:

- `v7-users-autoswitch.timer`: present, enabled, inactive at inspection time
- `v7-users-autoswitch.service`: present, inactive at inspection time

Evidence:

- `program_d_evidence/phase0_runtime_discovery.txt`
- `program_d_evidence/remote_program_d_execution_summary.json`

### Phase 2 - Failure Handling

Fail-closed behavior was observed for:

- missing rollback packet
- restore-barrier generation/hash mismatch
- packet path outside repo
- stale/expired restore-barrier clearance

Evidence:

- remote `/tmp/program_d/phase2_missing_rollback_packet.json`
- remote `/tmp/program_d/phase2_generation_hash_mismatch.json`
- local summary: `program_d_evidence/remote_program_d_execution_summary.json`

### Phase 3 - Blast Radius 1

Result: PASS after selected-move packet fix.

- approval packet selected count: 1
- clearance: `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- forward operation: `APPLIED`
- selected user: `10.0.0.2`
- operation-scoped rollback: `ROLLBACK_COMPLETED`
- rollback rows: 1
- route verification: rc 0

Evidence:

- remote `/tmp/program_d/phase3_blast1_*`
- local summary: `program_d_evidence/remote_program_d_execution_summary.json`

### Phase 4 - Blast Radius 2

Result: PASS after bounded multi-user rollback fix.

- approval packet selected count: 2
- clearance: `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- forward operation: `APPLIED`
- selected users: `10.0.0.3`, `10.0.0.6`
- initial rollback denial exposed the one-user ceiling defect
- after fix and deploy: `ROLLBACK_COMPLETED`
- rollback rows: 2
- route verification: rc 0

Evidence:

- remote `/tmp/program_d/phase4_blast2_*`
- local summary: `program_d_evidence/remote_program_d_execution_summary.json`

### Phase 5 - Blast Radius 5

Result: BLOCKED.

Read-only readiness plan:

- requested max selected moves: 5
- candidate switch decisions: 12
- production failover limit: 3
- selected before guard: 3
- selected after guard: 0
- terminal reason: `dry_run_restore_barrier_clearance_selected_moves_exceed_budget`

The next legal blast level cannot be certified without a production policy change.

## Not Reached

These phases were not certified because Program D must stop at the first proven blocker:

- blast radius 10
- blast radius 25
- service-aware routing production certification beyond observed planner evidence
- capacity-aware routing production certification beyond observed planner evidence
- full production runtime certification
- runtime platform certification

## Final Verdicts

```text
autonomy_certified=false
fail_closed_certified=true
blast_radius_1_pass=true
blast_radius_2_pass=true
blast_radius_5_pass=false
blast_radius_10_pass=false
blast_radius_25_pass=false
service_aware_routing_certified=false
capacity_aware_routing_certified=false
production_runtime_certified=false
runtime_platform_certified=false
program_d_final=BLOCKED
single_proven_blocker=blast_radius_5_blocked_by_production_policy_limit
safe_to_continue_without_policy_change=false
```

