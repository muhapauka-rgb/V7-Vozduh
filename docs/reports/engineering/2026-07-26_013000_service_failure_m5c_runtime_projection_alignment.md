# Service Failure M5c: выравнивание Runtime Authority projection

Дата: `2026-07-26`
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Этап: `M5c — Execution-boundary preparation`, только read-only consumer alignment.

## Причина

Production planner уже останавливал каждый shadow recommendation до Packet,
lease и apply: текущий `/etc/v7/policy.json` не содержит валидного
`current_action_class_contract`. Однако автономный trust inventory по
умолчанию показывал исторический reference policy как
`DELEGATED_AUTONOMY` с `runtime_apply_enabled=true`. Это не давало Runtime
исполнение, но создавало противоречивую producer→consumer projection.

## Исправление

В существующем owner `admin_core/autonomy_trust_acceleration.py` reference
policy теперь означает ровно то, чем он является:

- `current_mode=GOVERNED_ONLY`;
- `runtime_apply_enabled=false`;
- `current_action_class_contract_state=MISSING`;
- eligibility возвращает точный blocker
  `CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`.

Только вызывающий owner, который прочитал фактический exact scoped contract,
может передать explicit `ACTIVE` state и runtime mode в read-only model. Это
не создаёт contract, Candidate, Packet, lease или approval.

## Проверка

- `120` unit tests trust/eligibility/OMP owners: `PASS`.
- Local `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only`:
  `GOVERNED_ONLY`, `MISSING`,
  `CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`,
  `runtime_can_execute_automatically=false`.

## Effects и terminal

Runtime apply, routing mutation, user movement, Packet/lease creation,
restore-barrier write, rollback apply, Authority expansion и Production
Maturity change: `NONE`.

`M5c` не может подготовить executable boundary без exact owner-issued
current action-class contract. Current legal terminal остаётся
`ENGINEERING_AUTHORITY`; exact next frontier остаётся
`V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION`.

## Production deploy и caller verification

Commit `8f0b47cf52b6635ddb11dd2602d9b1a042f1d18a` deployed through
`tools/v7-safe-deploy`:
`deploy-z8-14-Updatesystem-8f0b47c-20260726T012213`.

Production non-test caller
`/usr/local/bin/v7-autonomy-trust-evidence-inventory --action-class-runtime-only`
returned the exact intended consumed result:

- `current_mode=GOVERNED_ONLY`;
- `current_action_class_contract_state=MISSING`;
- `runtime_apply_enabled=false`;
- `runtime_can_execute_automatically=false`;
- blocker `CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`.

`tools/v7-truth-check --all --json`: `PASS`.
`tools/v7-convergence-status --json`: `ALIGNED`; local, GitHub and production
all equal `8f0b47cf52b6635ddb11dd2602d9b1a042f1d18a`.
