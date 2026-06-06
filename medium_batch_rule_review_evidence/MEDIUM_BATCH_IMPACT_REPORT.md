# MEDIUM_BATCH_IMPACT_REPORT

Project: V7 Vozduh

Scope: impact if MEDIUM_BATCH were approved. This review did not approve it.

## If MEDIUM_BATCH Were Approved

Expected changes:

| Area | Change |
| --- | --- |
| authority state | `SMALL_BATCH -> MEDIUM_BATCH` after explicit certification/promotion |
| runtime budget | `2 -> 5` |
| packet generation | canonical packet generator may bind up to 5 users |
| rollback scope | rollback manifest expands from 2 to up to 5 users |
| restore barrier scope | restore barrier must bind exact 5-user packet scope |
| planner gate | selected moves after authority gate may remain up to 5 |

## Current State

MEDIUM_BATCH is not approved.

Current state remains:

| Field | Value |
| --- | --- |
| current_certified_authority | SMALL_BATCH |
| current_runtime_authority | SMALL_BATCH |
| current_allowed_user_budget | 2 |
| next_authority_class | MEDIUM_BATCH |
| next_allowed_user_budget | 5 |
| authority_promoted | false |

## Impact Verdict

Because readiness is not approved, no authority state, runtime budget, packet scope, rollback scope, or restore barrier scope changes are allowed.

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO
