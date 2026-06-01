# Z7.1 Evidence 03 - Audit and Closure Wiring

## Operation to Audit Wiring

### Connected

`tools/runtime-support/v7-audit-log` writes canonical audit events with:

- `schema_version`
- `ts`
- `host`
- `actor`
- `severity`
- `action`
- `component`
- `message`
- `object_type`
- `object_id`
- `user_ip`
- `result`
- `request_id`
- `before_hash`
- `after_hash`
- `metadata`
- `pid`

Admin `audit_admin(...)` writes into the same audit model. Admin autoswitch dry-run/apply, closure-set, rollback-apply, and many Admin actions use the Admin audit wrapper.

Operator execution writes append-only governance audit records with:

- `operation_id`
- `approval_id`
- `packet_id`
- `record_hash`
- `recheck` facts

### Partial

`v7-audit-log` can carry `operation_id` through metadata because it preserves arbitrary metadata, but it does not expose `operation_id` as a first-class field.

Admin autoswitch guarded apply audits the Admin wrapper action, but the audit event does not include a canonical runtime `operation_id` from autoswitch.

Operator observability has an audit export preview keyed by `operation_id`, but that preview is historical/read-only and does not prove live autoswitch audit linkage.

### Missing

No observed live path:

```text
tools/v7-users-autoswitch terminal result
  -> v7-audit-log with operation_id
```

## Operation to Closure Wiring

### Connected

Admin closure model exists:

- `CLOSURE_STORE_FILE`
- `closure_records()`
- `closure_lookup()`
- `closure_for()`
- `attach_operational_metadata()`
- `closure_set_response()`
- `/api/actions/closure-set`

Supported closure object types:

- `evidence`
- `proposal`
- `runtime`
- `release`
- `trust`
- `drift`

Closure states:

- `OPEN`
- `VERIFIED`
- `CLOSED`
- `EXPIRED`

Closure-set appends JSONL closure records and writes Admin audit.

### Partial

`runtime` is a valid closure object type, so a runtime operation can be represented if a stable runtime object id exists.

Operator observability can present historical operations and evidence references by `operation_id`.

### Missing

No observed live autoswitch path:

```text
autoswitch operation_id
  -> Admin closure object_id
  -> closure record
```

Closure currently attaches to Admin/evidence/proposal/runtime object ids supplied by callers, not to an autoswitch-emitted operation id.

## Audit and Closure Verdict

Audit and closure mechanisms are real and reusable. The missing part is not the sink/store; it is the live operation identity bridge from autoswitch runtime result into audit and closure.

