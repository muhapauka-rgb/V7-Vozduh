# Engineering Report — Service Failure Lifecycle M0

Дата: `2026-07-25`

Mission: `V7_SFL_M0_CURRENT_STATE_AND_RESIDUAL_RECONCILIATION_V1`

Verdict: `PASS_RESIDUAL_PROVEN`

## Fresh truth

- local/GitHub/production source до Mission: `8a79dd7cd0c79e72ccb3b198c0fc832d9ce3d333`;
- production timer: `OnUnitActiveSec=15min`, `RandomizedDelaySec=60s`;
- последний production lifecycle: start `2026-07-25 17:54:32 MSK`,
  exit `17:55:36 MSK`, `Result=success`, `ExecMainStatus=0`;
- passive production consumer: `PASS`, forbidden effects отсутствуют;
- `egress.registry`: `vless` имеет protocol `vless`; numeric `id=1` имеет
  protocol `amneziawg` и является отдельным canonical egress;
- VLESS outbound сохранён только как fingerprint
  `a476ada6de9cc2f99b74e8d358ac520d14b529944aec1d5eb4f7d95379e9228d`;
  endpoint/credentials не извлекались в отчёт.

## Current incident

- `vless`: `1/14 OK`, `13/14` persistent failures, шесть samples,
  episode start около `2026-07-25T13:37:41Z`;
- production runtime logs подтверждают upstream `TCP_CONNECTION_REFUSED`;
- `id=1` AmneziaWG: `0/14 OK`, transport timeout family;
- VLESS нельзя честно назвать total channel hard-fail: Telegram остаётся
  reachable, поэтому доказан partial service-plane incident с upstream refused;
- Natural L8 credit: `NO`; provenance остаётся
  `EXTERNAL_UNATTRIBUTED`, пока owner-backed provenance/outcome contract не
  докажет иное.

## Proven residual

1. Continuity была magic literal `2100`, а не derivation от cadence/jitter/batch.
2. Episode ID не включал registry/config generation и failure family.
3. Durable emitted-event metadata терялась при следующей Matrix записи; один
   deterministic event повторно добавлялся в JSONL.
4. Production snapshot: 79 rows для `vless`/`1`, `source_incident_id=0`,
   recovery events `0`.
5. 13 сервисных failures создавали независимые Situation chains вместо одного
   correlated parent incident.
6. Recovery не обновляла temporal outcome/closure через passive consumer.
7. Успешный passive capture не материализовал exact OMP product frontier;
   repair frontier существовал только для consumer failure.
8. Multi-lane selector был hard-coded только на channel hard-fail.
9. Polygon не различал все required families: partial service, refused,
   timeout, DNS, TLS, intermittent/recovery и correlated provider incident.

## Exact next

`V7_SFL_M1_EPISODE_IDENTITY_RECOVERY_AND_INCIDENT_CORRELATION_V1`

Forbidden effects: `NONE`.
