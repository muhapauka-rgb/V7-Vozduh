# PERF.3 Test Results

## Commands

- `PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache_perf3 python3 -m py_compile admin_core/intelligence_workers.py tools/v7-intelligence-snapshot-refresh tests/unit/test_intelligence_workers.py`
  - result: PASS

- `python3 -m unittest tests.unit.test_intelligence_workers`
  - result: PASS
  - tests: 9

- `python3 -m unittest discover tests`
  - result: PASS
  - tests: 241

- `git diff --check`
  - result: PASS

## Covered

- service score worker
- channel service score worker
- trust worker
- risk worker
- blast radius worker
- overview worker
- bounded JSONL tail
- missing input warnings
- snapshot write/read
- worker architecture forbidden authority
