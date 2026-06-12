# PROGRAM BA2.GATE - TWO USER AUTONOMY POLICY ESCALATION AND CERTIFICATION

## Executive Summary

Verdict: **TWO_USER_AUTONOMY_BLOCKED**

BA2.GATE proved that the canonical autonomy policy can be raised from `1` to `2` through the existing admin policy owner, and the planner can produce a real 2-user candidate set under the existing POOL authority budget.

However, the program did **not** execute user movement. The runtime safety chain stopped before apply because the post-clearance dry-run detected an atomic restore-barrier mismatch caused by source bundle drift:

- `quality_summary`
- `service_matrix`

This is not a planner blocker, not an authority-budget blocker, and not a candidate-count blocker. It is a runtime atomicity/source-stability blocker.

Because execution was blocked, the temporary policy escalation was reverted from `2` back to `1`, the temporary 2-user restore-barrier clearance was expired, and final truth/convergence returned to PASS.

## Evidence

Evidence folder: `BA2_GATE_EVIDENCE/`

Key evidence:

- `phase1_policy_before.json`
- `phase3_policy_after.json`
- `phase4_truth_gate.json`
- `phase4_convergence_gate.json`
- `phase5_two_user_fresh_planner.json`
- `phase5_two_user_packet_summary.json`
- `phase5_two_user_restore_barrier_summary_retry3.json`
- `phase5_two_user_post_clearance_dry_run_target_awg0.json`
- `phase7_policy_after_revert.json`
- `phase7_safety_post_expiry_dry_run_summary.json`
- `phase7_final_truth_gate.json`
- `phase7_final_convergence_gate.json`
- `phase7_final_post_refresh_dry_run_summary.json`

## Phase 1 - Policy Reality Audit

Canonical policy owner:

- Admin API policy file: `/etc/v7/policy.json`
- Admin API path: `/api/actions/policy-update`
- Code owner: `admin/v7-admin-api`
- Runtime consumer: `tools/v7-users-autoswitch`

Local references:

- `admin/v7-admin-api`: `POLICY_FILE = /etc/v7/policy.json`
- `admin/v7-admin-api`: `update_policy(actor, patch)`
- `tools/v7-users-autoswitch`: default policy file `/etc/v7/policy.json`
- `tools/v7-users-autoswitch`: consumes `autoswitch_max_planned_per_run`

Policy before escalation:

```json
{
  "autoswitch_max_planned_per_run": 1,
  "autoswitch_max_failover_per_run": 25,
  "autoswitch_mode": "guarded",
  "autoswitch_enabled": true
}
```

## Phase 2 - Policy Escalation Review

Current authority budget was already sufficient:

```json
{
  "authority_class": "POOL",
  "current_allowed_user_budget": 25
}
```

The blocking value was the narrower autonomy policy:

```json
{
  "autoswitch_max_planned_per_run": 1
}
```

Raising this to `2` was safe to test because:

- POOL authority budget already allowed up to 25.
- The change used the canonical admin policy endpoint.
- No planner, governance, restore-barrier, execution, or truth-source code was changed.
- The program still required fresh planner, fresh packet, fresh restore barrier, and dry-run recheck before apply.

## Phase 3 - Policy Update

Policy patch applied through the canonical owner:

```json
{
  "switch": {
    "autoswitch_max_planned_per_run": 2
  }
}
```

Policy after update:

```json
{
  "autoswitch_max_planned_per_run": 2,
  "autoswitch_max_failover_per_run": 25,
  "autoswitch_mode": "guarded"
}
```

No user movement occurred during the policy update.

## Phase 4 - Truth Gate

After policy escalation:

```json
{
  "truth_check": "PASS",
  "convergence_status": "ALIGNED",
  "convergence_verdict": "PASS",
  "runtime_action_safe": true,
  "runtime_action_status": "READY_FOR_RUNTIME_ACTION"
}
```

## Phase 5 - Two User Autonomy Attempt

Fresh planner with `--max-selected-moves 2` produced a valid 2-user pre-gate selection under POOL authority:

```json
{
  "planned_limit": 2,
  "requested_max_selected_moves": 2,
  "authority_class": "POOL",
  "current_allowed_user_budget": 25,
  "selected_moves_before_gate": 2,
  "selected_moves_after_gate": 2
}
```

Fresh packet was generated for two real planner-selected users:

