# Safe Deploy и Production Certification operation-scoped controlled window

Дата: `2026-07-11T11:18:40+0700`
Mission ID: `V7_OMP_CONTROLLED_WINDOW_PRODUCTION_CERTIFICATION_V1`
Режим: safe deploy, read-only production certification, без controlled execution
Final Verdict: `CONTROLLED_WINDOW_PRODUCTION_CERTIFIED_OPEN`

## 1. Summary

Сертифицированная operation-scoped controlled-window implementation доставлена в production существующим `v7-safe-deploy`. Production identity, bindings, повторные gate checks, terminal finalization и отсутствие обходного user-routing path подтверждены. Live Safe Mode не изменялся и остался `OPEN`. Packet/lease/barrier не создавались, apply/rollback не выполнялись, пользователь не перемещался.

## 2. ECR и архитектурная граница

Прочитаны обязательные владельцы: Kernel, ECR, CPS section 0 и authoritative registry, OMP, Production Maturity, Canonical Reference, SYSTEM_MAP, Runtime Model, Decision Model, backlog/mission registry, Phase 4A preparation report, unfinished-capability reconciliation report и repository implementation report.

```text
ARCHITECTURE_CLOSED_BY_DEFAULT = PASS
NEW_OWNER_REQUIRED = NO
NEW_BACKLOG_ITEM_REQUIRED = NO
ARCHITECTURE_EXTENSION = NO
OMP_CHANGE = NO_CHANGE
```

Переиспользованы существующие owners: safe commit/push/deploy, truth/convergence, Admin Safe Mode v2, packet/lease, governed coordinator, autoswitch, low-level switch, verification/finalization и CPS.

## 3. Repository revalidation

Исходный implementation commit: `5f8c1419`. При повторной сертификации найден только formatting defect в предыдущем report; он исправлен commit `3604847c1ad2c634a5538114c948820f802e7213` без изменения semantics. Safe-deploy dry run затем выявил evidence defect: Admin restart планировался, но `release_manifest.service_restart_required` оставался false. Существующий deploy owner минимально исправлен и покрыт тестами commit `99b40f2802c68ce7b48c0c9262a10de91b64ef2b` (`fix: align deploy restart manifest`). Нового deploy path не создано.

Сертификация:

| Проверка | Результат |
| --- | --- |
| Implementation targeted suites | `281 PASS` |
| Targeted suites с deploy-owner regression | `305 PASS` |
| Full unittest discovery | `752 PASS` |
| Python compile/import | `PASS` |
| Shell syntax | `PASS` |
| `git diff --check` | `PASS` |
| Safe-deploy allowlist | `PASS` |
| Runtime apply / user movement | `NO` |

## 4. Certified scope

Deploy delta содержал ровно шесть сертифицированных artifacts:

| Artifact | Repository SHA-256 | Production SHA-256 | Match | Owner |
| --- | --- | --- | --- | --- |
| `tools/v7-users-autoswitch` | `0de1be1c20ef042b8907dfc639affcab95a3d837ab0303332ae2e02acdc14661` | same | `PASS` | autoswitch owner |
| `tools/runtime-support/v7-user-switch` | `eb9f24d3f9ca044dc8291c37a1ddb48647c9ff641cd905a3b4a933c8cb4b7667` | same | `PASS` | low-level user-switch owner |
| `admin/v7-admin-api` | `d06389325c57a1782218727693ae8afca5a81d140b8d610000fd2a8d6d7dcbe7` | same | `PASS` | Admin owner |
| `tools/v7-governed-canary-dry-run-cycle` | `0733f2bc27ee1d94ef86e3ba9a0060ff8ca1e07462e4e9a027478b091eb8d4c8` | same | `PASS` | governed coordinator |
| `admin_core/operator_execution.py` | `b0006cf66b906c84aa107048d3f6684a48a62dbf6e49bb26e5c7009cce7fb7b3` | same | `PASS` | packet/lease/control owner |
| `admin_core/operator_execution_pipeline.py` | `f1239d13410e54323cc6ef3318d2341072ef1b53f1a74eaf30f0b3a5fe9b1b9b` | same | `PASS` | execution pipeline owner |

