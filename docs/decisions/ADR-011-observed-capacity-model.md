# ADR-011 Observed Capacity Model

Status: Accepted
Date: 2026-06-20
Commit: pending CAPACITY.2 commit

## Context

CAPACITY.1 and ADR-009 established that current V7 Capacity/Load means assignment pressure against configured limits. It is not speed quality, bandwidth saturation, CPU load, RAM use, or real provider capacity.

V7 often observes third-party tunnels. It may not own the tunnel infrastructure or know provider-side CPU, RAM, bandwidth, or hard capacity. However, V7 already observes assigned users, service matrix, runtime readiness, route readiness, speed samples, latency, fail rate, stability, and history.

## Decision

V7 should introduce the concept of `Observed Capacity Shadow`.

Observed capacity is the practical user-count range at which measured channel quality remains stable. It is learned from observations, not configured as a static limit.

The model is approved as a canonical concept and future architecture direction only. It is not approved as runtime behavior.

## Boundaries

Observed Capacity Shadow must not:

- change planner eligibility;
- change assignment decisions;
- change autoswitch behavior;
- change governance;
- change runtime execution;
- change `soft_limit`, `hard_limit`, `capacity_users`, or score formulas;
- create a new truth source.

It may:

- observe;
- measure;
- learn;
- record derived advisory evidence;
- recommend a future operator review.

## Alternatives considered

1. Keep static limits only.
   - Rejected as the long-term model because V7 often does not own third-party tunnels and static limits do not learn observed degradation.

2. Replace static limits immediately with observed capacity.
   - Rejected as unsafe. Current evidence does not yet prove causal capacity curves.

3. Add shadow observed capacity.
   - Accepted. It preserves safety while allowing V7 to learn practical capacity.

## Consequences

- Current Capacity/Load semantics remain unchanged.
- Observed Capacity becomes a separate canonical concept.
- Any future implementation must be shadow/advisory first.
- Planner integration requires a separate ADR/program after enough evidence exists.
- Operator wording must distinguish assignment limit from observed degradation.

## Affected modules

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- future optional read-only intelligence/snapshot modules
- no runtime modules changed in CAPACITY.2

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` section 6 Capacity
- `docs/reference/V7_CANONICAL_REFERENCE.md` new section Observed Capacity
- `docs/reference/SYSTEM_MAP.md` new Observed Capacity Shadow row

## Related reports

- `docs/capacity_2/CAPACITY_2_OBSERVED_CAPACITY_MODEL_REPORT.md`
- `docs/capacity_2/CURRENT_CAPACITY_MODEL.md`
- `docs/capacity_2/OBSERVED_CAPACITY_THEORY.md`
- `docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md`
- `CAPACITY_1_REALITY_AUDIT_REPORT.md`
- `CHANNEL_SCORE_REALITY_AUDIT.md`
- `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`
- ADR-009
- ADR-010
