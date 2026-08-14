# V7 Vozduh — Track 5.4 Test Discovery & Extraction Gate Hardening Report

Generated: 2026-05-23

## Scope

Track 5.4 hardened the local extraction gate.

No new extraction was performed.
No admin runtime logic was changed.
No live deploy was performed.

## 1. Root Cause Of Discovery Issue

Before Track 5.4:

```bash
python3 -m unittest discover tests
```

Result:

```text
Ran 0 tests in 0.000s
OK
```

Root causes:

1. `unittest discover` uses the default pattern `test*.py`.
2. The contract file was named `endpoint_inventory_test.py`, which does not match `test*.py`.
3. Test subdirectories were not explicit importable packages.
4. Existing tests worked through explicit module invocation, but the default discovery gate was fake-green.

## 2. Exact Changes Made

Added package markers:

- `tests/__init__.py`
- `tests/contracts/__init__.py`
- `tests/unit/__init__.py`

Added discovery wrapper:

- `tests/contracts/test_endpoint_inventory.py`

This wrapper exposes the existing `EndpointInventoryContractTest` class under a default-discovery-compatible filename.

Updated endpoint inventory guard:

- `tests/contracts/endpoint_inventory_test.py`

Added exact frozen count assertions for:

- `endpoint_count`: 192
- `GET`: 47
- `HEAD`: 8
- `POST`: 137
- `public`: 19
- `required`: 173
- `csrf_required_count`: 132
- `safe_mode_blocked_count`: 86

Added stable local runner:

- `tools/v7-run-tests`

Added extraction gate documentation:

- `docs/track5/EXTRACTION_GATE.md`

## 3. Test Discovery Before/After

Before:

```text
Ran 0 tests in 0.000s
OK
```

After:

```text
Ran 20 tests in 0.146s
OK
```

The 20 discovered tests include:

- endpoint inventory contract tests: 5;
- sanitize helper tests: 4;
- time helper tests: 4;
- registry reader tests: 7.

## 4. Test Runner Behavior

Runner:

```bash
tools/v7-run-tests
```

Behavior:

- exits on first real failure via `set -euo pipefail`;
- runs `python3 -m unittest discover tests`;
- runs `py_compile` with `PYTHONPYCACHEPREFIX=/private/tmp`;
- does not touch runtime;
- does not require VPS access;
- does not require secrets;
- does not require admin login.

Observed output:

```text
== unittest discovery ==
Ran 20 tests
OK
== py_compile ==
== ok ==
```

## 5. Endpoint Inventory Guard Status

Current frozen counts:

```json
{
  "endpoint_count": 192,
  "by_method": {
    "GET": 47,
    "HEAD": 8,
    "POST": 137
  },
  "by_auth": {
    "public": 19,
    "required": 173
  },
  "csrf_required_count": 132,
  "safe_mode_blocked_count": 86
}
```

If these counts change, the test now fails unless the inventory contract is intentionally updated with explanation.

## 6. Fixture Path Robustness

Registry fixture tests use:

```python
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "registry"
```

This is stable under:

- repository root execution;
- `python3 -m unittest discover tests`;
- explicit module invocation.

No fixture depends on the current working directory.

## 7. Commands Run And Results

Baseline:

```bash
python3 -m unittest discover tests
```

Result before fix:

- OK, but 0 tests discovered.

Verification after fix:

```bash
python3 -m unittest discover tests
```

Result:

- OK, 20 tests.

```bash
tools/v7-run-tests
```

Result:

- OK, 20 tests plus py_compile.

```bash
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py
```

Result:

- OK.

## 8. Diff Safety Review

Track 5.4 changed only:

- test package structure;
- test discovery wrapper;
- endpoint inventory contract assertions;
- local test runner;
- extraction gate documentation;
- this report.

Track 5.4 did not change:

- `admin/v7-admin-api`;
- endpoint logic;
- Handler dispatch;
- JSON response shapes;
- auth/session/RBAC/CSRF/safe-mode;
- identity;
- provisioning;
- autoswitch;
- Direct/RU or Trusted RU/Gosuslugi;
- shell wrappers;
- runtime paths;
- embedded UI;
- production runtime.

Note: the working tree still contains prior Track 5.2/5.3 admin/core/test additions. Track 5.4 itself added no admin runtime logic changes.

## 9. Extraction Gate Reliability Verdict

The extraction gate is now reliable for local containment work.

Before Track 5.4, the default command was dangerously fake-green.
After Track 5.4, the default command discovers and runs the existing contract and unit tests.

## 10. Whether Next Tiny Extraction Is Allowed

Allowed only if it passes the hardened gate:

1. Add fixtures before moving logic.
2. Run `tools/v7-run-tests`.
3. Regenerate endpoint inventory.
4. Confirm frozen endpoint counts remain unchanged.
5. Confirm no admin/runtime behavior changes.
6. Do not live deploy without explicit approval.

Still not allowed:

- state layer extraction;
- registry writer extraction;
- auth/session extraction;
- identity extraction;
- provisioning extraction;
- autoswitch extraction;
- routing/Direct/RU/Trusted RU extraction;
- Handler extraction;
- UI extraction.
