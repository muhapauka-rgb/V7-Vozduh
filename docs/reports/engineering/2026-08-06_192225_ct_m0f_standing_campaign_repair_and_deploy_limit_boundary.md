# Engineering Report: CT-M0F standing validation campaign

Дата: `2026-08-06T19:22:25+07:00`

## Итог

Mission продолжена через существующие Matrix, governed execution, Authority,
audit и Time owners. Standing policy активна, per-sample подтверждение человека
не требуется. Автоматическая production generation доказала wake, fresh
Candidate/Packet/lease, bounded cutover одной certification identity,
verification, exact-once reservation recovery и durable successor.

Mission **не завершена**: последний producer-consumer repair готов в commit
`1b92f9f142821f8b61f63783afed02e0b293fcbb`, но его штатный production deploy
отклонён внешним Codex usage limit. Обход ограничения не выполнялся.

## Authority и scope

- request: `ctm0fsdpauth_r1_0c4ee69155202936f0d8bb06`;
- request hash: `0c4ee69155202936f0d8bb06e1dc3b609fc05c3b24f9082483fb14b044bb6438`;
- active contract: `ctm0fsdpc_208482a67dc4103e5f0ef7b6`;
- contract hash: `208482a67dc4103e5f0ef7b6` owner-backed full hash in production policy/audit;
- contract expiry: `2026-09-05T09:32:42.689887+00:00`;
- bounds: certification-only, `max_users=1`, concurrency `1`, maximum five
  valid and three invalid attempts per implementation fingerprint;
- ordinary users, Authority expansion, Stage 25/48, CT-M8, Natural L8 and
  Production Maturity credit: `NONE`.

## Выполненные repairs

1. `ad8da17b` — disabled prepared source retained from current registry and
   Matrix truth instead of disappearing from active-only pool projection.
2. `c408d108` — owner-declared disabled/maintenance state accepted as the
   controlled condition even when the underlying interface remains reachable.
3. `872477e7` — controlled source reset restores the source and keeps the
   identity on the verified forward target.
4. `ac64375e` — active reservation is closed before new source selection;
   duplicate/restart recovery no longer enters a circular predecessor.
5. `1b92f9f1` — controlled incident identity/generation are derived from the
   existing condition audit record, failure clocks are persisted by the
   condition owner, and target expected IP is read from the canonical nested
   registry projection.

No new owner, queue, registry, watcher, daemon, Runtime, Planner, scheduler,
evidence store or Authority system was created.

## Production evidence

- ordinary Matrix wake: `2026-08-06T11:38:42+00:00`;
- exact certification identity: `10.7.0.107`;
- source: `amneziawg-exec-20260528-10-8-1-14`;
- target: `vless`;
- reservation: `ctm0fsample_1b418940c1726ba599f840ec`;
- generation: `ctm0fgen_964ee8689558ed56ba399552`;
- Packet: `pkt_4fd359f35bb7c80943716a37`;
- operation: `govexec_ddbff9ce49ffd7bced025bb6`;
- lease: `execlease_d69505beedcbac2c123ef582`;
- route apply and verification: `PASS`, identity ended on `vless`;
- automatic closure generation: `2026-08-06T12:09:36+00:00`;
- durable successor:
  `NEXT_ORDINARY_MATRIX_GENERATION_PREPARES_FRESH_SAMPLE`;
- source reset: `enabled=1` through existing `v7-egress-set-state` owner;
- sample credit: `INVALID`, honestly rejected because the pre-repair forward
  evidence lacked `incident_id` and canonical target expected-IP binding.

The invalid historical sample is not reused and grants no CT-M0F terminal.

## Verification

- focused selector/reset/closure tests: PASS;
- affected suites: `355` tests PASS;
- GitHub branch `Updatesystem` was pushed through
  `1b92f9f142821f8b61f63783afed02e0b293fcbb`;
- safe-deploy preflight for `1b92f9f1`: PASS;
- manifest delta: only `tools/v7-users-autoswitch` and
  `tools/v7-governed-canary-dry-run-cycle`;
- production remains at `ac64375e545554e692b494f4585f4584f9b92007`;
- runtime implementation target is
  `1b92f9f142821f8b61f63783afed02e0b293fcbb`; the report-only successor commit
  does not alter that runtime delta;
- final truth/convergence not run because the required production identity is
  not yet aligned.

## Exact blocker and re-entry

Blocker:

`EXTERNAL_CODEX_USAGE_LIMIT_BLOCKED_APPROVED_SAFE_DEPLOY`

Tool result states that usage becomes available after
`2026-08-08T14:11` (product-displayed time). This is not ENGINEERING_AUTHORITY,
OPERATIONAL_AUTHORITY, REAL_WORLD_LIMIT or a V7 program terminal.

Exact re-entry:

1. run `tools/v7-safe-deploy` preflight from branch HEAD containing runtime
   implementation commit `1b92f9f1`;
2. require delta exactly the two runtime files above and no blockers;
3. apply only through `tools/v7-safe-deploy`;
4. verify production non-test selector/evidence caller;
5. let ordinary Matrix generations consume five valid current-fingerprint
   samples (one cold, two warm, at least two generations) without manual wake;
6. consume Time ledger/SLO, reset/deferred closure, Outcome/Replay/Learning;
7. run truth, convergence and local/GitHub/production identity reconciliation;
8. atomically update CPS/OMP only from those owner-backed terminals.

Current legal terminal:

`DEPLOY_REQUIRED_EXTERNAL_USAGE_LIMIT_WITH_DURABLE_CT_M0F_REENTRY`
