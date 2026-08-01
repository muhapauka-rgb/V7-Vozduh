# Stage 10 receipt reuse и классификация active target trial

## Решение

`STAGE_10_REUSE_OR_INVALIDATION_DECISION = REUSE_VALID_RECEIPT`.

Канонический append-only receipt:

- Stage: `10`;
- receipt: `afstage_74d124e8951bfaccf499067a`;
- standing contract: `sdpc_285af5fc6f4de20415c3e5b1`;
- packet-set fingerprint: `16cb3dd28fb2842eb433ec823235da7e50bb758f18ba513f58165abcf03739c5`;
- Outcome/Replay/Learning: consumed;
- baseline reset: verified;
- ordinary customer count: `0`.

Проверенные material invalidation triggers: semantics, adapter, verification,
rollback/containment, receipt lineage и contract binding. Owner-backed
invalidation не найден. Изменение Matrix generation, route/current source,
target observation, CPS/report или возврат identity к baseline не являются
invalidation trigger и receipt не отменяют.

## Причина ложного противоречия

Активный runtime process имеет аргументы:

`--availability-first-stage 10 --availability-first-target-bound-trial-target awg3`.

Это не повторный campaign Stage 10. Это `TARGET_BOUND_TRIAL` с verified scope
`10` для `campaign_next_stage=25`. Уже существуют target-bound receipts,
также явно указывающие `campaign_next_stage=25`. Campaign receipt owner и
target-capacity owner — разные semantic classes.

## Исправление projection

Подготовлен commit `22de2622` (ещё не deployed, пока active transaction не
достигнет terminal): compact Matrix projection теперь выводит:

- `execution_scope_kind=TARGET_BOUND_TRIAL`;
- `trial_scope=10`;
- `campaign_stage=25`;
- target-bound identity.

Тем самым transient trial не может быть интерпретирован consumer как duplicate
completed campaign stage.

## Живой checkpoint

На момент наблюдения Matrix/service и governed executor active; active lease и
restore barrier принадлежат одному текущему packet-bound operation. Campaign
accounting: `48 = 43 baseline(vless) + 5 active_forward`; ordinary users `0`.
Новая transaction, Stage 25 или cancellation не выполнялись.

## Exact next step

Наблюдать существующий target-bound trial до terminal, затем atomically
reconcile Packet/lease/barrier, current routes и accounting. Только после
terminal target-bound trial допустим fresh capacity decision для campaign
Stage 25. Повторная campaign Stage 10 production credit запрещена.
