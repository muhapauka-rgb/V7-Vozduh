# CT-M0F: независимая линия, контракт и reconciliation substrate

Дата: `2026-08-08T22:29:36+07:00`  
Режим: `read-only production reconciliation + canonical Program clarification`

## Итог

`CT_M0F_STANDING_CONTROLLED_FAILURE_READY` пока не может быть сформирован.
Это не ожидание Stage-48, не просроченный approval и не дефект автоматического
wake: активный standing CT-M0F contract существует, но существующий
controlled-pool owner не нашёл точную безопасную тройку для controlled sample.

## Свежая production truth

Проверен существующий production entrypoint
`/usr/local/bin/v7-users-autoswitch --ct-m0f-standing-source-selection`.

| Поле | Owner-backed результат |
|---|---|
| Contract | `ctm0fsdpc_208482a67dc4103e5f0ef7b6` — `ACTIVE` |
| Expiry | `2026-09-05T09:32:42.689887+00:00` |
| Envelope | один certification user, одна concurrent operation, CT-M0F only |
| Selection status | `STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED` |
| Eligible source / identity | `0 / 0` |
| Production effects | все `false`, `user_movement=0` |

Точные blockers:

```text
no_healthy_isolated_controlled_source_with_group_aligned_certification_identity
no_exact_certification_identity_for_controlled_condition
no_distinct_controlled_contract_admitted_target
```

## Проверенная причинность

Существующий selection owner допускает только source, который уже является
controlled-certification source, изолирован от обычных пользователей и имеет
group-aligned certification identity. Для deliberately disabled
`EXECUTION_ONLY` source он восстанавливает только точную existing-owner
execution lineage; generic production channel не является допустимой заменой.
Следовательно, блокер не может быть снят выбором «любого работающего канала»:
это создало бы source/identity/policy effect за пределами active contract.

## Отдельный найденный consumer gap

Локальный CPS Section 0 ещё указывает на исторический pending request
`ctm0fsdpauth_r1_0c4ee69155202936f0d8bb06` и
`ENGINEERING_AUTHORITY`, тогда как свежий production policy/audit owner
подтверждает активный contract `ctm0fsdpc_208482a67dc4103e5f0ef7b6`.
Это stale contract-projection gap между existing policy/audit producer и
CPS/OMP consumer; он не отменяет substrate blocker, но не должен скрываться
за ним. Его exact repair frontier: existing Matrix/policy-audit contract-state
consumer -> atomic CPS/OMP projection `ACTIVE_CONTRACT +
AUTO_REENTRY_ON_CONTROLLED_POOL_CHANGE`. До production deployment этого
consumer repair нельзя выдавать CPS local documentation за production runtime
consumption.

## Внесённое canonical уточнение

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md` обновлён до V5.0:

1. policy/audit owner заново сверяет contract ID/hash, expiry и envelope перед
   каждой Matrix generation;
2. CT-M0F отделён от Stage-48 только при доказанном отсутствии shared
   source/target/identity/reservation/operation/lock;
3. implementation fingerprint rebind разрешён лишь внутри неизменного
   standing envelope;
4. Matrix/timer остаётся единственным ordinary wake owner;
5. controlled condition требует exact contract admission и сохраняет реальную
   provenance failure clock;
6. отсутствие controlled triple получает durable automatic re-entry через
   existing pool/Matrix source-change consumer, без ручного запуска;
7. deploy boundary нельзя обходить policy write или другим execution command.

## Проверка

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q \
  tests.unit.test_service_failure_episode \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet
PASS (только существующие DeprecationWarning invalid escape sequence)
```

## Legal terminal и re-entry

Текущий terminal: `EXTERNAL_OWNER_OR_CONTROLLED_SUBSTRATE_REQUIRED`.

Автоматический re-entry: следующая owner-backed topology, health, identity,
reservation или policy generation -> existing controlled-certification
pool/Matrix source-change consumer -> fresh source selection. Ни Candidate,
ни Packet/lease, ни restore barrier, ни routing/user movement до появления
точной допустимой тройки не создаются.

Production implementation deploy для этого документа не требуется. Отдельно
остаётся уже известное independent deploy-review boundary для ранее
подготовленного V3 auto-substrate source change; оно не было обойдено и не
используется как основание для CT-M0F action.
