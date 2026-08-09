# CT-M0F: сохранение invalid sample diagnostic и deploy scope blocker

Дата: 2026-08-10

## Результат

Исправлен существующий CT-M0F reservation/audit consumer. Невалидная
контролируемая попытка больше не теряет точную причину как
`sample_forward_evidence_missing_or_invalid_after_safe_reconciliation`.
Она сохраняется тем же append-only audit owner как
`INVALID_DIAGNOSTIC_EVIDENCE` и затем закрывается тем же reservation terminal.
Новый store, watcher, planner, Runtime или Authority owner не создан.

## Owner-backed причина

Обычный production Matrix run 2026-08-09 прошёл собственную цепочку
Matrix -> advisory -> OMP consumer -> CT-M0F consumer. Три reservation одного
implementation fingerprint были закрыты invalid без forward-evidence record:

- `ctm0fsample_5cac2a6d58efa4a78ad1613d`;
- `ctm0fsample_0ca65592b879af11202e8919`;
- `ctm0fsample_feeda120d7a687c316e49705`.

После третьего terminal существующий budget правильно отказал новой попытке:
`ct_m0f_standing_validation_budget_exhausted`. Последний ответственный link
оказался в CT-M0F cutover-evidence producer -> reservation audit consumer:
consumer сохранял только `CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS`, поэтому
diagnostic invalid result не имел durable payload.

## Реализация

Commit `114f649091df15b2c65e17508e2d1d48c70e7c48`:

- `admin_core/operator_execution.py`: тот же forward-evidence record теперь
  хранит строго либо valid evidence, либо invalid evidence с непустым
  predicate/blocker; повтор и конфликт остаются fail-closed;
- `tools/v7-governed-canary-dry-run-cycle`: отсутствие output от route/apply
  consumer сохраняется как `CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID` с
  точным producer-consumer diagnostic, а не подменяется успехом;
- CPS/Service Failure Program нормализованы к фактическому claim class
  `CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER`, не к неподтверждённому user-path
  latency claim.

Production effects этого engineering repair: `NONE`. Не выполнялись policy
write, Candidate/Packet/lease creation, restore-barrier write, apply, routing
mutation, user movement, rollback, Authority expansion или Production Maturity
change.

## Проверка

Пройдены 272 affected unit tests:

```text
python3 -m unittest tests.unit.test_operator_execution_packet \
  tests.unit.test_service_failure_episode tests.unit.test_governed_canary_cli
```

Отдельный test доказывает:

```text
invalid exact observation
-> INVALID_DIAGNOSTIC_EVIDENCE
-> one reservation terminal
-> invalid attempt count increments once
-> no active reservation remains
```

## Deploy truth и legal terminal

Local и GitHub указывают на commit `114f6490`. Production остаётся на
`b5e52067` до safe deploy.

Штатный `tools/v7-safe-deploy --json` прошёл allowlist и GitHub truth, но
показал три несовпадения:

1. `admin_core/operator_execution.py` — требуемый repair;
2. `tools/v7-governed-canary-dry-run-cycle` — требуемый repair;
3. `docs/reference/V7_RUNTIME_MODEL.md` — накопившийся независимый docs delta.

По правилу точного deploy scope production deploy не выполнялся: штатный
инструмент в этой конфигурации не может применить только первые два файла.

Текущий legal terminal:

```text
SAFE_DEPLOY_SCOPE_SEPARATION_REQUIRED
```

Re-entry owner: существующий `tools/v7-safe-deploy` scope/manifest owner.
Re-entry condition: manifest, содержащий только два runtime repair файла, либо
явно одобренный независимый scope, включающий также runtime-model contract.
После успешного safe deploy следующий owner — обычный Matrix timer; он создаёт
новую generation сам, без Codex/manual Matrix invocation.
