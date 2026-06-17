# ADR-003 Health Screen Diagnostics Only

Status: Accepted
Date: 2026-06-18
Commit: `8ba2178f`

## Context

Channel health details were at risk of becoming a second primary operator workflow. Audits concluded that Health is valuable only when it explains the channel score and evidence behind it. The primary operator question belongs to Channel Decision V7, not Health.

## Decision

Technical Health is diagnostics-only. It explains why the score is what it is. It lives inside the Channel Drawer as nested diagnostics and must not become a separate primary Health drawer, new page, new workflow, or action owner.

## Alternatives considered

- Keep Health as a primary screen: rejected because it forces operators to reason from technical components instead of V7's decision.
- Remove Health entirely: rejected because score explanation is necessary for trust and debugging.
- Turn Health red rows into independent action owners: rejected unless they reuse existing safe handlers and remain inline diagnostics.

## Consequences

- Health answers "why this score", not "what should I do first".
- Decision/action language belongs to V7 Decision, Problems, and existing safe actions.
- Diagnostics can show Services, Stability, Capacity, Route, Runtime/Readiness, and History.

## Affected modules

- `admin/v7-admin-api` channel diagnostics functions
- Channel Drawer
- Channel score explanation

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` sections: Channel Score, Technical Health, Admin UI Operator Model.

## Related reports

- `docs/operator_actions/CHANNEL_HEALTH_SCREEN_EXISTENCE_AUDIT.md`
- `docs/operator_actions/CHANNEL_HEALTH_2_DIAGNOSTICS_ONLY_IMPLEMENTATION_REPORT.md`
- `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`
