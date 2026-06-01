# Block D1 Autoswitch Safety Remediation And Decision Tree Report

Project: V7 Vozduh

Block: D1

Title: Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Summary

Block D1 was analysis-only. No runtime decisions were executed.

Recommended path:

```text
HOLD + CREATE_NEW_EXECUTION_TARGET + PLANNER_CAP + AUTOSWITCH_SHADOW_RETRY
```

Do not proceed to operator autoswitch until the safety parser and proposal cap are fixed.

## 1. Reality Audit

Current execution target:

- Count: `10`
- Hard limit: `10`
- Headroom: `0`

Actual enabled egress count: `7`

Safety review sees enabled egress count: `0`

Shadow planner:

- `candidate_moves=12`
- `selected_moves=0`
- `failover=12`

## 2. Conflict Audit

Existing components are sufficient and should be extended:

- `v7-users-autoswitch`
- `v7-autoswitch-safety-review`
- `v7-operator-execution-packet`
- `v7-route-movement-preview`
- `v7-second-canary-target-readiness`

No duplicate planner, safety review, approval system, or execution engine should be created.

## 3. Truth Source Audit

Canonical sources:

- Planner: autoswitch shadow JSON
- Safety: safety review output
- Capacity: egress registry plus policy
- Execution target: egress registry
- Candidate generation: planner decisions
- Trust: trusted RU state
- Health: checker outputs

Main truth mismatch:

- safety review parser does not match current KV registry format.

## 4. Runtime Audit

Runtime checkers are OK.

Admin API remains unavailable.

Trusted RU remains `NEEDS_ATTENTION`.

Execution target remains at `10/10`.

## 5. Safety Critical Analysis

Root cause:

- `v7-autoswitch-safety-review` parses registry rows as first token plus second token.
- Current egress registry is KV format.
- It therefore reads `protocol=...` where it expects an enabled marker.

Classification:

- logic/interpretation problem
- not a real absence of enabled egress

## 6. Enabled Egress Analysis

Actual enabled egress:

- `7`

Planner view:

- `egress_total=7`
- `healthy_egress_total=2`

Safety review view:

- `enabled_egress=0`

Wrong component:

- `v7-autoswitch-safety-review`

## 7. Planner Analysis

The `12` failovers are:

- ten execution cohort users
- two enabled users on `vless`

Reason:

- `current_egress_not_eligible`

Classification:

- expected from raw planner rules
- overly broad for governed autoswitch

## 8. Planner Cap Analysis

Planner cap is possible without changing scoring.

Use:

- raw planner output
- capped proposal builder
- operator approval packet

Start with budget `1`, then prove `2`, `5`, `10`.

## 9. Execution Cohort Analysis

Best strategy:

- HOLD current cohort
- create new execution target

Do not rollback all ten users by default.

## 10. Second Target Analysis

No second execution-only target exists.

Existing enabled non-execution channels are not equivalent to a second execution target.

## 11. Packet Autoswitch Analysis

Packet autoswitch is feasible:

```text
shadow -> proposal packet -> approval packet -> runtime recheck -> bounded execution -> observation
```

## 12. Decision Tree

Decision tree complete:

- parser bug -> fix parser
- target full -> create target
- raw planner too broad -> cap proposal
- execution cohort recommended for failover -> add hold semantics
- safety/admin/checker not clean -> deny execution

## 13. Target Limit Analysis

Limit source:

- egress registry `soft_limit=10 hard_limit=10`

Classification:

- governance/certification guardrail
- not proven technical interface limit

Increasing to `20` requires certification.

Increasing to `50` is high blast-radius risk.

Increasing to `100` exceeds current policy max hard limit `80`.

## 14. Remediation Matrix

Primary remediation:

1. Fix safety parser.
2. Add enabled-egress regression.
3. Add planner cap proposal model.
4. Add execution cohort hold semantics.
5. Create or certify second execution target.
6. Retry shadow with budget `1`.

## 15. Final Decision

Recommended path:

```text
HOLD + CREATE_NEW_EXECUTION_TARGET + PLANNER_CAP + AUTOSWITCH_SHADOW_RETRY
```

## 16. Recommended Next Program

Next program should be D2:

```text
Autoswitch Safety Parser Fix And Bounded Proposal Builder
```

D2 should remain non-mutating until tests prove:

- enabled egress count is correct
- safety review status is no longer false-critical
- planner proposal cap works
- execution cohort hold semantics prevent broad failover proposals

## Required Verdicts

- `safety_root_cause_known=true`
- `enabled_egress_issue_understood=true`
- `planner_behavior_understood=true`
- `planner_cap_possible=true`
- `execution_cohort_decision_complete=true`
- `second_target_strategy_known=true`
- `packet_autoswitch_feasible=true`
- `decision_tree_complete=true`
- `target_limit_source_known=true`
- `remediation_matrix_complete=true`
- `recommended_path_defined=true`
- `safe_to_continue=true`

## Safety Verdict

- `users_moved=false`
- `rollback_executed=false`
- `autoswitch_apply_run=false`
- `routing_changed=false`
- `deploy_performed=false`

