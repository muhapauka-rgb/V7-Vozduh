# Operation-Scoped Controlled Window And Packet Binding

Дата: 2026-07-11T10:48:25+0700
Mission: `V7_OMP_CONTROLLED_WINDOW_AND_PACKET_BINDING_V1`
Режим: repository implementation и read-only certification; production mutation запрещена.

## Summary

Существующие owners расширены без новой архитектуры. Реализован operation-scoped `CLOSED` contract для одного `operation_id`, одного `selected_move_hash` и `max_users=1`; packet/lease identity теперь включает breaker generation, `source_bundle_hash`, fingerprint `source_hashes`, `snapshot_bundle_hash` и user/source/target/action identity. Governed coordinator начинает только из валидного `OPEN`, создаёт свежий bound generation после точной approval binding, повторно валидирует identity после `CLOSED` и перед apply, а единый идемпотентный finalizer возвращает `OPEN` для всех terminal paths и restart recovery.

Финальный verdict: `CONTROLLED_WINDOW_AND_PACKET_BINDING_IMPLEMENTATION_CERTIFIED_READ_ONLY`.

## ECR И Architecture Closed

Прочитаны Kernel, ECR, CPS section 0 и authoritative registry, OMP, Production Maturity, Canonical Reference, SYSTEM_MAP, Runtime/Decision models, backlog и два обязательных source reports. Code-level revalidation подтвердила gap в существующей цепочке Admin Safe Mode -> packet/lease -> pipeline -> governed coordinator -> autoswitch -> low-level switch. Новый owner, Runtime, Planner, Engine, lifecycle, capability, policy, roadmap или truth source не создан.

`ARCHITECTURE_CLOSED_BY_DEFAULT = PASS`
`NEW_OWNER_REQUIRED = NO`

## Existing Owners Reused

| Responsibility | Existing owner |
| --- | --- |
| Safe Mode schema, decision, finalization | `admin_core/operator_execution.py` |
| Authenticated Admin writer | `admin/v7-admin-api` |
| Source/snapshot envelope producer and packet preview | `admin_core/operator_execution_pipeline.py` |
| One-operation coordination and terminal cleanup | `tools/v7-governed-canary-dry-run-cycle` |
| Final pre-mutation revalidation | `tools/v7-users-autoswitch` |
| Last low-level route mutation gate | `tools/runtime-support/v7-user-switch` |
| Volatile continuation state | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |

## Baseline И Gap-To-Code Mapping

Baseline: production Safe Mode v2 `OPEN`; autoswitch service/timer inactive; no admitted packet, lease, restore barrier or Authority. Найденные Phase 4A gaps закрыты так:

1. Empty `source_hashes`: synthetic fallback удалён; pipeline публикует hashes реальных registry/runtime/snapshot inputs; strict packet отказывает при пустом наборе.
2. Empty `snapshot_bundle_hash`: pipeline materializes non-empty bundle fingerprint; strict packet отказывает при пустом значении.
3. Global controlled window: forward-capable window имеет `scope=operation` и exact identity.
4. Missing mandatory final OPEN: один finalizer используется normal terminal, exception, cancellation, expiry и restart recovery paths.
5. Missing post-CLOSED revalidation: exact decision выполняется после generation creation, после packet materialization, перед autoswitch apply, для каждого item и в low-level primitive.

## Schema И Identity

`v7.autonomous-execution-control.v2` сохранён. `OPEN` остаётся global и обратно совместимым. Новый forward-capable `CLOSED` требует `operation_id`, `selected_move_hash`, `action_class`, `source_bundle_hash`, `snapshot_bundle_hash`, `max_users=1`, fresh generation и TTL. Legacy global state не получает новые bindings; governed controlled run его не использует, а low-level forward primitive не принимает неполный context.

Strict governed packet отмечается существующим execution metadata marker. Его immutable identity и lease material state включают source/snapshot fingerprints и breaker generation. Missing, stale, malformed, substituted или mismatched binding даёт `STOP_SAFE`; re-materialization после `CLOSED` обязательна.

## Controlled Window Coverage

| Entry/Terminal Path | Binding Checked | Mutation Allowed | Final OPEN Guaranteed | Evidence | Result |
| --- | --- | --- | --- | --- | --- |
| Fresh governed entry | operation/move/source/snapshot/max-users | только exact match | да | governed + operator tests | PASS |
| Deny/stale/generation/source/snapshot mismatch | exact decision/packet gate | нет | да | terminal matrix test | PASS |
| Success/verification/rollback/partial/subprocess failure | pre-mutation + per-item | bounded exact operation | да | common finalizer tests | PASS |
| Exception/cancellation/timeout | owned generation | нет или один начатый bounded attempt | да | wrapper/finalizer tests | PASS |
| Expired window/restart recovery/malformed state | fail-closed recovery | нет | да, fresh rerun required | expiry/restart tests | PASS |

## Packet Identity Coverage

