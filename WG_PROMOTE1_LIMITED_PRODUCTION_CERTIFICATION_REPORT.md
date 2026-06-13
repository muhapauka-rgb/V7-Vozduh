# WG.PROMOTE.1 - Limited Production Promotion Certification

## Executive Summary

Channel:

```text
wireguard-1779454504-c43409
```

Final verdict:

```text
LIMITED_PROMOTION_CERTIFIED
```

Meaning:

WireGuard is certified for a bounded transition from canary reservation to limited production participation, using an explicit `capacity_users=2` cap.

No production state was changed in this program.

No users were moved.

No autoswitch apply was run.

No deploy was run.

## Phase 1 - Pre-Promotion Audit

Local workspace:

```text
clean=true
branch=Updatesystem
local_commit=f6bb3218cf9fe01a650eaff93b5119f0d3c63a4d
```

Runtime truth:

```text
runtime_final_verdict=PASS
runtime_convergence_status=RUNTIME_ALIGNED
runtime_action_guard=docs_only_mismatch_ignored
runtime_safe=true
```

GitHub direct check:

```text
origin/Updatesystem=f6bb3218cf9fe01a650eaff93b5119f0d3c63a4d
```

Tool caveat:

`tools/v7-truth-check --all --json` and `tools/v7-convergence-status --json` returned overall NO-GO because the tool path reported:

```text
github_remote_unreadable
canonical_branch_missing_on_remote
```

Direct `git ls-remote origin refs/heads/Updatesystem` succeeded and proved the branch exists at the expected commit. Therefore this is classified as a local tool/network read caveat, not a runtime blocker.

WireGuard current health:

```text
service_score=100.0
telegram=OK
avg_mbps=55.03
min_mbps=51.35
stability=0.933
required_service_missing=[]
required_service_low=[]
```

Evidence:

- `WG_PROMOTE1_EVIDENCE/gates/truth_check_all.json`
- `WG_PROMOTE1_EVIDENCE/gates/convergence_status.json`
- `WG_PROMOTE1_EVIDENCE/gates/github_ls_remote_updatesystem.txt`
- `WG_PROMOTE1_EVIDENCE/analysis/baseline_planner.json`

## Phase 2 - Canary Dereservation Plan

Canonical reservation owner:

```text
control_plane_governance
```

Current reservation fields:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Current blocker:

```text
canary_reserved_production_assignment_blocked
```

Canonical runtime consumer:

```text
tools/v7-users-autoswitch
```

Relevant code behavior:

- `canary_reserved=true` is parsed by `_load_egress`.
- reserved egresses are excluded from production assignment.
- reserved current targets are held, not silently drained.

Bounded removal plan:

```text
remove canary_reserved
remove reservation_reason
remove reservation_owner
add capacity_users=2
```

This is not full promotion. The added `capacity_users=2` is the runtime-consumed cap that prevents unlimited assignment.

## Phase 3 - Capacity Certification

Initial production phase cap:

```text
capacity_users=2
```

Reason:

- historical E11 WireGuard proof reached two users;
- WG.CAPACITY.1 proved `1/2` is not the current runtime capacity authority;
- current dynamic runtime capacity sees much larger capacity, but using full dynamic capacity blindly would be too broad;
- `capacity_users=2` is the existing runtime-recognized per-egress cap;
- this keeps promotion bounded while allowing pool expansion.

Rejected options:

| Option | Decision | Reason |
| --- | --- | --- |
| keep canary forever | rejected | healthy channel remains unnecessarily excluded |
| remove canary only | rejected | planner would treat channel as broad best-pool target |
| use full dynamic capacity | rejected | full production capacity not freshly certified |
| use `capacity_users=2` | accepted | bounded, runtime-consumed, matches prior evidence |

## Phase 4 - Counterfactual Dry Run

Counterfactual mutation was applied only to copied evidence state:

```text
WG_PROMOTE1_EVIDENCE/counterfactual_limited_state/egress.registry
```

No production state was changed.

Counterfactual row:

```text
id=wireguard-1779454504-c43409 ... capacity_users=2
```

Planner impact:

