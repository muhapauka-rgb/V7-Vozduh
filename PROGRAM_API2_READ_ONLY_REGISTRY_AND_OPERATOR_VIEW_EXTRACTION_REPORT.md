# PROGRAM API.2 READ-ONLY REGISTRY AND OPERATOR VIEW EXTRACTION REPORT

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Mission

Extract the first read-only admin API helpers from `admin/v7-admin-api` into `admin_core` without touching execution, governance, rollback, auth, CSRF, audit writes, closure writes, UI separation, or runtime mutation.

## Baseline

Initial workspace was clean before API.2 changes.

Baseline endpoint inventory:

- endpoint count: `264`
- read API endpoints: `109`
- action endpoints: `133`
- CSRF-required endpoints: `133`
- safe-mode-blocked endpoints: `86`

Evidence:

- `api2_evidence/before_endpoint_inventory.json`

## Extraction Performed

Created:

- `admin_core/admin_registry_views.py`

Extracted pure read-only registry helpers for:

- registry file loading
- registry row parsing
- redaction-preserving registry serialization
- egress registry rows/maps/defaults
- user registry rows/maps
- safe egress id and user IP validation helpers
- lightweight request snapshot foundation via `AdminRegistrySnapshot`

Updated `admin/v7-admin-api` only by replacing local registry helper bodies with calls into `admin_core.admin_registry_views`.

## Operator Views

Operator summaries, evidence/timeline builders, service matrix summaries, and route-class summaries were not extracted in API.2.

Reason: those areas are more tightly coupled to endpoint rendering and operational state readers. Moving them without dedicated parity fixtures would increase risk. They are classified as API.3 scope.

## Request Snapshot Foundation

`AdminRegistrySnapshot` was added as a lightweight request snapshot helper. It loads registry rows once and exposes read-only row/map/default helpers.

No caching layer was added. No runtime behavior changed.

## Tests

Added:

- `tests/unit/test_admin_registry_views.py`

Coverage:

- user registry view parity
- egress registry view parity
- redaction parity
- missing file handling
- malformed row handling
- no write/action API exposed
- request snapshot foundation behavior

Verification:

```bash
python3 -m unittest tests.unit.test_admin_registry_views
PYTHONPYCACHEPREFIX=/tmp/api2_pycache python3 -m py_compile admin/v7-admin-api admin_core/admin_registry_views.py
python3 -m unittest discover tests
```

Results:

- registry view unit tests: `OK`, `5` tests
- compile check: `OK`
- full unit suite: `OK`, `205` tests

## Endpoint Parity

After inventory:

- endpoint count: `264`
- stable endpoint definitions unchanged: `true`
- summary unchanged: `true`

Expected metadata drift:

- `admin/v7-admin-api` source line count changed from `36468` to `36459`
- endpoint source line metadata shifted because helper code moved out of the monolith

Evidence:

- `api2_evidence/after_endpoint_inventory.json`
- `api2_evidence/endpoint_inventory_comparison.md`

## Safety Scan

No forbidden surface was changed.

Confirmed:

- `runtime_behavior_changed=false`
- `governance_behavior_changed=false`
- `execution_behavior_changed=false`
- `rollback_behavior_changed=false`
- `auth_changed=false`
- `run_action_changed=false`
- `users_moved=false`
- `autoswitch_apply_run=false`

No deploy, autoswitch apply, runtime mutation, service restart, rollback, governance mutation, audit write, or closure write was performed.

## Metrics

- lines removed from `admin/v7-admin-api`: `9`
- lines added in `admin_core/admin_registry_views.py`: `163`
- test lines added: `97`
- remaining monolith size: `36459` lines

## API.3 Recommendation

The next safest API.3 scope is read-only operator/service/route view extraction with dedicated parity fixtures before moving any additional logic.

Recommended API.3 candidates:

- operator summary payload builders
- evidence/timeline read builders
- service matrix summaries
- route-class summaries

Continue to exclude auth, RBAC, CSRF, `run_action`, execution, rollback, governance mutation, audit writers, closure writers, and UI separation.

## Final Verdicts

- `registry_views_extracted=true`
- `operator_views_extracted=false`
- `request_snapshot_foundation_created=true`
- `schema_tests_created=true`
- `endpoint_inventory_unchanged=true`
- `tests_pass=true`
- `runtime_behavior_preserved=true`
- `governance_behavior_preserved=true`
- `safe_to_begin_API3=true`
