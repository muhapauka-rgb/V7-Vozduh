# Autonomous User Movement System Audit

Дата: 2026-06-30 22:20:33 +07
Статус: READ-ONLY AUDIT
Вердикт: AUTONOMOUS_MOVEMENT_SYSTEM_PARTIAL

## Summary

Аудит проверил весь существующий контур перемещения пользователей: производители сигналов, read-models, planner, authority, eligibility, apply, verification, rollback, learning, evidence, OMP и следующий runtime cycle.

Главный ответ: если пользователь должен быть автоматически перемещен, не каждый существующий production path сегодня может реально довести пользователя до движения без оператора.

Система частично материализована:

- сигналы и evidence в production живые;
- service matrix refresh, Telegram sentinel, quality compact и planner refresh работают;
- основной исполнитель движения существует: `tools/v7-users-autoswitch`;
- фактический apply path существует через `v7-user-switch`;
- verification, rollback, terminal classification, learning и closure существуют;
- L3 код deployed и validated;
- но autonomous movement не active/certified;
- old broad autoswitch timer intentionally inactive;
- service failure evidence не материализуется как активный L3 wake consumer path;
- production state прямо блокирует runtime apply, automation, authority expansion и user movement.

Итог: это не отсутствие planner/executor. Это незамкнутая autonomous production цепочка.

## Semantic Duplicate Audit

Перед предложением исправлений проверены существующие смысловые аналоги.

| Responsibility | Existing owner | Status | Duplicate needed |
| --- | --- | --- | --- |
| Planner / selected moves | `tools/v7-users-autoswitch` | EXISTS_COMPLETE | NO |
| User movement apply | `tools/v7-users-autoswitch::_run_switch` -> `v7-user-switch` | EXISTS_COMPLETE | NO |
| Governed operator approval | `admin_core/operator_execution.py` | EXISTS_COMPLETE | NO |
| Execution feedback / terminal classification | `admin_core/operator_execution_feedback.py` | EXISTS_COMPLETE | NO |
| Event shaping/read-only consumer trace | `admin_core/events.py` | EXISTS_PARTIAL | NO |
| Service regression producer | `tools/v7-service-matrix-refresh-all`, `tools/v7-telegram-sentinel` | EXISTS_COMPLETE as producers | NO |
| Quality/degradation producer | `tools/v7-egress-quality-compact` | EXISTS_COMPLETE as producer | NO |
| L3 wake consumer | `tools/v7-users-autoswitch::_l3_wake_decision` | EXISTS_PARTIAL | NO |
| L3 authority gate | `tools/v7-users-autoswitch::_emergency_failover_authority_gate` | EXISTS_PARTIAL | NO |
| Runtime eligibility before apply | `tools/v7-users-autoswitch::_l3_execution_eligibility` and apply gate | EXISTS_PARTIAL/IMPLEMENTED | NO |
| Old timer apply loop | `systemd/v7-users-autoswitch.timer` | EXISTS but intentionally rejected | NO |

Conclusion: no new Runtime, Planner, service, timer, watcher, owner, policy, or architecture is needed. Reuse and extension of existing owners is sufficient.

## Production Liveness Snapshot

Read-only live SSH audit confirmed:

| Unit | Active | Enabled | Meaning |
| --- | --- | --- | --- |
| `v7-users-autoswitch.service` | inactive | static | oneshot executor, not a daemon |
| `v7-users-autoswitch.timer` | inactive | enabled | old broad apply timer, last triggered more than one month ago |
| `v7-autoswitch-planner.timer` | active | enabled | planner/read-model refresh is alive |
| `v7-service-matrix-refresh.timer` | active | enabled | service evidence refresh is alive |
| `v7-telegram-sentinel.timer` | active | enabled | fast service regression sentinel is alive |
| `v7-egress-quality-compact.timer` | active | enabled | quality compaction is alive |
| `v7-admin-api.service` | active | enabled | operator/admin surface is alive |

Wake event files:

| File | State |
| --- | --- |
| `/opt/v7/events/l3-wake-events.jsonl` | missing |
| `/opt/v7/events/service-failure-events.jsonl` | missing |
| `/opt/v7/events/runtime-wake-events.jsonl` | missing |
| `/opt/v7/events/service-matrix-refresh-20260630.jsonl` | exists, active evidence stream |

L3 capability state:

| Field | Value |
| --- | --- |
| implemented | true |
| validated | true |
| production_proven | false |
| certified | false |
| active_capability | false |
| success_outcomes | 0 |
| rollback_outcomes | 0 |
| failure_or_no_execution_outcomes | 163 |

## Complete Movement Trigger Inventory

