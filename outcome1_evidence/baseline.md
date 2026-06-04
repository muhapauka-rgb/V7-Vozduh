# Baseline

Branch: `Updatesystem`

Latest pre-program commit:

`61ceab4 PROGRAM data lineage reality audit and outcome map`

Baseline checks:

- workspace clean before edits;
- lineage audit present;
- RI6 worker forced `prediction_actuals=[]`, `service_actuals=[]`, `candidate_outcomes=[]` before this program.

Touched components:

| Component | Classification |
| --- | --- |
| `admin_core/intelligence_workers.py` | EXTEND |
| `tools/v7-intelligence-snapshot-refresh` | EXTEND |
| `tests/unit/test_intelligence_workers.py` | EXTEND |
| `admin_core/intelligence_platform.py` | DO_NOT_TOUCH |
| planner/governance/execution/rollback owners | DO_NOT_TOUCH |