## 5. Commit, push и deploy

| Evidence | Результат |
| --- | --- |
| Branch | `Updatesystem` |
| Deployed commit | `99b40f2802c68ce7b48c0c9262a10de91b64ef2b` |
| Local/GitHub before deploy | aligned |
| Safe deploy dry run | `PASS`, exact six-artifact delta |
| Deploy confirmation owner | existing `v7-safe-deploy` |
| Deploy ID | `deploy-z8-14-Updatesystem-99b40f2-20260711T111335` |
| Service restart | Admin only, manifest says required |
| Backup/rollback path | present |
| Repeated dry run | `PASS`, `deployment_required=false` |

Manual copy, manual production edit и SSH mutation bypass не использовались.

## 6. Truth и convergence

После deploy:

```text
TRUTH = PASS
CONVERGENCE = PASS
STATUS = ALIGNED
LOCAL_COMMIT = 99b40f2802c68ce7b48c0c9262a10de91b64ef2b
GITHUB_COMMIT = 99b40f2802c68ce7b48c0c9262a10de91b64ef2b
PRODUCTION_COMMIT = 99b40f2802c68ce7b48c0c9262a10de91b64ef2b
DEPLOY_DELTA_MISMATCHES = NONE
```

Один sandboxed read-only вызов временно вернул `github_remote_unreadable`; повторная проверка существующим owner с сетевым доступом дала `PASS/ALIGNED`. Это не repository drift.

## 7. Safe Mode и production posture

| Поле | До deploy | После deploy |
| --- | --- | --- |
| Schema | `v7.autonomous-execution-control.v2` | same |
| State | `OPEN` | `OPEN` |
| Scope | `global` | `global` |
| Generation | `aec_a78732b833c8df6b509432b1` | same |
| Permissions | `0600` | `0600` |
| Admin service | active | active |
| Autoswitch service | inactive | inactive |
| Autoswitch timer | inactive | inactive |
| Users registry SHA-256 | `c819588d8ea0c71df486fd957f9ee15f913bb2e8c6d0bf60e4984ca570fbc14f` | same |

Existing lease имеет terminal status `EXECUTION_FINISHED`; существующий restore barrier исторический и expired (`expires_at=2000-01-01T00:00:00+00:00`). Активной operation/lease/barrier нет.

## 8. Packet identity contract

| Field | Required | Non-empty | Fingerprinted | Post-CLOSED revalidated | Mismatch STOP_SAFE |
| --- | --- | --- | --- | --- | --- |
| packet id | YES | YES | YES | YES | YES |
| decision id | YES | YES | YES | YES | YES |
| operation id | YES | YES | YES | YES | YES |
| selected move hash | YES | YES | YES | YES | YES |
| user/source/target | YES | YES | YES | YES | YES |
| action class | YES | YES | YES | YES | YES |
| breaker generation | YES | YES | YES | YES | YES |
| source hashes / bundle | YES | YES | YES | YES | YES |
| snapshot bundle hash | YES | YES | YES | YES | YES |
| max users | YES | `1` | YES | YES | YES |
| rollback target | YES | YES | YES | YES | YES |
| verification plan | YES | YES | YES | YES | YES |

## 9. Production controlled-window certification

Certification выполнялась deployed code на isolated temporary state root. Live Safe Mode не записывался.

| Condition | Production code supports | Evidence | Result |
| --- | --- | --- | --- |
| Initial live `OPEN` | YES | read-only live state | PASS |
| Operation scope and exact operation id | YES | isolated validator | PASS |
| Exact selected move hash | YES | isolated mismatch matrix | PASS |
| `max_users=1` | YES | isolated mismatch matrix | PASS |
| Generation and TTL | YES | state parser/decision | PASS |
| Second/different operation denied | YES | isolated mismatch matrix | PASS |
| Source/snapshot mismatch denied | YES | isolated mismatch matrix | PASS |
| Final `OPEN` | YES | 16 terminal classes | PASS |
| Idempotent finalization | YES | repository tests | PASS |
| Malformed restart recovery | YES | isolated deployed-code validator | PASS |

