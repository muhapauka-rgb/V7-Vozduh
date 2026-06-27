# Engineering Report: A4 goal-directed selection fix

## Summary

Исправлен существующий A4 governed selection path: перед bounded transaction теперь выбирается safe eligible кандидат, который закрывает текущий A4 missing evidence key. Негэповые кандидаты больше не доходят до lease/restore/apply в A4 collection.

## Action Performed

- Расширен существующий owner `tools/v7-governed-canary-dry-run-cycle`.
- Добавлен read-model scan текущего `candidate-suitability-summary`.
- Добавлен выбор missing `(user, target)` candidate key перед packet cycle.
- Добавлен fail-closed stop `NO_SAFE_GAP_REDUCING_A4_CANDIDATE`.
- Добавлены unit tests для выбора, stop-safe, one-user limit и сохранения authority/runtime boundaries.

## Files Changed

- `tools/v7-governed-canary-dry-run-cycle`
- `tests/unit/test_governed_canary_cli.py`

## Functions Changed

- `select_a4_gap_reducing_candidate`
- `merge_a4_gap_candidate_into_surface`
- `execute_governed_transaction_with_guards`
- `GovernedCanaryCliTest.ready_cycle`

## Objective Observations

- Missing keys are loaded before A4 selection through existing `current_a4_missing_candidate_keys`.
- Candidate universe is read from existing `candidate-suitability-summary`.
- `candidate_key` is `(user, target)`.
- Non-missing candidates are skipped before packet cycle.
- Unsafe/unready candidates are skipped before packet cycle.
- If no safe gap-reducing candidate exists, transaction stops before lease, restore barrier, apply, or movement.

## Engineering Conclusions

Root cause is fixed through existing owners only. This is not a new planner, not new governance, not a new runtime path, and not authority expansion.

## Tests Run

- `python3 -m unittest tests.unit.test_governed_canary_cli -v` = PASS
- `python3 -m unittest tests.unit.test_operator_execution_feedback tests.unit.test_autonomy_trust_acceleration -v` = PASS
- `python3 -m unittest tests.unit.test_operator_execution_pipeline tests.unit.test_operator_execution_packet -v` = PASS
- `PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7-governed-canary-dry-run-cycle` = PASS

## Validation

- `tools/v7-autonomy-trust-evidence-inventory --json` = not supported by current CLI.
- `tools/v7-autonomy-trust-evidence-inventory --pretty` = PASS, read-only, no movement.
- Safe deploy = PASS.
- Deploy id: `deploy-z8-14-Updatesystem-1db9267-20260627T180506`.
- `tools/v7-truth-check --all --json` = PASS.
- `tools/v7-convergence-status --json` = PASS / ALIGNED.

## Impact

- Runtime automation enabled: NO.
- Authority expanded: NO.
- Users moved during implementation: 0.
- Synthetic evidence created: NO.
- A4 is no longer blocked by non-gap-directed selection.

## Capability Progress

A4 remains `94 / 156 = 60.3%` until the next real governed production outcome is recorded.

## Next Step

Continue OMP: resume A4 bounded representative evidence collection through the existing governed transaction owner.

## Re-audit Rule

Re-audit only if A4 again selects a non-missing candidate while safe gap-reducing candidates exist.
