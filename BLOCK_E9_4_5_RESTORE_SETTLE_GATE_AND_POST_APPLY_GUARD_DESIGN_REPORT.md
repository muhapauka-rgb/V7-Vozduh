# BLOCK E9.4.5 — Restore Settle Gate and Post-Apply Guard Design Report

Mode: read-only / governance and tooling design only.

## Executive Verdict

```text
restore_settle_gate_rules_created=true
restore_settle_checker_created=true
current_restore_settle_status=NO-GO
pre_restore_required_samples=3
required_apply_timer_intervals=2
post_restore_settle_required=true
additional_policy_fix_required=true
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## Why This Exists

E9.4.2 proved that a final planner gate can be clean at one instant:

```text
selected_moves=0
telegram_hard_blocked=false
egress_1_eligible=true
```

E9.4.3 and E9.4.4 proved that the same restore can still produce delayed timer-driven movement later:

```text
10.7.0.5: 1 -> vless
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
root_cause=telegram_hard_block_recurred_after_clean_gate
```

Therefore a single clean planner gate is insufficient. Restore governance now requires a settle window.

## Rules Created

Created:

```text
docs/track7/control-plane/RESTORE_SETTLE_GATE_RULES.md
```

Pre-restore GO requires:

- at least `3` consecutive samples;
- samples span at least `2` full apply timer intervals;
- every sample has `selected_moves=0`;
- every sample has `telegram.hard_blocked=false`;
- egress `1` remains eligible when users are on egress `1`;
- no hidden `v7-user-switch` or `v7-routing-sync`;
- runtime checkers stay OK;
- `users.registry` and `egress.registry` hashes stay stable.

Post-restore settle requires:

- observation across at least `2` full apply timer intervals;
- `movement_count=0` for a clean restore;
- any movement is classified as autoswitch recovery, not canary movement;
- broad failover keeps the next canary NO-GO.

## Checker Created

Created:

```text
tools/v7-restore-settle-gate
tests/unit/test_v7_restore_settle_gate.py
```

The checker is read-only. It reads saved samples or fixture directories and emits:

```text
gate_status=GO/CONDITIONAL/NO-GO
selected_moves_by_sample
telegram_hard_blocked_by_sample
egress_1_eligible_by_sample
samples_span_seconds
apply_timer_intervals_covered
registry_stable
checkers_ok
hidden_movers_observed
recommended_action
```

It does not run `systemctl`, `v7-users-autoswitch --apply`, `v7-user-switch`, `v7-routing-sync`, `ip`, `nft`, or registry edits.

## Current Checker Result

Saved evidence:

```text
docs/track7/control-plane/e9_4_5-evidence/restore-settle-current-pretty.txt
docs/track7/control-plane/e9_4_5-evidence/restore-settle-current.json
```

Current result:

```text
gate_status=NO-GO
selected_moves_by_sample=[3]
telegram_hard_blocked_by_sample=[true]
egress_1_eligible_by_sample=[false]
movement_count_by_sample=[3]
recommended_action=keep_apply_restore_blocked_until_consecutive_clean_settle_window
```

This result is expected because the E9.4.4 restore-window evidence contains the delayed hard-block/movement class.

## Fixture Tests

Added tests for:

- three clean samples spanning the required interval => GO;
- one sample with `selected_moves>0` => NO-GO;
- Telegram hard-block in one sample => NO-GO;
- egress blocked in one sample => NO-GO;
- registry hash changes => NO-GO;
- too-short window => CONDITIONAL;
- post-restore delayed movement => NO-GO for next canary;
- post-restore no movement across the required window => GO.

## Governance Updates

Updated:

- `APPLY_RESTORE_APPROVAL_RULES.md`
- `STAGED_AUTOSWITCH_RESTORE_MODEL.md`
- `STAGED_CANARY_RESTORE_RUNBOOK.md`
- `CANARY_GO_NO_GO.md`
- `CONTROL_PLANE_RISK_MATRIX.md`
- `tools/v7-control-plane-governance-check`

## Final Answers

```text
restore_settle_gate_rules_created=true
restore_settle_checker_created=true
current_restore_settle_status=NO-GO
pre_restore_required_samples=3
required_apply_timer_intervals=2
post_restore_settle_required=true
additional_policy_fix_required=true
next_canary_readiness=NO-GO
recommended_next_step=run future apply-restore only after restore-settle gate returns GO on fresh evidence
execution_allowed_now=false
```

## Verification

```text
tools/v7-run-tests=PASS
targeted_autoswitch_policy_tests=PASS
restore_settle_gate_tests=PASS
tools/v7-control-plane-governance-check --pretty=PASS current_canary_status=NO-GO_RESTORE_SETTLE_GATE_CURRENTLY_NO_GO
tools/v7-second-canary-target-readiness --pretty=PASS second_canary_readiness=NO-GO
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
