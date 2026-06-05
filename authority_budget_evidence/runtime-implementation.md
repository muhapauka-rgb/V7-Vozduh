# Runtime Implementation

Implemented in:

- `tools/v7-users-autoswitch`

Runtime evidence path:

- `plan.safety.authority_budget_gate`

Runtime behavior:

- default `CANARY` budget is `1`;
- prepared `SMALL_BATCH` budget is `2`;
- class ceilings are enforced even when policy attempts a higher budget;
- disabling the gate fails closed to zero selected moves;
- gate runs before restore barrier, snapshot gate, and apply.

Performance boundary:

- no network calls;
- no history scans;
- no per-user external scans;
- no new snapshot root;
- no new truth source;
- in-memory cap over already selected moves.

