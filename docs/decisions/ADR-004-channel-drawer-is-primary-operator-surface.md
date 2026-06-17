# ADR-004 Channel Drawer Is Primary Operator Surface

Status: Accepted
Date: 2026-06-18
Commit: `8ba2178f`

## Context

Channel work previously exposed engineering objects and metrics before the operator could answer: Is the channel healthy? Is action required? Can users safely stay? What should I do?

UX and channel truth work converged on a decision-first channel model that matches the User Drawer philosophy.

## Decision

The Channel Drawer is the primary channel operator surface. Its first screen must answer the operator's decision question using V7 Decision, reason, action, and safety/problem summary. Technical Health, evidence, service matrix, history, execution, and raw diagnostics must remain deeper.

## Alternatives considered

- Use a separate channel health page: rejected because it creates another workflow.
- Make the table the only channel surface: rejected because operators need detail, evidence, and safe actions after the decision.
- Keep raw service/trust/recovery blocks first: rejected because operators cannot quickly infer the required action.

## Consequences

- Channel table leads with V7 Decision.
- Channel Drawer first screen is operator-answer first.
- Screen 2/3 carry investigation and technical proof.
- User Drawer and Channel Drawer share one mental model.

## Affected modules

- Channel table
- Channel Drawer
- `admin/v7-admin-api`
- `admin_core/operator_decision_surface.py`

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` sections: Channels, Channel Decision V7, Admin UI Operator Model.

## Related reports

- `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`
- `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`
- `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`
- `CHANNEL_SUITABILITY_3_FINAL_CHANNEL_UI_POLISH_REPORT.md`
