# Engineering Report: A4 architecture intent audit

Status: COMPLETE
Language: Russian
Task: A4 architecture / OMP intent audit
Runtime mutation: NO
Apply executed: NO
Users moved: NO
Code inspected first: NO
Thresholds changed: NO
Formulas changed: NO
Runtime behavior changed: NO
New owner created: NO
New backlog item created: NO
Architecture changed: NO

## Summary

Аудит сначала установил исходное намерение OMP и Product Architecture без просмотра реализации.

Вывод:

```text
Original intent = Representative action-class evidence
Not = Enumeration of every user -> candidate-channel combination
```

Текущая реализация соответствует этому намерению только частично: она использует `user -> candidate_channel` coverage как важный suitability signal, но этот enumeration signal не должен становиться постоянной заменой action-class evidence.

## Action Performed

Прочитаны intent-документы в заданном порядке:

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md`
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`
- `docs/reference/V7_RUNTIME_MODEL.md`

Только после установления intent была проверена текущая реализация:

- `admin_core/intelligence_workers.py::_candidate_keys`
- `admin_core/autonomy_trust_acceleration.py::build_candidate_outcome_reality_collection`
- `admin_core/autonomy_trust_acceleration.py::_promotion_missing_evidence`

## Objective Observations

### OMP intent

OMP описывает A4 как:

```text
A4: Materialize representative outcome evidence for the first action class.
```

Связанные формулировки OMP:

- Autonomy Promotion Engine governs action classes, not individual packets.
- OMP asks whether this action class can move to the next autonomy state.
- A4 gives promotion decisions enough real evidence.
- Learning target requires representative evidence and metric reliability.
- A4 and B13 must precede authority expansion recommendations.

OMP intent: action-class promotion through representative real outcomes.

### Product intent

Product Specification says:

- Autonomy Promotion Engine decides whether an action class has enough real evidence to be promoted.
- An action class is a repeated kind of product action.
- Promotion is based on real outcomes, verification, rollback quality, safety, blast radius, learning, trust, and authority policy.
- Runtime asks whether a fresh packet belongs to an approved action class inside an approved Autonomy Policy.
- Action-class promotion is never based on reports alone.

Product intent: durable action-class evidence, not packet or identity enumeration as the product abstraction.

### Policy 005 intent

`POLICY_005_ACTION_CLASS_PROMOTION.md` says:

- Action class promotion moves a repeated operational capability from manual/governed use toward broader automation only after evidence proves it safe at the next scope.
- One successful canary is not sufficient proof for unbounded promotion.
- Canary representativeness matters.
- Promotion after repeated success is safer than promotion after one success.
- V7 fit analysis maps representativeness preservation to A4.
- Metric reliability is mapped separately to B13.

Policy intent: representative action-class evidence with staged promotion.

### Production Maturity intent

`V7_PRODUCTION_MATURITY_MODEL.md` describes A4 as representative outcome evidence for the first action class and says `REAL_WORLD_LIMIT` applies if representative outcomes are insufficient.

Production Maturity intent: production readiness grows through repeated real representative outcomes, not through full user/channel enumeration.

### Runtime Model intent

`V7_RUNTIME_MODEL.md` says Runtime executes certified action classes only when OMP and authority policy have promoted that class.

Runtime Model intent: Runtime consumes promoted action-class state; it does not promote classes and does not require every concrete user/channel combination as the architectural approval object.

## Implementation Comparison

Current implementation uses:

```text
candidate_key = (candidate_user, channel)
missing_keys = candidate_keys - consumed_keys
missing_candidate_outcomes = len(missing_keys)
```

This is calculated through:

```text
admin_core.intelligence_workers._candidate_keys
admin_core.autonomy_trust_acceleration.build_candidate_outcome_reality_collection
admin_core.autonomy_trust_acceleration._promotion_missing_evidence
```

The implementation is valid as a suitability knowledge signal.

It is only partially aligned if the `missing_candidate_outcomes` number is treated as the primary or exhaustive action-class promotion requirement.

## Engineering Conclusions

### 1. Original OMP intent

Representative action-class evidence.

### 2. Original Product intent

Representative action-class evidence.

The Product Architecture wants the operator/product layer to think in terms of action classes, policy, real outcomes, rollback, verification, learning, and authority boundaries.

### 3. Current implementation match

```text
PARTIAL
```

It matches the requirement for real observed outcomes and no synthetic evidence.

It partially diverges because its dominant numeric blocker is currently user->candidate-channel enumeration coverage.

### 4. Classification

This is:

```text
unfinished implementation of the existing design
```

It is not required architectural evolution.

It is not proof that a new owner is needed.

It is not proof that a new backlog item is needed.

It may become implementation drift only if future OMP treats full user->candidate-channel enumeration as the canonical action-class certification rule.

### 5. Existing backlog owner

Primary:

```text
A4: Materialize representative outcome evidence for the first action class.
```

Supporting:

```text
B13: Certify metric reliability for automated promotion recommendations.
```

Related downstream:

```text
A6: Implement action-class runtime eligibility arbitration using certified gates.
```

### 6. Is A4 intended to solve it?

Yes.

A4 is the intended owner for turning first-class real outcome evidence into representative action-class evidence.

### 7. Is B13 intended to solve it?

Partially.

B13 is not the primary evidence-materialization owner.

B13 is the owner that prevents weak or misleading metrics, including raw enumeration coverage, from becoming unsafe automated promotion recommendations.

### 8. Is a new backlog item required?

No.

Need New Backlog Item:

```text
FALSE
```

Need New Owner:

```text
FALSE
```

Architecture Extension:

```text
NO
```

## Impact

Engineering Maturity: unchanged at `100.0%`.

Production Maturity: unchanged at `24.0%`.

Runtime automation: disabled.

Users moved: `0`.

No runtime behavior changed.

No code changed.

No formulas or thresholds changed.

## Capability Progress

| Capability | Progress |
| --- | ---: |
| Learning | `40.0%` |
| Authority Evolution | `40.0%` |
| Production Readiness | `24.0%` |
| Production Autonomy | `0.0%` |
| Movement Protection | `35.7%` |

## Backlog Progress

| Scope | Progress |
| --- | ---: |
| Tier A | `3 / 6` = `50.0%` |
| Tier B | `0 / 21` = `0.0%` |
| Tier C | `0 / 7` = `0.0%` |
| Overall actionable | `3 / 34` = `8.8%` |

## Canonical Knowledge

No additional canonical owner update was required in this audit.

The durable knowledge is already mapped to the existing owners:

- `POLICY_005_ACTION_CLASS_PROMOTION`
- OMP Autonomy Promotion Engine
- `A4`
- `B13`
- `A6`
- Canonical Reference A4 representative evidence scope

## Next Step

Continue OMP through existing backlog only.

Do not create a new backlog item.

Do not redesign architecture.

Do not change thresholds.

When OMP selects implementation work, extend existing A4/B13/A6 semantics so:

```text
candidate_count remains a suitability signal
representative action-class evidence remains the promotion target
metric reliability prevents raw enumeration from becoming unsafe promotion proof
```

## Re-audit Rule

Do not re-audit this intent unless:

- OMP changes A4 wording materially;
- Product Specification changes action-class promotion semantics;
- `POLICY_005_ACTION_CLASS_PROMOTION` changes materially;
- Runtime Model starts treating user/channel enumeration as the authority object;
- explicit operator request.

