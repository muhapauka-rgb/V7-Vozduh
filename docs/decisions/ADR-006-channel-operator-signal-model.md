# ADR-006 Channel Operator Signal Model

Status: Accepted
Date: 2026-06-18
Commit: `72ede82b`

## Context

Reference-first review confirmed that Channel Score is a mixed technical/operational readiness score, Technical Health is diagnostics-only, and the Channel Drawer is the primary channel operator surface.

The remaining problem was presentation semantics: the UI still risked implying that one mixed score could explain channel quality, assignment eligibility, capacity, route readiness, service health, runtime readiness, and history.

## Decision

V7 channels use a multi-signal operator model.

The first operator layer must lead with V7 Decision / assignment role, then show compact operator signals that explain the decision and user impact. The mixed technical score remains secondary and diagnostic.

Accepted signal categories:

- Operator Signal: visible immediately when it changes the operator answer.
- Supporting Signal: visible in tooltip, compact expansion, or drawer details.
- Diagnostic Only: visible only in technical diagnostics/evidence/history.

Route is classified as a Supporting Signal because the current route component is readiness/topology confidence, not direct user traffic quality.

Capacity must be shown as operator language: headroom, full, overloaded, or users affected. Raw capacity component score remains diagnostic.

## Alternatives considered

- Keep one mixed score as the main operator signal: rejected because it can conflict with assignment truth.
- Replace score with planner assignment only: rejected because score breakdown still explains technical condition.
- Show every component as a first-level signal: rejected because it increases cognitive load and recreates diagnostics as the operator workflow.

## Consequences

- Channel table should use the order: Channel, Decision, Signals, Users.
- Channel Drawer should use: Decision, Signals, Problems, Works, Diagnostics.
- Default sorting should not use mixed score. It should prioritize decision severity, affected users, worst operator signal, then name.
- Tooltips may explain signals but must not introduce actions, validators, or new workflows.
- Technical Health remains diagnostics-only and must not become a second primary action owner.

## Affected modules

- Channel table
- Channel Drawer
- Channel technical diagnostics
- `admin/v7-admin-api`
- `admin_core/operator_decision_surface.py`
- `tools/v7-users-autoswitch`

## Reference updates

- Added `Channel Operator Signal Model` to `docs/reference/V7_CANONICAL_REFERENCE.md`.
- Added `Channel Operator Signal Model` to `docs/reference/SYSTEM_MAP.md`.

## Related reports

- `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`
- `CHANNEL_SCORE_REALITY_AUDIT.md`
- `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`
- `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`
- `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`
