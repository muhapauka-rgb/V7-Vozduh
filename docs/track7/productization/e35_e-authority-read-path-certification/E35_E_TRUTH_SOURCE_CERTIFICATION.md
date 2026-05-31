# E35.E Truth Source Certification

## Single Source Of Truth

Authority truth:

```text
STATE_DIR/routing-authority.json
```

Authority history/audit:

```text
STATE_DIR/routing-authority-events.jsonl
```

Runtime route truth:

```text
users.registry
```

Channel identity truth:

```text
egress.registry
```

## Classification

| Component | Truth Level |
|---|---|
| Authority Store | Authoritative for authority state |
| Authority Events | Authoritative for authority history/audit |
| Read Models | Derived |
| Admin Models | Presentation |
| API Responses | Derived/presentation transport |
| Evaluator Context | Derived decision input |
| Conflict Resolver Context | Derived decision input |
| Evidence | Link/reference only |
| Proposal | Link/reference only |
| Runtime Trust | Input truth for trust state |
| Release Trust | Input truth for release state |

## Certification Rules

- Read models must not invent authority state.
- APIs must not override read models.
- Admin must not infer authority from labels alone.
- Evaluator and conflict resolver must consume the same normalized context.
- Any mismatch becomes read-path drift.

## Verdict

```text
single_truth_source_defined=true
```
