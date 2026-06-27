# A4 Bounded Evidence Collection Mode

## Summary

В existing governed canary owner добавлен bounded режим для A4: один явный authority envelope может собрать до заданного числа успешных one-user governed outcomes без повторного packet approval на каждый кандидат.

## Action Performed

- Расширен `tools/v7-governed-canary-dry-run-cycle`.
- Добавлены флаги:
  - `--execute-a4-bounded-evidence-collection`;
  - `--confirm-a4-bounded-evidence-collection`;
  - `--max-evidence-outcomes`.
- Добавлены unit tests в `tests/unit/test_governed_canary_cli.py`.
- Коммит `87c9d2fecec9a418cf9214d0b523f90ee4ecc0af` запушен и задеплоен.

## Objective Observations

- A4 progress: `88 / 156` representative candidate outcomes, `56.4%`.
- Remaining A4 evidence: `68 / 156`, `43.6%`.
- Runtime automation: `NO`.
- Authority expanded: `NO`.
- Users moved by this implementation: `NO`.
- New owner: `NO`.
- New backlog item: `NO`.

## Engineering Conclusions

Текущий ручной loop по одному packet approval заменен на безопасно материализованный bounded collection mode внутри существующего owner. Это не автономия и не authority expansion: production movement всё еще требует явного approval для bounded envelope.

## Impact

- A4 теперь может двигаться не через десятки ручных подтверждений, а через один bounded approval.
- Каждый transaction всё равно остается one-user governed transaction.
- Любой failed gate останавливает collection.

## Capability Progress

- Learning: progress can advance only through real observed outcomes.
- Authority Evolution: repeated exact packet approval is reduced, but runtime autonomy is still disabled.
- Production Readiness: deployment/truth/convergence passed after implementation.

## Backlog Progress

- Current backlog item: `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`.
- A4 remains `IN_PROGRESS`.
- Next required action: approve or reject bounded A4 evidence collection.

## Production Maturity

Production Maturity remains `24.0%` until real governed outcomes are recorded and consumed by evidence inventory.

## Canonical Knowledge

Durable rule confirmed: bounded evidence collection must reuse existing governed transaction, packet, lease, restore barrier, apply, verification, rollback, feedback, and learning owners.

## Evidence

- Focused tests: `tests.unit.test_governed_canary_cli` -> `8` tests OK.
- Relevant tests: `tests.unit.test_governed_canary_cli`, `tests.unit.test_operator_execution_feedback`, `tests.unit.test_operator_execution_pipeline`, `tests.unit.test_v7_sync_tools` -> `76` tests OK.
- Deploy id: `deploy-z8-14-Updatesystem-87c9d2f-20260627T120908`.
- Full truth with network access: `PASS`.
- Production CLI exposes `--execute-a4-bounded-evidence-collection`.

## Next Step

Stop at `OPERATIONAL_AUTHORITY`: approve or reject bounded A4 evidence collection for up to `68` successful one-user governed outcomes.

## Re-audit Rule

Re-audit this mode only if governed transaction semantics, A4 evidence model, authority boundaries, restore barrier, verification, rollback, or feedback/learning owners materially change.