```json
{
  "packet_id": "pkt_d6cd402b40439ed5f84e90de",
  "operation_id": "govexec_963f8eb8bb7ebac69b1924ea",
  "allowed_users": [
    "10.0.0.2",
    "10.0.0.3"
  ],
  "allowed_targets": [
    "awg0"
  ],
  "selected_move_budget": 2,
  "rollback_items": 2,
  "selected_moves": [
    {
      "user_ip": "10.0.0.2",
      "current_egress": "awg3",
      "recommended_egress": "awg0",
      "move_type": "failover"
    },
    {
      "user_ip": "10.0.0.3",
      "current_egress": "vless",
      "recommended_egress": "awg0",
      "move_type": "rebalance"
    }
  ]
}
```

Fresh restore-barrier clearance was written through the existing runtime-action owner:

```json
{
  "verdict": "ALLOW_RESTORE_BARRIER_CLEARANCE",
  "selected_move_count": 2,
  "selected_move_hash": "ab112e551b4d020a40bc17584afd613a6568d5c54b5cad76da5809320326fc46",
  "clearance_result": "RESTORE_BARRIER_CLEARANCE_WRITTEN",
  "runtime_mutation_scope": "restore_barrier_clearance_only",
  "user_movement": false
}
```

Post-clearance dry-run blocked execution:

```json
{
  "terminal_reason": "dry_run_restore_barrier_clearance_atomic_envelope_id_mismatch",
  "selected_moves": 0,
  "snapshot_gate": {
    "stop_required": false,
    "source_mismatch_families": []
  }
}
```

The blocker was the restore-barrier source bundle lease:

```json
{
  "reason": "restore_barrier_source_bundle_lease_hard_source_changed",
  "changed_source_keys": [
    "quality_summary",
    "service_matrix"
  ]
}
```

This means the runtime did not accept the clearance because the approved atomic envelope no longer matched the current source bundle. The guard worked as designed and prevented apply.

## Phase 6 - Post Execution Review

No execution was performed.

```json
{
  "users_moved": 0,
  "apply_executed": false,
  "routing_changed": false,
  "verification_pass": "not_applicable",
  "rollback_pass": "not_applicable",
  "feedback_pass": "not_applicable",
  "trust_pass": "not_applicable",
  "planner_reuse_pass": "not_applicable"
}
```

## Phase 7 - Safety Revert

Because the two-user execution gate did not pass, the temporary policy escalation was reverted:

```json
{
  "autoswitch_max_planned_per_run": 1,
  "autoswitch_max_failover_per_run": 25,
  "autoswitch_mode": "guarded"
}
```

The temporary 2-user restore-barrier clearance was also expired through a short-lived safety overwrite. Final dry-run confirmed the old clearance is no longer usable:

```json
{
  "terminal_reason": "dry_run_restore_barrier_clearance_generation_expired",
  "selected_move_count": 0,
  "snapshot_stop_required": false,
  "source_mismatch_families": [],
  "planned_limit": 1,
  "authority_class": "POOL",
  "current_allowed_user_budget": 25
}
```

Final truth/convergence:

```json
{
  "truth_check": "PASS",
  "convergence_status": "ALIGNED",
  "convergence_verdict": "PASS",
  "runtime_action_safe": true,
  "runtime_action_status": "READY_FOR_RUNTIME_ACTION"
}
```

## No-Bypass Review

No new planner was created.

No new governance owner was created.

No new execution path was created.

No new truth source was created.

No target substitution occurred.

No user substitution occurred.

No apply was executed.

The stop happened inside the existing restore-barrier/atomic-envelope safety path.

## Final Verdict

Final verdict: **TWO_USER_AUTONOMY_BLOCKED**

Final values:

```json
{
  "policy_owner_identified": true,
  "policy_escalation_tested": true,
  "policy_left_at_2": false,
  "policy_reverted_to_1": true,
  "truth_gate_pass": true,
  "convergence_pass": true,
  "runtime_action_safe": true,
  "two_user_planner_ready": true,
  "two_user_packet_created": true,
  "two_user_restore_barrier_created": true,
  "two_user_execution_gate_pass": false,
  "two_user_autonomy_certified": false,
  "users_moved": 0,
  "apply_executed": false,
  "single_blocker": "restore_barrier_source_bundle_drift_quality_summary_service_matrix",
  "safe_next_step": "BA2.SOURCE_BUNDLE_STABILITY_OR_LEASE_POLICY_REVIEW_BEFORE_TWO_USER_EXECUTION"
}
```

## Plain Language Conclusion

The system is ready to plan and package two-user autonomy, but not yet safe to execute it.

The limit `1 -> 2` is not the real problem anymore. The real problem is that between restore-barrier approval and final runtime recheck, the live quality/service source bundle changed enough that the atomic envelope no longer matched. V7 correctly refused to move users.

Next work should focus only on this blocker:

`quality_summary + service_matrix source bundle drift between clearance and runtime recheck`

Do not retry BA2 execution until that is closed.
