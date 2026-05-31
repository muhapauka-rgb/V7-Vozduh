# E35.D Audit Model

## Questions Authority Audit Must Answer

- Who changed mode?
- Who created pin?
- Who removed pin?
- Why?
- When?
- What evidence?
- What proposal?
- What governance packet?
- What containment event?

## Audit Event Requirements

Every authority state change must include:

- actor;
- action;
- previous state;
- next state;
- reason;
- evidence/proposal/governance links;
- timestamp;
- mutation flags;
- source hash.

## Audit Links

Authority events may link to:

- Evidence bundle;
- Proposal;
- approval packet;
- operator execution audit record;
- runtime trust record;
- release trust record;
- containment event.

## Admin Surface

Logs:

- filter by authority event;
- filter by user;
- filter by actor;
- filter by review/emergency.

Users drawer:

- authority timeline.

## Tests

- state change without event is invalid;
- event without actor is invalid;
- event without reason is invalid for operator action;
- mutation flags remain false for read-only E35.D.

## Verdict

```text
audit_model_defined=true
```
