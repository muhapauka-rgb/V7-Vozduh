# P2.5 Log Retention Architecture

## Result

log_retention_architecture_defined=true

## Audit Scope

Execution-related logging includes:

- Execution Events;
- Validation Events;
- Verification Events;
- Rollback Events;
- Readiness Events;
- Authority Events;
- Simulation Events;
- Preview Events;
- JSONL stores;
- Audit stores.

## Persisted vs Derived

Persisted:

- execution contracts;
- execution events;
- authority state;
- authority events;
- audit events;
- evidence and proposal stores.

Derived:

- validation preview;
- readiness explain;
- outcome preview;
- blast radius;
- service impact;
- readiness forecast;
- rollback impact;
- simulation events in P2.5.

## Retention Requirements

- No infinite JSONL growth.
- No infinite event growth.
- Unresolved reviews survive cleanup.
- Active emergencies survive cleanup.
- Latest authority state survives cleanup.
- Audit lineage remains provable.

## Proposed Retention Design

1. Keep latest authority state indefinitely.
2. Keep active execution contracts and unresolved review lineage indefinitely.
3. Rotate JSONL event stores by size and age.
4. Compact resolved preview events into daily summary records.
5. Archive raw resolved event segments with hash manifests.
6. Preserve evidence/proposal hashes referenced by any active or unresolved workflow.
7. Expose summary views for old resolved events instead of loading unbounded JSONL tails.

## Safe Cleanup Rules

Cleanup must fail closed if:

- authority state cannot be read;
- unresolved review records are present but not indexed;
- active emergency is detected;
- an archive hash manifest cannot be written or verified;
- compacted summary cannot prove original event range.

## Boundary

P2.5 defines this architecture only. It does not implement cleanup, rotation, compaction, deletion, or archive writes.
