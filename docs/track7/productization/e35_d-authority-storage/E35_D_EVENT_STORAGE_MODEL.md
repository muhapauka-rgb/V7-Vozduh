# E35.D Event Storage Model

## Product Meaning

Events explain what happened to authority decisions, conflicts, reviews and emergencies.

## Storage Format

Append-only JSONL:

```text
STATE_DIR/routing-authority-events.jsonl
```

## Event Types

Reuse E35.C event types:

- `VERDICT_CREATED`
- `VERDICT_DENIED`
- `VERDICT_ALLOWED`
- `VERDICT_REVIEW_REQUIRED`
- `VERDICT_EMERGENCY`
- `CONFLICT_DETECTED`
- `CONFLICT_RESOLVED`
- `REVIEW_CREATED`
- `REVIEW_CLOSED`
- `EMERGENCY_CREATED`
- `EMERGENCY_EXPIRED`
- `AUTHORITY_STATE_CHANGED`

## Indexes

JSONL has no physical index initially. Read adapter should build in-memory indexes by:

- `event_id`;
- `user_ip`;
- `current_channel`;
- `target_channel`;
- `event_type`;
- `verdict`;
- `conflict_id`;
- `review_id`;
- `emergency_id`;
- `created_at`.

If event volume grows, migrate indexes to SQLite while preserving JSONL as audit archive.

## Linkage Rules

Events may link to:

- evidence bundle;
- proposal;
- governance packet;
- runtime trust record;
- release trust record;
- authority state hash.

## Retention

- verdict events: active 90 days;
- conflicts/reviews/emergencies: active 180 days;
- authority state changes: active 365 days;
- archive compressed after active window.

## Audit Rules

Every event must include:

- schema version;
- event id;
- timestamp;
- actor;
- action type;
- user/channel when applicable;
- mutation flags false for E35.D read model.

## Tests

- append-only ordering;
- event id uniqueness;
- event redaction;
- timeline adapter sorts by timestamp;
- archive rules do not remove active unresolved reviews/emergencies.

## Verdict

```text
event_storage_defined=true
```