```text
healthy_egress_total: 1 -> 2
candidate_moves_total: 3 -> 26
selected_moves: 1 -> 1
selected_to_wireguard=1
```

WireGuard counterfactual candidate:

```text
eligible=true
blocked=[]
best_available_pool=true
pool_rank=1
score=2234.66
capacity_users=2
projected_load.users=0
projected_load.soft_limit=2
projected_load.hard_limit=2
telegram=OK
service_aggregate_score=100.0
```

The first selected move would be:

```text
10.0.0.2: awg3 -> wireguard-1779454504-c43409
projected_load.users=1
soft_limit=2
hard_limit=2
```

This proves the cap is active in planner output.

Evidence:

- `WG_PROMOTE1_EVIDENCE/analysis/limited_promotion_counterfactual_planner.json`
- `WG_PROMOTE1_EVIDENCE/analysis/limited_promotion_summary.json`

## Phase 5 - Limited Promotion Patch

Exact proposed governance mutation:

- `WG_PROMOTE1_EVIDENCE/analysis/proposed_limited_promotion_mutation.md`

Before:

```text
... canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance
```

After:

```text
... capacity_users=2
```

Mutation status:

```text
prepared=true
applied=false
production_changed=false
```

Only a later approved production program may mutate `/opt/v7/egress/state/egress.registry`.

## Phase 6 - Post-Promotion Dry Run

The copied-state post-promotion dry run verifies:

| Check | Result |
| --- | --- |
| WireGuard eligible | true |
| WireGuard blocked | false |
| healthy pool expands | true |
| best available pool includes WireGuard | true |
| capacity cap active | true |
| target substitution observed | false |
| governance bypass observed | false |
| planner bypass observed | false |
| apply executed | false |

Planner behavior is sane for limited promotion.

## Phase 7 - BA.3 Impact Review

Would BA.3 become feasible automatically?

```text
no
```

Would the candidate pool recover?

```text
yes
```

Would autonomy gain a second healthy channel?

```text
yes
```

Reason:

The limited promotion expands healthy egress from 1 to 2 and candidate moves from 3 to 26. However, the current planner still selects only one real move in this captured state. Even with a diagnostic policy file setting `autoswitch_max_planned_per_run=5`, selected moves remain 1.

Evidence:

- `WG_PROMOTE1_EVIDENCE/analysis/ba3_impact_planned_limit_5_summary.json`
- `WG_PROMOTE1_EVIDENCE/analysis/limited_promotion_planned_limit_5_dry_run.json`

BA.3 conclusion:

Limited WireGuard promotion is useful and necessary for pool recovery, but it does not by itself certify five-user autonomy. BA.3 still requires a fresh planner state with five selected moves.

## Phase 8 - Final Certification

Final verdict:

```text
LIMITED_PROMOTION_CERTIFIED
```

Final results:

```text
pre_promotion_audit_complete=true
runtime_truth_pass=true
github_direct_check_pass=true
tool_github_read_caveat=true
wireguard_health_pass=true
wireguard_stability_pass=true
service_matrix_pass=true
telegram_pass=true
canary_dereservation_plan_prepared=true
initial_cap_defined=2
initial_cap_runtime_consumed=true
counterfactual_dry_run_complete=true
wireguard_eligible_after_counterfactual=true
healthy_pool_expands=true
candidate_pool_recovers=true
limited_promotion_patch_prepared=true
limited_promotion_patch_applied=false
production_changed=false
users_moved=0
autoswitch_apply_run=false
ba3_automatically_feasible=false
FINAL_VERDICT=LIMITED_PROMOTION_CERTIFIED
SAFE_NEXT_STEP=WG_PROMOTE1_APPLY_LIMITED_DERESERVATION_WITH_CAPACITY_USERS_2
```

## One Remaining Operational Boundary

The next step must be a separate approved production mutation block.

It should:

1. rerun truth/convergence outside the GitHub-read caveat;
2. backup `/opt/v7/egress/state/egress.registry`;
3. apply exactly the prepared row mutation;
4. run planner dry-run;
5. verify WireGuard eligible with `capacity_users=2`;
6. stop before any user movement unless separately approved.

