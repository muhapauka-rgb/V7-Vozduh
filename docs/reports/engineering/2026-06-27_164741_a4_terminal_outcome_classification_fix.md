# Engineering Report: A4 Terminal Outcome Classification Fix

Дата: 2026-06-27 16:47:41 +0700
Статус: IMPLEMENTED_LOCALLY
Owner reused: `tools/v7-governed-canary-dry-run-cycle`, `admin_core/operator_execution_feedback.py`
Need New Owner: FALSE
Need New Backlog: FALSE
Need New Architecture: FALSE

## Summary

Исправлен A4 defect: результат `apply YES + verification FAIL + rollback COMPLETED` больше не материализуется как `SUCCESS`.
Классификация теперь идет от финального terminal transaction state.

## Action Performed

- `materialize_governed_transaction_feedback` теперь передает `terminal_outcome_classification`.
- `operator_execution_feedback` классифицирует outcome в порядке:
  `Apply -> Verification -> Rollback / No-Rollback -> Terminal Transaction State -> Outcome Classification`.
- Legacy success/rollback records сохранены совместимыми.

## Objective Observations

Предыдущий дефект возникал потому, что apply был успешным, но verification failed и rollback completed.
Старый путь считал apply success как итоговый success.
Это давало ложное положительное learning/trust/promotion evidence.

## Classification Matrix

| Terminal facts | Classification |
| --- | --- |
| Apply PASS, Verification PASS, Rollback NOT_REQUIRED | `SUCCESS` |
| Apply PASS, Verification FAIL, Rollback COMPLETED | `ROLLBACK_SUCCESS` |
| Apply PASS, Verification FAIL, Rollback FAILED | `ROLLBACK_FAILURE` |
| Apply FAIL | `APPLY_FAILURE` |
| STOP_SAFE before Apply | `NO_EXECUTION` |

## Learning Matrix

| Classification | Learning |
| --- | --- |
| `SUCCESS` | Positive learning; trust and recommendation may increase. |
| `ROLLBACK_SUCCESS` | Rollback/failure-family learning; trust does not increase; recommendation decreases for this condition. |
| `ROLLBACK_FAILURE` | Failure and rollback-risk learning; success metrics do not increase. |
| `APPLY_FAILURE` | Failure learning only. |
| `NO_EXECUTION` | No production outcome learning. |

## Impact

Rollback evidence remains real evidence, but no longer counts as successful move evidence.
Promotion readiness is protected because rollback categories stay separate from `SUCCESS`.
A4 can resume bounded evidence collection after safe deploy and truth/convergence alignment.

## Capability Progress

A4 representative evidence remains `93 / 156 = 59.6%`.
This fix improves Learning and Production Readiness correctness, but does not itself add production evidence.

## Backlog Progress

Backlog item: `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`.
Progress unchanged until the next real bounded transaction outcome.

## Production Maturity

Production Maturity remains `24.0%` until deployment and further certified production outcomes.

## Canonical Knowledge

Durable rule added to `docs/reference/V7_RUNTIME_MODEL.md`:
production transaction classification must use final terminal transaction state, not intermediate apply state.

## Evidence

Focused and relevant tests:

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m unittest \
  tests.unit.test_operator_execution_feedback \
  tests.unit.test_governed_canary_cli \
  tests.unit.test_intelligence_workers \
  tests.unit.test_autonomy_trust_acceleration \
  tests.unit.test_intelligence_platform \
  tests.unit.test_channel_trust_recovery

Ran 124 tests in 0.873s
OK
```

Syntax validation:

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile \
  admin_core/operator_execution_feedback.py \
  tools/v7-governed-canary-dry-run-cycle

PASS
```

## Next Step

Run safe deploy, truth, convergence, then continue bounded A4 evidence collection under the existing approved A4 envelope.

## Re-audit Rule

Re-audit terminal classification only if transaction terminal states change, feedback materialization changes, promotion consumes rollback as success, or production evidence disproves the classification matrix.
