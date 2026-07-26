# M5a: production request audit registration verification

## Реальный caller / consumer

После deploy `deploy-z8-14-Updatesystem-dc8ddc9-20260726T230838` existing production chain успешно выполнил:

`v7-users-autoswitch read-only reconciliation -> operator-execution audit request registration -> source CPS consumer`.

Зарегистрирован один short-lived immutable preimage:

- request ID: `accauth_r1_fbd403e97422f1684420e5d3`;
- request hash: `fbd403e97422f1684420e5d3f167fdbe9dd58d13490c76e6b0dc7ada73c636d7`;
- expiry: `2026-07-26T16:14:14.985800+00:00`;
- audit record hash: `bb53bc58c98996a712dfd12e6a9e6867205a8c34607ce08613edb79588d5432e`.

Scope exactly: user `10.0.0.2`, `vless -> wireguard-1779454504-c43409`, one user and one concurrent transaction.

## Safety result

Registration returned `REGISTERED`, `policy_write=false`. Contract не выдан; Candidate, Packet, lease, restore barrier, apply, routing mutation, user movement, rollback, Authority expansion и Production Maturity change отсутствуют.

`tools/v7-truth-check --reconcile-action-class-contract-request` потребил тот же preimage в CPS atomically: `PASS`, `ATOMIC_CPS_UPDATE_APPLIED`, reread `PASS`.

## Terminal

Следующая и единственная разрешённая операция — independent exact `APPROVE_ONCE_AS_SCOPED` или `DECLINE` для указанного ID/hash до expiry. Existing issuer теперь сможет потребить этот immutable audit preimage без повторного producer call. После expiry нужен новый request; старый не переиспользуется.
