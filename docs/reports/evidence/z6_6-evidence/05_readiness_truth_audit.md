# Orchestrator Readiness Impact and Truth Audit

## Existing Operation Model Coverage

Estimated operation model already exists: 55%.

Already exists:

- `operation_id` in operator observability and operator execution packets;
- proposal IDs and proposal linkage;
- execution contract IDs and status/event vocabulary;
- approval IDs, packet IDs, replay detection, and audit-chain hashes;
- selected-move hash and planner generation in autoswitch;
- runtime snapshot hashes in operator recheck;
- restore-barrier generation/hash/count/token fields;
- audit event linkage fields in `v7-audit-log`;
- Admin closure object keys and closure records;
- historical operation summaries and evidence refs.

Requires ownership wiring only:

- attach autoswitch runtime cycles to canonical `operation_id`;
- carry operation identity into audit event linkage;
- carry operation identity into closure object key;
- link selected-move hash/count and generation into operation timeline;
- link rollback result to operation timeline;
- represent no-op decisions as operation terminal facts when recorded.

Requires future implementation:

- any concrete event emission;
- any concrete operation ID generation logic;
- any storage/API representation;
- any runtime wiring;
- any closure/audit enforcement.

Requires no work:

- primary runtime owner selection;
- scheduler ownership;
- audit sink ownership;
- closure owner selection;
- low-level primitive classification.

## Truth Source Audit

No duplicate operation truth:

- Runtime Operation is a semantic envelope over existing facts. It does not create a new source of truth in Z6.6.

No duplicate operation identity:

- `operation_id` is selected as canonical semantic identity because it already exists. `proposal_id`, `contract_id`, `approval_id`, selected-move hash, and closure key remain lineage IDs.

No duplicate audit identity:

- `v7-audit-log` remains canonical audit sink. Audit event linkage should reference `operation_id` through existing object/request/metadata fields in future wiring.

No duplicate closure identity:

- closure identity remains Admin closure key. For Runtime Operations, the closure object should semantically be keyed by operation identity, but this report does not define storage/API.

No duplicate rollback identity:

- rollback remains linked to operation identity and rollback scope/result; no separate rollback truth is created.

No duplicate lineage identity:

- lineage is the set of existing IDs attached to operation identity; it is not a new competing identity.

## Identity Boundary

Canonical:

- `operation_id`

Lineage:

- `proposal_id`
- `contract_id`
- `approval_id`
- `packet_id`
- `event_id`
- `record_hash`
- `selected_move_hash`
- `planner_generation_id`
- `runtime_snapshot_hash`
- restore-barrier generation/hash/token fields
- closure key
- evidence IDs

Never canonical operation identity:

- selected-move hash alone;
- proposal_id alone;
- approval_id alone;
- audit event alone;
- closure key alone;
- barrier generation alone.

