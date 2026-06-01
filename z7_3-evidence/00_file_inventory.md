# Z7.3 Evidence 00 - File Inventory

Program: PROGRAM Z7.3 - Minimal Implementation Plan Audit  
Project: V7 Vozduh  
Branch target: v7-next  
Mode: READ ONLY implementation-readiness audit

## File Inventory

| File | Role | Ownership | Change Likelihood | Risk | Classification |
|---|---|---|---|---|---|
| `tools/v7-users-autoswitch` | Runtime owner; planner/apply/verify/rollback JSON producer | Runtime/execution owner | HIGH | MEDIUM | REUSE, EXTEND |
| `tools/runtime-support/v7-audit-log` | Canonical audit sink; accepts metadata/object/request fields | Audit owner | LOW | LOW | REUSE, NO CHANGE preferred |
| `admin/v7-admin-api` | Admin action wrapper, autoswitch guarded apply/dry-run, closure store/actions, audit wrapper | Operator/closure owner | LOW/MEDIUM | MEDIUM | REUSE, OPTIONAL EXTEND |
| `admin_core/operator_observability.py` | Operation lineage reader, historical operation summaries, audit/export/governance previews | Observability owner | LOW/MEDIUM | LOW | REUSE, OPTIONAL EXTEND |
| `admin_core/operator_execution.py` | Zero-move governance packet validation and append-only governance audit | Governance owner | LOW | LOW/MEDIUM | REUSE, DO NOT TOUCH for minimal runtime wiring |
| `tests/unit/test_v7_users_autoswitch_policy.py` | Autoswitch planner fixtures and plan assertions | Unit tests | HIGH | LOW | EXTEND |
| `tests/unit/test_operator_execution_packet.py` | Governance packet/replay/hash tests | Unit tests | LOW | LOW | REUSE, optional extension only if packet references change |
| `tests/unit/test_operator_observability.py` | Operator views, audit export preview, lineage archive tests | Unit tests | LOW/MEDIUM | LOW | OPTIONAL EXTEND |
| `tests/contracts/test_endpoint_inventory.py` | API endpoint contract inventory | Contract tests | LOW | LOW | NO CHANGE unless endpoints change |
| `systemd/v7-users-autoswitch.timer` | Runtime scheduler | Scheduler | NONE | HIGH if touched | DO NOT TOUCH |
| `systemd/v7-users-autoswitch.service` | Runtime service invocation | Scheduler/service bridge | NONE | HIGH if touched | DO NOT TOUCH |
| `systemd/drafts/v7-autoswitch-planner.*` | Dormant/draft planner scheduler | Latent duplicate | NONE | HIGH if activated | DO NOT TOUCH |

## Additional File Findings

No new file is required for minimum implementation.

No storage file should be created.

No API file should be created.

No systemd file should be changed.

## Minimal File Set

Absolute minimum code file:

- `tools/v7-users-autoswitch`

Absolute minimum test file:

- `tests/unit/test_v7_users_autoswitch_policy.py`

Optional follow-up files:

- `admin/v7-admin-api`
- `admin_core/operator_observability.py`
- `tests/unit/test_operator_observability.py`

