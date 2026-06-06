# Phase 2 - Authority Promotion Path Review

Program: `PROGRAM_MEDIUM_BATCH_AUTHORITY_PROMOTION_AND_REAL_5_USER_EXECUTION`

## MEDIUM_BATCH Criteria

`tools/v7-users-autoswitch` defines:

```text
AUTHORITY_CLASS_BUDGETS:
CANARY=1
SMALL_BATCH=2
MEDIUM_BATCH=5
LARGE_BATCH=10
POOL=25
```

`MEDIUM_BATCH` certification rule:

- `required_successful_small_batch_runs=2`
- `requires_no_recent_rollback_or_verification_failure=true`
- `requires_trust_prediction_recommendation_feedback=true`

Current evidence now satisfies the two successful small-batch outcome requirement.

## Existing Authority Gate

Current production policy remains:

```text
authority_class=SMALL_BATCH
certified_authority_class=SMALL_BATCH
current_allowed_user_budget=2
next_allowed_user_budget=5
```

Therefore runtime remains capped at 2 users. A 5-user approval packet or apply would be inconsistent with the currently certified runtime authority.

## Existing Promotion Mechanisms Reviewed

Reviewed possible existing paths:

| Path | Result |
| --- | --- |
| `tools/v7-users-autoswitch` | Contains authority gate and certification model, but no promotion write command. |
| `/api/actions/policy-update` | Existing admin action, but `update_policy()` only accepts/sanitizes `switch`, `quality`, `load`, `reconnect`, `safety`, and `intervals`; it does not accept `authority_budget`. |
| `/api/actions/org-egress-policy-update` | Organization egress policy, not global authority budget. |
| direct `/etc/v7/policy.json` write | Rejected as unsafe because the program forbids manual policy edits and requires existing governance promotion. |

## Promotion Decision

`authority_promotion_approved=false`

Reason:

The evidence criteria are satisfied, but the product does not currently provide a first-class authority promotion action/API/tool for `SMALL_BATCH -> MEDIUM_BATCH`.

Direct policy rewrite would widen execution authority from 2 to 5 users without a certified promotion path. That would weaken governance and violate the block boundary.

## Blocker

`MEDIUM_BATCH_PROMOTION_PATH_MISSING`

This blocker is not an evidence blocker. It is an implementation/governance-surface blocker:

```text
evidence_ready=true
feedback_materialized=true
promotion_path_available=false
```

Required safe closure:

Create a first-class authority promotion action that:

1. reads current authority state;
2. validates certification evidence;
3. validates feedback materialization;
4. validates runtime truth/convergence;
5. creates a policy backup;
6. updates only `authority_budget`;
7. writes audit;
8. returns before/after authority state;
9. never moves users or routes.

