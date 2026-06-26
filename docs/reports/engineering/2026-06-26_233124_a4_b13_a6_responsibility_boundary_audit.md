# Engineering Report: A4 / B13 / A6 Responsibility Boundary Audit

Дата: 2026-06-26

## Summary

Проведен архитектурный audit границ ответственности между `A4`, `B13` и `A6` без инспекции runtime implementation и без изменения OMP, Runtime, backlog или кода.

Итог: overlap не найден. Ownership gap не найден. Новый владелец не нужен. Новый backlog item не нужен.

## Action Performed

Прочитаны существующие владельцы:

- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`;
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`;
- `docs/product/V7_PRODUCT_SPECIFICATION.md`;
- `docs/reference/V7_RUNTIME_MODEL.md`;
- `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md`;
- `docs/reference/V7_CANONICAL_REFERENCE.md`;
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Implementation code не инспектировался.

## Objective Observations

`A4` уже определен как materialization of representative outcome evidence for the first action class.

`B13` уже определен как certification of metric reliability for automated promotion recommendations.

`A6` уже определен как action-class runtime eligibility arbitration using certified gates.

`POLICY_005_ACTION_CLASS_PROMOTION` подтверждает:

- one canary is not proof for unbounded promotion;
- promotion needs real outcomes, verification, rollback quality, safety, blast radius, learning, trust, and authority policy;
- automated promotion from metrics is allowed only when metrics are reliable and rollback is ready;
- metrics may recommend promotion, but cannot grant authority alone.

## Responsibility Classification

| Backlog item | Single responsibility | OWNED | CONSUMES | PRODUCES | DEPENDS_ON |
| --- | --- | --- | --- | --- | --- |
| `A4` | Materialize representative real outcome evidence for the first action class. | Representative action-class evidence materialization. | A3 real no-rollback outcome, feedback/learning, suitability/outcome inventory, real comparable governed/manual outcomes. | Representative evidence set, evidence gap status, real-world evidence boundary. | Real comparable outcomes; no synthetic evidence; existing feedback/learning owners. |
| `B13` | Certify whether promotion metrics are reliable enough to support automated promotion recommendations. | Metric reliability certification for promotion recommendations. | A4 representative evidence, trust/confidence, freshness, rollback/no-rollback, eligibility, verification quality. | Certified or rejected metric reliability verdict; promotion recommendation reliability status. | Representative outcome evidence; rollback readiness; metric source freshness; verification quality. |
| `A6` | Implement runtime eligibility arbitration that consumes certified gate outputs and produces one runtime `EXECUTE` or `STOP_SAFE` decision. | Runtime eligibility arbitration across existing gates. | A1-A5 gate outputs, action-class state, authority, freshness, blast radius, rollback, anti-flap, verification, learning, and B13 metric reliability where promotion recommendation quality is required. | Unified runtime eligibility result; execute-or-stop decision surface; runtime readiness state. | Certified gates; approved authority/policy where required; no runtime apply enabled by this item alone. |

## Must Never Own

| Backlog item | Must NEVER own |
| --- | --- |
| `A4` | Runtime execution, authority expansion, metric reliability certification, blast-radius certification, runtime eligibility arbitration, formula changes, threshold lowering, synthetic evidence creation. |
| `B13` | Evidence creation, outcome fabrication, authority approval, runtime execution, runtime arbitration, action-class certification by itself, backlog reprioritization by metrics alone. |
| `A6` | Evidence generation, metric reliability proof, action-class promotion, authority expansion, planner reranking, packet approval retirement by itself, runtime apply enablement. |

## Dependency Graph

```text
A4
  -> representative action-class evidence
  -> B13
  -> certified metric reliability for promotion recommendations
  -> A6
  -> runtime eligibility arbitration consumes certified gates
  -> EXECUTE or STOP_SAFE readiness
```

Important qualifier:

`A6` also depends on `A1-A5` gate outputs by backlog definition. `A5` remains the separate owner for class-level blast-radius certification. `B13` is required before automated promotion recommendations or authority expansion can rely on metrics. `A6` may implement arbitration as a read-model/eligibility surface, but it must not enable runtime autonomy without the required certified gates and authority.

## Engineering Conclusions

The correct split is:

```text
A4 = evidence materialization
B13 = metric reliability certification
A6 = runtime eligibility arbitration
```

This matches:

- OMP dependency rule: `A4` and `B13` precede authority expansion recommendations; `A6` precedes runtime autonomy readiness.
- Product Specification: action-class promotion uses real operational experience; runtime executes certified decisions only.
- Runtime Model: Runtime consumes promoted class state and existing owner evidence; OMP owns promotion.
- POLICY_005: automated metric promotion is acceptable only after metric reliability and rollback readiness.

## Impact

Production impact: OMP can continue from `A4` without mixing representative evidence work with metric certification or runtime arbitration.

Runtime impact: none. Runtime behavior did not change.

## Capability Progress

- Learning: `40.0%`, blocked by additional real representative outcomes.
- Authority Evolution: `40.0%`, blocked by evidence, metric reliability, and authority approval.
- Runtime Eligibility: `28.6%`, blocked by A6 and certified gate inputs.
- Production Readiness: `24.0%`.
- Production Autonomy: `0.0%`.

## Backlog Progress

- Tier A: `3 / 6` complete, `50.0%`.
- Overall actionable backlog: `3 / 34` complete, `8.8%`.
- Current highest priority remains `A4`.

## Canonical Knowledge

No canonical owner update required. The responsibility boundary is already represented by:

- `V7_IMPLEMENTATION_BACKLOG.md`;
- `OPERATIONAL_MATURITY_PROGRAM.md`;
- `V7_RUNTIME_MODEL.md`;
- `POLICY_005_ACTION_CLASS_PROMOTION.md`;
- `V7_CANONICAL_REFERENCE.md`.

## Evidence

Key evidence:

- `V7_IMPLEMENTATION_BACKLOG.md`: `A4`, `B13`, and `A6` have distinct tasks, owners, dependencies, and implementation classes.
- `OPERATIONAL_MATURITY_PROGRAM.md`: dependency rules say `A4` and `B13` precede authority expansion recommendations; `A6` precedes runtime autonomy readiness.
- `V7_RUNTIME_MODEL.md`: Runtime consumes promoted class state; OMP owns action-class promotion.
- `POLICY_005_ACTION_CLASS_PROMOTION.md`: one canary is insufficient; metric promotion requires reliable metrics and rollback readiness.

## Next Step

Continue OMP with `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`.

If a fresh governed production action becomes eligible, prepare exact operational authority request. Otherwise stop at `REAL_WORLD_LIMIT` and wait for real comparable outcomes.

## Re-audit Rule

Re-audit A4/B13/A6 boundaries only if:

- backlog definitions materially change;
- POLICY_005 changes;
- Runtime Model changes;
- production evidence contradicts the current boundary;
- operator explicitly requests re-audit.
