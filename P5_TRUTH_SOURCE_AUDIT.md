# P5 Truth Source Audit

## Canonical Truth Sources

P5 requires current, fresh truth sources for the first runtime action.

Expected truth sources:

- action packet: canonical requested action, actor, approval id, source hashes, and expected no-op movement proof
- runtime state: canonical live state under `/opt/v7/egress/state`
- approval record: canonical approval evidence for exactly one packet
- audit store: canonical append-only action and denial records
- governance store: canonical append-only zero-move governance transition record

## Runtime Truth Source Check

Checked path:

`/opt/v7/egress/state`

Result:

`No such file or directory`

Fresh source hashes cannot be produced.

Fresh selected-move count cannot be proven.

Fresh no-user-movement evidence cannot be proven from live state.

## Stale Evidence Handling

Repository fixtures and previous reports were treated as non-authoritative for P5 runtime execution.

They can explain expected behavior, but cannot authorize a real runtime action.

## Conflict Decision

No competing truth source was promoted.

The block stops because the canonical runtime truth source is missing.

## Verdicts

- truth_source_audit_complete=true
- truth_sources_clean=false
- canonical_runtime_truth_source_available=false
- stale_values_reused=false
- action_may_proceed=false
- abort_reason=FRESH_RUNTIME_STATE_MISSING
