Mission ID: `V7_OMP_HEARTBEAT_REAL_CONSUMER_WIRING_V1`
Run Nonce: `V7_OMP_REAL_CONSUMER_ACTIVATION_V1_3E8A71D25C9F`

# OMP heartbeat: wiring реального consumer

Дата: `2026-07-14T23:33:00+0700`

## Admission

```text
GAP_ID=AEP-GAP-14AA3FCC0574FB31E202
CANDIDATE_INSTANCE_ID=BDP-ICI-7CFAE2C09DBC51947C9718E6
REPAIR_ID=REPAIR-REAL-CONSUMER-ACTIVATION
OMP_ADMISSION_DECISION=MISSION_ACCEPTED
DECISION_TRACE_ID=ompdt_b7237913630dbe578daffeba
DECISION_FINGERPRINT=b7237913630dbe578daffebaf3efe61475ffbb44fbd3d76584b1e1091a179d6b
MISSION_ID_CREATED=V7_OMP_HEARTBEAT_REAL_CONSUMER_WIRING_V1
```

Первый естественный run доказал broken link `RECONCILIATION_INVOCATION`. Existing owner достаточен; новый owner, scheduler, queue, daemon, Runtime, Planner или automation не требуются.

## Реализация

Расширены только существующие owners:

- `tools/v7_sync_lib.py`: fresh canonical source loader, dependency fingerprint, bounded `heartbeat_program_reentry()` и legal no-action/next-output consumer;
- `tools/v7-truth-check`: read-only `--omp-heartbeat-reentry` entrypoint;
- existing CPS owner: heartbeat run provenance и промежуточная completion truth;
- existing automation prompt: после deploy будет указывать на canonical entrypoint без изменения task identity, target thread и schedule.

Цепочка после изменения:

```text
natural platform prompt
-> tools/v7-truth-check --omp-heartbeat-reentry
-> fresh CPS and canonical program inputs
-> heartbeat_boundary_dry_run
-> program_execution_reconciliation
-> OMP_HEARTBEAT_REENTRY_CONSUMER
-> LEGAL_NO_ACTION or READY_FRONTIER_AVAILABLE
-> bounded stop; natural schedule only
```

Unchanged state возвращает `LEGAL_NO_ACTION` и `WAIT_FOR_OWNER_BACKED_DEPENDENCY_CHANGE`. Duplicate wakeup, identity mismatch и active Mission останавливаются до reconciliation. CLI read-only: CPS/report/git/Runtime/production не изменяются.

## Verification до deploy

```text
FOCUSED_TESTS=91/91_PASS
FULL_UNIT_REGRESSION=1208/1208_PASS
PROGRAM_RECONCILIATION_SOURCE_CALLERS=1
PROGRAM_RECONCILIATION_TEST_CALLERS=3
SAMPLE_ADAPTER_RESULT=NO_CHANGE_DEPENDENCY_UNCHANGED
SAMPLE_RECONCILIATION_INVOKED=TRUE
SAMPLE_CONSUMER_INVOKED=TRUE
SAMPLE_CONSUMER_DECISION=LEGAL_NO_ACTION
SAMPLE_NEXT_OUTPUT=WAIT_FOR_OWNER_BACKED_DEPENDENCY_CHANGE
RUNTIME_MUTATION=FALSE
PRODUCTION_MUTATION=FALSE
USER_MOVEMENT=FALSE
AUTHORITY_EXPANSION=FALSE
PERSISTED_EVENT_REPLAY_RESULT=NO_CHANGE_DUPLICATE_WAKEUP
PERSISTED_EVENT_REPLAY_RECONCILIATION_INVOKED=FALSE
```

Тесты и локальный вызов являются supporting evidence, не natural-run completion. AEP Phase 4 остаётся `IMPLEMENTED_MANUALLY_CALLABLE`, Phase 5 остаётся `BLOCKED_MISSING_REAL_CONSUMER` до post-repair естественного запуска.

## Deployment state

```text
IMPLEMENTATION_RESULT=IMPLEMENTED_WAITING_SAFE_DEPLOY
IMPLEMENTATION_COMMIT=PENDING
DEPLOY_ID=PENDING
DEPLOYMENT_ALIGNMENT=PENDING
POST_REPAIR_NATURAL_RUN=PENDING
CURRENT_COMPLETION_CONTRACT=AUTOMATION_COMPLETION
CURRENT_COMPLETION_VERDICT=AUTOMATION_INCOMPLETE
```

Rollback: вернуть source/prompt/CPS commit и сохранить существующий manual `Continue OMP`. Итог этого evidence snapshot: `REPAIR_IMPLEMENTED_WAITING_SAFE_DEPLOY`.