| Trigger | Producer | Existing consumer | Movement path | Current state |
| --- | --- | --- | --- | --- |
| Service failure | `v7-service-matrix-refresh-all`, `v7-telegram-sentinel` | Planner/read-only views; partial L3 wake inference | L3 should consume once authority/certification active | PARTIAL/SLEEPING |
| Required service failure | Service matrix + user service requirements | `tools/v7-users-autoswitch` candidate scoring | Failover candidate can be produced | PARTIAL/SLEEPING |
| Current channel failed | Service matrix / planner evidence | L3 incident/wake logic in autoswitch | Emergency failover path exists but not active | PARTIAL/SLEEPING |
| Channel degradation | `v7-egress-quality-compact`, quality summaries | Planner/read-only suitability | Planned/degradation movement remains governed/read-only | PARTIAL |
| Channel quarantine | Egress safety/quarantine state | Planner gates | Blocks bad targets; can produce failover/keep decisions | PARTIAL |
| Channel disabled/maintenance/removed | Egress registry/state gates | Planner candidate gates | Can block current/target suitability; autonomous movement still blocked by authority | PARTIAL |
| Planner proposal | `tools/v7-users-autoswitch` | Operator UI / governed packet / dry-run | Can become governed transaction with approval | MANUAL/GOVERNED |
| Capacity overflow/load | Dynamic load/capacity policy in autoswitch | Planner rebalance logic | Rebalance candidates exist; autonomous apply not certified | PARTIAL |
| Restore/recovery | Restore/recovery admission owners | Read-only gates / restore barrier | Runtime apply blocked without authority | PARTIAL |
| Verification failure | `tools/v7-users-autoswitch` verification | Rollback path in same owner | Rollback can run after authorized apply | EXISTS but only after execution |
| Rollback | Autoswitch rollback packet/execution owner | Feedback/learning/closure | Exists, but not autonomous broad production rollback | GOVERNED/PARTIAL |
| Manual approval | Operator + `admin_core/operator_execution.py` | Restore barrier + autoswitch apply when separately approved | Can move users | EXECUTABLE_MANUAL |
| Future autonomous authority / L3 | L3 capability + autoswitch emergency policy | L3 gate in autoswitch | Not active/certified | SLEEPING |
| Reconnect rotation | Reconnect state + autoswitch planner | Autoswitch selected moves | Movement needs apply authority | PARTIAL |
| Planned optimization | Autoswitch planner | Operator surface / dry-run | Default read-only; apply requires approval | MANUAL/GOVERNED |
| Rebalance | Autoswitch load policy | Autoswitch selected moves | Automation not certified | PARTIAL |

## Autonomy Matrix

| Trigger | Producer | Consumer | Wake | Incident | Planner | Authority | Execution | Verification | Rollback | Learning | Current State | Root Cause |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Service failure | Active service timers | Read-only matrix/planner | Missing active L3 wake file/consumption | Partial | Present | Disabled/not certified | Not reached | Not reached | Not reached | No new outcome | Sleeping | RC1 + RC2 |
| Required service failure | Service matrix | Planner candidate scoring | Partial inferred wake only | Partial | Present | Disabled/not certified | Not reached | Not reached | Not reached | No new outcome | Sleeping | RC1 + RC2 |
| Current channel failed | Service evidence | L3/autoswitch | Partial | Partial | Present | Disabled/not certified | Not reached | Not reached | Not reached | No new outcome | Sleeping | RC1 + RC2 |
| Channel degradation | Quality compact | Planner/read-only UI | No certified autonomous wake | No | Present | Disabled/not certified | Not reached | Not reached | Not reached | Read-only only | Partial | RC1 |
| Quarantine/disabled/removed | Registry/safety state | Planner gates | No autonomous wake | No | Present | Disabled/not certified | Not reached | Not reached | Not reached | Read-only only | Partial | RC1 |
| Capacity overflow | Load/capacity policy | Planner rebalance | No autonomous wake | No | Present | Disabled/not certified | Not reached | Not reached | Not reached | Read-only only | Partial | RC1 |
| Planner proposal | Autoswitch planner | Operator UI / packet owner | N/A | N/A | Present | Operator required | Can execute only with approved apply | Present | Present | Present | Manual/governed | RC3 |
| Verification failure | Verification owner | Rollback owner | N/A | N/A | N/A | Existing execution authority required | Already after apply | Present | Present | Present | Exists after governed execution | RC3 |
| Rollback | Rollback packet/operation | Autoswitch rollback executor | N/A | N/A | N/A | Explicit/separate authority | Can execute only when authorized | Present | Present | Present | Governed/partial | RC3 |
| L3 autonomous failover | L3 capability | Autoswitch emergency policy | Partial | Partial | Present | Not active/certified | Not reached in production | Not reached | Not reached | No production proof | Sleeping | RC1 + RC2 |
| Old autoswitch timer | systemd timer | Autoswitch service | Timer rejected | None | Present | Broad apply not approved | Inactive by design | Would exist if enabled | Would exist | Would exist | Intentionally inactive | RC4 |

## Chain Closure Findings

### Producer -> Consumer

PASS for read-only evidence and planner refresh:

- service matrix refresh produces service evidence;
- Telegram sentinel produces service regression evidence and currently runs with `--no-autoswitch`;
- quality compact produces channel quality evidence;
- planner refresh consumes read-models and produces plans/selected moves.

PARTIAL for autonomous execution:

