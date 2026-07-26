# M5a: production caller и CPS consumption

Дата production caller: `2026-07-26T15:07Z`.

## Реальный caller -> consumer

Production non-test existing owner `/usr/local/bin/v7-users-autoswitch --action-class-contract-reconciliation-only` успешно вызван после deploy `deploy-z8-14-Updatesystem-6272950-20260726T220638`.

Он вернул `ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY` и единственный fresh M5a request:

- request ID: `accauth_r1_4a553e5a4151a81bb5a0ea38`;
- request hash: `4a553e5a4151a81bb5a0ea38289dd7fcb5b2f79bae0580a2f1469f1e8a274dfe`;
- expiry: `2026-07-26T15:12:15.276518+00:00`;
- class: `ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY`;
- action: `INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST`;
- scope: exact `10.0.0.2`, `vless -> wireguard-1779454504-c43409`, `max_users=1`, `max_concurrent_transactions=1`.

Existing source consumer `tools/v7-truth-check --reconcile-action-class-contract-request` validated and atomically projected this result into CPS: `ACTION_CLASS_CONTRACT_REQUEST_CPS_RECONCILED`, `ATOMIC_CPS_UPDATE_APPLIED`, reread `PASS`.

## Effects

Все запрещённые эффекты подтверждены как `false`/`0`: контракт не выдан, policy не записана, Candidate/Packet/lease не созданы, restore barrier не записан, apply/routing/user movement/rollback отсутствуют, Authority и Production Maturity не изменены.

## CPS/OMP result

CPS теперь хранит только current request identity, hash, expiry, fingerprint, status/scope и `CURRENT_PACKET=NONE`, `CURRENT_LEASE=NONE`. OMP pointer обновлён на exact M5a next action; он не создаёт новую Mission и не изменяет scheduler semantics.

## Legal terminal

Этот request короткоживущий и не переиспользуется. После expiry единственный legal путь — новый read-only production reconciliation. Пока request свеж, следующий шаг остаётся независимым exact Authority decision `APPROVE_ONCE_AS_SCOPED` или `DECLINE`; без него M5b/M5c и production action запрещены.