Isolated result: exact binding allowed; mismatch denied for operation, move, action class, source, snapshot and max users; `16/16` terminal classes final `OPEN`; malformed recovery final `OPEN`.

## 10. Mutation-entry coverage

| Entry point | Generation | Operation | Move | Source/Snapshot | Live reread | Fail-closed |
| --- | --- | --- | --- | --- | --- | --- |
| governed coordinator preflight/pre-apply | YES | YES | YES | YES | YES | YES |
| autoswitch apply entry | YES | YES | YES | YES | YES | YES |
| per-item `_run_switch` | YES | YES | YES | YES | YES | YES |
| rollback/compensation entry | YES | YES | N/A for certified rollback | rollback-certified | YES | YES |
| low-level `v7-user-switch` before `ip route replace` | YES | YES | YES | YES | YES | YES |
| Admin guarded autoswitch | delegated | delegated | delegated | delegated | YES | YES |
| systemd/timer | governed coordinator only | delegated | delegated | delegated | YES | YES |

## 11. Terminal finalization

Единый finalizer owner: `finalize_autonomous_execution_control_window`.

| Terminal paths | OPEN guaranteed | Idempotent/recovery evidence | Result |
| --- | --- | --- | --- |
| success, deny, stale, generation/source/snapshot mismatch | YES | deployed isolated test | PASS |
| timeout, verification failure, partial/subprocess/internal failure | YES | deployed isolated test | PASS |
| rollback success/failure, cancellation | YES | deployed isolated test | PASS |
| expiry, restart recovery, malformed state | YES | deployed isolated test | PASS |

## 12. Bypass audit

Поиск реальных callers показал: единственный executable caller low-level `v7-user-switch` для user route movement — `v7-users-autoswitch`; preview tools только печатают команду. Admin и Telegram sentinel делегируют autoswitch, systemd unit делегирует governed coordinator. Autoswitch делает live decision перед каждым item; low-level primitive независимо требует все bindings и повторно вызывает control validator непосредственно перед `ip route replace` и registry write. Manual egress/config maintenance commands принадлежат отдельным explicit operator owners и не являются controlled-run user-movement обходом.

`BYPASS_AUDIT = NO_BYPASS_FOUND`.

## 13. No-action proof

```text
PRODUCTION_PACKET_CREATED = NO
PRODUCTION_LEASE_CREATED = NO
RESTORE_BARRIER_WRITTEN = NO
SAFE_MODE_TRANSITION = NO
RUNTIME_APPLY = NO
ROLLBACK_APPLY = NO
USER_MOVEMENT = NO
AUTHORITY_CHANGE = NO
BLAST_RADIUS_CHANGE = NO
AUTOSWITCH_SERVICE_OR_TIMER_ENABLED = NO
```

Users registry hash, Safe Mode generation/state и terminal historical lease/barrier facts остались неизменными.

## 14. Behavior Enforcement и State Transition

Behavior chain закрыта для deployment/safety certification: repository output -> safe deploy -> matching production hashes -> deployed isolated validation -> truth/convergence -> CPS/OMP next step. Runtime action не исполнялся и не требовался.

State transition:

```text
repository implementation certified
-> canonical branch pushed
-> exact artifacts deployed
-> production identity and safety contract certified
-> Safe Mode remains OPEN
-> Phase 4A fresh rerun ready
```

Legal terminal consumer: `OMP Next Step Produced` через authoritative CPS registry.

## 15. Work placement, cost и scale

Проверки выполнены существующими repository, deploy, truth, Runtime и execution owners. Runtime hot path не расширен. Дополнительная production certification использовала read-only hashes и isolated temporary fixtures; live routing cost равен нулю. Production Scale First сохранён: exact one-operation and one-user bounds проверяются до и непосредственно перед mutation.