- service failure evidence is not currently materialized as an active L3 wake stream consumed by production L3;
- L3 wake files are absent;
- L3 state is validated but not certified/active.

### Consumer -> Behavior Changed

PASS for read-only behavior:

- planner/read models change;
- operator surfaces can show decisions;
- selected moves can be produced.

FAIL for autonomous movement behavior:

- no production autonomous user movement occurs;
- no autonomous incident reaches apply;
- no new L3 success/rollback outcome increments production proof.

### Execution -> Verification -> Rollback -> Learning

EXISTS for governed/manual apply:

- `tools/v7-users-autoswitch` calls `v7-user-switch`;
- verification runs after apply;
- rollback can run after verification failure;
- terminal classification preserves success/rollback/failure semantics;
- feedback/learning owners exist.

NOT REACHED autonomously:

- autonomous L3 never reaches apply in current production state.

## Dead / Sleeping / Unreachable Branches

| Branch | Classification | Reason |
| --- | --- | --- |
| Old `v7-users-autoswitch.timer` broad apply | Sleeping intentionally | Timer-only movement is rejected by canonical model. |
| L3 autonomous execution | Sleeping/partial | Capability not certified/active; wake stream not active. |
| Service failure -> L3 autonomous movement | Broken at autonomous consumption | Service evidence exists, but no active L3 wake consumed in production. |
| Planner proposal -> user movement | Manual/governed only | Stops at authority unless explicit operator/governed execution exists. |
| Rollback autonomous path | Partial/governed | Rollback exists after authorized apply, not broad autonomous rollback authority. |
| Event consumer read-only trace | Read-model only | Explicitly `execution_allowed_now=false`, `apply_executed=false`. |

## Root Cause Reduction

### RC1: AUTONOMOUS_AUTHORITY_AND_CERTIFICATION_NOT_ACTIVE

Symptom:

- no production path can autonomously apply movement;
- L3 `production_proven=false`, `certified=false`, `active_capability=false`;
- Current Program State blocks Runtime Apply, Automation, Authority, User Movement.

Responsible owner:

- OMP / Current Program State;
- Policy 004 Authority;
- L3 capability certification;
- `tools/v7-users-autoswitch` emergency failover gate.

Minimal executable fix:

- Continue existing L3 production certification path until `production_proven`, `certified`, and `active_capability` become true through existing owners only.

### RC2: SERVICE_FAILURE_TO_L3_WAKE_CONSUMPTION_GAP

Symptom:

- production has service failure evidence streams;
- L3 wake event files are missing;
- service matrix refresh evidence exists but is not consumed as an active L3 wake that opens an executable incident.

Responsible owner:

- event producers: `tools/v7-service-matrix-refresh-all`, `tools/v7-telegram-sentinel`, `tools/v7-egress-quality-compact`;
- wake/incident consumer: `tools/v7-users-autoswitch`;
- canonical event-driven autonomy contract in SYSTEM_MAP / Canonical Reference.

Minimal executable fix:

- Materialize existing service/current-channel failure evidence into the existing L3 wake consumer path, without creating a new wake framework, after authority/certification rules allow mutation.

### RC3: GOVERNED_PATH_REQUIRES_OPERATOR_AUTHORITY

Symptom:

- governed packet / transaction path can move users, but only after explicit operator authority;
- it is not autonomous.

Responsible owner:

- `admin_core/operator_execution.py`;
- `tools/v7-users-autoswitch`;
- OMP authority boundary.

Minimal executable fix:

- No bug fix required. Packet/governed flow remains manual until action-class or delegated authority is certified.

### RC4: OLD_TIMER_APPLY_LOOP_INTENTIONALLY_REJECTED

Symptom:

- `v7-users-autoswitch.timer` inactive.

Responsible owner:

- SYSTEM_MAP Runtime Timers / Periodic Checks;
- V7 Canonical Reference POOL_AUTONOMY_RUNTIME_RULES;
- OMP Engineering Authority stop gates.

Minimal executable fix:

- None. Do not enable old broad autoswitch timer. Event-driven L3 path must be used instead.

## Priority Order

1. RC1: complete/activate existing L3 certification and authority path.
2. RC2: connect existing service/current-channel failure producers to existing L3 wake consumer.
3. RC3: preserve governed/manual path as fallback until authority promotion.
4. RC4: keep old timer disabled.

Fixing RC1 and RC2 closes the maximum number of downstream dead/sleeping autonomous chains.

## Is The System Complete?

No.

The production system has:

- complete manual/governed execution path;
- complete movement executor;
- complete verification/rollback/learning owners;
- active evidence producers;
- active planner refresh;
- deployed L3 code.

But it does not have a currently alive autonomous movement loop that can move users end-to-end without operator authority.

## Verdict

AUTONOMOUS_MOVEMENT_SYSTEM_PARTIAL

Need New Owner: FALSE

Need New Planner: FALSE

Need New Runtime: FALSE

Need New Service: FALSE

Need New Timer: FALSE

Need New Architecture: FALSE

Minimal next action: continue through existing L3 production certification and existing L3 wake-consumption materialization path.
