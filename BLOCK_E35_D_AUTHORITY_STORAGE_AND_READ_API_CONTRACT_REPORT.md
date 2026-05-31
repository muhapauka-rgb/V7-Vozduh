# BLOCK E35.D Authority Storage And Read API Contract Report

## 1. Storage Discovery

E35.D audited existing stores:

- Evidence Store;
- Proposal Store;
- Runtime Trust Store;
- Release Trust Store;
- Audit Logs;
- Switch Logs;
- JSONL Stores;
- Identity DB;
- Users Registry;
- Egress Registry;
- Operator Execution Records;
- Approval Packet Records;
- Existing Admin Data Adapters.

Decision:

Authority must not be stored in `users.registry`, `egress.registry`, Evidence, Proposal or Trust stores.

## 2. Authority State Model

Authority state records:

- routing mode;
- owner;
- source;
- status;
- reason;
- preferred/pinned target;
- expiry;
- pin/manual/containment metadata.

It does not duplicate current runtime route.

## 3. Authority Store

Recommended storage:

```text
STATE_DIR/routing-authority.json
STATE_DIR/routing-authority-events.jsonl
```

Current authority truth is JSON.

History is append-only JSONL.

## 4. Event Storage

Event storage uses append-only JSONL and reuses E35.C event taxonomy.

Active retention:

- verdicts: 90 days;
- conflicts/reviews/emergencies: 180 days;
- authority state changes: 365 days.

## 5. Read Models

Defined:

- Authority Summary;
- Authority Timeline;
- Conflict Summary;
- Conflict Detail;
- Review Queue;
- Emergency Queue;
- Authority Health;
- Authority Explanation.

## 6. Admin View Models

Use existing `/admin-v2`:

- Home: summary/pending/emergency/drift;
- Users: routing mode, owner, pin, conflict, timeline;
- Channels: pinned users, conflicts, emergency usage;
- Checks: authority/evaluator health;
- Logs: events/reviews/conflicts/emergency actions.

## 7. Read API Contract

READ APIs only:

- `GET /api/authority/summary`
- `GET /api/authority/user/{id}`
- `GET /api/authority/conflicts`
- `GET /api/authority/reviews`
- `GET /api/authority/emergency`
- `GET /api/authority/timeline`
- `GET /api/authority/explain`

## 8. Data Adapters

Adapters map:

- State -> Effective Authority;
- Events -> Timeline;
- Conflicts -> Queue;
- Reviews -> Queue;
- Emergency -> Queue;
- Registries -> Runtime Context;
- Evidence/Proposal/Trust -> Links.

## 9. Audit Model

Authority audit must answer:

- who changed mode;
- who created or removed pin;
- why;
- when;
- what evidence/proposal/governance/containment object was involved.

## 10. Retention Model

Rules:

- never delete unresolved review;
- never delete active emergency;
- never delete latest authority state;
- archive before cleanup;
- cleanup never changes routing.

## 11. Runtime Readiness

Future read integrations:

- autoswitch;
- manual switch;
- governed execution;
- containment;
- scheduler;
- evaluator;
- conflict resolver.

If authority store is unreadable, future forward movement must fail closed.

## 12. Implementation Readiness

Recommended implementation order:

1. Authority Store.
2. Event Store.
3. Read Models.
4. Data Adapters.
5. Read APIs.
6. Admin Visibility.
7. Runtime Readers.
8. Future Write Paths.

## 13. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Authority duplicated into registry | High | Dedicated authority store, registries remain runtime truth. |
| Event log grows too large | Medium | Retention/archive rules, future SQLite indexes. |
| Admin reads raw storage | Medium | Read models only. |
| Store unreadable causes unsafe allow | High | Fail closed to DEGRADED/REVIEW_REQUIRED. |
| Evidence/Proposal mistaken for authority | High | Link only, never truth source. |

## 14. Recommendations For E35.E

Recommended next block:

```text
E35.E_AUTHORITY_READ_MODEL_AND_EVALUATOR_PREVIEW_IMPLEMENTATION_PLAN
```

Focus:

- implement read-only authority state;
- implement event reader;
- implement read APIs;
- implement admin visibility;
- add evaluator preview using read models;
- no autonomous execution yet.

## Required Verdicts

```text
authority_state_model_defined=true
authority_store_defined=true
event_storage_defined=true
read_models_defined=true
admin_view_models_defined=true
read_api_contract_defined=true
audit_model_defined=true
retention_model_defined=true
runtime_readiness_defined=true
implementation_ready=true
e35_e_ready=true
```

## Safety Verdict

```text
runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_changed=false
```
