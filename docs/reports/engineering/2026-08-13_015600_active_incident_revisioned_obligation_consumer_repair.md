# Отчёт: revision-aware consumption active incident obligation

Дата: 2026-08-13 01:56 MSK  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Родительская Mission: `CT-M0F CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY`

## Результат

`PASS — ACTIVE_INCIDENT_REVISIONED_OBLIGATION_CONSUMER_REPAIRED_AND_PRODUCTION_CONSUMED`.

Исправлена общая причинная связь существующего append-only owner:

`changed current incident scope/classification → new semantic fingerprint → one OMP consumption → CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Новые owner, queue, watcher, timer, registry, policy или Runtime path не созданы.

## Root cause

Producer `tools/v7-users-autoswitch` уже умел дописывать изменившуюся семантику active obligation, но consumer в `tools/v7_sync_lib.py` считал любой исторически потреблённый `automation_obligation_id` окончательно потреблённым. Поэтому новая current projection того же immutable lineage могла не попасть к OMP consumer.

Исправление вводит `automation_consumption_fingerprint` только для новых producer projections. Exact-once теперь действует на semantic revision; historical rows без fingerprint сохраняют прежнюю ID-scoped дедупликацию и не переинтерпретируются после deploy.

## Verification

- Focused tests: `3/3 PASS`, включая changed-scope re-entry и cross-process exact-once.
- Full `tests.unit.test_service_failure_automation_evolution`: `PASS`.
- Deploy manifests: `PASS`; изменялись только `tools/v7_sync_lib.py` и `tools/v7-users-autoswitch`.
- Production deploys: `4f16345c`, затем совместимый migration fix `adc4356e`.
- Production ordinary consumer, без ручного Matrix/autoswitch:
  - obligation `sfaob_3fad990568f118aab69e4ce6`;
  - fingerprint `a0f486aa6043e2bc1c947807d3448add6e629a9843cc260c210d87f42271d014`;
  - source incident `sfinc_ab1dda90210a824d7698c84c822caa2f`;
  - current scope: affected `12`, unresolved `12`, protected `0`;
  - receipt `sfomp_2fe82a0265071da132ee3c8d` at `2026-08-12T22:54:35Z`;
  - successor: `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`; local, GitHub and production runtime all at `adc4356efa4cdfcf86b4b1ef6aea9724fefb97f8`.

## Safety and CT-M0F status

No Candidate, Packet, lease, restore-barrier write, apply, routing mutation, user movement, Authority expansion or Production Maturity change was made by this repair.

The receipt correctly ends at `STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED`; it does **not** constitute a CT-M0F latency sample. The live next consumer must revalidate fresh target health/capacity and the standing policy before it may create fresh execution artifacts. A valid `Time receipt` has not been produced in this repair.

## Exact next frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` through the existing ordinary Matrix/Planner chain:

`fresh Matrix observation → live target/capacity gates → fresh Candidate → Packet → lease → permitted bounded cutover → exact client-context Time receipt`.

If any live gate fails, the existing consumer must emit its predicate-level `STOP_SAFE` with automatic re-entry; it must not fabricate a latency sample or wait for operator continuation.
