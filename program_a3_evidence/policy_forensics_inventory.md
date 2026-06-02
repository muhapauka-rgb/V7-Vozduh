# PROGRAM A.3 Policy Forensics Inventory

Scope: read-only local repository and prior A.2 runtime evidence. No production, planner, policy, governance, service, or runtime state mutation was performed.

## Authoritative Runtime Planner

The authoritative implementation for runtime autoswitch eligibility is `tools/v7-users-autoswitch`.

Evidence:

- `tools/v7-users-autoswitch:42-57` defines default switch and quality policy.
- `tools/v7-users-autoswitch:337-340` merges `policy.quality` and org policy into the active quality policy.
- `tools/v7-users-autoswitch:1315-1324` evaluates candidates through basic, reservation, org, quality, service, load, and safety gates before scoring.
- `tools/v7-users-autoswitch:1324-1328` returns blocked candidates before score calculation.

## Quality Floors

Default floors:

- `min_avg_mbps=15.0`
- `min_floor_mbps=10.0`
- `min_stability=0.45`
- `metrics_fresh_seconds=900`

Locations:

- `tools/v7-users-autoswitch:52-57`
- `admin/v7-admin-api:461-464`
- `admin/v7-admin-api:15661-15663`
- `BLOCK2_2_CONTROLLED_DRAIN_REBALANCE_REPORT.md:141-143`

Actual semantics:

- `tools/v7-users-autoswitch:1407-1417` applies these floors as hard eligibility gates.
- `tools/v7-users-autoswitch:1418-1420` treats high one-hour fail rate as advisory, not hard.
- `tools/v7-users-autoswitch:1530-1572` also uses quality/stability in scoring, but only after hard gates pass.

Classification:

- `min_avg_mbps`: Hard Safety Floor and Eligibility Gate.
- `min_floor_mbps`: Hard Safety Floor and Eligibility Gate.
- `min_stability`: Hard Safety Floor and Eligibility Gate when nonzero.
- `quality_history_fail_rate`: Preference/diagnostic advisory in current planner.

## Migration Thresholds

Default migration thresholds:

- `min_score_improvement_pct=0.20`
- `min_score_delta=50.0`

Locations:

- `tools/v7-users-autoswitch:42-50`
- `tools/v7-users-autoswitch:1618-1621`
- `admin/v7-admin-api:458-459`
- `admin/v7-admin-api:15659-15660`

Actual semantics:

- A candidate must first pass all hard gates.
- Only then `_beats_current` checks relative score improvement and absolute score delta.

Classification:

- Migration Threshold, not candidate eligibility gate.

## Severity Logic

Locations:

- `tools/v7-users-autoswitch:503-518` excludes severity outside `OK/WARN` from healthy load accounting.
- `tools/v7-users-autoswitch:1334-1345` blocks candidate eligibility for any severity outside `OK/WARN`.
- `admin/v7-admin-api:15905-15913` scores non-OK/WARN admin route candidates as a penalty, not a hard planner gate.

Actual semantics:

- Runtime autoswitch treats `SUSPECT` as a hard blocker.
- Admin route scoring treats unknown/severe diagnostics as score penalties.

Classification:

- Runtime planner: Hard Safety Floor and Eligibility Gate.
- Admin UI route scoring: Preference Weight / advisory scoring.

## Reservation Logic

Locations:

- `tools/v7-users-autoswitch:503-511` excludes `canary_reserved` from healthy load accounting.
- `tools/v7-users-autoswitch:1352-1359` blocks non-current production assignment to `canary_reserved`.
- `BLOCK_E11_8_TARGET_RESERVATION_ENFORCEMENT_ROOT_CAUSE_AND_FIX_REPORT.md:49-52` documents intended reservation enforcement.

Actual semantics:

- `canary_reserved` is a hard production assignment gate.
- Existing users already on a reserved target may be held but require separate drain approval.

Classification:

- Governance/Safety Eligibility Gate.

## Service And Route-Class Logic

Locations:

- `tools/v7-users-autoswitch:1454-1483`
- `tools/v7-users-autoswitch:1500-1508`
- `admin/v7-admin-api:15865-15920`

Actual semantics:

- Telegram hard-down blocks required Telegram candidates.
- Multiple critical service failures block eligibility.
- Route class `FAIL` blocks eligibility.
- Route class `WARN` is a reason/penalty, not a hard block.

Classification:

- Telegram hard down: Hard Safety Floor.
- Service multiple critical failure: Hard Safety Floor.
- Route class `FAIL`: Hard Safety Floor.
- Route class `WARN`: Preference Weight / risk signal.

## Capacity And Load Logic

Locations:

- `tools/v7-users-autoswitch:58-70`
- `tools/v7-users-autoswitch:503-518`
- `tools/v7-users-autoswitch:1361-1363`
- `admin/v7-admin-api:466-479`
- `BLOCK_E32_1_5_CAPACITY_RUNTIME_IMPACT_REPORT.md:21-44`

Actual semantics:

- Dynamic load excludes channels failing hard health/quality/reservation gates.
- In dynamic mode, `HARD_FULL` is not a direct planned-candidate block inside `_gate_basic`.
- Capacity is a forward movement gate but not execution authority by itself.

Classification:

- Capacity/Load Gate after health and eligibility.

## Product Intent Reconstructed

The product intent is not "move to fastest raw channel." The consistent intent across docs and code is:

1. Never move users to obviously broken, reserved, manual-only, or service-failing channels.
2. Require a meaningful improvement over current route for planned movement.
3. Keep movement under restore barrier, audit, approval, and generation safeguards.
4. Use capacity as a forward admission gate, with requalification allowed only through evidence.
5. Prefer fail-closed behavior when policy truth is unknown.

The mismatch discovered in A.3 is narrower:

- The current runtime policy also treats all quality floors and `SUSPECT` severity as hard candidate disappearance gates.
- For protocol-specific diagnostics like `handshake_unsupported_for_protocol_vless`, `SUSPECT` may be a diagnostic limitation rather than a proven transport failure.
- For VLESS, fresh raw speed and one-hour minimum throughput contradict the hard canonical rejection enough to justify a policy design, not an override.

