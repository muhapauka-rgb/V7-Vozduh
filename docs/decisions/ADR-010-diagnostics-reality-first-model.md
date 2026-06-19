# ADR-010 Diagnostics Reality-First Model

Status: Accepted
Date: 2026-06-19
Commit: DIAGNOSTICS.1 implementation commit

## Context

The channel operator surface is now Decision-First. The Channel Drawer starts from what V7 wants, why, compact signals, active problems, working checks, and then diagnostics.

Diagnostics still used legacy score-first language such as component points, point loss, and score contribution. That made operators reason from arithmetic instead of reality:

- Services looked like a point contribution instead of availability.
- Load looked like a score penalty instead of assigned-user pressure.
- Route looked like route quality or speed instead of readiness/topology confidence.
- Runtime and history looked like score components instead of evidence confidence.

Reference-first review confirmed that Channel Score remains a mixed technical diagnostic score and must not become assignment truth. The UI problem was presentation, not formula.

## Decision

Channel Diagnostics must be Reality-First.

Diagnostics explain what is observed:

- Services: working services, unavailable services, and impact.
- Stability: channel/interface state in operator language.
- Capacity / Load: assigned users, preferred assignment level, hard assignment limit, and whether new assignments are restricted.
- Route: readiness/topology confidence, not traffic quality, speed, or bandwidth.
- Runtime: runtime snapshot readiness.
- History: recent negative or calm history.

Diagnostics must not explain operator state through:

- component point totals;
- lost points;
- penalties;
- score contribution;
- "full score" or "partial score" language.
- generic "requires verification" / "needs check" language when a concrete reality-first state is available.

The underlying Channel Score calculation remains unchanged and may remain available as secondary metadata outside the reality-first diagnostic explanation.

## Alternatives considered

1. Keep score-first diagnostics.
   - Rejected. It makes operators interpret arithmetic instead of understanding channel reality.

2. Remove diagnostics.
   - Rejected. Engineers and operators still need evidence after the Decision-First answer.

3. Change score formula.
   - Rejected. The problem is presentation, not scoring semantics.

## Consequences

- Channel Drawer diagnostics remain last and collapsed.
- Diagnostics show reality/evidence first.
- Channel Score remains a mixed diagnostic calculation but no longer drives diagnostic copy.
- Capacity/Load text must follow ADR-009 and never imply speed, CPU, bandwidth, or physical saturation.
- Route text must explain readiness/topology confidence and not traffic quality.
- Route copy should say readiness/confidence is incomplete, not that the route is broken, unless runtime route evidence explicitly shows mismatch or leak risk.
- Capacity copy should explain preferred assignment level, hard assignment limit, new-assignment restriction, and that current users are not automatically disconnected.
- Channel signal dots may use a minimal legend to reduce operator memory burden, but must not become a noisy badge system.
- Diagnostics must not become a new planner, workflow, action owner, governance path, execution path, storage, or truth source.

## Affected modules

- `admin/v7-admin-api`
- Channel Drawer diagnostics rendering
- Canonical reference
- System map

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` sections: Channel Score, Technical Health, Channel Operator Signal Model.
- `docs/reference/SYSTEM_MAP.md` row: Channel Score / Technical Health.

## Related reports

- `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`
- `CHANNELS_FINAL_POLISH_AND_LOCK_REPORT.md`
- `CHANNEL_DECISION_FIRST_2_DRAWER_REPORT.md`
- `CAPACITY_1_REALITY_AUDIT_REPORT.md`
- `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`
- `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`