| Field | Material Identity | Fingerprint | Post-CLOSED Revalidated | Mismatch Result |
| --- | --- | --- | --- | --- |
| packet/decision/operation IDs | YES | YES | YES | STOP_SAFE |
| selected move/user/source/target/action class | YES | YES | YES | STOP_SAFE |
| breaker generation | YES | YES | YES | STOP_SAFE |
| source hashes/source bundle | YES | YES | YES | STOP_SAFE |
| snapshot bundle | YES | YES | YES | STOP_SAFE |
| max users | YES (`1`) | YES | YES | STOP_SAFE |
| rollback target/verification plan | existing approved lock/envelope | YES | existing gates | STOP_SAFE |

## Mutation Entry Coverage

| Entry Point | Final Gate | Generation | Operation | Move Hash | Source/Snapshot | Fail-Closed | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Governed coordinator | control decision | bound | bound | bound | bound | YES | PASS |
| Autoswitch entry | control + envelope | bound | bound | bound | bound | YES | PASS |
| Autoswitch per item | control reread | bound | bound | bound | bound | YES | PASS |
| Low-level `v7-user-switch` | CLI validator immediately before route replace | bound | bound | bound | bound | YES | PASS |

## Cleanup/Finalization Coverage

| Terminal State | Cleanup Owner | Idempotent | OPEN Result | Audit Evidence | Result |
| --- | --- | --- | --- | --- | --- |
| success / deny / stale / mismatch | `operator_execution` finalizer | YES | OPEN | structured transaction result + tests | PASS |
| timeout / subprocess / internal exception / cancellation | тот же owner | YES | OPEN | structured result + tests | PASS |
| verification failure / rollback success/failure / partial failure | тот же owner | YES | OPEN | structured result + tests | PASS |
| expiry / process restart / malformed stale state | тот же fail-closed recovery path | YES | OPEN | recovery result + tests | PASS |

## Verification

- Targeted packet/pipeline/governed/autoswitch/Admin-contract/low-level suites: `281 tests`, PASS.
- Full unittest discovery after final changes: `752 tests`, PASS. Предварительный прогон ранее дал один unrelated Telegram Sentinel lock timing error; isolated rerun `7/7` PASS, финальный полный прогон чистый.
- Python compileall: PASS.
- Shell syntax (`v7-user-switch`): PASS.
- Import smoke: PASS.
- `git diff --check`: PASS.
- Safe-deploy allowlist dry-run: allowlist `PASS`; apply не запускался. Общий dry-run закономерно `NO-GO` из-за dirty implementation worktree и недоступной GitHub remote проверки до commit/push; production delta только отображён.

## No-Mutation Proof

`PRODUCTION_DEPLOYED = NO`. Не создавались production packet/lease, restore barrier или Authority. Safe Mode не изменялся, Runtime apply/rollback не выполнялся, users moved `0`, service/timer не включались и не перезапускались. Все mutation tests использовали temporary fixtures или mocks.

## Required Reviews

- Behavior Enforcement: exact bindings enforced in every governed forward entry; no silent widening.
- State Transition Verification: `OPEN -> bound CLOSED generation -> terminal OPEN`; restart recovery требует fresh rerun.
- Production Scale First: `max_users=1`; blast radius не расширен.
- Work Placement: heavy hashing выполняется coordinator/pipeline до mutation; low-level path остаётся thin validator.
- Latency/Runtime Cost: final path добавляет короткие JSON reads и scalar/hash comparisons; broad audit/recomputation отсутствует.
- Production Maturity: `NO_CHANGE`; production evidence не создавалось.

## CPS / OMP

CPS authoritative registry обновлён: active WIP остаётся первым; repository implementation certified; stop = `CONTROLLED_WINDOW_NOT_DEPLOYED_OR_PRODUCTION_CERTIFIED`; Authority required now = `NO`; next action = separate safe deploy and production certification Mission. OMP = `NO_CHANGE`, scheduler/optimizer semantics не менялись.

## Engineering Intent Closure

Точный repository implementation intent закрыт: source/snapshot обязательны, post-CLOSED revalidation существует, все governed mutation entries fail-closed, terminal/recovery paths используют mandatory OPEN, production behavior в Mission не менялось.

`ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED`

Re-audit rule: при изменении Safe Mode schema, packet identity, governed coordinator, autoswitch mutation gates, low-level switch context или finalizer повторить весь targeted matrix и full regression до deploy.

## Final

```text
FINAL_VERDICT = CONTROLLED_WINDOW_AND_PACKET_BINDING_IMPLEMENTATION_CERTIFIED_READ_ONLY
ARCHITECTURE_CLOSED_BY_DEFAULT = PASS
NEW_OWNER_REQUIRED = NO
CONTROLLED_WINDOW_IMPLEMENTED = PASS
PACKET_SOURCE_BINDING = PASS
SNAPSHOT_BUNDLE_BINDING = PASS
POST_CLOSED_REVALIDATION = PASS
ALL_TERMINAL_PATHS_FINAL_OPEN = PASS
MUTATION_ENTRY_COVERAGE = PASS
TESTS = PASS
PRODUCTION_DEPLOYED = NO
SAFE_MODE_FINAL_STATE = OPEN
RUNTIME_APPLY = NO
USER_MOVEMENT = NO
AUTHORITY_CHANGE = NO
PRODUCTION_MATURITY_DECISION = NO_CHANGE
ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED
NEXT_OMP_ACTION = RUN_SEPARATE_SAFE_DEPLOY_AND_PRODUCTION_CERTIFICATION_MISSION
```
