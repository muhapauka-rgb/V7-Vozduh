# Autoswitch Transient Service Signal Policy

Status: repo-side policy implemented in E9.3.8; runtime deploy not performed.
Runtime mutation: no.
Autoswitch apply restore: forbidden until separately approved.

## Problem Statement

E9.3.5 aborted apply restore because planner-only state produced:

```text
selected_moves=3
candidate_moves_total=15
target=vless
reason=current_egress_not_eligible
```

E9.3.6 traced the root cause to:

```text
egress=1
hard blocker=service_instagram_failed
telegram=DEGRADED but not hard-blocked
```

Datapath checks remained OK, so the platform did not prove egress `1` was transport-broken. The dangerous behavior is policy-level: one transient non-Telegram service failure can make an egress globally ineligible and generate broad failover candidates.

## Current Unsafe Semantics

Current source semantics:

```text
non-Telegram service ok=false -> candidate blocked
current candidate blocked -> current_egress_not_eligible
current_egress_not_eligible -> failover path
failover path -> candidate set for all users currently on egress
selected moves limited per run, but candidate set can be broad
```

This is too aggressive for restore stages and canary-adjacent governance because a timer restore may immediately apply a broad failover plan.

## Refined Model

Autoswitch should separate four levels of health:

| Level | Meaning | Movement Authority |
|---|---|---|
| `OK` | Egress passes transport and service checks | Normal scoring |
| `DEGRADED_SERVICE` | One service failed or soft-degraded without persistence | Penalty only, no global failover |
| `CONDITIONAL_INELIGIBLE` | Repeated service failure or multiple critical services failed | Planner may propose bounded movement, apply needs staged approval |
| `HARD_INELIGIBLE` | Interface/transport failure, hard-block sentinel, repeated multi-signal failure | Failover allowed under movement caps |

## Rule 1: Single Service Failure Is Not Global Ineligibility

A single failed non-Telegram service sample should not immediately call `_block(...)` for the whole egress.

Expected behavior:

```text
instagram ok=false one sample
-> candidate.reasons += service_instagram_degraded
-> candidate.score penalty
-> current egress remains eligible
-> selected_moves=0 unless other hard signals exist
```

## Rule 2: Hard Ineligibility Requires Persistence Or Multiple Signals

Hard ineligibility should require one of:

- interface missing/down
- egress state disabled/maintenance/quarantine
- Telegram or sentinel hard-block
- route class fitness `FAIL`
- at least `service_failure_persistence_samples` repeated failures for the same critical service
- at least `service_failure_min_critical_count` critical services failing in the same window
- high-confidence safety quarantine signal

## Rule 3: Service Failures Are Route-Class Signals

Instagram, Telegram, YouTube, Google, and other service failures should first map to service/route-class degradation. They should not automatically imply that every user should leave the egress.

Examples:

```text
instagram failed only -> service-specific degradation
telegram degraded only -> Telegram penalty, not hard failover
youtube + instagram persistent fail -> conditional ineligibility
interface down -> hard ineligibility
```

## Rule 4: Restore Stage Needs Extra Suppression

During staged restore, planner-only observation may show predicted moves. Apply restore should not be permitted unless:

- predicted moves are understood;
- movement count is within the approved bound;
- target egress is eligible under production rules;
- no hidden `v7-user-switch` or `v7-routing-sync` process exists;
- checkers are OK;
- operator approves the apply restore stage separately.

## Rule 5: Max-Failover Limit Remains Necessary But Not Sufficient

`autoswitch_max_failover_per_run` must remain. It limits immediate blast radius but does not solve broad candidate generation.

The refined policy must suppress unsafe candidate generation before movement caps are applied.

## Proposed Decision States

Per egress and route class:

```json
{
  "egress": "1",
  "route_class": "GLOBAL",
  "transport_state": "OK",
  "service_state": "DEGRADED_SERVICE",
  "global_eligibility": "ELIGIBLE",
  "confidence": 0.35,
  "hard_reasons": [],
  "soft_reasons": ["service_instagram_failed_single_sample"],
  "apply_allowed": false
}
```

## E9.3.5 Counterfactual

Under this refined model, E9.3.5 would have produced:

```text
egress_1_state=DEGRADED_SERVICE
global_eligibility=ELIGIBLE
reason=service_instagram_failed_single_sample
selected_moves=0
candidate_moves_total=0 or service-specific warnings only
```

Unless additional persistence or multi-service evidence existed, apply restore would not have been aborted by a broad failover candidate set.

## Governance Status

E9.3.8 implemented this model in repo source:

```text
tools/v7-users-autoswitch
```

Runtime deploy was not performed. Runtime remains unchanged until a separate approval updates:

```text
/usr/local/bin/v7-users-autoswitch
```

Fixture tests prove the E9.3.5 class now produces:

```text
selected_moves_for_single_instagram_failure_after_fix=0
candidate_moves_total_for_single_instagram_failure_after_fix=0
```

No runtime policy was changed. No apply timer was restored. No users were moved.

## E9.3.9 Runtime Deploy Status

The repo-fixed policy was deployed to runtime:

```text
runtime_policy_deployed=true
runtime_path=/usr/local/bin/v7-users-autoswitch
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
backup_path=/usr/local/bin/v7-users-autoswitch.backup.e9_3_9.20260525T213519Z
```

Post-deploy planner-only observation, with apply timer still held:

```text
selected_moves=[]
apply_result=no_selected_moves
single_transient_service_signal_broad_failover_observed=false
```

This confirms the runtime planner no longer reproduced the E9.3.5 broad failover class during the observed post-deploy window. Apply restore still requires separate approval.

## E9.4.1 Post-Policy Root Cause

E9.4.1 classified the non-zero E9.4 final planner gate after the runtime policy deploy.

The deployed policy did not regress the single non-Telegram service failure fix. In the E9.4 abort sample, Instagram was classified as:

```text
service_instagram_degraded
service_instagram_failed_samples_1
service_signal_DEGRADED_SERVICE
```

That is the intended penalty-only behavior.

The actual hard blocker on egress `1` was:

```text
blocked=["telegram_required_telegram_down_14s"]
telegram.status=TELEGRAM_DOWN_14S
telegram.hard_blocked=true
```

Policy implication:

- single non-Telegram service failures remain degraded/penalty-only;
- Telegram hard-block remains a global ineligibility signal under current policy;
- apply restore remains held unless a fresh final planner-only sample returns `selected_moves=0` or the operator explicitly approves the exact movement list.

```text
post_policy_root_cause=telegram_required_telegram_down_14s
root_cause_classification=TELEGRAM_HARD_BLOCK
policy_fix_incomplete=false
apply_should_remain_held=true
```
