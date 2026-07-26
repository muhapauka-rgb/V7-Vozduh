# M5a: истёкшее approval и fresh reconciliation

Дата: 2026-07-26
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Полученное exact approval относилось к request
`accauth_r1_c956e2cc486f8364e80035c3`, который истёк в
`2026-07-26T16:25:43.918931+00:00`. В момент проверки production clock был
`2026-07-26T16:29:17Z`; выдача contract была законно отклонена как stale.

Существующий read-only autoswitch producer и append-only audit owner выдали
и зарегистрировали новый request:

- `request_id`: `accauth_r1_c3a68b774a0e483e98bf1933`;
- `request_hash`: `c3a68b774a0e483e98bf1933356daa0321bdd57a64dbf8d2bff5c637f25b0edb`;
- expiry: `2026-07-26T16:35:02.540445+00:00`;
- scope: `10.0.0.2`, `vless -> wireguard-1779454504-c43409`, one user and
  one concurrent transaction;
- immutable audit record:
  `a43ac85c23abc02cc31a65ae41fd6c1ff40994bdd7273be6e31ebcfc0088fb4b`.

`tools/v7-truth-check --reconcile-action-class-contract-request` завершился
`PASS`: CPS update и reread атомарны. `contract_written=false`,
`packet_created=false`, `lease_created=false`, Runtime/Routing impact `NONE`,
`users_moved=0`, Authority impact `NONE`, Production Maturity `NO_CHANGE`.

Следующий legal terminal: независимое exact решение только по новому request.