## 16. Production Maturity

Decision: `ACCEPT` только для deployment/safety certification evidence. Это не controlled-run outcome, не Authority и не Autonomy promotion. Score вручную не изменялся.

## 17. CPS и OMP

CPS section 0 и authoritative unfinished-capability registry обновлены:

```text
CURRENT_MODE = CONTROLLED_WINDOW_PRODUCTION_CERTIFIED_OPEN
CURRENT_PRIMARY_STOP = NONE_FOR_PHASE_4A_RERUN_PREPARATION
CURRENT_ACTIVE_SCOPE = FIRST_GOVERNED_CONTROLLED_RUN_PHASE_4A_RERUN
CURRENT_SAFE_NEXT_ACTION = RERUN_FIRST_GOVERNED_OMP_CONTROLLED_RUN_PHASE_4A_FROM_FRESH_EVIDENCE
CONTROLLED_RUN_EXECUTION_AUTHORIZED = NO
AUTHORITY_REQUIRED_NOW = NO
SAFE_MODE = OPEN
```

Active WIP остаётся первым. Parent Engineering Intent остаётся `INTENT_NOT_CLOSED` до реального governed execution/outcome closure. OMP scheduler semantics не изменились: `OMP_CHANGE = NO_CHANGE`.

## 18. Engineering Intent Closure и re-audit

Mission intent закрыт: exact artifacts deployed, identity/alignment/hashes подтверждены, fail-closed contract production-certified, bypass не найден, final state `OPEN`, production action отсутствовал, CPS продвинут к fresh Phase 4A rerun.

`ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED`.

Re-audit required при изменении любого из шести artifacts, Safe Mode schema/generation semantics, packet identity contract, mutation entry, finalizer, deploy owner, runtime fingerprint или CPS active Mission state.

## 19. Final flags

```text
ARCHITECTURE_CLOSED_BY_DEFAULT = PASS
NEW_OWNER_REQUIRED = NO
REPOSITORY_CERTIFICATION = PASS
SAFE_COMMIT = PASS
SAFE_PUSH = PASS
SAFE_DEPLOY_DRY_RUN = PASS
DEPLOY_APPLIED = YES
DEPLOY_ID = deploy-z8-14-Updatesystem-99b40f2-20260711T111335
TRUTH = PASS
CONVERGENCE = PASS
PRODUCTION_HASHES = PASS
PACKET_SOURCE_BINDING_PRODUCTION = PASS
SNAPSHOT_BUNDLE_BINDING_PRODUCTION = PASS
OPERATION_SCOPED_WINDOW_PRODUCTION = PASS
POST_CLOSED_REVALIDATION_PRODUCTION = PASS
ALL_TERMINAL_PATHS_FINAL_OPEN_PRODUCTION = PASS
MUTATION_ENTRY_COVERAGE_PRODUCTION = PASS
BYPASS_AUDIT = PASS
SAFE_MODE_FINAL_STATE = OPEN
AUTOSWITCH_SERVICE_ACTIVE = NO
AUTOSWITCH_TIMER_ACTIVE = NO
PRODUCTION_PACKET_CREATED = NO
PRODUCTION_LEASE_CREATED = NO
RESTORE_BARRIER_WRITTEN = NO
RUNTIME_APPLY = NO
ROLLBACK_APPLY = NO
USER_MOVEMENT = NO
AUTHORITY_CHANGE = NO
BLAST_RADIUS_CHANGE = NO
PRODUCTION_MATURITY_DECISION = ACCEPT
ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED
NEXT_OMP_ACTION = RERUN_FIRST_GOVERNED_OMP_CONTROLLED_RUN_PHASE_4A_FROM_FRESH_EVIDENCE
FINAL_VERDICT = CONTROLLED_WINDOW_PRODUCTION_CERTIFIED_OPEN
```
