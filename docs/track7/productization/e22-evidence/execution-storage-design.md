# E22 Execution Storage Design

## Store Path

store_path=docs/track7/productization/e22-evidence/operator-execution-audit.jsonl
store_type=append_only_jsonl
runtime_state_directory_mutation=false
database_migration=false

The E22 audit store is intentionally repo-local evidence storage for the first
governance transition. It does not write to `/opt/v7`, does not alter runtime
registries, and does not create a production DB migration.

## Record Format

Each line is one canonical JSON object:

- schema_version;
- record_type;
- approval_id;
- packet_id;
- operation_id;
- selected_first_action;
- runtime_action;
- verdict;
- errors;
- checks;
- created_at;
- previous_record_hash;
- record_hash;
- runtime_mutation=false;
- user_movement=false;
- routing_mutation=false.

## Append-Only Semantics

Records are appended with `O_APPEND`. Each record includes the previous record
hash, producing a tamper-evident chain.

## Replay Detection

Any existing record with the same `approval_id` causes `DENY_REPLAY` and appends
a denial record.

## Denial Records

Denials are first-class audit records. They preserve the same chain semantics as
approval records.

## Path Safety

The CLI resolves packet and audit-store paths under the repository root. Paths
outside the repo are denied.

## Secret Safety

Records are passed through the shared redaction helper before append.

## Storage Verdict

execution_storage_design_complete=true
approval_audit_store_implemented=true
append_only_semantics_implemented=true
runtime_mutation_surface_present=false
