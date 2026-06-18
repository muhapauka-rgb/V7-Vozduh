# ADR-007 Channel Signal Semantics Correction

Status: Accepted
Date: 2026-06-18
Commit: `169e868a`

## Context

CHANNEL.SIGNALS.2 correctly changed the channel table to `Channel / Decision / Signals / Users`.

Live validation then showed semantic contradictions:

- Channels with `Use` or `Keep Current Users` could show red or warning Route even when Route was only reflecting capacity or service state.
- Primary Services could warn because hidden companion endpoint checks such as Anthropic API failed while the user-facing service still worked.
- Load could look like a channel quality failure instead of an assignment/capacity limit.

Reference-first review confirmed:

- Channel Decision V7 remains planner/assignment truth.
- Channel Score remains mixed diagnostics.
- Technical Health remains diagnostics-only.
- Route is readiness confidence, not route quality, speed, latency, packet loss, or user traffic quality.

## Decision

The first-level channel table signal set is:

- Services
- Load
- Runtime
- Stability only when not OK

Route is supporting/diagnostics-only in the table context. It may be shown deeper in the Channel Drawer, score explanation, route evidence, or as a first-level problem only if a future planner/route blocker explicitly exposes a real route issue.

First-level Services tracks primary user-facing services. Hidden endpoint checks such as `anthropic`, `openai_auth`, and `google_auth` remain supporting diagnostics and do not downgrade the table Services signal by themselves.

Load is an assignment/capacity signal. It means "can this channel accept or keep users under current policy limits", not "internet quality is bad".

## Alternatives Considered

- Keep Route visible as a first-level red/warn badge: rejected because current Route can be reduced by capacity/services and misleads operators.
- Hide Services whenever only one optional endpoint fails: accepted for hidden/supporting endpoints only, rejected for primary user-facing service failures.
- Remove Load from the table: rejected because overload directly explains why users should not be added or may need movement.
- Change planner or score formulas: rejected because this ADR concerns operator signal semantics only.

## Consequences

- The table better follows `Decision -> Signals that explain decision`.
- `Use` channels should no longer look broken because of hidden endpoint failures or Route readiness artifacts.
- Capacity/Load warnings remain visible when they explain assignment pressure.
- Score and Route evidence remain available in diagnostics.

## Affected Modules

- `admin/v7-admin-api`
- Channel table
- Channel signal tooltip helpers
- Channel diagnostics/reference docs

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` sections: Capacity, Service Matrix, Channel Operator Signal Model.

## Related Reports

- `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`
- `CHANNEL_SIGNALS_2_TABLE_IMPLEMENTATION_REPORT.md`
- `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`
- `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`
- `CHANNEL_SCORE_REALITY_AUDIT.md`

