# BLOCK E9.2.1 - Target 1 Load-State Truth Refresh

Mode: read-only / diagnostic only.

Runtime mutation performed: NO
User movement performed by Codex: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO

## Executive Verdict

```text
target_1_load_state_classification=REAL_HIDDEN_LOAD
target_1_ready_for_E9_3=false
waiver_required=true
waiver_acceptable=false
real_hidden_load_detected=true
load_calculator_bug_detected=false
candidate_10.7.0.14_still_valid=true
execution_allowed_now=false
```

`REAL_HIDDEN_LOAD` here means the load was hidden from the E9.2 approval packet snapshot, not hidden after E9.2.1 inspection. E9.2.1 found a concrete current assignment:

```text
10.7.0.5 current=1 table=1003 enabled=1
table 1003 default dev v7e356a192b79
route_get from 10.7.0.5 dev v7e356a192b79 table 1003
```

Therefore `1_users=1` is real current runtime state, not stale E9 residue, not just planner estimate, and not a load calculator bug.

## Key Evidence

E9.2 snapshot:

```text
users.registry_sha256=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
all enabled users appeared current=vless
target_1 load-state showed 1_users=1
```

E9.2.1 snapshot:

```text
users.registry_sha256=f3d22fbfbde9631345c6c07e3dc7fe7b25cad4f9e49ed4f174105bae4ae0515e
10.7.0.5 current=1 table=1003 enabled=1
10.7.0.14 current=vless table=1012 enabled=1
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Interpretation:

- an autonomous control-plane movement occurred between E9.2 and E9.2.1;
- Codex did not perform it;
- target `1` is now genuinely occupied by `10.7.0.5`;
- candidate `10.7.0.14` remains on `vless` and remains a valid user variable for a future canary packet;
- target `1` is no longer a clean second-canary target.

## Refresh Observation

Three read-only samples showed the same state:

| Sample | Time UTC | `users.registry` Hash | Target 1 User | `1_users` | `1_load_status` | Candidate |
|---|---|---|---|---:|---|---|
| A | 2026-05-25T15:19:12Z | `f3d22fbf...0515e` | `10.7.0.5` | 1 | `SOFT_FULL` | `10.7.0.14 current=vless` |
| B | 2026-05-25T15:20:16Z | `f3d22fbf...0515e` | `10.7.0.5` | 1 | `SOFT_FULL` | `10.7.0.14 current=vless` |
| C | 2026-05-25T15:22:57Z | `f3d22fbf...0515e` | `10.7.0.5` | 1 | `SOFT_FULL` | `10.7.0.14 current=vless` |

All samples preserved:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Source Analysis

`v7-egress-load` counts `users.registry` directly:

```text
count=$(grep -c "current=${id}" "$USERS_REG" 2>/dev/null || true)
```

So static `egress-load.state` does not need history, reconnect state, route tables, or desired-state to produce `1_users=1`.

`v7-users-autoswitch` also syncs user counts from active users:

```text
self.users = self._load_users()
self.egress = self._load_egress()
self._sync_egress_user_counts()
self.dynamic_load = self._dynamic_load_summary()
```

The dynamic load summary is planner-derived, but its `per_egress.1.users=1` agrees with registry reality.

Important nuance:

- static load uses `soft_limit=1`, `hard_limit=2`, so target `1` is `SOFT_FULL`;
- dynamic load summary reports target `1` status `OK` because it uses dynamic limits `19/24`;
- for a bounded live canary, the stricter static load signal should block target `1` unless separately approved.

## Classification

```text
classification=REAL_HIDDEN_LOAD
stale_state=false
planner_derived_only=false
real_hidden_load=true
load_calculator_bug=false
expected_non_registry_count=false
```

The most precise description is:

```text
real current target-1 assignment detected: 10.7.0.5
```

## Second Canary Implication

Can E9.3 proceed without waiver?

```text
false
```

Is waiver acceptable?

```text
false for target 1 as currently occupied
```

Reason: E9.2's strategy was "different user -> same target 1" for mechanics reproducibility. Since target `1` now already hosts `10.7.0.5` and static load marks it `SOFT_FULL`, a second canary to target `1` would test capacity/load behavior as well as mechanics. That changes the experiment.

Should target `1` still be used?

```text
not now
```

Should another target be selected?

```text
yes, if it is healthy, zero-user, not reserve-only, not manual-only, and has clean route/check evidence
```

Should the load calculator be fixed first?

```text
no
```

No calculator bug was found. The issue is real runtime movement/assignment, not bad counting.

Does candidate `10.7.0.14` remain valid?

```text
true
```

Candidate `10.7.0.14` remains on `vless`, table `1012`, checks OK. The target must change or be revalidated after target `1` is no longer occupied.

## Recommended Next Step

Do not execute E9.3 on target `1` now.

Recommended next step:

```text
E9.2.2 read-only target selection refresh:
- preserve candidate 10.7.0.14 if still stable;
- compare zero-user targets;
- choose a target that is health-ready and load-clean;
- or wait for target 1 to return to zero users before refreshing the E9.2 packet.
```

If the operator specifically wants to continue with target `1`, require a new explicit waiver acknowledging:

- target `1` already has one real user;
- static load is `SOFT_FULL`;
- second canary would add a second user to target `1`;
- the test would no longer isolate pure one-user route mechanics.

## Final Answers

```text
target_1_load_state_classification=REAL_HIDDEN_LOAD
target_1_ready_for_E9_3=false
waiver_required=true
waiver_acceptable=false
real_hidden_load_detected=true
load_calculator_bug_detected=false
candidate_10.7.0.14_still_valid=true
recommended_next_step=E9.2.2 read-only target selection refresh or wait for target 1 zero-user state
execution_allowed_now=false
runtime_mutation_performed=NO
user_movement_performed=NO
routing_mutation_performed=NO
kill_switch_mutation_performed=NO
autoswitch_apply_performed_manually=NO
canary_performed=NO
```
