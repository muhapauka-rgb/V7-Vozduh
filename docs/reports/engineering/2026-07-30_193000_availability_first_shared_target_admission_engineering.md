# Engineering Report: availability-first shared-target admission

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `BOUNDED_AVAILABILITY_FIRST_CONTROLLED_FAILOVER_AND_PROGRESSIVE_LADDER_V1`  
Scope in this change: read-only availability classification and bounded
technical-capacity projection only.

## Итог

Исправлен конкретный semantic gap существующего shared-target owner: попадание
ниже normal stability floor больше не отождествляется с hard failure и нулевой
технической capacity. Normal production floor не менялся.

Новая compact projection различает:

- `HEALTHY` — normal admission, существующая reserve capacity;
- `DEGRADED_USABLE` — свежие sustained positive measurements при soft quality
  deviation; максимум одна certification identity до реального Outcome;
- `LAST_RESORT_USABLE` — только current positive measurement, также максимум
  одна identity и отдельный exact policy boundary;
- `DEGRADED_OBSERVATION_INSUFFICIENT` — hard failure не доказан, но данных для
  emergency allocation недостаточно;
- `HARD_INELIGIBLE` — source=target, reachability, reserve/capacity,
  verification, containment, freshness либо иной hard owner-backed gate failed.

`DEGRADED_USABLE` и `LAST_RESORT_USABLE` не являются execution admission. Они
не создают Candidate, Packet, lease, restore barrier, policy write, routing,
user movement или Production Maturity effect. Единственный возможный дальнейший
шаг — exact existing standing-policy Authority contract, затем полностью fresh
planner generation.

## Reuse and extension

Использованы существующие Matrix, quality, service reachability,
capacity/reserve, Planner ranking, controlled-topology, policy, verification,
rollback/containment и Polygon contract owners. Не создано новых owners,
registries, queues, schedulers или Runtime paths.

Projection теперь публикует availability-first stages `1`, `2` и все stages
уже существующей campaign. Multi-target allocation использует только
`target_safe_additional_capacity`, а не raw hard limit. Обычные assignments и
routes остаются неизменяемыми, target fault injection запрещён.

## Verification before deploy

- focused unit tests: `test_service_failure_automation_evolution`,
  `test_operator_execution_packet`, `test_omp_live_state_pointer_consistency`;
- syntax compilation: `tools/v7-users-autoswitch`;
- `git diff --check`.

All focused checks passed. Existing legacy `DeprecationWarning` in
`tools/v7_sync_lib.py` remains unrelated.

## Exact next step

Deploy this narrow runtime-owner change through `tools/v7-safe-deploy`, invoke
the production read-only topology diagnostic, and classify the actual target
set. If at least one distinct target is `DEGRADED_USABLE` or
`LAST_RESORT_USABLE`, prepare one exact existing Authority request only. If
none is usable, retain an owner-backed capacity-substrate boundary instead of
repeating diagnosis or manufacturing production evidence.
