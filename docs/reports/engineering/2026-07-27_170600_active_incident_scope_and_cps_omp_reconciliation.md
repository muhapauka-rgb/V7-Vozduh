# Reconciliation active VLESS incident: scope → CPS/OMP

Дата: `2026-07-27`  
Mission: `V7_SERVICE_FAILURE_ACTIVE_INCIDENT_CPS_OMP_PROJECTION_RECONCILIATION_V1`  
Статус: `CONSUMED_ACTIVE_INCIDENT_SUCCESSOR_PUBLISHED`

## Факт и причина

Production Matrix подтвердил продолжающуюся деградацию VLESS: `1/14` сервисов
доступен. Старый compact projection ошибочно считал исторический packet outcome
за защиту новой source-scope generation только по времени outcome. Поэтому
`protected_scope=1` не был доказан текущим scope lineage.

Исправленный existing owner требует одновременно:

`exact source_scope fingerprint + source count + source channel + current route truth`.

Исторические outcomes не удалены и не переиспользованы: они сохранены как
lineage, но не уменьшают новый denominator без exact membership binding.

## Живой scope

Incident: `sfinc_be20296fba3d8a6a33e58a583f1b58db`  
Generation: `egid_be6367407f70e591005185a2`  
Current source-scope event: `sfrev_d08397ac0bac5b0b3f0fa675d5c78b36`  
Fingerprint: `07c292f68339f7ec87370d2608b4a8de650cc0af7f1a330d8dbc744112a65967`

| Категория | Count | Основание |
| --- | ---: | --- |
| affected | 53 | current Matrix snapshot / `users.registry` owner |
| protected | 0 | нет packet-bound outcome с exact current scope generation |
| unresolved | 53 | current live VLESS assignments |
| explicitly excluded/recovered | 0 | нет current-generation closure pointer |

Инвариант выполнен: `53 = 0 + 53 + 0`.

Пользователи `10.0.0.2`, `10.0.0.3` и `10.7.0.18` сейчас находятся на
`wireguard-1779454504-c43409`. Их старые packet/outcome pointers сохранены,
но не считаются protected current-generation scope: у `10.0.0.2` нет incident
binding, у `10.0.0.3` и `10.7.0.18` binding относится к pre-baseline scope.
Legacy generation `55` явно invalidated, а не «сжата» молча.

## Потребление и successor

Production OMP receipt: `sfomp_c12b66c38f9c7b0f248802df`.

```text
verified historical outcome
-> live scope reconciliation
-> production OMP receipt
-> atomic source CPS/OMP projection
-> event-driven wake request
-> CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN
```

Caller: `tools/v7-service-matrix-refresh-all`.
Consumer: `tools/v7_sync_lib.continue_omp_engineering_control_loop`.
Ни Candidate, Packet, lease, apply, routing mutation, rollback, Authority
expansion или Production Maturity change этой reconciliation не создавала.

## Tier и Program residual

Certified/Authority-approved/Runtime-enabled tier остаётся `1` (standing
delegated policy, max users `1`, max concurrent transactions `1`). Исторические
tiers `2/5/10/bounded` — evidence, не действующая Runtime authority; они не
пересертифицируются без declared invalidation. Точный текущий M7 verdict:
`HOLD_CURRENT_TIER_ACTIVE_INCIDENT_SCOPE_REVALIDATION_REQUIRED`.

`CAUSAL_M4`–`CAUSAL_M10` не объявлены completed: их residual — текущий
unrecovered incident и последующая fresh revalidation через уже published
successor. Terminal `PERSISTENT_INCIDENT_CAUSAL_CLOSURE_RUNTIME_CONSUMED` пока
не допустим: `unresolved_scope=53`.

## Проверки

- focused unit suite: `102 PASS`;
- safe deploy manifests: только `tools/v7-users-autoswitch` и затем
  `tools/v7_sync_lib.py`, оба `PASS`;
- production caller/consumer и source receipt reconciliation: `PASS`;
- truth: `FULLY_ALIGNED`;
- convergence: `PASS / ALIGNED`.
