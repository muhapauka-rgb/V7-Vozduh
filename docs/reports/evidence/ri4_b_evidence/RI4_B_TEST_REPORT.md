# RI4-B Test Report

## Focused Tests

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/ri4b_pycache python3 -m unittest tests.unit.test_intelligence_snapshots tests.unit.test_intelligence_workers tests.unit.test_routing_brain tests.unit.test_runtime_snapshot_fast_path
```

Result:

```text
Ran 40 tests
OK
```

## Full Test Suite

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/ri4b_pycache python3 -m unittest discover tests
```

Result:

```text
Ran 252 tests in 16.803s
OK
```

Raw output:

`docs/reports/evidence/ri4_b_evidence/unittest_discover.txt`

## Coverage Added

- user-service scoring snapshot;
- candidate suitability scoring snapshot;
- best available pool snapshot;
- snapshot freshness/confidence contract;
- planner advisory merge through fast path;
- risk influence;
- trust influence;
- history influence;
- channel quality influence;
- service quality influence;
- no execution/governance authority transfer.

