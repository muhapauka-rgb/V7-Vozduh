# Engineering Report: A4 Marginal Evidence Value Note

## Summary

Зафиксирована неблокирующая будущая оптимизация A4: выбирать не просто любого безопасного кандидата, который закрывает текущий evidence gap, а самого ценного из текущих безопасных кандидатов.

## Action Performed

Обновлены существующие владельцы: OMP и Current Program State. Новый backlog item, новый owner, runtime change или authority expansion не создавались.

## Objective Observations

Текущая A4-логика корректно отвечает: `Does this candidate reduce the A4 evidence gap?`

Будущая оптимизация может отвечать: `Among currently eligible candidates, which one gives the highest marginal evidence value?`

## Engineering Conclusions

Marginal Evidence Value определяется как:

`expected A4 gap reduction + verified learning value + new cohort/user/channel coverage value - movement/risk/cost/anti-flap penalty`.

Это efficiency improvement, а не required fix.

## Impact

Текущий A4 не блокируется. Runtime automation остается disabled. Batch movement не разрешен. Один governed transaction по-прежнему ограничен одним пользователем и должен останавливаться на любом failed live gate.

## Capability Progress

A4 остается `88 / 156 = 56.4%`; missing evidence остается `68 / 156 = 43.6%`.

## Backlog Progress

Новый backlog item не создан. Текущий highest leverage item остается `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`.

## Production Maturity

Production Maturity остается `24.0%`.

## Canonical Knowledge

Durable note записана в OMP и Current Program State как `A4_MARGINAL_EVIDENCE_VALUE_RANKING`.

## Evidence

Изменения документационные. Код, runtime behavior, thresholds, formulas, authority и apply не менялись.

## Next Step

Продолжить OMP: требуется operational authority для одного bounded A4 evidence collection cycle, максимум `68` successful missing candidate outcomes.

## Re-audit Rule

MEV-ранжирование не переоткрывать как блокер A4. Возвращаться к нему только при оптимизации candidate selection, intelligence workers, outcome leverage model или A4 read-model.
