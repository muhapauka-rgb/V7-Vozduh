# V7 Vozduh - Track 5.1 Endpoint Inventory & Read-Only Contract Tests

Generated: 2026-05-23

Goal: create endpoint inventory and initial contract-test foundation before any admin monolith extraction.

Runtime behavior changed:

```text
none
```

## 1. Endpoint Inventory Summary

Created machine-readable inventory:

- `docs/track5/endpoint-inventory.json`

Generator:

- `tools/v7-admin-endpoint-inventory`

Inventory source:

- `admin/v7-admin-api`

Summary:

| Metric | Count |
|---|---:|
| Source lines | 30067 |
| Endpoint branches | 192 |
| GET | 47 |
| HEAD | 8 |
| POST | 137 |
| Public | 19 |
| Auth required | 173 |
| CSRF-required | 132 |
| Safe-mode blocked actions | 86 |

Risk distribution:

| Risk | Count |
|---|---:|
| low | 47 |
| medium | 37 |
| high | 95 |
| critical | 13 |

## 2. Read-Only Endpoint Contract Status

Initial required read-only endpoints are now represented by fixtures/specs:

- `/health`
- `/api/session`
- `/api/overview`
- `/api/events`
- `/api/diagnostics`

Captured:

- expected unauthenticated behavior;
- response type;
- top-level authenticated keys;
- redaction expectations;
- auth requirement.

## 3. Fixtures / Tests Created

Created:

- `tests/contracts/endpoint_inventory_test.py`
- `tests/contracts/fixtures/health.json`
- `tests/contracts/fixtures/session_unauthenticated.json`
- `tests/contracts/fixtures/overview_schema.json`
- `tests/contracts/fixtures/events_schema.json`
- `tests/contracts/fixtures/diagnostics_schema.json`

Test coverage:

- admin file compiles;
- inventory schema exists and has counts;
- required endpoints are present;
- fixture specs match inventory;
- selected dangerous POST endpoints require auth + CSRF + role.

## 4. Auth Behavior Captured

Captured statically:

- public endpoints;
- required-auth endpoints;
- GET role overrides;
- action minimum roles;
- CSRF-required action endpoints;
- safe-mode-blocked actions.

Important:

No test bypasses auth. Authenticated live contracts are still fixtures/specs until a safe test session strategy exists.

## 5. Response-Shape Freeze Status

Frozen now:

- initial top-level keys for the first read-only endpoint set;
- unauthenticated behavior for protected read-only endpoints;
- JSON/html/file response type classification;
- critical action guard requirements in inventory tests.

Still missing:

- nested schemas;
- live authenticated snapshots;
- full action endpoint response schemas;
- binary/file endpoint contracts;
- redaction tests for token/config paths.

## 6. Exact Files Created / Changed

Created:

- `docs/track5/endpoint-inventory.json`
- `docs/track5/ENDPOINT_INVENTORY_REPORT.md`
- `tools/v7-admin-endpoint-inventory`
- `tests/contracts/endpoint_inventory_test.py`
- `tests/contracts/fixtures/health.json`
- `tests/contracts/fixtures/session_unauthenticated.json`
- `tests/contracts/fixtures/overview_schema.json`
- `tests/contracts/fixtures/events_schema.json`
- `tests/contracts/fixtures/diagnostics_schema.json`
- `TRACK5_1_ENDPOINT_CONTRACT_TESTS_REPORT.md`

Modified:

- none of the runtime admin endpoint logic.

## 7. Verification Results

Commands run locally:

```text
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/track5/endpoint-inventory.json
python3 -m unittest tests.contracts.endpoint_inventory_test
```

Results:

```text
inventory generated: OK
tests: OK
Ran 5 tests in 0.133s
```

No live runtime verification was performed because no production runtime file was changed.

## 8. Extraction Readiness Verdict

Can start next:

```text
admin_core.sanitize
admin_core.time
```

Only if:

- extraction is tiny;
- pure helpers only;
- no state IO;
- no Handler changes;
- no endpoint response changes;
- no shell command changes;
- contract tests pass before and after.

Not ready:

- registry parser extraction;
- auth extraction;
- identity extraction;
- provisioning extraction;
- autoswitch extraction;
- direct/RU extraction;
- UI extraction;
- Handler route split.

## 9. Remaining Gaps

Next contract work should add:

1. Authenticated read-only smoke strategy.
2. Nested schema assertions for `/api/overview`.
3. Preview endpoint fixtures.
4. Redaction assertions for profile/config/token-bearing responses.
5. Static command dependency checks per endpoint.
6. Endpoint inventory diff check in CI or local pre-deploy script.

