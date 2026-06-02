# P2.1 Execution Contract Store

## Store

Path:
`STATE_DIR/execution-contracts.json`

Environment override:
`V7_EXECUTION_CONTRACTS_FILE`

Supported shapes:

- JSON array of contract objects.
- Object with `contracts`.
- Object with `items`.
- Object keyed by contract id.

## Contract Fields

Normalized fields:

- `contract_id`
- `contract_version`
- `status`
- `action_type`
- `autonomy_level`
- `allowed_users`
- `allowed_targets`
- `affected_users`
- `target`
- `authority_references`
- `proposal_references`
- `evidence_references`
- `validation_state`
- `verification_state`
- `rollback_state`
- `rollback_manifest`
- `movement_budget`
- `blast_radius`
- `created_at`
- `updated_at`
- `expires_at`
- `replay_nonce`
- `consumed_at`
- `summary`

Safety fields always set:

- `read_only=true`
- `non_authoritative=true`
- `execution_allowed_now=false`

## Supported Statuses

`DRAFT`, `PRECHECKED`, `APPROVED`, `SCHEDULED`, `VALIDATED`, `RECHECKED`, `EXECUTING`, `VERIFYING`, `OBSERVING`, `ROLLBACK_READY`, `ROLLING_BACK`, `COMPLETED`, `FAILED_CLOSED`, `ROLLED_BACK`, `REPLAY_DENIED`, `CANCELLED`, `EXPIRED`.

Unknown statuses fail down to `DRAFT`.

## Verdict

contract_store_implemented=true
contract_store_read_only=true
runtime_mutation_performed=false
