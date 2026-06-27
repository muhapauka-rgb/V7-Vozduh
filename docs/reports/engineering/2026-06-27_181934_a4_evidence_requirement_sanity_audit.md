# A4 Evidence Requirement Sanity Audit

Status: COMPLETE
Language: Russian
Runtime mutation: NO
Apply executed: NO
Users moved: NO
Thresholds changed: NO
Formulas changed: NO
New owner created: NO
New backlog item created: NO
Architecture changed: NO

## Summary

Проверен вопрос: должен ли A4 реально требовать все `156` representative candidate outcomes перед прогрессией.

Вывод:

`156` не является каноническим порогом A4. Это динамический размер текущего inventory покрытия `user -> candidate_channel`.

Текущее `62 remaining` является разрывом inventory coverage, а не доказанным минимальным критерием сертификации первой action class.

## Action Performed

Read-only аудит существующих владельцев:

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `admin_core/intelligence_workers.py`
- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-governed-canary-dry-run-cycle`

## Objective Observations

1. `candidate_count=156` создается динамически из текущего `candidate-suitability-summary`.

2. Точная единица:

```text
candidate_key = (user, candidate_channel)
```

3. Число `156` возникает из текущей производственной матрицы:

```text
active candidate users * candidate channels per user
```

4. Текущее состояние:

```text
candidate_outcomes_consumed = 94
candidate_count = 156
missing_candidate_outcomes = 62
coverage_ratio = 60.3%
```

5. Владельцы расчета:

```text
admin_core.intelligence_workers::_candidate_keys
admin_core.intelligence_workers::build_candidate_outcome_rows
admin_core.autonomy_trust_acceleration::build_candidate_outcome_reality_collection
```

6. Текущая реализация выставляет:

```text
readiness_impact.exact_outcome_deficit_blocks_canary = missing_candidate_outcomes
```

Это делает inventory deficit hard blocker, хотя canonical product/OMP intent говорит о representative action-class evidence.

## Engineering Conclusions

### 1. Why candidate_count = 156

Потому что текущий snapshot содержит `156` уникальных пар `user -> candidate_channel`.

### 2. What dimensions create this number

Только конкретный пользователь и candidate channel.

Это не action class, не protocol class, не cohort, не failure family и не statistical representative segment.

### 3. Are all 156 required for first action-class certification?

NO.

Каноническая цель A4:

```text
Materialize representative outcome evidence for the first action class.
```

Ни OMP, ни Product Specification, ни Policy 005 не требуют полного перебора всех текущих user-channel комбинаций.

### 4. Are 62 remaining mandatory?

NO as canonical completion condition.

YES only as current implementation inventory gap.

### 5. Can A4 progress with statistically sufficient representative evidence?

YES, if existing A4/B13 evidence owners prove representative class evidence, metric reliability, rollback/no-rollback semantics, verification, freshness, anti-flap, blast-radius safety, and learning quality.

This audit does not define or lower the threshold.

### 6. How A5/B13/A6 depend on this count

| Item | Dependency |
| --- | --- |
| `A5` | Consumes class-level evidence and blast-radius proof. It does not require full user-channel enumeration. |
| `B13` | Owns metric reliability for promotion recommendations. It should validate whether candidate coverage is a reliable signal, not treat full matrix coverage as the only proof. |
| `A6` | Consumes certified evidence for runtime eligibility arbitration. It should consume action-class certification, not raw enumeration alone. |

### 7. Is current A4 evidence target over-scoped?

YES, if interpreted as "collect all 156 before A4 can progress."

NO, if treated as a useful inventory coverage signal.

### 8. Minimum safe A4 completion criterion already defined

Existing OMP/policy intent requires:

- real representative outcomes;
- no synthetic evidence;
- terminal outcome classification preserved;
- verification passed where applicable;
- rollback/no-rollback evidence preserved;
- failure/rollback outcomes not counted as success;
- freshness/safety/anti-flap gates active;
- blast-radius remains one-user governed scope for this stage;
- B13 metric reliability confirms the evidence is suitable for promotion decisions.

### 9. Need formula or threshold change?

YES for the existing implementation gate, but not by lowering thresholds.

The minimal correction is to stop treating full `missing_candidate_outcomes == 0` as the A4 completion blocker and make it one signal inside representative evidence quality.

### 10. Need new architecture?

NO.

Existing owners cover this:

- A4 for representative evidence materialization;
- B13 for metric reliability;
- A5 for blast-radius proof;
- A6 for runtime eligibility consumption;
- Policy 005 for promotion semantics;
- Product Scale Model for non-enumerative production scale.

## Impact

Runtime behavior unchanged.

No evidence created.

No users moved.

No runtime automation enabled.

No authority expanded.

## Next OMP Step

Stop bounded collection as a completion strategy until the existing A4/B13 owner separates:

```text
inventory coverage signal
```

from:

```text
representative action-class completion criterion
```

Then resume A4 only through the corrected existing evidence gate.

## Final Verdict

`A4_EVIDENCE_REQUIREMENT_OVERSCOPED`
