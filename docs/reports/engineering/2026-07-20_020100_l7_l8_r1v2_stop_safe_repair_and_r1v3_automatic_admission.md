# Инженерный отчёт: R1 v2 STOP_SAFE, ремонт и автоматический допуск R1 v3

Дата: `2026-07-20T02:01:00+07:00`  
Program: `V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_PROGRAM_V1`  
Mission: `V7_L7_L8_R1V2_STOP_SAFE_REPAIR_AND_R1V3_AUTOMATIC_ADMISSION_V1`  
Terminal: `R1_V3_EXACT_SCOPE_REPAIR_CONTINUATION_AUTO_ADMITTED_READY`

## Итог

Одноразовый request v2 `engauth_r1_f89460c18394f8fee79c9724` потреблён ровно один раз и остановлен до forward apply. Пользователь не перемещён, rollback не запускался, L7 evidence не создано. Exact cleanup восстановил certification user `10.7.0.16` на `vless`, controlled source включён, Admin Safe Mode `OPEN`.

Причина STOP_SAFE — преждевременный full service-matrix refresh изменил активный incident-source до planner admission. Approved-plan lock затем честно обнаружил:

- `approved_plan_lock_incident_source_mismatch`;
- `approved_plan_lock_user_source_mismatch`.

Blocker fingerprint: `d5a3338f8023562d9d803231eaf035d99d13c6aea0eaa528c552650b6a06cad1`.

## Ремонт существующих owners

Commit: `2eceabb312eb1cbe2f224439c9c460ccb48585d8`  
Safe deploy: `deploy-z8-14-Updatesystem-2eceabb-20260720T015856`

- lifecycle refresh теперь сообщает отдельный owner-backed marker только после фактического захвата writer lock;
- controlled contention начинается только после подтверждённого forward route acknowledgement;
- exact controlled verifier scope отделён от несвязанных matrix incidents и повторно читает canonical registry;
- ошибка запуска lifecycle восстанавливает source и не вызывает direct rollback;
- fresh request участвует в Packet/operation identity, поэтому новый request не наследует старые identities;
- существующий admission owner валидирует standing repair-continuation policy и может разрешить только fresh exact-scope one-use request.

Проверки: `248 + 71 = 319 PASS`. Manifest safe deploy содержал только пять ожидаемых runtime-файлов; Runtime apply, routing/user mutation, service restart, Authority и Production Maturity effects при deploy отсутствовали.

## Автоматизация без повторного запроса человеку

Policy: `engrepair_fe6a2c49ae391f397330274a`  
Policy hash: `fe6a2c49ae391f397330274acbe55b3d081f9cf7bcffd8c45d741e81bbbc2cc5`

Автоматический continuation разрешён только когда одновременно доказаны:

- предыдущий request завершился pre-apply `STOP_SAFE`;
- apply=false, moved=0, rollback=false;
- exact cleanup PASS;
- blocker новый и не повторился после ремонта;
- ремонт протестирован, закоммичен, безопасно задеплоен и truth/convergence aligned;
- user/source/target/condition/policy/evidence cell/blast radius полностью совпадают.

Это не повторное использование approval. Каждый допуск создаёт fresh request, Candidate, Packet, lease и transaction nonce. Повтор того же blocker fingerprint или любой scope drift автоматически останавливает процесс.

## Fresh v3

Request: `engauth_r1_5ecff8aa38fd049d142a030a`  
Contract: `5ecff8aa38fd049d142a030a4d6e72269ce1767d245aa6b265d22558ca2cbd22`  
Decision: `APPROVE_ONCE_AS_SCOPED`, resolved by existing owner from the standing policy  
Execution mode: one foreground controlled-production transaction; no retry; no background Runtime

CPS atomically advanced to `cpsgen_V7_L7_L8_R1V3_5ECFF8AA38FD`. Controlled lane is `READY`; natural L8 lane remains capture-ready at its honest `REAL_WORLD_LIMIT`.

## Evidence classes and safety

- Code: repaired and deployed.
- Tests: `319 PASS`.
- Deploy: PASS, no forbidden deploy effects.
- v2 production transaction: `CONSUMED_STOP_SAFE_BEFORE_APPLY`, not L7 evidence.
- Cleanup: PASS, Engineering Evidence only.
- v3 production transaction: `READY_NOT_STARTED` at this report boundary.
- Authority expansion: `NONE`.
- Production Maturity: `NO_CHANGE`, `66.9`.

Exact next output: `EXECUTE_CONTROLLED_ROLLBACK_PRODUCTION_TRANSACTION_R3_R4_V3`.
