# E35.D Authority Store

## Decision

Use a hybrid:

```text
STATE_DIR/routing-authority.json
STATE_DIR/routing-authority-events.jsonl
```

Current state:

- JSON document.

History/audit:

- append-only JSONL.

## Why Not Registry

`users.registry` must remain current runtime state.

Authority is intent and permission. Mixing authority into registry would blur:

```text
where user is
vs
who may move user
```

## Why Not SQLite First

SQLite is useful later for complex queries, but current V7 operational pattern already uses JSONL for Evidence, Proposal, Runtime Trust and Release Trust. Authority should start with the same low-risk operational shape.

## Single Source Of Truth

Current authority truth:

```text
routing-authority.json
```

Authority history:

```text
routing-authority-events.jsonl
```

Read models may cache/derive but must never become authority truth.

## Recovery

Recovery order:

1. Load current state JSON.
2. Validate schema/version.
3. If state unreadable, fail closed to REVIEW_REQUIRED.
4. Use events only for audit/timeline, not automatic reconstruction unless explicit repair mode exists.

## Admin Surface

Admin never shows raw store first. It shows read models.

## API Contract

Read APIs expose redacted/effective state.

No write APIs in E35.D.

## Tests

- unreadable store fails closed;
- duplicate user entry rejected;
- JSON schema validates;
- event append does not mutate route;
- read model does not become source of truth.

## Verdict

```text
authority_store_defined=true
storage_backend=json_plus_jsonl
```
