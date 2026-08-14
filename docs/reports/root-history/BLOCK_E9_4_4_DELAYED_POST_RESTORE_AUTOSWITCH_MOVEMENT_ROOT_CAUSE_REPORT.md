# BLOCK E9.4.4 — Delayed Post-Restore Autoswitch Movement Root-Cause Report

Mode: read-only / delayed autoswitch root-cause only.

## Executive Verdict

```text
delayed_movement_root_cause=telegram_hard_block_recurred_after_clean_gate
root_cause_classification=MIXED_TELEGRAM_HARD_BLOCK_RECURRENCE_AND_CLEAN_GATE_WINDOW_TOO_SHORT
confidence=high
moved_users=10.7.0.5,10.0.0.2,10.0.0.3
movement_count=3
max_failover_behavior_expected=true
clean_gate_failure_reason=single clean restore gate did not span enough autoswitch timer/service-signal cycles
restore_governance_live_proven=false
apply_restore_model_safe=false
additional_policy_fix_required=true
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## What Happened

E9.4.2 restored `v7-users-autoswitch.timer` after a clean final planner gate:

```text
final_planner_selected_moves=0
final_telegram_hard_blocked=false
egress_1_eligible=true
actual_movements_count=0 during immediate observation
```

E9.4.3 later found delayed timer-driven movement:

```text
10.7.0.5: 1 -> vless
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
movement_ts=2026-05-26T07:29:08Z
```

## Root Cause

The clean gate was real, but it sampled a soft state:

```text
telegram.status=DOWN_GRACE
telegram.hard_blocked=false
selected_moves=0
```

The later apply timer cycle sampled a hard state:

```text
telegram.status=TELEGRAM_DOWN_14S
telegram.hard_blocked=true
egress_1_blocker=telegram_required_telegram_down_14s
candidate_moves_total=16
selected_moves=3
```

The policy then did expected failover mechanics: current egress `1` was globally ineligible for Telegram-required users, and `vless` was the eligible target. Runtime `failover_limit=3` capped the broad candidate set to exactly three selected users.

## Per-User Result

| User | From | To | Table | Reason |
|---|---|---|---:|---|
| `10.7.0.5` | `1` | `vless` | `1003` | `current_egress_not_eligible` via `telegram_required_telegram_down_14s` |
| `10.0.0.2` | `1` | `vless` | `100` | `current_egress_not_eligible` via `telegram_required_telegram_down_14s` |
| `10.0.0.3` | `1` | `vless` | `101` | `current_egress_not_eligible` via `telegram_required_telegram_down_14s` |

## Was This Expected?

Mechanically, yes. Governance-wise, no.

The autoswitch timer behaved normally once restored. The movement was not manual apply, not `v7-user-switch` by this block, and not hidden `v7-routing-sync`. But the restore model treated a short clean gate plus immediate no-op as enough, and that was too weak for canary attribution.

## Clean Gate Failure

```text
classification=CLEAN_GATE_WINDOW_TOO_SHORT
```

The gate did not require:

- multiple consecutive zero-selected-move samples;
- observation across full apply timer periods;
- Telegram hard-block absence across a persistence window;
- delayed post-restore settle before declaring restore proven.

## Governance Implication

Current apply restore model is not safe enough for canary attribution:

```text
restore_governance_live_proven=false
apply_restore_model_safe=false
next_canary_readiness=NO-GO
```

Future restore must include:

1. `N>=3` consecutive planner-only samples with `selected_moves=0`.
2. Samples spanning at least two full apply timer intervals.
3. Telegram hard-block absent through the whole window.
4. Apply restore followed by delayed settle across at least two full apply timer intervals.
5. Movement budget and classification separate from canary blast radius.

## Recommended Next Step

Design and implement a restore settle gate:

```text
BLOCK E9.4.5 = delayed restore settle gate / post-apply guard design
```

The fix should be governance/tooling first. A code-level policy guard may also be needed if the platform wants `max_apply_movements=0` or a suppression window for first restore cycles.

## Verification

```text
tools/v7-run-tests=PASS
targeted_autoswitch_policy_tests=PASS
tools/v7-control-plane-governance-check --pretty=PASS
tools/v7-second-canary-target-readiness --pretty=PASS current_readiness=NO-GO selected_target=NONE
tools/v7-second-canary-target-readiness --json=PASS
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty=PASS warnings=runtime_manifest_not_supplied
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty=PASS warnings=runtime_manifest_missing_locally_or_not_supplied,source_worktree_dirty,known_43_production_only_tools_require_lineage,archive_manifest_missing_locally_or_not_supplied
py_compile admin/tools/governance/autoswitch=PASS
git diff --check=PASS
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
