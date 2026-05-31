# Convergence F Test Results

Project: V7 Vozduh
Block: Convergence F

## Commands Run

- `py_compile admin/v7-admin-api`
- Convergence C/E/F contract tests
- full `unittest discover`
- API route inventory checks
- UI mapping tests
- dangerous-call scan
- secret scan
- `git diff --check`

## Results

- `PYTHONPYCACHEPREFIX=/private/tmp/pycache-convergence-f python3 -m py_compile admin/v7-admin-api`: OK
- Convergence C/E/F contract tests: 35 tests OK
- `PYTHONPYCACHEPREFIX=/private/tmp/pycache-convergence-f python3 -m unittest discover -s tests -p 'test*.py'`: 154 tests OK
- `git diff --check`: OK
- focused dangerous execution endpoint scan: no mutating `/api/execution/apply`, `/api/execution/execute`, `/api/execution/run`, `/api/execution/route-apply`, or `/api/execution/autoswitch-apply` handlers found
- secret/safety scan against F reports and F test: no matches

full_tests_passed=true
