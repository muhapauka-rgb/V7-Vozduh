# Engineering Report: Decision Commit Replay Validation

## Summary

Проверен original stale-packet loop после Phase 1 Decision Commit implementation.

Вердикт: `ROOT_CAUSE_ELIMINATED` локально.

## Action Performed

- Воспроизведен сценарий: READY preview -> operator approval identity -> lease creation from committed preview.
- Проверены negative identity cases: packet, decision, operation, selected move, user, source, target, authority.
- Runtime apply не выполнялся.

## Objective Observations

- READY preview produced: YES.
- Decision committed: YES.
- Same semantic refreshed preview changed `packet_id`: YES.
- Same semantic refreshed preview preserved `decision_id`: YES.
- Lease created from committed preview: YES.
- Planner reran before lease: NO.
- Candidate selection reran before lease: NO.
- Lease preserved packet / decision / operation / selected move hash: YES.
- Identity violations fail closed: YES.

## Engineering Conclusions

Original stale-packet loop is removed for the implemented local committed-preview lease path.

The previous failure mode was:

```text
approved preview -> lease path rebuilds preview -> different identity -> stop
```

The validated behavior is now:

```text
approved committed preview -> lease consumes same preview -> same packet/decision/operation/hash -> no planner rerun
```

## Impact

A4 can safely return to OMP after deploy. This validation does not create production evidence and does not certify A4.

## Capability Progress

Decision Commit / A4 support improved. Production maturity unchanged.

## Backlog Progress

A4 implementation support validated locally. A4 still requires production governed outcome evidence after deployment.

## Production Maturity

Unchanged.

## Canonical Knowledge

No canonical owner updated. Durable contract already exists in Phase 0 / 0.5 reports.

## Evidence

- Replay script: committed preview consumed, lease written, planner rerun false, packet/decision/operation/hash preserved.
- Negative cases: packet, decision, operation, selected move, user, source, target and authority mismatches returned `EXECUTION_LEASE_NOT_CREATED`.
- Relevant tests: `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_replay_tests python3 -m unittest tests.unit.test_operator_execution_pipeline tests.unit.test_operator_execution_packet tests.unit.test_v7_users_autoswitch_policy tests.unit.test_operator_observability tests.unit.test_v7_restore_settle_gate tests.unit.test_v7_second_canary_target_readiness` -> OK, 187 tests.
- Truth: NO-GO because workspace is dirty, runtime-critical local changes are not deployed, GitHub remote is unreadable / canonical branch missing on remote.
- Convergence: NOT_ALIGNED / DEPLOY_REQUIRED for `admin_core/operator_execution_pipeline.py` and `tools/v7-governed-canary-dry-run-cycle`.

## Next Step

Deploy the tested runtime-relevant changes through existing safe deploy owner, then return to OMP/A4 governed production flow.

## Re-audit Rule

Re-audit only if packet/decision/lease identity behavior changes, or production replay disproves local replay behavior.
