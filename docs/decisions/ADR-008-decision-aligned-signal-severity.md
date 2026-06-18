# ADR-008 Decision-Aligned Signal Severity

Status: Accepted
Date: 2026-06-18
Commit: `2859c0e2`

## Context

CHANNEL.SIGNALS.2A corrected several signal meanings, but production review still showed a first-level contradiction: the channel table could show a planner decision such as `Использовать` while the adjacent signal strip still showed a red diagnostic badge.

Reference-first review confirmed that:

- Channel Decision V7 / assignment truth is the operator decision source.
- Channel Score and Technical Health are diagnostics, not planner truth.
- Load/capacity can explain assignment pressure without meaning the channel is unusable for current planner purposes.

## Decision

First-level channel signal severity must be aligned to the visible planner/assignment decision.

Red first-level signal badges mean the current planner decision requires removal, block, evacuation, or immediate operator action. If the assignment decision is `Use`, `Keep Current Users`, or `Emergency Only`, a raw diagnostic `bad` signal may remain visible as a warning/diagnostic signal and in tooltip text, but it must not appear as a red contradiction beside the decision.

Raw diagnostic truth remains available through score breakdown, technical diagnostics, detailed tooltips, evidence, and drawer details. This ADR changes operator signal presentation only.

## Alternatives considered

- Keep raw diagnostic red in the first-level table: rejected because it makes operators distrust planner truth and forces inference.
- Hide non-blocking diagnostic problems entirely: rejected because diagnostic truth must remain discoverable.
- Change channel score, capacity policy, or planner eligibility: rejected because the contradiction is presentation-layer semantics, not a planner bug.

## Consequences

- `Use` channels cannot show red first-level signals.
- `Keep Current Users` and `Emergency Only` decisions can show warning/diagnostic signals without implying evacuation or planner contradiction.
- Evacuation/block decisions may still show red signals because red matches the action.
- Filters and table sorting follow the operator-visible severity rather than raw diagnostic severity.

## Affected modules

- `admin/v7-admin-api`
- Channel table signal strip
- Channel signal tooltip helpers
- Channel topology filters that use worst visible signal

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` section: Channel Operator Signal Model.

## Related reports

- `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`
- `CHANNEL_SIGNALS_2_TABLE_IMPLEMENTATION_REPORT.md`
- `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`
- `CHANNEL_SIGNALS_2B_ALIGNMENT_REPORT.md`
