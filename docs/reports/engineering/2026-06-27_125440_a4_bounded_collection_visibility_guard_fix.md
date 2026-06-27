# Engineering Report: A4 bounded collection visibility guard fix

## Summary

Исправлен текущий `UNSAFE_IMPLEMENTATION` для A4 bounded evidence collection.

## Action Performed

- Existing governed transaction owner extended.
- Existing feedback owner extended.
- No new owner.
- No new backlog item.
- No runtime automation.
- No authority expansion.
- No user movement during the fix.

## Objective Observations

Production bounded collection previously produced `4` successful governed transaction records, but A4 evidence remained `88 / 156 = 56.4%`.

Root cause:

- bounded collection accepted transactions that did not necessarily close a current missing A4 candidate key;
- duplicate candidate detection happened after a transaction completed, so a repeated candidate could reach apply before `STOP_SAFE`;
- feedback lineage did not expose `selected_moves` at the materialized record level.

## Engineering Conclusions

The issue maps to existing owners:

- `tools/v7-governed-canary-dry-run-cycle`;
- `admin_core/operator_execution_feedback.py`;
- existing A4 evidence matcher/read-model owners.

Need New Owner: `FALSE`.

Need New Backlog Item: `FALSE`.

## Impact

Bounded A4 collection now:

- computes current missing A4 candidate keys before each transaction;
- stops before lease, restore barrier, and apply if the fresh packet does not reduce A4 evidence;
- stops before lease, restore barrier, and apply if the same transaction identity repeats;
- preserves selected-move lineage in materialized execution feedback.

## Capability Progress

A4 implementation safety improved.

A4 evidence progress is unchanged until a new real production transaction is executed:

- current: `88 / 156 = 56.4%`;
- remaining: `68 / 156 = 43.6%`.

## Backlog Progress

Current item remains:

`A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`

## Production Maturity

Production Maturity remains `24.0%` until real evidence is consumed.

## Canonical Knowledge

Durable knowledge: bounded evidence collection must execute only candidates that can reduce the current A4 evidence gap.

Canonical owner is unchanged.

## Evidence

Focused tests:

`python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_feedback tests.unit.test_intelligence_workers`

Result: `58 / 58 PASS`.

Relevant tests:

`python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_feedback tests.unit.test_intelligence_workers tests.unit.test_autonomy_trust_acceleration tests.unit.test_operator_execution_pipeline tests.unit.test_v7_users_autoswitch_policy`

Result: `209 / 209 PASS`.

Truth/convergence before commit correctly reported `NO-GO` because runtime-relevant files were dirty.

## Next Step

Commit, deploy through existing safe deployment owner, run truth/convergence, then resume A4 bounded evidence collection only if production is aligned.

## Re-audit Rule

Re-audit only if bounded collection again produces successful governed transactions without reducing A4 evidence, or if duplicate candidates can still reach apply.
