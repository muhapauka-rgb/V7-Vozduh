# P5.1 Implementation Conflict Audit

## Scope

Inspect existing runtime truth access implementations and prevent duplicate readers.

## Existing Implementations

### Registry Readers

- `admin_core/registry_readers.py`
- side-effect free parser only
- no file IO
- shared parser for admin surfaces

### Operator Execution

- `admin_core/operator_execution.py`
- reads `users.registry` and `egress.registry` from a supplied `state_dir`
- reads selected moves from:
  - `selected-moves.json`
  - `selected_moves.json`
  - `current-selected-moves.json`
- computes:
  - users registry hash
  - egress registry hash
  - selected moves hash
  - runtime snapshot hash
- fails closed on missing registries and hash mismatch

### Admin Runtime APIs

- `admin/v7-admin-api`
- direct runtime readers:
  - `/api/state`
  - `/api/users`
  - `/api/egress`
  - `/api/runtime/fingerprint`
  - `/api/runtime/convergence`
  - `/api/runtime/dry-run/summary`
  - `/api/runtime/dry-run/verification`
- these are authenticated read-only presentation/derived APIs

### Runtime Support

- `tools/runtime-support/v7-state-json`
- `tools/runtime-support/v7-state-json-save`
- `tools/runtime-support/v7-state-stale-check`
- `tools/v7-runtime-contract-validate`
- `tools/v7-observability-summary`
- `tools/v7-infrastructure-readiness-review`
- `tools/v7-intelligence-readiness-review`

## Conflict Decision

Equivalent runtime truth access already exists.

P5.1 does not add new readers, new APIs, runtime hooks, execution engines, or state stores.

Future work should reuse the existing `STATE_DIR` model and `operator_execution.runtime_recheck(...)`.

## Verdicts

- implementation_conflict_audit_complete=true
- duplicate_runtime_truth_reader_created=false
- duplicate_runtime_truth_store_created=false
- reuse_existing_state_dir_model=true
