# Исправление lineage действующей policy после ротации audit

Дата: 2026-08-02  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Commit/deploy: `7490960c23c031eb052836e4f6ed066c3e46cd1e` / `deploy-z8-14-Updatesystem-7490960-20260802T084943`

## Итог

`RESOLVED_EXISTING_OWNER_CONSUMER_GAP`.

Действующий contract `sdpc_285af5fc6f4de20415c3e5b1` не истёк и не был отозван. После ротации `/opt/v7/audit/operator-execution-audit.jsonl` его единственное Authority decision осталось в существующем `.jsonl.1`. Верхний policy-status уже читал bounded durable lineage и возвращал `ACTIVE`, но вложенный `controlled_source_topology_diagnostic` продолжал читать только active segment. Из-за этого один consumer возвращал `PASS`, а другой ошибочно — `standing_delegated_policy_authority_audit_missing_or_duplicate`.

Исправлен только этот existing producer-to-consumer link: topology diagnostic теперь использует `read_live_execution_lineage_records`, как policy-status и target-selection. Это bounded read-only projection существующего append-only audit: без новой базы, registry, cache, policy write или Authority owner.

## Проверка

- Focused unit suites: `test_service_failure_automation_evolution`, `test_operator_execution_packet`, `test_governed_canary_cli` — PASS.
- `tools/v7-safe-deploy` manifest: allowlist PASS, truth PASS, blockers none.
- Production deploy выполнен только через `tools/v7-safe-deploy`.
- Production non-test consumer:
  - contract status: `ACTIVE`;
  - availability ladder receipts: `[1, 2, 5, 10]`;
  - exact next stage: `25`;
  - topology admission: `AUTO_ADMITTED_BY_STANDING_DELEGATED_AVAILABILITY_FIRST_POLICY`;
  - successor: `EXISTING_MATRIX_PLANNER_CANDIDATE_PACKET_LEASE_CONSUMER`.
- Forbidden effects during repair: policy write, Candidate, Packet, lease, barrier, routing mutation, user movement, rollback, Authority expansion, Production Maturity change — all absent.
- `tools/v7-truth-check --all --json`: PASS.
- Local/GitHub/production commit convergence: `ALIGNED` on `7490960c`.

## Не выданный кредит

Stage 25, Stage 48, campaign closure и ordinary multi-user batch не завершены этим исправлением и не заявляются. Исправление доказало admission/consumer binding, а не controlled-production effect.

## Следующий owner-backed frontier

`AUTO_ADMITTED_BY_STANDING_DELEGATED_AVAILABILITY_FIRST_POLICY:EXISTING_MATRIX_PLANNER_CANDIDATE_PACKET_LEASE_CONSUMER`.

Его вызовет уже включённый штатный `v7-service-matrix-refresh.timer`; на момент проверки следующий wake: `2026-08-02 05:00:49 MSK`. Matrix не запускался вручную и текущий report не является wake source.
