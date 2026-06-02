# P2.3 Adapter Implementation

## Result

adapters_implemented=true

## Implemented functions

Implemented in `admin/v7-admin-api`:

- `selected_moves_read_adapter`
- `restore_settle_read_adapter`
- `hidden_movers_read_adapter`
- `target_readiness_read_adapter`
- `capacity_read_adapter`
- `required_services_read_adapter`
- `policy_read_adapter`
- `concurrency_read_adapter`
- `routing_mode_read_adapter`
- `containment_read_adapter`
- `group_constraints_read_adapter`
- `execution_gate_adapters_for_draft`
- `execution_gate_catalog_for_drafts`

## Adapter contract

Each adapter normalizes source truth into:

- gate id
- label
- status
- reason
- blocking flag
- source
- adapter_connected
- detail
- read-only/preview-only context

Allowed statuses:

- PASS
- FAIL
- REVIEW_REQUIRED
- UNKNOWN

## Safety

Adapters only read existing state and normalize it. They do not run commands, do not call runtime mutation paths, do not move users, do not change routing, and do not apply autoswitch.
