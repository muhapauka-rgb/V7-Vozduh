# ADR-009 Capacity and Health Semantics

Status: Accepted
Date: 2026-06-19
Commit: `2fb9d205`

## Context

V7 operators saw apparently contradictory channel states:

- a channel could be technically good but still show load/capacity warning;
- a channel could be marked `Use` while another surface said load was on the limit;
- an emergency/reserve channel could look technically healthy but should not receive normal production users;
- "Healthy", "Use", "Emergency", "Overloaded", and "Capacity" were being read as one combined good/bad verdict.

This made channel reality hard to understand. The system already had separate planner, capacity, assignment, and diagnostic concepts, but the canonical documentation did not define their boundaries precisely enough.

## Decision

Capacity/Load is assignment pressure, not speed quality, CPU load, bandwidth saturation, or a generic channel-goodness verdict.

The canonical meanings are:

- `Use`: V7 can use the channel under current planner/assignment evidence. It does not mean fastest, best, warning-free, or unlimited capacity.
- `Emergency Only`: the channel is restricted by role or policy for manual/reserve/canary/execution-only use. It may still be technically healthy.
- `Technical Health`: diagnostics and score explanation. It can be good while assignment is restricted.
- `Table Healthy`: a narrower operator table state requiring usable/keep assignment posture and no red first-level operator signal.
- `Load OK`: current assignment is within policy limits.
- `Soft Full`: the channel is at/near soft assignment limit; new additions require caution/checking.
- `Hard Full`: planned new assignments are restricted; current users are not automatically failing.
- `Overloaded`: failover-hard capacity limit is reached. This is stronger than hard-full and still means assignment/load emergency, not traffic saturation by itself.

Capacity must remain separate from channel score and assignment decision, while still feeding both as an input.

## Alternatives Considered

1. Treat Channel Score as the single channel truth.
   - Rejected. Previous truth audits established score as mixed technical/operational diagnostics, not assignment truth.

2. Treat Load/Capacity as speed quality.
   - Rejected. Code and runtime evidence show load is based on assigned users and policy limits.

3. Hide Capacity when it creates confusion.
   - Rejected. Capacity is a real planner gate and must remain visible, but with correct language.

## Consequences

- Reports and UI copy must not imply that load/capacity warning means the channel is slow or physically overloaded.
- Future audits must read this ADR and `docs/reference/V7_CANONICAL_REFERENCE.md` before re-auditing capacity semantics.
- Operator surfaces should explain quality, assignment, blocker, and action as separate concepts.
- A channel can be technically healthy and still be Emergency Only or assignment-limited.
- A channel can be Use and still need a load/capacity check before broad new assignment.

## Affected Modules

- `tools/v7-users-autoswitch`
- `admin/v7-admin-api`
- `admin_core/operator_decision_surface.py`
- `admin_core/diagnostic_views.py`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` section 2, Channel Decision V7
- `docs/reference/V7_CANONICAL_REFERENCE.md` section 3, Channel Score
- `docs/reference/V7_CANONICAL_REFERENCE.md` section 4, Technical Health
- `docs/reference/V7_CANONICAL_REFERENCE.md` section 6, Capacity
- `docs/reference/V7_CANONICAL_REFERENCE.md` section 18, Channel Operator Signal Model
- `docs/reference/SYSTEM_MAP.md`

## Related Reports

- `CAPACITY_1_REALITY_AUDIT_REPORT.md`
- `docs/track7/productization/e35_0_1-audit/capacity-policy-audit.md`
- `CHANNEL_SCORE_REALITY_AUDIT.md`
- `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`
- `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`
- `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`
- `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`
