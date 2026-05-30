# E34.G Progressive Disclosure Model

progressive_disclosure_defined=true
complexity_hidden_by_default=true

## Disclosure Levels

| Level | Default visibility | Examples |
| --- | --- | --- |
| Summary | Always visible | Status, affected users, degraded channels, next action. |
| Explanation | On click / drawer | Why blocked, why proposed, which evidence matters. |
| Operational detail | Workspace panel / result panel | Preview result, impact, rollback, verification. |
| Expert diagnostics | Explicit expert drawer / logs | Raw JSON, packet IDs, lock IDs, manifests, command output. |

## Hidden By Default

Hide:

- capacity class internals;
- batch lifecycle state machine;
- policy rule graph;
- scheduler queue internals;
- lock/reservation IDs;
- release manifest internals;
- backup archive internals;
- installer shell command output;
- raw JSON payloads.

## Shown By Default

Show:

- status;
- impact;
- affected users/channels/routes;
- reason;
- confidence;
- blocker;
- next safe action;
- preview/apply distinction;
- rollback availability;
- audit result.

## Expert Mode Rule

Expert diagnostics may expose internal details, but only after the operator has already seen the plain-language summary and safety boundary.
