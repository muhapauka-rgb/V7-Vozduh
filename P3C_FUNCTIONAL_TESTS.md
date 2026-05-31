# P3.C Functional Tests

Project: V7 Vozduh
Block: P3.C First Runtime Dry-Run

## Functional Coverage

`tests/contracts/test_p3c_first_runtime_dry_run.py` imports `admin/v7-admin-api` with a temporary read-only state tree and verifies:

- Input adapter reads.
- Report shape.
- Decision mapping into allowed outputs.
- Safety flags.
- Derived-on-demand storage.
- Empty write path.

Existing preview tests were also rerun:

- `tests.contracts.test_convergence_c_wave2_execution_preview_layer`
- `tests.contracts.test_convergence_c_wave3_candidate_workflow_layer`
- `tests.contracts.test_convergence_f_final_resolution`

## Test Results

- P3.C test: PASS, 6 tests.
- Existing preview/candidate/simulation tests: PASS, 17 tests.

## Verdict

`functional_tests_passed=true`

