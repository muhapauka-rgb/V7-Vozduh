# BLOCK E9.4.6 — Fresh Restore Settle Gate Observation Report

## Executive Verdict

```text
fresh_restore_settle_observation_executed=true
current_restore_settle_status=GO
restore_governance_live_proven=true
next_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

E9.4.6 collected a fresh read-only settle window after the earlier Telegram hard-block recurrence. The fresh window is clean: `selected_moves=0` in every sample, Telegram hard-block was absent, egress `1` stayed eligible, registry hashes stayed stable, and runtime checks remained OK.

This does not authorize canary execution. It means the project can return to a fresh approval-packet stage.

## Authority Snapshot

Source: `docs/track7/control-plane/e9_4_6-evidence/current-authority-snapshot.txt`

```text
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
manual_autoswitch_apply=false
manual_user_switch=false
manual_routing_sync=false
```

The apply timer was already active from E9.4.2. E9.4.6 did not mutate timer state.

## Fresh Settle Window

Sources:

- `docs/track7/control-plane/e9_4_6-evidence/fresh-settle-samples-combined.txt`
- `docs/track7/control-plane/e9_4_6-evidence/fresh-settle-hash-window.txt`
- `docs/track7/control-plane/e9_4_6-evidence/settle-samples/`

```text
samples_count=3
sample_A=2026-05-26T10:24:28Z
sample_B=2026-05-26T10:25:01Z
sample_C=2026-05-26T10:25:36Z
samples_span_seconds=68
apply_timer_intervals_covered=3.4
required_apply_timer_intervals=2
```

## Gate Results

Fresh pre-restore checker:

```text
gate_status=GO
selected_moves_by_sample=[0,0,0]
telegram_hard_blocked_by_sample=[false,false,false]
egress_1_eligible_by_sample=[true,true,true]
registry_stable=true
egress_registry_stable=true
checkers_ok=true
hidden_movers_observed=false
```

Fresh post-restore checker:

```text
gate_status=GO
movement_count_by_sample=[0,0,0]
recommended_action=post_restore_settle_clean_next_canary_can_return_to_approval_packet_stage
```

## Required Answers

```text
fresh_restore_settle_observation_executed=true
current_restore_settle_status=GO
samples_count=3
samples_span_seconds=68
apply_timer_intervals_covered=3.4
selected_moves_all_zero=true
telegram_hard_blocked_seen=false
egress_1_eligible_all_samples=true
users.registry_stable=true
egress.registry_stable=true
runtime_checks_ok=true
new_delayed_movements_observed=false
restore_governance_live_proven=true
next_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

## Interpretation

The earlier E9.4.3/E9.4.4 delayed movement remains a real historical restore-governance failure and is not erased by this block. E9.4.6 proves that the current runtime can now sustain a clean settle window across more than two apply timer intervals.

Because this was only observation, the next safe step is not live canary. The next safe step is a fresh canary or target-selection approval packet that uses the current registry truth.

## Recommended Next Step

```text
recommended_next_step=prepare_fresh_next_canary_approval_packet_or_target_refresh
```

Before any new canary:

- collect a fresh target/candidate snapshot;
- rerun `v7-second-canary-target-readiness`;
- preserve staged restore governance;
- require explicit operator approval for any live movement.

## Verification

```text
tools/v7-run-tests=PASS
targeted_autoswitch_policy_tests=PASS
restore_settle_gate_tests=PASS
tools/v7-control-plane-governance-check --pretty=PASS
tools/v7-restore-settle-gate --pre-restore --pretty=PASS_READ_ONLY_DEFAULT_E9_4_4_NO_GO
tools/v7-restore-settle-gate --pre-restore --json=PASS_READ_ONLY_DEFAULT_E9_4_4_NO_GO
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/control-plane/e9_4_6-evidence/settle-samples --pretty=PASS_GO
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/control-plane/e9_4_6-evidence/settle-samples --json=PASS_GO
tools/v7-second-canary-target-readiness --pretty=PASS_READ_ONLY_NO_GO
tools/v7-second-canary-target-readiness --json=PASS_READ_ONLY_NO_GO
tools/v7-runtime-repo-diff=PASS_WITH_WARNING_runtime_manifest_not_supplied
tools/v7-release-lineage-check=PASS_WITH_KNOWN_WARNINGS
py_compile=PASS
git diff --check=PASS
```

Known release-lineage warnings:

- `runtime_manifest_missing_locally_or_not_supplied`
- `source_worktree_dirty`
- `known_43_production_only_tools_require_lineage`
- `archive_manifest_missing_locally_or_not_supplied`

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
