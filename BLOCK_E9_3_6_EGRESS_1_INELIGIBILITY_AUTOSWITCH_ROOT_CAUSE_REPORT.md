# Block E9.3.6 — Egress 1 Ineligibility and Autoswitch Candidate Root-Cause Report

Mode: read-only autoswitch root-cause analysis.

## Executive Verdict

E9.3.5 apply restore was aborted because the final planner-only sample saw egress `1` as ineligible for users currently assigned to it. The hard blocker in that sample was `service_instagram_failed`; Telegram was degraded but not hard-blocking. The planner then selected `vless` as the best eligible failover target and capped immediate selected moves at 3 under `autoswitch_max_failover_per_run=3`.

Fresh E9.3.6 read-only evidence shows egress `1` can become eligible again in later planner samples, with checkers OK and routes intact. The root cause is therefore not a stable route/datapath failure. It is a transient service signal interacting with expected autoswitch failover policy.

## Required Answers

```text
egress_1_ineligibility_root_cause=service_instagram_failed hard service gate in E9.3.5 final planner sample
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
confidence=high_for_abort_sample_medium_for_current_stability
candidate_moves_count=15
selected_moves_count=3
selected_moves_summary=10.0.0.2:1->vless,10.0.0.3:1->vless,10.0.0.6:1->vless
vless_target_reason=best eligible failover target with service checks OK and load OK
max_failover_behavior_expected=true
apply_restore_safe_now=false
apply_should_remain_held=true
execution_allowed_now=false
```

## Evidence

- Current autoswitch/runtime snapshot: `docs/track7/control-plane/e9_3_6-evidence/current-autoswitch-snapshot.txt`
- Egress 1 ineligibility analysis: `docs/track7/control-plane/e9_3_6-evidence/egress-1-ineligibility.md`
- Candidate move matrix: `docs/track7/control-plane/e9_3_6-evidence/candidate-move-matrix.md`
- Autoswitch policy/source analysis: `docs/track7/control-plane/e9_3_6-evidence/autoswitch-policy-analysis.md`

## Current Authority State

Read-only snapshot:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
```

No `v7-user-switch` or `v7-routing-sync` process was observed in the snapshot. The apply timer remained held.

## Runtime Health

```text
v7-reconcile-check=OK
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
```

Current route reality shows all enabled users now assigned to egress `1`, with route tables defaulting to `v7e356a192b79`. This is coherent with registry state and does not show routing drift.

## Root Cause Detail

At E9.3.5 abort time:

```text
egress=1
eligible=false
blocked=["service_instagram_failed"]
telegram.status=DEGRADED
telegram.hard_blocked=false
load.status=OK
```

Source semantics:

- `service_instagram_failed` is a hard service gate.
- Telegram degraded is not hard by itself; it adds a reason/score penalty unless hard-blocked.
- When current egress is not eligible, autoswitch enters failover mode and appends `current_egress_not_eligible`.
- Selected failovers are capped by `autoswitch_max_failover_per_run`.

## Candidate Movement Scope

The planner saw 15 users on egress `1` as failover candidates to `vless`, but selected only three:

```text
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
10.0.0.6: 1 -> vless
```

This is expected under current max-failover behavior, but still unsafe to apply without explicit operator approval because subsequent timer runs could continue movement if the signal persists.

## Restore Implication

Apply restore is not safe right now under the zero-move approval model. The apply timer should remain held.

Acceptable next paths:

1. Wait for a fresh final planner-only sample with `selected_moves=0`, then repeat E9.3.5.
2. Approve a bounded apply restore with exact accepted users and `max_apply_movements=3`.
3. Design/fix autoswitch policy so transient service failures do not immediately produce broad candidate movement, then reassess.

## Verification

```text
tools/v7-run-tests: OK, 49 tests
tools/v7-control-plane-governance-check --pretty: OK
tools/v7-second-canary-target-readiness --pretty: OK, second_canary_readiness=NO-GO
tools/v7-second-canary-target-readiness --json: OK, mutation=false
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, runtime_governance=partial
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release_object ready, provenance incomplete
py_compile admin/tools/governance: OK
git diff --check: OK
```

Release/governance warnings remain expected for this track: runtime manifest is not supplied locally, source worktree is dirty, release provenance remains incomplete, and unresolved production-only lineage remains outside this root-cause block.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
