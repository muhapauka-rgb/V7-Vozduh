# E35.B User Rights Model

## Product Position

V7 philosophy:

```text
Operator manages complexity.
User consumes stable internet.
```

Users currently do not manage routing.

## User Rights Decision

| Question | Decision |
|---|---|
| Should users have routing rights? | No, not direct movement rights. |
| Should users influence routing? | Yes, through needs/preferences captured by operator or future safe request flow. |
| Should users select required services only? | Not directly in current admin model; operator may configure required services for user/group. |
| Should users request pinning? | Future request-only, not authority. |
| Should users see authority state? | Not in current admin; future user-facing view may show simple status, not controls. |

## User Domain Scope

User can influence:

- required services;
- service problems/feedback;
- future route request;
- future "need stable service X" signal.

User cannot:

- move self;
- pin self;
- override group;
- override operator;
- override safety;
- override governance.

## Admin Surface

Users drawer should show:

- required services;
- authority owner;
- whether user-originated request exists;
- operator-managed status.

## Runtime Mapping

User input becomes evidence/proposal input only.

It never directly calls movement.

## Storage Impact

Future user requests should be stored as:

- request;
- evidence;
- proposal input;
- not authority.

## API Impact

Future APIs can accept request/feedback, but must not mutate routing.

## Tests

- user request creates proposal/evidence only;
- user request cannot move channel;
- operator must approve or reject.

## Verdict

```text
user_rights_model_defined=true
```
