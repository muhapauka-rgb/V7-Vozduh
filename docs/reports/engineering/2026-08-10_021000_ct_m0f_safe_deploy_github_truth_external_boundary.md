# CT-M0F: safe-deploy GitHub truth external boundary

Дата: 2026-08-10

## Результат

Проверен текущий CT-M0F deploy frontier без создания нового owner, deploy
mechanism, Runtime Model, registry или state surface. Исторический terminal
`SAFE_DEPLOY_SCOPE_SEPARATION_REQUIRED` больше не является текущей причиной
остановки: `docs/reference/V7_RUNTIME_MODEL.md` уже является allowlisted
production Runtime contract и должен быть частью штатного manifest, если его
локальный hash отличается от production.

Текущий exact terminal:

```text
EXTERNAL_GITHUB_TRUTH_ACCESS_REQUIRED
```

## Свежая owner-backed проверка

`tools/v7-safe-deploy --json` на local `37d4325f` показал:

- allowlist: `PASS`;
- ожидаемые Runtime mismatch: `admin_core/operator_execution.py`,
  `tools/v7-governed-canary-dry-run-cycle` и
  `docs/reference/V7_RUNTIME_MODEL.md`;
- `V7_RUNTIME_MODEL.md` имеет existing deploy owner
  `tools/v7_sync_lib.APPROVED_DEPLOY_FILES` и remote path
  `/opt/v7/engineering/reference/V7_RUNTIME_MODEL.md`;
- blocker: `github_truth_check_failed`.

Последний blocker подтверждён независимо:

```text
git ls-remote origin Updatesystem
-> Could not resolve host: github.com

gh auth status
-> active GitHub token is invalid
```

Следовательно, исключить Runtime Model из manifest или ослабить scope classifier
было бы ошибкой: это скрыло бы реальное production contract mismatch. В код
`tools/v7-safe-deploy` и `tools/v7_sync_lib.py` изменения не вносились, потому
что current scope behavior доказан как существующая safety invariant, а не как
implementation defect.

## Неизменённые границы

Не выполнялись production deploy, policy write, Candidate/Packet/lease creation,
restore-barrier write, Matrix invocation, routing mutation, user movement,
rollback, Authority expansion или изменение Production Maturity. 272 focused
tests repair commit `114f6490` сохраняют valid evidence: remote-access failure
их не инвалидирует.

## Re-entry

Owner: existing GitHub truth consumer inside `tools/v7-safe-deploy` /
`tools/v7-truth-check`.

Condition: GitHub DNS becomes reachable and the configured GitHub authentication
is restored by its external credential owner. No credential was requested,
received or stored.

После этого единственный следующий безопасный шаг:

```text
tools/v7-safe-deploy --json
-> manifest/truth PASS
-> tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED
-> production caller/consumer verification
-> ordinary Matrix-owned CT-M0F generation
```

До выполнения condition CT-M0F остаётся incomplete; повторять tests, scope
analysis или ручной Matrix run нельзя.
