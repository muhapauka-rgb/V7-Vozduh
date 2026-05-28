# E13 Design Consistency Review

## Purpose

This file records the mandatory E13 design reviews. No runtime mutation, UI
implementation, deployment, user movement, routing mutation, kill switch
mutation, manual autoswitch apply, or canary was performed.

## Review Matrix

| Review | Result | Evidence |
|---|---|---|
| Screen consistency | PASS | All 12 screens use the same fields: purpose, visible information, progressive disclosure, actions, dangerous actions, approvals, mobile, empty, warning. |
| Approval flow consistency | PASS | Approval contracts bind preview, generation token, selected-move fingerprint, rollback, barrier, delayed monitoring, expiry, and replay prevention. |
| Rollback visibility consistency | PASS | Pending Movement Preview, Approval Center, Restore Lifecycle, Cohort Governance, and Operations History all require rollback visibility. |
| Observability hierarchy consistency | PASS | Timeline, replay, movement, restore, generation, planner/apply, selected moves, target pressure, and delayed movement use summary-first evidence. |
| Progressive disclosure consistency | PASS | Raw logs, JSON, route tables, and diagnose internals are hidden until drawers or Evidence Viewer. |
| Mobile operator flow review | PASS | Each screen specifies compact first-visible state, single-operation focus, and full-screen deep evidence. |
| Blast radius visibility review | PASS | Movement Preview, Approval Center, Topology Model, and Approval Contracts require affected users, target delta, rollback, capacity, and delayed-monitor scope before approval. |
| Dangerous-action UX review | PASS | Broad autoswitch apply, Direct/RU mutation, Trusted RU refresh, proxy apply, kill switch mutation, and unbounded repair are explicitly not one-click. |
| Topology scaling review | PASS | Topology uses grouped lane model with exact users for small cohorts and summary/filter model for larger sets; no graph/spaghetti model. |
| Governance language consistency review | PASS | Canonical vocabulary is movement, selected moves, generation token, restore barrier, rollback contract, delayed monitor, evidence freshness, and bounded approval. |

## Cross-Screen Invariants

- Every serious action starts from fresh evidence.
- Every movement approval has rollback before forward approval.
- Every nonzero movement budget has generation-token ownership.
- Every restore lifecycle stays open until delayed monitoring is clean.
- Every historical evidence item is labeled historical, superseded, or current.
- Every disabled action explains the failed gate and safe next action.
- Overview surfaces state; action lives in Approval Center or specific workflow.

## Visual Consistency Verdict

The design follows the existing V7 admin direction:

- calm dark surfaces;
- data-first hierarchy;
- restrained semantic color;
- compact status bands;
- minimal frames;
- no heavy topology;
- progressive disclosure;
- no generic VPN dashboard.

